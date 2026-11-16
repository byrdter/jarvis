#!/bin/bash
# JARVIS AI-Futures Daily Pipeline (Byrddynasty knowledge pipeline)
#   1. sweep RSS sources (daily cadence; + weekly on Mon, + monthly on the 1st)
#   2. ingest any new academic PDFs the user dropped in
#   3. build digest + deliver via Gmail (preferred) or Telegram (fallback)
#   4. reindex FTS + embeddings, rebuild knowledge graph
#
# Designed to live OUTSIDE Dropbox/CloudStorage so macOS TCC lets launchd run it.

set -eo pipefail

# Sanitize env — same fix the news-aggregator uses.
unset VIRTUAL_ENV PYTHONPATH PYTHONHOME
export PATH="/Users/terrybyrd/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date +%Y-%m-%d)
LOG_DIR="/Users/terrybyrd/.local/share/jarvis/ai-futures/logs"
STDOUT_LOG="$LOG_DIR/ai-futures-stdout.log"
STDERR_LOG="$LOG_DIR/ai-futures-stderr.log"
AGENT_SDK_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/agent-sdk"

mkdir -p "$LOG_DIR"
exec >>"$STDOUT_LOG" 2>>"$STDERR_LOG"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  JARVIS AI-Futures Daily — $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "════════════════════════════════════════════════════════════"

cd "$AGENT_SDK_DIR" || { echo "❌ Cannot cd $AGENT_SDK_DIR"; exit 1; }

# Load .env. macOS TCC blocks launchd from `source`-ing files inside the Dropbox
# CloudStorage mount, so prefer a home-copy at ~/.config/jarvis/ai-futures.env
# (TCC-readable). Fall back to Dropbox for interactive runs from a normal shell.
# Use set +e around the load so a permission failure doesn't kill the wrapper.
ENV_HOME="$HOME/.config/jarvis/ai-futures.env"
ENV_DROPBOX="$AGENT_SDK_DIR/.env"
set +e
if [ -r "$ENV_HOME" ]; then
  echo "→ loading env: $ENV_HOME"
  set -a; source "$ENV_HOME" 2>/dev/null; set +a
elif [ -r "$ENV_DROPBOX" ]; then
  echo "→ loading env: $ENV_DROPBOX"
  set -a; source "$ENV_DROPBOX" 2>/dev/null; set +a
else
  echo "⚠️  no .env found — Telegram/Gmail delivery may fail"
fi
set -e

# Day-of-week → which extra cadences to fold in (Bun script chooses these
# automatically inside the scheduler.ts version of the job; CLI version is
# simpler — daily + day-trigger).
DOW=$(date +%u)   # 1=Mon … 7=Sun
DOM=$(date +%d)
EXTRAS=""
[ "$DOW" = "1" ] && EXTRAS="$EXTRAS weekly"
[ "$DOM" = "01" ] && EXTRAS="$EXTRAS monthly"

echo "→ Sweeping daily$EXTRAS"
bun run src/fetchers/sweep.ts daily $EXTRAS || echo "⚠️  sweep returned non-zero"

echo "→ Ingesting academic library"
bun run src/fetchers/ingest-academic.ts || echo "⚠️  academic ingest non-zero"

echo "→ Reindexing FTS + embeddings"
bun run src/fetchers/reindex-ai-futures.ts || echo "⚠️  reindex non-zero"

echo "→ Rebuilding knowledge graph"
bun run src/fetchers/graph.ts build || echo "⚠️  graph build non-zero"

echo "→ Delivering digest (Gmail if configured, else Telegram)"
bun run src/fetchers/digest.ts daily $EXTRAS || echo "⚠️  digest non-zero"

echo "✅ done $(date '+%H:%M:%S')"
