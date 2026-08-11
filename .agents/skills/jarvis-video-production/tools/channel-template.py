#!/usr/bin/env python3
"""channel-template.py — read ONE channel's own repeated title template, and count its refills.

TOOL CONTRACT
  SUBSYSTEM  D (Demand). The DISCOVERY front end. Feeds format-index.py -> bend-map.py.
  STATE      writes raw/templates/<handle>.json (cache) · --emit appends to ratchet/formats.json
  GATE       none. Emits measured templates for reading.
  MODULE     jarvis-video-production (tools tree)
  COST       ZERO. yt-dlp flat-playlist only -- no vidIQ credits, no API key, no download.

    channel-template.py @extramintyy
    channel-template.py https://www.youtube.com/@wuhoops --top 6
    channel-template.py @extramintyy --emit why-did-x-look-like-that

WHY THIS EXISTS -- AND WHY THE OBVIOUS APPROACH FAILED FIRST
  Measured 2026-08-10: n-gram mining ACROSS channels produced zero usable formats from a
  2,288-video pool. Every frame it surfaced was ordinary English ("worse than a" enumerated to
  "Nothing worse than a bad day gym day"). The design error is recorded in format-index.py:

      A format's signature is ONE CHANNEL'S OWN repeated template. Across unrelated channels,
      the only thing that recurs is English. Within one channel, the TOPIC is what varies and
      the TEMPLATE is what repeats -- the exact mirror image, which is why frequency analysis
      works here and cannot work there.

  So this reverses the axis. It reads one channel's catalogue and asks what that channel says
  the same way over and over. That is the method our own prior research used to find
  ExtraMint's ~14 refillable slots and to measure the ~19x template lever
  (jarvis-private/reports/YoutubeResearchTopics/YOUTUBE-DEMAND-RESEARCH-2026-08-09.md §3, §4).

THE HEADLINE METRIC -- LIFT
      lift = median(views of videos USING the template) / median(views of the channel's REST)

  This is the ~19x lever computed directly: ExtraMint's era-titles median 631,043 against its
  own non-era videos at 33,617. Because both terms come from the SAME channel, lift controls
  for channel size, audience and era in a way no cross-channel comparison can. It is the
  closest thing to a controlled experiment available from public data.

  A template with high lift and few slots is a lucky title. A template with high lift AND many
  slots is an ASSET -- "a template used once is just a title." Both numbers are reported and
  neither is sufficient alone.

  LOW LIFT IS NOT A VERDICT ON THE TEMPLATE. Measured across 14 channels 2026-08-10: Company
  Man's "The Decline of {X}" scores lift 1.35x while medianing 504,000 views over 114 slots,
  and Modern MBA's "The Business of {X}" scores 1.86x at a 1,083,000 median. Lift near 1 on a
  large channel means the WHOLE CATALOGUE performs -- there is no weak remainder to beat -- not
  that the shape is inert. Read lift together with the absolute median and the slot count:
      high lift + high median   the template is the lever          (ExtraMint 12.2x / 463k)
      low  lift + high median   the channel is uniformly strong    (Company Man 1.4x / 504k)
      high lift + low  median   arithmetic on a small base         (Who Gets Paid 22x / 3.9k)

METRIC DISCIPLINE (§2 of the same research -- all seven traps were measured, these three bind)
  MEDIAN, NEVER MEAN. avgViews is a mean and one hit destroys it: a channel showing 54,892 had
      a true median of 2,024, a 27x gap.
  p75/p25, NEVER max/median. max/median is sample-size dependent -- the same channel scored
      9.0x at n=30 and 23.7x at n=40, opposite verdicts. p75/p25 is stable in n.
  JUDGE A WINDOW, NOT A LIFETIME. Channels improve; pooling an apprenticeship with mature work
      measures the learning curve. ExtraMint: 26.9x spread lifetime vs 7.7x over 24 months.
      See the confound below for how the window is approximated here.

CONFOUNDS
  THE WINDOW IS A COUNT, NOT A DATE RANGE. yt-dlp's flat-playlist returns upload_date as NA,
      so there are no timestamps without paying for them. The catalogue arrives newest-first,
      so --recent K is a POSITION window, not the 24-month window §2 trap 4 specifies. For a
      steady uploader they are close; for one that changed cadence they are not. Lifetime and
      window figures are both printed so the gap is visible. Do not report the window as a date
      range.
  VIEW COUNTS ARE LIFETIME AND FAVOUR OLD VIDEOS. A template the channel abandoned can still
      out-median a current one purely by having had longer to accumulate. Read `positions`:
      if a template's videos all sit at the back of the catalogue, its lift is age, not shape.
  A TEMPLATE IS NOT YET A FORMAT. This proves ONE channel repeats a shape profitably. Whether
      the shape travels is a different question, and format-index.py's >=3-distinct-channel
      rule is the test for it. Do not skip that step: it is the whole reason bend-map exists.
  SHORT N-GRAMS ARE FINE HERE and dangerous elsewhere. "why did" is meaningless as a
      cross-channel format signature and completely meaningful as ExtraMint's spine. The
      minimum length is deliberately lower than format-index.py's because the channel context
      supplies the specificity that the n-gram itself lacks.
"""
import argparse
import json
import re
import statistics as st
import subprocess
import sys
import datetime as dt
from collections import Counter, defaultdict
from pathlib import Path

