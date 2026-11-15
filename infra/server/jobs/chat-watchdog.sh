#!/bin/bash
# Every 2 min: if jarvis-chat is up but its Telegram poller (bun) is gone, restart the chat.
# Why: any other Claude that loads the Telegram plugin SIGTERMs the running poller, and the
# chat session keeps running deaf. Learned 2026-11-15.
set -u
STATE="$HOME/.local/state/jarvis"; mkdir -p "$STATE"
systemctl --user is-active -q jarvis-chat || exit 0
# Give a fresh start 90s to bring the poller up.
PID=$(pgrep -f "^claude --channels plugin:telegram" | head -1)
[ -n "$PID" ] && [ "$(ps -o etimes= -p "$PID" | tr -d ' ')" -lt 90 ] && exit 0
if ! pgrep -f "bun run.*plugins-official/telegram" >/dev/null; then
  echo "$(date -Is) [watchdog] telegram poller missing; restarting jarvis-chat" >> "$STATE/jobs.log"
  systemctl --user restart jarvis-chat
fi
exit 0
