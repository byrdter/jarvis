---
name: portfolio-monitor
description: Daily stop checks and weekly portfolio reviews for active positions
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
    security_level: medium
    requires_approval: false
    allowed_operations:
      - read
      - network
    version: 2.0.0
    author: JARVIS
    tags:
      - investment
      - monitoring
      - stops
      - alerts
    integrates_with:
      - portfolio-builder
      - performance-tracker
    feeds_into:
      - performance-tracker
    consumes_from:
      - portfolio-builder
---
# Portfolio Monitor Skill

**Purpose:** Monitor active portfolio positions daily/weekly - check stop losses, track performance, alert on triggers, recommend rebalancing

**When to Use:** After executing portfolio allocation, run daily for stop checks and weekly for market review

**Output:** Daily monitoring reports and alerts in Obsidian vault

---

## Input Requirements

### 1. Current Portfolio State
- Read latest allocation from: `/Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md`
- Extract: positions, entry prices, stop losses, allocation %

### 2. Current Market Data
- Use CLI tool: `/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price`
- Fetch current prices for all positions

### 3. Monitoring Frequency
- **Daily:** Stop loss checks (critical)
- **Weekly:** Full review, ETF re-screening, rebalancing check
- **Monthly:** Performance summary (links to performance-tracker skill)

---

## Process Steps

### Daily Monitoring (Quick Check)

**Step 1: Load Current Portfolio**
```bash
# Find latest allocation report
latest_allocation=$(ls -t /Volumes/ORICO/jarvis/obsidian-vault/investments/reports/portfolio-allocation-*.md | head -1)

# Extract positions, entry prices, stops from report
# Look for sections like:
# Position 1: QQQ
# Entry Price: $622.78
# Stop Loss: $614.00
```

**Step 2: Fetch Current Prices**
```bash
# For each position in portfolio
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current QQQ --json
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current USO --json
/Users/terrybyrd/Dropbox/jarvis/cli-tools/jarvis-price current BIL --json
```

**Step 3: Check Stop Losses**
For each equity position:
```python
if current_price <= stop_loss:
    ALERT: "STOP LOSS HIT - EXIT IMMEDIATELY"
    severity = "CRITICAL"

if current_price < (stop_loss * 1.02):  # Within 2% of stop
    ALERT: "APPROACHING STOP LOSS - MONITOR CLOSELY"
    severity = "WARNING"
```

**Step 4: Check Conditional Triggers**
For conditional positions (like USO > $75):
```python
if current_price >= trigger_price:
    ALERT: "BREAKOUT TRIGGER HIT - EXECUTE CONDITIONAL ORDER"
    severity = "OPPORTUNITY"
```

**Step 5: Generate Daily Report**
Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/daily-check-YYYY-MM-DD.md`

---

### Weekly Review (Full Analysis)

**Step 1: Re-run ETF Screener**
```bash
# Execute etf-screener skill to get latest market state
# Compare to last week's screening
```

**Step 2: Stage Change Detection**
```python
# For each position
if previous_stage == "Stage 2" and current_stage == "Stage 3":
    ALERT: "POSITION ENTERING DISTRIBUTION - CONSIDER EXIT"

if previous_stage == "Stage 2" and current_stage == "Stage 4":
    ALERT: "POSITION IN DECLINE - EXIT IMMEDIATELY"
```

**Step 3: New Opportunities Check**
```python
# From new screening results
new_buy_candidates = [etf for etf in screening if etf.stage == 2 and etf.score >= 80]

# Compare to current holdings
if new_buy_candidates and cash_available > 10000:
    ALERT: "NEW BUY CANDIDATES - REVIEW FOR DEPLOYMENT"
```

**Step 4: Allocation Drift Check**
```python
# Calculate current allocation % based on market values
for position in portfolio:
    current_value = shares * current_price
    current_pct = current_value / total_portfolio_value

    if current_pct > (target_pct * 1.25):  # Grown 25% beyond target
        ALERT: "POSITION OVERSIZED - CONSIDER REBALANCING"

    if current_pct < (target_pct * 0.75):  # Shrunk 25% below target
        ALERT: "POSITION UNDERSIZED - REVIEW PERFORMANCE"
