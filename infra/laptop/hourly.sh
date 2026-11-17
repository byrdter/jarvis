#!/bin/bash
# The laptop's hourly jobs (launchd: com.jarvis.laptop-hourly). Each job logs to ~/Library/Logs/.
# 1. Library ingest first: quick, local, and doesn't need the network except for the brain sync.
# 2. YouTube transcripts: needs the server and YouTube; skips quietly when offline.
# 3. Brain: pull what the server wrote, then refresh the local search index (brain-ask.py).
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=/opt/homebrew/bin/python3
"$PY" "$HERE/ingest-library.py"
"$PY" "$HERE/yt-transcribe.py"
# Laptop Claude memory -> the brain, so the server sees it too (copies only; never deletes).
MEM="$HOME/Dropbox/jarvis-private/claude-memory/jarvis/memory"
rsync -a --include='*.md' --exclude='*' "$MEM/" "$HOME/code/jarvis-brain/raw/claude-memory/" \
  && echo "$(date '+%F %T') memory copy ok" \
  || echo "$(date '+%F %T') memory copy FAILED (launchd may be denied Dropbox access; see reference_launchd_tcc_and_storage)"
bash "$HOME/code/jarvis-brain/scripts/brain-sync.sh" || true
"$PY" "$HERE/brain-ask.py" index || true
exit 0
