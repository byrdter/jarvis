#!/bin/bash
# Copies the jobs into place and (re)enables the timers. Works from either machine:
# on the laptop it copies over ssh; on the server itself (a change JARVIS made from Telegram)
# it copies locally. Set JARVIS_ON_SERVER=1 to force the local path.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

if [[ "${JARVIS_ON_SERVER:-}" == 1 || "$(hostname -s)" == jarvis ]]; then
  run() { bash -c "$1"; }
else
  run() { ssh jarvis-server "$1"; }
  remote=1
fi

run 'mkdir -p ~/bin/jarvis-jobs ~/.config/systemd/user ~/.config/jarvis'
if [[ -n "${remote:-}" ]]; then
  scp -q "$HERE"/*.py "$HERE"/*.sh "$HERE"/*.toml jarvis-server:bin/jarvis-jobs/
  scp -q "$HERE"/systemd/* jarvis-server:.config/systemd/user/
  run 'test -f ~/.config/jarvis/jobs.env' || scp -q "$HERE/jobs.env.example" jarvis-server:.config/jarvis/jobs.env
else
  cp "$HERE"/*.py "$HERE"/*.sh "$HERE"/*.toml ~/bin/jarvis-jobs/
  cp "$HERE"/systemd/* ~/.config/systemd/user/
  test -f ~/.config/jarvis/jobs.env || cp "$HERE/jobs.env.example" ~/.config/jarvis/jobs.env
fi
run 'chmod +x ~/bin/jarvis-jobs/*.py ~/bin/jarvis-jobs/*.sh && systemctl --user daemon-reload &&
  for t in brain-sync heartbeat brief preflight chat-watchdog intake reflect audit brain-index; do systemctl --user enable --now jarvis-$t.timer; done &&
  systemctl --user list-timers "jarvis-*" --no-pager'