```

**Step 5: Cash Deployment Check**
```python
if cash_pct < target_cash_pct and new_opportunities_exist:
    ALERT: "CASH BELOW TARGET - EVALUATE NEW POSITIONS"

if cash_pct > target_cash_pct and no_opportunities:
    STATUS: "HIGH CASH APPROPRIATE - MARKET LACKS OPPORTUNITIES"
```

**Step 6: Generate Weekly Report**
Save to: `/Volumes/ORICO/jarvis/obsidian-vault/investments/monitoring/weekly-review-YYYY-MM-DD.md`

---

## Output Format

### Daily Check Report

```markdown
# Daily Portfolio Check - YYYY-MM-DD
**Time:** HH:MM AM/PM
**Portfolio Status:** [✅ All Clear | ⚠️ Warnings | 🚨 Critical Alerts]

---

## Stop Loss Check

### QQQ - Nasdaq-100
**Current Price:** $XXX.XX
**Entry Price:** $XXX.XX
**Stop Loss:** $XXX.XX
**Distance to Stop:** X.X% (XX points)
**Status:** ✅ Safe | ⚠️ Within 2% of stop | 🚨 STOP HIT - EXIT NOW

**Gain/Loss:** +X.X% ($XXX)

### USO - Oil (Conditional)
**Current Price:** $XX.XX
**Trigger Price:** $75.00
**Status:** ⏳ Not triggered | 🎯 TRIGGERED - EXECUTE ORDER

---

## Conditional Triggers

**USO Breakout ($75.00):**
- Current: $XX.XX
- Distance: $X.XX (X.X%)
- Status: [Waiting | 🎯 Triggered!]

---

## Summary

**Positions Monitored:** X
**Stops Hit:** 0 ✅
**Warnings:** 0
**Triggers Hit:** 0
**Action Required:** None | [Specific actions]

---

## Next Review
- Daily: Tomorrow at market close
- Weekly: [Next scheduled date]

*Tags: #monitoring #daily-check*
```

### Weekly Review Report

```markdown
# Weekly Portfolio Review - YYYY-MM-DD
**Week:** Week X of 2026
**Portfolio Value:** $XXX,XXX
**Cash Position:** XX% ($XX,XXX)

---

## Position Status

### QQQ - $XX,XXX (XX% of portfolio)
**Stage:** X ([Changed from X] or [Unchanged])
**Score:** XX/100 ([+/- X from last week])
**Current vs Stop:** X.X% above stop
**Performance:** +X.X% since entry
**Recommendation:** HOLD | EXIT | ADD

**Notes:**
[Any stage changes, technical concerns, or opportunities]

### USO - Conditional ($XX,XXX allocated)
**Status:** [Waiting for $75 | Triggered and executed]
**Current Price:** $XX.XX
**Distance to Trigger:** $X.XX

---

## New Screening Results

**Buy Candidates This Week:**
1. [SYMBOL] - Stage X, Score XX ([Same as last week | NEW])
2. [SYMBOL] - Stage X, Score XX

**Lost Candidates (Were buyable, now not):**
1. [SYMBOL] - Moved to Stage X (was Stage 2)

**Comparison:**
- Last week: X buy candidates
- This week: X buy candidates
- Market trend: [Improving | Deteriorating | Stable]

---

## Allocation Analysis

| Position | Target % | Current % | Drift | Action |
|----------|----------|-----------|-------|--------|
| QQQ | 25% | XX% | [+/- X%] | [HOLD / TRIM / ADD] |
| USO | 10% | 0% | N/A | [WAITING / EXECUTED] |
| BIL | 65% | XX% | [+/- X%] | [HOLD / DEPLOY] |

**Cash Deployment Opportunities:**
[List if any strong new Stage 2 candidates emerged]

---

## Alerts & Actions

### 🚨 Critical
[Stop losses hit, positions in Stage 4, etc.]

### ⚠️ Warnings
[Approaching stops, stage transitions to 3, etc.]

