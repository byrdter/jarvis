# Satellite Constellation

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, premium-product

## Use case
A central hero element (the subject) surrounded by 3–5 smaller "satellite" cards (sub-types or related concepts), with thin dashed connector lines from each satellite to the hero. The natural shape for "X has these sub-types" beats.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/008-tools/hyperframes/index.html` (`.tools-center`, `.satellite`, `.sat-mcp` / `.sat-skills` / `.sat-cli` / `.sat-code`, `.connections`, `.connection-line`).

## Build notes
- **Centerpiece:** ~480×350, dark-card treatment, large glyph + label inside.
- **Satellites:** ~220×110, dark-card treatment with smaller glow.
- **Standard 4-satellite positions:**
  - top-left: `(270, 220)`
  - top-right: `(1430, 220)`
  - bottom-left: `(270, 540)`
  - bottom-right: `(1430, 540)` (slightly wider if label is long, e.g., 280px for "CODE EXEC")
- **Connections:** SVG `<line>` elements, `stroke: #34F5FF; stroke-dasharray: 6 6; opacity: 0.55;`
- **Reveal pattern:** centerpiece materializes first; satellites stagger in (back.out(1.8), 0.6s each) with brief glow pulses; connection lines fade in shortly after.

## Anti-patterns
- Don't try to fit 5+ satellites without redesigning positions — corners get crowded.
- Don't let satellites overlap any other always-on element (cost meter, caption ribbon, brand mark). When introducing a meter or ribbon, fade satellites out cleanly first.
- Don't animate the connector lines unless you have a specific narrative reason — they're structural, not kinetic.

## Example beats
- Module 08 — TOOLS centerpiece with MCP / SKILLS / CLI / CODE EXEC satellites.
- Module 09 (Beat 1) — inherits same constellation; fades it out in Beat 2 to promote the cost meter.
