# Charts — the three data-viz primitives this channel actually needs

Built + pixel-verified 2026-08-04. `hyperframes check` clean: 0 errors, **44/44 WCAG AA**.

| function | shape | the beat it serves |
|---|---|---|
| `mountInversion` | four bars that **resize and reorder** between two measures | "volume is not cost" — the big bar becomes the small one |
| `mountDotGrid` | N dots, a subset lit, a sub-subset flared | concentration — "49 of these carry 90% of it" |
| `mountRatio` | stacked bars + a multiple | "20× what the read would have cost" |

## Files
- `charts.html` — three paste blocks + three mount functions.
- `build-demo.py` — regenerates `demo/index.html`. **Run after every edit.**
- `demo/` — 56s exercising all three on the REAL frozen figures.
- `demo/snapshots/contact-sheet.jpg` — six states.

## The reorder IS the argument

`mountInversion` computes slot order **from the data**, per measure, biggest first. The flip tweens
bar width and slot position together in one move. Don't treat it as a transition to be smoothed past
— it is the beat the scene exists for, and it should be the slowest thing on screen.

Slot order is derived, never declared, so the reorder cannot disagree with the bars being reordered.

## Numbers are passed in, never derived

Every value and its label are given together and must already agree. Nothing computes a percentage
from a value or vice versa. Source them from the project's `claim-source-map.md` and nowhere else —
**the VO says both aloud**, and a chart that derives its own label is a chart that can silently
disagree with the voice.

The demo uses the real frozen figures for the same reason: a chart demo built on fake numbers tells
you nothing about whether the chart can hold the real ones. (It caught that `0.03%` needs two
decimals where `92.9%` needs one.)

## Counters are seek-safe

They tween a proxy object and write `textContent` in `onUpdate`. That fires on **seek** as well as
on play, which is what the deterministic renderer does — it seeks every frame. Do not "optimise"
this into a `setInterval` or a `requestAnimationFrame` loop; both render FROZEN.

## Three bugs worth not reintroducing

1. **`width:100%` on the bar fills is load-bearing.** An absolutely-positioned element with no width
   is 0px wide, and `scaleX` on 0px is still 0px. The tweens ran perfectly and the bars were
   invisible — `check` passed, contrast passed, and only the render showed it.
2. **`vp.h` is a minimum, not the truth.** Each chart calls `fit()` to set its own height from laid-out
   content. A caller-supplied height that is too short makes every element below the fold report
   `escaped_container` — which is what the dot-grid captions and the ratio multiple both did.
3. **The two measure labels share a position.** The outgoing one must be gone *before* the incoming
   lands, or it reports `content_overlap`. There is a −0.30s lead on the fade-out.

Plus the two inherited build-script traps, re-armed here: extraction anchors on the **BLOCK marker
comments** (a bare `<style>` regex matches the usage notes and silently kills the next CSS rule), and
BLOCK B is taken **marker-to-marker** rather than "the first div".

## Dot grid notes
- The lit subset is the **first k in reading order**, so it reads as one block. Concentration is the
  claim; scattered dots would say the opposite.
- Lighting uses **one tween with many targets and a stagger**, not k separate tweens.
- `cols` should divide `total` exactly where possible — 490 = 35 × 14, so the grid has no ragged
  final row and the proportion is exact rather than approximate.

## Where they're used first
`jarvis-private/video-projects/claude-code-11-billion-tokens`:
`mountInversion` S03 (flip at abs 203.3) · `mountDotGrid` S03 (abs 224.1) and again S08 ·
`mountRatio` S09. Cue schedule in that project's `VISUAL-MAP.md` §4.
