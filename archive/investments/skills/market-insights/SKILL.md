---
name: market-insights
description: Automated Chris Vermeulen YouTube analysis and insights extraction
metadata:
  jarvis:
    requires:
      bins:
        []
      env:
        []
      config: []
      mcp_servers:
        []
    primaryEnv: ""
    domain: investment
    security_level: low
    requires_approval: false
    allowed_operations:
      - read
      - network
    version: 2.0.0
    author: JARVIS
    tags:
      - investment
      - insights
      - youtube
      - automation
    integrates_with:
      - youtube-monitor
    feeds_into:
      - market-analysis
    consumes_from:
      - youtube-monitor
---
# Market Insights Skill

**Purpose:** Automatically fetch and analyze Chris Vermeulen's YouTube videos - extract market insights, validate your portfolio decisions, identify warnings

**When to Use:** Daily automated check for new videos, or manually process a specific video transcript

**Output:** Daily insight reports cross-referenced with your current portfolio

---

## Input Requirements

### 1. Chris Vermeulen's YouTube Channel
- Channel: `@TheTechnicalTraders`
- URL: https://www.youtube.com/@TheTechnicalTraders
- Check frequency: Daily
- Video frequency: Variable (daily to every few days)

### 2. Current Portfolio State
- Read latest allocation: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md`
- Extract current positions for cross-referencing

### 3. Latest Market Screening
- Read latest screening: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/etf-screening-*.md`
- Compare expert analysis to quantitative screening

---

## Process Steps

### Daily Automated Workflow

**Step 1: Check for New Videos**
```bash
# Run the YouTube checker script
python /Users/terrybyrd/Dropbox/jarvis/skills/market-insights/check_new_videos.py

# Script does:
# 1. Fetch latest video from @TheTechnicalTraders
# 2. Check if already processed (compare to last processed date)
# 3. If new video found, return video ID and title
# 4. If no new video, exit gracefully
```

**Step 2: Fetch Transcript (if new video)**
```python
# Uses youtube-transcript-api (no API key needed)
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript(video_id)
full_text = " ".join([entry['text'] for entry in transcript])

# Save raw transcript for reference
save_to: ${JARVIS_PRIVATE}/research/transcripts/vermeulen/vermeulen-YYYY-MM-DD-[video-id].txt
```

**Step 3: AI Summarization & Analysis**
```
# Use Claude to analyze transcript
Prompt:
"Analyze this Chris Vermeulen market analysis video transcript.

Extract:
1. Overall market sentiment (bullish/neutral/bearish)
2. Specific ETF mentions and his analysis
3. Technical levels mentioned (support/resistance)
4. Warning signals or opportunities
5. His current positioning

Focus on actionable insights relevant to Asset Revesting methodology.

Transcript:
[full_text]
"
```

**Step 4: Cross-Reference with Portfolio**
```python
# Load current portfolio positions
portfolio_positions = ["QQQ", "USO", "BIL"]  # From latest allocation

# For each position mentioned in video
for symbol in mentions:
    if symbol in portfolio_positions:
        ALERT: f"Vermeulen mentioned your position: {symbol}"
        EXTRACT: His specific analysis and recommendations

# Check for conflicts
if vermeulen_sentiment_on_position != your_position_sentiment:
    WARNING: "Conflicting view - review decision"
```

**Step 5: Generate Insight Report**
```markdown
Save to: /Volumes/ORICO/jarvis/obsidian-vault/research/daily-insights/vermeulen-YYYY-MM-DD.md

Include:
- Video title and date
- Summary of key insights
- Positions mentioned (especially yours)
- Technical levels to watch
- Warnings or opportunities
- Cross-reference with your portfolio
- Action items
```

---

### Manual Workflow (Process Specific Video)

**User provides transcript:**
```
User: "Here's today's Chris Vermeulen transcript: [paste text]"

JARVIS:
1. Skip video fetching (user provided)
2. Run AI analysis on provided text
3. Cross-reference with portfolio
4. Generate insight report
5. Save to vault
```

---

## Output Format

### Daily Insight Report

