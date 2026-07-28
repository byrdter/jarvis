#!/usr/bin/env python3
"""
Demand probe — does anyone actually WATCH this shape of video?

The companion to outlier-scan.py. That one asks "what travelled on the channels we
track"; this one asks "if we made a video about X, is there evidence of demand at a
size we can reach?" It searches YouTube for a phrasing, scores every result by
outlier (views / the POSTING channel's subs), and returns a verdict.

Why it exists: on 2026-07-27 four angles were recommended on the strength of
sounding like burning problems. Measured, they were the worst-scoring cells in the
scan (0.03x-0.10x medians). Low competition was ABSENCE OF DEMAND, not an open
lane. Without this probe, "nobody covered it" and "nobody watches it" look
identical, and the ideas ranker hedges toward whatever a competitor already touched.

    python3 demand-probe.py "gmail ai training opt out" "windows recording clipboard"
    python3 demand-probe.py --file queries.txt
    python3 demand-probe.py --json "one query"        # machine-readable
    python3 demand-probe.py --refresh "one query"     # ignore cache

READ BEFORE TRUSTING A NUMBER
  * Query drift. YouTube search relevance decays down the result list; the tail of
    a bucket is often off-topic. Bucket medians are DIRECTIONAL. The per-video rows
    are the real evidence -- read them.
  * Age confound. Views accumulate for a video's life; subscriber count is a
    CURRENT snapshot. Old videos on since-grown channels score high for no good
    reason; recent breakouts score LOW because the subs they just earned are
    already in the denominator. The --since cutoff drops the first artifact; the
    second means high recent scores are conservative, not inflated.
  * A verdict is about the SHAPE of the phrasing, not the topic. Probe the title
    you would actually publish, not the subject in the abstract.

Quota: search.list costs 100 units/query against a 10,000/day default. Results are
cached in raw-probe/ keyed by query+params; delete a file to re-probe just that one.
"""
import os, sys, json, csv, time, hashlib, statistics, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw-probe")
ENV = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/Dropbox/jarvis/.env")

SINCE = "2025-01-01"     # recency floor; see AGE CONFOUND
MAX_RESULTS = 40         # per query (API pages at 50)
MIN_SUBS = 1_000         # below this, outlier score is noise
MIN_SECONDS = 90         # exclude shorts -- different algorithm, different game
BAND_SUBS = 300_000      # "reachable band" -- what a small channel can realistically hit
CANDIDATE = 1.5          # calibrated in outlier-scan.py; NOT 5x
# >=50% of results discarded as off-topic -> demote a positive verdict.
# Calibrated on only four cases (gmail 0.08 keep / resume 0.43 keep / claude-artifacts
# 0.53 demote / deepseek-template 0.83 demote) -- a rough dial, not a law. The
# per-video rows remain the real evidence; this only stops a heavily-drifted bucket
# from being reported as hard proof.
DRIFT_LIMIT = 0.5


