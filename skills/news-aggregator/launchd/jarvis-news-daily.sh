#!/bin/bash
# JARVIS News Aggregator Daily Wrapper
#   - 36h rolling window across 20 RSS feeds + Hacker News
#   - Full-text article extraction via trafilatura
#   - Persistent dedupe via ai-knowledge.db (no day-over-day repeats)
#   - Per-source quota (max 3/source) in email digest, total cap 40
#   - All articles persisted to ORICO + Obsidian vault + ai-knowledge.db

set -eo pipefail

# Sanitize env — same fix as YouTube; prevents launchd from picking up a
# Dropbox-side venv and hitting "Resource deadlock avoided".
unset VIRTUAL_ENV PYTHONPATH PYTHONHOME
export PATH="/Users/terrybyrd/.local/share/jarvis/news-aggregator/venv/bin:/Users/terrybyrd/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date +%Y-%m-%d)
OUTPUT="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/reports/news-digests/ai-news-digest-$DATE.md"
PYTHON="/Users/terrybyrd/.local/share/jarvis/news-aggregator/venv/bin/python3"
SCRIPT_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/skills/news-aggregator"
SCRIPT="$SCRIPT_DIR/aggregate.py"
EMAIL_SCRIPT="$SCRIPT_DIR/send-email.py"
EMAIL_CONFIG="/Users/terrybyrd/.local/share/jarvis/news-aggregator/email-config.sh"
AGENT_SDK_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/agent-sdk"

# Load email configuration (defines EMAIL_TO, SMTP_*)
if [ -f "$EMAIL_CONFIG" ]; then
    source "$EMAIL_CONFIG"
fi

cd "$SCRIPT_DIR"
"$PYTHON" "$SCRIPT" daily --output "$OUTPUT"

# Email digest
if [ -f "$OUTPUT" ]; then
    echo "Sending email digest..."
    "$PYTHON" "$EMAIL_SCRIPT" "$OUTPUT" \
        && echo "✓ Email sent successfully" \
        || echo "✗ Email sending failed"
fi

# Trigger Phase 2B vector reindex so new article markdown files become
# semantically searchable. Non-fatal if Bun/indexer is missing.
if command -v bun >/dev/null 2>&1 && [ -f "$AGENT_SDK_DIR/scripts/index-vault.ts" ]; then
    echo ""
    echo "🔄 Triggering Phase 2B vector reindex..."
    (cd "$AGENT_SDK_DIR" && bun run scripts/index-vault.ts) || echo "⚠️  Vector reindex failed (non-fatal)"
fi
