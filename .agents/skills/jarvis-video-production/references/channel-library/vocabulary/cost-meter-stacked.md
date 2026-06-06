# Cost Meter — Stacked Attribution

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, analytical, telemetry

## Use case
A vertical bar meter that decomposes a total budget (tokens, dollars, time, %) into colored bands stacked from bottom to top. Each band has a label and amount. Bands land synced to VO word boundaries as each cost source is named.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/009-context-window/hyperframes/index.html` (`.cost-meter`, `.cost-meter-bar`, `.cost-band`, `.band-system` / `.band-schemas` / `.band-conv` / `.band-results` / `.band-mcp` / `.band-skills` / `.band-cli` / `.band-code`, `.scale-tick`).

## Build notes
- **Meter container:** ~280px wide × 760px tall for the "wide promoted" state. Promotes from a thin (~80px wide) foreshadow state.
- **Header:** "CONTEXT WINDOW / 200K TOKENS" stacked, Inter 800 small-caps.
- **Scale ticks:** position outside the meter on the left, labels at 0 / 50K / 100K / 150K / 200K (or your scale).
- **Bands:** absolute-positioned with `bottom` and `height` in px, computed from `meter_height / scale_max * band_value`.
- **Band colors:** distinct palette per category (slate / teal / lavender / amber for always-on; cyan / magenta / lime / orange for sub-types). Distinct enough to read as separate categories at thumbnail size.
- **Band labels:** to the LEFT of the meter. For very thin bands at the top of the stack, use explicit `top` offsets with thin leader lines (CSS `::after` pseudo) instead of relying on auto-centering.
- **Counter:** monospace below the meter, animated via GSAP `onUpdate` callback ticking up to the new total when each band lands.

## CSS gotcha
`.cost-meter-bar { overflow: hidden; }` will clip band labels positioned with negative `left`. Use `overflow: visible` on the bar and isolate any clipping needs to a separate inner element (e.g., the orange foreshadow fill).

## Anti-patterns
- Don't show a horizontal caption ribbon at full width during a meter beat — it overlaps the meter. Narrow the ribbon to fit the empty half of the frame.
- Don't keep more than 4 always-on bands; the labels get crowded fast. 4 is the practical max for readability.
- Don't fade out scale ticks while bands are still landing — viewers need the scale to interpret heights.

## Example beats
- Module 09 (Beats 3–4) — 4 always-on bands + 4 sub-type bands stack to 55,000 tokens of 200K budget.
