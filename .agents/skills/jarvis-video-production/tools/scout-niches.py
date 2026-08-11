#!/usr/bin/env python3
"""
scout-niches.py — niche-agnostic demand SCOUT over vidIQ's channel index.

    python3 scout-niches.py --dry-run          # cost estimate only, spends nothing
    python3 scout-niches.py                    # full sweep -> CSV + niche roll-up
    python3 scout-niches.py --production any   # include non-faceless channels
    python3 scout-niches.py --min-avg-views 50000

WHY THIS EXISTS
    outlier-ratchet.py answers "what is beating its own distribution INSIDE the 26 query
    stems we hardcoded." It is niche-agnostic in its MATH and niche-locked in its SEED.
    This script is the other half: it asks "which niches are winning at a size we can
    reach, in a production mode we can actually execute" -- with no subject filter at all.

    NICHES ARE AN OUTPUT OF THIS SYSTEM, NOT AN INPUT TO IT. Find where the people are,
    then decide what to make -- never the reverse. That inversion is the governing rule
    of the studio's demand layer; see ai-film-studio/docs/STUDIO-ROADMAP.md "SCOPE".

MARKET AXES (P1a, added 2026-08-08)
    The columns above answer "what will get watched". The _implied_rpm / _tier1_geo /
    _runtime_min columns answer the DIFFERENT and UPSTREAM question "which market should
    the studio serve at all". Category is deliberately not one of them: the 2026-08-07
    survey found niche a weak predictor because these axes cut ACROSS categories.
    Validated on the 647-channel 2026-08-08 survey, costing zero extra credits:
        tier-1 geo   -> implied RPM  $1.19 median vs $0.14 rest   (8.5x, n=51/136)
        by country   -> US $1.26 vs India $0.04                   (31x, n=30 each)
        runtime >=10m -> $21 median per video vs $6-8 under 10m   (~3.5x, n=104/242)

    Measured 2026-08-08, first run: personal finance was independently confirmed by two
    instruments that share no code (our adjacent lane had it at 38.3x / 43.9x; vidIQ's
    index surfaced 72x-1068x in the same territory). That corroboration is the pattern
    this script exists to find again.

DIVISION OF LABOUR (settled 2026-08-08 after calibration)
    vidIQ supplies BREADTH -- it indexes channels our search stems can never reach.
    OUR DOCTRINE supplies RANKING -- vidIQ ranks by percent subscriber growth, which
    saturates (~500% cap) and surfaces 2k-sub channels averaging 1k views. We re-rank
    locally on avgViews/subs, exactly as outlier-ratchet.py does (views/subs, line 291).
    Verified: vidIQ's own top-5 "breakout" list re-ordered completely under our metric --
    its headline pick scored 12.7x, its footnote scored 81.5x.

CONFOUNDS -- read before trusting a column
    PERCENT GROWTH IS UNUSABLE. subsGrowth1y returns values like 243233% because the
        channel started from ~zero. It is arithmetic noise, not durability. We ignore
        every *Growth* field for ranking and derive durability from publishedAt +
        absolute trajectory instead. Do not reintroduce a growth-percentage filter.
    AGE CONFOUND (same as outlier-ratchet.py:61). Lifetime views accumulate; subscriber
        count is a CURRENT snapshot. Young channels therefore score LOW on lifetime
        views/subs. We rank on avgViews/subs (per-video), which is far less age-sensitive,
        and carry lifetime views/subs only as a secondary column.
    NICHE GRANULARITY. vidIQ's `niche` is very fine ("Origami", "Comic Dubs", "Military
        Humor"). A single 50-row call rolls up to almost nothing. That is why this script
        STRATIFIES across subscriber bands to accumulate a few hundred channels before
        aggregating. Roll-ups below MIN_NICHE_N are suppressed, not shown as weak signal.
    EARNINGS ARE ESTIMATES. estimatedEarnings is vidIQ's model, not observed revenue.
        Treat it as a ceiling ORDERING, not a forecast. It is still the only ceiling
        signal available -- no free source prices a niche.

CREDITS
    Every channel_search call costs 5 credits from the shared vidIQ pool (2,000/month
    on the current plan, resets monthly). A default sweep is 4 calls = 20 credits.
    Check the balance any time with:  python3 scout-niches.py --balance   (free)
"""

