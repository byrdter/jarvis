#!/usr/bin/env bash
# build-master.sh — concat all V14 scene renders into a single master.mp4
#
# Usage:
#   build-master.sh [VIDEO_DIR] [OUT_FILE]
#
# Defaults:
#   VIDEO_DIR = current working directory
#   OUT_FILE  = master.mp4 (in VIDEO_DIR)
#
# How it picks each scene's canonical render:
#   1. If scenes/NN-pilot/renders/LOCKED file exists, use the filename it points at
#   2. Otherwise, use the most recent .mp4 in scenes/NN-pilot/renders/ by mtime
#
# How to lock a scene's "current best take" so iterating doesn't re-pick:
#   echo "01-pilot_2026-06-03_18-26-27.mp4" > scenes/01-pilot/renders/LOCKED
#
# How to unlock and go back to latest-by-mtime:
#   rm scenes/01-pilot/renders/LOCKED

set -euo pipefail

VIDEO_DIR="${1:-$(pwd)}"
OUT_FILE="${2:-master.mp4}"

if [ ! -d "$VIDEO_DIR/scenes" ]; then
  echo "❌ $VIDEO_DIR/scenes/ not found — is this a V14 project root?" >&2
  exit 1
fi

cd "$VIDEO_DIR"

CONCAT_LIST=$(mktemp)
SCENE_NAMES=$(mktemp)
trap "rm -f $CONCAT_LIST $SCENE_NAMES" EXIT

echo "📂 V14 master build — $VIDEO_DIR"
echo ""

# Walk every scene directory in numeric order
for scene_dir in $(ls -d scenes/*-pilot 2>/dev/null | sort); do
  renders="$scene_dir/renders"
  scene_name=$(basename "$scene_dir")

  if [ ! -d "$renders" ]; then
    echo "❌ $scene_name — no renders/ directory" >&2
    exit 1
  fi

  # Prefer the LOCKED file if it exists
  if [ -f "$renders/LOCKED" ]; then
    locked_name=$(head -1 "$renders/LOCKED" | tr -d '[:space:]')
    chosen="$renders/$locked_name"
    pin_marker="🔒 LOCKED"
  else
    chosen=$(ls -t "$renders"/*.mp4 2>/dev/null | head -1)
    pin_marker="latest"
  fi

  if [ ! -f "$chosen" ]; then
    echo "❌ $scene_name — no MP4 found in $renders" >&2
    exit 1
  fi

  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$chosen")
  printf "  ✓ %-12s %s (%ss) [%s]\n" "$scene_name" "$(basename "$chosen")" "$duration" "$pin_marker"

  echo "file '$(realpath "$chosen")'" >> "$CONCAT_LIST"
  echo "$scene_name $(basename "$chosen") $duration" >> "$SCENE_NAMES"
done

echo ""
echo "🔧 ffmpeg concat (re-encoded for codec consistency)..."

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  "$OUT_FILE"

master_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_FILE")
master_size=$(ls -lh "$OUT_FILE" | awk '{print $5}')

echo ""
echo "✅ $OUT_FILE — ${master_duration}s ($master_size)"

# Length sanity vs. V14 minimum
min_secs=480
if (( $(echo "$master_duration < $min_secs" | bc -l) )); then
  remaining=$(echo "$min_secs - $master_duration" | bc -l)
  echo "⚠️  Below V14 minimum (8 min / 480s). Add ~${remaining}s of content before shipping."
  echo "   See ~/.claude/skills/byrddynasty-video-v14/MIN-LENGTH.md for how."
else
  target_min=600
  if (( $(echo "$master_duration < $target_min" | bc -l) )); then
    echo "ℹ️  Above 8-min minimum. V14 ideal range is 10–15 min."
  else
    echo "✅ Within V14 ideal range (10–15 min)."
  fi
fi

# Write a manifest of what went into this cut
manifest="${OUT_FILE}.manifest.json"
{
  echo "{"
  echo "  \"built_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"video_dir\": \"$(realpath "$VIDEO_DIR")\","
  echo "  \"output\": \"$OUT_FILE\","
  echo "  \"duration_seconds\": $master_duration,"
  echo "  \"scenes\":"
  echo "  ["
  first=1
  while IFS=$' ' read -r sname fname dur; do
    [ "$first" = 1 ] && first=0 || echo "    ,"
    echo "    { \"scene\": \"$sname\", \"file\": \"$fname\", \"duration_seconds\": $dur }"
  done < "$SCENE_NAMES"
  echo "  ]"
  echo "}"
} > "$manifest"
echo "📋 wrote $manifest"
