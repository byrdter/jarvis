# Data Flow Particles

**STATUS:** to-build
**Channel fit:** universal
**Tone fit:** educational, technical-demo

## Use case
Animated tokens / particles flowing between nodes (e.g., agent → tool → result, or source → pipeline → destination). The kinetic shape for "data moves through the system" beats.

## Pattern (to implement)
- An SVG path (or arc) connecting two nodes.
- Small particles (dots or pills) travel along the path.
- Particles spawn at the source node and absorb into the destination.
- Multiple particles can be in flight simultaneously with stagger.

## Build approach
- SVG `<path>` defining the route; `stroke` invisible (`opacity: 0`).
- For each particle: a small `<circle>` or `<div>` that follows the path using GSAP's `motionPath` plugin.
- Stagger spawn times: every 0.2–0.4s for a steady flow; longer gaps for a "data trickle."
- Particles fade out at the destination (don't pile up).

## Reference (public examples)
- HyperFrames "particle reveal" templates.
- D3 / Observable data-flow visualizations.

## Anti-patterns (anticipated)
- Too many particles — visual noise. Keep it to 3–6 in flight at any moment.
- Particles too small to see at 1080p — minimum 6–8px diameter.
- Particles that loop forever (`repeat: -1`) — violates HyperFrames deterministic capture. Use finite `repeat: Math.floor(beatDuration / cycleDuration) - 1`.

## Build location when first needed
A Part 2 module showing data flow through an MCP server, or a Part 4 worked-example showing requests/responses.
