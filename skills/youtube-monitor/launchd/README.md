# Launchd assets

These files mirror what's installed on the production machine so a new machine
can re-create the daily scheduler from this repo.

## Files

- `jarvis-youtube-daily.sh` — daily harvest script (installed to `~/bin/`)
- `com.jarvis.youtube-aggregator.plist` — launchd plist (installed to `~/Library/LaunchAgents/`)

## Install on a new machine

```bash
# 1. Wrapper script
cp launchd/jarvis-youtube-daily.sh ~/bin/jarvis-youtube-daily.sh
chmod +x ~/bin/jarvis-youtube-daily.sh

# 2. Launchd job (fires daily at 10 AM)
cp launchd/com.jarvis.youtube-aggregator.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.jarvis.youtube-aggregator.plist

# 3. Verify
launchctl list | grep youtube-aggregator
```

## Trigger a manual run

```bash
bash ~/bin/jarvis-youtube-daily.sh
```
