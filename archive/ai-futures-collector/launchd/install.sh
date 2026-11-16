#!/bin/bash
# Install the daily ai-futures pipeline as a macOS launchd job.
#
# Bootstraps:
#   - ~/bin/jarvis-ai-futures-daily.sh         (TCC-readable wrapper)
#   - ~/.config/jarvis/ai-futures.env          (TCC-readable .env copy)
#   - ~/Library/LaunchAgents/com.jarvis.ai-futures-digest.plist
#   - ~/.local/share/jarvis/ai-futures/logs/   (log dir)
#
# macOS TCC blocks launchd from sourcing files inside the Dropbox CloudStorage
# mount, so the wrapper + .env must live OUTSIDE that mount.

set -eo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
AGENT_SDK_DIR="$(cd "$HERE/.." && pwd)"

mkdir -p ~/bin ~/.config/jarvis ~/.local/share/jarvis/ai-futures/logs

echo "→ Installing wrapper to ~/bin/jarvis-ai-futures-daily.sh"
cp "$HERE/jarvis-ai-futures-daily.sh" ~/bin/jarvis-ai-futures-daily.sh
chmod +x ~/bin/jarvis-ai-futures-daily.sh

echo "→ Copying .env to ~/.config/jarvis/ai-futures.env (TCC-readable)"
if [ -f "$AGENT_SDK_DIR/.env" ]; then
  cp "$AGENT_SDK_DIR/.env" ~/.config/jarvis/ai-futures.env
  chmod 600 ~/.config/jarvis/ai-futures.env
  echo "   ✓ ~/.config/jarvis/ai-futures.env updated"
else
  echo "   ⚠️  $AGENT_SDK_DIR/.env not found — wrapper will warn at runtime"
fi

echo "→ Installing launchd plist"
cp "$HERE/com.jarvis.ai-futures-digest.plist" ~/Library/LaunchAgents/

if launchctl print "gui/$(id -u)/com.jarvis.ai-futures-digest" >/dev/null 2>&1; then
  echo "→ Reloading existing job"
  launchctl bootout "gui/$(id -u)/com.jarvis.ai-futures-digest" 2>/dev/null || true
fi
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.jarvis.ai-futures-digest.plist
echo "✅ Installed. Fires daily at 09:15 local time."
echo
echo "Whenever you change agent-sdk/.env, re-run this script to refresh the home copy."
