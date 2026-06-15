#!/bin/bash
# JARVIS system launcher
# Starts all JARVIS components

JARVIS_HOME="$HOME/Library/CloudStorage/Dropbox/jarvis"
JARVIS_PRIVATE="$HOME/Library/CloudStorage/Dropbox/jarvis-private"

echo "🤖 Starting JARVIS System..."
echo ""

# Function to check if a process is running
check_process() {
    pgrep -f "$1" > /dev/null
    return $?
}

# 1. Check if Agent SDK server is running
if check_process "bun.*server.ts"; then
    echo "✅ Agent SDK server already running"
else
    echo "🚀 Starting Agent SDK server..."
    cd "$JARVIS_HOME/agent-sdk"
    bun run src/server.ts > "$JARVIS_PRIVATE/logs/agent-sdk/server-$(date +%Y%m%d-%H%M%S).log" 2>&1 &
    sleep 2
    if check_process "bun.*server.ts"; then
        echo "✅ Agent SDK server started (port 3000)"
    else
        echo "❌ Failed to start Agent SDK server"
    fi
fi

echo ""
echo "🎯 JARVIS Components:"
echo "  - Agent SDK:  http://localhost:3000"
echo "  - Heartbeat:  Running via launchd cron jobs"
echo "  - Memory:     $JARVIS_PRIVATE/context/memory/"
echo "  - Logs:       $JARVIS_PRIVATE/logs/"
echo ""

# 2. Option to launch tmux session
read -p "Launch tmux multi-window session? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    bash "$JARVIS_HOME/scripts/jarvis-tmux-session.sh"
else
    echo ""
    echo "To launch tmux session later:"
    echo "  bash $JARVIS_HOME/scripts/jarvis-tmux-session.sh"
    echo ""
    echo "To start Claude Code:"
    echo "  cd $JARVIS_HOME && claude --continue"
fi
