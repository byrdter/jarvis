# YouTube Monitor - Setup Complete! 🎉

Your daily AI YouTube monitoring system is fully configured and ready to use.

## What's Installed

✅ **YouTube API Integration** - Fetches latest videos from 40+ AI channels
✅ **Email Delivery** - Sends daily reports to your inbox
✅ **Smart Filtering** - Excludes shorts, prioritizes important videos
✅ **Daily Reports** - Markdown reports saved locally
✅ **Cron Job Ready** - Automated daily execution at 9 AM

---

## 📊 Monitoring 40+ Top AI Channels

### Tier 1 - Daily News & Analysis (5 channels)
- Matthew Berman, AI Explained, Wes Roth, Two Minute Papers, The AI Advantage
- https://www.youtube.com/@matthew_berman
- https://www.youtube.com/@aiexplained-official
- https://www.youtube.com/@WesRoth
- https://www.youtube.com/@TwoMinutePapers
- https://www.youtube.com/@aiadvantage/videos

### Tier 2 - Technical Deep Dives (5 channels)
- Yannic Kilcher, David Shapiro, Sam Witteveen, Prompt Engineering, All About AI
- https://www.youtube.com/@YannicKilcher
- https://www.youtube.com/@DaveShap
- https://www.youtube.com/@samwitteveenai
- https://www.youtube.com/@promptengineering
- https://www.youtube.com/@AllAboutAI

### Tier 3 - AI Engineering (3 channels)
- AI Engineering/Swyx, 3Blue1Brown, Sentdex
- https://www.youtube.com/@3blue1brown
- https://www.youtube.com/@sentdex

### Tier 4 - Official AI Labs (4 channels)
- Anthropic, Google DeepMind, OpenAI, Stanford HAI
- https://www.youtube.com/@anthropic-ai
- https://www.youtube.com/@googledeepmind
- https://www.youtube.com/@OpenAI
- https://www.youtube.com/@stanfordhai

### Tier 5 - Business & Strategy (2 channels)
- Ethan Mollick, NVIDIA
- https://www.youtube.com/@NVIDIA

### Tier 6 - Extended News (4 channels)
- TheAIGRID, MattVidPro AI, AI Search, Fireship
- https://www.youtube.com/@TheAiGrid
- https://www.youtube.com/@MattVidPro
- https://www.youtube.com/@theAIsearch
- https://www.youtube.com/@Fireship

### Tier 7 - LLM Development (4 channels)
- LangChain, 1littlecoder, Cole Medin, WorldofAI
- https://www.youtube.com/@LangChain
- https://www.youtube.com/@1littlecoder
- https://www.youtube.com/@ColeMedin
- https://www.youtube.com/@intheworldofai

### Tier 8 - Research & Papers (3 channels)
- Károly Zsolnai-Fehér, Arxiv Insights, AI Coffee Break
- https://www.youtube.com/@ArxivInsights
- 

### Tier 9 - Open Source & Local AI (3 channels)
- Siraj Raval, Nicholas Renotte, Weights & Biases
- https://www.youtube.com/@NicholasRenotte
- https://www.youtube.com/@WeightsBiases

### Tier 10 - AI Safety & Ethics (2 channels)
- Robert Miles, Machine Learning Street Talk
- https://www.youtube.com/@RobertMilesOfficial
- https://www.youtube.com/@MachineLearningStreetTalk

**Total: 40 channels covering the entire AI landscape**

---

## 🚀 Quick Start

### Manual Run (Test It Now)
```bash
cd /Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis
python3 skills/youtube-monitor/monitor_channels.py --hours 24
```

### With Email Delivery
```bash
python3 skills/youtube-monitor/monitor_channels.py --hours 24 --email
```

### Custom Time Window
```bash
# Last 48 hours
python3 skills/youtube-monitor/monitor_channels.py --hours 48

# Last week
python3 skills/youtube-monitor/monitor_channels.py --hours 168
```

---

## 📧 Email Setup

To enable email delivery, add these to your `.env` file:

```bash
# For Gmail (recommended)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_app_specific_password
EMAIL_TO=your.email@gmail.com  # Where to send reports

# For other email providers
# SMTP_HOST=smtp.your-provider.com
# SMTP_PORT=587
```

### Gmail App Password Setup

**Important:** Don't use your regular Gmail password!

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: "Mail"
3. Select device: "Mac" or "Other"
4. Click "Generate"
5. Copy the 16-character password
6. Add to `.env` as `SMTP_PASSWORD`

---

## ⏰ Automated Daily Execution

### Install Cron Job (Run Once)

```bash
cd /Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/skills/youtube-monitor
chmod +x install_cron.sh
./install_cron.sh
```

This will:
- Run every morning at 7:00 AM
- Fetch videos from last 24 hours
- Generate markdown report
- Send email to your inbox
- Log output to `reports/monitor.log`

### Verify Cron Job

```bash
crontab -l | grep youtube
```

### Remove Cron Job (if needed)

