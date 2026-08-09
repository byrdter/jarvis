#!/usr/bin/env python3
"""
channel-outliers.py — find channels beating their SIZE-CONTROLLED peers on revenue per
video, in ANY niche. Then hand you the facts needed to reverse-engineer them.

    python3 channel-outliers.py                        # latest sweep, ranked outliers
    python3 channel-outliers.py --csv ratchet/scout-2026-08-08-faceless-wide.csv
    python3 channel-outliers.py --min-multiple 3 --top 40
    python3 channel-outliers.py --teardown @globaldatalab24
    python3 channel-outliers.py --baselines            # show the peer cells only

WHY THIS EXISTS -- and why it ranks CHANNELS, not niches
    The 2026-08-08 survey (574 faceless + 647 all-mode channels) measured category
    medians for revenue-per-video and found them clustered and low: Sport $277,
    Action game $277, Music $239, RPG $94, Hobby $78, Film $74, Entertainment $66,
    Lifestyle $44. Individual channels INSIDE those same categories reach $1,000+.
    Total Track and Time earns 20x the median of its own category.

    WITHIN-CATEGORY VARIANCE DWARFS BETWEEN-CATEGORY DIFFERENCE. Picking the right
    niche explains little; being the right channel inside one explains a lot. A tool
    that ranked niches would have pointed at Sport and still missed the channel earning
    20x inside it. So this ranks channels and treats the niche as an OUTPUT.

THE METRIC
    $/video = estimated monthly earnings / true monthly upload count.
    Revenue per unit of production effort -- what a studio actually optimises. Total
    earnings favours whoever is biggest; outlier score (views/subs) favours clip farms
    earning $0. $/video is the only measure on which a 5,570-sub comedy channel and a
    54k-sub history channel are directly comparable.

FOUR CORRECTIONS THIS TOOL HARD-CODES (each cost a wrong conclusion on 2026-08-08)
    1. CADENCE FROM 30d COUNTS, NEVER videoCount/age. The lifetime average is wrong the
       moment a channel changes pace -- 63% of the survey differed by >3x. It made a
       daily 2-hour-ASMR operation read as 1.1 uploads/month and inflated its $/video
       by 35x. vidIQ's own 30d counts lag too, so cadence is a LOWER BOUND.
    2. COMPARE WITHIN A SIZE BAND. A category median pooled across all sizes is not a
       peer group. Every multiple here is against (category x subscriber band).
    3. NEVER COMPARE ACROSS SWEEPS. Two sweeps of the same index overlapped by 6%; a
       cross-sweep difference is a sampling artifact, not a finding. One CSV at a time.
    4. ABSOLUTE FLOOR AS WELL AS MULTIPLE. 10x a $5 baseline is $50 and means nothing.
       A channel must clear MIN_USD_PER_VIDEO in absolute terms to rank.

CONFIDENCE -- read this before acting on any single row
    Spot-checked against the YouTube API on 2026-08-08: durations were within +/-50% of
    truth on 10 of 12 sampled channels (~83%), and earnings estimates were defensible
    where checked ($4.77 RPM on 7.58M real monthly views). But single-channel figures
    were wrong often enough that every row carries a flag. VERIFY A CANDIDATE AGAINST
    YOUTUBE BEFORE BUILDING ANYTHING ON IT -- this tool nominates, it does not confirm.
"""

import argparse, csv, datetime as dt, glob, json, os, re, statistics as st, sys, urllib.parse, urllib.request
from collections import defaultdict

