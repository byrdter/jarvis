#!/bin/bash
# smart-recall.sh — UserPromptSubmit hook wrapper for JARVIS Memory Fix #1
#
# On the FIRST prompt of a session, reads the user's prompt from the hook's
# stdin JSON, runs claude-mem's `search` + `get_observations` MCP tools via
# .claude/hooks/smart-recall.mjs, and emits a query-aware "Relevant memories"
# block on stdout. Claude Code injects stdout as additional context for that
# turn.
#
# Note: despite the name, this does NOT call claude-mem's `smart_search` tool —
# that tool is a tree-sitter codebase search, not memory search. The name
# refers to "smart, query-aware recall" of the observation corpus.
#
# Augments (does not replace) claude-mem's existing chronological-context dump.
#
# Subsequent prompts in the same session are no-ops (marker-file gated) so we
# only pay the latency cost once per session.
#
# Logs every invocation to .claude/sessions/smart-recall.log for the
# upcoming memory-architecture video demo.
#
# Beads: jarvis-yz9

set -o pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
HOOKS_DIR="${PROJECT_DIR}/.claude/hooks"
SESSIONS_DIR="${PROJECT_DIR}/.claude/sessions"
LOG_FILE="${SESSIONS_DIR}/smart-recall.log"

mkdir -p "$SESSIONS_DIR"

# ---- read hook payload from stdin --------------------------------------------
# Must happen BEFORE the marker gate: the session id lives in this payload.
PAYLOAD="$(cat || true)"

# ---- session id --------------------------------------------------------------
# FIXED 2026-08-02. This previously read only $CLAUDE_SESSION_ID, which the hook
# environment does not set — so SESSION_ID fell back to the literal "unknown",
# and the very first such run wrote `unknown.smart-recall.done`. That one file
# then matched the gate for EVERY later session, and the hook exited at line 1
# without logging. It had been silently dead since 2026-05-29 (65 days).
#
# Claude Code passes session_id inside the stdin JSON, so read it from there
# first. If it still can't be determined, scope the marker to the current
# timestamp so a missing id can never permanently wedge the hook again.
SESSION_ID="$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys
try:
  d = json.load(sys.stdin)
  print(d.get("session_id") or d.get("sessionId") or "")
except Exception:
  pass' 2>/dev/null)"
[ -z "$SESSION_ID" ] && SESSION_ID="${CLAUDE_SESSION_ID:-}"
[ -z "$SESSION_ID" ] && SESSION_ID="noid-$(date +%Y%m%dT%H%M%S)-$$"

MARKER="${SESSIONS_DIR}/${SESSION_ID}.smart-recall.done"

# Gate: only run on the first prompt of this session.
if [ -f "$MARKER" ]; then
  exit 0
fi

# Extract the user's prompt text. Hook payload is JSON with a `prompt` field.
if command -v jq >/dev/null 2>&1; then
  QUERY="$(printf '%s' "$PAYLOAD" | jq -r '.prompt // .user_input // empty' 2>/dev/null)"
else
  # Fallback: pull "prompt": "..." with a permissive grep.
  QUERY="$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys
try:
  d = json.load(sys.stdin)
  print(d.get("prompt") or d.get("user_input") or "")
except Exception:
  pass' 2>/dev/null)"
fi

# Trim and skip if empty / too short.
QUERY="${QUERY#"${QUERY%%[![:space:]]*}"}"
QUERY="${QUERY%"${QUERY##*[![:space:]]}"}"
if [ -z "$QUERY" ] || [ "${#QUERY}" -lt 6 ]; then
  touch "$MARKER"
  echo "[$(date -Iseconds)] session=$SESSION_ID skipped (empty/short prompt)" >> "$LOG_FILE"
  exit 0
fi

# Mark BEFORE running so a crash doesn't trigger us repeatedly.
touch "$MARKER"

# Truncate very long prompts before passing as a query.
TRUNC_QUERY="$(printf '%s' "$QUERY" | head -c 500)"

START_TS=$(perl -MTime::HiRes=time -e 'printf "%d\n", time*1000' 2>/dev/null || date +%s)
RESULT="$(node "$HOOKS_DIR/smart-recall.mjs" "$TRUNC_QUERY" 7 2>>"$LOG_FILE")"
RC=$?
END_TS=$(perl -MTime::HiRes=time -e 'printf "%d\n", time*1000' 2>/dev/null || date +%s)
ELAPSED=$((END_TS - START_TS))

if [ $RC -ne 0 ] || [ -z "$RESULT" ]; then
  echo "[$(date -Iseconds)] session=$SESSION_ID query='${TRUNC_QUERY:0:80}' rc=$RC elapsed=${ELAPSED}ms result=empty" >> "$LOG_FILE"
  exit 0
fi

echo "[$(date -Iseconds)] session=$SESSION_ID query='${TRUNC_QUERY:0:80}' rc=$RC elapsed=${ELAPSED}ms bytes=${#RESULT}" >> "$LOG_FILE"

# ---- emit injected context ---------------------------------------------------
cat <<EOF
=== JARVIS QUERY-AWARE RECALL ===
The user's first prompt was matched against the claude-mem observation
corpus by relevance (not recency). These memories augment the chronological
context already loaded by the claude-mem SessionStart hook and are likely
useful for the current request.

Query: ${TRUNC_QUERY:0:200}
Retrieval: ${ELAPSED}ms

$RESULT
=== END QUERY-AWARE RECALL ===
EOF

exit 0
