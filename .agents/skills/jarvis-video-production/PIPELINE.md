# Video Pipeline — raw HeyGen take → finished master

The end-to-end runbook. Goal: Terry hands over **(1) the raw HeyGen mp4 and (2) the VO script with
scene markers**, and the operator produces a complete first-cut master, running every QC gate, with
**Terry's only required input at the final review**. This is the path; follow it in order.

> Read first: this file, then `knowledge/HYPERFRAMES-LESSONS.md`, `knowledge/ASSEMBLY-AND-AVATAR.md`,
> `references/PRESENTATION-VARIETY.md`, `references/ANTI-PATTERNS.md`, `references/QC-PASS.md`.
> Tools live in `tools/` (`scene-validator.py`, `assemble-master.py`). The legacy
> `scripts/build-master.sh` / `validate-scenes.sh` are superseded — see LEGACY note at bottom.

## Inputs the operator needs
- `heygen.mp4` — the recorded take (one continuous VO performance).
- The VO script broken into N scenes/segments, with per-scene "avatar visible vs graphics" intent
  and any visibility notes.
- Project dir: `${JARVIS_PRIVATE}/video-production/<series>/<video-NN-name>/` with a
  `hyperframes-v3/scenes/NN-name/` per scene (each: `index.html`, `hyperframes.json` with top-level
  `duration`, `assets/`, `renders/`).

## Step 0 — Tell Terry which skill is running (the standing rule)
Before any work, state that this is `jarvis-video-production` and what it does. Then proceed. Do NOT
run from raw directions or skip the QC gate; surface to Terry only at Step 8.

## Step 1 — Intake / split
Extract audio, transcribe, and split the HeyGen take into per-scene `audio` + `transcript.json`
(+ `avatar.mp4` for avatar-visible scenes), anchored to the script's scene boundaries.
(Phase-2: `tools/split-heygen.py` will automate this; until then split with ffmpeg + whisper by the
script's segment timings.) Verify each scene's audio duration matches its `hyperframes.json` duration.

## Step 2 — Per-scene VO map (correctness foundation)
For each scene, print the sentence-level transcript with timestamps. Build the beat plan anchored to
real word times (see HYPERFRAMES-LESSONS "VO-anchored timing"). This is non-negotiable — even spacing
is the #1 bug.

## Step 3 — Treatment / variety pass
Choose each scene's register from `references/PRESENTATION-VARIETY.md` (≥6 registers per episode, ≤3
consecutive sharing one). Prefer imagination over text: isotype grids, self-drawing diagrams,
data-viz, B-roll backgrounds, exec headshots — not headline+bullets. Pull assets from the asset
library (see `references/ASSET-CONTRACT.md`).

## Step 4 — Author scenes (HyperFrames)
Build each `index.html`. ALL motion on the registered `tl` (never free gsap). Add the ambient glow
layer. Anchor every reveal to its VO word. Kicker labels ≥26px/700. No text-on-text / boxes-on-boxes.
For avatar-visible scenes, pass the avatar through (light chrome only).

## Step 5 — Render each scene
`cd <scene> && npx hyperframes render .` — confirm render duration == `assets/audio.mp3`.

## Step 6 — QC GATE per scene (iterate until clean) — do NOT show Terry before this passes
```bash
python3 <skill>/tools/scene-validator.py <project>/hyperframes-v3 --frames
```
Plus the raw gates from HYPERFRAMES-LESSONS (freeze >=5s, white frames). Fix and re-render any scene
that fails (static hold → ambient/breath; sync drift → re-anchor; white → trim/freeze-fill).

## Step 7 — Assemble the master
Handle HeyGen avatar white frames (trim tail / freeze-fill head) per `knowledge/ASSEMBLY-AND-AVATAR.md`,
then:
```bash
python3 <skill>/tools/assemble-master.py master.mp4
```
(varied xfade transitions + matched audio crossfades; pad any scene whose VO runs to its last frame.)
Run the FINAL master gate (freeze + white). Spot-check avatar boundaries and rebuilt beats by frame.

## Step 8 — Human review (the one checkpoint)
Surface the finished master to Terry with: what changed, the gate results, and any flags. Iterate on
his notes. Promote to `master.mp4`, keep the prior as a `.prev.mp4` rollback.

## Step 9 — Close out (Maintenance Rule)
- Fold any NEW lesson learned this video into `knowledge/` or the matching `references/` doc.
- Add new reusable assets to the asset library.
- Commit + push (skill is in the public repo): `git add -A && git commit && git push`.

---
## LEGACY note
`scripts/build-master.sh` (plain concat, hard cuts, no white-frame handling) and
`scripts/validate-scenes.sh` (assumes `scenes/*-pilot` + `compositions[0].duration`) predate the
current `scenes/NN-name` + top-level-duration convention. Use `tools/assemble-master.py` and
`tools/scene-validator.py` instead. Remove the legacy scripts once nothing references them.
