# Portfolio Monitor - Design Requirements

Quality standards and specifications for portfolio monitoring skill.

---

## Output Locations

### Daily Checks
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/daily-check-YYYY-MM-DD.md`
- Naming: Date-stamped for historical tracking
- Tags: `#monitoring #daily-check`

### Weekly Reviews
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/weekly-review-YYYY-MM-DD.md`
- Naming: Date of review (typically weekend)
- Tags: `#monitoring #weekly-review`

### Alerts (Critical)
- Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/alerts-YYYY-MM-DD.md`
- Only created when critical alerts exist
- Tags: `#monitoring #alert #critical`

---

## Data Sources

### Portfolio State
```bash
# Latest allocation report
/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md

# Extract from report:
- Positions (symbol, shares, entry price)
- Stop losses
- Conditional triggers
- Target allocations
```

### Market Data
```bash
# CLI tool for current prices
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current SYMBOL --json
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price indicators SYMBOL --json

# Fetch for each position in portfolio
```

### Historical Screening
```bash
# Latest ETF screening (for weekly review)
/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/etf-screening-*.md

# Compare to previous week's screening
```

---

## Alert Thresholds

### Stop Loss Alerts
```python
CRITICAL = current_price <= stop_loss  # Hit or below
WARNING = current_price <= (stop_loss * 1.02)  # Within 2%
SAFE = current_price > (stop_loss * 1.02)  # Above 2% buffer
```

### Stage Transition Alerts
```python
CRITICAL:
- Stage 2 → 4 (markup to decline) = EXIT IMMEDIATELY
- Stage 3 → 4 (distribution to decline) = EXIT

WARNING:
- Stage 2 → 3 (markup to distribution) = PREPARE TO EXIT
- Stage 1 → 4 (accumulation to decline) = AVOID/EXIT

OPPORTUNITY:
- Stage 1 → 2 (accumulation to markup) = POTENTIAL BUY
```

### Allocation Drift Alerts
```python
WARNING:
- Position > (target * 1.25)  # 25% oversized
- Position < (target * 0.75)  # 25% undersized
- Cash < (target * 0.90) AND opportunities exist
```

### Conditional Trigger Alerts
```python
OPPORTUNITY:
- Price >= trigger_price AND volume confirmed
- Conditional order ready to execute

APPROACHING:
- Price within 2% of trigger (get ready)
```

---

## Report Quality Standards

### Daily Check Report

**Must Include:**
- [ ] Date and time of check
- [ ] Overall portfolio status (emoji indicator)
- [ ] Each position with current price
- [ ] Distance to stop loss (% and $)
- [ ] Current gain/loss per position
- [ ] Conditional trigger status
- [ ] Summary of alerts (if any)
- [ ] Next review date

**Format:**
- Scannable (use tables, emojis, clear sections)
- Action-oriented (what to do, not just what is)
- Consistent structure (same format daily)

### Weekly Review Report

**Must Include:**
- [ ] Week number and date range
- [ ] Total portfolio value
- [ ] Each position with stage, score, performance
- [ ] Comparison to last week (stage changes)
- [ ] New screening results (buy candidates)
- [ ] Allocation drift analysis (table)
- [ ] Market environment assessment
- [ ] Recommended actions for next week

**Analysis Depth:**
- Compare to last week (not just current state)
- Identify trends (improving/deteriorating)
- Surface opportunities (new Stage 2 candidates)
- Flag warnings (stage transitions, allocation drift)

---

## Monitoring Logic

### Daily Stop Check Algorithm

