#!/bin/bash
#
# Install cron job for YouTube Monitor
# Runs daily at 7 AM and sends email report
#

echo "Installing YouTube Monitor cron job..."

# Get the full path to python3
PYTHON_PATH=$(which python3)
JARVIS_PATH="/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis"

# Create cron job entry
CRON_ENTRY="0 9 * * * cd $JARVIS_PATH && $PYTHON_PATH skills/youtube-monitor/monitor_channels.py --hours 24 --email >> skills/youtube-monitor/reports/monitor.log 2>&1"

# Add to crontab (preserving existing entries)
(crontab -l 2>/dev/null | grep -v "youtube-monitor"; echo "# JARVIS YouTube Monitor - Daily AI video report at 9 AM"; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job installed successfully!"
    echo ""
    echo "Scheduled task:"
    echo "  - Runs daily at 9:00 AM"
    echo "  - Fetches videos from last 24 hours"
    echo "  - Sends email report"
    echo "  - Logs to: skills/youtube-monitor/reports/monitor.log"
    echo ""
    echo "Current crontab:"
    crontab -l | grep -A1 "YouTube"
else
    echo "❌ Failed to install cron job"
    exit 1
fi
