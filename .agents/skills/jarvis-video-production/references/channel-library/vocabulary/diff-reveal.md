# Diff Reveal

**STATUS:** to-build
**Channel fit:** universal (Byrddynasty + faceless-dev)
**Tone fit:** educational, technical-demo

## Use case
Before/after code side-by-side or top-and-bottom, with red highlights on removed lines and green on added lines. The natural shape for "the agent rewrites this code" or "this approach vs that approach" beats.

## Pattern (to implement)
- Two code panels (or one with overlay) showing before + after.
- Removed lines: subtle red tint background (`rgba(255, 100, 100, 0.12)`), strikethrough optional.
- Added lines: subtle green tint (`rgba(100, 255, 130, 0.12)`).
- Animation: removed lines fade out / slide left; added lines slide in from right or fade in.

## Build approach
- Each line is a `<div>` with a class indicating its diff state (`added`, `removed`, `unchanged`).
- GSAP timeline:
  1. Show "before" state with both `removed` and `unchanged` lines.
  2. `removed` lines fade out / slide / strike.
  3. `added` lines fade in.
- Optional: a thin vertical "diff gutter" on the left showing `-` / `+` markers.

## Reference (public examples)
- GitHub PR-style diff visualizations.
- HyperFrames "code-card reveal" templates can be adapted.

## Anti-patterns (anticipated)
- Showing huge code blocks (>20 lines) — viewer can't track changes. Keep diffs surgical: 3–8 lines of relevant context.
- Heavy red/green saturation — clashes with cream stage. Use the subtle tints above.
- Diff appearing without VO support — give the viewer the verbal callout ("we changed the prompt from X to Y").

## Build location when first needed
Likely in a Part 2 Skills module showing procedural code, or any Part 2/3 beat comparing approaches.