```python
def check_stops(portfolio, current_prices):
    alerts = []

    for position in portfolio.equity_positions:
        current = current_prices[position.symbol]
        stop = position.stop_loss
        entry = position.entry_price

        # Calculate metrics
        distance_pct = ((current - stop) / stop) * 100
        distance_dollars = current - stop
        gain_loss_pct = ((current - entry) / entry) * 100

        # Determine status
        if current <= stop:
            alerts.append({
                'symbol': position.symbol,
                'severity': 'CRITICAL',
                'message': f'STOP LOSS HIT - EXIT {position.symbol} IMMEDIATELY',
                'current': current,
                'stop': stop,
                'action': 'Sell all shares at market open'
            })
        elif current <= (stop * 1.02):
            alerts.append({
                'symbol': position.symbol,
                'severity': 'WARNING',
                'message': f'{position.symbol} within 2% of stop',
                'distance_pct': distance_pct,
                'action': 'Monitor closely, prepare to exit'
            })

    return alerts
```

### Weekly Stage Change Detection

```python
def detect_stage_changes(current_screening, previous_screening):
    changes = []

    for symbol in portfolio.positions:
        curr = current_screening.get_etf(symbol)
        prev = previous_screening.get_etf(symbol)

        if curr.stage != prev.stage:
            severity = determine_severity(prev.stage, curr.stage)

            changes.append({
                'symbol': symbol,
                'previous_stage': prev.stage,
                'current_stage': curr.stage,
                'severity': severity,
                'action': get_action_for_transition(prev.stage, curr.stage)
            })

    return changes

def determine_severity(from_stage, to_stage):
    if from_stage == 2 and to_stage == 4:
        return 'CRITICAL'  # Markup to decline
    elif from_stage == 2 and to_stage == 3:
        return 'WARNING'  # Markup to distribution
    elif to_stage == 2:
        return 'OPPORTUNITY'  # Moving to markup
    else:
        return 'INFORMATIONAL'
```

---

## Error Handling

### Market Data Unavailable
```python
if unable_to_fetch_price:
    WARNING: "Unable to fetch current price for {symbol}"
    USE: Last known price (with timestamp)
    NOTE: "Price data stale - verify before making decisions"
```

### Portfolio State Missing
```python
if no_allocation_report_found:
    ERROR: "No portfolio allocation found"
    ACTION: "Run portfolio-builder first to create allocation"
    SKIP: Daily check (nothing to monitor)
```

### CLI Tool Failure
```python
if cli_tool_error:
    TRY: Alternative data source (if available)
    LOG: Error details
    NOTIFY: "Data quality reduced - manual verification recommended"
```

---

## Performance Calculations

### Position Performance
```python
entry_price = position.entry_price
current_price = fetch_current_price(position.symbol)
shares = position.shares

unrealized_gain_loss = (current_price - entry_price) * shares
unrealized_pct = ((current_price - entry_price) / entry_price) * 100

position_value = current_price * shares
```

### Portfolio Performance
```python
total_value = sum(position.current_value for position in positions)
total_invested = sum(position.cost_basis for position in positions)
total_cash = cash_position.value

portfolio_value = total_value + total_cash
total_return_pct = ((portfolio_value - initial_capital) / initial_capital) * 100
```

---

## Integration Standards

### Input from Other Skills

**From portfolio-allocation:**
- Position list with entries and stops
- Target allocation percentages
- Conditional trigger prices

**From etf-screener (weekly):**
- Current stages for all ETFs
- Scores and grades
- New buy candidates

### Output for Other Skills

**To performance-tracker:**
- Daily price snapshots
- Position values over time
- Exit dates and prices

**To portfolio-builder:**
- Allocation drift data
- Rebalancing recommendations
- New opportunity candidates

---

## Notification Rules

### When to Create Alert File

**Critical Alerts (Separate file):**
- Any stop loss hit
- Position moved to Stage 4
- Major allocation drift (>50% from target)

**Include in Daily/Weekly Report:**
- Warnings (approaching stops, stage 2→3)
- Opportunities (triggers, new candidates)
- Informational (normal status)

### Alert Fatigue Prevention

