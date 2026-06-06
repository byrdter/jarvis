# Chapter Card Dissolve to Title

**STATUS:** proven
**Channel fit:** universal
**Tone fit:** transition-beat, Part-opener

## Use case
The "NEXT — X" chapter card from a previous module transforms IN PLACE into the new module's editorial title. The card's dark background dissolves, its cyan border dissipates, and the headline scales up to dominate the frame — instead of fading out and being replaced by a separate title element. Creates continuity between Part-N closer and Part-N+1 opener.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/010-mcp-what-it-is/hyperframes/index.html` (`.chapter-card` Beat-2 transformation in the GSAP timeline).

## Build notes
- Inherit the chapter card from the previous module's end state.
- Tween in parallel during the dissolve (~1.6s):
  - `background: rgba(244, 239, 230, 0)` (matches cream stage)
  - `borderColor: rgba(52, 245, 255, 0)`
  - `boxShadow: 0 0 0 rgba(52, 245, 255, 0)`
- Eyebrow + subhead fade out with small `y` lift/drop.
- Headline gets `color: #1A2634` (from white), `textShadow: 0 0 0 rgba(0,0,0,0)`, and `fontSize` scale-up (e.g., 132px → 240px).
- Card itself can resize + reposition to anchor the now-larger headline.
- Progress dots dim and drift down — keep them present as a quiet persistent reference for the rest of the module.

## Anti-patterns
- Don't fade-and-replace — that breaks the continuity signal. The card BECOMES the title; it doesn't get replaced by it.
- Don't keep the chapter card chrome (border/glow) during the new module's main beats — it should be fully gone after dissolve.

## Example beats
- Module 10 (Beat 2) — chapter card "NEXT — MCP. SIX SEGMENTS." dissolves into massive Fraunces "MCP" with "MODEL · CONTEXT · PROTOCOL" subtitle.
