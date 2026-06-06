# Interaction Vocabulary Library

The tactical bag of patterns. Each file in this directory is one technique.

## File format

Every vocabulary file follows this structure:

```
# <Pattern name>

**STATUS:** proven | to-build
**Channel fit:** Byrddynasty | universal | faceless-promo-cinematic | etc.
**Tone fit:** educational | promo-cinematic | premium-product | etc.

## Use case
When you'd reach for this technique.

## Reference implementation
Path to working HTML (or "to build" with a build approach note).

## Anti-patterns
What goes wrong with this technique.

## Example beats
Real-world uses in shipped modules, if any.
```

---

## Index

### Proven (working reference HTML available)

- [`chat-panel.md`](chat-panel.md) — IDE-style chat with prompt + streaming response
- [`editorial-spread.md`](editorial-spread.md) — eyebrow + headline-with-italic-period left pane
- [`headline-italic-period.md`](headline-italic-period.md) — channel signature device
- [`indicator-strip.md`](indicator-strip.md) — 5-card status row at bottom
- [`satellite-constellation.md`](satellite-constellation.md) — centerpiece + 4 sub-type satellites
- [`action-blips.md`](action-blips.md) — small pills emerging from a hero element
- [`cost-meter-stacked.md`](cost-meter-stacked.md) — token meter with stacked attribution bands
- [`caption-ribbon.md`](caption-ribbon.md) — emphasized text band overlay
- [`chapter-card.md`](chapter-card.md) — Part-opener "NEXT — X. SIX SEGMENTS." card
- [`chapter-card-dissolve-to-title.md`](chapter-card-dissolve-to-title.md) — chapter card transforms into editorial title
- [`flow-node-with-floating-label.md`](flow-node-with-floating-label.md) — small dot + floating label, NO chip
- [`animated-flow-arc.md`](animated-flow-arc.md) — thin curved line between nodes + traveling particle
- [`sketchy-annotation-arrow.md`](sketchy-annotation-arrow.md) — hand-drawn-feel SVG arrow
- [`monospace-on-stage.md`](monospace-on-stage.md) — code fragments on cream stage, no terminal chrome

### To-build (need first reference implementation before use)

- [`cursor-click-inline-reveal.md`](cursor-click-inline-reveal.md) — animated cursor clicks UI element, content reveals inline
- [`vscode-ide-simulation.md`](vscode-ide-simulation.md) — file tree + tabs + syntax-highlighted code + terminal
- [`terminal-session.md`](terminal-session.md) — typewriter command → output → next command
- [`3d-perspective-reveal.md`](3d-perspective-reveal.md) — card flip / depth pan / parallax stack
- [`bento-grid-pan.md`](bento-grid-pan.md) — multi-panel zoom-and-traverse
- [`numeric-reveal-flip.md`](numeric-reveal-flip.md) — large number → large number transition
- [`diff-reveal.md`](diff-reveal.md) — before/after code with highlighted line ranges
- [`data-flow-particles.md`](data-flow-particles.md) — animated tokens flowing between nodes
- [`comparison-split-screen.md`](comparison-split-screen.md) — side-by-side with synced highlights
- [`annotated-screenshot.md`](annotated-screenshot.md) — still + motion annotations
- [`ambient-cutaways.md`](ambient-cutaways.md) — tangential atmospheric visuals (drift overlays, interstitial breaths, periphery orbits)

---

## When you encounter a `to-build` pattern

The first module that needs it builds a minimal reference implementation. Then update that vocabulary file:
1. Change `STATUS:` to `proven`
2. Fill in the `Reference implementation` path
3. Note the build approach you used so future implementations can copy
4. Add the module to `Example beats`

This is how the library grows. Don't ship a vocabulary entry without a reference impl.
