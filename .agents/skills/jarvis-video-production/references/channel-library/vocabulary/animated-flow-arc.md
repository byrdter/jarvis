# Animated Flow Arc

**STATUS:** proven
**Channel fit:** universal
**Tone fit:** educational, technical-demo, transition-beat

## Use case
A thin curved SVG line connecting two flow nodes, drawn in stroke-by-stroke via `strokeDashoffset` animation, with an optional traveling particle that moves along the path. Used to show direction of data flow, protocol message paths, or relationships in a diagram.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/010-mcp-what-it-is/hyperframes/index.html` (`.bridge-arc`, `.bridge-particle`, `.fan-arc`).

## Build notes
- SVG path: gentle quadratic Bezier (e.g., `M 510 510 Q 960 470 1395 510`). 2.5px cyan stroke.
- Animate `strokeDashoffset` from path length down to 0 over ~1.2s with `power2.inOut`. Set `stroke-dasharray` to the path length first.
- For a traveling particle: a small `<circle>` with `motionPath: { path: "#pathId", align: "#pathId", alignOrigin: [0.5, 0.5] }` over 1.5–2s.
- **Note:** GSAP's `motionPath` plugin must be registered via `gsap.registerPlugin(MotionPathPlugin)` — if not loaded, the particle won't travel. Load the plugin in the HyperFrames script tag explicitly:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/MotionPathPlugin.min.js"></script>
  ```
  Then in your script: `gsap.registerPlugin(MotionPathPlugin);`
- Once a particle reaches the destination, fade it out (0.3s) — don't let it pile up.

## Anti-patterns
- Straight lines instead of arcs — feels mechanical. Always use a slight curve via Q or C commands.
- Multiple arcs converging at the same point without staggered draw timing — visual confusion.
- Forgetting to register MotionPathPlugin — the particle silently fails to animate (console warning only).
- Persisting the arc beyond its beat — see Module 10 R1 anti-pattern (bridge arc lingered all the way to Beat 8).

## Example beats
- Module 10 Beat 4 — bridge arc between AGENT ↔ MCP ↔ SERVICE with a traveling particle showing direction of flow.
- Module 10 Beat 5 — 6 fan-arcs from 3 agents through MCP to 4 services, stagger-drawn in waves.
