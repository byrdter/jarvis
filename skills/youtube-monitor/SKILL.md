---
name: youtube-monitor
description: Monitor top AI YouTube channels and generate daily video reports
metadata:
  jarvis:
    requires:
      bins: []
      env: ["YOUTUBE_API_KEY"]
      config: []
    primaryEnv: "YOUTUBE_API_KEY"
    domain: "research"
    security_level: "low"
---

# YouTube AI Monitor

Monitor curated AI YouTube channels and generate daily reports of the latest videos.

## Purpose

Automatically track the best AI YouTube channels to stay current on:
- AI news and announcements
- Research paper breakdowns
- Tool reviews and demos
- Technical deep dives
- Industry trends

## Usage

### Daily Report Generation

```bash
# Generate report for last 24 hours
python skills/youtube-monitor/monitor_channels.py

# Custom time window (last 48 hours)
python skills/youtube-monitor/monitor_channels.py --hours 48
```

### Output

Reports are saved to: `skills/youtube-monitor/reports/daily/ai-youtube-YYYY-MM-DD.md`

Each report includes:
- Top videos by engagement
- Channel categorization (news, technical, official, etc.)
- Video statistics (views, likes, comments)
- Descriptions and links
- Summary statistics

## Channels Monitored

### Tier 1 - Daily News & Analysis
- Matthew Berman (AI news, tool reviews)
- AI Explained (deep analysis, industry trends)
- Wes Roth (emerging trends, AGI discussion)
- Two Minute Papers (research visualizations)

### Tier 2 - Technical Deep Dives
- Yannic Kilcher (paper reviews)
- David Shapiro (agentic AI, cognitive architecture)
- Sam Witteveen (LangChain, agents)

### Tier 3 - AI Engineering
- AI Engineering / Swyx (engineering practices)
- 3Blue1Brown (math foundations)

### Tier 4 - Official Labs
- Anthropic (Claude updates)
- Google DeepMind (research breakthroughs)
- OpenAI (GPT updates)

### Tier 5 - Business & Strategy
- Ethan Mollick (AI in business)
- NVIDIA (GPU tech, infrastructure)

## Configuration

Edit `config/channels.yaml` to:
- Add/remove channels
- Adjust filtering preferences
- Customize report format

## Requirements

**Python packages:**
```bash
pip install google-api-python-client pyyaml python-dotenv
```

**Environment variable:**
```bash
YOUTUBE_API_KEY=your_api_key_here
```

## Automation

### Daily Execution via Cron

```bash
# Run every day at 9 AM
0 7 * * * cd /path/to/jarvis && python skills/youtube-monitor/monitor_channels.py
```

### Integration with JARVIS Heartbeat

Add to heartbeat tasks:
```yaml
- name: youtube_monitor
  schedule: daily
  time: "07:00"
  skill: youtube-monitor
  priority: medium
```

## API Quota

**YouTube API Free Tier:**
- 10,000 quota units/day
- This skill uses ~2,000-3,000 units/day
- Well within free tier limits

## Filtering

Videos are filtered to exclude:
- Shorts (under 2 minutes)
- Live streams (over 2 hours)
- Keywords: LIVE, livestream

Videos are prioritized if they mention:
- Claude, GPT-4, Gemini
- Agents, agentic
- Breaking news, announcements

## Example Output

```markdown
# AI YouTube Daily Report

**Date:** March 11, 2026
**Period:** Last 24 hours
**Videos Found:** 15

## Tier1 Daily

### Claude 4 Released: Everything You Need to Know

**Channel:** Matthew Berman

📹 [Watch Video](link) | ⏱️ 18m 45s | 👁️ 45,2a low view count | 👍 2,341 likes | 💬 432 comments

> Breaking down the new Claude 4 features, benchmarks, and how it compares to GPT-4...

---

## 📊 Summary

- Total videos: 15
- Total views: 234,567
- Total watch time: 4h 32m
- Most active channel: AI Explained (3 videos)
```

## Notes

- Reports are cumulative (not deleted)
- Check `reports/daily/` for historical reports
- Adjust `channels.yaml` to customize channels
- Engagement score ranks videos by views, likes, comments, and recency

## Future Enhancements

- [ ] Email digest delivery
- [ ] Slack notifications
- [ ] Transcript analysis for key topics
- [ ] Auto-generate summary with Claude
- [ ] Track trending topics across channels
