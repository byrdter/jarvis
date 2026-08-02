# Bed drift — the always-moving photographic bed, as a `tl` transform

Implements `CONDUIT-VISUAL-SYSTEM.md`'s *"darkened, defocused photographic bed with continuous
ambient motion"* without generating a video clip. One continuous transform on the still, spanning the
whole scene. Built + pixel-verified 2026-08-02.

## Files
- `bed-drift.html` — the component. Three paste blocks (style / markup / script) + one call,
  `mountBed(tl, opts)`. Full usage in the file header.
- `demo/` — a 20s render exercising `drift-left`. `hyperframes check` passes clean
  (0 errors, 0 warnings, 0 layout issues across 9 samples, 5/5 contrast WCAG AA).
  Re-render after any edit; it's the regression test.
- `demo/snapshots/contact-sheet.jpg` — t=0 / 10 / 19.9s against a **static** gold reference cross,
  so the drift is provable rather than asserted.

## Why not just generate the bed as a clip

| | generated clip | `tl` transform |
|---|---|---|
| under a 2:47 scene | ~16 loop cycles | **one continuous move, no loop point** |
| cost | ~10 credits each | **0** |
| re-render | can vary between runs | **deterministic** |
| scene length changes | re-generate the clip | **change one number** |

The honest tradeoff: a generated bed has *internal* motion (haze billowing, lights shimmering); a
transform moves a flat image. At 0.50 opacity behind the scrim, under chart content, that difference
has not been visible in testing. If a specific scene needs real internal motion, generate that one.

## Usage

```js
mountBed(tl, {
  src: 'assets/bg-03_workspace.png',
  duration: 100.1,        // the SCENE's full length in seconds
  move: 'drift-left'      // push | drift-left | drift-right | rise | sink
});
```

`scale` defaults to `.08` (8% travel across the whole scene, regardless of length, so every bed
feels equally slow). `scrim: false` drops the scrim if the scene supplies its own.

## Two things that are load-bearing and non-obvious

**1. `BASE_SCALE` is 1.06, not 1.00.** A pure zoom from 1.00 is edge-safe. A zoom *plus a translate*
is not — at 1.00, any x/y move drags the image edge into frame as a black band, which is §9 rule 3's
"never a blank frame" in its most embarrassing form. The bed sits at 6% overscan (3% each side) and
grows; `MAX_SHIFT` is capped at 2% so it can never exceed the margin. **Never lower `BASE_SCALE`
without also lowering the cap.**

**2. `data-layout-allow-overflow` is required on `#bed`.** The overscan deliberately pushes the image
outside `.bedwrap`, so without the attribute `hyperframes check` reports `container_overflow` at every
sampled time — nine info lines of pure noise that train you to skim the layout checker. Declare the
intent instead.

## What `hyperframes check` gave us for free

Before the overflow was declared, the checker printed the overflow in pixels at each sampled time:

```
t=10s     #bed overflowed left 115.2px, right 76.8px
t=18.89s  #bed overflowed left 166.3px, right 93.86px
```

Left exceeds right, and the gap widens 38px → 72px. **That asymmetry is a frame-by-frame proof the
tween is live under seek** — a frozen bed would report identical symmetric numbers at every
timestamp. Worth remembering as a cheap frozen-render detector for any transformed element.

## The renderer rule this exists to satisfy

HyperFrames renders by **seeking**: for frame N it sets the timeline to `N/fps` and screenshots.
Anything animating outside the registered `tl` has no defined state at an arbitrary time and
**renders frozen** — silently, no error. So the single tween is on `tl`, it never loops, and nothing
else ever touches `#bed`'s transform. That last clause matters: the bug that froze the earlier spine
was an ambient loop sharing a property with a discrete tween on the same element. If you need an
extra flourish, put it on its own element.

Built against **hyperframes 0.7.88**. ⚠️ The global binary self-updates — it moved 0.7.87 → 0.7.88
during this session. Run `hyperframes --version` at batch start; if it has moved, re-render the whole
batch so one master never mixes versions.
