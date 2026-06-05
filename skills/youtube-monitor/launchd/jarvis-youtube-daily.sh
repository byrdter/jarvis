#!/bin/bash
# JARVIS YouTube Daily AI Monitor
# Runs daily at 10 AM to check 77 AI YouTube channels
# Pipeline: harvest -> transcripts (captions + Whisper fallback) -> vault + knowledge DB -> Phase 2B reindex -> email

set -eo pipefail

# Sanitize env (prevents launchd from picking up a Dropbox-side venv -> deadlock)
unset VIRTUAL_ENV PYTHONPATH PYTHONHOME
export PATH="/Users/terrybyrd/.local/share/jarvis/youtube-monitor/venv/bin:/Users/terrybyrd/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

PYTHON="/Users/terrybyrd/.local/share/jarvis/youtube-monitor/venv/bin/python3"
MONITOR_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/skills/youtube-monitor"
AGENT_SDK_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/agent-sdk"

cd "$MONITOR_DIR"
"$PYTHON" monitor_channels.py --email --transcripts

# Trigger Phase 2B vector reindex on the vault so the new transcripts become
# searchable via JARVIS hybrid (vector + keyword) memory search.
# Non-fatal: if Bun or the indexer is missing, log and continue.
if command -v bun >/dev/null 2>&1 && [ -f "$AGENT_SDK_DIR/scripts/index-vault.ts" ]; then
    echo ""
    echo "🔄 Triggering Phase 2B vector reindex..."
    (cd "$AGENT_SDK_DIR" && bun run scripts/index-vault.ts) || echo "⚠️  Vector reindex failed (non-fatal)"
else
    echo "⚠️  Skipping vector reindex (bun or index-vault.ts not found)"
fi
