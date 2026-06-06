# Numeric Reveal Flip

**STATUS:** to-build
**Channel fit:** universal
**Tone fit:** climactic, payoff-beat, promo

## Use case
A large number on screen flips dramatically to another number — the "77,000 → 8,700" cost-crash beat. The whole frame is dominated by the number; the transition is the moment.

## Pattern (to implement)
- Initial number on screen, large (200–400pt Fraunces or similar editorial face).
- "Crash" transition: old number scales up briefly then fades / smashes; new number drops in from above with a heavier weight.
- Optional: per-digit flip (like an old airport board / split-flap display).
- Caption above ("BEFORE") and below ("AFTER") frames the comparison.

## Build approach

### Variant A: Smash transition
- Old: `scale: 1 → 1.15 → 0` over 0.6s with red tint final.
- New: `y: -80 → 0; opacity: 0 → 1; scale: 0.8 → 1` over 0.7s with green tint, `back.out(1.8)`.

### Variant B: Split-flap per digit
- Each digit is a separate `<span>`.
- Per-digit tween: rotate `rotateX: 0 → -90` while old digit fades, then `rotateX: 90 → 0` for new digit fade-in.
- Stagger digits left-to-right (or center-out).

## Reference (public examples)
- Stripe pricing comparison templates.
- Y Combinator-style "from X to Y" stat reveal.

## Anti-patterns (anticipated)
- Both numbers visible simultaneously without a clear "moment of flip" — feels uneventful.
- Too-fast flip (under 0.5s) — viewer can't read either number clearly.
- Tiny numbers — defeats the purpose; this is a full-screen moment.

## Reserved for
- Part 2 cost-crash beats (e.g., MCP-without-skill 77K tokens vs MCP-with-skill 8.7K tokens).
- Promo cut hero shots.

Do NOT use this for Module 09 (Context Window) — the cost surface there is a stacked meter, not a single number flip. Save the flip for the Part 2 payoff.
