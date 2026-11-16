---
name: performance-tracker
description: Monthly strategy validation and performance analytics
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
      - write
      - network
    version: 2.0.0
    author: JARVIS
    tags:
      - investment
      - performance
      - analytics
      - validation
    integrates_with:
      - portfolio-monitor
    feeds_into:
      []
    consumes_from:
      - portfolio-monitor
---
# Performance Tracker Skill

**Purpose:** Calculate and track portfolio performance - returns, win/loss ratios, benchmark comparison, validate Asset Revesting strategy

**When to Use:** Monthly performance review, after significant events (exits, rebalancing), strategy validation

**Output:** Monthly performance reports showing what's working and what's not

---

## Input Requirements

### 1. Portfolio History
- Read allocation reports: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md`
- Read monitoring reports: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/`
- Trade history: entries, exits, rebalances

### 2. Current Market Data
- Current positions values
- Benchmark prices (SPY for comparison)
- Market indices for context

### 3. Time Period
- **Monthly:** Default (first weekend of month)
- **Quarterly:** Every 3 months
- **Annual:** End of year
- **Custom:** Any date range

---

## Process Steps

### Step 1: Gather Performance Data

**Portfolio Timeline:**
```bash
# Find all allocation reports
find /Volumes/ORICO/jarvis/obsidian-vault/investments/reports/ -name "portfolio-allocation-*.md"

# Extract:
- Initial capital
- Each position (entry date, price, shares)
- Exit dates and prices (from monitoring reports)
- Rebalancing actions
```

**Current Values:**
```bash
# Fetch current prices for all positions
for symbol in portfolio:
    /Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current $symbol --json
```

**Benchmark Data:**
```bash
# Fetch SPY for benchmark comparison
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current SPY --json
```

### Step 2: Calculate Returns

**Total Portfolio Return:**
```python
initial_capital = 100000  # From allocation report
current_value = sum(position.current_value for position in positions) + cash

total_return_dollars = current_value - initial_capital
total_return_pct = (total_return_dollars / initial_capital) * 100

annualized_return = (total_return_pct / days_held) * 365  # If <1 year
```

**Per-Position Returns:**
```python
for position in positions:
    if position.status == "OPEN":
        current_value = position.shares * current_price
        unrealized_gain = current_value - position.cost_basis
        unrealized_pct = (unrealized_gain / position.cost_basis) * 100

    if position.status == "CLOSED":
        realized_gain = exit_proceeds - position.cost_basis
        realized_pct = (realized_gain / position.cost_basis) * 100
        holding_period = exit_date - entry_date
```

**Benchmark Comparison:**
```python
# If started with $100K on 2026-01-26
spy_entry_price = get_spy_price(start_date)
spy_current_price = get_current_price("SPY")

spy_return_pct = ((spy_current_price - spy_entry_price) / spy_entry_price) * 100
outperformance = portfolio_return_pct - spy_return_pct
```

### Step 3: Analyze Win/Loss Metrics

**Exit Analysis:**
```python
closed_positions = [p for p in history if p.status == "CLOSED"]

winners = [p for p in closed_positions if p.realized_gain > 0]
losers = [p for p in closed_positions if p.realized_gain < 0]

win_rate = len(winners) / len(closed_positions) * 100
avg_win = sum(p.realized_pct for p in winners) / len(winners)
avg_loss = sum(p.realized_pct for p in losers) / len(losers)

profit_factor = sum(p.realized_gain for p in winners) / abs(sum(p.realized_gain for p in losers))
```

**Exit Reasons:**
```python
stop_loss_exits = [p for p in closed if p.exit_reason == "Stop Loss"]
stage_change_exits = [p for p in closed if p.exit_reason == "Stage 3/4"]
profit_taking_exits = [p for p in closed if p.exit_reason == "Profit Target"]
rotation_exits = [p for p in closed if p.exit_reason == "Rotation"]
```

### Step 4: Calculate Risk Metrics

**Maximum Drawdown:**
```python
peak_value = max(daily_values)
trough_value = min(daily_values[daily_values.index(peak_value):])
max_drawdown_pct = ((trough_value - peak_value) / peak_value) * 100
```

**Sharpe Ratio (if enough data):**
```python
if months >= 3:
    excess_return = portfolio_return_pct - risk_free_rate  # BIL yield ~5%
    sharpe = excess_return / volatility
```

**Actual Portfolio Risk:**
```python
# Maximum risk taken at any point
max_risk_pct = max(daily_portfolio_risk for day in period)
avg_risk_pct = mean(daily_portfolio_risk for day in period)
target_risk_pct = 3.0  # Asset Revesting target

risk_discipline = "Within target" if max_risk_pct < 3.0 else "Exceeded target"
```

### Step 5: Strategy Validation

