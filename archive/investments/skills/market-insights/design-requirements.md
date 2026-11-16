# Market Insights - Design Requirements

Quality standards and specifications for automated expert analysis tracking.

---

## Output Format

### File Location
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/research/daily-insights/vermeulen-YYYY-MM-DD.md`
- Naming: Date-stamped for chronological tracking
- Tags: `#market-insights #vermeulen #expert-analysis #YYYY-MM-DD`

### Report Frequency
- **Daily (Automated):** Check for new videos every day at 6 PM
- **Ad-hoc (Manual):** Process user-provided transcript anytime
- **Historical:** Re-analyze past videos if needed

---

## Data Sources

### YouTube Channel
```bash
# Channel information
Channel: @TheTechnicalTraders
URL: https://www.youtube.com/@TheTechnicalTraders/videos
Video Frequency: Daily to every 2-3 days
Typical Post Time: Afternoon/evening after market close
```

### Portfolio State
```bash
# Current positions for cross-referencing
/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md

# Extract:
- Current positions (symbols)
- Entry prices and stop losses
- Allocation percentages
- Conditional triggers
```

### Market Context
```bash
# Latest screening for environment comparison
/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/etf-screening-*.md

# Extract:
- Stage 2 count
- Market character (bullish/neutral/defensive)
- Buy candidates
```

---

## Processing Standards

### Transcript Quality

**Minimum Acceptable:**
- Transcript length: >1000 words
- Coherent sentences (not just music lyrics)
- Market-related content detected

**Quality Checks:**
```python
def validate_transcript(text):
    # Length check
    if len(text.split()) < 1000:
        WARNING: "Short transcript - may be incomplete"

    # Market content check
    market_keywords = ["SPY", "market", "chart", "support", "resistance", "trend"]
    if not any(keyword.lower() in text.lower() for keyword in market_keywords):
        WARNING: "No market keywords detected - verify content"

    # Coherence check
    if text.count("♪") > 100:  # Music lyrics
        ERROR: "Transcript appears to be music/auto-generated"
```

### AI Analysis Standards

**Prompt Template:**
```
Analyze this Chris Vermeulen market analysis video transcript from {date}.

Chris Vermeulen is a technical analyst who specializes in:
- Weinstein Stage Analysis (Stage 1-4 market cycles)
- Multi-timeframe technical analysis
- Fibonacci levels and whole number resistance
- Inter-market relationships (stocks, bonds, gold, oil)
- Sentiment and pattern recognition (feeding frenzy, topping patterns)

Extract:
1. Overall market sentiment (bullish/neutral/bearish/mixed)
2. Specific ETF/asset mentions with his analysis
3. Technical levels mentioned (support/resistance/targets)
4. Warning signals or topping patterns
5. Opportunities he's highlighting
6. His current positioning (if mentioned)

Focus on actionable insights relevant to Asset Revesting methodology:
- Stage transitions
- Support/resistance levels
- Market environment assessment
- Risk warnings

Transcript:
{full_text}
```

**Response Quality:**
- Extract specific quotes (not paraphrase)
- Include dollar levels and percentages
- Identify timeframes (short-term vs long-term views)
- Flag contradictions or nuances
- Note confidence level (definitive vs speculative)

---

## Cross-Reference Standards

### Position Matching

**Direct Mentions:**
```python
# Portfolio positions
portfolio_symbols = ["QQQ", "USO", "BIL"]

# Extract from transcript
for symbol in portfolio_symbols:
    if symbol in transcript or symbol.lower() in transcript:
        MATCH: Direct mention found
        EXTRACT: All sentences mentioning this symbol
        ANALYZE: His sentiment on this position
```

**Indirect Mentions:**
```python
# Category matching
position_categories = {
    "QQQ": ["Nasdaq", "tech", "Magnificent 7", "QQQ", "technology"],
    "USO": ["oil", "crude", "energy", "USO", "WTI"],
    "BIL": ["cash", "T-bills", "safety", "defensive", "bonds"]
}

# Match categories to portfolio
for position, keywords in position_categories.items():
    if any(keyword in transcript.lower() for keyword in keywords):
        MATCH: Category mention found
        EXTRACT: Context and sentiment
```

### Alignment Detection

