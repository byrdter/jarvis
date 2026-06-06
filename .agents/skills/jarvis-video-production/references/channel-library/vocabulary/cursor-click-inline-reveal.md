# Cursor Click + Inline Reveal

**STATUS:** to-build
**Channel fit:** universal (especially Byrddynasty + faceless promo)
**Tone fit:** educational, technical-demo, product-walkthrough

## Use case
An animated cursor moves into frame, clicks a UI element (link, button, card), and the result reveals inline (panel slides open, content materializes, navigation transitions). Mimics real user behavior on a web app or interface.

## Pattern (to implement)
1. Cursor SVG enters from a corner, moves to target via easing curve.
2. Brief "click" animation: cursor scales down to 0.85 then back to 1.0 over 0.15s.
3. Target element flashes (border or background pulse) to acknowledge the click.
4. Result content reveals: slide-in, fade-in, or expand-in depending on the surface.

## Build approach
- Cursor: inline SVG with arrow shape, ~28×32px, white fill + dark stroke for visibility on any background.
- Use GSAP `motionPath` plugin OR explicit `to({x, y})` keyframes for cursor movement.
- "Click" tween: `scale: 1 → 0.85 → 1` over 0.15s with `power2.inOut`.
- Target pulse: short border flash (`borderColor: '#34F5FF'`, `boxShadow: '0 0 20px #34F5FF'`) yoyo:1.
- Result reveal: GSAP `fromTo` on the result panel with the matching easing.

## Reference (public examples)
- Stripe product tour HyperFrames templates show cursor-click-then-reveal patterns.
- Notion template demonstrates a cursor clicking a sidebar link and main content swapping.

## Anti-patterns (anticipated)
- Cursor moving too fast — users can't follow if path duration is under 0.6s.
- Cursor moving in a straight line — feels robotic. Use a slight curve or arc.
- No acknowledgment of the click — without target pulse, the click looks ineffective.
- Click happening before the cursor reaches the target — common GSAP timing bug; sequence carefully.

## Build location when first needed
Likely in a Part 2 MCP, Skills, or Code Exec deep-dive module where we demo a real workflow.
