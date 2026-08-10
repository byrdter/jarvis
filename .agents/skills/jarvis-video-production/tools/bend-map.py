#!/usr/bin/env python3
"""bend-map.py — walk one FORMAT across every MARKET and find the empty cells.

TOOL CONTRACT
  SUBSYSTEM  D (Demand), feeding P1a Market Selection
  STATE      reads ratchet/formats.json (format-index.py owns it)
             writes markets_occupied back into that file, + ratchet/bendmap-<fmt>-<date>.csv
  GATE       none. Emits RANKED CELLS FOR READING. market-gate.py is the gate.
  MODULE     jarvis-video-production (tools tree)
  SCOPE      market-agnostic, subject-agnostic

    bend-map.py --format exhaustive-analysis-flex --dry-run     # cost, spends nothing
    bend-map.py --format exhaustive-analysis-flex               # expert+strong markets
    bend-map.py --format pov-tier-ranking --all-markets
    bend-map.py --list                                          # grids already measured

WHY THIS EXISTS
  format-index.py owns the row axis. This walks the columns. For one format it asks, market by
  market, "is anyone already doing this here?" -- and the answer is the whole point, because
  the practitioner rule the governing report mechanizes is: pursue a format where the FREE
  cells outnumber the TAKEN ones.

  Governing report: jarvis-private/reports/FACELESS-NICHE-SYSTEM-2026-08-10.md

THE FIVE VERDICTS -- and why VACATED is the valuable one
  TAKEN     >=1 title match with traction INSIDE the recency window. Someone owns this now.
  VACATED   title matches exist and travelled, but the most recent is OUTSIDE the window.
            Demand is proven and the incumbent has left. This is the best cell on the board
            and it only exists because the verdict is time-windowed -- see below.
  THIN      matches exist, all weak. Tried, did not travel.
  FREE      the market clearly has content, but ZERO titles match the frame.
  UNPROVEN  the probe returned too little to say anything. NOT a synonym for FREE.

  UNPROVEN vs FREE is the load-bearing distinction and it is the same doctrine market-gate.py
  runs on: missing evidence BLOCKS, it is never read as a pass. A search that returns nothing
  usually means the query was wrong, not that a market is virgin territory. Only a probe that
  came back healthy and contained no match is allowed to say FREE.

WHY THE VERDICT IS TIME-WINDOWED
  Measured while building this, 2026-08-10: probing "every level of wealth explained" ordered by
  viewCount returned, as its top hit, a video published in NOVEMBER 2012. Ranking by lifetime
  views makes long-dead videos look like live incumbents, and would have marked a wide-open cell
  as TAKEN. Our own prior research reached the same place from the other direction -- its chosen
  video's lane had an incumbent who "vacated 13 months ago", after which a 1,290-sub channel won
  in it. So recency is not a refinement here, it is the difference between the two most
  opposite verdicts the tool can emit.

RANKING -- CORRECTED 2026-08-10, DO NOT REVERT
  The first spec ranked free cells by market size x MARKET-LEVEL RPM. Our own prior investigation
  (jarvis-private/reports/YoutubeResearchTopics/YOUTUBE-DEMAND-RESEARCH-2026-08-09.md §7a) had
  already measured that as the wrong instrument: WITHIN-category variance dwarfs BETWEEN-category
  difference. Category medians for revenue/video cluster tightly and low -- Sport $277, Music
  $239, Hobby $78, Lifestyle $44 -- while individual channels inside those same categories reach
  $1,000-3,900. One track-and-field channel earns $5,463/video against a Sport median of $277.
  Verbatim: "A tool that ranked niches would point at Sport and still miss the channel earning
  20x inside it."

  So cells are ranked on, in order:
    1. GEO  -- §7b, geography dominates where category does not (US vs IN, same category:
              Entertainment $4.19 vs $0.01 implied RPM, ~400x). Handled as a PROBE CONTROL,
              see the confound below.
    2. CHANNEL-LEVEL economics inside the cell -- the best REACHABLE channel's views/subs.
              Never the cell's category median.
    3. COMPETENCE -- format-index.py's market index. Barrier-to-entry #2 (skill).
    4. SLOT EVIDENCE -- see below.

REFILL SLOTS -- measured as evidence, never as a number
  §3 of the same research measured a refillable title template at ~19x and sharpened it: "a
  template used once is just a title" -- the asset is the FILLED SLOTS, fourteen of them. So
  n_channels>=3 (format-index) proves a shape is PORTABLE; refill count proves it is an ASSET.
  A portable shape with four refills is a dead end.

  This tool does NOT invent a refill count. It emits `slot_anchors`: the distinct concrete
  subjects it actually saw the frame filled with in that market. Enumerating the remaining
  slots is a judgement call and belongs to an agent or a human downstream -- the same division
  outlier-ratchet.py draws when it refuses to classify topic.

CONFOUNDS -- read before trusting a column
  GEO IS A PROBE CONTROL, NOT A MEASUREMENT. vidiq_youtube_search does not return
      channelCountry, so this cannot measure where a cell's audience is. It probes with
      regionCode (default US) and records that. A cell ranked well here has been probed in a
      tier-1 region; it has NOT been shown to have a tier-1 audience. To measure that, run
      scout-niches.py over the market. Do not report the two as if they were the same.
  avgViews IS A MEAN AND IS NOT USED. §2 trap 2: one hit destroys it (a channel showing
      avgViews 54,892 had a true median of 2,024, a 27x gap). Every per-cell figure here is a
      MEDIAN over the matched videos.
  SEARCH THE AUDIENCE'S WORD, NOT OUR LABEL. §5: "why does everything online look fake now"
      returns n=0 where "dead internet theory" probes 108.94x. MARKET_TERMS below are audience
      phrasings for exactly this reason; our internal market names would manufacture false FREEs.
  ONE PROBE PER CELL IS ONE SAMPLE. A FREE verdict on a single query is weak evidence. Re-probe
      a cell with a different phrasing before committing production to it.
  MARKET BINNING IS KEYWORD MATCHING AND IT PRODUCES FALSE CELLS. Caught on the first live
      enumeration, 2026-08-10: "Ranking EVERY Boss Fight In Super Mario Odyssey!" was binned
      into MANAGEMENT & LEADERSHIP because the term list contained "bosses". The worst
      collisions have been removed, but the mechanism is inherently lossy -- a term that is
      unambiguous in one market is ordinary English in another. ALWAYS read best_title on a
      TAKEN or VACATED cell before believing it. A cell whose evidence is one mis-binned video
      is FREE, not occupied.
  BINNING SILENTLY DROPS WHAT IT CANNOT PLACE -- so it is reported instead. Two of the three
      instances of exhaustive-analysis-flex ("...30,093,975,536 Battleship Boards...",
      "...Every Draw Engine...") matched no market at all. Unclassified instances are printed
      because they are evidence the MARKET LIST has a hole, not evidence of an empty grid.
  FORMATS WITH NO TITLE SIGNATURE CANNOT BE WALKED. low-poly-3d-shorts, rapid-news-3d and
      sleep-length-narration are visual formats; there is nothing to match. The tool refuses
      rather than returning a grid of meaningless FREEs.
"""
import argparse
import csv
import datetime as dt
import importlib.util
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

