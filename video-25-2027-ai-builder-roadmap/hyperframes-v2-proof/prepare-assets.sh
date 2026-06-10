#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"

mkdir -p "$ROOT/assets"

printf "file '%s'\nfile '%s'\n" \
  "$REPO/video-25-2027-ai-builder-roadmap/heygen/scenes/scene-01.wav" \
  "$REPO/video-25-2027-ai-builder-roadmap/heygen/scenes/scene-02.wav" \
  > "$ROOT/assets/audio-concat.txt"

ffmpeg -y -loglevel error \
  -f concat -safe 0 \
  -i "$ROOT/assets/audio-concat.txt" \
  -c copy "$ROOT/assets/audio.wav"

cp -f "$REPO/asset-library/products/chatgpt/surfaces/web/scroll-homepage.webm" "$ROOT/assets/chatgpt-scroll.webm"
cp -f "$REPO/asset-library/products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png" "$ROOT/assets/claude-code.png"
cp -f "$REPO/asset-library/products/codex/desktop/CodexDesktop.png" "$ROOT/assets/codex.png"
cp -f "$REPO/asset-library/products/github/surfaces/web/pull-requests-scroll.webm" "$ROOT/assets/github-pr-scroll.webm"

echo "Prepared v2 proof assets in $ROOT/assets"

