# Video QC Pass

Run this on rendered MP4s before locking scene takes or the master.

## Required Validator Gate

Run the scene validator before Terry reviews any HyperFrames scene set:

```bash
python3 tools/scene-validator.py <project-dir>
python3 tools/scene-validator.py <project-dir> --frames
```

Use `--frames` after renders exist to sample frame variance and catch near-empty/background-only stretches. Use `--fix` only for the validator's narrow auto-fix target: shifting overrun `BT.*` helper animations that extend past composition end. Review any `--fix` edit before rendering.

The validator is expected to catch:

- audio-vs-composition duration mismatches
- VO overruns and excessive dead air
- animation events past composition end
- stale `data-duration` attributes
- `tl.call(...)` in scene HTML or transition libraries
- end-of-scene visual gaps
- text overflow risk from large nowrap text
- optional post-render low-variance frame stretches

Validator output must be clean before a scene is considered ready for human review. If a video uses a non-HyperFrames workflow, apply the same classes of checks manually or with the closest available tool.

## Audio

- VO is the main audio by default.
- Music beds, UI clicks, type sounds, section stings, impact hits, and ambient texture are optional supporting elements.
- Supporting audio should be subtle enough that the narration remains clean and intelligible.
- B-roll audio must not double with VO unless intentionally mixed for a brief effect.
- Do not use audio effects to compensate for weak visuals or dead screen time.

## Runtime

- Minimum 8 minutes unless user explicitly requested shorter.
- Preferred 10-15 minutes for full educational/explanatory videos.
- Do not stretch weak content. Add scenes, examples, source proof, or visual demonstrations.

## Text

- No word split mid-letters across lines.
- No adjacent words joined together without spaces.
- No typo in on-screen text, code labels, captions, or source names.
- Kicker labels should be large enough to read on mobile.
- Body/subhead text should not become fine print.
- Headlines and key labels should use the largest feasible size for the layout.
- Avoid narrow containers that force awkward wrapping.
- Use `white-space: nowrap` where a label must stay intact.

## Visual Scale

- Important brain icons, logos, product screenshots, and code should be large enough to understand at YouTube mobile size.
- Avoid tiny "Brain One" style labels. Section labels should read as design elements, not captions.
- Important UI screenshots need zoom/crop/highlight when full-screen capture text is too small.

## Layout

- No overlap between text, icons, charts, cursors, or source screenshots.
- No important text under lower-thirds, logos, captions, or cursor callouts.
- Safe margins are respected.
- Final frame reads clearly as a completed idea.

## Motion And Timing

- Animation beats land on VO words or intentional audio hits.
- No long static sections unless deliberately held for breath.
- Scene rhythm changes every 3-8 seconds for normal explanatory sections.
- B-roll audio does not double with VO unless intentionally mixed.
- No animation reveal should be scheduled after the composition ends.
- No scene should hold a completed visual for multiple seconds unless the hold is an intentional breath and still visually alive.

## Variety

- Compare the scene sequence against `PRESENTATION-VARIETY.md`.
- Patch monotony before final render, not after upload packaging.

## Master

- Run `tools/scene-validator.py` cleanly before final master assembly when applicable.
- Validate scene durations and selected takes.
- Confirm `master.mp4` duration, resolution, codec, and audio stream.
- Watch intro, middle, final third, and all recently changed scenes.
