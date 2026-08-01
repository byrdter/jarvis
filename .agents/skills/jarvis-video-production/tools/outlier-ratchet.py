#!/usr/bin/env python3
"""
Outlier ratchet — find the channels that beat their own size, then watch them forever.

    python3 outlier-ratchet.py --discover        # search sweep -> GROW the watchlist
    python3 outlier-ratchet.py --monitor         # cheap daily sweep -> candidate videos
    python3 outlier-ratchet.py --status          # what's on the watchlist and why
    python3 outlier-ratchet.py --discover --lane ai-native      # one lane only
    python3 outlier-ratchet.py --monitor --days 14 --min 4      # loosen the daily filter

WHY THIS EXISTS
    outlier-scan.py watches a HAND-PICKED list of 17 channels, chosen once on 2026-07-20.
    On 2026-07-29 we probed demand across two sessions and surfaced ~12 genuine outliers
    at 9x-95x. **ZERO of the 14 channels that produced them were on that list.** Worse,
    all 17 tracked channels are AI-commentary/news channels -- the exact lane the channel
    already decided it cannot win. We were monitoring the competitors we can't beat and
    were blind to the lane where the outliers actually are.

    This inverts it: stop starting from a topic we like and asking whether anyone watches
    it. Start from what is already beating its own distribution, and adapt.

THE COST INVERSION THAT MAKES A DAILY HABIT POSSIBLE
    search.list        100 units   <- discovery is expensive
    playlistItems.list   1 unit    <- monitoring is nearly free
    videos.list          1 unit /50
    channels.list        1 unit /50

    At the 10,000/day default that is ~100 searches -- but ~5,000 channel checks. So:
      DISCOVER  weekly, ~60 queries          ~6,000 units
      MONITOR   daily,  ~500 channels          ~600 units
    Every discovery run permanently grows the cheap set. Search once to find a channel;
    watch it forever for about one unit a day. That ratchet is the whole point.

WHAT THIS TOOL DOES NOT DO -- READ THIS BEFORE TRUSTING THE OUTPUT
    It does NOT classify topic. On 2026-07-29 the word-overlap relevance gate in
    demand-probe.py produced THREE confident false positives in one session:
      "why your job title no longer describes your job" -> PROVEN 31.16x on RESUME COACHING
      "the work you actually do isn't your job anymore" -> PROVEN 41.29x on ANTI-WORK content
      "openai study on how people use chatgpt at work"  -> its only hit was a ChatGPT TUTORIAL
    No threshold on word overlap can separate on-entity-but-off-topic from on-topic. So this
    tool deliberately does not try. It emits RANKED CANDIDATES FOR READING. The classify step
    (is it actually about AI? is it evergreen or date-anchored? what shape is it?) belongs to
    an LLM or a human downstream.

    And note the third false positive was the most useful result of the day: the anti-work
    drift revealed a register running 8-41x where AI-and-jobs runs 2-11x. Drift is not always
    noise. That is another reason the rows get printed instead of filtered away.

THE FLOOD PROBLEM — observed on the first real --monitor run, 2026-07-29
    A channel earns a watchlist slot with ONE strong video, then floods the daily sweep with
    whatever else it posts. Decoded Genius Clips got in at 95.41x on "No, AI Isn't Conscious"
    -- and then supplied FOUR of the twelve rows in the first sweep, all of them relationship
    /manosphere clips at 5-6x. Nothing is broken: it is a clips channel that happens to have
    posted one AI clip that travelled.
    Mitigations, cheapest first: (a) the [?] ai_hint column flags rows with no AI term in the
    title -- it caught all four; (b) raise --min; (c) an LLM classify pass downstream; (d) if a
    channel keeps supplying off-topic rows, delete it from ratchet/watchlist.json by hand.
    Do NOT auto-drop on the hint. "Hard Work is a Scam" has no AI term either, and that lane
    is the most valuable thing this tool has surfaced.

AGE CONFOUND (inherited from outlier-scan.py / demand-probe.py)
    Views accumulate over a video's life; subscriberCount is a CURRENT snapshot. Recent
    breakouts therefore score LOW, because the subs they just earned are already in the
    denominator. --monitor looks at recent uploads by design, so its scores are systematically
    CONSERVATIVE. That is why MONITOR_MIN is lower than DISCOVER_MIN -- it is not a looser
    standard, it is the same standard corrected for the bias.
"""
import os, sys, json, time, csv, re, argparse, datetime, urllib.parse, urllib.request