**Alignment Categories:**
```python
def determine_alignment(vermeulen_view, your_position):
    """
    ✅ Strong Alignment: Views completely agree
    ⚠️ Partial Alignment: Some differences but generally aligned
    🚨 Conflict: Major disagreement requiring review
    ℹ️ No Opinion: He didn't discuss this position
    """

    # Examples:
    # You: Long QQQ | Vermeulen: "Nasdaq looking strong, Stage 2"
    #   → ✅ Strong Alignment

    # You: Long QQQ | Vermeulen: "Tech showing distribution signs"
    #   → ⚠️ Partial Alignment (warning signs)

    # You: Long QQQ | Vermeulen: "Magnificent 7 topping, time to exit"
    #   → 🚨 Conflict (opposing view)

    # You: Long QQQ | Vermeulen: [No mention of tech/Nasdaq]
    #   → ℹ️ No Opinion
```

### Action Item Generation

**Action Priority:**
```python
IMMEDIATE = [
    "Vermeulen says exit now",
    "Stop loss recommendation below your stop",
    "Stage 4 warning on your position",
    "Major topping pattern identified"
]

MONITOR = [
    "Approaching resistance",
    "Distribution signs emerging",
    "Stage 2 → 3 transition warning",
    "Correlation changes noted"
]

CONSIDER = [
    "New opportunity mentioned",
    "Alternative allocation suggested",
    "Market environment shifting",
    "Different timeframe view"
]

CONFIRMED = [
    "Agrees with your position",
    "Validates your entry/stop",
    "Similar market read",
    "Complementary analysis"
]
```

---

## Report Quality Standards

### Daily Insight Report

**Must Include:**
- [ ] Video metadata (title, date, URL)
- [ ] Market sentiment summary (1-2 sentences)
- [ ] Key insights by asset class
- [ ] Cross-reference with YOUR positions
- [ ] Technical levels to watch (table format)
- [ ] Warning signals specific to your portfolio
- [ ] Action items categorized by priority
- [ ] Alignment score with your decisions

**Quality Markers:**
- Specific (not vague): "QQQ resistance at $640" not "tech facing headwinds"
- Actionable: "Monitor QQQ break below $614 stop" not "watch QQQ"
- Personal: "Your QQQ position" not "QQQ in general"
- Graded: "✅ Aligns" or "🚨 Conflicts" not "interesting view"

### Position Cross-Reference Section

**Format Standard:**
```markdown
### 🎯 Your Positions Mentioned

**QQQ (Your 25% position):**
**Vermeulen's View:** [Bullish / Bearish / Neutral / Mixed]
**His Analysis:**
> "[Exact quote from transcript]"

**Technical Levels Mentioned:**
- Support: $XXX (he said: "[quote]")
- Resistance: $XXX (he said: "[quote]")
- Target: $XXX or [No target given]

**Your Position:**
- Entry: $622.78
- Stop: $614.00
- Current: $XXX
- Status: [Gaining / Losing / Stable]

**Assessment:**
[✅ / ⚠️ / 🚨] [Specific alignment analysis]

**Reasoning:**
[Why aligned or conflicted - use his words and your metrics]
```

---

## Automation Standards

### Video Checking Logic

**State Management:**
```python
# last_processed.json format
{
    "video_id": "abcd1234567",
    "date": "2026-01-26T18:30:00",
    "title": "Market Analysis Video Title"
}

# Check logic
latest_video = fetch_latest_from_channel()
last_processed = load_state()

if latest_video["video_id"] != last_processed["video_id"]:
    NEW_VIDEO = True
    process_video(latest_video)
    save_state(latest_video)
else:
    NEW_VIDEO = False
    exit_gracefully()
```

**Error Handling:**
```python
# No videos found
if not latest_video:
    LOG: "No videos found on channel"
    EXIT: Gracefully, no alert

# Transcript unavailable
if not transcript:
    LOG: "Transcript not available for video {video_id}"
    SAVE: Video metadata for manual processing
    NOTIFY: "New video found but transcript unavailable"

# Network failure
if network_error:
    LOG: Error details
    RETRY: Once after 30 seconds
    if still_failing:
        NOTIFY: "Unable to check for new videos - check manually"
```

### Transcript Storage

**File Naming:**
```bash
# Format
vermeulen-YYYY-MM-DD-{video_id}.txt

# Example
vermeulen-2026-01-26-abcd1234567.txt
```

