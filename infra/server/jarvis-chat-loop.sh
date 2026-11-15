#!/bin/bash
# Runs JARVIS's Telegram chat session forever; restarts after a crash or exit.
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
cd "$HOME/code/jarvis"
while true; do
  claude --channels plugin:telegram@claude-plugins-official --permission-mode auto
  echo "[jarvis-chat] claude exited ($?); restarting in 10s" >&2
  sleep 10
done
