# Sketchy Annotation Arrow

**STATUS:** proven (basic version)
**Channel fit:** universal — specifically valuable for breaking the rigid-grid feel of HTML composition
**Tone fit:** educational, hand-drawn-aesthetic, breaks the geometric tone

## Use case
A cyan SVG arrow connecting two on-stage elements with a "hand-drawn" feel via irregular dasharray. Used for annotations that read as casual rather than systematic — "this goes here," "this comes back here." Reduces the "I'm looking at a deck of slides" feeling.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/010-mcp-what-it-is/hyperframes/index.html` (`.sketchy-arrow`, `.sketchy-arrowhead`, `.sketch-down`, `.sketch-up`).

## Build notes
- SVG path with cubic Bezier (e.g., `M 380 540 C 460 580 580 605 720 615`). Slight asymmetric curve = handmade feel.
- Stroke: cyan `#34F5FF`, 2.5px, `stroke-linecap: round; stroke-linejoin: round;`
- **Irregular dasharray** is the load-bearing detail: `stroke-dasharray: 6 3 10 4 8 3` — uneven dashes simulate a pen wavering.
- Add a drop-shadow filter for slight depth: `filter: drop-shadow(0 1px 2px rgba(52, 245, 255, 0.25))`.
- Arrowhead: separate `<polygon>` element positioned at the path's terminus, faded in 0.25s after the arrow.
- Reveal: simple opacity fade-in (0.6s) — `strokeDashoffset` reveal also works but the irregular dasharray pattern makes it feel jittery during the draw.

## Anti-patterns (and how to improve)
- **Current limitation:** the path itself is smooth Bezier, so the "sketchy" feel comes only from the dasharray. For a stronger hand-drawn effect, future iterations should use rough-svg or rough.js to actually deform the path with noise, OR construct the path from multiple short Bezier segments with slight randomization.
- Don't use for system-critical flow lines (use `animated-flow-arc` instead). Sketchy arrows are for ANNOTATIONS, not structure.
- Arrowhead must point at a recognizable target — if the arrow ends in negative space, viewer wonders what it's pointing at.

## Example beats
- Module 10 Beat 6 — two sketchy arrows annotate the MCP call: one from AGENT down to the request line, one from the response line back up to AGENT.

## Build improvement queue
- Wire `rough.js` for genuinely hand-drawn path generation. Current version is "irregular dashed line on a smooth Bezier" — readable but not yet truly sketchy.