**Content Format:**
```
Title: [Video title from YouTube]
Video ID: [YouTube video ID]
Date: [Publish date or processing date]
URL: https://www.youtube.com/watch?v={video_id}

--- TRANSCRIPT ---

[Full transcript text here]
```

**Retention:**
- Keep all transcripts indefinitely
- Useful for re-analysis
- Pattern learning over time
- Historical context

---

## Integration Standards

### Input from Other Skills

**From portfolio-allocation:**
- Current positions list
- Entry prices and stops
- Target allocations
- Conditional triggers

**From etf-screener:**
- Latest Stage 2 count
- Market environment
- Your quantitative assessment

**From portfolio-monitor:**
- Current position status
- Recent alerts or concerns
- Stop distances

### Output for Other Skills

**To portfolio-builder:**
- Expert validation of allocations
- Alternative ideas to consider
- Market environment confirmation

**To portfolio-monitor:**
- Technical levels to watch
- Early warning signals
- Position-specific concerns

**To performance-tracker:**
- Expert opinion on performance
- Strategy validation
- Market context for results

---

## Validation Metrics

### Expertise Validation

**Vermeulen's Track Record:**
- Document his calls (right/wrong)
- Track his timing accuracy
- Note his typical biases
- Learn his signal patterns

**Example Tracking:**
```markdown
## Historical Validation

**2026-01-15:** Called gold "feeding frenzy at $5K"
- Outcome: [Topped at $5,100 on 2026-01-20] ✅ Accurate

**2026-01-10:** Said "Small caps spiking = warning"
- Outcome: [Market corrected 3 days later] ✅ Accurate

**2025-12-20:** Suggested "Tech topping pattern"
- Outcome: [Tech continued +10% for 2 weeks] ❌ Early

**Win Rate:** Track over time
**Best Signals:** [Pattern types he nails]
**Miss Patterns:** [What he gets wrong]
```

### Cross-Reference Quality

**Grading Standards:**
```python
# Relevance Score
HIGH = "Mentioned your exact position with specific analysis"
MEDIUM = "Discussed asset class or related instruments"
LOW = "General market commentary, no direct relevance"
NONE = "No overlap with your portfolio"

# Action Score
CRITICAL = "Immediate action required (exit/enter)"
IMPORTANT = "Monitor closely or prepare to act"
INFORMATIONAL = "Useful context, no action needed"
REDUNDANT = "You already knew this from your analysis"

# Quality Score = (Relevance * 0.6) + (Action * 0.4)
```

---

## Alert Fatigue Prevention

### Notification Rules

**Only Notify When:**
```python
# Critical conflicts
if vermeulen_says_exit and you_are_long:
    NOTIFY: True
    PRIORITY: High

# Major opportunities
if vermeulen_says_buy and you_have_cash and aligns_with_screening:
    NOTIFY: True
    PRIORITY: Medium

# Redundant validation
if vermeulen_agrees_with_your_exact_view:
    NOTIFY: False  # Just document, don't alert
    LOG: "Confirmation of existing view"

# Minor commentary
if general_market_talk and no_portfolio_relevance:
    NOTIFY: False
    LOG: "Processed but not relevant"
```

### Report Length

**Target Length:**
- Executive summary: 3-5 sentences
- Position cross-reference: 100-200 words per YOUR position
- Technical levels: Table format (scannable)
- Action items: Bulleted, 1-2 sentences each
- Total: 800-1500 words (5-10 min read)

**Avoid:**
- Summarizing everything he said (too long)
- Repeating your existing knowledge (redundant)
- Generic market commentary (not actionable)

---

## Comparison Standards

### Quantitative vs Qualitative

**Your ETF Screening (Quant):**
- Stage 2 count: X
- Scores: 0-100
- Objective criteria
- Systematic

**Vermeulen's Analysis (Qual):**
- Pattern recognition
- Sentiment assessment
- Experience-based
- Discretionary

**Integration:**
```markdown
## Market Environment Comparison

### Your Latest ETF Screening (YYYY-MM-DD)
- Stage 2 Count: X ETFs
- Market: [Bullish/Neutral/Defensive]
- Recommendation: XX% cash

### Vermeulen's Assessment
- Market character: [His description]
- Risk level: [His assessment]
- Positioning: [His strategy]

**Alignment:**
[✅ / ⚠️ / 🚨] [Analysis of agreement/disagreement]

**Synthesis:**
[How to combine both perspectives]
```

