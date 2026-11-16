#!/bin/bash
# Run on the laptop: installs the hourly YouTube transcription job (see yt-transcribe.py for why
# it runs here and not on the server). Needs yt-dlp, ffmpeg, whisper-cpp (brew) and a model at
# ~/.whisper-models/ggml-small.en.bin.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/Library/LaunchAgents/com.jarvis.yt-transcribe.plist"
sed "s#__HOME__#$HOME#" "$HERE/com.jarvis.yt-transcribe.plist" > "$DEST"
launchctl bootout "gui/$(id -u)/com.jarvis.yt-transcribe" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
echo "installed; log: ~/Library/Logs/jarvis-yt-transcribe.log"
