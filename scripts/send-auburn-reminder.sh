#!/bin/bash
# Sunday Morning Auburn Library Reminder
# Prompts Terry to ensure Auburn Library Chrome session is active
#
# ⚠️  THIS FILE IS NOT THE ONE THAT RUNS. Kept for readability/history.
#     Live copy: ~/bin/jarvis-auburn-reminder.sh
#     launchd (com.jarvis.auburn-reminder, Sun 08:20) points there.
#
# WHY (2026-08-02): the plist used to exec this path directly and failed with
# exit 78 on every firing — a launchd agent inherits no Full Disk Access, so
# macOS TCC denies it access inside ~/Library/CloudStorage/. Routing through
# ~/bin fixes exec, but a launchd job still cannot READ Dropbox unless its TCC
# grant was inherited at bootstrap from a Full-Disk-Access context. This
# reminder needs nothing from Dropbox, so the logic moved to ~/bin outright.
#
# Edit ~/bin/jarvis-auburn-reminder.sh — then mirror the change here.

osascript <<EOF
display notification "Weekly academic research will run in 15 minutes. Please ensure Chrome is running with Auburn Library logged in." with title "JARVIS Auburn Reminder" sound name "Glass"
EOF

echo "[$(date)] Auburn Library reminder sent"