import argparse, csv, datetime as dt, json, os, re, statistics as st, sys, time, urllib.request
from collections import defaultdict

PACE_SECONDS = 1.5         # gap between calls; vidIQ 429s a tight 24-call loop

# --- doctrine constants: kept identical to outlier-ratchet.py so the two agree -------
#
# CANONICAL HOME. market-gate.py and channel-outliers.py both IMPORT these rather than
# restating them. They diverged once already: channel-outliers used a cadence ceiling of
# 12 while market-gate and this file used 15, so a channel uploading 13 times a month was
# an aggregation farm to one tool and legitimate production to the other. Two copies of a
# threshold is how doctrine and build drift apart -- change a number here, nowhere else.
MIN_SUBS      = 1_000      # below this, any ratio is noise
BAND_SUBS     = 300_000    # "reachable" ceiling for a channel starting from cold
MIN_AVG_VIEWS = 20_000     # per-video reach floor; kills the 500%-growth artifact
MIN_NICHE_N   = 3          # a roll-up needs this many channels or it is not reported
MIN_EARNINGS  = 300        # est. monthly USD; the axis that separates a business from a farm
MIN_AGE_MONTHS = 6         # younger than this and there is no trajectory to read
MAX_UPLOADS_MO = 15        # above this it is aggregation/reposting, not production

# Tier-1 ad markets: where advertisers actually bid. Used only as an EXPLANATORY flag --
# the continuous money signal is _implied_rpm. Kept deliberately short; adding marginal
# markets here would blur the one axis it exists to make legible.
TIER1_COUNTRIES = {"US", "CA", "GB", "AU", "NZ", "IE", "DE", "AT", "CH",
                   "NL", "SE", "NO", "DK", "FI", "BE", "FR", "JP", "SG"}

# Subscriber strata. One call per band beats the hard limit=50 cap and, more importantly,
# stops the biggest channels from crowding out the small reachable ones we actually want.
BANDS = [(1_000, 5_000), (5_000, 20_000), (20_000, 80_000), (80_000, 300_000)]

# --wide: the SURVEY configuration, for establishing category baselines rather than
# answering a question. vidIQ hard-caps limit=50, so a single sort returns only the top
# 50 by that key -- which is a biased sample, not a census. Finer bands plus multiple
# sort keys is the only way to accumulate enough channels per category for a median to
# mean anything. Built 2026-08-08 after the narrow sweep produced categories at n=4.
WIDE_BANDS = [(1_000, 3_000), (3_000, 6_000), (6_000, 12_000), (12_000, 25_000),
              (25_000, 50_000), (50_000, 100_000), (100_000, 180_000), (180_000, 300_000)]
# viewsGrowth30d is the least efficient sort (19-37 new channels per call, vs ~50 for the
# other two, measured 2026-08-08). It was briefly dropped to "save credits" -- a mistake:
# credits cost $0.00475 each, so those 8 calls are 19 CENTS and they buy ~180 channels.
# The binding constraint is the 400-calls/month pool and the ~20-rapid-call rate limit,
# NOT money. Optimise for coverage; only drop a sort if the monthly pool is actually tight.
WIDE_SORTS = ["subsGrowth30d", "subscriberCount", "viewsGrowth30d"]

URL      = "https://mcp.vidiq.com/mcp"
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
OUT_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ratchet")
_SESSION = {}


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
    if "data:" in raw[:200]:                       # streamable-HTTP SSE framing
        for ln in raw.splitlines():
            if ln.startswith("data:"):
                try:
                    return json.loads(ln[5:].strip())
                except json.JSONDecodeError:
                    pass
    return json.loads(raw)