HERE  = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "ratchet")
ENV   = os.path.join(os.path.expanduser("~"), "Library/CloudStorage/Dropbox/jarvis/.env")

MIN_SUBS      = 1_000      # below this the outlier score is noise
BAND_SUBS     = 300_000    # "reachable" ceiling -- what a small channel can realistically hit
MIN_SECONDS   = 90         # exclude shorts: different algorithm, different game
DISCOVER_MIN  = 5.0        # outlier needed for a channel to EARN a watchlist slot
MONITOR_MIN   = 3.0        # lower on purpose -- see AGE CONFOUND above
MONITOR_DAYS  = 21         # how far back a daily sweep looks
SINCE         = "2025-01-01"

# Date-anchored titles fail the evergreen constraint. Flagged, never dropped -- a
# date-anchored outlier still teaches us the SHAPE that travelled.
DATED = ("2024","2025","2026","2027","2028","2029","2030","by 20","this week","this month",
         "just announced","breaking","today","new model","launch","released","update",
         "january","february","march","april","may ","june","july","august","september",
         "october","november","december")

# ---------------------------------------------------------------------------
# QUERY STEMS. Short, high-frequency phrasings -- NOT publishable titles.
# demand-probe.py's docstring correction of 2026-07-29 applies here too: a real title
# is specific enough that YouTube has no near neighbour, so it returns nothing. Probe
# the SHAPE FAMILY. Every stem marked (P) is proven; the score is the measured max.
# ---------------------------------------------------------------------------
LANES = {
 "ai-native": [
   "how big is a single ai data center",          # (P) 13.4x -- deepest bench measured
   "the true scale of ai data centers",           # (P) 40.5x
   "how much water do ai data centers use",       # (P)  9.4x
   "why ai can never be conscious",               # (P) 95.6x -- highest ceiling measured
   "what ai will never be able to do",            # (P) 69.0x
   "comparing the size of every ai model",        # (P) 17.9x
   "will ai take my job",                         # (P) 10.9x
   "jobs ai will never replace",
   "how ai actually works inside",
   "what ai gets wrong",
   "why ai makes things up",
   "how much energy ai uses",
   "who owns the ai companies",
   "what happens when ai runs out of data",
   "why ai models get worse",
   "the real cost of training an ai model",
 ],
 # Adjacent lanes: proven audiences whose SHAPE can carry an AI payload. This is where
 # the anti-work discovery came from, and it was the highest-value finding of 2026-07-29.
 # Do not delete this lane because it "isn't AI" -- that is exactly its function.
 "adjacent": [
   "the real reason nobody wants to work anymore",  # (P) 13.7x
   "hard work is a scam",                           # (P) 41.3x
   "why every 9 to 5 feels like a life sentence",   # (P)  8.9x
   "how banks treat you at every level of wealth",  # (P) 43.9x
   "what happens if you invest 500 a month",        # (P) 38.3x
   "why everything feels more expensive",
   "why your degree is worthless now",
   "the skills that still matter",
   "how companies decide who to lay off",
   "why nobody can afford anything",
 ],
}


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


QUOTA = {"units": 0}


EXIT_QUOTA = 2   # distinct from 1 so a wrapper can tell "out of quota" from "broken"


