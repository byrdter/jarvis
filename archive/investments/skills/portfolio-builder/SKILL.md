---
name: portfolio-builder
description: Construct portfolio allocation with position sizing based on screened opportunities
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
    security_level: high
    requires_approval: true
    allowed_operations:
      - read
      - write
      - network
    version: 2.0.0
    author: JARVIS
    tags:
      - investment
      - portfolio
      - allocation
      - position-sizing
    integrates_with:
      - etf-screener
      - portfolio-monitor
    feeds_into:
      - portfolio-monitor
    consumes_from:
      - etf-screener
---
# Portfolio Builder Skill

**Purpose:** Construct a specific portfolio allocation based on ETF screening results and available capital

**When to Use:** After running etf-screener to identify buy candidates, use this to determine exact dollar allocations

**Output:** Concrete portfolio allocation plan with specific dollar amounts, entry prices, and stop losses

---

## Input Requirements

### 1. Capital Available
- Total cash available for deployment
- Any existing positions to account for
- Timeline for deployment (lump sum vs phased)

### 2. ETF Screening Results
- Buy candidates (Stage 2 ETFs with grades A/B)
- Watch list (Stage 1 near breakout)
- Current prices and technical levels

### 3. Risk Parameters
- Target cash allocation (default: 40-60% based on market)
- Maximum position size (default: 25% per position)
- Stop loss method (default: 50 SMA or 8% loss)
- Maximum total positions (default: 5-7)

### 4. Market Environment
- Number of Stage 2 candidates available
- Overall market strength (bullish/neutral/defensive)
- Sector concentration considerations

---

## Asset Revesting Position Sizing Rules

### Core Principles

**1. Quality Over Quantity**
- Better to have 2-3 strong positions than 7 mediocre ones
- Only buy Stage 2 (Markup) with confidence >70%
- Stage 1 can be added IF near breakout (confirmation required)

**2. Position Size Based on Conviction**

**High Confidence Stage 2 (Score 85+, Grade A/B):**
- 15-25% of portfolio per position
- Strong technical setup, all SMAs aligned
- Clear trend, good momentum

**Medium Confidence Stage 2 (Score 70-84, Grade C):**
- 10-15% of portfolio per position
- Some mixed signals but still Stage 2
- Lower conviction, smaller size

**Stage 1 Breakout Candidates:**
- 5-10% of portfolio
- Only if technical breakout confirmed
- Tighter stops (higher risk)

**Cash (BIL or money market):**
- 40-60% in transitional markets (few Stage 2)
- 20-40% in strong bull markets (many Stage 2)
- 60-80% in weak markets (mostly Stage 3/4)

**3. Risk Management Per Position**

**Stop Loss Rules:**
- Primary: 50 SMA (dynamic, trails price)
- Alternative: 8% maximum loss from entry
- Use whichever is tighter
- MUST be followed, no exceptions

**Position Limits:**
- No single position >25% of portfolio
- Max 3 positions in same sector
- Avoid concentration risk

**Portfolio Heat:**
- Total risk across all positions <3% of capital
- Example: $100K portfolio, max risk $3K total
- If 3 positions @ 8% stop each = 24% position size max combined

---

## Process Steps

### Step 1: Assess Market Environment

Review ETF screening results:

**Count Stage 2 candidates:**
- 5+ Strong Stage 2: Bullish environment (40% cash)
- 2-4 Stage 2: Neutral environment (50% cash)
- 0-1 Stage 2: Defensive environment (60-70% cash)

**Current market (from screening):**
- Only 1 strong Stage 2 (QQQ)
- 10 in Stage 1 (accumulation)
- **Environment:** DEFENSIVE
- **Recommended cash:** 60-70%

### Step 2: Allocate to Buy Candidates

For each Stage 2 buy candidate:

**Calculate position size:**
```
Base allocation = (Total Capital × Equity Target) / Number of positions

Adjust for confidence:
- High confidence (85+): Base × 1.2
- Medium confidence (70-84): Base × 0.8
- Low confidence (<70): Skip or Base × 0.5
```

**Apply constraints:**
- Max position size: 25% of total capital
- Min position size: 5% of total capital (or don't bother)
- Round to practical increments ($5K, $10K, etc.)

**Example with $100K capital:**
- Equity target: 40% = $40K
- 2 positions planned
- Base allocation: $40K / 2 = $20K each
- QQQ (high confidence): $20K × 1.2 = $24K
- Adjust to practical: $25K

### Step 3: Determine Entry Levels

For each position:

**Immediate Entry:**
- If Stage 2 confirmed, current price acceptable
- Note: slightly extended if >5% above 200 SMA
- Consider: scale in if >10% above 200 SMA

**Conditional Entry:**
- Stage 1 near breakout: Wait for trigger
- Specify exact price level for entry
- Only execute if level hit with volume

**Example:**
- QQQ: Current $622.78 - Enter now (Stage 2 confirmed)
- USO: Current $73.94 - Enter IF breaks $75.00 (Stage 1 breakout)

### Step 4: Set Stop Losses

For each position:

**Calculate 50 SMA stop:**
- Use current 50 SMA from screening data
- This becomes the stop loss level
- Trails price as market moves up

**Calculate 8% stop:**
- Entry price × 0.92
- Fixed level, doesn't move

**Use tighter of the two:**
- Protects capital faster
- More aggressive risk management

**Example:**
- QQQ entry: $622.78
- 50 SMA: $614.00
- 8% stop: $573.00
- **Use:** $614.00 (tighter, better protection)

### Step 5: Allocate Remaining to Cash

**Calculate cash position:**
```
Cash = Total Capital - Sum(All Equity Positions)
```

**Verify cash target met:**
- Defensive market: 60-70% cash
- Neutral market: 40-60% cash
- Bullish market: 20-40% cash

**Cash vehicle:**
- BIL (1-3 month T-Bills) - Default choice
- Yields ~5% (current environment)
- Liquid, can deploy quickly

### Step 6: Calculate Risk Metrics

**Portfolio risk:**
```
For each position:
  Position Risk = Position Size × (Entry - Stop) / Entry

Total Portfolio Risk = Sum(All Position Risks)
```

**Target:** Total portfolio risk <3% of capital

**Example:**
- $25K QQQ position
- Entry $622.78, Stop $614
- Risk per share: $8.78
- Shares: $25K / $622.78 = 40 shares
- Position risk: 40 × $8.78 = $351
- Portfolio risk: $351 / $100K = 0.35%
- **Good:** Well under 3% limit

### Step 7: Generate Portfolio Allocation Plan

Create detailed allocation document with:

1. **Summary**
   - Total capital
   - Equity allocation (%)
   - Cash allocation (%)
   - Number of positions
   - Portfolio risk (%)

2. **Individual Positions**
   - Symbol, allocation amount
   - Entry price (current or trigger)
   - Stop loss level
   - Shares to buy
   - Risk per position

3. **Cash Reserve**
   - Amount in BIL
   - Percentage of portfolio
   - Purpose (defensive/opportunistic)

4. **Execution Plan**
   - What to buy now
   - What to watch (conditional)
   - Order types recommended

5. **Monitoring Plan**
   - Review frequency
   - Rebalance triggers
   - Exit signals

---

## Example Portfolio Construction

**Inputs:**
- Capital: $100,000
- Market: Defensive (1 Stage 2 candidate)
- Cash target: 60-70%
- Max positions: 3

**ETF Candidates (from screening):**
- QQQ: Stage 2, Score 86 (Grade B) - $622.78
- USO: Stage 1, Score 80 (Grade B) - $73.94 (watch >$75)
- SPY: Stage 2, Score 78 (Grade C) - $689.20 (MACD bearish, wait)

**Allocation Logic:**

**Equity target:** 30-40% ($30K-$40K)

**Position 1 - QQQ (High Confidence):**
- Allocation: $25,000 (25%)
- Entry: $622.78 (current price)
- Shares: 40 shares
- Stop: $614.00 (50 SMA)
- Risk: $351 (0.35% of portfolio)

**Position 2 - USO (Conditional):**
- Allocation: $10,000 (10%)
- Entry: $75.00 (breakout trigger)
- Shares: 133 shares
- Stop: $72.00 (below breakout)
- Risk: $400 (0.40% of portfolio)
- **Condition:** ONLY if breaks above $75 with volume

**Position 3 - SPY (Not included):**
- Reason: MACD bearish, mixed signals
- Action: WAIT for MACD to improve
- Reserve: $10K set aside if setup improves

**Cash Reserve:**
- BIL: $65,000 (65%)
- Purpose: Defensive + opportunistic
- Yield: ~5% while waiting

**Total Portfolio:**
- QQQ: $25,000 (25%) - Execute now
- USO: $10,000 (10%) - Conditional on $75 break
- Cash: $65,000 (65%) - BIL
- Reserved: $10,000 for SPY if improves

**Portfolio Risk:**
- QQQ risk: 0.35%
- USO risk: 0.40% (if executed)
- Total: 0.75% (well under 3% limit)

**Deployment:**
- Immediate: $90K (QQQ $25K + BIL $65K)
- Conditional: $10K (USO if breaks out)
- Future: $10K (SPY if setup improves or other opportunities)

---

## Special Considerations

### Leveraged ETFs

If including leveraged ETFs (SSO, UPRO, etc.):

**Reduce position size by 50%:**
- 2x leverage: Max 12% position (vs 25% normal)
- 3x leverage: Max 8% position
- Reason: Amplified volatility

**Tighter stops:**
- Use 5% stop instead of 8%
- Or 20 SMA instead of 50 SMA
- More aggressive risk management

**Current recommendation:**
- UPRO too extended (+19.7% above 200 SMA)
- SSO underperforming badly
- **Avoid leveraged currently**

### Inverse ETFs

Only include if:
- Market clearly in Stage 4 (decline)
- Bearish positioning desired
- Short-term tactical trade

**Current recommendation:**
- Market not in decline
- SQQQ, SPXS not appropriate
- **Avoid inverse currently**

### Sector Concentration

**Limit exposure:**
- Max 50% in any one sector
- Example: QQQ is tech-heavy, be aware
- Diversify when possible

**Current portfolio:**
- QQQ (tech) = 25%
- USO (energy) = 10%
- **Good:** Sector diversified

---

## Integration with Other Skills

**Requires:**
- `etf-screener` results (buy candidates identified)
- Market data (current prices, SMAs, technical levels)

**Feeds into:**
- `portfolio-monitor` (ongoing tracking)
- Trade execution (brokerage)

**Updates:**
- Re-run monthly or when market environment changes
- Adjust allocations as new Stage 2 candidates emerge
- Rotate from weak to strong

---

## Notes

**Key Principles:**
1. **Cash is a position** - Especially in transitional markets
2. **Quality over quantity** - Better 2 strong than 5 mediocre
3. **Risk management first** - Always know your stop before buying
4. **Be patient** - Wait for quality Stage 2 setups
5. **Follow the system** - No emotional overrides

**Common Mistakes to Avoid:**
- ❌ Forcing positions when market weak (few Stage 2)
- ❌ Oversizing positions (greed)
- ❌ Not setting stop losses (hope)
- ❌ Ignoring cash allocation targets (FOMO)
- ❌ Chasing extended positions (GLD +33%, SLV +120%)

**Asset Revesting Wisdom:**
- "Only hold what's rising"
- "Rotate to strength"
- "Cut losses quickly, let winners run"
- "Cash preserves capital for better opportunities"

---

*This skill translates screening analysis into actionable portfolio construction.*
