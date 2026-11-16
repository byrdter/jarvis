# Performance Tracker - Design Requirements

Quality standards and specifications for performance tracking skill.

---

## Output Format

### File Location
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/performance-YYYY-MM.md`
- Naming: Year-Month for easy chronological sorting
- Tags: `#performance #monthly-report #YYYY-MM`

### Report Frequency
- **Monthly:** First weekend of each month (primary)
- **Quarterly:** Every 3 months (Q1, Q2, Q3, Q4)
- **Annual:** End of year comprehensive review
- **Ad-hoc:** After significant events (major exits, rebalancing)

---

## Performance Calculation Standards

### Return Calculations

**Total Portfolio Return:**
```python
initial_capital = 100000  # From first allocation
current_value = sum(position_values) + cash_position

# Absolute return
total_return_dollars = current_value - initial_capital
total_return_pct = (total_return_dollars / initial_capital) * 100

# Time-weighted return (if periods vary)
daily_returns = [(day_value - prev_value) / prev_value for day in period]
cumulative_return = prod(1 + r for r in daily_returns) - 1

# Annualized return (if <1 year)
days_held = (end_date - start_date).days
annualized_return = ((1 + total_return_pct/100) ** (365/days_held)) - 1
```

**Per-Position Return:**
```python
# Open position (unrealized)
cost_basis = shares * entry_price
current_value = shares * current_price
unrealized_gain = current_value - cost_basis
unrealized_pct = (unrealized_gain / cost_basis) * 100

# Closed position (realized)
proceeds = shares * exit_price
realized_gain = proceeds - cost_basis
realized_pct = (realized_gain / cost_basis) * 100

# Holding period
holding_days = (exit_date - entry_date).days
annualized_return = ((1 + realized_pct/100) ** (365/holding_days)) - 1
```

**Benchmark Comparison:**
```python
# SPY buy and hold from same start date
spy_shares = initial_capital / spy_entry_price
spy_current_value = spy_shares * spy_current_price
spy_return = ((spy_current_value - initial_capital) / initial_capital) * 100

# Outperformance
alpha = portfolio_return - spy_return  # positive = beating benchmark
```

---

## Risk Metrics Standards

### Maximum Drawdown
```python
# Peak to trough decline
peak = max(portfolio_values[:i] for i in range(len(portfolio_values)))
trough = min(portfolio_values[peak_index:])
drawdown = (trough - peak) / peak * 100

# Current drawdown (from all-time high)
current_peak = max(all_portfolio_values)
current_value = portfolio_values[-1]
current_drawdown = (current_value - current_peak) / current_peak * 100
```

### Sharpe Ratio (if ≥3 months data)
```python
# Risk-adjusted return
risk_free_rate = 5.0  # BIL yield (annualized)
excess_return = annualized_return - risk_free_rate

# Volatility (standard deviation of returns)
volatility = std(daily_returns) * sqrt(252)  # Annualized

# Sharpe
sharpe_ratio = excess_return / volatility

# Interpretation:
# <0.5 = Poor
# 0.5-1.0 = Fair
# 1.0-2.0 = Good
# 2.0-3.0 = Very Good
# >3.0 = Excellent
```

### Sortino Ratio (downside deviation)
```python
# Only penalize downside volatility
downside_returns = [r for r in daily_returns if r < 0]
downside_deviation = std(downside_returns) * sqrt(252)

sortino_ratio = excess_return / downside_deviation
# Higher is better (focus on downside risk only)
```

### Portfolio Risk (Asset Revesting)
```python
# Maximum possible loss if all stops hit
for position in equity_positions:
    risk_per_share = entry_price - stop_loss
    position_risk = shares * risk_per_share
    position_risk_pct = position_risk / total_capital * 100

total_portfolio_risk = sum(position_risk_pct for position in positions)

# Target: <3.0%
# Warning: >3.0%
# Critical: >5.0%
```

---

## Win/Loss Analysis Standards

### Exit Classifications

**Winner:**
```python
realized_pct > 0
# Even +0.01% counts as winner
```

**Loser:**
```python
realized_pct < 0
# Any loss counts
```

**Breakeven:**
```python
abs(realized_pct) < 0.1  # Within 0.1%
# Count separately in some analyses
```