**Asset Revesting Principles Check:**
```python
# 1. "Only hold what's rising"
positions_in_stage_2 = [p for p in open_positions if p.stage == 2]
compliance_pct = len(positions_in_stage_2) / len(open_positions) * 100

# 2. "Cut losses quickly"
avg_days_to_stop_exit = mean(p.holding_days for p in stop_exits)
fast_exits = avg_days_to_stop_exit < 30  # Quick exits good

# 3. "Let winners run"
avg_win_holding_period = mean(p.holding_days for p in winners)
avg_loss_holding_period = mean(p.holding_days for p in losers)
discipline = avg_win_holding_period > avg_loss_holding_period

# 4. "High cash in uncertain markets"
avg_cash_pct = mean(daily_cash_allocation for day in period)
appropriate_for_market = check_cash_vs_opportunities()
```

### Step 6: Generate Performance Report

Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/performance-YYYY-MM.md`

---

## Output Format

### Monthly Performance Report

```markdown
# Portfolio Performance Report
**Period:** YYYY-MM (Month X of Year)
**Report Date:** YYYY-MM-DD
**Days Tracked:** XX days
**Strategy:** Asset Revesting (Simplified)

---

## Executive Summary

**Portfolio Value:** $XXX,XXX
**Starting Capital:** $XXX,XXX
**Total Return:** +X.X% ($X,XXX) or -X.X% ($X,XXX)
**Benchmark (SPY):** +X.X%
**Outperformance:** +X.X% or -X.X%

**Month Highlights:**
- [Key achievement or event]
- [Significant position change]
- [Market environment impact]

**Grade:** [A+ to F based on results vs objectives]

---

## Performance Breakdown

### Total Portfolio

| Metric | Value | Comparison |
|--------|-------|------------|
| Starting Value | $XXX,XXX | - |
| Ending Value | $XXX,XXX | - |
| Gain/Loss | $X,XXX | +X.X% |
| Benchmark (SPY) | +X.X% | [Beat by X.X% / Trail by X.X%] |
| Best Day | +X.X% | [Date] |
| Worst Day | -X.X% | [Date] |
| Volatility | X.X% | [Higher/Lower than SPY] |

### Position Performance

#### Open Positions

**QQQ - Nasdaq-100** (XX% of portfolio)
- Entry: $XXX.XX on YYYY-MM-DD
- Current: $XXX.XX
- Unrealized: +X.X% ($X,XXX)
- Holding Period: XX days
- Stage: X ([Stable / Changed from X])
- Grade: [Excellent / Good / Fair / Poor]

**USO - Oil** ([Conditional / Executed])
- Status: [Waiting for trigger / Entered on YYYY-MM-DD]
- [If entered: Performance metrics]

**BIL - Cash Position** (XX% of portfolio)
- Value: $XX,XXX
- Yield: ~X.X%
- Opportunity Cost: [vs SPY return]

#### Closed Positions (This Month)

[If any positions exited]

**[SYMBOL] - [Name]**
- Entry: $XXX.XX on YYYY-MM-DD
- Exit: $XXX.XX on YYYY-MM-DD
- Holding Period: XX days
- Realized: +X.X% ($X,XXX) or -X.X% ($X,XXX)
- Exit Reason: [Stop Loss / Stage Change / Profit Target / Rotation]
- Asset Revesting Grade: [Excellent exit / Good / Poor discipline]

---

## Win/Loss Analysis

**Closed Positions:** X total
**Winners:** X (XX%)
**Losers:** X (XX%)
**Win Rate:** XX%

**Average Win:** +X.X%
**Average Loss:** -X.X%
**Largest Win:** +X.X% ([SYMBOL])
**Largest Loss:** -X.X% ([SYMBOL])
**Profit Factor:** X.XX (dollars won per dollar lost)

### Exit Reasons

| Reason | Count | Avg Return | Assessment |
|--------|-------|------------|------------|
| Stop Loss | X | -X.X% | ✅ Discipline maintained |
| Stage 3/4 | X | +X.X% or -X.X% | [Assessment] |
| Profit Target | X | +X.X% | [Assessment] |
| Rotation | X | +X.X% | [Assessment] |

**Discipline Assessment:**
- Stops followed: [XX% of time]
- Average time to exit after stop: [X days]
- Grade: [Excellent / Good / Needs Improvement]

---

## Risk Analysis

### Portfolio Risk Metrics

**Maximum Risk Taken:** X.X% of capital
**Average Risk:** X.X% of capital
**Target Risk:** 3.0% of capital
**Compliance:** ✅ Within target | ⚠️ Occasionally exceeded | ❌ Frequently exceeded

**Maximum Drawdown:** -X.X%
**Current Drawdown:** -X.X% (from peak)
**Recovery Status:** [At new high / Down X.X% from peak]

**Sharpe Ratio:** X.XX ([If enough data] or "Insufficient data")
**Sortino Ratio:** X.XX ([If enough data] or "Insufficient data")

