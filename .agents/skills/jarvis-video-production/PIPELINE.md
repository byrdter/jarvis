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

**Standing rule:** before any work, state that this is `jarvis-video-production` and what it does;
don't run from raw directions or skip the QC gate; surface to Terry only at Step 8.

## Step 0 — Script the video (topic → VO script)  →  `SCRIPTING.md`
If you're starting from a TOPIC (not an existing script), produce the VO script first — see
[SCRIPTING.md](SCRIPTING.md): research the wikis (`tools/research-topic.py`), write in the Show
Bible voice/lenses, structure into 6–9 scenes each with a verbatim first-line **anchor**, and
fact-check into a claim-source map. Scaffold the folder with `tools/scaffold-script.py` (emits
`01-script/` + a `scenes.json` that Step 1 consumes). Output: `VO-ONLY.md` (Terry records it in
HeyGen) + `scenes.json`. If a finished script + take already exist, skip to Step 1.

## Step 1 — Intake / split  →  `tools/split-heygen.py`
Split the HeyGen take into per-scene `assets/audio.mp3` + `transcript.json` (word-level,
scene-relative) + `avatar.mp4` (avatar scenes) + `hyperframes.json`. It transcribes the whole take
once (whisper-1, word timestamps) then slices by scene boundaries — given either explicit start/end
times OR first-line "anchor" phrases from the script (the hands-off path).
```bash
python3 <skill>/tools/split-heygen.py --video heygen.mp4 --spec scenes.json \
  --out <project>/hyperframes-v3/scenes            # --dry-run to preview boundaries first
```
`scenes.json` = ordered `[{name, avatar?, anchor:"first ~6 words"} | {name, start, end}]`.
Always `--dry-run` first to confirm the located boundaries look right; then write. Needs
OPENAI_API_KEY (for whisper) unless `--no-transcribe`.

## Step 2 — Per-scene VO map (correctness foundation)
For each scene, print the sentence-level transcript with timestamps. Build the beat plan anchored to
real word times (see HYPERFRAMES-LESSONS "VO-anchored timing"). This is non-negotiable — even spacing
is the #1 bug.

## Step 3 — Treatment / variety pass
Choose each scene's register from `references/PRESENTATION-VARIETY.md` (≥6 registers per episode, ≤3
consecutive sharing one). **Do NOT default to HyperFrames** — read `knowledge/VISUAL-SOURCING.md` and,
for each scene, ask "what is the BEST way to carry this moment?": a standalone B-roll clip, a
screenshot/web-roll, a real or fabricated document, a symbolic/atmospheric visual, or a HyperFrames
composition. Visuals need NOT be literal — symbolic (papers piling = overwhelm) and atmospheric beats
count. Explicitly assign some scenes to non-HyperFrames registers, and plan **at least one breather
(~3–6s clip) and one symbolic beat** per video. Prefer imagination over headline+bullet text. Pull
assets from the asset library by querying its metadata (see `references/ASSET-CONTRACT.md` +
`knowledge/VISUAL-SOURCING.md` "How the asset database drives this").

## Step 4 — Author scenes (HyperFrames)
Build each `index.html`. ALL motion on the registered `tl` (never free gsap). Add the ambient glow
layer. Anchor every reveal to its VO word. Kicker labels ≥26px/700. No text-on-text / boxes-on-boxes.
For avatar-visible scenes, pass the avatar through (light chrome only).

## Step 5 — Render each scene
`cd <scene> && hyperframes render .` — confirm render duration == `assets/audio.mp3`.

> **Use the PINNED global CLI, never bare `npx hyperframes`.** `npx` grabs whatever version is in its
> cache (this machine had 0.6.7 → 0.7.42 side by side); a scene that needs a registry block or adapter
> from a newer version then renders wrong or fails silently. The pinned binary is installed globally
> (`hyperframes --version` → 0.7.42, at `/opt/homebrew/bin/hyperframes`). Re-pin with
> `npm install -g hyperframes@<ver>` and bump this line when you deliberately upgrade.

## Step 6 — QC GATE per scene (iterate until clean) — do NOT show Terry before this passes
```bash
python3 <skill>/tools/scene-validator.py <project>/hyperframes-v3 --frames
```
The validator now runs a **pre-render determinism gate** (check H) that hard-fails a scene using the
render-killer class — off-timeline `gsap.to/from/fromTo`, CSS `@keyframes`/`animation`,
`requestAnimationFrame`, wall-clock timers, `Date.now`/`performance.now`, `Math.random`. These LOOK
animated in a browser but render FROZEN (or vary frame-to-frame), and are the #1 reason "the effects
don't show up." Fix at the source (attach to `tl`, use `tl.time()` + a seeded PRNG); a deliberate
exception opts out with a trailing `// hf-ok`. Run it BEFORE rendering to avoid wasting a render.
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
**Update the project's `DECISIONS.md`** (in the video folder) as you go — a video-specific log of WHAT
was chosen and WHY: per-scene treatments, every bug found + fix, the `assemble-master.py` parameters
and their reason, and known/open items. This is what lets a future session continue THIS video without
re-deriving (the scene code records the *what*; DECISIONS.md records the *why*). See video-01's
`DECISIONS.md` for the format. Keep it current — it is a required deliverable, not optional.

## Step 9 — Close out (Maintenance Rule)
- Confirm `DECISIONS.md` is complete for this video.
- Fold any NEW *general* lesson into `knowledge/` or the matching `references/` doc (video-specific
  choices stay in the video's `DECISIONS.md`).
- Add new reusable assets to the asset library (tag them via `batch-analyze-assets.py`).
- Commit + push (skill is in the public repo): `git add -A && git commit && git push`.

---
## LEGACY note
`scripts/build-master.sh` (plain concat, hard cuts, no white-frame handling) and
`scripts/validate-scenes.sh` (assumes `scenes/*-pilot` + `compositions[0].duration`) predate the
current `scenes/NN-name` + top-level-duration convention. Use `tools/assemble-master.py` and
`tools/scene-validator.py` instead. Remove the legacy scripts once nothing references them.
