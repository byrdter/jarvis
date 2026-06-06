# Comparison Split Screen

**STATUS:** to-build
**Channel fit:** universal
**Tone fit:** educational, analytical, Part-3 comparison

## Use case
Two (or three) panels side-by-side showing different approaches / options / states, with synchronized highlights and labels. Used for Part 3 comparison beats: "MCP vs Skills" or "with vs without code execution."

## Pattern (to implement)
- Vertical divider down the middle (or 1/3 / 2/3 split).
- Each side has its own header, content, and stats.
- Synchronized highlights: when the VO names a property, both sides flash a small badge showing how they handle it.
- Optional: a "winner" indicator (subtle checkmark or accent border) appears on the favored side.

## Build approach
- Two flex children with `flex: 1`.
- Headers (Inter 800, small caps) at top of each side.
- Content area can include code, diagrams, or stats.
- Bottom row: stats grid that gets pulsed in stagger as VO covers each.

## Reference (public examples)
- Marketing comparison tables ("Free vs Pro").
- Performance benchmark charts.

## Anti-patterns (anticipated)
- More than 3 columns — readability collapses. For 4-way comparisons, use a small-multiples grid instead.
- Asymmetric content load (one side has 5 features, the other has 2) — visual imbalance. Match the count or use a different shape.
- "Winner" indicators on Part 2 segments (where we're teaching one mechanism in isolation). Save the verdict for Part 3.

## Build location when first needed
Part 3 comparison module of the Agent Stack video.
