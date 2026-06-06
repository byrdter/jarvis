#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: $0 <episode-folder>" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$SKILL_DIR/templates/episode-command-center"
EPISODE_DIR="$1"

mkdir -p "$EPISODE_DIR"

for template in "$TEMPLATE_DIR"/*.md; do
  name="$(basename "$template")"
  [ "$name" = "README.md" ] && continue
  dest="$EPISODE_DIR/$name"
  if [ -e "$dest" ]; then
    echo "skip $dest (exists)"
  else
    cp -f "$template" "$dest"
    echo "created $dest"
  fi
done

mkdir -p "$EPISODE_DIR/scenes"
echo "ready $EPISODE_DIR"