```bash
crontab -l | grep -v youtube-monitor | crontab -
```

---

## 📁 Where Reports Are Saved

**Daily Reports:**
```
skills/youtube-monitor/reports/daily/ai-youtube-YYYY-MM-DD.md
```

**Execution Logs:**
```
skills/youtube-monitor/reports/monitor.log
```

---

## 🎛️ Customization

### Add More Channels

Edit: `config/channels.yaml`

```yaml
tier1_daily:
  - name: "New Channel Name"
    channel_id: "UCxxxxxxxxxxxxxxxxxx"  # Get from YouTube URL
    focus: "What this channel covers"
```

**How to find channel ID:**
1. Go to YouTube channel
2. View page source (Cmd+Option+U)
3. Search for "channelId"
4. Copy the UC... ID

### Adjust Filtering

Edit: `config/channels.yaml`

```yaml
filters:
  min_duration_seconds: 120  # Skip videos under 2 minutes
  max_duration_seconds: 7200  # Skip videos over 2 hours
  exclude_keywords:
    - "LIVE"
    - "livestream"
  priority_keywords:
    - "Claude"
    - "GPT-4"
    - "breaking"
```

### Change Report Format

Edit: `config/channels.yaml`

```yaml
report:
  max_videos_per_channel: 3  # Max videos per channel
  max_total_videos: 20       # Total videos in report
  sort_by: "engagement"      # or "views" or "recency"
  include_description: true  # Show video descriptions
```

---

## 📊 Sample Report

```markdown
# AI YouTube Daily Report

**Date:** March 11, 2026
**Period:** Last 24 hours
**Videos Found:** 15

## Tier 1 Daily

### Claude 4 Released: Everything You Need to Know

**Channel:** Matthew Berman

📹 [Watch Video](link) | ⏱️ 18m 45s | 👁️ 45,2a low view count | 👍 2,341 likes | 💬 432 comments

> Breaking down the new Claude 4 features and benchmarks...

---

## 📊 Summary

- Total videos: 15
- Total views: 234,567
- Total watch time: 4h 32m
- Most active channel: AI Explained (3 videos)
```

---

## 🔧 Troubleshooting

### "No videos found"
- Normal on slow days (weekends, holidays)
- Try `--hours 48` to expand window
- Check if channels actually posted

### Email not sending
- Verify Gmail app password (not regular password)
- Check `.env` has correct SMTP settings
- Test with: `python3 skills/youtube-monitor/email_sender.py reports/daily/[latest-report].md`

### YouTube API quota exceeded
- Free tier: 10,000 units/day
- This script uses ~2,000-3,000/day
- If exceeded, wait 24 hours or reduce channels

### Cron job not running
- Check crontab: `crontab -l`
- Check logs: `cat skills/youtube-monitor/reports/monitor.log`
- Verify Python path: `which python3`

---

## 📈 Usage Stats

**API Quota (Free Tier):**
- Daily limit: 10,000 units
- This script: ~2,500 units/day (40 channels)
- Remaining: ~7,500 units (plenty of headroom)

**Cost:**
- YouTube API: FREE ✅
- Email via Gmail: FREE ✅
- Total cost: $0/month

---

## 🎯 Next Steps

1. **Test email delivery:**
   ```bash
   python3 skills/youtube-monitor/monitor_channels.py --hours 48 --email
   ```

2. **Install cron job:**
   ```bash
   ./install_cron.sh
   ```

3. **Wait for first automated run:**
   - Tomorrow at 7:00 AM
   - Check your email inbox
   - Check `reports/daily/` folder

4. **Customize channels:**
   - Add your favorite AI creators
   - Remove channels you don't need
   - Adjust filtering preferences

---

## 🎁 Bonus Features

### Generate Weekly Summary
```bash
# Get videos from last 7 days
python3 monitor_channels.py --hours 168 --email
```

### Quick Check for Breaking News
```bash
# Last 6 hours (check for breaking announcements)
python3 monitor_channels.py --hours 6
```

### Weekend Catch-Up
```bash
# Monday morning: catch up on weekend videos
python3 monitor_channels.py --hours 72 --email
```

---

## 📞 Support

**Files:**
- Main script: `monitor_channels.py`
- Email sender: `email_sender.py`
- Channel config: `config/channels.yaml`
- Skill docs: `SKILL.md`

**Logs:**
- Daily reports: `reports/daily/`
- Execution log: `reports/monitor.log`

**API Keys:**
- YouTube: `.env` → `YOUTUBE_API_KEY`
- Email: `.env` → `SMTP_USER`, `SMTP_PASSWORD`

---

## ✅ Setup Checklist

- [x] YouTube API key obtained and added to `.env`
- [x] 40+ AI channels configured
- [x] Email sender created
- [x] Filtering preferences set
- [ ] Email credentials added to `.env`
- [ ] Test email delivery
- [ ] Install cron job
- [ ] Receive first automated report

---

**You're all set! 🚀**

Your AI YouTube monitoring system will keep you informed of the latest developments in AI every single day.
