#!/bin/bash
# JARVIS tmux session launcher
# Creates a multi-pane tmux session for running JARVIS processes

SESSION_NAME="jarvis"
JARVIS_HOME="$HOME/Library/CloudStorage/Dropbox/jarvis"
JARVIS_PRIVATE="$HOME/Library/CloudStorage/Dropbox/jarvis-private"

# Check if session already exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? == 0 ]; then
    echo "Session '$SESSION_NAME' already exists. Attaching..."
    tmux attach-session -t $SESSION_NAME
    exit 0
fi

# Create new session with first window
echo "Creating new JARVIS tmux session..."

# Window 0: Agent SDK Server
tmux new-session -d -s $SESSION_NAME -n "agent-sdk" -c "$JARVIS_HOME/agent-sdk"
tmux send-keys -t $SESSION_NAME:0 "# Agent SDK Server (port 3000)" C-m
tmux send-keys -t $SESSION_NAME:0 "bun run src/server.ts" C-m

# Window 1: Claude Code Interactive
tmux new-window -t $SESSION_NAME:1 -n "claude" -c "$JARVIS_HOME"
tmux send-keys -t $SESSION_NAME:1 "# Claude Code Interactive Session" C-m
tmux send-keys -t $SESSION_NAME:1 "# Start with: claude --continue" C-m

# Window 2: Monitoring (split into 3 panes)
tmux new-window -t $SESSION_NAME:2 -n "monitor" -c "$JARVIS_PRIVATE"
tmux send-keys -t $SESSION_NAME:2 "# JARVIS Monitoring Dashboard" C-m

# Split horizontally (top/bottom)
tmux split-window -t $SESSION_NAME:2 -v -c "$JARVIS_PRIVATE/logs"
tmux send-keys -t $SESSION_NAME:2.1 "# Watching agent-sdk execution logs" C-m
tmux send-keys -t $SESSION_NAME:2.1 "tail -f agent-sdk/execution-*.log 2>/dev/null || echo 'No logs yet...'" C-m

# Split the top pane vertically (left/right)
tmux select-pane -t $SESSION_NAME:2.0
tmux split-window -t $SESSION_NAME:2.0 -h -c "$JARVIS_HOME/agent-sdk"
tmux send-keys -t $SESSION_NAME:2.1 "# Database queries" C-m
tmux send-keys -t $SESSION_NAME:2.1 "# sqlite3 databases/command-center.db" C-m

# Window 3: Git/Development
tmux new-window -t $SESSION_NAME:3 -n "dev" -c "$JARVIS_HOME"
tmux send-keys -t $SESSION_NAME:3 "# Development / Git / Testing" C-m
tmux send-keys -t $SESSION_NAME:3 "git status" C-m

# Window 4: Market Data (for investment domain)
tmux new-window -t $SESSION_NAME:4 -n "market" -c "$JARVIS_HOME"
tmux send-keys -t $SESSION_NAME:4 "# Market Data & Analysis" C-m
tmux send-keys -t $SESSION_NAME:4 "# Example: jarvis-price indicators SPY --json" C-m

# Set default window to Claude interactive
tmux select-window -t $SESSION_NAME:1

# Attach to session
echo "JARVIS tmux session created!"
echo ""
echo "Windows:"
echo "  0: agent-sdk  - Agent SDK server (port 3000)"
echo "  1: claude     - Claude Code interactive session"
echo "  2: monitor    - Monitoring dashboard (3 panes)"
echo "  3: dev        - Development / Git"
echo "  4: market     - Market data tools"
echo ""
echo "Navigation:"
echo "  Ctrl+b <number> - Switch to window"
echo "  Ctrl+b arrow    - Switch panes within window"
echo "  Ctrl+b d        - Detach (keeps running)"
echo "  Ctrl+b [        - Scroll mode (q to exit)"
echo ""

tmux attach-session -t $SESSION_NAME
