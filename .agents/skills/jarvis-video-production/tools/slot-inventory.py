#!/usr/bin/env python3
"""slot-inventory.py — for one format, what has been FILLED and is the inventory exhausting?

TOOL CONTRACT
  SUBSYSTEM  D (Demand). Third leg of the discovery layer.
             channel-template.py (discover) -> format-index.py (catalogue) ->
             bend-map.py (which MARKETS are free) -> THIS (which SLOTS are free)
  STATE      writes slot_inventory into ratchet/formats.json · ratchet/slots-<fmt>-<date>.csv
  GATE       none. Emits the filled inventory plus exhaustion signals.
  COST       one vidiq_youtube_search per time slice (5 credits each, default 6 = 30)

    slot-inventory.py --format economics-of-owning-a --dry-run
    slot-inventory.py --format economics-of-owning-a
    slot-inventory.py --list

WHY THIS EXISTS -- bend-map asked the wrong question for this kind of format
  bend-map.py walks a format across MARKETS. Run on "The Economics of Owning a {X}" it returned
  free_ratio 44% and reported eight FREE cells in Terry's strong markets: information systems,
  higher education, software engineering, AI. Those are not opportunities. They are empty
  because "The Economics of Owning a Higher Education" is not a video -- the format requires a
  BUSINESS YOU CAN OWN, so the free cells are precisely the markets where the format does not
  apply. The market axis was answering a question this format does not pose.

  The question it does pose is SLOT INVENTORY: the format lives in one market (small business)
  and its content supply is the list of fillable anchors -- gas station, gym, movie theater,
  car wash, laundromat. That list is the asset. "A template used once is just a title";
  ExtraMint's asset was fourteen FILLED SLOTS, not one title
  (YOUTUBE-DEMAND-RESEARCH-2026-08-09.md §4).

WHAT CAN AND CANNOT BE MEASURED -- read this before believing any number below
  FILLED is measurable: enumerate the frame, extract each video's anchor, dedupe. That is a
      census of what exists, bounded only by search coverage.
  OPEN is NOT measurable. Knowing that "laundromat" is an unfilled slot requires knowing the
      universe of ownable small businesses, which is domain knowledge, not a search result.
      This tool therefore NEVER prints a list of open slots. Inventing one would be exactly the
      confident-false-positive failure the demand layer keeps catching.

  What it measures instead is whether the inventory is EXHAUSTING, which is the decision the
  open list would have been used for anyway:
      SLOT DECAY      median views of early-filled slots vs late-filled ones. If the newest
                      anchors underperform the oldest, the good slots are gone.
      CONTESTED SHARE anchors filled by 2+ distinct channels. A contested anchor is a slot
                      someone already re-ran; a high share means the obvious list is worked out.
      CONCENTRATION   share of total views held by the top 5 anchors. High concentration means
                      a few slots carry the format and the tail does not pay.
      UNCONTESTED WINNERS  anchors with ONE channel and above-median views. These are the
                      MODEL for what an open slot looks like -- the closest the data comes to
                      pointing at the gap without inventing it.

CONFOUNDS
  ANCHOR EXTRACTION IS STRING SURGERY. The anchor is whatever survives removing the template
      tokens, so "a Gas Station in 2024" and "a Gas Station" are two anchors unless normalised.
      Normalisation is deliberately shallow (case, articles, punctuation, trailing years) --
      aggressive stemming would merge genuinely different slots.
  SEARCH COVERAGE IS NOT A CENSUS. Time-slicing widens it well beyond a single 50-cap call, but
      an anchor absent here may exist and simply not rank. Absence is weak evidence; the
      CONTESTED and DECAY signals lean on what IS present and are the more trustworthy outputs.
  LIFETIME VIEWS FAVOUR OLD SLOTS. Slot decay is measured against publish order, so an old
      anchor has had longer to accumulate -- which BIASES TOWARD FINDING DECAY. Read a decay
      signal as an upper bound on how exhausted the inventory is, never a lower one.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import statistics as st
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

TOOLS   = Path(__file__).resolve().parent
RATCHET = TOOLS / "ratchet"
INDEX   = RATCHET / "formats.json"
URL      = "https://mcp.vidiq.com/mcp"
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
_SESSION = {}

SLICES           = 6      # time windows to probe; each is one 50-cap call
SLICE_YEARS      = 4      # total span covered by the slices
PROBE_LIMIT      = 50
CREDITS_PER_CALL = 5
MIN_ANCHOR_CHARS = 3
TOP_CONC         = 5      # anchors counted in the concentration figure

STOP_EDGE = re.compile(r"^(a|an|the|of|in|on|for|and|is|was|to)\b\s*|\s*\b(a|an|the|of|in|on|for|and)$",
                       re.I)


def api_key():
    k = os.environ.get("VIDIQ_API_KEY")
    if k:
        return k
    try:
        for line in open(ENV_PATH):
            if re.match(r"\s*VIDIQ_API_KEY\s*=", line):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    sys.exit("No VIDIQ_API_KEY (env or jarvis/.env).")


def _rpc(method, params=None, notify=False):
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notify:
        body["id"] = 1
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {api_key()}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if "id" in _SESSION:
        req.add_header("Mcp-Session-Id", _SESSION["id"])
    try:
        r = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode()[:400]}
    sid = r.headers.get("Mcp-Session-Id")
    if sid:
        _SESSION["id"] = sid
    raw = r.read().decode()
    if not raw.strip():
        return {}
    if raw.lstrip().startswith("event:") or "\ndata:" in raw or raw.startswith("data:"):
        for line in raw.splitlines():
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
        return {}
    return json.loads(raw)


def call_tool(name, args):
    if "id" not in _SESSION:
        _rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                            "clientInfo": {"name": "slot-inventory", "version": "1"}})
        _rpc("notifications/initialized", notify=True)
    res = _rpc("tools/call", {"name": name, "arguments": args})
    if "_http_error" in res:
        sys.exit(f"vidIQ HTTP {res['_http_error']}: {res['_body']}")
    for b in (res.get("result") or {}).get("content") or []:
        if b.get("type") == "text":
            try:
                return json.loads(b["text"])
            except json.JSONDecodeError:
                return {}
    return {}


def frame_phrase(fmt):
    tpl = fmt.get("title_template") or fmt["name"]
    return re.sub(r"\s+", " ", re.sub(r"\{[A-Z]+\}", " ", tpl)).strip()


def anchor_of(title, fmt):
    """Strip the template out of a title; what is left is the slot that was filled."""
    t = title
    t = re.sub(fmt["title_regex"], " ", t, flags=re.I)
    t = re.sub(r"[|:\-–—#()\[\]\"'?!.]+", " ", t)
    t = re.sub(r"\b(19|20)\d{2}\b", " ", t)          # trailing years are not different slots
    t = re.sub(r"\s+", " ", t).strip()
    prev = None
    while prev != t:                                   # shallow normalisation only -- see CONFOUNDS
        prev = t
        t = STOP_EDGE.sub("", t).strip()
    return t.lower()


def enumerate_slots(fmt, a):
    phrase = frame_phrase(fmt)
    today = dt.date.today()
    span = int(SLICE_YEARS * 365 / a.slices)
    pool, seen = [], set()
    for i in range(a.slices):
        hi = today - dt.timedelta(days=span * i)
        lo = today - dt.timedelta(days=span * (i + 1))
        res = call_tool("vidiq_youtube_search", {
            "query": phrase, "type": ["video"], "order": "viewCount", "limit": PROBE_LIMIT,
            "regionCode": a.region,
            "publishedAfter": f"{lo.isoformat()}T00:00:00Z",
            "publishedBefore": f"{hi.isoformat()}T00:00:00Z"})
        got = res.get("results") or []
        new = 0
        for v in got:
            if v.get("id") and v["id"] not in seen:
                seen.add(v["id"])
                pool.append(v)
                new += 1
        print(f"  {lo} → {hi}   {len(got):>2} results, {new:>2} new")
    return phrase, pool


ISO_DUR = re.compile(r"P(?:\d+D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def duration_min(iso):
    m = ISO_DUR.match(iso or "")
    if not m:
        return 0
    h, mi, sec = (int(x) if x else 0 for x in m.groups())
    return h * 60 + mi + sec / 60


def coherent(fmt, matches):
    r"""Is this regex matching a FORMAT, or ordinary English?

    PORTED FROM bend-map.py 2026-08-10 after this tool shipped without it and immediately
    produced a 97-slot "inventory" for `\bbusiness\s+of\b` containing Diwali Shorts, Hindi
    serials and an Apple TV trailer. bend-map had the gate; this did not; the same two-token
    generic phrase sailed through. Any tool that matches titles by regex needs this check --
    it is not a bend-map feature, it is a property of regex-matching titles.
    """
    if not matches:
        return True
    durs = [duration_min(v.get("duration")) for v in matches]
    shorts = sum(1 for d in durs if d < 1.5) / len(durs)
    band = fmt.get("runtime_min") or [0, 0]
    in_band = sum(1 for d in durs if band[0] * 0.5 <= d <= max(band[1] * 2, 3)) / len(durs)
    if shorts > 0.30 or in_band < 0.40:
        print(f"\n⚠ INCOHERENT FRAME — {shorts:.0%} of matches are Shorts, {in_band:.0%} sit "
              f"near the declared {band[0]}-{band[1]}m runtime.")
        print("  This regex is matching ORDINARY ENGLISH. An inventory built on it is noise;\n"
              "  tighten title_regex until the matches are one recognisable shape.")
        for v in matches[:5]:
            print(f"    · {duration_min(v.get('duration')):>5.1f}m  {(v.get('title') or '')[:62]}")
        return False
    return True


def build(fmt, pool):
    matches = [v for v in pool if re.search(fmt["title_regex"], v.get("title") or "", re.I)]
    slots = defaultdict(list)
    for v in matches:
        an = anchor_of(v.get("title") or "", fmt)
        if len(an) >= MIN_ANCHOR_CHARS:
            slots[an].append(v)
    rows = []
    for an, vids in slots.items():
        chans = {v.get("channelId") for v in vids}
        rows.append({
            "anchor": an, "n_videos": len(vids), "n_channels": len(chans),
            "contested": len(chans) > 1,
            "median_views": int(st.median([v.get("viewCount") or 0 for v in vids])),
            "best_views": max(v.get("viewCount") or 0 for v in vids),
            "first_seen": min((v.get("publishedAt") or "")[:10] for v in vids),
            "last_seen": max((v.get("publishedAt") or "")[:10] for v in vids),
            "best_title": max(vids, key=lambda v: v.get("viewCount") or 0).get("title"),
            "best_channel": max(vids, key=lambda v: v.get("viewCount") or 0).get("channelTitle"),
        })
    rows.sort(key=lambda r: -r["median_views"])
    return matches, rows


def report(fmt, matches, rows, a):
    if not rows:
        print("\nNO SLOTS EXTRACTED. Either the regex matched nothing or every anchor was "
              "empty.\nThat is a tooling result, not an inventory finding.")
        return
    med_all = st.median([r["median_views"] for r in rows])
    total = sum(r["median_views"] for r in rows)
    conc = sum(r["median_views"] for r in rows[:TOP_CONC]) / total if total else 0
    contested = [r for r in rows if r["contested"]]

    # SLOT DECAY, biased toward finding decay by construction -- see CONFOUNDS.
    by_age = sorted(rows, key=lambda r: r["first_seen"])
    half = max(1, len(by_age) // 2)
    early = st.median([r["median_views"] for r in by_age[:half]])
    late = st.median([r["median_views"] for r in by_age[half:]])
    decay = round(early / late, 2) if late else None

    print(f"\n{'='*94}\nSLOT INVENTORY  {fmt['format_id']}")
    print(f"  authority={fmt.get('authority')}  runtime={fmt.get('runtime_min')}  "
          f"{len(matches)} matching videos -> {len(rows)} distinct slots\n")
    print(f"  filled slots       {len(rows)}")
    print(f"  contested          {len(contested)} ({len(contested)/len(rows):.0%}) — "
          f"anchors 2+ channels have both run")
    print(f"  concentration      top {TOP_CONC} anchors hold {conc:.0%} of pooled median views")
    print(f"  slot decay         {decay}x  (older half medians {int(early):,} vs newer "
          f"{int(late):,})" if decay else "  slot decay         n/a")
    # FILL RATE. The first live run measured 39 slots whose first_seen dates ALL fell inside a
    # four-month window -- a format in a land grab, not a mature one. Decay and contest share
    # both read "OPEN" and both missed it, because neither looks at the calendar. A slot count
    # is meaningless without the rate it was consumed at.
    firsts = sorted(r["first_seen"] for r in rows if r["first_seen"])
    age_days = (dt.date.today() - dt.date.fromisoformat(firsts[0])).days if firsts else 0
    months = max(age_days / 30.0, 0.5)
    fill_rate = len(rows) / months
    print(f"  format age         {age_days}d — first slot filled {firsts[0] if firsts else '?'}")
    print(f"  fill rate          {fill_rate:.1f} slots/month "
          + ("← LAND GRAB. The obvious anchors are being taken now."
             if fill_rate >= 4 else "steady" if fill_rate >= 1 else "dormant"))

    verdict = ("EXHAUSTING — newer slots underperform and the obvious anchors are contested"
               if (decay or 0) > 2 and len(contested) / len(rows) > 0.25 else
               "OPEN — newer slots still perform and most anchors are uncontested"
               if (decay or 0) < 1.5 and len(contested) / len(rows) < 0.25 else
               "MIXED — read the rows")
    if fill_rate >= 4 and age_days < 240:
        verdict = (f"LAND GRAB — {len(rows)} slots consumed in {age_days} days. Uncontested "
                   f"today because\n        nobody has had TIME to contest them, not because "
                   f"the inventory is deep.\n        Decay and contest-share are both "
                   f"misleading this early; read the fill rate.")
    print(f"\n  READ: {verdict}")

    print(f"\n  FILLED INVENTORY (top {min(len(rows), a.top)} by median views)")
    print(f"  {'med views':>10} {'ch':>3} {'c':>2}  {'first':>10}  anchor")
    print("  " + "-" * 88)
    for r in rows[: a.top]:
        print(f"  {r['median_views']:>10,} {r['n_channels']:>3} "
              f"{'!' if r['contested'] else ' ':>2}  {r['first_seen']:>10}  {r['anchor'][:52]}")

    solo = [r for r in rows if not r["contested"] and r["median_views"] >= med_all]
    print(f"\n  UNCONTESTED WINNERS — {len(solo)} anchors, one channel each, at or above the "
          f"slot median.\n  These are the MODEL for an open slot. The tool does not invent the "
          f"open list (see\n  WHAT CAN AND CANNOT BE MEASURED); domain knowledge supplies it.")
    for r in solo[:10]:
        print(f"    {r['median_views']:>9,}  {r['anchor'][:44]:<44} {str(r['best_channel'])[:22]}")


def do_list(idx):
    hit = False
    for fid, f in sorted(idx["formats"].items()):
        inv = f.get("slot_inventory")
        if not inv:
            continue
        hit = True
        print(f"{fid:32} {inv['filled']:>3} slots  {inv['contested_share']:>4.0%} contested  "
              f"decay {inv.get('decay')}x  measured {inv['measured']}")
    if not hit:
        print("no inventories measured. Run: slot-inventory.py --format <id>")


def main():
    p = argparse.ArgumentParser(description="Filled slot inventory + exhaustion signals.")
    p.add_argument("--format")
    p.add_argument("--list", action="store_true")
    p.add_argument("--slices", type=int, default=SLICES, help="time windows to probe")
    p.add_argument("--region", default="US")
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    if not INDEX.exists():
        sys.exit("no ratchet/formats.json — run format-index.py --seed")
    idx = json.loads(INDEX.read_text())
    if a.list:
        return do_list(idx)
    if not a.format:
        sys.exit("pass --format <id>, or --list")
    fmt = idx["formats"].get(a.format)
    if not fmt:
        sys.exit(f"unknown format '{a.format}'")
    if not fmt.get("title_regex"):
        sys.exit(f"'{a.format}' has no title_regex — a visual format has no slots to enumerate.")

    cost = a.slices * CREDITS_PER_CALL
    print(f"format  {a.format}   phrase \"{frame_phrase(fmt)}\"")
    print(f"probe   {a.slices} time slices over {SLICE_YEARS}y, region {a.region}   "
          f"cost {cost} credits (~${cost*0.00475:.2f})\n")
    if a.dry_run:
        print("--dry-run: nothing spent.")
        return

    phrase, pool = enumerate_slots(fmt, a)
    matches, rows = build(fmt, pool)
    if not coherent(fmt, matches):
        return
    report(fmt, matches, rows, a)
    if not rows:
        return

    contested = [r for r in rows if r["contested"]]
    by_age = sorted(rows, key=lambda r: r["first_seen"])
    half = max(1, len(by_age) // 2)
    early = st.median([r["median_views"] for r in by_age[:half]])
    late = st.median([r["median_views"] for r in by_age[half:]])
    fmt["slot_inventory"] = {
        "filled": len(rows),
        "contested_share": len(contested) / len(rows),
        "decay": round(early / late, 2) if late else None,
        "age_days": (dt.date.today() - dt.date.fromisoformat(
            min(r["first_seen"] for r in rows if r["first_seen"]))).days,
        "fill_rate_per_month": round(len(rows) / max(
            (dt.date.today() - dt.date.fromisoformat(
                min(r["first_seen"] for r in rows if r["first_seen"]))).days / 30.0, 0.5), 1),
        "measured": dt.date.today().isoformat(),
        "anchors": [r["anchor"] for r in rows[:60]],
    }
    fmt["refill_slots"] = len(rows)
    INDEX.write_text(json.dumps(idx, indent=1))

    RATCHET.mkdir(parents=True, exist_ok=True)
    out = RATCHET / f"slots-{a.format}-{dt.date.today().isoformat()}.csv"
    cols = ["anchor", "n_videos", "n_channels", "contested", "median_views", "best_views",
            "first_seen", "last_seen", "best_title", "best_channel"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