TOOLS   = Path(__file__).resolve().parent
RATCHET = TOOLS / "ratchet"
CACHE   = TOOLS / "raw" / "templates"
INDEX   = RATCHET / "formats.json"

MIN_TEMPLATE_VIDEOS = 3     # a shape used twice is a coincidence; three times is a habit
MIN_NGRAM           = 2     # see the CONFOUNDS note -- channel context supplies specificity
MAX_NGRAM           = 8
DF_FLOOR_ABS        = 3     # a token in fewer than this many of the channel's titles is topic
DF_FLOOR_REL        = 0.05  # ...or fewer than this share of them.
                            # LOWERED from 0.08 on 2026-08-11. Terry noticed by eye that Modern
                            # MBA also runs "The Economics of X"; the tool could not see it.
                            # Cause: 'economics' appears in 5 of 80 titles and the floor was
                            # max(3, 0.08*80) = 6.4 — it missed by 1.4, so the variant could
                            # never form a template at all.
                            # THE PRINCIPLE: a template only needs MIN_TEMPLATE_VIDEOS (3) to
                            # exist, so a df floor far above 3 over-filters by construction, and
                            # it gets WORSE as a catalogue grows because the floor scales with n.
                            # MIN_TEMPLATE_VIDEOS is the real quality gate; this floor only has
                            # to strip one-off words.
                            # Measured across four known channels: Modern MBA 1 -> 4 templates
                            # (surfacing 'economics of', 'really make money', "can't survive" —
                            # all three real and all three previously invisible), Company Man
                            # 9 -> 10, ExtraMint 12 -> 15, Wu Hoops 7 -> 7. Noise did not move.
RECENT_DEFAULT      = 24    # position window; see the CONFOUNDS note on why it is not months
MAX_SHARE_FOR_LIFT  = 0.60  # above this the template IS the channel and lift is noise
MIN_BASE_VIEWS      = 5_000 # below this median, LIFT IS SCALE-BLIND. 22x from 176 -> 3,900
                            # views is arithmetic; 12x from 38,000 -> 463,000 is a business.
                            # A ratio cannot tell them apart, so the absolute base is printed
                            # and flagged rather than folded into the score.

TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(title):
    t = re.sub(r"\d+", " zqnumzq ", (title or "").lower())
    return ["{N}" if w == "zqnumzq" else w for w in TOKEN.findall(t)]


def fetch(channel, refresh=False):
    """Full catalogue via yt-dlp. Free, complete, and not capped at 50 like the paid endpoints."""
    handle = re.sub(r"[^A-Za-z0-9_@.-]", "", channel.rstrip("/").split("/")[-1]) or "channel"
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{handle}.json"
    if cache.exists() and not refresh:
        return handle, json.loads(cache.read_text())

    url = channel if channel.startswith("http") else f"https://www.youtube.com/{channel}"
    if not url.rstrip("/").endswith(("/videos", "/shorts")):
        url = url.rstrip("/") + "/videos"
    print(f"fetching {url} …")
    try:
        out = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(title)s|%(view_count)s|%(duration)s",
             url], capture_output=True, text=True, timeout=300)
    except FileNotFoundError:
        sys.exit("yt-dlp not found. brew install yt-dlp")
    vids = []
    for line in out.stdout.splitlines():
        p = line.split("|")
        if len(p) < 4:
            continue
        vids.append({"id": p[0], "title": p[1],
                     "views": int(p[2]) if p[2].isdigit() else 0,
                     "duration": int(p[3]) if p[3].isdigit() else 0})
    if not vids:
        sys.exit(f"no videos returned for {url}\n{out.stderr[-300:]}")
    cache.write_text(json.dumps(vids, indent=1))
    return handle, vids