def call(endpoint, key, cost=1, **params):
    params["key"] = key
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                d = json.load(r)
            if "error" in d:
                sys.exit(f"API error on {endpoint}: {d['error'].get('message')}")
            QUOTA["units"] += cost
            return d
        except urllib.error.HTTPError as e:
            # 429/403 mean the daily quota is gone. Backing off and retrying cannot help --
            # it resets at midnight Pacific. Observed 2026-07-30 after ~9k units of testing:
            # the raw traceback in the launchd log said nothing useful about the cause.
            if e.code in (429, 403):
                print(f"\n  QUOTA EXHAUSTED (HTTP {e.code}) after {QUOTA['units']:,} units "
                      f"this run. Not a bug — the YouTube quota resets at midnight Pacific.",
                      file=sys.stderr)
                sys.exit(EXIT_QUOTA)
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def iso_seconds(dur):
    if not dur or not dur.startswith("PT"):
        return 0
    n, total = "", 0
    for c in dur[2:]:
        if c.isdigit():
            n += c
        else:
            v = int(n or 0)
            total += v * {"H": 3600, "M": 60, "S": 1}.get(c, 0)
            n = ""
    return total


def load(name, default):
    p = os.path.join(STORE, name)
    try:
        return json.load(open(p, encoding="utf8"))
    except (OSError, ValueError):
        return default


def save(name, obj):
    os.makedirs(STORE, exist_ok=True)
    json.dump(obj, open(os.path.join(STORE, name), "w", encoding="utf8"), indent=1, ensure_ascii=False)


def chunk(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def hydrate(video_ids, key):
    """videos.list -> stats + duration. 1 unit per 50."""
    out = {}
    for grp in chunk(list(video_ids), 50):
        d = call("videos", key, cost=1, part="statistics,contentDetails,snippet",
                 id=",".join(grp), maxResults=50)
        for it in d.get("items", []):
            out[it["id"]] = it
    return out


def channel_meta(channel_ids, key):
    """channels.list -> subs + uploads playlist. 1 unit per 50."""
    out = {}
    for grp in chunk(list(channel_ids), 50):
        d = call("channels", key, cost=1, part="statistics,contentDetails,snippet",
                 id=",".join(grp), maxResults=50)
        for it in d.get("items", []):
            out[it["id"]] = {
                "title":   it["snippet"]["title"],
                "subs":    int(it["statistics"].get("subscriberCount", 0) or 0),
                "uploads": it["contentDetails"]["relatedPlaylists"].get("uploads"),
            }
    return out


AI_TERMS = ("ai","a.i.","artificial intelligence","chatgpt","gpt","llm","claude","gemini",
            "openai","anthropic","neural","model","algorithm","machine learning","agi",
            "data center","datacenter","automation","robot","copilot","transformer")


# WORD BOUNDARIES ARE LOAD-BEARING. The first version used substring matching and a bare
# "ai" matched inside "expl-AI-ned", "ag-AI-n", "m-AI-ntain" -- so "Every Illegal Operating
# System Explained" and "Peter Hitchens Explains Why Britain Is Finished" were both tagged
# as AI content on the first real run. Caught by reading the output, not by any test.
AI_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in AI_TERMS) + r")s?\b", re.I)


def ai_hint(title):
    """A HINT, NOT A VERDICT. Word presence only -- the same class of signal that produced
    three confident false positives on 2026-07-29. It exists to help sort a long list, never
    to decide. The title is printed beside it precisely so the hint can be overruled."""
    return "term" if AI_RE.search(title) else "-"


def dated(title):
    t = title.lower()
    return any(d in t for d in DATED)


