#!/bin/bash
# Promote the free Codex stills into backgrounds/ and broll/, archiving the paid
# Higgsfield versions to alt-higgsfield/ (gitignored — regenerable, not worth carrying).
cd "$(dirname "$0")"
mkdir -p alt-higgsfield
swapped=0; missing=0
for f in generated/*.png; do
  slug=$(basename "$f" .png)
  case "$slug" in *-bg-*) dest=backgrounds ;; *) dest=broll ;; esac
  [ -f "$dest/$slug.png" ] && mv "$dest/$slug.png" "alt-higgsfield/$slug.png"
  cp "$f" "$dest/$slug.png"; swapped=$((swapped+1))
done
for f in prompts/*.txt; do
  slug=$(basename "$f" .txt)
  [ -f "generated/$slug.png" ] || { echo "  STILL HIGGSFIELD: $slug"; missing=$((missing+1)); }
done
echo "swapped $swapped · still on paid version: $missing"
