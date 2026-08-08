# Annotation HUD — lock a dark analysis overlay onto a REAL captured page

For any beat where the argument is carried by someone else's published page and the VO names
specific rows aloud. The capture stays untouched underneath; the HUD acquires rows, brackets
two of them, draws a flat line across a run, and marks a step change.

Built + pixel-verified 2026-08-04. `hyperframes check` clean: 0 errors, **16/16 WCAG AA**.

## Files
- `annotation-hud.html` — the component. Three paste blocks + one call, `mountHUD(tl, opts)`.
- `build-demo.py` — regenerates `demo/index.html`. **Run after every edit.**
- `demo/` — a 44s render on the REAL C5 capture exercising every primitive.
- `demo/snapshots/contact-sheet.jpg` — six states at a glance.

## The rule this component exists to protect

**Rendering a lookalike of a third party's page is the fabrication `VISUAL-SOURCING` §9 forbids.**
The HUD may draw boxes, ratios and labels *over* the capture. The rates must be the capture's own
pixels.

That extends to the labels: **a chip never re-types a number off the page.** Labels are semantic —
`A YEAR AGO`, `TODAY`, `3× CHEAPER`, `NO CHANGE`, `+50%`, `NEW TIER`. The first draft used
`$15 / $75` chips; that was both redundant *and* the thing this component is supposed to prevent,
and as a bonus every chip overflowed the canvas. Short semantic labels fixed all three at once.

## Coordinates come from a measurement, never by hand

```
python3 tools/measure-capture-table.py CAPTURE.png OUT.json --x0 1049 --x1 2692 --y0 1030
```
Pass the emitted JSON as `geometry` plus a `rows` map of semantic name → band index. Re-capture the
page and you re-run the measurement; you do not edit this component or the scene.

**Band ORDER is not semantics.** Crop each band, *read* it, and only then write the `rows` map. Done
for C5 on 2026-08-04 — all 12 bands confirmed against pixels before a line of HUD was written.

## Framing

A framing is a **source rectangle** `{sx, sy, sw}`; scale and translate are derived from the viewport
box, so you author in the capture's own coordinate space.

- **Prefer scale ≤ 1.** Showing 1980 source px of a 3840-wide capture inside a 1380px viewport is a
  0.70× downscale — natively sharp, and ~2× the apparent size of the whole page. Never
  crop-and-upscale to fill the frame; that soft-focuses the one asset that must read as real.
- **Frame WIDER than the table.** The extra page margin on the right becomes the chip gutter. Framed
  tight to the table, every chip lands past x=1920 and the layout checker flags `canvas_overflow`.
- **Pick both vertical edges from the measured bands.** `sy` above the column-header band so
  "Base Input Tokens" / "Output Tokens" are readable, and a height that lands the bottom edge in a
  gap between rows — a capture sliced through a row's text looks like a bug.
- **Keep the viewport clear of the spine rail (x 64–448).** Default box starts at x=500.

## Cue types

| cue | what it does | notes |
|---|---|---|
| `kicker` | source label above the box | lives **outside** the clipped box — inside, it covers the first table row |
| `acquire` | corner brackets + tint on one row | `label` gets a leader line into the gutter |
| `bracket` | vertical brace spanning two rows | for a ratio between them |
| `flatline` | rule drawn across a run of rows | for "these are all identical" |
| `step` | arrow from one row to another | head lands on the **`to`** row, up or down |
| `release` | fades what has already fired | see below |

`tone:'rise'` switches to the crimson accent. Use it **only** for a move in the opposite direction to
the scene's argument — a deliberate comparison split under CONDUIT §2, not a second decorative
colour. It is deliberately **not** the spine's provisional amber, which means something else
("we wrote this and it was wrong").

## Four bugs worth not reintroducing

1. **`release` faded everything, including cues that hadn't fired.** Several reveals animate *scale*,
   not opacity (flatline, tint, leader), so they could never come back. It now fades only cues with
   an earlier index *and* an earlier time.
2. **The step arrow always pointed up.** It ignored row order, so it pointed at the row being moved
   *from*. A viewer tracing it read the change backwards. The head now lands on the `to` row.
3. **Chips overflowed the 1920 canvas** because the table filled the whole viewport. `auditChips()`
   now measures every chip after layout and warns. **If it fires, shorten the label** — do not widen
   the gutter by shrinking the capture.
4. **The kicker sat on top of the first table row.** Never put chrome over the evidence.

Plus the two inherited from `spine-ledger`, both re-armed here: the build script anchors extraction
on the **BLOCK marker comments** (a bare `<style>` regex matches the usage notes and silently kills
the next CSS rule), and `BLOCK B` is extracted **marker-to-marker** rather than "the first div" — a
first-`</div>` regex dropped `#hud-kick` the moment the kicker moved outside the box.

## Mounting across scenes

Scenes render separately and concatenate. `mountHUD` takes **master-absolute** seconds and subtracts
`sceneStart`; anything already past is applied as an immediate end-state via a bare `gsap.set`
(a zero-duration tween parked at position 0 never ticks when the playhead is already at 0 — see
`spine-ledger`'s README).

**In practice, mount each scene with only its own cues** and set `start` to the framing the previous
scene ended on. For this video: S05 starts `wide` and pushes to `table`; **S06 must start `table`
with no move**, or the capture jumps back to the establishing shot at the cut.

## After ANY edit
```
python3 build-demo.py && (cd demo && hyperframes check && hyperframes render)
```
then read the rendered frames. `check` will not tell you whether a box landed on the right row —
only your eyes will, and three of the four bugs above were invisible to it.

## Where it's used first
`jarvis-private/video-projects/claude-code-11-billion-tokens` — S05 (the reversal, abs 306.8) and
S06 (the second reversal, abs 358.6). Cue schedule in that project's `VISUAL-MAP.md` §4.
