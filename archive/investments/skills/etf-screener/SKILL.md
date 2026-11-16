---
name: etf-screener
description: Analyze a universe of ETFs to identify which are in favorable market stages
metadata:
  jarvis:
    requires:
      bins:
        - jarvis-price
      env:
        - ALPACA_API_KEY
      config: []
      mcp_servers:
        []
    primaryEnv: ALPACA_API_KEY
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
      - etf
      - screening
      - stage-detection
    integrates_with:
      - market-analysis
      - portfolio-builder
    feeds_into:
      - portfolio-builder
    consumes_from:
      - market-analysis
---
# ETF Screener Skill

**Purpose:** Analyze a universe of ETFs to identify which are in favorable market stages for portfolio construction

**When to Use:** When building a new portfolio from scratch or looking for rotation opportunities

**Output:** Ranked list of ETFs categorized by stage with actionable recommendations

---

## ETF Universe

### Core ETFs (9)
- **SPY** - S&P 500
- **QQQ** - Nasdaq-100 (Tech-heavy)
- **IWM** - Russell 2000 (Small-cap)
- **TLT** - 20+ Year Treasury Bonds
- **IEF** - 7-10 Year Treasury Bonds
- **GLD** - Gold
- **SLV** - Silver
- **USO** - Oil
- **BIL** - 1-3 Month T-Bills (Cash equivalent)

### Leveraged ETFs (5)
- **SSO** - 2x S&P 500 (Leveraged long)
- **UPRO** - 3x S&P 500 (Leveraged long)
- **SQQQ** - -3x Nasdaq (Inverse tech, bearish)
- **SPXS** - -3x S&P 500 (Inverse market, bearish)
- **TBT** - -2x 20+ Year Treasuries (Inverse bonds, rising rates)

**Total: 14 ETFs**

---

## Process Steps

### Step 1: Fetch Data for All ETFs

For each ETF in the universe, fetch technical indicators using the market-data CLI:

```bash
DATA=$(/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/cli-tools/jarvis-price indicators SYMBOL --json)
```

**Parse required fields:**
- symbol
- current_price
- sma_20, sma_50, sma_150, sma_200
- price_vs_sma_50_pct, price_vs_sma_150_pct, price_vs_sma_200_pct
- rsi_14
- macd, macd_signal

### Step 2: Determine Market Stage for Each ETF

Apply 4-stage framework (same logic as market-analysis skill):

**Stage 2 (Markup) - BEST for buying:**
- Price > 50 SMA > 150 SMA > 200 SMA
- All SMAs trending up
- RSI between 50-70 (strong but not overbought)
- MACD above signal line (bullish momentum)

**Stage 1 (Accumulation) - WATCH for breakout:**
- Price near 150 SMA (±5%)
- SMAs flattening or beginning to slope up
- RSI 40-60 (neutral)
- Low volatility, basing pattern

**Stage 3 (Distribution) - AVOID:**
- Price above 150 SMA but showing distribution signals
- MACD bearish divergence
- RSI > 70 (overbought)
- SMAs rolling over

**Stage 4 (Decline) - AVOID or SHORT:**
- Price < 50 SMA < 150 SMA < 200 SMA
- All SMAs trending down
- RSI < 40 (weak)
- MACD below signal line

### Step 3: Calculate Composite Score

For each ETF, calculate a composite score (0-100):

**Trend Strength (40 points):**
- Price > 200 SMA: 10 points
- Price > 150 SMA: 10 points
- Price > 50 SMA: 10 points
- 50 SMA > 150 SMA > 200 SMA: 10 points

**Momentum (30 points):**
- RSI 50-70: 15 points (scale down if outside range)
- MACD > Signal: 15 points

**Position vs SMAs (30 points):**
- % above 50 SMA: 0-10 points (scale: 0-10% above)
- % above 150 SMA: 0-10 points (scale: 0-10% above)
- % above 200 SMA: 0-10 points (scale: 0-10% above)

**Grade Scale:**
- 90-100: A (Excellent - Strong buy)
- 80-89: B (Good - Buy)
- 70-79: C (Fair - Consider)
- 60-69: D (Weak - Watch)
- Below 60: F (Poor - Avoid)

### Step 4: Categorize by Stage

Group ETFs into categories:

**Buy Candidates (Stage 2):**
- ETFs in Stage 2 with grades A or B
- Sorted by composite score (highest first)

**Watch List (Stage 1):**
- ETFs in Stage 1 accumulation
- Potential future buys if they break out

**Distribution Warning (Stage 3):**
- ETFs showing distribution signals
- Consider exiting if held

**Decline/Avoid (Stage 4):**
- ETFs in downtrends
- Do not buy

**Inverse Opportunities:**
- SQQQ, SPXS, TBT (only if their underlying is weak)
- Stage 2 in inverse = underlying in Stage 4

### Step 5: Generate Screening Report

Create a markdown report with:

1. **Executive Summary**
   - How many buyable ETFs found
   - Current market conditions
   - Overall risk posture recommendation

2. **Buy Candidates** (Stage 2)
   - Ranked list with scores
   - Entry recommendations
   - Risk considerations

3. **Watch List** (Stage 1)
   - Potential future opportunities
   - Breakout levels to monitor

4. **Avoid List** (Stage 3 & 4)
   - ETFs to stay away from
   - Why they're unfavorable

5. **Inverse Opportunities** (if applicable)
   - When to consider bearish positions
   - Risk warnings

6. **Summary Table**
   - All 14 ETFs with stage, score, grade

---

## Example Workflow

```bash
# 1. Fetch data for all ETFs (can parallelize)
for SYMBOL in SPY QQQ IWM TLT IEF GLD SLV USO BIL SSO UPRO SQQQ SPXS TBT; do
  echo "Analyzing $SYMBOL..."
  DATA=$(/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/cli-tools/jarvis-price indicators $SYMBOL --json)
  # Parse and analyze
done

# 2. Calculate stages and scores

# 3. Rank and categorize

# 4. Generate report to reports/etf-screening-YYYY-MM-DD.md

# 5. Update memory with findings
```

---

## Design Requirements

See `design-requirements.md` for:
- Scoring methodology details
- Report format specifications
- Data quality standards
- Edge case handling

---

## Integration with Other Skills

**Feeds into:**
- `portfolio-builder` - Uses buy candidates to construct portfolio
- `portfolio-monitor` - Tracks changes in stages over time

**Uses:**
- `market-data CLI` - Real-time indicators and stage detection

---

## Notes

- **Leveraged ETFs:** Use caution - higher risk/reward, daily reset
- **Inverse ETFs:** Only consider in bearish markets or for hedging
- **Cash (BIL):** Always Stage 2 (safe haven), use for defensive allocation
- **Update Frequency:** Run weekly or when market conditions change significantly

---

*This skill embodies Asset Revesting principles: only hold what's rising, rotate to strength.*
