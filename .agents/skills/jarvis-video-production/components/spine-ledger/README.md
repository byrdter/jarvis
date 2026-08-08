# Open-question ledger spine — the persistent progress rail for an ARGUMENT

Implements `knowledge/DECISION-RECORD-2026-08-01.md` §3.2. A fork of `spine-elimination`.

**Use `spine-elimination` when the video eliminates suspects. Use this when it argues.**
`spine-elimination` strikes candidates off a list; this tracks *answers to one question*, keeps a
fixed arithmetic head on screen as the stake, and can show an answer being **written and then
corrected** — which is how you put a reversal on the spine itself.

Built + pixel-verified 2026-08-04. `hyperframes check` clean: 0 errors, **67/67 WCAG AA**.

## Files
- `spine-ledger.html` — the component. Three paste blocks (style / markup / script) + one call,
  `mountLedger(tl, opts)`. Full usage in the file header.
- `build-demo.py` — regenerates `demo/index.html` from the component. **Run after every edit.**
- `probe-midscene.js` — the mid-video mount check. **Run after every edit** (see below).
- `demo/` — a 34s render exercising every state. Re-render after any edit; it's the regression test.
- `demo/snapshots/contact-sheet.jpg` — the six states at a glance.

## The one thing this component adds: `provisional`

A row may carry **two** answers. The first is written in amber and tagged `PROVISIONAL`; the second
**strikes it** and lands beneath. The provisional **does not tick the counter**, so the count stays
monotonic (§3.2 property 1) while the viewer watches an answer get written and crossed out.

> **STRIKE MEANS EXACTLY ONE THING: *we wrote this and it was wrong.*** A question that closed
> without a result is `tone:'closed'` — rendered muted, no strike. Diluting the strike costs you the
> reversal, which is the only reason this component exists.

## It satisfies §3.2's four properties, verified in pixels

| Property | How | Verified |
|---|---|---|
| 1 MONOTONIC | `OPEN n` only ticks down; a provisional closes nothing | 4 → 2 → 1 → 0 across the frames |
| 2 GHOSTED NOT LISTED | two ghosts per row (question + first answer), resolve in 0.40s | inside CONDUIT §5's ~1.2s limit |
| 3 UPDATES EVERY BEAT | open / answer / provisional / strike / counter | 17 state changes over 10 units |
| 4 RESOLVES AT VERDICT | last row lands gold and lifts | `THE LONG SESSIONS FIRST` at t=29.2 |

**§3.2's screenshot test passes:** 5.6s / 19s / 24s / 31.5s are told apart from the rail alone.

## ⚠️ ABSOLUTE TIMES — and the mid-scene mount

Scenes render separately and concatenate, so `mountLedger` takes **master-absolute** seconds and
subtracts `sceneStart` itself. Mount it **identically in every scene**, changing only `sceneStart`.
Copy times straight out of `01-script/scenes-v2-build.json`; do no arithmetic by hand.

Anything scheduled before the scene starts is applied as an immediate end-state, so a mid-video scene
opens with its history already on screen. **This path is what breaks, and neither `check` nor
`render` can catch it** — the demo mounts at `sceneStart:0`, where nothing is in the past.

### The bug that proves it — 2026-08-04
Past state was first applied with `tl.set(sel, e, 0)`. A zero-duration tween parked at position 0
**never ticks when the playhead is already at 0**, so it silently did nothing: every scene after S01
would have opened with a **completely blank panel**. `hyperframes check` passed. The render passed.
The contact sheet looked perfect. Only probing the mount at a real `sceneStart` found it.

Fixed by applying past state with a bare `gsap.set()` at mount time. That does **not** violate
*all motion on the registered `tl`* — a scene's static opening state is not motion; everything that
moves is still a `tl` tween.

**So: after ANY edit, run all three.** Check and render alone will lie to you here.
```
python3 build-demo.py && (cd demo && hyperframes check && hyperframes render)
```
then load `demo/index.html` in a browser and paste `probe-midscene.js` into the console.
Expect `ALL PASS`.

## Why it can't hit the old spine's overwrite bug
Inherited from `spine-elimination`. Ghost, question, each answer, each strike bar, each tag and each
counter value are **separate elements**, and **nothing loops** — the original freeze was an ambient
loop sharing a property with a discrete tween on one element. No element is tweened twice on one
property in overlapping windows. Every strike bar sits at `z-index:1` **behind** its answer's
`z-index:2`; drawn on top it is `text_occluded` and the checker fails it, correctly.

**Do not add opacity-dimming to the muted text.** `spine-elimination` can dim `#EBE4D2` to `.46` and
still clear AA; the blue-grey here cannot. Row state is carried by the live marker, the bullet and
the answer's presence instead.

**Never animate the panel's height.** The full DOM is built up front at `opacity:0` so nothing ever
reflows and heights are final from frame one.

## Two accepted cosmetic properties — not defects
1. **A provisional row reserves its second answer slot from the start**, so it sits slightly taller
   than its neighbours before anything happens. Checked in pixels: it reads as layout spacing, not as
   a tell. The alternatives are reflow (worse) or reserving a slot on every row (an empty hole in
   each). Left as is.
2. **The `PROVISIONAL` tag sits ~10px from the end of a 19-character answer.** Legible, and the
   occlusion check passes. A much longer provisional answer would crowd it — the script warns to the
   console on one-line overflow.

## The rule that makes it honest
**Every `open` and every `at` must be pinned to a real VO word-start, never eyeballed.**
```
python3 tools/cue.py 02-vo/v2-transcripts/<act>.json "so the honest shape"
```
The demo's timings are compressed to 34s to exercise the mechanism — exactly as
`spine-elimination`'s and `quote-card-synced`'s demos do. A real build that fabricates them puts a
row's answer off the sentence answering it, which is worse than having no spine.

## Where it's used first
`jarvis-private/video-projects/claude-code-11-billion-tokens` — "We Investigated Claude's Pricing.
Now We're Worried." Spec and the full cue schedule in that project's `VISUAL-MAP.md` §3; machine-
readable in `01-script/scenes-v2-build.json` under `spine_ledger_cues`.
