#!/bin/bash
# SessionStart hook: load JARVIS's brain (jarvis-brain repo) into every session.
# Layer 1 of the memory design (PLAN.md §11): SOUL + USER + MEMORY + recent daily logs,
# plus BOOTSTRAP.md while first-run onboarding is still pending.
set -u
BRAIN="${JARVIS_BRAIN:-$HOME/code/jarvis-brain}"

if [ ! -d "$BRAIN" ]; then
  echo "[load-brain] jarvis-brain not found at $BRAIN. Clone it: gh repo clone byrdter/jarvis-brain \"$BRAIN\"" >&2
  exit 0
fi

# Refresh from GitHub in the background so startup never waits on the network.
( "$BRAIN/scripts/brain-sync.sh" >/dev/null 2>&1 & )

section() { [ -f "$BRAIN/$1" ] && { echo; echo "===== $1 ====="; cat "$BRAIN/$1"; }; }

echo "=== JARVIS BRAIN (from $BRAIN): this is who you are and what you know ==="
section SOUL.md
section USER.md
section MEMORY.md
if [ -f "$BRAIN/BOOTSTRAP.md" ]; then
  echo
  echo "===== BOOTSTRAP.md (PENDING: onboarding not finished; offer to continue it) ====="
  cat "$BRAIN/BOOTSTRAP.md"
fi
# The two most recent daily logs, tail only, for "what happened lately".
for f in $(ls -1 "$BRAIN"/daily/*.md 2>/dev/null | sort | tail -2); do
  echo; echo "===== daily/$(basename "$f") (last 40 lines) ====="; tail -40 "$f"
done
echo
echo "=== Write new facts and session summaries to $BRAIN/daily/$(date +%Y-%m-%d).md (append-only). ==="
exit 0
