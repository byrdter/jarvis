# Video Pipeline — raw HeyGen take → finished master

The end-to-end runbook. Goal: Terry hands over **(1) the raw HeyGen mp4 and (2) the VO script with
scene markers**, and the operator produces a complete first-cut master, running every QC gate, with
**Terry's only required input at the final review**. This is the path; follow it in order.

> Read first: this file, then `knowledge/HYPERFRAMES-LESSONS.md`, `knowledge/ASSEMBLY-AND-AVATAR.md`,
> `references/PRESENTATION-VARIETY.md`, `references/ANTI-PATTERNS.md`, `references/QC-PASS.md`.
> Tools live in `tools/` (`scene-validator.py`, `assemble-master.py`, `make-dispatch-endcard.py`). The legacy
> `scripts/build-master.sh` / `validate-scenes.sh` are superseded — see LEGACY note at bottom.

## Inputs the operator needs
- `heygen.mp4` — the recorded take (one continuous VO performance).
- The VO script broken into N scenes/segments, with per-scene "avatar visible vs graphics" intent
  and any visibility notes.
- Project dir: `${JARVIS_PRIVATE}/video-projects/<video-name>/` with a
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

**Before authoring each scene, pick its technique from `knowledge/HYPERFRAMES-TECHNIQUE-PALETTE.md`**
(match the beat's JOB — proportion/place/timeline/relationship/comparison — never default to a text
card). The load-bearing capability docs are ALWAYS available on every machine at
`~/.claude/skills/hyperframes-{animation,creative,registry}/` — read the specific rule/blueprint there.
**For real "this is what it should look like" examples, consult the maker compositions** — but they
live on the external ORICO drive, so guard first:
```bash
REF=/Volumes/ORICO/hyperframes-upstream
[ -d "$REF" ] && echo "ref available: $REF/hyperframes-launches (vfx-heygen-combined, spacex-launch, texture-launch…)" \
             || echo "ORICO not mounted — skip example lookup; plugin skills at ~/.claude/skills/hyperframes-* are sufficient"
```
If ORICO isn't mounted, proceed with the plugin skills (nothing critical is gated behind the drive).

## Step 5 — Render each scene
**FIRST run `hyperframes check .` in the scene dir — it catches a whole class of defect that
`scene-validator.py` does not.** Expect `Check passed, 0 errors`. Do not render a scene that errors.

> ### `media_missing_id` — add ids, but it is an ADVISORY, not a frozen-render bug (batch 2026-07-18)
> `hyperframes check` errors on a timed `<video>` that has `data-start` but no `id`, and its message
> ("this video will be FROZEN in renders") reads as a hard defect. **On 0.7.63 it is not.** We chased
> this hard and the fix proved to be a **pure no-op**: old and new renders came back pixel-identical
> (mean abs diff 0.73–1.29 = encoder noise), and the footage was verified *playing in both*.
> **Add the ids anyway** — `hyperframes check` is a gate you want passing, and the guarantee may change
> between versions — but do NOT tear down a finished master over this alone. **Verify before escalating.**
>
> **The cautionary tale:** the escalation was built on inference, not measurement — a check error, a
> scary message, and an inconclusive frame-diff. Composited frames cannot settle it: scrim and opacity
> scale the difference, and a near-static subject (a talking-head avatar) shows low motion even when
> playing perfectly. Cost: 18 scenes re-rendered for nothing.
> ```html
> <!-- WRONG — renders frozen, silently -->
> <video src="assets/clip.mp4" data-start="31.8" data-duration="3.2" muted playsinline>
> <!-- RIGHT -->
> <video id="vid-clip-1" src="assets/clip.mp4" data-start="31.8" data-duration="3.2" muted playsinline>
> ```
> **Audit any project fast:**
> ```bash
> python3 - <<'EOF'
> import re,glob
> for f in glob.glob('*/hyperframes-v3/scenes/*/index.html'):
>     for t in re.findall(r'<video[^>]*>', open(f).read()):
>         if 'data-start' in t and not re.search(r'\bid\s*=', t): print('MISSING id:', f)
> EOF
> ```
> ### ✅ THE way to prove a clip is playing (source-time tracking)
> Frame-diffing a render against itself is inconclusive. Ask instead: **does the rendered frame at Δ
> seconds into the clip's window match the SOURCE at Δ, or the source at 0?** Playing tracks Δ; frozen
> pins to 0. Edge-filter both first so it's brightness/scrim-invariant, and crop to the clip's panel rect
> if it's an inset (a full-frame compare on a small inset reads as ambiguous):
> ```python
> # for delta in (0.5, 2.5):
> #   render@(data_start+delta)  vs  source@delta   -> score A
> #   render@(data_start+delta)  vs  source@0.1     -> score B
> #   A < B  => PLAYING (tracks source time)   |   B < A => FROZEN
> ```
> Real numbers from a confirmed-good scene: `render@Δ2.5 vs source@2.5 = 10.31` against
> `vs source@0 = 11.79` → playing. Use this before claiming any clip is frozen.

