#!/bin/bash
# Timer wrapper for jarvis-brain/scripts/brain-sync.sh (every 2 min).
# Success: touch a marker preflight reads. Failure: tell Terry on Telegram, at most once an hour.
set -u
STATE="$HOME/.local/state/jarvis"; mkdir -p "$STATE"
OUT=$(bash "$HOME/code/jarvis-brain/scripts/brain-sync.sh" 2>&1); RC=$?
if [ $RC -eq 0 ]; then
  touch "$STATE/brain-sync.ok"; rm -f "$STATE/brain-sync.alerted"; exit 0
fi
echo "$(date -Is) [brain-sync] rc=$RC $OUT" >> "$STATE/jobs.log"
if [ -z "$(find "$STATE/brain-sync.alerted" -mmin -60 2>/dev/null)" ]; then
  touch "$STATE/brain-sync.alerted"
  cd "$HOME/bin/jarvis-jobs" && python3 -c "from jarvis_jobs import tg_send; import sys; tg_send(sys.argv[1])" \
    "⚠️ Brain sync failed on the server (code $RC). $OUT"
fi
exit $RC
