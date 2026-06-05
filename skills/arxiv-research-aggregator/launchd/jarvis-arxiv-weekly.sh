#!/bin/bash
# JARVIS arXiv Weekly Research Aggregator
#   - Sunday 10 AM scheduled run
#   - 7-day rolling window, up to 50 papers
#   - Persistent dedupe via ai-knowledge.db (no repeats week-over-week)
#   - All papers persisted to ORICO + Obsidian vault + ai-knowledge.db
#   - Phase 2B vector reindex triggered after

set -eo pipefail

# Sanitize env — same fix as YouTube and news; prevents launchd from picking
# up a Dropbox-side venv and hitting "Resource deadlock avoided" or worse,
# Apple TCC blocking execute on Dropbox paths ("Operation not permitted").
unset VIRTUAL_ENV PYTHONPATH PYTHONHOME
export PATH="/Users/terrybyrd/.local/share/jarvis/arxiv-research-aggregator/venv/bin:/Users/terrybyrd/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

PYTHON="/Users/terrybyrd/.local/share/jarvis/arxiv-research-aggregator/venv/bin/python3"
SCRIPT_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/skills/arxiv-research-aggregator"
AGENT_SDK_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/agent-sdk"

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/reports/arxiv-digests"
mkdir -p "$OUTPUT_DIR"
OUTPUT="$OUTPUT_DIR/arxiv-digest-$DATE.md"

echo "============================================"
echo "WEEKLY ARXIV RESEARCH AGGREGATION"
echo "Started: $(date)"
echo "============================================"

cd "$SCRIPT_DIR"
"$PYTHON" aggregate-arxiv.py --days 7 --max-results 50 --output "$OUTPUT"

# Trigger Phase 2B vector reindex so new paper markdowns become searchable.
if command -v bun >/dev/null 2>&1 && [ -f "$AGENT_SDK_DIR/scripts/index-vault.ts" ]; then
    echo ""
    echo "🔄 Triggering Phase 2B vector reindex..."
    (cd "$AGENT_SDK_DIR" && bun run scripts/index-vault.ts) || echo "⚠️  Vector reindex failed (non-fatal)"
fi

echo ""
echo "Completed: $(date)"