### Win Rate Calculation

```python
total_closed = len(closed_positions)
winners = len([p for p in closed_positions if p.realized_pct > 0])
losers = len([p for p in closed_positions if p.realized_pct < 0])

win_rate = winners / total_closed * 100
loss_rate = losers / total_closed * 100

# Minimum sample size for reliability
if total_closed < 5:
    NOTE: "Insufficient sample size for reliable win rate"
```

### Profit Factor

```python
total_wins = sum(p.realized_gain for p in closed_positions if p.realized_gain > 0)
total_losses = abs(sum(p.realized_gain for p in closed_positions if p.realized_gain < 0))

profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')

# Interpretation:
# <1.0 = Losing money (bad)
# 1.0-1.5 = Breaking even to slight edge
# 1.5-2.0 = Good edge
# 2.0-3.0 = Excellent edge
# >3.0 = Exceptional (verify data quality)
```

### Expectancy

```python
# Expected value per trade
avg_win = mean([p.realized_pct for p in closed_positions if p.realized_pct > 0])
avg_loss = mean([p.realized_pct for p in closed_positions if p.realized_pct < 0])
win_prob = win_rate / 100

expectancy = (win_prob * avg_win) + ((1 - win_prob) * avg_loss)

# Positive = edge
# Negative = no edge
```

---

## Strategy Validation Standards

### Asset Revesting Principle Compliance

**1. "Only Hold What's Rising" (Stage 2)**
```python
open_positions_in_stage_2 = [p for p in open_positions if p.current_stage == 2]
compliance_rate = len(open_positions_in_stage_2) / len(open_positions) * 100

# Grading:
# 100% = A+ (all positions Stage 2)
# 90-99% = A (mostly Stage 2)
# 80-89% = B (acceptable)
# 70-79% = C (concerning)
# <70% = F (poor discipline)
```

**2. "Cut Losses Quickly"**
```python
stop_loss_exits = [p for p in closed_positions if p.exit_reason == "Stop Loss"]
avg_days_to_exit = mean([p.holding_days for p in stop_loss_exits])

# Grading:
# <15 days = A+ (very quick)
# 15-30 days = A (quick)
# 31-60 days = B (acceptable)
# 61-90 days = C (slow)
# >90 days = F (not following system)
```

**3. "Let Winners Run"**
```python
winners = [p for p in closed_positions if p.realized_pct > 0]
losers = [p for p in closed_positions if p.realized_pct < 0]

avg_winner_hold = mean([p.holding_days for p in winners])
avg_loser_hold = mean([p.holding_days for p in losers])

ratio = avg_winner_hold / avg_loser_hold

# Grading:
# >3.0 = A+ (excellent discipline)
# 2.0-3.0 = A (good)
# 1.5-2.0 = B (acceptable)
# 1.0-1.5 = C (needs improvement)
# <1.0 = F (cutting winners, holding losers)
```

**4. "High Cash in Uncertain Markets"**
```python
# Cross-reference with market environment from ETF screening
avg_stage_2_count = mean([screening.stage_2_count for screening in period])
avg_cash_allocation = mean([daily_cash_pct for day in period])

if avg_stage_2_count < 3:  # Defensive market
    target_cash = 60-70%
elif avg_stage_2_count < 5:  # Neutral market
    target_cash = 50-60%
else:  # Bullish market
    target_cash = 30-40%

appropriate = abs(avg_cash_allocation - target_cash_midpoint) < 10%

# Grade: Yes/No appropriateness
```

---

## Benchmark Standards

### Primary Benchmark: SPY

```python
# Always compare to SPY buy-and-hold
# Same starting capital, same start date
# No rebalancing, no management

spy_portfolio_value = (initial_capital / spy_entry_price) * spy_current_price
spy_return = ((spy_portfolio_value - initial_capital) / initial_capital) * 100
```

### Risk-Adjusted Comparison

```python
# Only beating SPY with less/equal risk counts
if portfolio_return > spy_return:
    if portfolio_volatility <= spy_volatility:
        assessment = "Outperforming with lower risk" (EXCELLENT)
    elif portfolio_volatility <= (spy_volatility * 1.1):
        assessment = "Outperforming with similar risk" (GOOD)
    else:
        assessment = "Outperforming but with higher risk" (FAIR)
else:
    assessment = "Underperforming" (POOR - strategy not working)
```