```markdown
# Market Insights - Chris Vermeulen - YYYY-MM-DD

**Video:** [Title]
**Published:** YYYY-MM-DD
**Source:** https://www.youtube.com/watch?v=[video_id]
**Analysis Date:** YYYY-MM-DD HH:MM

---

## Summary

**Market Sentiment:** [Bullish / Neutral / Bearish / Mixed]
**Key Theme:** [Main topic or concern]
**Relevance to Your Portfolio:** [High / Medium / Low]

**Quick Takeaway:** [One sentence summary]

---

## Key Insights

### Overall Market Assessment

**S&P 500 / Nasdaq:**
[His analysis of major indices]

**Market Phase:**
[Topping / Bottoming / Trending / Choppy]

**Warning Signals:**
- [Signal 1]
- [Signal 2]

**Opportunities:**
- [Opportunity 1]
- [Opportunity 2]

### Asset Classes

**Precious Metals:**
[His analysis of gold, silver, platinum]

**Energy:**
[His analysis of oil, USO, energy sector]

**Bonds:**
[His analysis of TLT, IEF, rates]

**Small Caps / Other:**
[His analysis of IWM, sector rotation, etc.]

---

## Relevant to Your Portfolio

### 🎯 Your Positions Mentioned

**QQQ (Your 25% position):**
**Vermeulen's View:** [Bullish / Bearish / Neutral]
**His Analysis:**
[Specific comments about Nasdaq, Magnificent 7, tech]

**Technical Levels Mentioned:**
- Support: $XXX
- Resistance: $XXX
- Key levels: $XXX

**Your Position:**
- Entry: $XXX
- Stop: $XXX
- Status: [Aligns / Conflicts with his view]

**Assessment:**
✅ Aligns with Vermeulen's analysis
⚠️ Some concerns raised
🚨 Major conflict - review decision

---

**USO (Your conditional 10%):**
**Vermeulen's View:** [If mentioned]
**His Analysis:**
[Specific comments about oil, energy]

**Your Status:**
- Waiting for $75 breakout trigger
- Vermeulen's take: [Supports / Questions / No mention]

---

**Positions NOT in Your Portfolio (But Mentioned):**

**[SYMBOL]:**
- Vermeulen's view: [Bullish/Bearish]
- Why relevant: [Extended / Opportunity / Warning]
- Consider for: [Future allocation / Avoid]

---

## Technical Levels to Watch

| Asset | Support | Resistance | Key Level | Vermeulen's Target |
|-------|---------|------------|-----------|-------------------|
| S&P   | $XXX    | $XXX       | $XXX      | [Target or N/A]   |
| Gold  | $XXX    | $5,000     | $5,000    | $5,100-5,200      |
| QQQ   | $XXX    | $XXX       | $XXX      | [Target or N/A]   |

---

## Market Environment Comparison

### Your Latest ETF Screening (YYYY-MM-DD)
- Stage 2 Count: X ETFs
- Market: Transitional/Defensive
- Recommendation: 60-70% cash

### Vermeulen's Assessment
- Market character: [His view]
- Risk level: [His assessment]
- Positioning: [His strategy]

**Alignment:**
✅ Consistent views (both defensive/both bullish)
⚠️ Some differences
🚨 Conflicting views - investigate further

---

## Warning Signals

**From This Video:**
1. [Warning 1: e.g., Small caps spiking = correction warning]
2. [Warning 2: e.g., Magnificent 7 topping pattern]
3. [Warning 3: e.g., Precious metals feeding frenzy]

**Impact on Your Portfolio:**
- QQQ: [High / Medium / Low impact]
- USO: [High / Medium / Low impact]
- Cash allocation: [Validated / Question / Adjust]

---

## Opportunities Identified

**New Opportunities:**
1. [If he mentions breakouts or setups]
2. [Levels to watch for entries]

**Compared to Your Watch List:**
- [Alignment or differences]

---

## Vermeulen's Positioning

**His Current Positions (if mentioned):**
- Long: [Assets he's holding]
- Short: [Assets he's shorting]
- Waiting: [Setups he's watching]

**His Strategy:**
[Offensive / Defensive / Balanced]

**Compare to Yours:**
[Similar positioning / Different approaches]

---

## Quote Highlights

> "[Notable quote about market environment]"

> "[Notable quote about specific asset]"

> "[Notable technical insight]"

---

## Action Items for Your Portfolio

### 🚨 Immediate
[If any critical warnings apply to your positions]

### ⚠️ Monitor
1. [Specific level or condition to watch]
2. [Position to monitor more closely]

### 💡 Consider
1. [Opportunity to evaluate]
2. [Adjustment to think about]

### ✅ Confirmed
1. [Your decision validated by his analysis]
2. [Strategy alignment noted]

---

## Asset Revesting Validation

**Your Application:**
- Cash allocation: XX%
- Stage 2 focus: X positions
- Stop discipline: [Status]

**Vermeulen's Approach:**
- Positioning: [Similar / Different]
- Risk management: [His approach]
- Market timing: [His views]

**Alignment Score:** XX% (Grade: [A-F])

---

## Next Steps

**For Your Portfolio:**
1. [Specific action or monitoring task]
2. [Level to watch or decision to make]

**For Next Video:**
- Check again: [Tomorrow / In 2 days]
- Topics to watch for: [Specific interests]

---

## Raw Transcript

**Link:** ${JARVIS_PRIVATE}/research/transcripts/vermeulen/vermeulen-YYYY-MM-DD-[video-id].txt

[Or embedded if short enough]

---

*Tags: #market-insights #vermeulen #expert-analysis #YYYY-MM-DD*
*Source: The Technical Traders YouTube*
*Processed: YYYY-MM-DD HH:MM*
```

---

## Python Script: Check New Videos

