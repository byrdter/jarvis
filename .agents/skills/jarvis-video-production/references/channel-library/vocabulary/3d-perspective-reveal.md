# 3D Perspective Reveal

**STATUS:** to-build
**Channel fit:** Byrddynasty (cinematic moments), faceless-promo
**Tone fit:** premium-product, transition-beat, climactic

## Use case
Card flip, depth pan, parallax stack, isometric reveal. Used for "introducing the subject from a dramatic angle" or "revealing what's behind a surface." Higher-energy than a flat reveal.

## Pattern (to implement)

### Variant A: Card flip
- Card starts rotated 90° around Y-axis (edge-on, invisible).
- Rotates to 0° with `power3.out`, 0.8–1.2s.
- Optional: back-face has a different graphic (the "reveal").

### Variant B: Depth pan
- Multi-layer composition: background, midground, foreground.
- "Camera" moves forward by tweening each layer's `scale` and `translateZ` (CSS perspective).
- Layers move at different rates (parallax).

### Variant C: Isometric stack
- Multiple cards stacked at slight angles in 3D space.
- Tween `rotateX`, `rotateY`, `translateZ` to reveal the stack from above.

## Build approach
- Parent container: `perspective: 1200px; transform-style: preserve-3d;`
- Each layer: `transform: translateZ(<depth>px) rotateY(<angle>deg);`
- GSAP can tween these properties directly. Keep tweens short (0.8–1.5s) — long 3D moves get nauseating.
- Use `will-change: transform` on the animated elements.

## Reference (public examples)
- HyperFrames "UI 3D reveal" templates.
- Apple-style "card flip to reveal feature" patterns.

## Anti-patterns (anticipated)
- Excessive perspective angle (under 600px) — distortion looks broken.
- Rotating elements past 180° — back faces show up unintentionally; viewers get disoriented.
- Multiple simultaneous 3D animations — vestibular overload.
- 3D on educational beats — feels promo when the tone should be educational. Reserve for climax / promo cuts.

## Build location when first needed
Possibly in a Part 2 climactic reveal (e.g., showing the Code Execution sandbox "from inside"). Definitely in promo cuts for vertical/short-form.