def spread(xs):
    """p75/p25 — stable in n, unlike max/median. §2 trap 3."""
    xs = sorted(x for x in xs if x)
    if len(xs) < 4:
        return None
    q = st.quantiles(xs, n=4)
    return round(q[2] / q[0], 2) if q[0] else None


def templates_of(vids):
    """Every n-gram used by >=MIN_TEMPLATE_VIDEOS of this channel's own titles."""
    toks = [tokenize(v["title"]) for v in vids]
    df = Counter()
    for t in toks:
        for w in set(t):
            df[w] += 1
    floor = max(DF_FLOOR_ABS, DF_FLOOR_REL * len(vids))
    # WITHIN a channel, frequency identifies the TEMPLATE because the topic is what varies.
    # This is the exact inverse of the cross-channel case, where frequency identified the topic.
    common = {w for w, c in df.items() if c >= floor}

    groups = defaultdict(list)
    for v, t in zip(vids, toks):
        run = []
        for w in t + [None]:
            if w is not None and w in common:
                run.append(w)
                continue
            for size in range(MIN_NGRAM, MAX_NGRAM + 1):
                for i in range(0, len(run) - size + 1):
                    groups[" ".join(run[i:i + size])].append(v)
            run = []

    rows = []
    for ng, used in groups.items():
        used = list({v["id"]: v for v in used}.values())
        if len(used) < MIN_TEMPLATE_VIDEOS:
            continue
        rows.append({"template": ng, "videos": used})
    # maximal phrases only: drop an n-gram wholly contained in a longer one covering >= the
    # same videos. Otherwise every template reports as a dozen nested substrings.
    rows.sort(key=lambda r: (-len(r["template"].split()), -len(r["videos"])))
    kept = []
    for r in rows:
        if any(r["template"] in k["template"] and len(k["videos"]) >= len(r["videos"])
               for k in kept):
            continue
        kept.append(r)
    return kept


def anchor_of(title, template):
    """The VARYING part — what fills the slot. This list IS the refill inventory."""
    words = template.split()
    t = title
    for w in words:
        if w == "{N}":
            t = re.sub(r"\d[\d,\.]*", " ", t, count=1)
        else:
            t = re.sub(r"(?i)\b" + re.escape(w) + r"\b", " ", t, count=1)
    return re.sub(r"\s+", " ", re.sub(r"[|:\-–—?!.]+", " ", t)).strip()


def analyse(vids, a):
    total_med = st.median([v["views"] for v in vids]) or 1
    rows = []
    for r in templates_of(vids):
        used = r["videos"]
        used_ids = {v["id"] for v in used}
        rest = [v for v in vids if v["id"] not in used_ids]
        med_used = st.median([v["views"] for v in used])
        med_rest = st.median([v["views"] for v in rest]) if rest else 0
        idxs = [i for i, v in enumerate(vids) if v["id"] in used_ids]
        rows.append({
            "template": r["template"],
            "slots": len(used),
            "share": len(used) / len(vids),
            "median_views": int(med_used),
            "median_rest": int(med_rest),
            # LIFT: the ~19x lever, computed inside one channel so size/audience are controlled.
            "lift": round(med_used / med_rest, 2) if med_rest else None,
            "spread": spread([v["views"] for v in used]),
            "median_runtime_min": round(st.median([v["duration"] for v in used]) / 60, 1),
            "positions": f"{min(idxs)}-{max(idxs)}",
            "recent_hits": sum(1 for i in idxs if i < a.recent),
            "anchors": [anchor_of(v["title"], r["template"])[:38] for v in
                        sorted(used, key=lambda v: -v["views"])][:12],
            "best": max(used, key=lambda v: v["views"]),
        })
    rows = [r for r in rows if r["lift"]]
    rows.sort(key=lambda r: -(r["lift"] * r["slots"]))
    return rows, total_med