# --- YouTube Data API: the ONLY external check available -------------------------------
# vidIQ's channel_search gives no per-video distribution, and its avgViews is a MEAN --
# one viral hit destroys it. Kem Rogue and 1C2 both ranked well on avgViews while their
# TYPICAL video gets fewer views than they have subscribers. Consistency therefore cannot
# be measured at sweep time; it needs video-level data, which is what --verify pulls.
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
# CONSISTENCY IS MEASURED WITH AN INTERQUARTILE RATIO, NOT max/median.
# max/median is SAMPLE-SIZE DEPENDENT and therefore worthless: the larger the sample, the
# likelier it contains a big outlier, so the verdict drifts with how many videos you happen
# to fetch. Measured 2026-08-08 on choopo twoopo -- 9.0x at n=30, 23.7x at n=40, same
# channel, opposite conclusions. p75/p25 is robust in both tails and stable as n grows.
SPREAD_LOTTERY    = 12.0  # p75/p25 at or above this = wildly uneven performance
SPREAD_CONSISTENT = 5.0   # at or below this = a dependable performer
MIN_LONG_VIDEOS   = 6     # fewer than this and quartiles are meaningless

# JUDGE THE MATURE ERA, NOT THE APPRENTICESHIP.
# Channels improve. Pooling a creator's first fumbling year with their current work
# measures the learning curve, not the format. ExtraMint scored 26.9x spread (LOTTERY)
# over its lifetime and 8.1x over its mature era -- and its median view count DOUBLED,
# from 125,957 to 260,775 -- because its 2023 videos predate the repeatable title formula
# it found in Feb 2024. Same failure class as the cadence bug: a lifetime aggregate
# applied to a channel that changed. Lifetime figures are still reported alongside.
MATURE_MONTHS = 24


def yt_key():
    k = os.environ.get("YOUTUBE_API_KEY")
    if k:
        return k
    for line in open(ENV_PATH):
        if line.startswith("YOUTUBE_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No YOUTUBE_API_KEY (env or jarvis/.env).")


def yt(endpoint, **params):
    params["key"] = yt_key()
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?{urllib.parse.urlencode(params)}"
    return json.load(urllib.request.urlopen(url))


