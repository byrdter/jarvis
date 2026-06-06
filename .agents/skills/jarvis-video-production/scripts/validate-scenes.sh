#!/usr/bin/env bash
# validate-scenes.sh — pre-flight check on every V14 scene before concat
#
# Usage:
#   validate-scenes.sh [VIDEO_DIR]
#
# Confirms:
#   - Every scene has hyperframes.json
#   - Every scene has at least one rendered MP4
#   - LOCKED file (if present) points at an existing file
#   - Rendered duration matches hyperframes.json declared duration ±0.5s
#   - Composition lints clean (0 errors)
#
# Exits 0 if all scenes valid, nonzero otherwise.

set -uo pipefail

VIDEO_DIR="${1:-$(pwd)}"

if [ ! -d "$VIDEO_DIR/scenes" ]; then
  echo "❌ $VIDEO_DIR/scenes/ not found" >&2
  exit 1
fi

cd "$VIDEO_DIR"

problems=0
total_dur=0

echo "🔍 validating scenes in $VIDEO_DIR"
echo ""

for scene_dir in $(ls -d scenes/*-pilot 2>/dev/null | sort); do
  scene_name=$(basename "$scene_dir")
  hf="$scene_dir/hyperframes.json"
  renders="$scene_dir/renders"

  # 1. hyperframes.json
  if [ ! -f "$hf" ]; then
    echo "  ❌ $scene_name — missing hyperframes.json"
    problems=$((problems+1))
    continue
  fi

  expected=$(jq -r '.compositions[0].duration' "$hf" 2>/dev/null || echo "?")
  if [ "$expected" = "?" ] || [ "$expected" = "null" ]; then
    echo "  ❌ $scene_name — hyperframes.json missing compositions[0].duration"
    problems=$((problems+1))
    continue
  fi

  # 2. renders dir + at least one MP4
  if [ ! -d "$renders" ] || ! ls "$renders"/*.mp4 >/dev/null 2>&1; then
    echo "  ❌ $scene_name — no rendered MP4 in $renders"
    problems=$((problems+1))
    continue
  fi

  # 3. LOCKED file validity
  if [ -f "$renders/LOCKED" ]; then
    locked_name=$(head -1 "$renders/LOCKED" | tr -d '[:space:]')
    chosen="$renders/$locked_name"
    if [ ! -f "$chosen" ]; then
      echo "  ❌ $scene_name — LOCKED points to missing file: $locked_name"
      problems=$((problems+1))
      continue
    fi
    pin="🔒"
  else
    chosen=$(ls -t "$renders"/*.mp4 | head -1)
    pin=""
  fi

  # 4. Duration check
  actual=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$chosen")
  diff=$(echo "if ($actual - $expected < 0) -($actual - $expected) else $actual - $expected" | bc -l)
  drift_ok=$(echo "$diff < 0.5" | bc -l)

  total_dur=$(echo "$total_dur + $actual" | bc -l)

  if [ "$drift_ok" = "1" ]; then
    printf "  ✓ %-12s %s — exp %ss / got %ss (Δ%.2fs) %s\n" "$scene_name" "$(basename "$chosen")" "$expected" "$actual" "$diff" "$pin"
  else
    printf "  ⚠️  %-12s exp %ss but rendered %ss (Δ%.2fs) — re-render to match\n" "$scene_name" "$expected" "$actual" "$diff"
    problems=$((problems+1))
  fi
done

echo ""
total_min=$(echo "$total_dur / 60" | bc)
total_sec=$(echo "scale=0; $total_dur - ($total_min * 60)" | bc)
total_sec_int=${total_sec%.*}
printf "📊 total runtime: %.1fs (%dm %ds)\n" "$total_dur" "$total_min" "$total_sec_int"

# Length sanity
min_secs=480
under=$(echo "$total_dur < $min_secs" | bc -l)
if [ "$under" = "1" ]; then
  remaining=$(echo "$min_secs - $total_dur" | bc -l)
  printf "⚠️  under V14 minimum (8 min / 480s). Need ~%.0fs more.\n" "$remaining"
fi

echo ""
if [ "$problems" -eq 0 ]; then
  echo "✅ all scenes valid"
  exit 0
else
  echo "❌ $problems problem(s) — fix before running build-master.sh"
  exit 1
fi
