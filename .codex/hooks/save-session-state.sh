#!/bin/bash
# PreCompact Hook - Save Session State Before Context Compaction
# Preserves critical context so conversations can continue seamlessly after compaction

set -euo pipefail

# Environment variables provided by Claude Code
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Paths
SESSION_DIR="${PROJECT_DIR}/.claude/sessions"
STATE_FILE="${SESSION_DIR}/${SESSION_ID}-state.md"
CONVERSATION_FILE="${HOME}/.claude/projects/$(basename "$PROJECT_DIR")"

# Ensure sessions directory exists
mkdir -p "$SESSION_DIR"

# Log that we're saving state
echo "[ScriptSelect PreCompact] Saving session state (Session: ${SESSION_ID})" >&2

# Read recent conversation context from JSONL (last 50 messages for analysis)
RECENT_MESSAGES=""
if [ -f "${CONVERSATION_FILE}/${SESSION_ID}.jsonl" ]; then
    RECENT_MESSAGES=$(tail -50 "${CONVERSATION_FILE}/${SESSION_ID}.jsonl" 2>/dev/null || echo "")
fi

# Create state snapshot
cat > "$STATE_FILE" <<'EOF'
# Session State Snapshot - ScriptSelect

**Session ID:** ${SESSION_ID}
**Saved:** ${TIMESTAMP}
**Trigger:** PreCompact hook (approaching context limit)
**Project:** $(basename "$PROJECT_DIR")

---

## Instructions for Claude

This session was saved before context compaction to prevent context loss.

When resuming, you should:

1. **Understand where we left off** - What were we working on?
2. **Recall active goals** - What task/domain were we focused on?
3. **Remember key decisions** - What did we decide or implement?
4. **Preserve domain context** - Health/Wealth/Business/Content/etc.?
5. **Continue naturally** - Ask user: "I've resumed our session after context compaction. We were working on [INFERRED_TASK]. Should we continue?"

---

## Session Context

**Working Directory:** ${PROJECT_DIR}

**Git Status:**
$(cd "$PROJECT_DIR" && git status --short 2>/dev/null || echo "Not a git repository")

**Recent File Changes:**
$(cd "$PROJECT_DIR" && git diff --name-status HEAD~3..HEAD 2>/dev/null || echo "No recent changes")

**Current Branch:**
$(cd "$PROJECT_DIR" && git branch --show-current 2>/dev/null || echo "unknown")

**Environment Hints:**
- Active Domain: ${JARVIS_DOMAIN:-unknown}
- Active Task: ${JARVIS_TASK:-unknown}
- Session Name: ${CLAUDE_SESSION_NAME:-unnamed}

---

## Recent Conversation Context

*Last ~50 messages before compaction (for pattern analysis):*

${RECENT_MESSAGES}

EOF

# Use environment variable substitution
eval "echo \"$(cat "$STATE_FILE")\"" > "$STATE_FILE.tmp"
mv "$STATE_FILE.tmp" "$STATE_FILE"

echo "[ScriptSelect PreCompact] ✅ Session state saved to: ${STATE_FILE}" >&2
echo "[ScriptSelect PreCompact] This state will be restored on SessionStart" >&2

# Always allow compaction to proceed
exit 0