TOOLS   = Path(__file__).resolve().parent
RATCHET = TOOLS / "ratchet"
INDEX   = RATCHET / "formats.json"

URL      = "https://mcp.vidiq.com/mcp"
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
_SESSION = {}

# --- thresholds ----------------------------------------------------------------------
RECENCY_MONTHS   = 24     # the window a match must fall in to count as TAKEN rather than
                          # VACATED. 24 months is the same window §2 trap 4 requires for judging
                          # a channel, so the two instruments agree on what "current" means.
MIN_TAKEN_VIEWS  = 25_000 # a match below this did not travel; it is THIN evidence, not an owner
MIN_RESULTS_FREE = 8      # a probe returning fewer than this says nothing -> UNPROVEN, not FREE
REACHABLE_SUBS   = 300_000  # BAND_SUBS in scout-niches.py -- "reachable from cold"
PROBE_LIMIT      = 50     # vidIQ hard cap. Fewer would bias toward mega-channels.
COHERENCE_MIN    = 0.40   # share of matches that must sit near the format's declared runtime
CREDITS_PER_CALL = 5

# Audience-facing search terms per market. NOT our internal labels -- see the CONFOUNDS note.
# One probe uses the first term; --deep adds the rest as extra probes.
MARKET_TERMS = {
    "personal finance":         ["money", "personal finance", "budgeting"],
    "investing & stock market": ["investing", "stock market", "stocks"],
    "retirement planning":      ["retirement", "401k", "social security"],
    "insurance":                ["insurance", "life insurance", "health insurance"],
    "real estate":              ["real estate", "housing market", "mortgage"],
    "economics":                ["economy", "inflation", "recession"],
    "accounting":               ["accounting", "bookkeeping"],
    "taxes":                    ["taxes", "IRS", "tax"],
    "credit & debt":            ["credit score", "debt", "credit card"],
    "banking":                  ["banking", "central bank", "retail bank"],
    "crypto":                   ["crypto", "bitcoin"],
    "business strategy":        ["business strategy", "companies", "corporate"],
    "management & leadership":  ["management", "leadership", "middle manager"],
    "entrepreneurship":         ["startups", "entrepreneurs", "small business"],
    "marketing":                ["marketing", "advertising", "branding"],
    "B2B & SaaS":               ["SaaS", "software companies", "B2B"],
    "information systems":      ["IT systems", "enterprise software", "databases"],
    "supply chain":             ["supply chain", "logistics", "shipping"],
    "sales":                    ["sales team", "salespeople", "sales job"],
    "careers & jobs":           ["jobs", "careers", "salary"],
    "higher education":         ["college", "university", "student loans"],
    "productivity":             ["productivity", "time management"],
    "nutrition":                ["nutrition", "diet", "food"],
    "fitness & exercise":       ["fitness", "workout", "exercise"],
    "longevity":                ["longevity", "aging", "lifespan"],
    "mental health":            ["mental health", "anxiety"],
    "sleep":                    ["sleep", "insomnia"],
    "medicine":                 ["medicine", "doctors", "hospitals"],
    "AI & machine learning":    ["AI", "artificial intelligence"],
    "software engineering":     ["programming", "software engineering", "coding"],
    "consumer tech":            ["gadgets", "phones", "consumer tech"],
    "cybersecurity":            ["hacking", "cybersecurity", "scams"],
    "space":                    ["space", "NASA", "rockets"],
    "history":                  ["history", "historical"],
    "military history":         ["war", "military", "battles"],
    "science":                  ["science", "physics", "chemistry"],
    "psychology":               ["psychology", "the brain", "behavior"],
    "philosophy":               ["philosophy", "philosophers"],
    "true crime":               ["true crime", "murder", "criminals"],
    "geography":                ["geography", "countries", "maps"],
    "engineering & how-things-work": ["engineering", "how it works", "machines"],
    "aviation":                 ["planes", "aviation", "airlines"],
    "maritime":                 ["ships", "shipping", "the ocean"],
    "disasters":                ["disasters", "accidents", "catastrophes"],
    "parenting":                ["parenting", "kids", "raising children"],
    "relationships":            ["relationships", "dating", "marriage"],
    "self-improvement":         ["self improvement", "discipline", "habits"],
    "travel":                   ["travel", "countries", "flights"],
    "food & cooking":           ["cooking", "food", "restaurants"],
    "fashion & beauty":         ["fashion", "clothes", "beauty"],
    "home & DIY":               ["home improvement", "DIY", "houses"],
    "cars & automotive":        ["cars", "automotive", "vehicles"],
    "pets":                     ["dogs", "pets", "cats"],
    "gardening":                ["gardening", "plants"],
    "gaming":                   ["video games", "gaming"],
    "sports":                   ["sports", "athletes"],
    "football (soccer)":        ["soccer", "football", "premier league"],
    "basketball":               ["NBA", "basketball"],
    "movies & TV":              ["movies", "films", "TV shows"],
    "music":                    ["music", "songs", "musicians"],
    "anime":                    ["anime", "manga"],
    "celebrity":                ["celebrities", "famous people"],
    "comics & superheroes":     ["Marvel", "superheroes", "comics"],
}

