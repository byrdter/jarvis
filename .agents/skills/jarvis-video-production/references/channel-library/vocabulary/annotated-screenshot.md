# Annotated Screenshot

**STATUS:** to-build
**Channel fit:** universal
**Tone fit:** educational, technical-demo

## Use case
A still screenshot of a real product / web app / IDE with motion annotations drawn on top: arrows, highlighted regions, circling shapes, callout boxes with text. The shape for "look at this specific thing on a real interface" beats — when you NEED actual product behavior, not a simulation.

## Pattern (to implement)
- Static screenshot fills the frame (or a contained area).
- Annotations layer animates in stagger: arrow draws in, highlight region pulses, callout text fades in.
- Optional: slight Ken-Burns pan/zoom on the screenshot to add life.

## Build approach
- Screenshot: `<img>` or background-image, scaled to fit.
- Annotations as SVG overlay (arrows, rectangles, circles).
- Use GSAP `drawSVG` plugin to "draw" the arrows in stroke-by-stroke.
- Highlight regions: animated `<rect>` with `stroke-dasharray` reveal.
- Callouts: small dark-card chips with text, slide-in from off-screen direction.

## Reference
- Standard tutorial-video annotation style.
- Existing Jarvis skill `skills/video-image-creation/SKILL.md` references annotation patterns.

## Anti-patterns (anticipated)
- Too many annotations on one screenshot — confusing. Max 3–5 per beat.
- Static annotations (no animation) — feels like a slide. Always animate the reveal.
- Screenshot at low resolution — pixelation kills credibility. Source 1920+ wide.
- Ken-Burns motion too aggressive — gentle 1.0 → 1.04 over 4–6s, no faster.

## Build location when first needed
Anywhere we need to show a REAL interface (Claude Code, Cursor, MCP Inspector, etc.) instead of a simulation. Probably in Part 2 or Part 4 worked examples.
