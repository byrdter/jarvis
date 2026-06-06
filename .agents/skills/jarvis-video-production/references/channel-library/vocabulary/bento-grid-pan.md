# Bento Grid Pan

**STATUS:** to-build
**Channel fit:** universal (especially faceless-promo)
**Tone fit:** premium-product, feature-overview, transition-beat

## Use case
Multiple panels arranged in a non-uniform grid (varying cell sizes), with the "camera" panning across and zooming into individual cells to feature each one in turn. Spotify's bento layouts and Apple product pages use this pattern.

## Pattern (to implement)
- Grid container with absolutely-positioned cells of varying sizes.
- Initial state: zoomed out, seeing all cells at small scale.
- Pan-and-zoom: tween container `scale` and `translate` to focus on each cell in turn.
- Each cell has its own internal content (card, demo, stat, image).

## Build approach
- Container: `transform-origin` set per pan target.
- GSAP `to({scale, x, y, transformOrigin: 'X% Y%'})` for each pan beat.
- Use `power2.inOut` easing for smooth pan-and-zoom.
- 1.5–2.5s per pan beat is the readable range.

## Reference (public examples)
- HyperFrames "Spotify bento" template.
- Apple product page bento sections.

## Anti-patterns (anticipated)
- Too many cells (>6) — viewer can't track which is the current focus.
- Zoom levels that distort text legibility — cap zoom ratio at ~2.5×.
- Pan paths that double back — feels lost.

## Build location when first needed
Possibly Part 3 (comparison module) showing 4 sub-types side-by-side with feature highlights. Or promo cuts.
