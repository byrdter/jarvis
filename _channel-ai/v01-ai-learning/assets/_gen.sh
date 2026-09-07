#!/bin/bash
# Generate every still with Codex — FREE on Terry's ChatGPT subscription.
# Mirrors ai-film-studio/locations/_gen.sh. NEVER pay image credits for these.
cd "$(dirname "$0")"
OUT="${1:-generated}"; mkdir -p "$OUT"
for f in prompts/*.txt; do
  slug=$(basename "$f" .txt)
  [ -f "$OUT/$slug.png" ] && { echo "skip $slug"; continue; }
  echo "=== $slug"
  codex exec --skip-git-repo-check --sandbox workspace-write \
    "Use your image_gen__imagegen tool to generate ONE 16:9 landscape image at the largest size you can, and save the PNG into $OUT/ as exactly: $slug.png

$(cat "$f")

Print only the saved absolute path when done." >/dev/null 2>&1
  [ -f "$OUT/$slug.png" ] && echo "  ok" || echo "  FAILED"
done
echo "DONE: $(ls -1 "$OUT"/*.png 2>/dev/null | wc -l | tr -d ' ') stills present in $OUT/"
