# Visual Fidelity Rules — the visual must mean what the VO says

**Status: HARD RULES. Non-negotiable. Enforced by `tools/visual-fidelity-check.py`.**

Written 2026-07-21 after the `athlete-syndicates-b2b` build failed review. This is the
single most damaging class of failure we've shipped: the video *looked* finished and was
semantically nonsense. Terry caught it in the first 90 seconds and stopped watching.

---

## What went wrong (the case study — read this, it's the whole reason for the rules)

The VISUALS-MAP for that video was **good**. It specified, scene by scene, a semantically
correct visual for every beat (a handshake under "the athlete rented out their face", a
constellation-hub of 100+ nodes for "Durant's firm spans more than a hundred companies",
an SPV flowchart, dot-grids, comparison-splits).

**The build ignored it.** Measured against the plan and against the last published video
(`ai-ponzi-or-vendor-financing`):

| | Spec / ponzi bar | What shipped |
|---|---|---|
| "athlete rented out their face" | `br-05b_handshake` (**the clip existed**) | a **parrot** from a hallucinations video |
| "own the cap table" | seedling metaphor | seedling + **rice terraces** |
| Durant "100+ companies" | constellation-hub, 100+ nodes | 8 refs, barely built |
| Animation density | 46–123 per scene (avg ~76) | **16–47 (avg ~27)** |
| Borrowed-from-other-video clips | occasional, purposeful | **~20 of ~40 clips** |

Clips from a **Pope encyclical** video (`br-07a_server-nave`), a **hallucinations** video
(`br-04a_two-reactions`, `br-07a_parrot`), and a **datacenter** video appeared in a video
about athlete venture syndicates.

**Root cause:** when you don't BUILD the argument as animated graphics, the frame is empty,
so you reach for whatever clip is nearby. Under-building *causes* the semantic mismatch.
They are one failure, not two.

---

## RULE 1 — The build implements the map. It does not improvise.

Every clip, still, and graphic in a rendered scene MUST be one the `VISUALS-MAP` specifies
for that scene. **You may not substitute an asset because the specified one is inconvenient
to find.** If the specified asset is genuinely missing:
1. Generate it (add to `ASSET-GENERATION.md` gap list), **or**
2. Replace the beat with a BUILT HyperFrames graphic, **or**
3. Change the map deliberately and write the reason in `DECISIONS.md`.

Silently swapping in an unrelated clip is the one thing you may never do.

## RULE 2 — Semantic fidelity: name the noun, then match it.

For each beat, write the concrete noun/idea the VO is saying at that moment, then pick a
visual that **is that thing or a direct symbol of it**. If you cannot state the link in one
short sentence ("a handshake = the endorsement deal being signed"), the visual is wrong.

A visual is WRONG if the only defence is "it's abstract" or "it's visually pleasing."
- ❌ parrot ← "athletes renting out their faces"
- ❌ seedling being watered ← "buying the equity underneath"
- ❌ rice terraces ← anything in a finance video
- ✅ handshake / contract signing ← the endorsement lease
- ✅ cap-table rows lighting up ← buying the equity
- ✅ empty arena with one lit seam ← "the bet they refuse"

## RULE 3 — Build the argument; the clip is a backdrop, not the content.

This is what the published ponzi video does and it is the standard. Its hero scene runs a
custom **node/edge diagram with animated flow pulses**, and b-roll sits *behind* it as a
`broll-scrim` at ~0.30–0.40 opacity. The built graphic carries the meaning; the clip carries
mood only.

If a scene's meaning would survive deleting every clip, it is built correctly.
If deleting the clips leaves an empty frame, the scene is under-built.

## RULE 4 — Animation density floor.

**Minimum 45 timeline animations (`tl.to` + `tl.fromTo`) per content scene; target 70+.**
Avatar/CTA scenes may run lower (≥35). Below the floor, the scene is under-built by
definition — go back and build the teaching graphic the map asked for.

Reference: ponzi shipped 46–123/scene. The rejected athlete build ran 16–47.

## RULE 5 — Cross-video clip reuse is capped and must be earned.