def call(tool, args, retries=4):
    """Returns the parsed payload, or {"_error": ...}. NEVER exits -- a mid-sweep abort
    burns every credit already spent and writes nothing. Learned the hard way 2026-08-08:
    a 429 on call 21 of 24 threw away 105 credits of collected channels."""
    if "id" not in _SESSION:
        _rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                            "clientInfo": {"name": "jarvis-scout", "version": "1.0"}})
        _rpc("notifications/initialized", {}, notify=True)
    res = None
    for attempt in range(retries):
        res = _rpc("tools/call", {"name": tool, "arguments": args})
        code = res.get("_http_error") if isinstance(res, dict) else None
        if code != 429:
            break
        wait = PACE_SECONDS * (2 ** attempt) * 4        # 6s, 12s, 24s, 48s
        print(f"    429 rate-limited; backing off {wait:.0f}s (attempt {attempt+1}/{retries})")
        time.sleep(wait)
    if isinstance(res, dict) and "_http_error" in res:
        return {"_error": f"HTTP {res['_http_error']}: {res.get('_body','')[:100]}"}
    out = []
    for c in res.get("result", {}).get("content", []):
        if c.get("type") == "text":
            # strict=False is REQUIRED. Channel descriptions carry raw control characters
            # (unescaped newlines/tabs); strict parsing rejects the whole payload and the
            # band silently vanishes from the sweep. Cost us 50 channels on 2026-08-08.
            try:
                out.append(json.loads(c["text"], strict=False))
            except json.JSONDecodeError:
                out.append(c["text"])
    return out[0] if len(out) == 1 else out


