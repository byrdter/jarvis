#!/bin/bash
# Run on the laptop: installs the hourly job (library ingest, YouTube transcripts, brain sync + search
# index; see hourly.sh) and the brain chat page at http://localhost:8765 (brain-ask.py).
# Needs yt-dlp, ffmpeg, whisper-cpp (brew), pypdf, and a model at ~/.whisper-models/ggml-small.en.bin.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
UID_=$(id -u)
# Replace the older single-purpose job if it's installed.
launchctl bootout "gui/$UID_/com.jarvis.yt-transcribe" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/com.jarvis.yt-transcribe.plist"
DEST="$HOME/Library/LaunchAgents/com.jarvis.laptop-hourly.plist"
sed "s#__HOME__#$HOME#" "$HERE/com.jarvis.laptop-hourly.plist" > "$DEST"
launchctl bootout "gui/$UID_/com.jarvis.laptop-hourly" 2>/dev/null || true
launchctl bootstrap "gui/$UID_" "$DEST"
DEST2="$HOME/Library/LaunchAgents/com.jarvis.brain-ask.plist"
sed "s#__HOME__#$HOME#" "$HERE/com.jarvis.brain-ask.plist" > "$DEST2"
launchctl bootout "gui/$UID_/com.jarvis.brain-ask" 2>/dev/null || true
launchctl bootstrap "gui/$UID_" "$DEST2"
mkdir -p "$HOME/JARVIS-Library"
echo "installed. Brain chat: http://localhost:8765. Drop documents in ~/JARVIS-Library/<creator>/. Logs: ~/Library/Logs/jarvis-*.log"