def api_key():
    k = os.environ.get("YOUTUBE_API_KEY")
    if k:
        return k.strip()
    try:
        for line in open(ENV, encoding="utf8"):
            if line.startswith("YOUTUBE_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    sys.exit("No YOUTUBE_API_KEY (env or jarvis/.env).")


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def call(endpoint, key, **params):
    params["key"] = key
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            d = get(url)
            if "error" in d:
                sys.exit(f"API error: {d['error'].get('message')}")
            return d
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def iso_seconds(dur):
    """PT#H#M#S -> seconds. Returns 0 on anything unparseable (treated as a short)."""
    if not dur or not dur.startswith("PT"):
        return 0
    n, total = "", 0
    for c in dur[2:]:
        if c.isdigit():
            n += c
        else:
            total += int(n or 0) * {"H": 3600, "M": 60, "S": 1}.get(c, 0)
            n = ""
    return total


STOP = {"the", "a", "an", "is", "are", "was", "it", "its", "to", "of", "in", "on", "for",
        "and", "or", "but", "not", "you", "your", "my", "this", "that", "how", "why",
        "what", "when", "do", "does", "did", "be", "been", "by", "with", "from", "at",
        "as", "we", "our", "i", "just", "can", "will", "than", "then", "if", "so"}


def content_words(q):
    """The distinctive terms a genuinely on-topic result should echo."""
    ws = [w.strip(".,!?\"'()[]").lower() for w in q.split()]
    return [w for w in ws if len(w) > 2 and w not in STOP]


def relevance(row, terms):
    """How many query terms appear in the title+description. Cheap, but it is the
    difference between measuring this topic and measuring whatever YouTube drifted to.
    Substring match so plural/possessive variants still count."""
    hay = (row.get("title", "") + " " + row.get("desc", "")).lower()
    return sum(1 for t in terms if t in hay)


def drift_filter(rows, query):
    """Split rows into on-topic and drifted. Threshold scales with query length: a
    2-word query can only ever match 1-2 terms, a 8-word query should match >=2."""
    terms = content_words(query)
    need = 1 if len(terms) <= 2 else 2
    on = [r for r in rows if relevance(r, terms) >= need]
    return on, len(rows) - len(on)


def probe(query, key, refresh=False, max_results=MAX_RESULTS, since=SINCE):
    os.makedirs(CACHE, exist_ok=True)
    # v2 = rows carry `desc` (needed by the relevance gate); bumping invalidates v1 caches.
    sig = hashlib.sha1(f"v2|{query}|{max_results}|{since}".encode()).hexdigest()[:16]
    path = os.path.join(CACHE, f"{sig}.json")
    if os.path.exists(path) and not refresh:
        return json.load(open(path, encoding="utf8"))

    # 1. search -> video ids (100 quota units)
    ids = []
    token = None
    while len(ids) < max_results:
        p = dict(part="snippet", q=query, type="video", maxResults=min(50, max_results - len(ids)),
                 publishedAfter=f"{since}T00:00:00Z", order="relevance")
        if token:
            p["pageToken"] = token
        d = call("search", key, **p)
        ids += [i["id"]["videoId"] for i in d.get("items", []) if i.get("id", {}).get("videoId")]
        token = d.get("nextPageToken")
        if not token:
            break

    if not ids:
        rows = []
    else:
        # 2. videos -> stats + duration + channel id (1 unit per 50)
        vids = []
        for i in range(0, len(ids), 50):
            d = call("videos", key, part="statistics,contentDetails,snippet", id=",".join(ids[i:i + 50]))
            vids += d.get("items", [])
        # 3. channels -> subscriber counts (1 unit per 50)
        chan_ids = sorted({v["snippet"]["channelId"] for v in vids})
        subs = {}
        for i in range(0, len(chan_ids), 50):
            d = call("channels", key, part="statistics", id=",".join(chan_ids[i:i + 50]))
            for c in d.get("items", []):
                st = c.get("statistics", {})
                if not st.get("hiddenSubscriberCount"):
                    subs[c["id"]] = int(st.get("subscriberCount", 0) or 0)

        rows = []
        for v in vids:
            s = subs.get(v["snippet"]["channelId"], 0)
            views = int(v.get("statistics", {}).get("viewCount", 0) or 0)
            secs = iso_seconds(v.get("contentDetails", {}).get("duration", ""))
            if s < MIN_SUBS or views <= 0 or secs < MIN_SECONDS:
                continue
            rows.append({
                "outlier": round(views / s, 3), "views": views, "subs": s,
                "date": v["snippet"]["publishedAt"][:10], "mins": round(secs / 60, 1),
                "channel": v["snippet"]["channelTitle"], "title": v["snippet"]["title"],
                "desc": (v["snippet"].get("description") or "")[:400], "id": v["id"],
            })

    out = {"query": query, "since": since, "n_raw": len(ids), "rows": rows}
    json.dump(out, open(path, "w", encoding="utf8"), indent=1)
    return out


def verdict(rows, query):
    """Judge on-topic rows in the REACHABLE band only. Two independent filters:
    a 2M-sub channel's result tells us nothing about what WE can reach, and a
    drifted result tells us nothing about this topic at all."""
    on, dropped = drift_filter(rows, query)
    band = [r for r in on if r["subs"] <= BAND_SUBS]
    if len(band) < 3:
        # Too little on-topic evidence to call it either way. This is NOT "dead" --
        # it is "unmeasured", and the two must never be conflated.
        return "INCONCLUSIVE", {"n": len(band), "dropped": dropped}
    o = sorted(r["outlier"] for r in band)
    hits = [x for x in o if x >= CANDIDATE]
    drift = dropped / max(1, len(rows))
    st = {"n": len(band), "dropped": dropped, "drift": round(drift, 2),
          "median": statistics.median(o),
          "p75": o[int(len(o) * 0.75)] if len(o) > 1 else o[0], "max": max(o), "hits": len(hits)}
    if len(hits) >= 2:
        v = "PROVEN"          # repeatable, not one lucky video
    elif len(hits) == 1:
        v = "MIXED"           # a lottery ticket cashed once
    elif st["max"] >= 0.5:
        v = "THIN"
    else:
        v = "DEAD"            # the round-3 trap: no competition because no demand

    # DRIFT DOWNGRADE. A verdict computed after discarding most of the result set is
    # measuring a thin, unrepresentative slice -- usually the broad interest in the
    # entity rather than demand for THIS shape. Annotating that and leaving the call
    # to downstream judgement does not work: on 2026-07-28 an 88%-drift PROVEN was
    # ranked #1 with the note "the PROVEN verdict outweighs drift concerns." It does
    # not. Positive verdicts built on heavy drift are demoted mechanically.
    if drift >= DRIFT_LIMIT and v in ("PROVEN", "MIXED"):
        st["downgraded_from"] = v
        v = "INCONCLUSIVE"    # unmeasured -- NOT dead
    return v, st


def report(results, as_json=False):
    if as_json:
        payload = []
        for r in results:
            v, st = verdict(r["rows"], r["query"])
            on, _ = drift_filter(r["rows"], r["query"])
            payload.append({"query": r["query"], "verdict": v, **st,
                            "top": sorted([x for x in on if x["subs"] <= BAND_SUBS],
                                          key=lambda x: -x["outlier"])[:5]})
        print(json.dumps(payload, indent=1))
        return

    print(f"\n{'=' * 100}\nDEMAND PROBE  (channels {MIN_SUBS:,}-{BAND_SUBS:,} subs; >={CANDIDATE}x = hit; "
          f"videos since {SINCE}, shorts excluded)\n"
          f"'drift' = off-topic results discarded by the relevance gate. INCONCLUSIVE means "
          f"UNMEASURED, not dead.\n{'=' * 100}")
    print(f"{'verdict':>13} {'n':>4} {'drift':>6} {'median':>8} {'p75':>7} {'max':>8} {'hits':>5}  query")
    for r in results:
        v, st = verdict(r["rows"], r["query"])
        if "median" not in st:
            print(f"{v:>13} {st.get('n', 0):>4} {st.get('dropped', 0):>6} {'-':>8} {'-':>7} "
                  f"{'-':>8} {'-':>5}  {r['query']}")
            continue
        tag = f" (was {st['downgraded_from']}, {int(st['drift']*100)}% drift)" if 'downgraded_from' in st else ''
        print(f"{v:>13} {st['n']:>4} {st['dropped']:>6} {st['median']:>7.2f}x {st['p75']:>6.2f}x "
              f"{st['max']:>7.2f}x {st['hits']:>5}  {r['query']}{tag}")

    for r in results:
        on, _ = drift_filter(r["rows"], r["query"])
        band = sorted([x for x in on if x["subs"] <= BAND_SUBS], key=lambda x: -x["outlier"])
        print(f"\n--- {r['query']}  (on-topic rows -- THIS is the evidence, not the median) ---")
        if not band:
            print("    (nothing on-topic in the reachable band -- unmeasured, not dead)")
        for x in band[:6]:
            flag = "*" if x["outlier"] >= CANDIDATE else " "
            print(f"{x['outlier']:>7.2f}x{flag}{x['views']:>10,} {x['subs']:>9,} {x['mins']:>5.1f}m "
                  f"{x['date']}  [{x['channel'][:20]:20}] {x['title'][:58]}")

    out = os.path.join(HERE, "demand-probe.csv")
    with open(out, "w", newline="", encoding="utf8") as fh:
        w = csv.DictWriter(fh, fieldnames=["query", "verdict", "ontopic", "outlier", "views",
                                           "subs", "date", "mins", "channel", "title", "id"])
        w.writeheader()
        for r in results:
            v, _ = verdict(r["rows"], r["query"])
            on, _ = drift_filter(r["rows"], r["query"])
            on_ids = {x["id"] for x in on}
            for x in sorted(r["rows"], key=lambda x: -x["outlier"]):
                w.writerow({"query": r["query"], "verdict": v,
                            "ontopic": int(x["id"] in on_ids),
                            **{k: x[k] for k in ["outlier", "views", "subs", "date", "mins",
                                                 "channel", "title", "id"]}})
    print(f"\n-> {out}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    as_json = "--json" in args
    refresh = "--refresh" in args
    args = [a for a in args if not a.startswith("--") or a == "--file"]
    queries = []
    if "--file" in args:
        i = args.index("--file")
        queries += [l.strip() for l in open(args[i + 1], encoding="utf8") if l.strip()
                    and not l.startswith("#")]
        del args[i:i + 2]
    queries += args
    if not queries:
        sys.exit(__doc__)

    key = api_key()
    results = []
    for q in queries:
        if not as_json:
            print(f"  probe  {q[:70]} ...", flush=True)
        results.append(probe(q, key, refresh=refresh))
    report(results, as_json=as_json)
