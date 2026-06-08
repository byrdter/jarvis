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
LOG_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/logs"
STDOUT_LOG="$LOG_DIR/news-aggregator-stdout.log"
STDERR_LOG="$LOG_DIR/news-aggregator-stderr.log"
OUTPUT="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/reports/news-digests/ai-news-digest-$DATE.md"
PYTHON="/Users/terrybyrd/.local/share/jarvis/news-aggregator/venv/bin/python3"
SCRIPT_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/skills/news-aggregator"
SCRIPT="$SCRIPT_DIR/aggregate.py"
EMAIL_SCRIPT="$SCRIPT_DIR/send-email.py"
EMAIL_CONFIG="/Users/terrybyrd/.local/share/jarvis/news-aggregator/email-config.sh"
AGENT_SDK_DIR="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/agent-sdk"

mkdir -p "$LOG_DIR"
exec >>"$STDOUT_LOG" 2>>"$STDERR_LOG"

echo ""
echo "============================================================"
echo "JARVIS News Aggregator wrapper start: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Output: $OUTPUT"

# Load email configuration (defines EMAIL_TO, SMTP_*)
if [ -f "$EMAIL_CONFIG" ]; then
    source "$EMAIL_CONFIG"
else
    echo "ERROR: missing email config: $EMAIL_CONFIG" >&2
    exit 11
fi

cd "$SCRIPT_DIR"
"$PYTHON" "$SCRIPT" daily --output "$OUTPUT"

# Email digest
if [ -f "$OUTPUT" ]; then
    echo "Sending email digest..."
    if "$PYTHON" "$EMAIL_SCRIPT" "$OUTPUT"; then
        echo "✓ Email sent successfully"
    else
        echo "✗ Email sending failed" >&2
        exit 12
    fi
else
    echo "ERROR: digest output missing: $OUTPUT" >&2
    exit 13
fi

# Trigger Phase 2B vector reindex so new article markdown files become
# semantically searchable. Non-fatal if Bun/indexer is missing.
if command -v bun >/dev/null 2>&1 && [ -f "$AGENT_SDK_DIR/scripts/index-vault.ts" ]; then
    echo ""
    echo "🔄 Triggering Phase 2B vector reindex in background..."
    (cd "$AGENT_SDK_DIR" && bun run scripts/index-vault.ts >>"$LOG_DIR/news-aggregator-reindex.log" 2>&1) &
fi

echo "JARVIS News Aggregator wrapper done: $(date '+%Y-%m-%d %H:%M:%S')"