def iso_secs(iso):
    """ISO-8601 duration -> seconds.

    THE `T` IS LOAD-BEARING. A pattern of P(\\d+H)?(\\d+M)?(\\d+S)? without it silently
    returns 0 for every value, because real durations look like 'PT19M8S'. That produced
    a full column of 0m00 runtimes on 2026-08-08 before anyone noticed.
    """
    m = re.match(r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = [int(x) if x else 0 for x in m.groups()]
    return d * 86400 + h * 3600 + mi * 60 + s


def verify_channel(handle, sample=40):
    """Video-level truth for one channel. Returns None if it cannot be measured."""
    h = handle.lstrip("@")
    try:
        ch = yt("channels", part="snippet,statistics,contentDetails", forHandle=h)["items"][0]
    except Exception:
        return {"handle": h, "error": "not found by handle"}
    subs = int(ch["statistics"].get("subscriberCount", 0) or 0)
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, token = [], None
    while len(ids) < sample:
        page = yt("playlistItems", part="contentDetails", playlistId=pl,
                  maxResults=min(50, sample - len(ids)), **({"pageToken": token} if token else {}))
        ids += [i["contentDetails"]["videoId"] for i in page["items"]]
        token = page.get("nextPageToken")
        if not token:
            break
    longs = []
    for i in range(0, len(ids), 50):
        for v in yt("videos", part="statistics,contentDetails,snippet", id=",".join(ids[i:i+50]))["items"]:
            dur = iso_secs(v["contentDetails"]["duration"])
            if dur > 180:                       # exclude Shorts; a different business
                longs.append((int(v["statistics"].get("viewCount", 0) or 0), dur,
                              v["snippet"]["title"], v["snippet"]["publishedAt"][:10]))
    if len(longs) < MIN_LONG_VIDEOS:
        return {"handle": h, "title": ch["snippet"]["title"], "subs": subs,
                "error": f"only {len(longs)} long-form videos"}
    def summarise(sample):
        vs = sorted(v for v, _, _, _ in sample)
        q = st.quantiles(vs, n=4)                       # [p25, p50, p75]
        spread = q[2] / max(q[0], 1)                    # robust, stable in n
        return {"n": len(vs), "median": st.median(vs), "min": vs[0], "max": vs[-1],
                "p25": q[0], "p75": q[2], "spread": spread,
                "med_subs": st.median(vs) / subs if subs else 0,
                "hit_rate": sum(1 for v in vs if subs and v >= subs) / len(vs),
                "runtime": st.median([d for _, d, _, _ in sample]),
                "verdict": ("LOTTERY" if spread >= SPREAD_LOTTERY
                            else "consistent" if spread <= SPREAD_CONSISTENT else "mixed")}

    cutoff = (dt.date.today() - dt.timedelta(days=MATURE_MONTHS * 30)).isoformat()
    mature = [v for v in longs if v[3] >= cutoff]
    life = summarise(longs)
    # Headline the mature era when there is enough of it; otherwise say so rather than
    # silently falling back, so nobody reads a lifetime number as a current one.
    if len(mature) >= MIN_LONG_VIDEOS:
        head, era = summarise(mature), f"since {cutoff[:7]}"
    else:
        head, era = life, "lifetime (too few recent)"
    return {"handle": h, "title": ch["snippet"]["title"], "subs": subs,
            "lifetime": life, "era": era,
            "last": max(p for _, _, _, p in longs), "videos": longs, **head}

TOOLS   = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(TOOLS, "ratchet")


def _load_sibling(filename):
    """Import a hyphenated sibling module. Same trick market-gate.py uses to reach
    scout-niches.py -- 'scout-niches' is not a legal identifier, so importlib it is.
    Both siblings guard their entry points with __main__, so importing runs nothing."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        filename.replace("-", "_").removesuffix(".py"), os.path.join(TOOLS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Peer cells. Same bands used for the size-controlled runtime replication, which held
# in both strata -- these are the sizes at which channels genuinely compete.
SUB_BANDS = [(1_000, 10_000, "1k-10k"), (10_000, 30_000, "10k-30k"),
             (30_000, 80_000, "30k-80k"), (80_000, 300_000, "80k-300k")]

MIN_CELL_N        = 5     # below this a (category x band) median is noise -> fall back
MIN_MULTIPLE      = 2.0   # must beat its own peer group by this much

# SHARED THRESHOLDS ARE IMPORTED, NEVER RESTATED. MAX_CADENCE was locally 12 here while
# scout-niches.py and market-gate.py both used 15 -- a channel at 13 uploads/month was a
# farm to this tool and production to the other two. Reconciled 2026-08-09 by importing.
_scout = _load_sibling("scout-niches.py")
_gate  = _load_sibling("market-gate.py")
MAX_CADENCE       = _scout.MAX_UPLOADS_MO      # 15/mo -- aggregation, not production
BAND_SUBS         = _scout.BAND_SUBS           # 300k -- "reachable from cold"
MIN_USD_PER_VIDEO = _gate.MIN_USD_PER_VID      # 150 -- calibrated to population p75 (148.6)

# MONETIZATION FLOOR. $/video says nothing about whether the AUDIENCE is worth serving:
# market-gate's --list shows US Entertainment at $4.19 implied RPM against IN Entertainment
# at $0.01 -- same category, ~400x apart. Ranking on $/video alone will happily top-rank a
# channel whose viewers monetize at a cent per thousand. Implied RPM is computable for only
# ~29% of rows, so a MISSING value is never a rejection -- it is flagged as unknown.
MIN_IMPLIED_RPM   = _gate.MIN_IMPLIED_RPM      # 1.00 -- population p75, ~the tier-1 boundary

# RPM REALITY GATE. earnings / (channel views accrued in the trailing 30 days) must land
# in a real YouTube RPM band. Catches earnings estimates that have drifted from reality.
#
# MEASUREMENT TRAP -- do NOT "verify" this with the YouTube Data API the naive way.
# longViewCount30d is views ACCRUED channel-wide in the window, including the entire back
# catalogue. Summing viewCount over videos PUBLISHED in the last 30 days measures something
# else entirely and undercounts any channel with an archive. On 2026-08-08 that mistake
# made Johnson's Small Engines look like a $53/1k impossibility (50,407 views on recent
# uploads) when vidIQ's channel-wide figure puts it at a perfectly ordinary $4.2/1k.
# Public API cannot give channel views-in-period at all -- that is owner-only Analytics --
# so this gate is INTERNAL-CONSISTENCY only, not external verification.
# Real YouTube RPM tops out near $20/1k even in premium niches.
# Only computable where vidIQ populates the 30d view counts -- 34% of rows.
RPM_MAX = 20.0
RPM_MIN = 0.20

# SLOP is a production signature, not a subject. A "fun" channel is not slop; a channel
# repackaging other people's footage, or churning AI-generated filler, is.
DERIV = ("clip", "compilation", "meme", "reaction", "highlight", "edits", "fan ",
         "best of", "funny moment", "tiktok", "repost", "stream", "celebrity",
         "gossip", "storytime")
AIGEN = re.compile(r"\bai\b.*\b(cover|music|animat\w*|stor\w+|video|art|movie|film|"
                   r"generated|voice)\b|\b(cover|music|animation|story|video|art|movie)"
                   r"\b.*\bai\b", re.I)


def num(r, k):
    try:
        return float(r.get(k) or 0)
    except (TypeError, ValueError):
        return 0.0


def band_of(subs):
    for lo, hi, lab in SUB_BANDS:
        if lo <= subs < hi:
            return lab
    return None


def prepare(rows):
    """Recompute every derived field from RAW columns.

    Deliberately ignores the CSV's own _vids_per_mo / _usd_per_video: sweeps written
    before the 2026-08-08 cadence fix carry the broken lifetime-average values, and a
    tool that silently trusts a stale derived column is how the 35x error survived.
    """
    RAW = ("subscriberCount", "avgViews", "viewCount", "videoCount", "estimatedEarnings",
           "longAvgDuration30d", "longAvgDuration1y", "shortAvgDuration30d",
           "longVideoCount30d", "shortVideoCount30d", "longViewCount30d", "shortViewCount30d")
    for r in rows:
        # Always recompute from RAW via scout.enrich() -- the one implementation of these
        # formulas. Sweeps written before the 2026-08-08 cadence fix carry a broken
        # lifetime-average _vids_per_mo, so the CSV's own derived columns are not trusted;
        # but the fix belongs in enrich(), not in a second copy of the arithmetic here.
        typed = dict(r)
        for k in RAW:
            typed[k] = num(r, k)
        typed["country"] = r.get("country") or ""
        e = _scout.enrich(typed)
        subs = num(r, "subscriberCount")
        r["_cad"]       = e["_vids_per_mo"] or 0.0
        r["_cad_src"]   = e["_cadence_src"]
        r["_usd_video"] = e["_usd_per_video"] or 0.0
        r["_dur"]       = (e["_runtime_min"] or 0.0) * 60.0      # enrich returns minutes
        r["_rpm"]       = e["_implied_rpm"]                       # None when uncomputable
        r["_tier1"]     = e["_tier1_geo"]
        r["_per_sub"]   = e["_per_video"]
        r["_band"]      = band_of(subs)
        text = f"{r.get('niche') or ''} {r.get('channelTitle') or ''}"
        flags = []
        if any(w in text.lower() for w in DERIV):
            flags.append("DERIV")
        if AIGEN.search(text):
            flags.append("AI-GEN")
        if r["_cad"] > MAX_CADENCE:
            flags.append("CHURN")
        r["_slop"] = flags
    return rows


def build_baselines(clean):
    """median $/video per (category x subscriber band), with documented fallbacks."""
    cells, bands = defaultdict(list), defaultdict(list)
    for r in clean:
        if not r["_band"]:
            continue
        cat = r.get("mainCategory") or "?"
        cells[(cat, r["_band"])].append(r["_usd_video"])
        bands[r["_band"]].append(r["_usd_video"])
    cell_med = {k: st.median(v) for k, v in cells.items() if len(v) >= MIN_CELL_N}
    band_med = {k: st.median(v) for k, v in bands.items() if len(v) >= MIN_CELL_N}
    glob_med = st.median([r["_usd_video"] for r in clean]) if clean else 0.0
    return cell_med, band_med, glob_med, {k: len(v) for k, v in cells.items()}


def peer_for(r, cell_med, band_med, glob_med):
    cat = r.get("mainCategory") or "?"
    key = (cat, r["_band"])
    if key in cell_med:
        return cell_med[key], f"{cat}/{r['_band']}"
    if r["_band"] in band_med:
        return band_med[r["_band"]], f"ALL/{r['_band']}"   # category cell too thin
    return glob_med, "GLOBAL"


def confidence(r, cell_n):
    """TWO INDEPENDENT KINDS OF DOUBT -- do not conflate them (I did, first pass).

    DATA doubt  = is this channel's OWN $/video trustworthy? Bad cadence or a missing
                  runtime means the number itself may be wrong.
    PEER doubt  = is the MULTIPLE trustworthy? A thin peer cell makes the ratio jumpy,
                  but says nothing about the channel.

    Conflating them biased the shortlist toward gaming, because gaming is the only
    category with cells thick enough to avoid the peer warning -- so every strong
    non-gaming candidate looked unreliable for a reason unrelated to its own data.
    """
    data, peer = [], []
    if r["_cad_src"] != "30d":
        data.append("cadence=lifetime")      # the exact bug that caused the 35x error
    if r["_cad"] <= 1:
        data.append("cadence<=1")            # divisor tiny -> $/video very sensitive
    if not r["_dur"]:
        data.append("no-runtime")
    if r["_rpm"] is None:
        data.append("rpm-uncheckable")       # vidIQ left the 30d view counts empty
    elif r["_rpm"] > RPM_MAX:
        data.append(f"RPM-IMPLAUSIBLE({r['_rpm']:.0f})")   # earnings almost certainly stale
    elif r["_rpm"] < RPM_MIN:
        data.append(f"rpm-low({r['_rpm']:.2f})")
    elif r["_rpm"] < MIN_IMPLIED_RPM:
        # Not a data problem -- a MARKET problem. The numbers are fine; the audience is
        # cheap. Kept separate from the data warnings so it never hides a good channel,
        # and never lets a $0.01-RPM market top the ranking unremarked.
        data.append(f"low-value-audience(${r['_rpm']:.2f}rpm)")
    if cell_n < MIN_CELL_N:
        peer.append("thin-peer-group")
    return data, peer


def print_verify(results):
    """The check that would have caught SaintBryce before it reached the user."""
    print(f"\n=== CONSISTENCY VERIFY (YouTube video-level truth) ===")
    print(f"{'channel':22} {'subs':>7} {'n':>3} {'median':>9} {'med/subs':>9} "
          f"{'p75/p25':>8} {'hit%':>5} {'run':>4} {'era':>13} {'lifetime':>10}  verdict")
    print("-" * 122)
    for r in results:
        if not r or r.get("error"):
            print(f"{(r or {}).get('title', (r or {}).get('handle','?'))[:24]:24} "
                  f"-- {(r or {}).get('error','failed')}")
            continue
        print(f"{r['title'][:22]:22} {r['subs']:>7,} {r['n']:>3} {r['median']:>9,.0f} "
              f"{r['med_subs']:>8.2f}x {r['spread']:>7.1f}x {100*r['hit_rate']:>4.0f}% "
              f"{r['runtime']/60:>3.0f}m {r['era']:>13} {r['lifetime']['spread']:>9.1f}x  {r['verdict']}"
              + ("  ⚠ typical video < subs" if r["med_subs"] < 0.5 else ""))
    good = [r for r in results if r and not r.get("error") and r["verdict"] == "consistent"]
    print(f"\n{len(good)} consistent performer(s). LOTTERY = earnings rest on a few hits and")
    print("the format is not proven; med/subs < 0.5 means the typical video underperforms the sub count.")


def latest_csv():
    c = sorted(glob.glob(os.path.join(OUT_DIR, "scout-*.csv")), key=os.path.getmtime)
    if not c:
        sys.exit("No scout-*.csv in ratchet/. Run: python3 scout-niches.py --wide")
    return c[-1]


def teardown(rows, handle):
    h = handle.lstrip("@").lower()
    match = [r for r in rows if (r.get("handle") or "").lstrip("@").lower() == h
             or h in (r.get("channelTitle") or "").lower()]
    if not match:
        sys.exit(f"'{handle}' not in this sweep.")
    r = match[0]
    print(f"\n=== TEARDOWN: {r.get('channelTitle')}  ({r.get('handle')}) ===")
    print(f"  niche          {r.get('niche')}   [{r.get('mainCategory')}]")
    print(f"  country/lang   {r.get('country')}  {r.get('languages')}")
    print(f"  subscribers    {num(r,'subscriberCount'):,.0f}   ({r['_band']})")
    print(f"  lifetime       {num(r,'viewCount'):,.0f} views over {num(r,'videoCount'):,.0f} videos")
    print(f"  avg views/vid  {num(r,'avgViews'):,.0f}   ({r['_per_sub']:.1f}x subs)")
    print(f"  cadence        {r['_cad']:.0f}/mo  [{r['_cad_src']}]  "
          f"= {num(r,'longVideoCount30d'):.0f} long + {num(r,'shortVideoCount30d'):.0f} short")
    print(f"  runtime        {r['_dur']/60:.1f} min" if r["_dur"] else "  runtime        unknown")
    print(f"  est. earnings  ${num(r,'estimatedEarnings'):,.0f}/mo  ->  ${r['_usd_video']:,.0f}/video")
    print(f"  created        {str(r.get('publishedAt'))[:10]}   last upload {str(r.get('lastVideoPublished'))[:10]}")
    print(f"  faceless       {r.get('isFaceless')}     slop flags: {r['_slop'] or 'none'}")
    print(f"\n  VERIFY BEFORE USE:  https://youtube.com/{r.get('handle')}")
    print("  Check: real runtime, real 30d upload count, whether the format is repeatable.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=None, help="sweep CSV (default: newest in ratchet/)")
    p.add_argument("--min-multiple", type=float, default=MIN_MULTIPLE)
    p.add_argument("--min-usd", type=float, default=MIN_USD_PER_VIDEO)
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--max-subs", type=int, default=300_000)
    p.add_argument("--baselines", action="store_true", help="print peer cells and exit")
    p.add_argument("--teardown", metavar="HANDLE", help="dump one channel's facts")
    p.add_argument("--include-slop", action="store_true", help="do not apply the slop screen")
    p.add_argument("--verify", nargs="?", const=10, type=int, metavar="N",
                   help="pull per-video distributions from YouTube for the top N shortlist entries")
    p.add_argument("--verify-handles", metavar="LIST",
                   help="comma-separated handles to verify directly, skipping the sweep")
    a = p.parse_args()

    if a.verify_handles:
        return print_verify([verify_channel(h.strip()) for h in a.verify_handles.split(",")])

    path = a.csv or latest_csv()
    if not os.path.isabs(path):
        path = os.path.join(TOOLS, path) if os.path.exists(os.path.join(TOOLS, path)) else path
    rows = prepare(list(csv.DictReader(open(path))))
    print(f"source: {os.path.basename(path)}   ({len(rows)} channels)")

    if a.teardown:
        return teardown(rows, a.teardown)

    clean = [r for r in rows if r["_usd_video"] > 0 and r["_band"]
             and (a.include_slop or not r["_slop"])]
    print(f"{len(clean)} earning + {'unscreened' if a.include_slop else 'slop-screened'} "
          f"+ inside a size band\n")

    cell_med, band_med, glob_med, cell_n = build_baselines(clean)

    if a.baselines:
        print(f"{'category x band':40} {'n':>4} {'med $/video':>12}")
        print("-" * 60)
        for (cat, b), n in sorted(cell_n.items(), key=lambda kv: -kv[1]):
            if n < MIN_CELL_N:
                continue
            print(f"{cat[:26]+' / '+b:40} {n:>4} {cell_med[(cat,b)]:>12,.0f}")
        print(f"\nband fallbacks: " + ", ".join(f"{k}=${v:,.0f}" for k, v in band_med.items()))
        print(f"global fallback: ${glob_med:,.0f}")
        return

    for r in clean:
        base, label = peer_for(r, cell_med, band_med, glob_med)
        r["_peer"], r["_peer_label"] = base, label
        r["_mult"] = (r["_usd_video"] / base) if base > 0 else 0.0
        r["_data_warn"], r["_peer_warn"] = confidence(
            r, cell_n.get((r.get("mainCategory") or "?", r["_band"]), 0))
        r["_warn"] = r["_data_warn"] + r["_peer_warn"]

    hits = [r for r in clean
            if r["_mult"] >= a.min_multiple
            and r["_usd_video"] >= a.min_usd
            and num(r, "subscriberCount") <= a.max_subs]
    hits.sort(key=lambda r: -r["_mult"])

    print(f"=== {len(hits)} OUTLIERS  (>= {a.min_multiple}x their size-controlled peers, "
          f">= ${a.min_usd:,.0f}/video) ===")
    print(f"{'channel':24} {'niche':24} {'subs':>7} {'/mo':>3} {'run':>5} "
          f"{'$/video':>8} {'peer':>7} {'mult':>6}  flags")
    print("-" * 118)
    for r in hits[:a.top]:
        run = f"{r['_dur']/60:.0f}m" if r["_dur"] else "?"
        print(f"{str(r.get('channelTitle'))[:24]:24} {str(r.get('niche'))[:24]:24} "
              f"{num(r,'subscriberCount'):>7,.0f} {r['_cad']:>3.0f} {run:>5} "
              f"{r['_usd_video']:>8,.0f} {r['_peer']:>7,.0f} {r['_mult']:>5.1f}x  "
              f"{','.join(r['_warn']) if r['_warn'] else 'ok'}")

    # Shortlist on DATA trust only, then rank by ABSOLUTE $/video rather than multiple.
    # The multiple is a discovery signal; it inflates wherever the peer median is small
    # ($3,899 against a $31 peer reads as 124x, which flatters a weak comparison rather
    # than describing the channel). Absolute revenue per video is what you can act on.
    solid = sorted([r for r in hits if not r["_data_warn"]],
                   key=lambda r: -r["_usd_video"])
    print(f"\n=== SHORTLIST: {len(solid)} of {len(hits)} have TRUSTWORTHY OWN DATA "
          f"(30d cadence + known runtime), ranked by absolute $/video ===")
    for r in solid[:12]:
        run = f"{r['_dur']/60:.0f}m" if r["_dur"] else "?"
        rpm = f"${r['_rpm']:.1f}rpm" if r["_rpm"] is not None else "  rpm?"
        print(f"  ${r['_usd_video']:>7,.0f}/video  {r['_mult']:>5.1f}x  {run:>4}  {rpm:>8}  "
              f"{r['_cad']:>2.0f}/mo  {str(r.get('channelTitle'))[:24]:24} "
              f"{str(r.get('handle') or '')[:22]:22} {'⚠ '+','.join(r['_peer_warn']) if r['_peer_warn'] else ''}")

    if a.verify:
        handles = [r.get("handle") for r in solid[:a.verify] if r.get("handle")]
        print_verify([verify_channel(h) for h in handles])

    out = os.path.join(OUT_DIR, "channel-outliers-" +
                       os.path.basename(path).replace("scout-", ""))
    cols = ["channelTitle", "handle", "niche", "mainCategory", "country", "subscriberCount",
            "avgViews", "estimatedEarnings", "isFaceless", "publishedAt",
            "_band", "_cad", "_cad_src", "_dur", "_usd_video", "_peer", "_peer_label",
            "_mult", "_per_sub", "_rpm", "_views30"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + ["_warnings"], extrasaction="ignore")
        w.writeheader()
        for r in hits:
            r["_warnings"] = ",".join(r["_warn"])
            w.writerow(r)
    print(f"\nwrote {out}")
    print("NOMINATIONS, NOT CONFIRMATIONS — verify a candidate on YouTube before building on it.")


if __name__ == "__main__":
    main()
