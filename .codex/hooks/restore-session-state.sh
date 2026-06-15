#!/bin/bash
# SessionStart Hook - Restore Session State After Context Compaction
# Loads saved state to maintain continuity across conversation boundaries

set -euo pipefail

# Environment variables
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Paths
SESSION_DIR="${PROJECT_DIR}/.claude/sessions"
STATE_FILE="${SESSION_DIR}/${SESSION_ID}-state.md"

# Check if state file exists for this session
if [ ! -f "$STATE_FILE" ]; then
    # No state to restore - this is a fresh session
    echo "[ScriptSelect SessionStart] No saved state for session ${SESSION_ID}" >&2
    exit 0
fi

echo "[ScriptSelect SessionStart] Found saved state, restoring context..." >&2

# Read the state file content
STATE_CONTENT=$(cat "$STATE_FILE")

# Output state content to stdout - Claude Code will inject this as context
echo "=== RESTORED SESSION STATE ==="
echo ""
echo "$STATE_CONTENT"
echo ""
echo "=== END RESTORED STATE ==="
echo ""
echo "The above context was automatically restored from your previous session before compaction."

# Clean up old state files (older than 7 days)
find "$SESSION_DIR" -name "*-state.md" -type f -mtime +7 -delete 2>/dev/null || true

echo "[ScriptSelect SessionStart] ✅ Session state restored successfully" >&2

# Always allow session to start
exit 0