# ---------------------------------------------------------------------------
# DISCOVER — expensive, occasional. Grows the watchlist.
# ---------------------------------------------------------------------------
def discover(key, lanes, quiet=False):
    watch = load("watchlist.json", {})
    before = len(watch)
    added, examined = [], 0

    for lane, stems in lanes.items():
        for q in stems:
            if not quiet:
                print(f"  search  [{lane}] {q}")
            d = call("search", key, cost=100, part="snippet", q=q, type="video",
                     maxResults=40, order="relevance", publishedAfter=SINCE + "T00:00:00Z")
            ids = [i["id"]["videoId"] for i in d.get("items", []) if i["id"].get("videoId")]
            if not ids:
                continue
            vids = hydrate(ids, key)
            chans = channel_meta({v["snippet"]["channelId"] for v in vids.values()}, key)

            for vid, v in vids.items():   # noqa: E501
                examined += 1
                cid  = v["snippet"]["channelId"]
                meta = chans.get(cid)
                if not meta or not (MIN_SUBS <= meta["subs"] <= BAND_SUBS):
                    continue
                if iso_seconds(v["contentDetails"].get("duration")) < MIN_SECONDS:
                    continue
                views = int(v["statistics"].get("viewCount", 0) or 0)
                score = views / meta["subs"]
                if score < DISCOVER_MIN or cid in watch:
                    continue
                watch[cid] = {
                    "title":       meta["title"],
                    "subs":        meta["subs"],
                    "uploads":     meta["uploads"],
                    "added":       datetime.date.today().isoformat(),
                    "found_by":    q,
                    "lane":        lane,
                    "found_score": round(score, 2),
                    "found_video": f"https://www.youtube.com/watch?v={vid}",
                    "found_title": v["snippet"]["title"],
                }
                added.append((score, meta["title"], meta["subs"], q, v["snippet"]["title"]))

        # Save per LANE, not just at the end. A quota 429 mid-sweep used to discard every
        # channel the run had already found (observed 2026-07-30).
        save("watchlist.json", watch)

    save("watchlist.json", watch)
    added.sort(reverse=True)
    print(f"\n{'='*94}\nDISCOVER — watchlist {before} -> {len(watch)}  (+{len(added)} new)"
          f"   ·  {examined} videos examined  ·  {QUOTA['units']:,} quota units\n{'='*94}")
    if not added:
        print("  no new channels cleared the bar. Widen the stems or lower DISCOVER_MIN.")
    for score, ch, subs, q, vt in added:
        print(f"  {score:7.2f}x  {ch[:26]:26} {subs:>8,} subs   [{q[:30]}]")
        print(f"            {vt[:88]}")
    return watch