def enrich(c):
    """Attach our metrics. vidIQ's ranking is not our ranking -- this is where ours lands."""
    subs   = c.get("subscriberCount") or 0
    avg    = c.get("avgViews") or 0
    life   = c.get("viewCount") or 0
    c["_per_video"] = (avg / subs) if subs else 0.0     # PRIMARY -- least age-sensitive
    c["_lifetime"]  = (life / subs) if subs else 0.0    # secondary, age-confounded
    age_days = None
    pub = c.get("publishedAt")
    if pub:
        try:
            born = dt.datetime.fromisoformat(str(pub).replace("Z", "+00:00"))
            age_days = (dt.datetime.now(dt.timezone.utc) - born).days
        except ValueError:
            pass
    c["_age_days"] = age_days
    # CADENCE. Use the ACTUAL trailing-30-day upload counts, never videoCount/age.
    # videoCount/age is a LIFETIME AVERAGE and it is wrong the moment a channel changes
    # pace -- which is 63% of the 2026-08-08 survey (361 of 574 differ by >3x). It made
    # Moe Phone Case DIY read as 1.1 uploads/month when it actually posts ~39, inflating
    # its $/video by 35x AND hiding it from the CHURN slop filter (which triggers at >12).
    # Caveat: vidIQ's 30d counts lag the index too (13 vs a true 39 for that channel), so
    # treat cadence as a lower bound. It is still far closer than the lifetime average.
    d30 = (c.get("longVideoCount30d") or 0) + (c.get("shortVideoCount30d") or 0)
    c["_vids_per_mo"] = float(d30) if d30 else (
        (c.get("videoCount") or 0) / max(age_days / 30.0, 1.0) if age_days else None)
    c["_cadence_src"] = "30d" if d30 else "lifetime-avg"
    # REVENUE PER UNIT OF PRODUCTION EFFORT -- the metric a studio actually optimises, and
    # the one that survived the 2026-08-08 survey. Total earnings favours big channels;
    # outlier score favours clip farms earning $0; category medians barely move. This is
    # the only measure where a 5,570-sub comedy channel and a 54k-sub history channel are
    # directly comparable ($2,165 vs $2,825 per video).
    vpm = c["_vids_per_mo"]
    c["_usd_per_video"] = ((c.get("estimatedEarnings") or 0) / max(vpm, 0.5)) if vpm else None

    # ---- MARKET AXES (P1a). Added 2026-08-08. -------------------------------------
    # These answer "which market should the studio serve", which is a DIFFERENT question
    # from "what will get watched" and is upstream of it. See ai-film-studio/docs/
    # STUDIO-ROADMAP.md "P1a - Market selection". All three are pure arithmetic on fields
    # already in the payload -- they cost ZERO extra credits.
    #
    # IMPLIED RPM is the load-bearing one: it collapses audience affluence, geography and
    # advertiser-category adjacency into one number. Verified on the 2026-08-08 survey it
    # separates 31x by country (US median $1.26 vs India $0.04, n=30 each).
    #   TREAT AS AN ORDERING, NEVER A FORECAST. Absolute values run far below real-world
    #   RPMs because vidIQ's earnings model is conservative, and it is computable for only
    #   ~29% of rows (187/647) -- the rest lack 30d view counts. A null here means MISSING,
    #   not zero; never coalesce it to 0.0 or the poor-data channels rank as poor markets.
    m_views = (c.get("longViewCount30d") or 0) + (c.get("shortViewCount30d") or 0)
    earn = c.get("estimatedEarnings") or 0
    # 10k floor: below it the ratio is dominated by rounding in vidIQ's earnings estimate.
    c["_implied_rpm"] = (earn / (m_views / 1000.0)) if (earn and m_views > 10_000) else None

    # GEOGRAPHY. Tier-1 = the ad markets that actually bid. This is a coarse flag on
    # purpose; the continuous signal is _implied_rpm, and this exists to explain it.
    c["_tier1_geo"] = (c.get("country") or "").upper() in TIER1_COUNTRIES

    # RUNTIME TOLERANCE. Does this audience sit still? Measured 2026-08-08: 15-30 min
    # videos earn ~4x more per video than sub-3-min. Length only pays where the audience
    # tolerates it, so this is an audience property, not a production choice.
    secs = c.get("longAvgDuration30d") or c.get("longAvgDuration1y")
    c["_runtime_min"] = (secs / 60.0) if secs else None
    return c


