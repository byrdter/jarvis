#!/bin/bash
# Run on the laptop: installs the hourly job (library ingest + YouTube transcripts; see hourly.sh).
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
mkdir -p "$HOME/JARVIS-Library"
echo "installed. Drop documents in ~/JARVIS-Library/<creator>/. Logs: ~/Library/Logs/jarvis-*.log"
