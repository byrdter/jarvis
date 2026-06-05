# JARVIS YouTube Scrapers Reference

## Overview

JARVIS has two YouTube scraping systems running automatically:

1. **Daily AI Scraper** - 40+ AI channels (news, research, tools)
2. **Sunday Claude Code Scraper** - 5 Claude Code channels (wiki updates)

---

## 1. Daily AI Scraper (40+ Channels)

### Schedule
**Daily at 10:00 AM**

### Channels Monitored
- **Tier 1 Daily:** Matthew Berman, AI Explained, Wes Roth, Two Minute Papers, The AI Advantage
- **Tier 2 Technical:** Yannic Kilcher, David Shapiro, Sam Witteveen, Prompt Engineering, All About AI
- **Tier 3 Engineering:** AI Engineering (Swyx/Alessio), 3Blue1Brown, Sentdex
- **Tier 4 Official:** Anthropic, Google DeepMind, OpenAI, Stanford HAI
- **Tier 5 Business:** Ethan Mollick, NVIDIA
- **Tier 6+ Extended:** TheAIGRID, MattVidPro AI, AI Search, Fireship, LangChain, Cole Medin, WorldofAI, and more

**Total:** ~40 channels across 10 tiers

### Configuration
- **Channel list:** `skills/youtube-monitor/config/channels.yaml`
- **Script:** `skills/youtube-monitor/monitor_channels.py`
- **Wrapper:** `~/bin/jarvis-youtube-daily.sh`
- **LaunchD:** `~/Library/LaunchAgents/com.jarvis.youtube-aggregator.plist`

### Output
- **Reports:** `skills/youtube-monitor/reports/daily/ai-youtube-YYYY-MM-DD.md`
- **Format:** Markdown with top videos, engagement stats, summaries

### Manual Run
```bash
~/bin/jarvis-youtube-daily.sh
```

---

## 2. Sunday Claude Code Scraper (5 Channels)

### Schedule
**Every Sunday at 8:00 AM**

### Channels Monitored
1. **Cole Medin** - Local AI, open source models, practical builds
2. **nateherk** - Claude Code tutorials and tips
3. **Greg Isenberg** - AI agents and business applications
4. **simonscrapes** - Automation and scraping with AI

**Total:** 4 active channels (Chase H A I URL needs fixing)

### Configuration
- **Channel list:** Hardcoded in `skills/wiki-ingest/check-claude-code-videos.py`
- **Script:** `skills/wiki-ingest/check-claude-code-videos.py`
- **Wrapper:** `~/bin/jarvis-claude-code-sunday.sh`
- **LaunchD:** `~/Library/LaunchAgents/com.jarvis.claude-code-sunday.plist`

### Output
- **Database:** `agent-sdk/data/ai-knowledge.db`
- **Wiki transcripts:** `jarvis-private/claude-code-wiki/raw/transcripts/<channel>/`
- **State file:** `skills/wiki-ingest/claude-code-last-check.json`

### Manual Run
```bash
~/bin/jarvis-claude-code-sunday.sh

# Or run the Python script directly:
cd ~/Library/CloudStorage/Dropbox/jarvis
python skills/wiki-ingest/check-claude-code-videos.py
```

---

## Logs

### Daily AI Scraper
- **stdout/stderr:** Configured in plist (check youtube-aggregator.plist)

### Sunday Claude Code Scraper
- **stdout:** `jarvis-private/logs/claude-code-scraper/stdout.log`
- **stderr:** `jarvis-private/logs/claude-code-scraper/stderr.log`

---

## Verify Jobs Are Running

```bash
# List all JARVIS jobs
launchctl list | grep jarvis

# Check specific jobs
launchctl list | grep youtube-aggregator
launchctl list | grep claude-code-sunday
```

Expected output:
```
-   0   com.jarvis.claude-code-sunday
-   0   com.jarvis.youtube-aggregator
```

---

## Reload Jobs (After Changes)

```bash
# Reload daily AI scraper
launchctl unload ~/Library/LaunchAgents/com.jarvis.youtube-aggregator.plist
launchctl load ~/Library/LaunchAgents/com.jarvis.youtube-aggregator.plist

# Reload Sunday Claude Code scraper
launchctl unload ~/Library/LaunchAgents/com.jarvis.claude-code-sunday.plist
launchctl load ~/Library/LaunchAgents/com.jarvis.claude-code-sunday.plist
```

---

## Add New Channels

### To Daily AI Scraper
Edit: `skills/youtube-monitor/config/channels.yaml`

Add channel to appropriate tier:
```yaml
- name: "Channel Name"
  channel_id: "UCxxxxxxxxxxxxxxxxxx"
  focus: "Description of content"
```

### To Sunday Claude Code Scraper
Edit: `skills/wiki-ingest/check-claude-code-videos.py`

Add to `CHANNELS` dict:
```python
"channel-slug": {
    "name": "Channel Name",
    "url": "https://www.youtube.com/@ChannelName/videos",
    "channel_id": "UCxxxxxxxxxxxxxxxxxx"
}
```

---

## Troubleshooting

### Daily AI Scraper Not Running
```bash
# Check if job is loaded
launchctl list | grep youtube-aggregator

# Test manually
~/bin/jarvis-youtube-daily.sh

# Check Python dependencies
cd ~/Library/CloudStorage/Dropbox/jarvis
source .venv/bin/activate
python -c "import yaml, googleapiclient; print('Dependencies OK')"
```

### Sunday Claude Code Scraper Not Running
```bash
# Check if job is loaded
launchctl list | grep claude-code-sunday

# Test manually
~/bin/jarvis-claude-code-sunday.sh

# Check database
cd ~/Library/CloudStorage/Dropbox/jarvis/agent-sdk
bun run - <<'EOF'
import { Database } from 'bun:sqlite';
const db = new Database('data/ai-knowledge.db');
const count = db.query('SELECT COUNT(*) as count FROM content_sources').get();
console.log('Total videos in database:', count.count);
EOF
```

### Check Recent Reports
```bash
# Daily AI reports
ls -lt ~/Library/CloudStorage/Dropbox/jarvis/skills/youtube-monitor/reports/daily/ | head -5

# Claude Code wiki files
ls -lt ~/Library/CloudStorage/Dropbox/jarvis-private/claude-code-wiki/raw/transcripts/*/ | head -10
```

---

## Summary

✅ **Daily AI Scraper:** Monitors 40+ AI channels, generates daily reports (10 AM)
✅ **Sunday Claude Code Scraper:** Updates Claude Code wiki from 5 channels (Sunday 8 AM)
✅ **Both scheduled and running automatically**

**Last updated:** May 1, 2026
