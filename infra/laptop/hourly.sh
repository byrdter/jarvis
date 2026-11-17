#!/bin/bash
# The laptop's hourly jobs (launchd: com.jarvis.laptop-hourly). Each job logs to ~/Library/Logs/.
# 1. Library ingest first: quick, local, and doesn't need the network except for the brain sync.
# 2. YouTube transcripts: needs the server and YouTube; skips quietly when offline.
# 3. Brain: pull what the server wrote, then refresh the local search index (brain-ask.py).
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=/opt/homebrew/bin/python3
"$PY" "$HERE/ingest-library.py"
"$PY" "$HERE/yt-transcribe.py"
bash "$HOME/code/jarvis-brain/scripts/brain-sync.sh" || true
"$PY" "$HERE/brain-ask.py" index || true
exit 0
