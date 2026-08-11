#!/bin/bash
# jarvis-format-sweep.sh — weekly FORMAT discovery. Runs the teardown front end over every
# channel the outlier ratchet has already found, and reports asset-grade templates that are
# NOT yet in the catalogue.
#
# WHY THIS COMPOSES INSTEAD OF DUPLICATING
#   outlier-ratchet.py already runs daily and permanently grows ratchet/watchlist.json — it
#   answers "which channels beat their own distribution". This answers the different question
#   "what SHAPE do those channels repeat", and channel-template.py is yt-dlp only. So the whole
#   sweep costs ZERO vidIQ credits: discovery is already paid for, and the format layer rides
#   on top of it for free.
#
#   That composition is the point. Before this existed the demand layer ran only when invoked
#   by hand, which cannot satisfy the practitioner's "insider knowledge" barrier — finding a
#   format while it is days old requires a schedule, not an occasional session.
set -uo pipefail

TOOLS="$HOME/Library/CloudStorage/Dropbox/jarvis/.agents/skills/jarvis-video-production/tools"
LOG_DIR="$HOME/Library/CloudStorage/Dropbox/jarvis-private/logs/format-sweep"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y-%m-%d)"
OUT="$LOG_DIR/sweep-$STAMP.md"
cd "$TOOLS" || exit 1

# Asset-grade floors. A template must clear ALL THREE or it is not a channel-worthy shape:
#   median views  — lift is scale-blind; 22x on a 3,900-view base is arithmetic
#   slots         — "a template used once is just a title"
#   share         — above ~60% the template IS the channel and lift measures nothing
MIN_MEDIAN=50000
MIN_SLOTS=5
MAX_SHARE=0.60
MIN_RUNTIME=3        # minutes. Shorts have an order-of-magnitude different view scale;
                     # mixing them in makes lift meaningless (60x on a 2-minute channel).

python3 - "$MIN_MEDIAN" "$MIN_SLOTS" "$MAX_SHARE" "$OUT" "$MIN_RUNTIME" <<'PY'
import json, glob, sys, argparse, importlib.util, subprocess, datetime as dt
from pathlib import Path

min_med, min_slots, max_share, out_path = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
min_runtime = float(sys.argv[5])
spec = importlib.util.spec_from_file_location("ct", "channel-template.py")
ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
a = argparse.Namespace(recent=24)

idx = json.loads(Path("ratchet/formats.json").read_text()) if Path("ratchet/formats.json").exists() else {"formats": {}}
# Visual formats (low-poly shorts, rapid-news 3D) carry title_template = None by design, so
# `or ""` is load-bearing, not defensive noise — without it the sweep dies on the catalogue.
known = {(f.get("title_template") or "").lower() for f in idx["formats"].values()}
known |= {(f.get("name") or "").lower() for f in idx["formats"].values()}
known.discard("")

# 1. every channel the ratchet has found, minus the ones already torn down
wl = json.loads(Path("ratchet/watchlist.json").read_text()) if Path("ratchet/watchlist.json").exists() else {}
have = {Path(p).stem for p in glob.glob("raw/templates/*.json")}
todo = [cid for cid in wl if cid not in have]
print(f"watchlist {len(wl)} · already torn down {len(have)} · new this run {len(todo)}")

for cid in todo[:40]:                      # cap per run so a weekly job stays bounded
    subprocess.run(["python3", "channel-template.py",
                    f"https://www.youtube.com/channel/{cid}", "--top", "1"],
                   capture_output=True, timeout=300)

# 2. mine everything cached, report only what is BOTH asset-grade AND new
rows = []
for f in glob.glob("raw/templates/*.json"):
    vids = json.load(open(f))
    if len(vids) < 10:
        continue
    try:
        res, _ = ct.analyse(vids, a)
    except Exception:
        continue
    for r in res[:3]:
        if (r["median_views"] >= min_med and r["slots"] >= min_slots
                and r["share"] <= max_share and r["median_runtime_min"] >= min_runtime
                and r["template"].lower() not in known):
            rows.append((Path(f).stem, r))

# Collapse near-duplicates to the MOST SPECIFIC form. n-gram extraction emits "business of",
# "the evil" and "the evil business of" for the same videos; reporting all three as separate
# findings is noise that makes an unattended weekly digest unreadable. Longest wins.
keep = []
for cid, r in sorted(rows, key=lambda x: (-len(x[1]["template"].split()), -x[1]["median_views"])):
    if any(r["template"] in k[1]["template"] for k in keep):
        continue
    keep.append((cid, r))
keep.sort(key=lambda x: -x[1]["median_views"])

lines = [f"# Format sweep — {dt.date.today().isoformat()}", "",
         f"{len(wl)} watchlist channels · {len(have) + len(todo)} torn down · "
         f"**{len(keep)} asset-grade templates not yet catalogued**", "",
         "Floors: median >= {:,} · slots >= {} · share <= {:.0%}. A template clearing all three "
         "is a SHAPE worth reading, not a decision — watch the videos before promoting."
         .format(min_med, min_slots, max_share), "",
         "| median | slots | share | lift | run | template | best |",
         "|---:|---:|---:|---:|---:|---|---|"]
for cid, r in keep[:25]:
    best = str(r["best"]["title"]).replace("|", "/")[:52]
    lines.append(f"| {r['median_views']:,} | {r['slots']} | {r['share']:.0%} | {r['lift']}x | "
                 f"{r['median_runtime_min']:.0f}m | `{r['template']}` | {best} |")
lines += ["", "## Promote one",
          "```bash", "cd " + str(Path.cwd()),
          "python3 channel-template.py https://www.youtube.com/channel/<CID> --emit <format-id>",
          "python3 market-gate.py --format <format-id> --market \"<market>\"", "```"]
Path(out_path).write_text("\n".join(lines))
print(f"wrote {out_path} — {len(keep)} new templates")
PY

echo "[$(date)] format sweep complete -> $OUT"