- **Max 2 clips per scene** may come from another video's asset set (`<other-video>__` prefix).
- **Max ~25% of a video's total clips** may be borrowed.
- A borrowed clip must pass RULE 2 on its own merits — the same semantic test, no discount
  for convenience. Its origin video must be thematically unrelated *in name only*, never in
  content (a "server-nave" from a religion video is not a datacenter shot).
- Prefer generating a purpose-built clip for any beat that carries an argument.

## RULE 6 — Backgrounds are per-video.

`bg-*` stills are episode-specific and may recur within the episode. Do NOT import another
episode's `bg-*` as a base layer (the rejected build pulled `datacenter-revolt__bg-02.png`
and `hallucinations-v8__bg-10_gallery-wall.png` into an athlete-finance video).

---

## The gate (run before Terry sees anything)

```bash
python3 tools/visual-fidelity-check.py <project-dir>
```

Fails the build on: unspecified assets in a scene, animation density below floor, borrowed-clip
caps exceeded, foreign `bg-*` imports. This runs **in addition to** `tools/scene-validator.py`
(which covers determinism/duration/freeze, not meaning).

**Both gates must pass before review.** `scene-validator` proves the scene *renders*;
`visual-fidelity-check` proves it *means something*.

---

## RULE 7 — Every scene has a persistent generated background (added 2026-07-23)

Every reference video (`ai-ponzi-or-vendor-financing`, `ai-what-has-to-happen`) gives EVERY scene a
dedicated generated `bg-*.png` that is **always on** behind the content (a `#bgstill`, z-index 1,
`inset:-40px`, slow Ken-Burns `scale 1.0→~1.12` over the whole comp, opacity ~.6–.85). Scenes with a
bare gradient/ambient backdrop read as empty and fail review ("there is no backgrounds at all").
- Generate one purpose-built bg per scene (nano_banana_pro, ~2 credits each), dark-editorial house
  style, vast negative space for overlays.
- **Brighten it enough to be a real backdrop** (filter `brightness(~1.4–1.6)`, light scrim). A too-dark
  bg contributes almost no pixel variance and the near-empty gate still trips. Verify with the
  `scene-validator --frames` sweep.
- Avatar scenes: the face is the primary layer; put the bg behind the **content column** (a right-side
  `#bgPanel`) instead of full-frame behind the face.

## RULE 8 — Build facsimiles, not text-and-boxes. Reach into the whole HyperFrames palette.

"Text + boxes" is the floor, not the bar. HyperFrames can build **facsimiles** that show the receipt
and are far more engaging. Default to these before a plain card:
- **Webpage/browser mock** for any web-source citation (chrome, traffic lights, lock, URL bar, the
  page with the quote highlighted/struck). Proven: the `playersfund.vc` facsimile replacing a cream
  card. This is the standard for web citations (cream cards remain fine for non-web sources).
- **Document/spreadsheet facsimiles** — a `cap-table.xlsx` register (rows, classes, a highlighted
  row, stake bars), a term sheet, a gov.au page. Keep numbers accurate or abstract (bars, not
  fabricated %).
- **Registry blocks** (`hyperframes catalog`, 134 of them): `code-snippet-*` (full VS Code / Apple
  Terminal with typing), `data-chart`, `flowchart`, `news-ticker`, `x-post`/`reddit-post`,
  `apple-money-count`, `world-map`/`us-map`, 3D devices (`vfx-iphone-device`), liquid-glass/WebGPU
  shaders. Install with `hyperframes add <block>` → it drops `compositions/<block>.html`; embed via
  `<div data-composition-src="compositions/<block>.html" ...>`. Build custom inline when you need
  tight VO-timed control on the registered `tl`.
- **Keyframe mechanisms** (`hyperframes-keyframes`): SVG morph/draw, clip/mask reveal, FLIP shared-
  element, SplitText, DOM 3D depth, Three.js camera, shader uniforms, html-in-canvas.
Pick the facsimile whose FORM matches the beat; a plain text card is the fallback, not the default.
