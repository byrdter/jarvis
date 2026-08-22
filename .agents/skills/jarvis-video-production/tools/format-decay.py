#!/usr/bin/env python3
"""format-decay.py — the SELF axis. We watch every channel except our own.

TOOL CONTRACT
  SUBSYSTEM  D (Demand), self-monitoring
  STATE      reads  ratchet/our-formats.json (config, hand-written)
             writes raw/selfdecay/<handle>/ (catalog + per-video info cache)
  GATE       exits 1 if any format is DECAYING. UNMEASURED never fails the gate.
  MODULE     jarvis-video-production (tools tree)
  SCOPE      our own channels only

    python3 format-decay.py --channel @byrddynasty              # pull + report
    python3 format-decay.py --channel @byrddynasty --no-pull    # report from cache
    python3 format-decay.py --channel @byrddynasty --json
    python3 format-decay.py --channel @byrddynasty --window 120 --min-n 4

WHY THIS EXISTS
  outlier-ratchet.py watches OTHER channels. outlier-scan.py watches OTHER channels.
  format-index.py catalogues formats in the wild. **Nothing measures whether a format WE
  OWN is still working.** That gap is the measured difference between the two channels we
  tore down on 2026-08-21/22:

      Fireship   "X in 100 Seconds" ran 1.34x (2022) -> 1.10x (2023) -> 0.52x (2024).
                 They read the decay and cut it from 55% to 1-5% of output. Channel held
                 flat at ~950K/video for five years afterwards.

      Snap Shift Found its best lever (two-clause titles, 3.86x, p<0.0001), rode it to 48%
                 of output in June, then drifted to 16% in July under volume pressure --
                 with no instrument that would have told them. Median fell 73,942 -> 49,535.

  Same mechanic, opposite outcomes, and the only difference is whether anyone was watching.
  This is the watching.

FIVE CORRECTIONS HARD-CODED -- each one cost a wrong conclusion, with the date
  1. AGE-NORMALISE, ALWAYS. Raw lifetime views favour whatever is oldest. On 2026-08-22 the
     Fireship runtime finding was a textbook Simpson's reversal: pooled, short videos looked
     1.79x better; within era they were 0.91x. Ranking on raw views reproduces that error.
     Every ratio here is computed on views/day within a bin.
  2. PARITY IS AGAINST THE CONTEMPORANEOUS CHANNEL MEDIAN, NEVER THE LIFETIME ONE. On a
     growing channel a lifetime baseline makes every recent format look like a triumph; on a
     shrinking one it condemns all of them. The comparison is always format-vs-channel
     INSIDE the same bin.
  3. REFUSE TO CALL DECAY ON THIN DATA. On 2026-08-22 a cluster ranking built on
     Byrddynasty's last 30 videos (3-96 views each) produced a confident answer that the full
     96-video catalog inverted. Below MIN_N the verdict is UNMEASURED. Per demand-probe.py's
     rule, which this inherits verbatim: **UNMEASURED IS NOT DEAD**, and it never fails the gate.
  4. A ZERO-EXIT yt-dlp RUN IS NOT A COMPLETE RUN. On 2026-08-22 a 783-video pull exited 0
     having failed 288 of them to YouTube rate-limiting. Because a channel's id list is
     chronological, the gap was era-biased -- 100% coverage of 2024-26, 2-16% of 2017-20.
     Reading only the exit code would have silently produced a decay curve with its own
     history missing. This tool counts errors and prints coverage before any verdict.
  5. approximate_date IS TRAJECTORY-ONLY AND IS NOT USED HERE. Measured 2026-08-22 against
     168 videos with both: 0% exact match, 23-day median error, 225-day max, 18% year-bin
     disagreement. Fine for a decade-scale shape, useless for the bins this tool needs.

WHAT THIS TOOL WILL NOT TELL YOU
  Views are impressions x CTR x recommendation. A format can decay because the packaging
  stopped working, because the subject cooled, or because the audience moved -- and this
  cannot separate those. It tells you WHEN to look, never WHY. The why is a teardown.

  It also measures the CLICK and is blind to the HOLD, like every other instrument we own.
"""
import argparse, json, os, re, subprocess, sys, statistics as st, datetime, math

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw", "selfdecay")
CONFIG = os.path.join(HERE, "ratchet", "our-formats.json")

WINDOW_DAYS = 90      # bin width. 90 suits a ~5/month channel; drop to 30 for a daily one.
MIN_N = 3             # below this, a bin is UNMEASURED. Never DECAYING.
PARITY = 1.0          # format vs contemporaneous channel median
DECAY_BINS = 2        # consecutive sub-parity bins before the gate fails
MIN_SECONDS = 90      # exclude shorts -- different algorithm, different game


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, check=False, **kw)


