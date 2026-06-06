# Editorial Spread

**STATUS:** proven
**Channel fit:** Byrddynasty, faceless-editorial
**Tone fit:** educational, premium-product

## Use case
Left pane with eyebrow + headline-with-italic-period. The "this is the topic" introduction shape used in Modules 04–07 as the opening bookend.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/004-foundation-model/hyperframes/index.html` (`.left-pane`, `.eyebrow`, `.headline`).

## Build notes
- Container: `position: absolute; left: 96px; top: 180px; width: 760px;`
- Eyebrow: Inter 700, 22px, letter-spacing 0.28em, uppercase, muted brown (`#8A7B6E`).
- Headline: Fraunces 600, 168px, letter-spacing -0.02em, dark navy.
- The period is wrapped in `<em>` and gets italic styling + warm-brown color (`#5B4738`).
- Drift-in: eyebrow first (`y: 18 → 0`, 0.7s, `power3.out`), then headline 0.5s later (`y: 28 → 0`, 1.0s, `power3.out`).

## Anti-patterns
- Don't compete with another large text element on the right side. If a chat panel is right-side, the headline must finish settling before the chat content starts streaming.
- Don't drop the italic period — it's a load-bearing channel signature.

## Example beats
- Module 04 — "Foundation model." with the period italicized warm brown.
- Module 05 — "Perception."
- Module 06 — "Memory."
- Module 07 — "Planning."
- Module 08 — "Tools." (climax variant — fades out before the constellation forms).