---

## Dependencies

### Required Libraries
```bash
# Python packages
pip install youtube-transcript-api
pip install requests

# Or add to requirements.txt:
youtube-transcript-api==0.6.1
requests>=2.31.0
```

### External Dependencies
- Internet connection (YouTube access)
- No API keys required
- No authentication needed

---

## Testing Standards

### Test Cases

**1. New Video Found:**
```python
# Given: New video published today
# When: Script runs
# Then:
#   - Video detected as new
#   - Transcript fetched successfully
#   - Report generated
#   - State saved
```

**2. No New Video:**
```python
# Given: No new video since last check
# When: Script runs
# Then:
#   - Gracefully exits
#   - No unnecessary processing
#   - No alerts
```

**3. Transcript Unavailable:**
```python
# Given: New video but no transcript yet
# When: Script runs
# Then:
#   - Video metadata saved
#   - User notified
#   - Can retry later
```

**4. Position Cross-Reference:**
```python
# Given: Portfolio with QQQ, USO, BIL
# When: Vermeulen mentions "Nasdaq topping"
# Then:
#   - QQQ flagged in cross-reference
#   - Specific quotes extracted
#   - Alignment assessed
#   - Action items generated
```

### Quality Checklist

Before finalizing daily insight report:
- [ ] Video metadata complete and accurate
- [ ] Transcript fetched and validated
- [ ] All YOUR positions cross-referenced
- [ ] Alignment assessments clear (✅/⚠️/🚨)
- [ ] Technical levels extracted with quotes
- [ ] Action items prioritized correctly
- [ ] No generic/vague statements
- [ ] Report length appropriate (not too long)
- [ ] Tags applied correctly

---

## Edge Cases

### First Video Ever Processed
```markdown
**Note:** This is the first video processed. Establishing baseline.
Historical validation metrics will develop over time.
```

### Multiple Videos Same Day
```python
# If Vermeulen posts 2+ videos in one day
if multiple_videos_today:
    PROCESS: All new videos separately
    COMBINE: Into single daily report with sections
    NOTE: "Multiple videos today - see sections below"
```

### Old Video Re-Analysis
```python
# User requests re-analysis of past video
if user_provides_old_video_id:
    FETCH: Transcript as normal
    PROCESS: With portfolio state from that date
    NOTE: "Historical analysis - portfolio state from {date}"
```

### No Portfolio Yet
```python
# Before first portfolio allocation
if no_portfolio_exists:
    STILL_PROCESS: Video and generate insights
    OMIT: Position cross-reference section
    NOTE: "General insights - no portfolio to cross-reference"
```

### Video is Not Market Analysis
```python
# Sometimes he posts interviews or Q&A
if not_standard_analysis:
    PROCESS: But flag as different format
    ADJUST: Report structure accordingly
    NOTE: "Format: {Interview/Q&A/Special} - adapted analysis"
```

---

## Performance Standards

### Processing Time
- Video detection: <5 seconds
- Transcript fetch: 5-15 seconds
- AI analysis: 30-60 seconds
- Report generation: 5-10 seconds
- **Total: <90 seconds**

### Accuracy Standards
- Position matching: 100% (must catch all mentions)
- Quote extraction: Exact (no paraphrasing)
- Alignment assessment: Consistent criteria
- Technical levels: Precise numbers from transcript

---

## Documentation Requirements

### Code Comments
```python
# Function docstrings required
def fetch_transcript(video_id):
    """
    Fetch transcript for YouTube video using youtube-transcript-api.

    Args:
        video_id: YouTube video ID (11 characters)

    Returns:
        str: Full transcript text with spaces joining entries
        None: If transcript unavailable or error

    Note: No API key required. Uses YouTube's auto-generated
          or manual captions when available.
    """
```

### Logging Standards
```python
# Log levels
INFO: "Checking for new videos..."
INFO: "New video found: {title}"
INFO: "Transcript fetched successfully"
WARNING: "Transcript unavailable, will retry"
ERROR: "Network error: {details}"

# Log location
/Users/terrybyrd/Dropbox/jarvis/skills/market-insights/logs/
```

---

*These requirements ensure high-quality automated expert analysis that provides genuine value by cross-referencing with your specific portfolio decisions.*