---

## Data Quality Requirements

### Minimum Data for Metrics

**Sharpe/Sortino Ratio:**
- Minimum: 3 months (60+ trading days)
- Ideal: 6+ months
- Note if insufficient data

**Win Rate Reliability:**
- Minimum: 5 closed positions
- Reliable: 10+ closed positions
- Note sample size

**Volatility Measures:**
- Minimum: 30 trading days
- Ideal: 60+ trading days

### Missing Data Handling

```python
if insufficient_data_for_metric:
    DISPLAY: "Insufficient data (need X days/trades)"
    DO_NOT: Calculate unreliable metric
    ALTERNATIVE: Show simpler metric or "N/A"
```

---

## Report Quality Checklist

Before finalizing monthly report:
- [ ] All position returns calculated accurately
- [ ] Benchmark comparison included
- [ ] Win/loss analysis complete (if positions closed)
- [ ] Risk metrics calculated or noted as N/A
- [ ] Strategy validation section complete
- [ ] Lessons learned section thoughtful (not generic)
- [ ] Forward outlook actionable
- [ ] No calculation errors
- [ ] Appropriate caveats if limited data
- [ ] Assessment grades fair and justified

---

## Assessment Grading Scale

### Overall Portfolio Grade

**A+ (95-100%)**
- Beating SPY by >5% with lower risk
- All Asset Revesting principles followed
- Win rate >60%, profit factor >2.0
- No discipline violations

**A (90-94%)**
- Beating SPY by 2-5% with similar/lower risk
- Minor discipline lapses
- Win rate >55%, profit factor >1.75

**B (80-89%)**
- Beating SPY or slight underperformance (<2%)
- Some discipline issues
- Win rate >50%, profit factor >1.5

**C (70-79%)**
- Underperforming SPY by 2-5%
- Significant discipline issues
- Win rate <50% or profit factor <1.5

**D (60-69%)**
- Underperforming SPY by 5-10%
- Poor discipline
- Strategy not working

**F (<60%)**
- Underperforming SPY by >10%
- Major losses
- Strategy failure, need major changes

### Individual Position Grades

**Excellent:** >20% gain, followed plan, clean exit
**Good:** 10-20% gain or stopped out with discipline
**Fair:** 0-10% gain or small loss with discipline
**Poor:** Larger loss but followed stop
**Terrible:** Loss due to not following stop/plan

---

## Integration Standards

### Input Sources

**Portfolio State:**
- `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md`
- Extract initial allocations, entry prices

**Daily Values:**
- `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/daily-check-*.md`
- Extract daily portfolio values

**Exits:**
- `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/weekly-review-*.md`
- Extract exit dates, prices, reasons

**Market Context:**
- `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/etf-screening-*.md`
- Extract Stage 2 counts, market environment

### Output Usage

**For Decision Making:**
- What positions are working (keep doing)
- What positions aren't (stop doing)
- Strategy validation (is Asset Revesting working?)

**For Skill Improvement:**
- performance-tracker → portfolio-builder (adjust sizing)
- performance-tracker → portfolio-monitor (tighten stops?)
- performance-tracker → market-insights (validate with expert)

---

## Edge Cases

### First Month (No Closed Positions)
```markdown
## Win/Loss Analysis

**Status:** No positions closed this month
**Open Positions:** X (all in progress)
**Unrealized Performance:** [Show current P&L]

**Note:** Win/loss metrics will be available after first exit.
```

### Large Drawdown
```markdown
## ⚠️ Drawdown Alert

**Current Drawdown:** -X.X% from peak
**Threshold:** -10% warning, -20% critical

**Analysis:**
- Cause: [Market correction / Position-specific / Stop failures]
- Duration: X days
- Recovery plan: [Specific actions]
```

### Outperformance Too Good
```python
if outperformance > 20%:  # Suspiciously high
    WARNING: "Verify calculations - exceptional outperformance"
    CHECK: Data quality, benchmark calculation, position values
    NOTE: "If correct, analyze what worked and document"
```

---

*These requirements ensure accurate performance tracking and honest assessment of strategy effectiveness.*
