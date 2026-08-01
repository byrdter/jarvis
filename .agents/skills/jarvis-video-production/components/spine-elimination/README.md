# Elimination-list spine — the persistent progress rail

Implements `knowledge/DECISION-RECORD-2026-08-01.md` §3.2. A dark-navy left rail that persists across
the whole video: candidates start as **ghosted blocks**, resolve to a name when the VO names them,
light while under examination, and get struck when ruled out. The last row resolves last and its
resolution **is** the verdict. Built + pixel-verified 2026-08-01.

## Files
- `spine-elimination.html` — the component. Three paste blocks (style / markup / script) + one call,
  `mountSpine(tl, opts)`. Full usage in the file header.
- `demo/` — a 32s render exercising every state. `hyperframes check` passes clean
  (0 errors, 36/36 contrast checks WCAG AA). Re-render after any edit; it's the regression test.
- `demo/snapshots/contact-sheet.jpg` — the three states at a glance.

## It satisfies §3.2's four properties, verified in pixels

| Property | How | Verified |
|---|---|---|
| 1 MONOTONIC | the counter only ticks down | 6 → 4 → 1 across the three frames |
| 2 GHOSTED NOT LISTED | slots visible from the start, names withheld; resolve in 0.45s | inside CONDUIT §5's ~1.2s ghost limit |
| 3 UPDATES EVERY BEAT | 3 events per row (resolve / light / strike) + counter ticks | ~18 events over the run |
| 4 RESOLVES AT VERDICT | survivor lights gold and lifts | `SESSION LENGTH` at t=29 |

**§3.2's screenshot test passes:** frames at 3s / 15s / 29s are told apart from the spine alone.

## Two things `hyperframes check` caught that reading the code would not have

1. **An overlay veil dimming a struck row is `text_occluded`** — and the checker is right: covering
   type is not the same as dimming it. The veil was removed; the label now tweens its **own** opacity
   down, in a window that cannot overlap its resolve tween (the same in/out pattern
   `quote-card-synced` uses safely).
2. **A strikethrough drawn on top of the glyphs is also `text_occluded`.** The bar now sits at
   `z-index:1` **behind** the label's `z-index:2`. It still reads as a strikethrough — it shows
   through the letter gaps — and the type stays fully legible.

Both were fixed, not suppressed.

## Why it can't hit the old spine's overwrite bug
The bug was an ambient **loop** sharing a property with a discrete tween on the same element
(breath vs resolve): the loop overwrote the resolve and the row rendered frozen. Here the ghost block
and the label are **separate elements**, the strike bar is its own element, and **nothing loops**.
Every element/property pair is tweened only in non-overlapping windows. All motion on the registered
`tl` — a bare `gsap.to` renders FROZEN.

If you add ambient motion later, put it on a dedicated element that no discrete tween touches.

## The one rule that makes it honest
**Every `resolve` and `strike` must be pinned to the VO word-start, never eyeballed.** At build time:

```
python3 tools/cue.py <scene-transcript.json> "the model"
```

The demo's timings are **compressed to 32s to exercise the mechanism** — exactly as
`quote-card-synced`'s demo fabricates word timings. A real build that fabricates them puts the row
resolve off the sentence naming that row, which is worse than having no spine.

## Where it's used first
`VIDEO-PLAN-claude-code-usage.md` (video 1) — six candidates, the survivor being SESSION LENGTH.
Act boundaries are measured in `VO-video1-claude-code-usage.txt`; the within-act times in the
component header are estimates until `cue.py` pins them.

## Known environment drift
Built against **hyperframes 0.7.87** (`npm ls -g` authoritative, 2026-08-01).

The binary reported 0.7.84 at the start of this build and 0.7.87 by the end — **it self-updated
mid-build, unprompted.** The demo's clean `check` and its three snapshots are therefore 0.7.87
output. The stale 0.7.72 pin has been reconciled across `CLAUDE.md`, `PIPELINE.md` and
`HYPERFRAMES-TECHNIQUE-PALETTE.md`; all three now say the pin is a **record, not a lock**, and to
assert the version at batch start AND before master assembly.