def sweep(faceless, min_avg_views, since, limit, min_earnings, bands, sorts,
          categories=None, country=None):
    seen, calls = {}, 0
    for lo, hi in bands:
        for sort_key in sorts:
            args = {
                "subscriberCountMin": lo, "subscriberCountMax": hi,
                "avgViewsMin": min_avg_views,
                "lastVideoPublishedAfter": since,
                "sort": sort_key, "limit": limit,
            }
            # TARGETING, added 2026-08-11. This tool was built as a pure attribute survey with
            # "no subject filter at all", which is right for establishing baselines and WRONG
            # when a specific market needs evidence. market-gate BLOCKED on "US Business, 0 of
            # 647 channels" — not a verdict on the market, just a sweep that never looked there.
            # An untargeted re-run would resample the same growth-sorted population (which
            # entertainment dominates) and very likely return zero again. Cheaper and honest to
            # aim it.
            if categories:
                args["mainCategory"] = categories
            if country:
                args["country"] = [country]
            if min_earnings:
                args["estimatedEarningsMin"] = min_earnings
            if faceless is not None:
                args["faceless"] = faceless
            r = call("vidiq_channel_search", args)
            calls += 1
            time.sleep(PACE_SECONDS)
            if isinstance(r, dict) and "_error" in r:
                print(f"  {lo:>6,}-{hi:<7,} {sort_key:16} -> {r['_error']}  (continuing)")
                continue
            # The API returns a bare string on refusal/empty ("no channels matched...",
            # quota messages). Do not let one band abort the sweep -- report and continue.
            if not isinstance(r, dict):
                print(f"  {lo:>6,}-{hi:<7,} {sort_key:16} -> API said: {str(r)[:70]}")
                continue
            got = r.get("channels") or r.get("results") or []
            new = 0
            for c in got:
                if c.get("channelId") not in seen:
                    seen[c["channelId"]] = enrich(c)
                    new += 1
            print(f"  {lo:>6,}-{hi:<7,} {sort_key:16} -> {len(got):>3} rows, "
                  f"{new:>3} new  ({len(seen)} unique)")
    return list(seen.values()), calls


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="cost estimate only, spends nothing")
    p.add_argument("--balance", action="store_true", help="show vidIQ credit balance (free)")
    p.add_argument("--production", choices=["faceless", "any"], default="faceless",
                   help="faceless (default) or any -- 'any' includes avatar/on-camera channels")
    p.add_argument("--min-avg-views", type=int, default=MIN_AVG_VIEWS)
    p.add_argument("--limit", type=int, default=50, help="rows per band (vidIQ caps at 50)")
    p.add_argument("--active-within-days", type=int, default=30)
    # THE FARM FILTERS. Measured 2026-08-08: without these the top of the ranking is
    # clip/meme/compilation reposters -- 1-2 months old, 20-33 uploads/month, huge
    # views-per-sub, and $0 estimated earnings. High outlier score, no business.
    p.add_argument("--min-earnings", type=int, default=MIN_EARNINGS,
                   help="minimum estimated monthly USD; 0 disables (surfaces farms)")
    p.add_argument("--min-age-months", type=int, default=MIN_AGE_MONTHS,
                   help="reject channels younger than this; a farm spikes then dies")
    p.add_argument("--max-uploads-per-month", type=int, default=MAX_UPLOADS_MO,
                   help="above this cadence it is an aggregation operation, not a studio")
    p.add_argument("--category", action="append",
                   help="vidIQ mainCategory to target (repeatable). Without it this is an "
                        "UNTARGETED baseline survey — see the note in sweep().")
    p.add_argument("--country", help="ISO-2 country of the CHANNEL (not the audience)")
    p.add_argument("--wide", action="store_true",
                   help="SURVEY mode: 8 bands x 3 sorts, for establishing category baselines")
    a = p.parse_args()

    bands = WIDE_BANDS if a.wide else BANDS
    sorts = WIDE_SORTS if a.wide else ["subsGrowth30d"]
    # In survey mode the earnings floor is applied at ANALYSIS time, not in the query.
    # Filtering on earnings server-side biases the baseline we are trying to establish
    # (it also collapsed the 1k-5k band to 6 rows). Farms are handled by age + cadence.
    if a.wide and a.min_earnings == MIN_EARNINGS:
        a.min_earnings = 0

    if a.balance:
        b = call("vidiq_balance", {})
        print(f"vidIQ credits: {b.get('totalCredits'):,} / {b.get('maxRenewableCredits'):,}"
              f"  (resets {b.get('renewableResetsAt','?')[:10]})")
        return

    if a.dry_run:
        n = len(bands) * len(sorts)
        print(f"{n} calls x 5 credits = {n*5} credits   (mode: {'WIDE survey' if a.wide else 'narrow sweep'})")
        print(f"{len(bands)} bands x {len(sorts)} sorts: {sorts}")
        print(f"bands: {bands}")
        print(f"faceless={a.production}  min_avg_views={a.min_avg_views:,}  min_earnings={a.min_earnings}")
        return

    since = (dt.date.today() - dt.timedelta(days=a.active_within_days)).isoformat()
    faceless = True if a.production == "faceless" else None
    print(f"SCOUT sweep  production={a.production}  avgViews>={a.min_avg_views:,}  active since {since}")
    chans, calls = sweep(faceless, a.min_avg_views, since, a.limit, a.min_earnings, bands, sorts, a.category, a.country)
    raw_n = len(chans)
    if a.min_age_months:
        chans = [c for c in chans
                 if c["_age_days"] is None or c["_age_days"] >= a.min_age_months * 30]
    if a.max_uploads_per_month:
        chans = [c for c in chans
                 if c["_vids_per_mo"] is None or c["_vids_per_mo"] <= a.max_uploads_per_month]
    print(f"\n{raw_n} unique channels from {calls} calls ({calls*5} credits)")
    print(f"{len(chans)} survived the farm filters "
          f"(age>={a.min_age_months}mo, uploads<={a.max_uploads_per_month}/mo, ${a.min_earnings}+/mo)\n")

    chans.sort(key=lambda c: -c["_per_video"])
    print(f"{'channel':26} {'niche':28} {'subs':>7} {'avgV':>8} {'/sub':>7} {'age':>5} {'v/mo':>5} {'$/mo':>7}")
    print("-" * 108)
    for c in chans[:25]:
        age = f"{c['_age_days']//30}m" if c["_age_days"] else "?"
        vpm = f"{c['_vids_per_mo']:.0f}" if c["_vids_per_mo"] else "?"
        print(f"{str(c.get('channelTitle'))[:26]:26} {str(c.get('niche'))[:28]:28} "
              f"{c.get('subscriberCount',0):>7,} {(c.get('avgViews') or 0):>8,.0f} "
              f"{c['_per_video']:>6.1f}x {age:>5} {vpm:>5} {(c.get('estimatedEarnings') or 0):>7,.0f}")

    # Roll up on mainCategory, NOT niche. Measured 2026-08-08: vidIQ's `niche` is so
    # granular ("Origami", "Comic Dubs", "Police Drama Shorts") that 44 of 45 niches fell
    # below n=3 at 106 channels -- the roll-up reported one row and hid everything. Niche
    # is the right label for a single channel and the wrong unit for aggregation.
    agg = defaultdict(list)
    for c in chans:
        agg[c.get("mainCategory") or c.get("niche") or "?"].append(c)
    thresh = 8 if a.wide else MIN_NICHE_N
    rows = [(k, v) for k, v in agg.items() if len(v) >= thresh]
    print(f"\n=== CATEGORY BASELINES (n>={thresh}; {len(agg)-len(rows)} thinner categories suppressed) ===")
    if not rows:
        print("  none reached the threshold -- widen the sweep or lower --min-avg-views")
    # 'paid' = channels with a non-zero earnings estimate. Reporting median-of-ALL and
    # median-of-PAID separately matters: a category can look poor only because most of
    # its channels have no earnings estimate, which is missing data, not zero revenue.
    print(f"{'category':30} {'n':>3} {'paid':>5} {'med /sub':>9} {'med subs':>9} {'med $ (paid)':>13}")
    print("-" * 76)
    for k, v in sorted(rows, key=lambda kv: -st.median([c["_per_video"] for c in kv[1]])):
        paid = [c.get("estimatedEarnings") or 0 for c in v if (c.get("estimatedEarnings") or 0) > 0]
        print(f"{k[:30]:30} {len(v):>3} {len(paid):>5} "
              f"{st.median([c['_per_video'] for c in v]):>8.1f}x "
              f"{st.median([c.get('subscriberCount') or 0 for c in v]):>9,.0f} "
              f"{(st.median(paid) if paid else 0):>13,.0f}")

    # ---- P1a MARKET ROLL-UP ------------------------------------------------------
    # Rolled up on COUNTRY, not category. The whole point of the market layer is that the
    # axes cut ACROSS categories -- a history channel and a comedy channel can sit in the
    # same market bracket. Rolling this on category would re-import the exact assumption
    # the 2026-08-07 finding refuted ("niche is a weak predictor").
    rpm_rows = [c for c in chans if c["_implied_rpm"] is not None]
    print(f"\n=== MARKET AXES (P1a) — implied RPM computable for {len(rpm_rows)}/{len(chans)} "
          f"({100*len(rpm_rows)//max(len(chans),1)}%; the rest lack 30d view counts) ===")
    if not rpm_rows:
        print("  no channel had both earnings and 30d view counts -- market axes unavailable")
    else:
        print("  ORDERING ONLY -- vidIQ's earnings model is conservative; these are not real RPMs.")
        geo = defaultdict(list)
        for c in rpm_rows:
            geo[(c.get("country") or "?").upper()].append(c)
        print(f"\n{'country':>8} {'t1':>3} {'n':>4} {'med RPM':>9} {'med run':>9} {'med /sub':>9} {'med $/vid':>10}")
        print("-" * 60)
        for k, v in sorted(geo.items(), key=lambda kv: -st.median([c["_implied_rpm"] for c in kv[1]])):
            if len(v) < 5:
                continue
            runs = [c["_runtime_min"] for c in v if c["_runtime_min"]]
            uvs  = [c["_usd_per_video"] for c in v if c["_usd_per_video"]]
            print(f"{k:>8} {'Y' if k in TIER1_COUNTRIES else '·':>3} {len(v):>4} "
                  f"${st.median([c['_implied_rpm'] for c in v]):>8.2f} "
                  f"{(st.median(runs) if runs else 0):>8.1f}m "
                  f"{st.median([c['_per_video'] for c in v]):>8.1f}x "
                  f"{(st.median(uvs) if uvs else 0):>10,.0f}")

        # The studio's actual target: high monetization density AND a reachable size AND a
        # runtime the audience tolerates. Not "the best niche" -- the best MARKET BRACKET.
        top = sorted(rpm_rows, key=lambda c: -c["_implied_rpm"])[:15]
        print(f"\n--- highest monetization density (reachable, <= {BAND_SUBS:,} subs) ---")
        print(f"{'channel':26} {'category':20} {'country':>7} {'RPM':>7} {'run':>6} {'subs':>8}")
        print("-" * 80)
        for c in top:
            print(f"{str(c.get('channelTitle'))[:26]:26} {str(c.get('mainCategory'))[:20]:20} "
                  f"{str(c.get('country') or '?'):>7} ${c['_implied_rpm']:>6.2f} "
                  f"{(c['_runtime_min'] or 0):>5.1f}m {c.get('subscriberCount',0):>8,}")

    os.makedirs(OUT_DIR, exist_ok=True)
    # Mode belongs in the filename: a --production any run and a faceless run are different
    # populations, and writing both to scout-<date>.csv silently overwrote the first.
    tag = f"{a.production}{'-wide' if a.wide else ''}"
    path = os.path.join(OUT_DIR, f"scout-{dt.date.today().isoformat()}-{tag}.csv")
    # Duration + per-format counts are load-bearing for PRODUCIBILITY: a channel earning
    # $2,800/video on 20-minute documentaries is a different business from one earning it
    # on 3-minute cutdowns. The 2026-08-08 survey omitted them and could not tell the two
    # apart -- which is exactly the axis a studio needs. Never drop these again.
    cols = ["channelTitle", "handle", "niche", "subNiches", "mainCategory", "nicheConfidence",
            "subscriberCount", "avgViews", "viewCount", "videoCount", "estimatedEarnings",
            "country", "languages", "isFaceless", "channelType", "breakoutChannel",
            "publishedAt", "lastVideoPublished", "channelId",
            "longAvgDuration30d", "longAvgDuration1y", "shortAvgDuration30d",
            "longVideoCount30d", "shortVideoCount30d",
            "longViewCount30d", "shortViewCount30d",
            "subsGrowth30d", "viewsGrowth30d",
            "_per_video", "_lifetime", "_age_days", "_vids_per_mo", "_cadence_src", "_usd_per_video",
            # P1a market axes. _implied_rpm is blank when uncomputable -- that is MISSING
            # data, not a zero. Do not fill it in downstream.
            "_implied_rpm", "_tier1_geo", "_runtime_min"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for c in chans:
            w.writerow(c)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