`cd <scene> && hyperframes render .` — confirm render duration == `assets/audio.mp3`.
**One render per shell call.** Chaining two renders in one call fails, and `render.sh … && echo` masks
HyperFrames render failures — a render can report success while producing nothing.

> **Use the PINNED global CLI, never bare `npx hyperframes`.** `npx` grabs whatever version is in its
> cache (this machine had 0.6.7 → 0.7.42 side by side); a scene that needs a registry block or adapter
> from a newer version then renders wrong or fails silently. The pinned binary is installed globally
> (`hyperframes --version` → **0.7.72**, at `/opt/homebrew/bin/hyperframes`). Re-pin with
> `npm install -g hyperframes@<ver>` and bump this line when you deliberately upgrade.
>
> **Verify the pin before a batch, not after.** Bumped 0.7.42 → 0.7.72 on 2026-07-26 after the
> messi-ai-investor build found the doc and the binary disagreed — scene 06 had been re-rendered on
> 0.7.72 while the other eleven were still 0.7.42 output. Mixed-version scenes in one master are a
> silent-difference risk, so when the pin moves, **re-render the whole batch, not just the scene you
> touched.**

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

### Step 6a — RENDER-FAILURE scan + GHOSTED-HOLD audit (two gates, not one)
```bash
python3 <skill>/tools/deadspace-scan.py <scene-render>.mp4   # near-black / blown-white
python3 <skill>/tools/deadspace-scan.py <MASTER>.mp4         # again on the master
python3 <skill>/tools/beatmap.py ghosts <scene>              # the ghosted-hold defect
```
> **CORRECTED 2026-07-26 (jarvis-tfo0.2).** Step 6a used to be a single photometric "dead-space"
> gate at `mean<22 or mean>234`. On the `#0A0E14` register that is broken: the Messi V2 master's
> *median* frame luma is **23.5** against a floor of **22**, so it flagged ~half the video — 28 runs
> on a good master. The axis was also inverted: genuinely dead frames measured 17.9–21.8 while the
> good frames it rejected measured 13.9–14.3. **Do not restore those thresholds.** Full evidence and
> the four ruled-out alternatives are in the `deadspace-scan.py` docstring and
> CITATION-CARD-FORMAT.md.

`deadspace-scan.py` now detects **render failure only** — a hole in the render, a white flash, a
missing asset — at floor 10 / ceiling 245. Zero hits on a healthy master, immediate on a real one.

The **ghosted-hold** defect (a panel present, content unresolved) is semantic and is caught
structurally from the build by `beatmap.py ghosts`: a ghost must resolve within **~1.2s**, and
anything resolving from below **0.40** opacity reads as absent rather than ghosted.

**Remedy:** raise the luminance FLOOR (lighter scrim, brighter bed, higher ghost opacity) or pull
the content in. **Never move a VO-anchored beat to satisfy a gate.**

### Step 6b2 — RE-RECORDED a scene's VO? Re-anchor with the tool, don't re-derive by hand
```bash
# ALWAYS keep the old transcript before overwriting it — it is what makes this possible
cp <scene>/assets/transcript.json <scene>/assets/transcript-preRERECORD.json
# ...drop in the new audio, re-transcribe, then:
python3 <skill>/tools/reanchor.py <scene> --old-transcript <scene>/assets/transcript-preRERECORD.json
python3 <skill>/tools/reanchor.py <scene> --old-transcript ... --write     # after reviewing
```
Every timeline position in these scenes is a bare number and there are **zero `tl.addLabel()` calls
across all 14**, so nothing records which word produced `15.28`. That is why the S10 re-record cost a
full production cycle. The positions *are* word-derived though — across 1417 of them, 85.7% sit within
0.20s of a word start — so the anchor is recoverable by aligning the old and new transcripts.

`reanchor.py` aligns the two word sequences (difflib; the takes tokenize differently, so positional
comparison is useless), builds a piecewise-linear old→new time map, and rewrites every position
through it. **Measured against the S10 ground truth — its pre-re-record HTML, old transcript and the
human's hand re-anchor all survive — median error 0.070s, 85.2% within 0.25s.**

> **It is an ASSIST, not an oracle.** The >1s deviations are beats the human moved *further than the
> take stretched* — content decisions the tool should not predict. Dry-run first, read the LOW-
> confidence list and the >1s deviations it prints, fix those by hand, then render and watch.
> It turns "re-derive 66 numbers" into "check a short list."

