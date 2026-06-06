# Chapter Card

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, transition-beat

## Use case
The "NEXT — X. SIX SEGMENTS." card that slides into upper-center at the close of a part / segment, signaling what's coming. Re-usable across every Part-N opener in long-form videos.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/009-context-window/hyperframes/index.html` (`.chapter-card`, `.chapter-eyebrow`, `.chapter-headline`, `.chapter-sub`, `.chapter-dots`, `.chapter-dot`).

## Build notes
- Card: 720×320, dark-card treatment (navy gradient + cyan border + glow halo).
- **Layout (stacked, all centered):**
  - Eyebrow: "NEXT" (Inter 800, 20px, letter-spacing 0.3em, uppercase, cyan)
  - Headline: the next topic name (Fraunces 600, 100–132px, white, soft cyan glow shadow)
  - Subhead: "SIX SEGMENTS." or other (Inter 500 italic, 24px, letter-spacing 0.12em, uppercase, muted)
  - Progress dots: 6 (or N) small cyan-bordered circles, unfilled
- **Slide-in:** `y: -200 → 0; opacity: 0 → 1`, 1.0s, `power3.out`.
- **Progress dot stagger:** fade-in at 0.7s after card lands, stagger 0.1s each.
- **Sync pulse:** when the next topic name is spoken in the VO, briefly pulse `text-shadow` brightness.

## Anti-patterns
- Don't position the card so it overlaps a still-visible Tools centerpiece or other hero — fade the hero to opacity 0 first.
- Don't reuse without changing the headline name and dot count — every Part opener should feel like a continuation, not a copy-paste.
- Don't animate the dots filling in — they're a teaser for the upcoming 6 segments, not a progress bar. Leave them unfilled until the actual segments unlock in Part 2.

## Example beats
- Module 09 (Beat 7) — "NEXT / MCP / SIX SEGMENTS." with 6 unfilled dots, sync-pulsing on the "MCP" VO word.

## Future expected uses
- Part 2 opener (MCP) — first segment fills dot 1.
- Part 2 mid (Skills opener) — chapter card with "SKILLS" + dot 1 filled.
- Part 2 mid (CLI opener) — "CLI" + dots 1–2 filled.
- Part 2 close (Code Exec opener) — "CODE EXECUTION" + dots 1–3 filled.
