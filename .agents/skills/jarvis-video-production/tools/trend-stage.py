#!/usr/bin/env python3
"""trend-stage.py — where in its life is this format? The timing gate the demand layer lacked.

TOOL CONTRACT
  SUBSYSTEM  D (Demand). The fourth leg, and the last missing axis.
             channel-template (discover) -> format-index (catalogue) -> bend-map (markets)
             -> slot-inventory (supply depth) -> THIS (timing)
  STATE      caches raw/trend/<key>.json · writes trend_stage into ratchet/formats.json
  GATE       none directly, but market-gate.py --trend-stage consumes the verdict and BLOCKS
             anything not at BREAKOUT.
  COST       one vidiq_youtube_search per bucket (5 credits each; default 9 = 45)

    trend-stage.py --format business-of-x --dry-run
    trend-stage.py --format business-of-x
    trend-stage.py --query "ancient humans" --months 24      # ad-hoc, no catalogue row needed

WHY THIS EXISTS
  Every other instrument here measures MAGNITUDE -- how big, how free, how deep. None measured
  WHERE IN ITS LIFE a format is, which is why probes kept returning "proven at 38x" with no way
  to tell a lane that is opening from one that is closing. The governing report names this our
  single most expensive blind spot.

  The five stages come from the practitioner corpus (25io2cyji1I) and the instruction attached
  to them is the whole point:

      VALIDATION -> BREAKOUT -> MOMENTUM -> PEAK -> DECLINE
                    ^^^^^^^^
      "The best time to enter is BREAKOUT: already validated by a competitor so you are not
       wasting time, but not peak stability yet, so there is still room for exponential growth."

  Our own research reached the same place from the other side: its chosen lane had an incumbent
  who had VACATED, and a 1,290-sub channel won in it afterwards. Timing beat size.

WHAT IS ACTUALLY MEASURED, AND WHICH NUMBER TO TRUST
  ENTRANT COUNT per period -- distinct channels publishing into the format, and how many are
      publishing into it for the FIRST time. This is the trustworthy series: it is a count of
      channels, so it is immune to the view-accumulation bias that corrupts everything else.
  MEDIAN VIEWS per period -- age-biased in a KNOWN DIRECTION. Older videos have had longer to
      accumulate, so old periods look better than they were. That bias works AGAINST detecting
      a decline, which means a measured fall in median views is CONSERVATIVE evidence and a
      measured rise is not. Read falls; discount rises.

  The classification leans on the interaction, because supply eating demand has a signature no
  single series shows: entrants still climbing WHILE median views fall.

      VALIDATION  <=2 channels ever, no sustained second mover
      BREAKOUT    entrants rising AND median views rising          <- the buy window
      MOMENTUM    entrants rising, median views flat
      PEAK        entrants rising, median views FALLING            <- supply is eating demand
      DECLINE     entrants falling and median views falling

CONFOUNDS -- read before acting on a verdict
  EACH BUCKET IS THE TOP 50 OF ITS PERIOD, NOT A SAMPLE OF IT. vidIQ caps a search at 50 and
      this orders by viewCount inside each time window. That is a CONSISTENT rule across
      buckets, which is what makes them comparable, but it is a ceiling: a period with 200
      entrants and a period with 60 can both report 50 videos. Entrant counts therefore
      UNDERSTATE crowding in hot periods -- so a rising entrant curve is, again, conservative.
  A SHORT WINDOW CANNOT SEE A CYCLE. Formats in the corpus ran 2-4 months end to end. With the
      default 2-month buckets such a format is 1-2 data points and is unclassifiable. Use
      --months 6 --buckets 12 for anything suspected to be fast-moving.
  NO COHERENCE GATE MEANS NO VERDICT. Same lesson bend-map and slot-inventory both learned the
      hard way: a regex matching ordinary English produces a beautiful, meaningless time
      series. The gate runs first here and refuses rather than reporting.
  THIS MEASURES A FORMAT, NOT A SUBJECT. "Is the format saturating" and "is this topic played
      out" are different questions. A BREAKOUT format can still contain a dead anchor.
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
CACHE   = TOOLS / "raw" / "trend"
URL      = "https://mcp.vidiq.com/mcp"
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
_SESSION = {}

BUCKETS          = 9
MONTHS           = 18
PROBE_LIMIT      = 50
CREDITS_PER_CALL = 5
FLAT_BAND        = 0.15   # |slope| under this reads as flat rather than rising/falling
VALIDATION_CHANS = 2

# Six, not five. The corpus's fifth stage is "peak STABILITY" -- a mature plateau -- and the
# first cut of this file collapsed that together with "supply eating demand" under one PEAK
# label. They are opposite situations: one is a format that has stopped growing and still pays,
# the other is a format whose payoff is actively falling as entrants pile in. Splitting them
# also removed a bug: flat entrants + flat views fell through to MOMENTUM, and business-of-x
# was reported as "the window is closing" when both of its slopes were ~0.03, i.e. nothing was
# moving at all.
VALIDATION, BREAKOUT, MOMENTUM, SATURATING, STABLE, DECLINE, UNCLASSIFIED, SPARSE = (
    "VALIDATION", "BREAKOUT", "MOMENTUM", "SATURATING", "STABLE", "DECLINE",
    "UNCLASSIFIED", "SPARSE")
MIN_VIDS_PER_BUCKET = 5   # below this a slope is fitted to noise -> SPARSE, no verdict


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
                            "clientInfo": {"name": "trend-stage", "version": "1"}})
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


ISO_DUR = re.compile(r"P(?:\d+D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def duration_min(iso):
    m = ISO_DUR.match(iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 60 + mi + s / 60


def coherent(rx, band, matches):
    r"""Refuse to emit a time series for a regex that matches ordinary English.

    Third tool to carry this check. bend-map learned it, slot-inventory shipped without it and
    produced a 97-slot inventory of Diwali Shorts, and it is now installed BEFORE any verdict
    rather than after. A trend line drawn through noise looks exactly like a trend line.
    """
    if not matches:
        return True
    durs = [duration_min(v.get("duration")) for v in matches]
    shorts = sum(1 for d in durs if d < 1.5) / len(durs)
    in_band = 1.0
    if band and band[1]:
        in_band = sum(1 for d in durs if band[0] * 0.5 <= d <= max(band[1] * 2, 3)) / len(durs)
    if shorts > 0.30 or in_band < 0.40:
        print(f"\n⚠ INCOHERENT — {shorts:.0%} of matches are Shorts, {in_band:.0%} near the "
              f"declared runtime.\n  The regex is matching ordinary English; a time series "
              f"built on it is noise. No verdict.")
        for v in matches[:4]:
            print(f"    · {duration_min(v.get('duration')):>5.1f}m  {(v.get('title') or '')[:62]}")
        return False
    return True


def slope(xs):
    """Least-squares slope normalised by the mean — a unitless per-bucket growth rate."""
    xs = [x for x in xs if x is not None]
    n = len(xs)
    if n < 3:
        return None
    mean_x = (n - 1) / 2
    mean_y = sum(xs) / n
    denom = sum((i - mean_x) ** 2 for i in range(n))
    if not denom or not mean_y:
        return None
    return round((sum((i - mean_x) * (y - mean_y) for i, y in enumerate(xs)) / denom) / mean_y, 3)


def probe(query, rx, a):
    today = dt.date.today()
    span = max(1, int(a.months * 30 / a.buckets))
    buckets = []
    for i in range(a.buckets - 1, -1, -1):          # oldest first
        hi = today - dt.timedelta(days=span * i)
        lo = today - dt.timedelta(days=span * (i + 1))
        res = call_tool("vidiq_youtube_search", {
            "query": query, "type": ["video"], "order": "viewCount", "limit": PROBE_LIMIT,
            "regionCode": a.region,
            "publishedAfter": f"{lo.isoformat()}T00:00:00Z",
            "publishedBefore": f"{hi.isoformat()}T00:00:00Z"})
        got = res.get("results") or []
        hits = [v for v in got if not rx or re.search(rx, v.get("title") or "", re.I)]
        buckets.append({"from": lo.isoformat(), "to": hi.isoformat(),
                        "raw": len(got), "videos": hits})
        print(f"  {lo} → {hi}   {len(got):>2} results, {len(hits):>2} match")
    return buckets


def classify(buckets):
    seen = set()
    series = []
    for b in buckets:
        chans = {v.get("channelId") for v in b["videos"] if v.get("channelId")}
        new = chans - seen
        seen |= chans
        views = [v.get("viewCount") or 0 for v in b["videos"]]
        series.append({
            "from": b["from"], "to": b["to"], "n": len(b["videos"]),
            "channels": len(chans), "new_channels": len(new),
            "median_views": int(st.median(views)) if views else 0,
        })

    live = [s for s in series if s["n"]]
    if len(live) < 3 or len(seen) <= VALIDATION_CHANS:
        return series, (VALIDATION if len(seen) <= VALIDATION_CHANS else UNCLASSIFIED), {}
    dens = st.median([s["n"] for s in live])
    if dens < MIN_VIDS_PER_BUCKET:
        return series, SPARSE, {"median_per_bucket": dens, "total_channels": len(seen)}

    # Trailing half carries the verdict — a format's stage is where it is NOW, not on average.
    tail = live[max(0, len(live) - max(3, len(live) // 2)):]
    ent_s = slope([s["channels"] for s in tail])
    view_s = slope([s["median_views"] for s in tail])
    m = {"entrant_slope": ent_s, "views_slope": view_s,
         "total_channels": len(seen), "buckets_live": len(live)}
    if ent_s is None or view_s is None:
        return series, UNCLASSIFIED, m

    rising_e = ent_s > FLAT_BAND
    falling_e = ent_s < -FLAT_BAND
    rising_v = view_s > FLAT_BAND
    falling_v = view_s < -FLAT_BAND

    if rising_e and rising_v:
        stage = BREAKOUT
    elif rising_e and falling_v:
        stage = SATURATING
    elif rising_e:
        stage = MOMENTUM
    elif falling_e and falling_v:
        stage = DECLINE
    elif falling_v:
        stage = SATURATING
    elif falling_e:
        stage = DECLINE
    else:
        stage = STABLE          # flat entrants AND flat views — the corpus's "peak stability"
    return series, stage, m


ADVICE = {
    BREAKOUT:   "ENTER. Validated by others, still expanding. This is the window.",
    STABLE:     "MATURE PLATEAU — the corpus's 'peak stability'. Neither entrants nor views "
                "are moving. Safe to enter on CRAFT rather than timing: no land grab is "
                "available, and none is closing either.",
    SPARSE:     "NO VERDICT — too few videos per bucket to fit a slope to. This is itself "
                "informative: a format published this rarely is not a trend, it is a low-"
                "cadence craft format. Judge it on slot inventory and absolute views instead.",
    MOMENTUM:   "ENTER WITH SPEED, or not at all. Entrants are climbing and views are flat — "
                "the window is closing, not open.",
    SATURATING: "DO NOT ENTER. Entrants still rising while views fall is supply eating demand.",
    DECLINE:    "DO NOT ENTER. Unless you are buying a vacated lane deliberately — check "
                "bend-map for VACATED cells, which is a different and better bet.",
    VALIDATION: "TOO EARLY. Nobody has proven it travels. Watch it; do not build on it.",
    UNCLASSIFIED: "NO VERDICT. Too few live buckets — widen --months or check the regex.",
}


def main():
    p = argparse.ArgumentParser(description="Which of the five stages is this format in?")
    p.add_argument("--format", help="format_id from format-index.py")
    p.add_argument("--query", help="ad-hoc phrase instead of a catalogued format")
    p.add_argument("--months", type=int, default=MONTHS)
    p.add_argument("--buckets", type=int, default=BUCKETS)
    p.add_argument("--region", default="US")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    idx = json.loads(INDEX.read_text()) if INDEX.exists() else {"formats": {}}
    fmt, rx, band = None, None, None
    if a.format:
        fmt = idx["formats"].get(a.format)
        if not fmt:
            sys.exit(f"unknown format '{a.format}'")
        rx = fmt.get("title_regex")
        band = fmt.get("runtime_min")
        query = re.sub(r"\s+", " ", re.sub(r"\{[A-Z]+\}", " ",
                       fmt.get("title_template") or fmt["name"])).strip()
    elif a.query:
        query = a.query
    else:
        sys.exit("pass --format <id> or --query \"<phrase>\"")

    cost = a.buckets * CREDITS_PER_CALL
    span_d = max(1, int(a.months * 30 / a.buckets))
    print(f"query    \"{query}\"" + (f"   regex {rx}" if rx else "   (no regex — --query mode)"))
    print(f"window   {a.months} months in {a.buckets} buckets of ~{span_d}d   region {a.region}")
    print(f"cost     {cost} credits (~${cost * 0.00475:.2f})\n")
    if a.dry_run:
        print("--dry-run: nothing spent.")
        return

    key = re.sub(r"[^a-z0-9]+", "-", (a.format or query).lower()).strip("-")[:50]
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / f"{key}-{a.months}m{a.buckets}b.json"
    if cf.exists() and not a.refresh:
        print(f"using cached probe {cf.name} (--refresh to re-spend)")
        buckets = json.loads(cf.read_text())
    else:
        buckets = probe(query, rx, a)
        cf.write_text(json.dumps(buckets, indent=1))

    allv = [v for b in buckets for v in b["videos"]]
    # The coherence gate polices FORMAT REGEXES. In --query mode there is no format claim to
    # violate: a subject trend legitimately spans Shorts and long-form, and the gate fired on
    # the "ancient humans" backtest purely because 32% of a topic's videos are Shorts. Applying
    # it there would have been a false refusal, which is its own kind of wrong answer.
    if rx and not coherent(rx, band, allv):
        return

    # Shorts are excluded from the SERIES regardless of mode. Their view distribution is an
    # order of magnitude apart from long-form, so mixing them makes median_views a measure of
    # the Shorts share rather than of demand. Reported, not silently dropped.
    n_shorts = sum(1 for v in allv if duration_min(v.get("duration")) < 1.5)
    if n_shorts:
        for b in buckets:
            b["videos"] = [v for v in b["videos"] if duration_min(v.get("duration")) >= 1.5]
        print(f"\nexcluded {n_shorts} Shorts from the series "
              f"({n_shorts/len(allv):.0%} of matches) — their view scale is not comparable")

    series, stage, m = classify(buckets)
    print(f"\n{'period':<24} {'vids':>5} {'chans':>6} {'new':>4} {'median views':>13}")
    print("-" * 60)
    for s in series:
        print(f"{s['from']} → {s['to'][5:]:<9} {s['n']:>5} {s['channels']:>6} "
              f"{s['new_channels']:>4} {s['median_views']:>13,}")

    print(f"\n{'='*68}\nSTAGE  {stage}")
    if m.get("entrant_slope") is not None:
        print(f"  entrant slope {m['entrant_slope']:+.3f}/bucket · views slope "
              f"{m['views_slope']:+.3f}/bucket · {m['total_channels']} channels total")
    elif m.get("median_per_bucket") is not None:
        print(f"  median {m['median_per_bucket']:.0f} videos/bucket "
              f"(floor is {MIN_VIDS_PER_BUCKET}) · {m['total_channels']} channels total")
    print(f"\n  {ADVICE[stage]}")
    if stage in (BREAKOUT, MOMENTUM) and m.get("entrant_slope"):
        # Saturation speed, not a date. A rate is defensible; a predicted peak date is not.
        print(f"\n  At the current entrant rate the field grows ~{m['entrant_slope']*100:.0f}% "
              f"per {span_d}d bucket.\n  That is a SPEED, not a forecast — the tool does not "
              f"predict a peak date, because\n  the entrant curve is censored by the 50-result "
              f"cap (see CONFOUNDS).")

    if fmt is not None:
        fmt["trend_stage"] = {"stage": stage, "measured": dt.date.today().isoformat(),
                              "months": a.months, "buckets": a.buckets, **m}
        INDEX.write_text(json.dumps(idx, indent=1))
        print(f"\nrecorded trend_stage={stage} on {a.format}")


if __name__ == "__main__":
    main()