**Consequence for Step 1:** never overwrite `assets/transcript.json` on a re-record without keeping
the old one. It is the only record of what the timeline was anchored to.

### Step 6c — BEAT MAP: generate it FROM the build, don't maintain it beside the build
```bash
python3 <skill>/tools/beatmap.py check   <scene>          # drift gate — non-zero exit on drift
python3 <skill>/tools/beatmap.py render  <scene> --write  # regenerate the map from the timeline
python3 <skill>/tools/beatmap.py ghosts  <scene>          # audit the ghosted-placeholder device
python3 <skill>/tools/reconcile-assets.py <project> --write   # write back what the build chose
```
`beatmap.py` reads the timeline and emits `BEATMAP.json` + the HTML comment: clustered visual
events, their targets, the VO phrase each lands on (from `assets/transcript.json`), and a seeded
`DEN`/`ATM` tag per event with a runtime-weighted ratio against the 90/10 rule.

**Run `check` before every render and after every timeline edit.** Measured on the Messi V2 build
before this existed: the maps documented **171 of 671** visual events, scene coverage ranging 64%
down to 13%. That spread is why counting lines across two maps is meaningless and why S01 looked
sparse when it is the densest scene in the video.

> **`render --write` PRESERVES the authored half.** A machine can derive timings, targets and cues;
> it cannot derive semantic beat names, bed assignments, or the FACTS / RIGHTS / LIKENESS blocks.
> Those are carried through verbatim under `--- AUTHORED ---`. Two bugs during development silently
> dropped them from 7 of 14 scenes — including a likeness rule — and were caught only by diffing
> against backups. **Back up before a bulk `--write`, and diff after.**