```python
# Don't alert on same issue repeatedly
if alert_exists_in_last_3_days(alert):
    SUPPRESS: Unless situation worsened

# Only alert on meaningful changes
if abs(new_value - old_value) < threshold:
    SKIP: No meaningful change

# Consolidate related alerts
if multiple_warnings_same_category:
    GROUP: Into single summary alert
```

---

## Data Retention

### Daily Checks
- Retain: 90 days (3 months)
- Archive: Older than 90 days
- Reason: Historical reference, pattern identification

### Weekly Reviews
- Retain: All (indefinitely)
- Index: For easy searching
- Reason: Long-term portfolio analysis

### Alerts
- Retain: All (indefinitely)
- Critical: Always accessible
- Reason: Learning from past decisions

---

## Quality Checklist

Before finalizing daily check:
- [ ] All positions checked
- [ ] Current prices fetched successfully
- [ ] Stop losses compared
- [ ] Conditional triggers evaluated
- [ ] Summary accurate
- [ ] Action items clear
- [ ] No data errors

Before finalizing weekly review:
- [ ] ETF screener re-run
- [ ] All positions compared to last week
- [ ] Stage changes identified
- [ ] New opportunities listed
- [ ] Allocation drift calculated
- [ ] Recommendations specific and actionable
- [ ] Market environment assessed

---

## Example Scenarios

### Scenario 1: Stop Loss Hit

**Input:**
- QQQ entry: $622.78
- QQQ stop: $614.00
- QQQ current: $612.50

**Expected Output:**
```markdown
## 🚨 CRITICAL ALERT

### QQQ Stop Loss Hit

**Current Price:** $612.50
**Stop Loss:** $614.00
**Hit By:** $1.50 (0.24%)

**ACTION REQUIRED:**
1. Exit entire QQQ position at market open
2. Sell all 40 shares
3. Expected proceeds: ~$24,500
4. Move proceeds to BIL (cash)
5. Update portfolio allocation

**DO NOT:**
- Wait for bounce
- Hope it recovers
- Lower stop loss
- Add to position

**Asset Revesting Rule:** "Cut losses quickly, follow the system"
```

### Scenario 2: Conditional Trigger Hit

**Input:**
- USO trigger: $75.00
- USO current: $75.25
- Volume: Confirmed strong

**Expected Output:**
```markdown
## 💡 OPPORTUNITY ALERT

### USO Breakout Triggered

**Trigger Price:** $75.00
**Current Price:** $75.25
**Breakout:** ✅ Confirmed

**ACTION REQUIRED:**
1. Execute conditional order
2. Buy 133 shares of USO
3. Entry: $75.25 (or current market)
4. Set stop loss: $72.00
5. Allocation: $10,000 (10%)
6. Update portfolio allocation

**Technical Confirmation:**
- Volume: Strong (breakout valid)
- Stage: Transitioning 1 → 2
- Setup: Fresh breakout
```

### Scenario 3: Stage Transition Warning

**Input:**
- QQQ previous: Stage 2
- QQQ current: Stage 3
- QQQ in portfolio: Yes (25% allocation)

**Expected Output:**
```markdown
## ⚠️ WARNING

### QQQ Stage Transition: Markup → Distribution

**Previous Stage:** 2 (Markup) - Uptrend, hold
**Current Stage:** 3 (Distribution) - Topping, prepare exit
**Position Size:** $25,000 (25% of portfolio)

**WHAT THIS MEANS:**
Stage 3 = Professional distribution phase
Smart money selling, public buying
Typically precedes Stage 4 (decline)

**RECOMMENDED ACTIONS:**
1. Monitor daily (not just weekly)
2. Tighten stop loss if possible
3. Consider taking partial profits (25-50%)
4. Prepare emotionally to exit
5. Do NOT add to position

**NEXT STEPS:**
- Daily: Check price vs 50 SMA
- If breaks below 50 SMA: Exit entirely
- Do not wait for stop loss to be hit
```

---

*These requirements ensure consistent, high-quality monitoring that maintains portfolio discipline.*
