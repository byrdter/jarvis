#!/usr/bin/env python3
"""
Outlier scan — implements RETENTION-AND-HOOKS.md §7.1.

Outlier score = views / subscriber count of the POSTING channel.
Ranks ideas by how far they travelled beyond their own distribution, which is
what we want; raw view counts just measure how big the channel already was.

    python3 outlier-scan.py            # fetch (cached) + report
    python3 outlier-scan.py --refresh  # ignore cache, re-fetch everything
    python3 outlier-scan.py --all      # include pre-cutoff videos (see AGE CONFOUND)

AGE CONFOUND — read before trusting any number:
    Views accumulate for the life of a video, but `channel_follower_count` is a
    CURRENT snapshot. So an old video on a channel that has since grown scores
    high for no good reason (a 2019 video divided by 2026 subs), while a recent
    breakout scores LOW because the subs it just earned are already in the
    denominator. The default cutoff below drops the first artifact; the second
    means recent high scores are conservative, not inflated.

Cache lives in raw/ beside this script. Delete a .tsv to re-fetch one channel.
"""
import subprocess, sys, os, csv, statistics
from collections import defaultdict

# The canonical Byrddynasty competitor set (chosen 2026-07-20).
# Weighted toward the 30K-250K band per §7.1 -- reachable outliers. The large
# channels are reference only; they essentially never register as outliers.
CHANNELS = [
    # core band: evidence/explainer register, closest to our format
    "bycloudAI", "InternetofBugs", "MachineLearningStreetTalk", "EdanMeyer",
    "DrWaku", "ArtemKirsanov", "WelchLabs", "AICoffeeBreak", "vcubingx",
    "TinaHuang1", "sentdex",
    # upper band: topic proximity reference
    "aiexplained-official", "matthew_berman", "WesRoth", "TheAiGrid",
    "TwoMinutePapers", "aiadvantage",
]

CUTOFF = "20250101"   # default recency floor; see AGE CONFOUND
CANDIDATE = 1.5       # calibrated on real data -- see §7.1. NOT 5x.
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

FIELDS = r"%(channel)s\t%(channel_follower_count)s\t%(view_count)s\t%(upload_date)s\t%(duration)s\t%(id)s\t%(title)s"


def fetch(refresh=False):
    os.makedirs(RAW, exist_ok=True)
    for ch in CHANNELS:
        out = os.path.join(RAW, f"{ch}.tsv")
        if os.path.exists(out) and os.path.getsize(out) > 0 and not refresh:
            print(f"  cached  {ch}")
            continue
        print(f"  fetch   {ch} ...", flush=True)
        with open(out, "w", encoding="utf8") as fh:
            subprocess.run(
                ["yt-dlp", "--no-update", "--playlist-end", "30", "--skip-download",
                 "--print", FIELDS, f"https://www.youtube.com/@{ch}/videos"],
                stdout=fh, stderr=subprocess.DEVNULL, check=False)
        n = sum(1 for _ in open(out, encoding="utf8"))
        if n == 0:
            print(f"    !! {ch}: 0 rows -- handle probably wrong, fix CHANNELS")
        else:
            print(f"    ok {n}")


def load(cutoff):
    rows = []
    for ch in CHANNELS:
        f = os.path.join(RAW, f"{ch}.tsv")
        if not os.path.exists(f):
            continue
        for line in open(f, encoding="utf8"):
            # yt-dlp --print emits a LITERAL backslash-t, not a tab.
            p = line.rstrip("\n").split("\\t")
            if len(p) < 7:
                continue
            try:
                subs, views = int(p[1]), int(p[2])
                dur = float(p[4])
            except ValueError:
                continue
            if subs <= 0 or p[3] < cutoff:
                continue
            rows.append({"channel": p[0], "subs": subs, "views": views, "date": p[3],
                         "dur": dur, "id": p[5], "title": "\\t".join(p[6:]),
                         "outlier": views / subs})
    return rows


def report(rows, cutoff):
    rows.sort(key=lambda r: -r["outlier"])
    print(f"\n{'=' * 96}\nTOP OUTLIERS  (uploaded >= {cutoff};  >={CANDIDATE}x = candidate)\n{'=' * 96}")
    print(f"{'score':>7} {'views':>10} {'subs':>9} {'min':>4} {'date':>9}  channel / title")
    for r in rows[:30]:
        flag = "*" if r["outlier"] >= CANDIDATE else " "
        print(f"{r['outlier']:>6.2f}x{flag}{r['views']:>10,} {r['subs']:>9,} "
              f"{r['dur'] / 60:>4.0f} {r['date']:>9}  [{r['channel'][:18]}] {r['title'][:55]}")

    d = defaultdict(list)
    for r in rows:
        d[r["channel"]].append(r["outlier"])
    print(f"\n{'=' * 96}\nMEDIAN BY CHANNEL  (register comparison -- the strategic read)\n{'=' * 96}")
    for c, v in sorted(d.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"{c[:40]:>40}  n={len(v):<3} median {statistics.median(v):>6.2f}x  max {max(v):>6.2f}x")

    n = sum(1 for r in rows if r["outlier"] >= CANDIDATE)
    print(f"\n{n} candidates at >={CANDIDATE}x, out of {len(rows)} videos across {len(d)} channels.")

    out = os.path.join(HERE, "outliers.csv")
    with open(out, "w", newline="", encoding="utf8") as fh:
        w = csv.DictWriter(fh, fieldnames=["outlier", "views", "subs", "date", "dur", "channel", "title", "id"])
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(r[k], 3) if k == "outlier" else r[k]) for k in w.fieldnames})
    print(f"-> {out}")


if __name__ == "__main__":
    cutoff = "00000000" if "--all" in sys.argv else CUTOFF
    fetch(refresh="--refresh" in sys.argv)
    report(load(cutoff), cutoff)
