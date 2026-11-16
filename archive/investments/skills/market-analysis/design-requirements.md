# Market Analysis - Design Requirements

These requirements ensure high-quality, consistent market analysis output.

## Quality Standards

### Accuracy Requirements
- [ ] All indicator values must be clearly sourced (real data, sample, or user-provided)
- [ ] Stage determination must cite specific criteria met
- [ ] Confidence level must be justified
- [ ] No indicator should show "N/A" without explanation

### Completeness Requirements
- [ ] All four stages must be considered and ruled in/out
- [ ] At minimum: price, 50/150/200 SMAs, RSI, MACD must be analyzed
- [ ] Both bullish and bearish signals must be considered
- [ ] Transition signals must be explicitly checked

### Clarity Requirements
- [ ] Use consistent terminology from Asset Revesting methodology
- [ ] Explain technical concepts if user is learning
- [ ] Recommendation must be actionable (specific action, not vague)
- [ ] Confidence levels: High (>80%), Medium (60-80%), Low (<60%)

## Stage Determination Criteria

### Stage 1 (Accumulation) - ALL must be true:
- Price below 200 SMA OR recently crossed above
- 50 SMA below 150 SMA (or just crossing)
- RSI recovering from below 40
- Volume declining or base-building

### Stage 2 (Markup) - MAJORITY must be true:
- Price above 50 SMA
- 50 SMA above 150 SMA above 200 SMA (or trending toward)
- RSI between 50-70
- MACD above zero line
- Higher highs and higher lows pattern

### Stage 3 (Distribution) - WARNING SIGNS present:
- Price making marginal new highs or failing at resistance
- RSI divergence (lower highs while price higher)
- MACD rolling over or diverging
- Volume spikes on down days
- Moving averages flattening

### Stage 4 (Decline) - MAJORITY must be true:
- Price below 50 SMA
- 50 SMA below 150 SMA (or crossing down)
- RSI below 50 and falling
- MACD below zero line
- Lower highs and lower lows pattern

## Composite Score Calculation

### Technical Score (40 points max)

| Criteria | Points |
|----------|--------|
| Price above 200 SMA | 8 |
| Price above 150 SMA | 6 |
| Price above 50 SMA | 6 |
| 50 SMA above 150 SMA | 5 |
| 150 SMA above 200 SMA | 5 |
| RSI 50-70 (healthy) | 5 |
| MACD above zero | 5 |

Subtract points for:
- Each bearish divergence: -5
- Price below key MA: -points for that MA
- RSI overbought (>70): -2
- RSI oversold (<30): context-dependent

### Relative Strength Score (30 points max)

| Criteria | Points |
|----------|--------|
| Outperforming SPY (30 days) | 10 |
| Outperforming SPY (90 days) | 10 |
| Sector leading | 5 |
| Relative strength line rising | 5 |

*Note: In Phase 0 without real data, estimate or mark as "N/A - requires data"*

### Stage Score (30 points max)

| Stage | Points |
|-------|--------|
| Stage 2 (confirmed) | 30 |
| Stage 2 (early) | 25 |
| Stage 1 (breakout pending) | 20 |
| Stage 3 (early) | 15 |
| Stage 1 (accumulating) | 10 |
| Stage 3 (confirmed) | 5 |
| Stage 4 | 0 |

## Recommendation Matrix

| Total Score | Stage | Recommendation |
|-------------|-------|----------------|
| 80-100 | 2 | Strong buy / Accumulate aggressively |
| 70-79 | 2 | Buy on pullbacks to support |
| 60-69 | 2/1 | Hold existing / Small adds only |
| 50-59 | 3/1 | Hold with tight stops / Monitor |
| 40-49 | 3 | Reduce exposure / Take profits |
| 30-39 | 3/4 | Exit most positions |
| 0-29 | 4 | Full cash / Avoid |

## Report Formatting Rules

### Headers
- Use h1 (#) only for title
- Use h2 (##) for main sections
- Use h3 (###) for subsections

### Tables
- Always include header row
- Align numbers to right
- Use consistent decimal places

### Signals
- ✅ for bullish/positive signals
- ⚠️ for warning/caution signals
- ❌ for bearish/negative signals
- ➡️ for neutral/transitional signals

### Numbers
- Prices: 2 decimal places ($XXX.XX)
- Percentages: 1 decimal place (XX.X%)
- RSI: whole numbers (no decimals)
- MACD: 2 decimal places

## Real Data Integration (Phase 1+)

**Status:** ✅ Real data available via CLI tool

When using real market data from CLI tool:

1. **State data source** at the top: "Data Source: Yahoo Finance (15-20 min delay)"
2. **Include timestamp** from when data was fetched
3. **Use all available indicators** - don't mark N/A unless truly unavailable
4. **Calculate relative strength** if comparing multiple symbols
5. **Flag data limitations** (e.g., "Only 172 days available - 200 SMA unavailable")

## Fallback (No Data Available)

If CLI tool fails or no internet:

1. **State clearly** at the top: "⚠️ Analysis based on [sample/provided] data"
2. **Skip relative strength** or mark as "Requires real data"
3. **Focus on methodology** - demonstrate the process
4. **Offer to re-run** with real data when available

## Error Handling

If unable to complete analysis:
- State what's missing
- Provide partial analysis if possible
- Suggest what's needed to complete
- Never make up data without clearly labeling it as sample/hypothetical