def pull(handle, refresh=False):
    """Catalog + per-video exact dates. Returns (rows, coverage_note)."""
    d = os.path.join(CACHE, handle.lstrip("@"))
    info = os.path.join(d, "info")
    os.makedirs(info, exist_ok=True)
    cat = os.path.join(d, "catalog.jsonl")

    if refresh or not os.path.exists(cat):
        r = sh(["yt-dlp", "--flat-playlist", "--dump-json",
                f"https://www.youtube.com/{handle}/videos"])
        if r.returncode != 0 or not r.stdout.strip():
            sys.exit(f"catalog pull failed for {handle}:\n{r.stderr[-600:]}")
        open(cat, "w").write(r.stdout)

    ids = [json.loads(l)["id"] for l in open(cat) if l.strip()]
    have = {f.split(".")[0] for f in os.listdir(info) if f.endswith(".info.json")}
    missing = [i for i in ids if i not in have]

    if missing:
        print(f"  pulling {len(missing)} missing info-json (3s spacing, "
              f"~{len(missing)*3//60+1} min)...", file=sys.stderr)
        lst = os.path.join(d, "_missing.txt")
        open(lst, "w").write("\n".join(f"https://www.youtube.com/watch?v={i}" for i in missing))
        log = os.path.join(d, "pull.log")
        with open(log, "w") as fh:
            subprocess.run(["yt-dlp", "--skip-download", "--write-info-json",
                            "--no-write-playlist-metafiles", "--sleep-requests", "3",
                            "--retries", "3", "--ignore-errors",
                            "-o", os.path.join(info, "%(id)s.%(ext)s"), "-a", lst],
                           stdout=fh, stderr=subprocess.STDOUT)
        # CORRECTION 4: exit code is not completeness. Count errors.
        errs = sum(1 for l in open(log, errors="ignore") if l.startswith("ERROR"))
        if errs:
            print(f"  !! {errs} video(s) failed to pull (rate-limit or age-gate). "
                  f"Coverage is incomplete -- re-run later to close the gap.", file=sys.stderr)

    rows = []
    for f in os.listdir(info):
        if not f.endswith(".info.json"):
            continue
        try:
            v = json.load(open(os.path.join(info, f)))
        except Exception:
            continue
        s, views, dur = v.get("upload_date"), v.get("view_count") or 0, v.get("duration") or 0
        if not s or views <= 0 or dur < MIN_SECONDS:
            continue
        rows.append(dict(id=v["id"], title=v.get("title", ""), views=views, dur=dur,
                         dt=datetime.date(int(s[:4]), int(s[4:6]), int(s[6:]))))
    cov = f"{len(rows)}/{len(ids)} videos with exact dates ({len(rows)/max(1,len(ids))*100:.0f}% coverage)"
    return rows, cov


def load_formats(path=CONFIG):
    if not os.path.exists(path):
        sys.exit(f"no format config at {path}\n"
                 'create it, e.g.  {"harness": "harness|agent harness", '
                 '"claude-code": "claude code|subagent|mcp"}')
    return json.load(open(path))


def classify(title, formats):
    """First match wins -- order the config most-specific first."""
    for name, pat in formats.items():
        if re.search(pat, title, re.I):
            return name
    return None


def analyse(rows, formats, window=WINDOW_DAYS, min_n=MIN_N, today=None):
    today = today or datetime.date.today()
    for r in rows:
        r["age"] = max(1, (today - r["dt"]).days)
        r["vpd"] = r["views"] / r["age"]           # CORRECTION 1: age-normalised
        r["fmt"] = classify(r["title"], formats)

    newest = max(r["dt"] for r in rows)
    oldest = min(r["dt"] for r in rows)
    bins = []
    end = newest
    while end > oldest:
        start = end - datetime.timedelta(days=window)
        g = [r for r in rows if start < r["dt"] <= end]
        if g:
            bins.append((start, end, g))
        end = start
    bins.reverse()

    out = []
    for start, end, g in bins:
        # CORRECTION 2: parity is against THIS bin's channel median, not lifetime
        chan = st.median(r["vpd"] for r in g)
        entry = {"start": str(start), "end": str(end), "n": len(g),
                 "channel_median_vpd": chan, "formats": {}}
        for name in formats:
            fg = [r for r in g if r["fmt"] == name]
            if not fg:
                continue
            fm = st.median(r["vpd"] for r in fg)
            entry["formats"][name] = {
                "n": len(fg), "median_vpd": fm,
                "ratio": (fm / chan) if chan else None,
                "share": len(fg) / len(g),
                # CORRECTION 3: thin bins are UNMEASURED, never DECAYING
                "measured": len(fg) >= min_n,
            }
        out.append(entry)
    return out


PROMISING = 1.5   # unmeasured but running this far above parity -> worth more samples