### Allocation Drift

| Position | Target | Average | Current | Drift |
|----------|--------|---------|---------|-------|
| QQQ | 25% | XX% | XX% | [+/- X%] |
| USO | 10% | XX% | XX% | [+/- X%] |
| BIL | 65% | XX% | XX% | [+/- X%] |

**Rebalancing Needed:** [Yes / No]
**Action:** [Specific rebalancing recommendations]

---

## Strategy Validation

### Asset Revesting Principles

**1. "Only Hold What's Rising" (Stage 2)**
- Positions in Stage 2: XX%
- Positions in other stages: XX%
- Grade: [A-F]
- Notes: [How well following this principle]

**2. "Cut Losses Quickly"**
- Average time to stop exit: XX days
- Target: <30 days
- Grade: [A-F]
- Notes: [Discipline assessment]

**3. "Let Winners Run"**
- Average winning holding period: XX days
- Average losing holding period: XX days
- Ratio: X.XX (want >1.0)
- Grade: [A-F]

**4. "High Cash in Uncertain Markets"**
- Average cash allocation: XX%
- Market opportunity count: X Stage 2 candidates
- Appropriate: [Yes / No / Borderline]
- Grade: [A-F]

**Overall Strategy Adherence:** XX% (Grade: [A-F])

---

## Market Context

### Market Environment This Month

**Stage 2 ETF Count:**
- Start of month: X
- End of month: X
- Trend: [Improving / Deteriorating / Stable]

**Market Character:**
- [Bullish / Neutral / Defensive]
- Notable events: [Fed announcements, earnings, geopolitical]

**Cash Allocation Appropriateness:**
- Portfolio cash: XX%
- Opportunities available: X Stage 2 candidates
- Assessment: [Appropriate / Too high / Too low]

---

## Lessons Learned

### What Worked
1. [Specific decision that worked well]
2. [Market call or position that paid off]
3. [Discipline maintained when tested]

### What Didn't Work
1. [Mistake or missed opportunity]
2. [Position that underperformed]
3. [Area for improvement]

### Actions for Next Month
1. [Specific improvement]
2. [Strategy adjustment]
3. [Skill to develop]

---

## Benchmark Comparison

### vs SPY (S&P 500)

**JARVIS Portfolio:** +X.X%
**SPY Benchmark:** +X.X%
**Outperformance:** [+X.X% / -X.X%]

**Since Inception:**
- JARVIS: +X.X% total
- SPY Buy & Hold: +X.X% total
- Difference: [+X.X% / -X.X%]

**Risk-Adjusted:**
- JARVIS volatility: X.X%
- SPY volatility: X.X%
- JARVIS max drawdown: -X.X%
- SPY max drawdown: -X.X%

**Assessment:** [Outperforming / Underperforming / In-line]
**Quality:** [With lower risk / With higher risk / Similar risk]

---

## Forward Outlook

### Current Positions

**Recommendations:**
- **HOLD:** [Symbols] - Reasons
- **MONITOR:** [Symbols] - Concerns
- **EXIT:** [Symbols] - Stage changes or technical warnings

### Cash Deployment

**Available Cash:** $XX,XXX (XX%)
**Opportunities:** [X new Stage 2 candidates or None]
**Recommendation:** [Deploy / Hold / Increase]

### Next Month Focus

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

## Performance Chart (Text-based)

**Portfolio Value Trend:**
```
Month Start:  $XXX,XXX  |████████████████░░░░|
Month Peak:   $XXX,XXX  |███████████████████░|
Month End:    $XXX,XXX  |██████████████████░░|
```

**Monthly Returns:**
```
[Chart showing monthly returns vs SPY if enough history]
```

---

## Next Review

**Monthly:** [First weekend of next month]
**Quarterly:** [If applicable]
**Annual:** [If applicable]

*Tags: #performance #monthly-report #YYYY-MM*
```

---

## Integration with Other Skills

**Requires:**
- `portfolio-monitor` - Daily/weekly position values
- `portfolio-allocation` - Initial allocations and targets
- `etf-screener` - Market environment data

**Feeds into:**
- `portfolio-builder` - Strategy adjustments
- Decision making - What's working, what's not
- Learning - Validate Asset Revesting

---

## Metrics Glossary

**Total Return:** % gain/loss from starting capital
**Benchmark:** SPY (S&P 500) buy and hold
**Win Rate:** % of closed positions that were profitable
**Profit Factor:** Total $ won / Total $ lost
**Sharpe Ratio:** Risk-adjusted return (>1.0 good, >2.0 excellent)
**Maximum Drawdown:** Largest peak-to-trough decline
**Portfolio Risk:** Max loss if all stops hit simultaneously

---

*This skill validates strategy effectiveness and provides data-driven insights for continuous improvement.*
