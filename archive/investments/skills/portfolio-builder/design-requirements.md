# Portfolio Builder - Design Requirements

Quality standards and specifications for portfolio construction skill.

---

## Output Format

### File Location
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-YYYY-MM-DD.md`
- Naming: Date-stamped for tracking over time
- Tags: Add `#portfolio-report #allocation` at bottom of file

### Report Structure

```markdown
# Portfolio Allocation Plan
Date: YYYY-MM-DD
Capital: $XXX,XXX
Strategy: Asset Revesting (Simplified)

---

## Executive Summary

**Total Capital:** $XXX,XXX
**Equity Allocation:** XX% ($XX,XXX)
**Cash Allocation:** XX% ($XX,XXX)
**Number of Positions:** X
**Portfolio Risk:** X.XX% of capital
**Market Environment:** [Bullish/Neutral/Defensive]

**Deployment Status:**
- Immediate: $XX,XXX (XX%)
- Conditional: $XX,XXX (XX%)
- Reserved: $XX,XXX (XX%)

---

## Portfolio Allocation

### Position 1: [SYMBOL] - [Name]

**Allocation:** $XX,XXX (XX% of portfolio)
**Status:** [BUY NOW / CONDITIONAL / WATCH]

**Entry Details:**
- Current Price: $XXX.XX
- Entry Price: $XXX.XX [or trigger level]
- Shares to Buy: XXX shares
- Total Cost: $XX,XXX

**Risk Management:**
- Stop Loss: $XXX.XX ([50 SMA / 8% rule])
- Risk per Share: $X.XX
- Position Risk: $XXX (X.XX% of portfolio)
- Risk/Reward: X.X:1

**Technical Setup:**
- Stage: X ([Markup/Accumulation])
- Score: XX/100 (Grade: [A/B/C])
- Price vs 200 SMA: +X.X%
- SMAs Aligned: [Yes/No]
- MACD: [Bullish/Bearish/Neutral]

**Rationale:**
[1-2 sentences explaining why this position, why this size]

**Monitoring:**
- Review: [Daily/Weekly]
- Exit Signal: [Below 50 SMA / Stage transition to 3]
- Target: [None / $XXX if applicable]

---

[Repeat for each equity position]

---

### Cash Position: BIL - 1-3 Month T-Bills

**Allocation:** $XX,XXX (XX% of portfolio)
**Status:** HOLD

**Purpose:**
- Capital preservation
- Defensive positioning
- Opportunistic reserve for future opportunities

**Yield:** ~X.X% (current T-bill rates)

**Deployment Triggers:**
- New Stage 2 candidates emerge (re-screen weekly)
- Existing watch list positions break out
- Market environment strengthens (more Stage 2)

---

## Risk Analysis

### Position-Level Risk

| Position | Allocation | Entry | Stop | Risk/Share | Shares | Position Risk | % of Portfolio |
|----------|-----------|-------|------|------------|--------|---------------|----------------|
| [SYM] | $XX,XXX | $XXX | $XXX | $X.XX | XXX | $XXX | X.XX% |
| Total | $XX,XXX | - | - | - | - | $XXX | X.XX% |

**Portfolio Risk:** X.XX% of total capital
**Target:** <3.0% of capital
**Status:** [Within limits / Exceeds limits]

### Sector Exposure

| Sector | Positions | Allocation | % of Equity | % of Portfolio |
|--------|-----------|-----------|-------------|----------------|
| [Sector] | X | $XX,XXX | XX% | XX% |
| Cash | 1 | $XX,XXX | N/A | XX% |

**Concentration Check:**
- No sector >50% of equity: [PASS/FAIL]
- Max position size <25%: [PASS/FAIL]
- Cash allocation within target: [PASS/FAIL]

### Correlation Risk

**ETF Correlations:**
- QQQ vs SPY: ~0.95 (Very high - both US equities)
- QQQ vs USO: ~0.20 (Low - diversification benefit)

**Current Portfolio:**
[List correlations if multiple equity positions]

**Diversification Assessment:** [Good/Moderate/Poor]

---

## Execution Plan

### Immediate Actions (Execute Today/This Week)

**Buy Orders:**

1. **[SYMBOL]**
   - Order Type: Market / Limit
   - Limit Price: $XXX.XX (if applicable)
   - Shares: XXX
   - Total: $XX,XXX
   - Stop Loss: Set at $XXX.XX (mental or hard stop)

2. **BIL (Cash position)**
   - Buy: $XX,XXX
   - Or: Keep in money market fund
   - Yield: ~X%

**Total Immediate Deployment:** $XX,XXX

---

### Conditional Orders (If/Then)

**1. [SYMBOL] Breakout Entry**

**Trigger:** IF [SYMBOL] > $XX.XX with volume

**Then:**
- Buy XXX shares
- Entry: $XX.XX
- Stop: $XX.XX
- Alert set at: $XX.XX

**2. [SYMBOL] Setup Improvement**

**Trigger:** IF MACD crosses above signal

**Then:**
- Re-evaluate for entry
- Allocate: $XX,XXX
- Alert set for: MACD cross

---

### Reserved Capital (Future Deployment)

**Amount:** $XX,XXX (XX%)

**Purpose:**
- Deploy as new Stage 2 candidates emerge
- Average up into winners (if Stage 2 continues)
- Replace positions that get stopped out

**Deployment Criteria:**
- Stage 2 with score >80 (Grade B+)
- Clear technical setup
- Not extended (>10% above 200 SMA)

---

## Monitoring & Rebalancing

### Daily Checks

**Review:**
- Open positions vs stop loss levels
- Any hits? Exit immediately
- Note: Only check at market close (avoid intraday noise)

**Action:**
- If stop hit: Sell immediately, no exceptions
- If conditional trigger hit: Execute per plan
- If nothing: Do nothing (patience)

### Weekly Reviews

**Every [Day of Week]:**

1. **Re-run etf-screener**
   - Check for new Stage 2 candidates
   - Check existing positions still Stage 2
   - Monitor watch list for breakouts

2. **Update stop losses**
   - If 50 SMA moved up, update stop
   - Never lower stops (only raise)

3. **Check portfolio allocation**
   - Still within cash target?
   - Any positions outsized (>25%)?
   - Rebalance if needed

### Monthly Rebalancing

**First [Day] of Month:**

1. **Full portfolio review**
   - Performance of each position
   - Stage classifications updated
   - Composite scores recalculated

2. **Rotation decisions**
   - Exit weak (Stage 3/4) if any
   - Add strong (new Stage 2) if cash available
   - Rebalance to targets

3. **Update allocation plan**
   - Generate new portfolio-allocation report
   - Document changes made
   - Update memory with learnings

---

## Exit Signals (CRITICAL)

### Automatic Exits (No Discretion)

**1. Stop Loss Hit**
- Position drops below 50 SMA at close
- Or 8% loss from entry (whichever tighter)
- **Action:** Sell next market open, no questions

**2. Stage Transition to Stage 3**
- MACD bearish divergence confirmed
- RSI >70 and rolling over
- Distribution signals appearing
- **Action:** Exit 50-100% of position

**3. Stage Transition to Stage 4**
- Breaks below 50 SMA decisively
- 50 SMA crosses below 150 SMA
- Clear downtrend forming
- **Action:** Exit 100% immediately

### Discretionary Exits (Optional)

**Partial Profit Taking:**
- If position up >20%, consider taking 25-50% off
- Lock in gains, let remainder run
- Asset Revesting: Let winners run, but book some profits

**Rotation to Stronger:**
- If new Stage 2 emerges with better setup
- Current position weakening (still Stage 2 but deteriorating)
- Rotate capital to stronger opportunity

---

## Position Sizing Calculator

### Formula

```
Position Size = Capital × Allocation %

