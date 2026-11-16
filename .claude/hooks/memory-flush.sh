#!/bin/bash
# SessionEnd + PreCompact hook: hand the transcript to memory_flush.py, which summarizes the new part
# of the conversation into jarvis-brain/daily/ in the background. Never blocks, never fails.
[ -n "${CLAUDE_INVOKED_BY:-}" ] && exit 0
python3 "$(dirname "$0")/memory_flush.py" 2>/dev/null
exit 0