> **The `DEN`/`ATM` tag is a SEED, not a verdict.** It classifies by target selector, so a beat whose
> abstract visual IS the content (S06's wireframe room teaching "spatial intelligence") mis-reads as
> atmospheric. Correct it by hand; treat `DEN%` as a floor because unknowns are unclassified.

`ghosts` inventories the signature device (§5 of CONDUIT-VISUAL-SYSTEM.md) — elements resting in the
0.05–0.60 opacity band that the timeline later resolves. Flags any resolving from **below 0.40**,
which reads as absent rather than ghosted. Class-based groups animated by id report as "permanent";
read that as "no direct resolve found", not proof.

`reconcile-assets.py` closes the loop one level up: ASSET-PLAN.md leaves forks open on purpose
("X.mp4 OR Y.mp4 — pick ONE") and the build's choice used to die at the bench. It reports referenced
/ unused / **missing** assets per scene and appends a RESOLVED section stating outcome next to intent.


Every scene's `index.html` opens with a `BEAT MAP` comment. It is the right artifact — timestamps, cue
phrases, bed assignments, FACTS/RIGHTS constraints — and on the Messi V2 build it had **drifted from
the scene in every direction**: the map described a design two revisions old (jersey `#30` / "THE
INVESTOR" where the render showed `#10` / "FORTUNE'S TENTH"), and two beats present in the scene were
absent from the map. Drift always runs one way — the scene improves, the doc doesn't.

Two rules:
1. **Fixed granularity.** One line per *visual event*, not per beat. Messi S07 documented sub-events
   (`6.35 axis draws · 7.00 chip A · 8.62 label`); S01 documented whole beats. Counting lines across
   the two produces a meaningless comparison — measure the render, not the plan.
2. **Classify every beat `DEN` or `ATM`** (CONDUIT-VISUAL-SYSTEM.md §6). ≥90% denotative. A scene that
   can't say which its beats are isn't planned.

**Write back after the build.** Decisions made during the build currently die there — unresolved
ASSET-PLAN forks ("office-collaboration OR happy-meeting"), and devices invented at the bench. The
strongest motion device in the reference build — *progressive disclosure with ghosted placeholders* —
appears throughout and was written down nowhere. A short reconciliation pass (what did we actually
pick, what did we invent) closes the loop.

### Step 6b — MANDATORY FRAME PASS (the automated layout gate is currently INERT)
**`scene-validator.py` is blind to layout defects**, and the tool that is *supposed* to cover them
**does not currently fire on our compositions.** Across one 4-video batch (2026-07-18) every scene agent
hit at least one of: overlapping labels / text-on-text, a caption cropped by a camera push-in, an inset
colliding with a label, a tag firing before its panel exited. ~25 such defects total. **Every single one
was found by a human-style look at frames.** A clean validator says the scene is *deterministic and
correctly timed* — it says nothing about whether the scene is *legible*.

> **Status of the automated gate (verified 2026-07-19, CLI 0.7.64).** `hyperframes check` has a Layout
> section (this is the old `hyperframes layout`, now a deprecated alias) with `--at-transitions` and
> `--samples=<n>`. On our scenes it reports **`Layout ◇ 0 issues across 0 sample(s)`** — zero samples —
> and `Contrast ◇ 0/0 text checks`, i.e. it is evaluating nothing. Confirmed on a scene with a KNOWN
> text-over-text collision, with `--at-transitions --samples=24`: still 0 samples, no detection.
> So the gate is real and documented but **inert in practice — do not rely on it.** If someone gets it
> sampling (>0 samples), it becomes the cheap first pass and the manual frame pass becomes the backstop.
> Until then the frame pass IS the gate.

So after each scene renders, extract frames at every major beat and LOOK at them:
```bash
for t in 3 8 13 20 28 36 44 52; do ffmpeg -v error -ss $t -i renders/<render>.mp4 -frames:v 1 frames/t${t}.png; done
```
Check each for: text over text · elements clipped by the frame or by a camera move · an inset landing
on a label · a panel that is empty when it should carry content · a beat that reveals before/after its
VO word. Fix and re-render. Do not report a scene as done on validator output alone.

### Step 6c — Transcript integrity (do this BEFORE anchoring, not after)
Whisper silently drops speech. In the same batch it dropped **7.4s** from one scene's
`assets/transcript.json` — every VO-anchored beat built on that file would have been wrong.
**There are TWO drop classes and you must screen for BOTH** — gap/density alone catches only the first,
and in this batch it produced a false "only one scene is corrupted" verdict while three more were broken:

1. **Gap drops** — the words vanish and leave a hole.
   - word density = `words / audio_duration * 60` → healthy ≈ **130–160 wpm**; **>15% below the project
     median** = suspect.
   - max inter-word gap **>2s** mid-scene (trailing silence at the tail is normal).
2. **Collapsed-token drops (invisible to the above)** — Whisper swallows the speech into ONE long token,
   so density looks near-normal and there is NO gap. Screen the token durations:
   - any token **>2.0s**, OR a short function word (`the`, `it`, `a`, ≤4 chars) **>1.0s**.
   - Real examples: a **3.36s `"the"`** hiding *"skipped is what happened next: Google and Meta"*; a
     **2.26s `"it"`** hiding the entire *"someone is going to lose a phenomenal amount"* Altman quote;
     a **4.4s `"a"`** hiding *"hyperscaler proudly breaks out an A-I revenue line."*
   - **Benign look-alikes — do not "fix" these:** spoken numerals (`"1999"`, `"1990s"`, `"34"`) and
     letter-by-letter acronyms (`"GPUs"` said G-P-Us) legitimately run 1.0–1.4s. Confirm against
     `VO-CLEAN.md` before repairing: print the transcript around the token and compare to the script.

**Repair:** re-transcribe that scene's `assets/audio.mp3` alone (a short clip beats a slice of a 9-min
take). If a plain retry comes back WORSE (it can — one retry went from a 2.26s drop to a 6.36s drop),
pass a **prompt hint** containing the expected phrasing with `temperature=0`:
```python
client.audio.transcriptions.create(model="whisper-1", file=f, response_format="verbose_json",
    timestamp_granularities=["word"], prompt="<expected sentences from VO-CLEAN.md>", temperature=0)
```
That recovered the full Altman quote (6.36s token → 0.74s). **Always re-scan after repairing** — never
assume the retry worked. Keep the bad file as `.bak-whisper-drop`.

## Step 6d — Today's Dispatch end-card (STANDARD final scene for 3-video sets)
For any video that is part of a daily **3-video set** (the default cadence — see the daily-ideas
"Today's Dispatch" block), the LAST scene is always the dispatch end-card. It names the day's set and
marks the other two "watch next", leaving the right side clear for YouTube's clickable end screens.
**Placement is load-bearing: it is the FINAL ~12s only — never during the hook** (retention-gated
channel; connection happens on the way out). Generate it per video with `--current` = which of the
three THIS video is:
```bash
python3 <skill>/tools/make-dispatch-endcard.py \
  --theme "<3-5 word through-line>" \
  --titles "Video A|Video B|Video C" \
  --current 1 \
  --dispatch-line "Today's dispatch: <one punchy sentence>" \
  --out <project>/hyperframes-v3/scenes/99-dispatch-endcard   # 99- so it sorts LAST
```
Copy the theme / titles / dispatch line straight from the daily-ideas email's "Today's Dispatch"
block. It emits a faceless-conduit scene (silent, all motion on the registered `tl`) — run it through
the **Step 6 validator** like any scene (`scene-validator.py`). Full contract + the end-screen /
playlist / pinned-comment connection stack: `references/DISPATCH-ENDCARD.md`. A one-off video (not
part of a set) skips this step.

## Step 7 — Assemble the master
Order scenes ascending by name, so the `99-dispatch-endcard` (Step 6c) lands LAST in the concat.
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
