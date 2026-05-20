# Video 12 HeyGen Overlay Test Design

Source: `../09-recordings/TestVideoChanges3.mp4`

Goal: keep the HeyGen talking head visible for the opening and closing segments, while replacing the blank middle of the HeyGen file with motion-heavy HyperFrames technical visuals.

Visual standard:

- HyperFrames-first technical editorial style based on the successful `002A`, `002B`, and Segment 003 proofs.
- Dark diagnostic canvas with cyan, amber, green, red, and blue accents.
- Dense but readable system diagrams, token dashboards, simulated code, data paths, meters, cards, and animated process flows.
- No viewer-facing internal labels such as video number, segment number, test labels, or production notes.

Motion standard:

- 2-3 visual beats per segment.
- Use builds, reveals, card flights, scanning beams, meter climbs, tile breaks, stack-in motion, path travel, and compression transforms.
- Fades may support transitions, but should not be the primary action.
- Each completed state should hold briefly before the next segment begins.

Timing assumption:

The HeyGen source contains long pauses between segments. This proof uses the pause-derived boundaries documented in `index.html`; they can be tightened after reviewing the rendered test.