Shares = Position Size / Entry Price

Risk per Share = Entry Price - Stop Loss

Position Risk = Shares × Risk per Share

Position Risk % = Position Risk / Total Capital
```

### Constraints

**Maximum position size:** 25% of capital
**Minimum position size:** 5% of capital (or skip)
**Maximum portfolio risk:** 3% of capital total

### Example Calculation

**Capital:** $100,000
**Allocation:** 25%
**Entry:** $622.78 (QQQ)
**Stop:** $614.00

```
Position Size = $100,000 × 0.25 = $25,000
Shares = $25,000 / $622.78 = 40.14 → 40 shares
Actual Cost = 40 × $622.78 = $24,911
Risk/Share = $622.78 - $614.00 = $8.78
Position Risk = 40 × $8.78 = $351.20
Position Risk % = $351.20 / $100,000 = 0.35%
```

**Result:** 40 shares, $351 at risk (0.35% of portfolio) ✓

---

## Report Quality Checklist

Before finalizing portfolio allocation, verify:

- [ ] All allocations sum to 100% of capital
- [ ] No position >25% of portfolio
- [ ] Total portfolio risk <3% of capital
- [ ] Cash allocation within target range (based on market)
- [ ] Stop losses calculated for all equity positions
- [ ] Entry prices specified (current or trigger levels)
- [ ] Execution plan clear (immediate vs conditional)
- [ ] Monitoring plan specified (daily/weekly/monthly)
- [ ] Exit signals documented for all positions
- [ ] Sector concentration acceptable (<50% any sector)
- [ ] Rationale provided for each position
- [ ] Next review date specified

---

## Integration Standards

### Input from etf-screener

Required data:
- Symbol, current price, stage, score, grade
- SMA levels (20, 50, 150, 200)
- Technical indicators (RSI, MACD)
- Recommendation (Buy/Watch/Avoid)

### Output for portfolio-monitor

Provide:
- Final position list with entry prices
- Stop loss levels for each
- Allocation percentages
- Review schedule
- Alert levels for conditionals

---

## Edge Cases

### Insufficient Buy Candidates

**If <2 Stage 2 candidates:**
- Increase cash to 60-80%
- Only take highest conviction (1 position fine)
- Wait patiently for market to provide more opportunities
- **Never force positions to "be invested"**

### All Candidates Extended

**If all Stage 2 candidates >10% above 200 SMA:**
- Note extension risk in report
- Reduce position sizes by 25-50%
- Consider waiting for pullback
- Or scale in (50% now, 50% on dip)

### Leveraged ETFs

**If including 2x or 3x ETFs:**
- Max position size: 50% of normal (12% vs 25%)
- Tighter stops (5% vs 8%)
- Note increased volatility risk
- Only in strong trends (score >85)

### Inverse ETFs

**If market bearish (mostly Stage 4):**
- Can include SQQQ, SPXS, TBT
- Treat as normal positions
- Stop above 50 SMA (inverse of normal)
- Note this is bearish positioning

---

## Performance Tracking

### Metrics to Log

For each portfolio allocation:
- Date created
- Initial allocation (% equity vs cash)
- Positions included
- Entry prices

**Track over time:**
- Portfolio value weekly
- Individual position performance
- Stops hit (how many, which ones)
- New additions / rotations made
- Cash deployed vs reserved

**Monthly Review:**
- Return vs SPY benchmark
- Win rate on exits
- Average holding period
- Sharpe ratio (if enough history)

---

*These requirements ensure consistent, high-quality portfolio construction that Terry can execute with confidence.*
