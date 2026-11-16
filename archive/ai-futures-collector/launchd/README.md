# AI-Futures Daily — launchd templates

Daily knowledge-pipeline runner. Independent of the (currently dead) Bun
`com.jarvis.agent-sdk` server; runs each fetcher CLI directly.

## Install

```bash
mkdir -p ~/bin ~/.local/share/jarvis/ai-futures/logs
cp launchd/jarvis-ai-futures-daily.sh ~/bin/
chmod +x ~/bin/jarvis-ai-futures-daily.sh
cp launchd/com.jarvis.ai-futures-digest.plist ~/Library/LaunchAgents/
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.jarvis.ai-futures-digest.plist
```

Wrapper LIVES OUTSIDE the Dropbox CloudStorage mount (`~/bin`) — required so
macOS TCC lets launchd execute it. The Bun fetcher scripts themselves stay
inside the Dropbox-resident agent-sdk repo (launchd is allowed to read those,
just not execute scripts there).

## Uninstall

```bash
launchctl bootout "gui/$(id -u)/com.jarvis.ai-futures-digest"
rm ~/Library/LaunchAgents/com.jarvis.ai-futures-digest.plist
rm ~/bin/jarvis-ai-futures-daily.sh
```

## Schedule

Fires at **09:15 local time** every day (15 minutes after `com.jarvis.news-aggregator`
so the two daily emails arrive side-by-side during the migration).

## Logs

`~/.local/share/jarvis/ai-futures/logs/{ai-futures-stdout.log,ai-futures-stderr.log}`