def verdicts(series, formats, decay_bins=DECAY_BINS):
    """Verdicts, most severe first.

    STALE exists because of a bug this tool caught in its own first run on 2026-08-23:
    `agent-failure` reported HEALTHY off a bin that was nine months old, simply because it
    was the most recent bin that cleared MIN_N. A format you stopped making would have read
    as healthy forever. A verdict is only about the CURRENT bin; anything older is stale.
    """
    current_bin = series[-1]["end"] if series else None
    res = {}
    for name in formats:
        hist = [(b["end"], b["formats"].get(name)) for b in series if name in b["formats"]]
        measured = [(d, f) for d, f in hist if f["measured"]]

        if not measured:
            # Thin -- but distinguish "thin and promising" from "thin and nothing".
            best = max((f["ratio"] for _, f in hist if f["ratio"] is not None), default=None)
            n_tot = sum(f["n"] for _, f in hist)
            if best is not None and best >= PROMISING:
                res[name] = ("PROMISING",
                             f"only n={n_tot} across all bins, but peaks at {best:.2f}x parity "
                             f"-- ship more to find out", hist)
            else:
                res[name] = ("UNMEASURED", f"n={n_tot} total, below the minimum sample", hist)
            continue

        last_d, last_f = measured[-1]
        if last_d != current_bin:
            res[name] = ("STALE", f"last measured bin ended {last_d} ({last_f['ratio']:.2f}x) "
                                  f"-- nothing current to judge", hist)
            continue

        tail = measured[-decay_bins:]
        ratios = ", ".join(f"{f['ratio']:.2f}x" for _, f in tail)
        if len(tail) >= decay_bins and all(f["ratio"] is not None and f["ratio"] < PARITY
                                           for _, f in tail):
            res[name] = ("DECAYING",
                         f"{decay_bins} consecutive measured bins below parity ({ratios})", hist)
        elif last_f["ratio"] is not None and last_f["ratio"] < PARITY:
            res[name] = ("WATCH", f"current bin {last_f['ratio']:.2f}x "
                                  f"(one bin -- not yet a trend)", hist)
        else:
            res[name] = ("HEALTHY", f"current bin {last_f['ratio']:.2f}x", hist)
    return res


def report(handle, cov, series, verd, formats):
    print(f"\n{'='*94}\nFORMAT DECAY -- {handle}\n{cov}")
    print(f"bins of {WINDOW_DAYS}d - ratio = format median views/day vs THAT BIN's channel median "
          f"- min n={MIN_N}\nUNMEASURED means unmeasured, NOT dead.\n{'='*94}")
    for b in series:
        marks = []
        for name, f in b["formats"].items():
            tag = f"{f['ratio']:.2f}x" if f["ratio"] is not None else "-"
            if not f["measured"]:
                tag += "?"
            marks.append(f"{name} {tag} (n={f['n']})")
        print(f"  {b['start']} -> {b['end']}  n={b['n']:>3}  "
              f"chan {b['channel_median_vpd']:.2f} vpd   " + " | ".join(marks))
    ORDER = ["DECAYING", "WATCH", "STALE", "PROMISING", "HEALTHY", "UNMEASURED"]
    print(f"\n{'format':<26} {'verdict':>11}   why")
    bad = False
    for name, (v, why, _) in sorted(verd.items(), key=lambda kv: ORDER.index(kv[1][0])):
        if v == "DECAYING":
            bad = True
        print(f"{name:<26} {v:>11}   {why}")
    print("\n  ? = below the minimum sample for that bin; shown for shape, excluded from verdicts.")
    if bad:
        print("\n  ACTION: a format you own is below parity two measured bins running.")
        print("  That is the Fireship moment -- they cut '100 Seconds' from 55% to 1-5% of output.")
        print("  This tool says WHEN to look, not WHY. Run a teardown before changing anything.")
    return bad


def main():
    ap = argparse.ArgumentParser(description="Watch OUR formats for decay.")
    ap.add_argument("--channel", required=True, help="@handle of a channel we own")
    ap.add_argument("--config", default=CONFIG)
    ap.add_argument("--window", type=int, default=WINDOW_DAYS)
    ap.add_argument("--min-n", type=int, default=MIN_N)
    ap.add_argument("--no-pull", action="store_true", help="report from cache only")
    ap.add_argument("--refresh", action="store_true", help="re-pull the catalog listing")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    formats = load_formats(a.config)
    if a.no_pull:
        d = os.path.join(CACHE, a.channel.lstrip("@"), "info")
        rows = []
        for f in os.listdir(d) if os.path.isdir(d) else []:
            if not f.endswith(".info.json"):
                continue
            v = json.load(open(os.path.join(d, f)))
            s = v.get("upload_date")
            if not s or (v.get("view_count") or 0) <= 0 or (v.get("duration") or 0) < MIN_SECONDS:
                continue
            rows.append(dict(id=v["id"], title=v.get("title", ""), views=v["view_count"],
                             dur=v["duration"],
                             dt=datetime.date(int(s[:4]), int(s[4:6]), int(s[6:]))))
        cov = f"{len(rows)} videos from cache (no pull)"
    else:
        rows, cov = pull(a.channel, refresh=a.refresh)

    if not rows:
        sys.exit("no usable videos")
    series = analyse(rows, formats, window=a.window, min_n=a.min_n)
    verd = verdicts(series, formats)

    if a.json:
        print(json.dumps({"channel": a.channel, "coverage": cov, "series": series,
                          "verdicts": {k: v[0] for k, v in verd.items()}}, indent=1))
        return 1 if any(v[0] == "DECAYING" for v in verd.values()) else 0

    bad = report(a.channel, cov, series, verd, formats)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
