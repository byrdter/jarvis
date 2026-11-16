#!/bin/bash
# Run on the laptop: copies the jobs to the server and (re)enables the timers.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ssh jarvis-server 'mkdir -p ~/bin/jarvis-jobs ~/.config/systemd/user ~/.config/jarvis'
scp -q "$HERE"/*.py "$HERE"/*.sh "$HERE"/*.toml jarvis-server:bin/jarvis-jobs/
scp -q "$HERE"/systemd/* jarvis-server:.config/systemd/user/
ssh jarvis-server 'test -f ~/.config/jarvis/jobs.env' || scp -q "$HERE/jobs.env.example" jarvis-server:.config/jarvis/jobs.env
ssh jarvis-server 'chmod +x ~/bin/jarvis-jobs/*.py ~/bin/jarvis-jobs/*.sh && systemctl --user daemon-reload &&
  for t in brain-sync heartbeat brief preflight chat-watchdog intake; do systemctl --user enable --now jarvis-$t.timer; done &&
  systemctl --user list-timers "jarvis-*" --no-pager'
