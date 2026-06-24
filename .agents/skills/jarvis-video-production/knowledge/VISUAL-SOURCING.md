# Visual Sourcing — beyond HyperFrames, and beyond literal

The core principle, learned the hard way on video-01: **HyperFrames is ONE register among many, and
on-screen visuals do NOT have to match the VO word-for-word.** We over-relied on HyperFrames-built
graphics and made too many beats literal text/data. A truly entertaining, informative experience uses
the full palette and lets visuals be symbolic, atmospheric, or just a breather.

> This sits alongside `references/PRESENTATION-VARIETY.md` (the 11 registers A–K) and is enforced at
> `PIPELINE.md` Step 3 (treatment pass). Default is NOT "build it in HyperFrames." Default is "what is
> the BEST way to carry this moment?" — which is often a clip, a screenshot, a document, or silence.

## Visuals do not have to be literal

A scene's visual can relate to the VO in any of these ways — all valid:
- **Literal:** the stat/diagram of exactly what's said (HyperFrames data-viz). Use when the number
  or relationship IS the point.
- **Symbolic / representational:** the IDEA, not the words. Papers piling up on someone = overwhelm.
  An empty chair / emptying office = layoffs. A fork in the road = a choice. A person leaning back
  satisfied = things working out. Often more memorable than a literal chart.
- **Atmospheric / human:** office, hands, devices, a person thinking — presence and texture, no direct
  referent. Reminds the viewer there are humans behind the abstractions.
- **Source proof:** the actual article / paper / announcement / screenshot behind a claim (register C).
- **Breather (tension-breaker):** a ~3–6s clip during a general or reflective VO line where the screen
  does NOT need specific text or data. Lets the viewer rest; resets pace before the next dense beat.

## Standalone B-roll / clips (independent of HyperFrames)

A clip can hold the screen by itself — no HyperFrames composition required.
- **Tension-breaker, ~3–6s:** play a fitting human/atmospheric clip full-frame (or lightly graded)
  under a general VO line. Not tied to specific words. Example from the asset library:
  `asset-library/clip-library/pixelvideos/person-leaning-back-satisfied2.mp4` — a "satisfied / it
  worked out" beat to break tension after a heavy section.
- **Establishing shot:** open a beat with a clip, then bring graphics in.
- **Background bed:** low-opacity, scrimmed, under text/graphics.
Rules: strip/silence the clip's audio under VO; keep breathers short (~3–6s); scrim if text sits over
it; don't overuse (a breather every scene stops being a breather).

## Documents & screenshots (real, or HyperFrames-made)

- **Real:** web-rolls, PDFs, articles, app/tool screenshots, code/terminal (registers A/B/C). Animate
  with cursor, highlight, scroll, zoom, callout.
- **HyperFrames-made:** when no real artifact exists, HyperFrames can *fabricate* the document feel —
  e.g. pages/cards piling on top of each other in time with the VO (symbolic accumulation). This is
  HyperFrames serving a non-literal, document-style idea, not a data chart.

## Decision heuristic — what carries this moment?

1. Is it a specific number / relationship? → HyperFrames data-viz or self-drawing diagram (literal).
2. Is there a named source / claim that needs credibility? → web-roll / screenshot (register C).
3. Is it human / emotional / a pace reset / a general statement? → standalone B-roll (atmospheric or
   symbolic), maybe just a breather.
4. Is it a concept or relationship with no number? → diagram (HyperFrames) OR a symbolic clip/image.
5. Is the VO reflective/transitional with no concrete referent? → breather clip or atmospheric bed.
Pick the BEST fit, not the default. Aim for the variety gate: ≥6 registers/episode, breathers and
symbolic beats present, not wall-to-wall literal graphics.

## How the asset database drives this (the metadata layer)

The asset library (being built out) is what makes non-HyperFrames sourcing fast: query the metadata
to find a clip/image/screenshot that fits a moment. For this to work, asset metadata should capture
not just *what it literally shows* but *what it can represent and how it can be used*:
- `concepts` / `symbolizes` — e.g. "overwhelm", "relief", "choice", "growth", "layoffs"
- `mood` — calm, tense, hopeful, somber, energetic
- `usable_as` — breather, background, establishing, symbolic, literal
- `people`, `setting`, `duration`, `palette` — for fit/scrim/length decisions
Then selection is: "find a ~5s calm clip that can represent relief/it-worked-out" → candidates →
pick → place. (Phase-2 asset-library work will audit current metadata and extend the schema toward
this; see PIPELINE Step 3 + the asset-library audit task.)

## What we under-did on video-01 (so we don't repeat it)
- Almost every beat was HyperFrames text/data; few standalone clips, no breathers, little symbolic
  representation, no real source-proof web-rolls.
- Going forward: in the Step-3 treatment pass, explicitly assign some scenes to non-HyperFrames
  registers and plan at least one breather and one symbolic beat per video.

## Background/foreground motion: don't loop short literal clips (Terry, video-02)
A short human/office video clip looped to fill a long beat reads as an obvious repeat — avoid it.
- **Long holds → use a STILL** (faded + scrimmed, Video-1 style), not a looped clip.
- **One-shot clips** (play once, ≤ their length, fade out before the loop point) are fine as ≤5–15s accents.
- **Only abstract "light-show" / particle / shader clips may loop** as a background (no recognizable
  subject to betray the repeat).
- Prefer the BEST presentation per scene — a single still throughout, or genuine change via distinct
  clips — but never the same recognizable clip cycling.

## Representation (Terry — required)
When generating or selecting imagery with people, **represent all people and races** — do NOT default
to a white person. Across a video (and the channel), vary race, gender, and age deliberately so the
audience sees everyone represented. In Nano Banana / Higgsfield prompts, specify diverse subjects
explicitly and vary them scene to scene.

## Foreground is not always HyperFrames (Terry — don't forget)
HyperFrames is the primary tool, NOT the only one. The FOREGROUND/primary of a beat can itself be a
non-HyperFrames format — a full real screenshot (register A), a full-bleed B-roll/clip carrying the
point, a real document/web-roll, a photo. Don't reflexively make every beat "HyperFrames spine +
images layered behind." Some beats should lead with the screenshot/clip/document as the main act, with
HyperFrames reduced to a caption/lower-third. Mix foreground formats across a scene and across scenes.