### 💡 Opportunities
[Conditional triggers, new buy candidates, etc.]

---

## Market Environment Assessment

**Stage 2 Count:** X ETFs (was X last week)
**Market Character:** [Bullish / Neutral / Defensive]
**Cash Allocation:** XX% ([Appropriate / Too high / Too low])

**Compared to Last Week:**
[Market strengthening, weakening, or stable?]

---

## Recommended Actions

**This Week:**
1. [Action item 1]
2. [Action item 2]

**Next Week:**
- Re-run etf-screener on [date]
- Monitor [specific positions/triggers]
- Consider [specific opportunities]

---

*Next Weekly Review: [Date]*
*Tags: #monitoring #weekly-review*
```

---

## Integration with Other Skills

**Requires:**
- `etf-screener` - Weekly re-screening
- Latest `portfolio-allocation` report - Current positions

**Feeds into:**
- `performance-tracker` - Performance data
- `portfolio-builder` - Rebalancing recommendations
- `obsidian-manager` - Alerts and organization

---

## Alert Severity Levels

### 🚨 CRITICAL (Immediate Action Required)
- Stop loss hit → Exit position immediately
- Position moved to Stage 4 → Exit immediately
- Major stage transition (2 → 4)

### ⚠️ WARNING (Monitor Closely)
- Within 2% of stop loss
- Stage transition 2 → 3 (distribution starting)
- Position oversized (>25% beyond target)

### 💡 OPPORTUNITY (Review and Decide)
- Conditional trigger hit (execute conditional order)
- New strong Stage 2 candidate emerged
- Cash available and opportunities present

### ✅ INFORMATIONAL
- Normal daily movement
- No stops threatened
- Portfolio stable

---

## Monitoring Schedule

### Daily (Market Close)
- Run: After 4:00 PM ET
- Time: ~5 minutes
- Output: Daily check report
- Focus: Stop losses and triggers

### Weekly (Weekend)
- Run: Saturday or Sunday
- Time: ~20 minutes
- Output: Weekly review report
- Focus: Re-screening, stage changes, rebalancing

### Monthly (First Weekend)
- Run: First weekend of month
- Time: ~30 minutes
- Output: Monthly summary
- Focus: Performance review (uses performance-tracker)

---

## Example Usage

### Daily Check
```
User: "Run daily portfolio check"

JARVIS:
1. Reads latest portfolio allocation
2. Fetches current prices for QQQ, USO, BIL
3. Compares to stop losses
4. Checks conditional triggers
5. Generates daily-check-2026-01-26.md
6. Reports: "✅ All positions safe. No stops hit. No triggers."
```

### Weekly Review
```
User: "Run weekly portfolio review"

JARVIS:
1. Re-runs etf-screener skill
2. Compares to last week's screening
3. Checks each position for stage changes
4. Analyzes allocation drift
5. Identifies new opportunities
6. Generates weekly-review-2026-01-26.md
7. Reports: "⚠️ SPY moved to Stage 3. Consider exit.
   New candidate: IWM broke out to Stage 2."
```

---

## Notes

**Key Principles:**
1. **Daily discipline** - Check stops every day (only takes 5 min)
2. **Weekly awareness** - Stay current on market changes
3. **Systematic approach** - Follow same process every time
4. **Alert fatigue prevention** - Only alert what matters
5. **Action-oriented** - Every alert includes clear next step

**Common Mistakes to Avoid:**
- ❌ Skipping daily stop checks (can lead to big losses)
- ❌ Ignoring stage transitions (distribution phase warning)
- ❌ Not re-screening weekly (missing new opportunities)
- ❌ Letting emotions override stops (discipline required)
- ❌ Forgetting to update stop losses when SMAs move up

**Asset Revesting Wisdom:**
- "Only hold what's rising" - Exit when stops hit
- "Cut losses quickly" - Don't hope, follow the system
- "Let winners run" - Raise stops as price rises, never lower
- "Stage matters more than hope" - Trust the stages

---

*This skill maintains portfolio discipline and ensures systematic monitoring of all positions.*
