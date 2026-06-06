# Caption Ribbon

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, emphasis-beat

## Use case
A horizontal band overlay that holds a single punchline ("FOUR ANSWERS TO ONE QUESTION", "BEFORE YOU'VE DONE ANY REAL WORK"). The visual emphasis for a key VO line that needs to land hard.

## Reference implementation
- `${JARVIS_HOME}/agent-stack-deep-dive/02-modules/008-tools/hyperframes/index.html` (full-width version, `.caption-ribbon`).
- `${JARVIS_HOME}/agent-stack-deep-dive/02-modules/009-context-window/hyperframes/index.html` (narrow left-aligned version, `.caption-ribbon`).

## Build notes
- Dark navy bg (`rgba(15, 20, 32, 0.92)`), cyan border, rounded corners.
- White text, Inter 800, 28–34px, letter-spacing 0.1em, uppercase.
- Slide-in: `y: 18 → 0; opacity: 0 → 1`, 0.7s, `power3.out`.
- Slide-out: `y: 0 → -10; opacity: 1 → 0`, 0.5s, `power2.in`.
- Drop-shadow + cyan glow for emphasis.

## Width and position decision tree

| Frame state | Use full-width ribbon | Use narrow left-aligned |
|---|---|---|
| Empty bottom half | ✅ | — |
| Meter or chart on right | — | ✅ |
| Centerpiece + satellites | ✅ at bottom 200px | — |
| Centerpiece + tall right element | — | ✅ in left half |

## Anti-patterns
- Full-width ribbon when there's a tall element on the right — text-on-text. Use narrow left-aligned instead.
- Holding the ribbon longer than 4s — punchlines lose impact if they linger.
- More than one ribbon in the same beat — only one punchline per beat.

## Example beats
- Module 08 — "FOUR ANSWERS TO ONE QUESTION" (full-width, sliding in after the four satellites land).
- Module 09 — "BEFORE YOU'VE DONE ANY REAL WORK." (narrow left-aligned, after the stacked meter settles).
