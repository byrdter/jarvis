#!/usr/bin/env bash
# extract-vo.sh — Extract audio and generate transcript from HeyGen video
#
# Usage:
#   ./extract-vo.sh <heygen-video.mp4> <output-dir>
#
# Output:
#   <output-dir>/assets/audio.mp3
#   <output-dir>/assets/transcript.json
#   <output-dir>/analysis/vo-analysis.json

set -euo pipefail

# Args
HEYGEN_VIDEO="${1:?Usage: $0 <heygen-video.mp4> <output-dir>}"
OUTPUT_DIR="${2:?Usage: $0 <heygen-video.mp4> <output-dir>}"

# Validate input
if [ ! -f "$HEYGEN_VIDEO" ]; then
  echo "❌ Error: Video file not found: $HEYGEN_VIDEO" >&2
  exit 1
fi

# Create directories
mkdir -p "$OUTPUT_DIR/assets"
mkdir -p "$OUTPUT_DIR/analysis"

AUDIO_OUT="$OUTPUT_DIR/assets/audio.mp3"
TRANSCRIPT_OUT="$OUTPUT_DIR/assets/transcript.json"
ANALYSIS_OUT="$OUTPUT_DIR/analysis/vo-analysis.json"

echo "🎬 Extracting audio from HeyGen video..."
echo "   Input: $HEYGEN_VIDEO"
echo "   Output: $AUDIO_OUT"
echo ""

# Extract audio stream
ffmpeg -i "$HEYGEN_VIDEO" -vn -acodec libmp3lame -ab 192k -ar 48000 "$AUDIO_OUT" -y -hide_banner -loglevel error

if [ ! -f "$AUDIO_OUT" ]; then
  echo "❌ Error: Failed to extract audio" >&2
  exit 1
fi

AUDIO_SIZE=$(ls -lh "$AUDIO_OUT" | awk '{print $5}')
echo "✓ Extracted audio → $AUDIO_OUT ($AUDIO_SIZE)"
echo ""

# Get duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_OUT")
DURATION_INT=${DURATION%.*}
MINUTES=$((DURATION_INT / 60))
SECONDS=$((DURATION_INT % 60))

echo "🎤 Transcribing audio with word-level timestamps..."
echo "   Duration: ${DURATION}s (${MINUTES}m ${SECONDS}s)"
echo ""

# Check if we're in a HyperFrames project directory
if [ -f "$OUTPUT_DIR/hyperframes.json" ]; then
  # Use HyperFrames transcribe (in project directory)
  cd "$OUTPUT_DIR"
  npx hyperframes transcribe "assets/audio.mp3" --output "assets/transcript.json"
  cd - >/dev/null
else
  # Use HyperFrames transcribe from audio file location
  npx hyperframes transcribe "$AUDIO_OUT" --output "$TRANSCRIPT_OUT"
fi

if [ ! -f "$TRANSCRIPT_OUT" ]; then
  echo "❌ Error: Failed to generate transcript" >&2
  exit 1
fi

# Count words
WORD_COUNT=$(jq '.words | length' "$TRANSCRIPT_OUT")
echo "✓ Transcribed → $TRANSCRIPT_OUT ($WORD_COUNT words)"
echo ""

# Generate VO analysis
echo "📊 Analyzing VO characteristics..."

python3 <<PYTHON
import json
import sys

# Load transcript
with open("$TRANSCRIPT_OUT", "r") as f:
    transcript = json.load(f)

words = transcript.get("words", [])
duration = float("$DURATION")

# Calculate speaking pace
word_count = len(words)
words_per_minute = (word_count / duration) * 60 if duration > 0 else 0

# Find natural pauses (≥1.5s silence between words)
pauses = []
for i in range(len(words) - 1):
    current_end = words[i].get("end", 0)
    next_start = words[i + 1].get("start", 0)
    gap = next_start - current_end

    if gap >= 1.5:
        pauses.append({
            "timestamp": current_end,
            "duration": round(gap, 2)
        })

# Extract top keywords (simple frequency count, excluding common words)
stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "what", "which", "who", "when", "where", "why", "how"}

word_freq = {}
for word_obj in words:
    word = word_obj.get("text", "").lower().strip(".,!?;:")
    if word and word not in stopwords and len(word) > 2:
        word_freq[word] = word_freq.get(word, 0) + 1

# Sort by frequency and take top 10
top_keywords = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10])

# Build analysis
analysis = {
    "duration_seconds": duration,
    "word_count": word_count,
    "words_per_minute": round(words_per_minute, 1),
    "natural_pauses": pauses,
    "pause_count": len(pauses),
    "top_keywords": top_keywords
}

# Write analysis
with open("$ANALYSIS_OUT", "w") as f:
    json.dump(analysis, f, indent=2)

print(f"  - Duration: {duration:.1f}s ({int(duration//60)}m {int(duration%60)}s)")
print(f"  - Speaking pace: {words_per_minute:.0f} words/min")
print(f"  - Natural pauses: {len(pauses)} (≥1.5s silence)")
print(f"  - Top keywords: {', '.join(list(top_keywords.keys())[:5])}")

PYTHON

echo ""
echo "✓ VO analysis → $ANALYSIS_OUT"
echo ""
echo "✅ Complete!"
echo ""
echo "Next steps:"
echo "  1. Review transcript: cat $TRANSCRIPT_OUT | jq '.words[:10]'"
echo "  2. Review analysis: cat $ANALYSIS_OUT"
echo "  3. Generate scene plan: python3 scripts/generate-scene-plan.py \\"
echo "       --transcript $TRANSCRIPT_OUT \\"
echo "       --brief episode-brief.md \\"
echo "       --output visual-treatment-board.md"
