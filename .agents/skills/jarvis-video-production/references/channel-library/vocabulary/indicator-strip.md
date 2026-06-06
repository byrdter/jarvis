# Indicator Strip

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, technical-demo

## Use case
A horizontal row of small status cards at the bottom of the frame, showing the "agent stack" or any 4–6 sibling concepts. One card brighter than others = "this is the current subject"; multiple dimmed = "context for the current subject."

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/004-foundation-model/hyperframes/index.html` (`.indicators`, `.ind`, `.ind-glyph`, `.ind-text`).

## Build notes
- Container: bottom-aligned, full-width minus margins (~1740px), spread-evenly with flex.
- Card size: ~320×130, dark navy background, soft border.
- Each card has a glyph (SVG) + label (Inter 800, small caps).
- "Active" card: 1.06× scale, intense cyan border, expanded glow.
- "Dim" cards: opacity 0.4.

## State transitions (Modules 04–07 pattern)
- Frame 1 (open): one card bright (the current subject), others dimmed.
- Frame N (close): the next module's subject brightens via cross-fade; old subject dims; "Tools" card visibly intensifies as the climax approaches.

## Anti-patterns
- Don't show more than 5 cards in a row — readability collapses.
- Don't animate the strip during the main teaching beat; it's foreground only when handing off between subjects.
- Don't let the strip rise above the bottom 200px — it competes with main content above.

## Example beats
- Module 04 — Foundation Model active, others dim.
- Module 05 — Perception active.
- Module 06 — Memory active.
- Module 07 — Planning active; Tools intensifies as handoff signal.
- Module 08 — Strip fades out entirely (all four context cards leave); Tools card lifts to centerpiece.