def main():
    p = argparse.ArgumentParser(description="One channel's repeated title template + refills.")
    p.add_argument("channel", nargs="?", help="@handle, URL, or channel id")
    p.add_argument("--top", type=int, default=8, help="templates to print")
    p.add_argument("--recent", type=int, default=RECENT_DEFAULT,
                   help="position window (NOT months — see CONFOUNDS)")
    p.add_argument("--refresh", action="store_true", help="ignore the cache")
    p.add_argument("--emit", metavar="FORMAT_ID",
                   help="write the top template into ratchet/formats.json as a catalogue row")
    a = p.parse_args()
    if not a.channel:
        sys.exit("pass a channel: channel-template.py @extramintyy")

    handle, vids = fetch(a.channel, a.refresh)
    rows, total_med = analyse(vids, a)
    print(f"\n{handle} — {len(vids)} videos · median {int(total_med):,} views "
          f"· lifetime spread {spread([v['views'] for v in vids])}x")
    print(f"window = most recent {a.recent} BY POSITION (not months — see CONFOUNDS)\n")
    if not rows:
        print("no repeated template. This channel does not run one, or the catalogue is too "
              "small.\nThat is a finding: a channel with no refillable shape is not a "
              "discovery source.")
        return

    print(f"{'lift':>7} {'slots':>5} {'share':>6} {'med views':>10} {'p75/p25':>8} {'run':>5}  template")
    print("-" * 104)
    for r in rows[: a.top]:
        sp = f"{r['spread']}x" if r["spread"] else "—"
        print(f"{r['lift']:>6.2f}x {r['slots']:>5} {r['share']:>5.0%} "
              f"{r['median_views']:>10,} {sp:>8} {r['median_runtime_min']:>4.0f}m  {r['template']}")
        print(f"{'':41}rest of channel: {r['median_rest']:,} · positions {r['positions']}")
        print(f"{'':41}slots: {' · '.join(x for x in r['anchors'][:6] if x)[:70]}")
        print(f"{'':41}best:  {r['best']['title'][:64]} ({r['best']['views']:,})")

    top = rows[0]
    if top["share"] > MAX_SHARE_FOR_LIFT:
        print(f"\n⚠ LIFT NOT MEANINGFUL — the template covers {top['share']:.0%} of the "
              f"catalogue.\n  Lift divides template videos by 'the rest', and when the rest is "
              f"a tiny remainder that\n  denominator is noise, not a control. Judge it on "
              f"ABSOLUTE median and slot count; ignore the ratio.")
    if top["median_views"] < MIN_BASE_VIEWS:
        print(f"\n⚠ SMALL BASE — the top template medians {top['median_views']:,} views. Lift is a "
              f"RATIO and\n  says nothing about scale: this channel could double every number "
              f"and still be small.\n  Treat as a HYPOTHESIS about a shape, not evidence that "
              f"the shape earns. Confirm by\n  finding the same template on a channel with a "
              f"real audience.")
    print(f"\nREAD: '{top['template']}' is used on {top['slots']} of {len(vids)} videos and "
          f"medians {top['lift']:.1f}x the rest of\nthis channel. "
          + ("That is an ASSET — high lift AND a filled inventory."
             if top["slots"] >= 5 and top["lift"] >= 3 else
             "Treat with care: lift without slots is a lucky title, not a template.")
          + "\nNEXT: is the shape PORTABLE? format-index.py needs >=3 DISTINCT channels using "
            "it before\nbend-map.py can ask which markets are free.")

    if a.emit:
        if not INDEX.exists():
            sys.exit("no ratchet/formats.json — run format-index.py --seed first")
        idx = json.loads(INDEX.read_text())
        rx = r"\b" + r"\s+".join(
            r"\d[\d,\.]*" if w == "{N}" else re.escape(w) for w in top["template"].split()) + r"\b"
        idx["formats"][a.emit] = {
            "format_id": a.emit, "name": top["template"],
            "anchor": "concrete", "refill_slots": top["slots"],
            "visual": None, "title_template": top["template"], "title_regex": rx,
            "runtime_min": [top["median_runtime_min"], top["median_runtime_min"]],
            "tier": None, "cost_usd": None, "seed_channel": handle,
            "corpus_occupied": [], "corpus_free": [], "markets_occupied": {},
            "provenance": f"teardown:{handle}:{dt.date.today().isoformat()}",
            "measured": {k: top[k] for k in
                         ("lift", "slots", "share", "median_views", "median_rest", "spread",
                          "positions", "recent_hits", "anchors")},
            "added": dt.date.today().isoformat(),
            "notes": f"Measured on ONE channel ({handle}): {top['slots']} filled slots at "
                     f"{top['lift']}x its own rest. Portability across channels is UNTESTED — "
                     f"that is format-index.py's >=3-channel rule, then bend-map.py.",
        }
        INDEX.write_text(json.dumps(idx, indent=1))
        print(f"\nemitted -> {a.emit}  (refill_slots={top['slots']}, lift={top['lift']}x)")


if __name__ == "__main__":
    main()