```python
# File: /Users/terrybyrd/Dropbox/jarvis/skills/market-insights/check_new_videos.py

#!/usr/bin/env python3
"""
Check Chris Vermeulen's YouTube channel for new videos.
No API key required - uses web scraping.
"""

import re
import json
from datetime import datetime
from pathlib import Path
import requests
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_URL = "https://www.youtube.com/@TheTechnicalTraders/videos"
STATE_FILE = Path(__file__).parent / "last_processed.json"
TRANSCRIPT_DIR = Path(os.environ.get("JARVIS_PRIVATE", Path.home() / "Library/CloudStorage/Dropbox/jarvis-private")) / "research/transcripts/vermeulen"

def get_latest_video():
    """Fetch latest video from channel (no API needed)."""
    response = requests.get(CHANNEL_URL)
    html = response.text

    # Extract video ID from page HTML
    # YouTube embeds data in ytInitialData variable
    match = re.search(r'"videoId":"([^"]+)"', html)
    if match:
        video_id = match.group(1)

        # Extract title
        title_match = re.search(r'"title":{"runs":\[{"text":"([^"]+)"', html)
        title = title_match.group(1) if title_match else "Unknown Title"

        return {
            "video_id": video_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }

    return None

def get_last_processed():
    """Get last processed video ID."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"video_id": None, "date": None}

def save_last_processed(video_info):
    """Save processed video ID and date."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({
            "video_id": video_info["video_id"],
            "date": datetime.now().isoformat(),
            "title": video_info["title"]
        }, f, indent=2)

def fetch_transcript(video_id):
    """Fetch transcript for video (no API needed)."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def save_transcript(video_id, title, text):
    """Save transcript to file."""
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"vermeulen-{date_str}-{video_id}.txt"
    filepath = TRANSCRIPT_DIR / filename

    with open(filepath, 'w') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Date: {date_str}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write("\n--- TRANSCRIPT ---\n\n")
        f.write(text)

    return filepath

def main():
    """Main execution."""
    # Get latest video
    latest = get_latest_video()
    if not latest:
        print("No videos found")
        return

    # Check if already processed
    last_processed = get_last_processed()
    if latest["video_id"] == last_processed.get("video_id"):
        print(f"No new video (latest: {latest['title']})")
        return

    # New video found!
    print(f"New video found: {latest['title']}")
    print(f"URL: {latest['url']}")

    # Fetch transcript
    print("Fetching transcript...")
    transcript = fetch_transcript(latest["video_id"])

    if not transcript:
        print("Could not fetch transcript")
        return

    # Save transcript
    filepath = save_transcript(latest["video_id"], latest["title"], transcript)
    print(f"Transcript saved: {filepath}")

    # Mark as processed
    save_last_processed(latest)

    # Output for JARVIS to process
    result = {
        "status": "new_video",
        "video_id": latest["video_id"],
        "title": latest["title"],
        "url": latest["url"],
        "transcript_file": str(filepath),
        "transcript_preview": transcript[:500] + "..."
    }

    print("\n=== NEW VIDEO READY FOR PROCESSING ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

---

## Integration with Other Skills

**Runs After:**
- Daily (automated check for new videos)
- Can run independently

**Feeds Into:**
- `portfolio-monitor` - Validate stop levels with expert
- `portfolio-builder` - Expert insight for allocation decisions
- `etf-screener` - Validate quantitative with qualitative
- Decision making - Expert second opinion

**Triggers:**
- Daily cron job or manual execution
- Can be automated via Task Scheduler (Mac)

---

## Automation Setup (Optional)

### macOS Cron Job
```bash
# Check daily at 6 PM (after market close, after Vermeulen typically posts)
crontab -e

# Add line:
0 18 * * * cd /Users/terrybyrd/Dropbox/jarvis && /usr/bin/python3 skills/market-insights/check_new_videos.py >> /tmp/market-insights.log 2>&1
```

### Manual Check
```bash
# Run anytime
cd /Users/terrybyrd/Dropbox/jarvis
python3 skills/market-insights/check_new_videos.py
```

---

## Notes

**Key Principles:**
1. **Expert validation** - Quantitative (your screening) + Qualitative (Vermeulen's analysis)
2. **Early warnings** - He often spots topping patterns before quant signals
3. **Market context** - Understand sentiment behind the numbers
4. **Not gospel** - Expert opinion to consider, not blindly follow
5. **Pattern learning** - Understand his reasoning to improve your own

**What Vermeulen Adds:**
- Pattern recognition (topping, blowoff, feeding frenzy)
- Sentiment analysis (fear, FOMO, professional distribution)
- Fibonacci levels and technical targets
- Inter-market analysis (gold vs equities, small caps vs large)
- Historical parallels (last time this happened...)

**Common Warnings to Watch For:**
- "Topping pattern" in index he's analyzing
- "Feeding frenzy" (late-stage bull, caution)
- "Small caps spiking" (historically precedes correction)
- "Distribution phase" (Stage 3 warning)
- "Fibonacci resistance" at whole numbers

**Validation Examples:**
- Your screening: GLD +33.6% extended → Vermeulen: "Gold at $5K feeding frenzy" ✅
- Your screening: QQQ Stage 2 buy → Vermeulen: "Magnificent 7 topping pattern" ⚠️
- Your screening: 65% cash defensive → Vermeulen: "Big money knows problems coming" ✅

---

*This skill bridges quantitative analysis with expert qualitative insights for better-informed decisions.*