TAKEN, VACATED, THIN, FREE, UNPROVEN = "TAKEN", "VACATED", "THIN", "FREE", "UNPROVEN"


# =====================================================================================
# transport (same shape as scout-niches.py / format-index.py -- duplicated on purpose so
# each tool runs standalone without a package layout)
# =====================================================================================
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
                            "clientInfo": {"name": "bend-map", "version": "1"}})
        _rpc("notifications/initialized", notify=True)
    res = _rpc("tools/call", {"name": name, "arguments": args})
    if "_http_error" in res:
        sys.exit(f"vidIQ HTTP {res['_http_error']}: {res['_body']}")
    for block in (res.get("result") or {}).get("content") or []:
        if block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except json.JSONDecodeError:
                return {"_raw": block["text"]}
    return {}


# =====================================================================================
# helpers
# =====================================================================================
def load_format_index():
    """format-index.py owns MARKETS and the catalogue. Import it rather than duplicating the
    market list -- two copies of the competence map would drift, and the whole point of the
    competence axis is that it is authored once, from Terry, in one place."""
    spec = importlib.util.spec_from_file_location("format_index", TOOLS / "format-index.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ISO_DUR = re.compile(r"P(?:\d+D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def duration_min(iso):
    m = ISO_DUR.match(iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return round(h * 60 + mi + s / 60, 1)


def med(xs):
    xs = sorted(x for x in xs if x)
    if not xs:
        return 0
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def frame_phrase(fmt):
    """The format's bare title phrase, with every placeholder removed.

    "I analyzed all {N} {X} so you don't have to" -> "I analyzed all so you don't have to"
    """
    tpl = fmt.get("title_template") or fmt["name"]
    q = re.sub(r"\{[A-Z]+\}", " ", tpl)
    return re.sub(r"\s+", " ", q).strip()


def assign_market(video, fi):
    """Bin one video into a market by matching AUDIENCE terms against its title+description.

    Returns every market that matched -- a video can legitimately sit in two. Returns [] when
    nothing matches, and those land in an "unclassified" bucket that is REPORTED rather than
    dropped, because a frame instance we cannot bin is evidence the market list has a hole.
    """
    hay = ((video.get("title") or "") + " " + (video.get("description") or "")[:400]).lower()
    hits = []
    for mkt, terms in MARKET_TERMS.items():
        if fi.MARKETS.get(mkt) == "avoid":
            continue
        if any(re.search(r"\b" + re.escape(t.lower()) + r"\b", hay) for t in terms):
            hits.append(mkt)
    return hits


def enumerate_frame(fmt, a):
    """STAGE 1 — find real instances of the frame, then bin them. This is the primary path.

    WHY THIS REPLACED PER-MARKET PROBING, measured 2026-08-10 and the reason to never go back:
    the first design ran one query per market, "<frame> <market term>", 26 calls. It returned
    21 FREE cells and a 91% free_ratio -- and a control probe proved that was mostly an
    artifact. The format's real, current incumbent ("I Analyzed All 30,093,975,536 Battleship
    Boards So You Don't Have To", 536,457 views, 20,500 subs, published two months earlier)
    NEVER SURFACED, because the gaming probe asked for "...all video games..." and the video is
    about a board game. Twenty-six narrow queries each missed it in a different way.

    Asking YouTube to enumerate the FRAME and binning what comes back finds instances wherever
    they actually live, costs ~4 calls instead of 26, and cannot miss an incumbent because we
    guessed its market wrong.
    """
    phrase = frame_phrase(fmt)
    plans = [("viewCount", None), ("date", None), ("relevance", None)]
    if not a.shallow:
        # A second, looser phrasing: the regex's own alternation often carries the real hook
        # ("so you don't have to") without the opening clause.
        tail = " ".join(phrase.split()[-5:])
        plans.append(("viewCount", tail))

    pool, seen = [], set()
    for order, override in plans:
        q = override or phrase
        res = call_tool("vidiq_youtube_search", {
            "query": q, "type": ["video"], "order": order,
            "limit": PROBE_LIMIT, "regionCode": a.region})
        got = res.get("results") or []
        new = 0
        for v in got:
            if v.get("id") and v["id"] not in seen:
                seen.add(v["id"])
                pool.append(v)
                new += 1
        print(f"  probe order={order:<9} \"{q[:46]}\" → {len(got):>2} results, {new:>2} new")
    return phrase, pool


def probe_query(fmt, market_term):
    """Build a query that reads like a real title in this market.

    Fill the format's placeholders with the market's AUDIENCE word (never our internal label),
    and drop the numeric slot -- "every {X} explained in {N} minutes" + "retirement" becomes
    "every retirement explained in minutes". Falls back to the format name when a row has no
    template, which is why --format on a signature-less row is refused upstream.
    """
    tpl = fmt.get("title_template") or fmt["name"]
    q = re.sub(r"\{N\}\s*", "", tpl)
    q = re.sub(r"\{[A-Z]+\}", market_term, q)
    return re.sub(r"\s+", " ", q).strip()


def classify(fmt, results, cutoff_iso):
    """One cell -> a verdict plus the evidence behind it."""
    rx = fmt.get("title_regex")
    matches = []
    for v in results:
        title = v.get("title") or ""
        if rx and re.search(rx, title, re.I):
            matches.append(v)

    ev = {
        "n_results": len(results),
        "n_matches": len(matches),
        "median_views": 0, "best_views": 0, "per_video": None,
        "median_runtime_min": 0, "latest": None,
        "best_title": None, "best_channel": None, "best_subs": None,
        "slot_anchors": [], "reachable_hits": 0,
    }
    if not matches:
        # A probe that came back thin proves nothing. Only a healthy, match-free probe is FREE.
        return (FREE if len(results) >= MIN_RESULTS_FREE else UNPROVEN), ev

    latest = max((v.get("publishedAt") or "") for v in matches)
    ev["latest"] = latest[:10]
    ev["median_views"] = int(med([v.get("viewCount") for v in matches]))
    ev["median_runtime_min"] = med([duration_min(v.get("duration")) for v in matches])

    # CHANNEL-LEVEL economics, restricted to reachable channels. §7a: the cell's value is what
    # a channel our size achieves in it, not what the category averages.
    reach = [v for v in matches if 0 < (v.get("subscriberCount") or 0) <= REACHABLE_SUBS]
    ev["reachable_hits"] = len(reach)
    ratios = [v["viewCount"] / v["subscriberCount"] for v in reach
              if v.get("viewCount") and v.get("subscriberCount")]
    if ratios:
        ev["per_video"] = round(med(ratios), 2)

    best = max(matches, key=lambda v: v.get("viewCount") or 0)
    ev["best_views"] = best.get("viewCount") or 0
    ev["best_title"] = best.get("title")
    ev["best_channel"] = best.get("channelTitle")
    ev["best_subs"] = best.get("subscriberCount")

    # Slot evidence, not a slot count -- the distinct subjects the frame was actually filled
    # with here. Enumerating the rest is a judgement call and is deliberately left downstream.
    ev["slot_anchors"] = sorted({(v.get("title") or "")[:60] for v in matches})[:6]

    if ev["best_views"] < MIN_TAKEN_VIEWS:
        return THIN, ev
    return (TAKEN if latest >= cutoff_iso else VACATED), ev


# =====================================================================================
# main flow
# =====================================================================================
def run_enumerate(fmt, markets, a, fi):
    """STAGE 2 — bin the enumerated instances into cells and emit a verdict per market."""
    cutoff_iso = (dt.date.today() - dt.timedelta(days=30 * RECENCY_MONTHS)).isoformat()
    rx = fmt["title_regex"]
    phrase, pool = enumerate_frame(fmt, a)
    matches = [v for v in pool if re.search(rx, v.get("title") or "", re.I)]
    print(f"\n  {len(pool)} unique videos pooled → {len(matches)} match the frame regex")
    if not matches:
        print("  NO INSTANCE OF THIS FRAME FOUND ANYWHERE. That is a probe or regex problem,\n"
              "  not proof the format is unused — treat every cell as UNPROVEN.")

    # COHERENCE GATE. A frame that enumerates to videos of wildly different LENGTH is not one
    # format -- it is a phrase. Caught 2026-08-10: four promoted 3-token frames all enumerated
    # to a mix of 20-minute finance essays and 15-second meme Shorts, and produced free_ratios
    # of 90-100% that meant nothing. Runtime is the cheapest coherence signal available from
    # this endpoint, and it is decisive: a format has a characteristic length.
    if matches:
        durs = [duration_min(v.get("duration")) for v in matches]
        shorts = sum(1 for d in durs if d < 1.5) / len(durs)
        band = fmt.get("runtime_min") or [0, 0]
        in_band = sum(1 for d in durs if band[0] * 0.5 <= d <= max(band[1] * 2, 3)) / len(durs)
        if shorts > 0.3 or in_band < COHERENCE_MIN:
            print(f"\n  ⚠ INCOHERENT FRAME — {shorts:.0%} of matches are Shorts, "
                  f"{in_band:.0%} fall near the declared {band[0]}-{band[1]}m runtime.")
            print("  This regex is matching ORDINARY ENGLISH, not a format signature. Verdicts\n"
                  "  below are meaningless; free_ratio is suppressed. Promote a LONGER frame.")
            for v in matches[:4]:
                print(f"    · {duration_min(v.get('duration')):>5.1f}m  {(v.get('title') or '')[:64]}")
            fmt["_incoherent"] = True

    binned, unclassified = {m: [] for m in markets}, []
    for v in matches:
        hits = [m for m in assign_market(v, fi) if m in binned]
        if not hits:
            unclassified.append(v)
        for m in hits:
            binned[m].append(v)

    rows = []
    for mkt in markets:
        vids = binned[mkt]
        verdict, ev = classify(fmt, vids, cutoff_iso) if vids else (
            # No instance found. With a healthy enumeration behind it that is real evidence of
            # an empty cell; with a thin one it is only our ignorance.
            (FREE if len(matches) >= MIN_RESULTS_FREE else UNPROVEN),
            {"n_results": len(matches), "n_matches": 0, "median_views": 0, "best_views": 0,
             "per_video": None, "median_runtime_min": 0, "latest": None, "best_title": None,
             "best_channel": None, "best_subs": None, "slot_anchors": [], "reachable_hits": 0})
        rows.append({"market": mkt, "competence": fi.MARKETS.get(mkt, "general"),
                     "verdict": verdict, "query": phrase, "region": a.region, **ev})

    if unclassified:
        print(f"\n  {len(unclassified)} frame instance(s) matched NO market — the market list "
              f"has a hole here:")
        for v in unclassified[:6]:
            print(f"    · {(v.get('title') or '')[:74]}")
    return rows


def run(fmt, markets, a, fi):
    cutoff = (dt.date.today() - dt.timedelta(days=30 * RECENCY_MONTHS))
    cutoff_iso = cutoff.isoformat()
    rows = []
    for i, mkt in enumerate(markets, 1):
        term = MARKET_TERMS.get(mkt, [mkt])[0]
        q = probe_query(fmt, term)
        args = {"query": q, "type": ["video"], "order": "viewCount",
                "limit": PROBE_LIMIT, "regionCode": a.region}
        if a.window_only:
            args["publishedAfter"] = f"{cutoff_iso}T00:00:00Z"
        res = call_tool("vidiq_youtube_search", args)
        results = res.get("results") or []
        verdict, ev = classify(fmt, results, cutoff_iso)
        comp = fi.MARKETS.get(mkt, "general")
        rows.append({"market": mkt, "competence": comp, "verdict": verdict,
                     "query": q, "region": a.region, **ev})
        flag = {"TAKEN": "·", "VACATED": "★", "THIN": "~", "FREE": "○", "UNPROVEN": "?"}[verdict]
        print(f"  [{i:>2}/{len(markets)}] {flag} {verdict:<9} {mkt:<28} "
              f"n={ev['n_results']:>2} m={ev['n_matches']:>2} "
              f"{('best ' + format(ev['best_views'], ',')) if ev['best_views'] else ''}")
    return rows


def report(fmt, rows, fi):
    counts = Counter(r["verdict"] for r in rows)
    decided = [r for r in rows if r["verdict"] != UNPROVEN]
    free_like = [r for r in rows if r["verdict"] in (FREE, VACATED)]
    print(f"\n{'='*96}\nFORMAT  {fmt['format_id']}  —  {fmt['name']}")
    print(f"  anchor={fmt.get('anchor')}  tier={fmt.get('tier')}  "
          f"runtime={fmt.get('runtime_min')}  provenance={fmt.get('provenance')}")
    print(f"\n  {' · '.join(f'{v}={counts.get(v,0)}' for v in (TAKEN, VACATED, THIN, FREE, UNPROVEN))}")

    if not decided:
        print("\n  NO CELL DECIDED. Every probe came back too thin to read. That is a probe "
              "problem,\n  not a discovery: check MARKET_TERMS and the title_template for this "
              "format.")
        return
    # free_ratio is computed over DECIDED cells only. Counting UNPROVEN as free would inflate
    # the headline number with our own ignorance -- the exact failure the verdict split exists
    # to prevent.
    if fmt.get("_incoherent"):
        print("\n  free_ratio SUPPRESSED — the frame failed the coherence gate above.")
        return
    ratio = len(free_like) / len(decided)
    print(f"  free_ratio = {len(free_like)}/{len(decided)} decided = {ratio:.0%}"
          f"   {'ABOVE' if ratio > 0.5 else 'below'} the 50% rule"
          f"   ({counts.get(UNPROVEN,0)} undecided, excluded)")

    order = {"expert": 0, "strong": 1, "general": 2, "avoid": 3}
    ranked = sorted(free_like, key=lambda r: (
        0 if r["verdict"] == VACATED else 1,      # proven demand + no incumbent first
        order.get(r["competence"], 9),            # then skill barrier
        -(r["per_video"] or 0),                   # then channel-level economics in the cell
    ))
    print(f"\n  RANKED OPPORTUNITY CELLS (region={rows[0]['region']}, "
          f"probe control not an audience measurement)")
    print(f"  {'verdict':<8} {'market':<28} {'comp':<8} {'per-vid':>8} {'run':>6} {'evidence'}")
    print("  " + "-" * 94)
    for r in ranked[: 20]:
        pv = f"{r['per_video']:.2f}x" if r["per_video"] else "—"
        rt = f"{r['median_runtime_min']:.0f}m" if r["median_runtime_min"] else "—"
        ev = (f"last {r['latest']} · best {r['best_views']:,}"
              if r["verdict"] == VACATED else f"{r['n_results']} results, 0 matches")
        print(f"  {r['verdict']:<8} {r['market']:<28} {r['competence']:<8} {pv:>8} {rt:>6} {ev}")
    for r in ranked[:3]:
        if r["verdict"] == VACATED and r["best_title"]:
            print(f"\n  ★ {r['market']}: \"{r['best_title'][:70]}\"")
            print(f"      {r['best_channel']} · {r['best_subs']:,} subs · "
                  f"{r['best_views']:,} views · last activity {r['latest']}")
    print("\n  NEXT: these are cells to READ, not a decision. Confirm a candidate with "
          "market-gate.py,\n  and re-probe with a different phrasing before committing "
          "production (one probe is one sample).")


def do_list(idx):
    any_ = False
    for fid, f in sorted(idx["formats"].items()):
        grid = f.get("markets_occupied") or {}
        if not grid:
            continue
        any_ = True
        c = Counter(v["verdict"] for v in grid.values())
        print(f"{fid:32} {len(grid):>3} cells  " +
              " ".join(f"{k}={c.get(k,0)}" for k in (TAKEN, VACATED, THIN, FREE, UNPROVEN)))
    if not any_:
        print("no grids measured yet. Run: bend-map.py --format <id>")


def main():
    p = argparse.ArgumentParser(description="Walk one format across markets; find empty cells.")
    p.add_argument("--format", help="format_id from format-index.py --list")
    p.add_argument("--list", action="store_true", help="grids already measured")
    p.add_argument("--all-markets", action="store_true",
                   help="every market, not just expert/strong (costs ~3x)")
    p.add_argument("--markets", help="comma-separated market subset")
    p.add_argument("--region", default="US",
                   help="regionCode for the probe. Geo is a PROBE CONTROL — see CONFOUNDS.")
    p.add_argument("--window-only", action="store_true",
                   help="restrict the probe itself to the recency window; makes VACATED "
                        "undetectable, so off by default")
    p.add_argument("--per-market", action="store_true",
                   help="legacy one-query-per-market probing. Kept for confirming a single "
                        "cell; it MISSED a real 2-month-old incumbent across 26 queries, so "
                        "it is never the primary path.")
    p.add_argument("--shallow", action="store_true", help="3 enumeration probes instead of 4")
    p.add_argument("--dry-run", action="store_true", help="cost estimate, spends nothing")
    a = p.parse_args()

    if not INDEX.exists():
        sys.exit("no ratchet/formats.json — run: format-index.py --seed")
    idx = json.loads(INDEX.read_text())
    fi = load_format_index()

    if a.list:
        return do_list(idx)
    if not a.format:
        sys.exit("pass --format <id> (see format-index.py --list), or --list")
    fmt = idx["formats"].get(a.format)
    if not fmt:
        sys.exit(f"unknown format '{a.format}'. format-index.py --list")
    if not fmt.get("title_regex"):
        sys.exit(f"'{a.format}' has no title_regex — it is a VISUAL format with no title "
                 f"signature\n(see CONFOUNDS). It cannot be walked by title probing; tear it "
                 f"down by hand instead.")

    if a.markets:
        markets = [m.strip() for m in a.markets.split(",")]
        unknown = [m for m in markets if m not in fi.MARKETS]
        if unknown:
            sys.exit(f"unknown market(s): {unknown}\nSee: format-index.py --markets")
    else:
        want = ("expert", "strong") if not a.all_markets else ("expert", "strong", "general")
        markets = [m for m, c in fi.MARKETS.items() if c in want]
    # 'avoid' markets are declined by Terry and are never probed, at any flag.
    markets = [m for m in markets if fi.MARKETS.get(m) != "avoid"]

    n_calls = len(markets) if a.per_market else (3 if a.shallow else 4)
    cost = n_calls * CREDITS_PER_CALL
    print(f"format   {a.format}")
    print(f"markets  {len(markets)}  ({'all' if a.all_markets else 'expert+strong'})")
    print(f"mode     {'per-market probe' if a.per_market else 'frame enumeration'}  "
          f"({n_calls} calls)")
    print(f"region   {a.region}   window {RECENCY_MONTHS}mo   cost {cost} credits "
          f"(~${cost * 0.00475:.2f})\n")
    if a.dry_run:
        if a.per_market:
            for m in markets:
                print(f"  {fi.MARKETS[m]:<8} {m:<28} → \"{probe_query(fmt, MARKET_TERMS.get(m,[m])[0])}\"")
        else:
            print(f"  enumeration phrase → \"{frame_phrase(fmt)}\"")
            print(f"  regex              → {fmt['title_regex']}")
            print(f"  binned into {len(markets)} markets by audience terms")
        print("\n--dry-run: nothing spent.")
        return

    rows = run(fmt, markets, a, fi) if a.per_market else run_enumerate(fmt, markets, a, fi)
    report(fmt, rows, fi)

    fmt["markets_occupied"] = {r["market"]: {k: r[k] for k in
                               ("verdict", "per_video", "best_views", "latest", "n_matches",
                                "n_results", "median_runtime_min", "slot_anchors")}
                               for r in rows}
    fmt["grid_measured"] = dt.date.today().isoformat()
    fmt["grid_region"] = a.region
    INDEX.write_text(json.dumps(idx, indent=1))

    RATCHET.mkdir(parents=True, exist_ok=True)
    out = RATCHET / f"bendmap-{a.format}-{dt.date.today().isoformat()}.csv"
    cols = ["market", "competence", "verdict", "per_video", "median_views", "best_views",
            "best_title", "best_channel", "best_subs", "latest", "n_matches", "n_results",
            "median_runtime_min", "reachable_hits", "region", "query"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