# ---------------------------------------------------------------------------
# MONITOR — cheap, daily. Reads the watchlist, surfaces new outliers.
# ---------------------------------------------------------------------------
def monitor(key, days, floor, quiet=False):
    watch = load("watchlist.json", {})
    if not watch:
        sys.exit("Watchlist is empty. Run --discover first.")
    seen = set(load("seen.json", []))
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(days=days)).replace(tzinfo=None).isoformat() + "Z"

    # refresh subs (they move, and they are the denominator)
    fresh = channel_meta(list(watch.keys()), key)
    for cid, m in fresh.items():
        watch[cid].update(subs=m["subs"], uploads=m["uploads"], title=m["title"])
    save("watchlist.json", watch)

    recent = []
    for cid, m in watch.items():
        if not m.get("uploads"):
            continue
        d = call("playlistItems", key, cost=1, part="contentDetails",
                 playlistId=m["uploads"], maxResults=10)
        for it in d.get("items", []):
            cd = it["contentDetails"]
            if cd.get("videoPublishedAt", "") >= cutoff and cd["videoId"] not in seen:
                recent.append((cd["videoId"], cid))

    rows = []
    if recent:
        vids = hydrate([r[0] for r in recent], key)
        for vid, cid in recent:
            v = vids.get(vid)
            if not v:
                continue
            if iso_seconds(v["contentDetails"].get("duration")) < MIN_SECONDS:
                continue
            subs = watch[cid]["subs"] or 0
            if subs < MIN_SUBS:
                continue
            views = int(v["statistics"].get("viewCount", 0) or 0)
            score = views / subs
            if score < floor:
                continue
            rows.append({
                "outlier": round(score, 2), "views": views, "subs": subs,
                "channel": watch[cid]["title"],
                "found_via": watch[cid].get("lane", "?"),   # PROVENANCE, not topic
                "ai_hint": ai_hint(v["snippet"]["title"]),
                "published": v["snippet"]["publishedAt"][:10],
                "evergreen": "no" if dated(v["snippet"]["title"]) else "maybe",
                "title": v["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={vid}",
            })
            seen.add(vid)

    save("seen.json", sorted(seen))
    rows.sort(key=lambda r: -r["outlier"])

    stamp = datetime.date.today().isoformat()
    if rows:
        p = os.path.join(STORE, f"candidates-{stamp}.csv")
        with open(p, "w", newline="", encoding="utf8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)

    print(f"\n{'='*100}\nMONITOR — {len(watch)} channels · last {days} days · floor {floor}x"
          f"  ·  {QUOTA['units']:,} quota units\n"
          f"NOT CLASSIFIED BY TOPIC. Candidates for READING.  [?] = no AI term in the title\n"
          f"'via:' is the lane that DISCOVERED the channel — NOT the topic of this video.\n{'='*100}")
    if not rows:
        print("  nothing new above the floor. That is a normal result on most days.")
    for r in rows:
        flag = "" if r["evergreen"] == "maybe" else "  [DATED]"
        hint = "     " if r["ai_hint"] == "term" else "  [?] "
        print(f"  {r['outlier']:7.2f}x  {r['views']:>9,} /{r['subs']:>8,}  {r['published']}"
              f"{hint}via:{r['found_via'][:9]}{flag}")
        print(f"            {r['channel'][:24]:24} {r['title'][:70]}")
    if rows:
        print(f"\n  -> {os.path.join(STORE, f'candidates-{stamp}.csv')}")
    return rows


def status():
    watch = load("watchlist.json", {})
    seen = load("seen.json", [])
    print(f"\nWATCHLIST — {len(watch)} channels · {len(seen)} videos already surfaced\n" + "="*94)
    by_lane = {}
    for m in watch.values():
        by_lane.setdefault(m.get("lane", "?"), []).append(m)
    for lane, ms in sorted(by_lane.items()):
        print(f"\n  [{lane}]  {len(ms)} channels")
        for m in sorted(ms, key=lambda x: -x.get("found_score", 0))[:40]:
            print(f"    {m.get('found_score',0):7.2f}x  {m['title'][:30]:30} {m['subs']:>8,} subs"
                  f"   added {m.get('added','?')}  via [{m.get('found_by','?')[:28]}]")


def main():
    ap = argparse.ArgumentParser(description="Outlier ratchet — grow a watchlist, then sweep it cheaply.")
    ap.add_argument("--discover", action="store_true", help="search sweep; grows the watchlist (EXPENSIVE)")
    ap.add_argument("--monitor",  action="store_true", help="cheap sweep of the watchlist")
    ap.add_argument("--status",   action="store_true", help="print the watchlist")
    ap.add_argument("--lane",     help="restrict --discover to one lane: " + ", ".join(LANES))
    ap.add_argument("--days",     type=int, default=MONITOR_DAYS)
    ap.add_argument("--min",      type=float, default=MONITOR_MIN)
    ap.add_argument("--quiet",    action="store_true")
    a = ap.parse_args()

    if a.status:
        return status()
    if not (a.discover or a.monitor):
        ap.print_help(); return

    key = api_key()
    if a.discover:
        lanes = {a.lane: LANES[a.lane]} if a.lane else LANES
        if a.lane and a.lane not in LANES:
            sys.exit(f"Unknown lane {a.lane!r}. Have: {', '.join(LANES)}")
        est = sum(len(v) for v in lanes.values()) * 102
        print(f"  {sum(len(v) for v in lanes.values())} queries ≈ {est:,} quota units "
              f"(10,000/day default)\n")
        discover(key, lanes, a.quiet)
    if a.monitor:
        monitor(key, a.days, a.min, a.quiet)


if __name__ == "__main__":
    main()
