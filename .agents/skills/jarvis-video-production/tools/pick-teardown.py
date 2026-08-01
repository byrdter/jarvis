#!/usr/bin/env python3
"""
Weekly teardown picker — choose one proven video and tear it down for study.

    python3 pick-teardown.py            # pick + tear down this week's candidate
    python3 pick-teardown.py --dry      # show the shortlist, tear nothing down
    python3 pick-teardown.py --url URL  # override the pick

WHY THIS EXISTS (DECISION-RECORD-2026-08-01, the 10-video run)
    teardown.py is the most underused tool in the repo. Everything genuinely learned on
    2026-07-31/08-01 came from reading one transcript against one number — and from being
    wrong four times doing it. Noema looked like the model until the teardown showed a
    panel with a housekeeping open; Mackard's 73x turned out to have no curiosity structure
    at all. Neither is visible from the outside.

    So: one teardown a week, alongside the week's build. Ten weeks, ten teardowns. This
    script does the MECHANICAL half (pick, fetch, measure) and stops. The ANALYSIS section
    is left blank ON PURPOSE — that is the part that teaches, and a script cannot do it.

SELECTION
    Ranks the ratchet's recent candidates and picks the highest-outlier one that is
      * not already in teardowns/
      * flagged on-topic where the classifier ran (about_ai != 'no')
      * NOT shape='clip'. A podcast clip's number comes from the famous person in it —
        borrowed authority, which is structurally uncopyable. That confound accounted for
        four of the biggest figures measured on 2026-07-31 (Noema, Decoded Genius,
        Perimeter/Veritasium, TRIGGERnometry). Tearing one down teaches nothing.
    Ties break toward the SMALLER channel: a 20x on 9k subs is a more copyable lesson
    than a 20x on 400k, where reach may be doing the work.

    ⚠️ KNOWN LIMITATION — READ THE SHORTLIST, DO NOT TRUST THE TOP ROW.
    The ratchet's watchlist was grown for the AI-commentary / anti-work lane the channel
    ABANDONED on 2026-08-01. So the shortlist still drifts there: on the first run the top
    pick was "How a 9 to 5 job takes over your life" (232x) — a real outlier in a lane we
    are not in. Shapes proven for OUR register are verdict / explainer / framework /
    comparison. Anything else, use --url and pick deliberately. This resolves itself once
    `outlier-ratchet.py --discover` is re-aimed at the build lane.
"""
import csv, glob, os, re, subprocess, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
RATCHET = os.path.join(HERE, "ratchet")
TEARDOWNS = os.path.join(HERE, "teardowns")
MIN_MINUTES = 8


def already_done():
    ids = set()
    for f in glob.glob(os.path.join(TEARDOWNS, "*.md")):
        ids.add(os.path.splitext(os.path.basename(f))[0])
    return ids


def vid_id(url):
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else None


def shortlist(limit=12):
    rows, seen = [], set()
    files = sorted(glob.glob(os.path.join(RATCHET, "classified-*.csv")), reverse=True) + \
            sorted(glob.glob(os.path.join(RATCHET, "candidates-*.csv")), reverse=True)
    done = already_done()
    for f in files:
        try:
            for r in csv.DictReader(open(f, encoding="utf8")):
                vid = vid_id(r.get("url"))
                if not vid or vid in seen or vid in done:
                    continue
                # the classifier only runs on some files; when present, respect it
                if (r.get("about_ai") or "").strip() == "no":
                    continue
                if (r.get("shape") or "").strip() == "clip":
                    continue          # borrowed authority — uncopyable, teaches nothing
                try:
                    out = float(r.get("outlier") or 0)
                    subs = int(float(r.get("subs") or 0))
                except ValueError:
                    continue
                if out <= 0 or subs < 1000:
                    continue
                seen.add(vid)
                rows.append({"id": vid, "outlier": out, "subs": subs,
                             "channel": (r.get("channel") or "").strip(),
                             "title": (r.get("title") or "").strip(),
                             "url": r.get("url"), "shape": (r.get("shape") or "").strip(),
                             "src": os.path.basename(f)})
        except OSError:
            continue
    # highest outlier first; ties toward the smaller channel (more copyable)
    rows.sort(key=lambda r: (-r["outlier"], r["subs"]))
    return rows[:limit]


def main():
    ap = argparse.ArgumentParser(description="Pick and tear down one video a week")
    ap.add_argument("--dry", action="store_true", help="show the shortlist, tear nothing down")
    ap.add_argument("--url", help="override the pick")
    a = ap.parse_args()

    if a.url:
        target, why = vid_id(a.url) or a.url, "manual override"
        if not target:
            sys.exit("could not parse a video id from --url")
    else:
        cands = shortlist()
        if not cands:
            print("No new candidates. Run the ratchet first:\n"
                  "  python3 outlier-ratchet.py --monitor")
            return 0
        print(f"SHORTLIST — {len(cands)} untorn candidates, highest outlier first\n")
        print(f"{'outlier':>9} {'subs':>9}  {'shape':<12} channel / title")
        for i, r in enumerate(cands):
            mark = "->" if i == 0 else "  "
            print(f"{mark}{r['outlier']:>7.2f}x {r['subs']:>9,}  {r['shape'][:12]:<12} "
                  f"{r['channel'][:22]:24} {r['title'][:52]}")
        pick = cands[0]
        target, why = pick["id"], f"{pick['outlier']:.2f}x on {pick['subs']:,} subs"
        print(f"\nPICK: {pick['title'][:70]}\n      {why}")
        ON_REGISTER = {"verdict", "explainer", "framework", "comparison"}
        if pick["shape"] and pick["shape"] not in ON_REGISTER:
            print(f"\n  ⚠️  shape='{pick['shape']}' is NOT one of the shapes proven for our"
                  f" register\n      ({', '.join(sorted(ON_REGISTER))}). The watchlist still"
                  f" leans to the abandoned lane.\n      Consider picking from the shortlist"
                  f" above with --url instead.")

    if a.dry:
        print("\n--dry: nothing torn down.")
        return 0

    print(f"\nRunning teardown on {target} ...\n")
    rc = subprocess.run([sys.executable, os.path.join(HERE, "teardown.py"), target]).returncode
    if rc != 0:
        print(f"teardown.py exited {rc}", file=sys.stderr)
        return rc

    print("\n" + "=" * 74)
    print("  MECHANICAL HALF DONE. The half that teaches is not.")
    print("  Open teardowns/%s.md and fill in the ANALYSIS section." % target)
    print("  Answer #7 TRANSFERABLE STRUCTURE last and in your own words — that is")
    print("  the only part you will still remember in ten weeks.")
    print("=" * 74)
    return 0


sys.exit(main())
