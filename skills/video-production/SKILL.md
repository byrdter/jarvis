# Video Production Skill — Byrddynasty Long-Form Video Pipeline

> **LEGACY / SPECIAL CASE:** This is the older HeyGen + Remotion + talking-avatar pipeline. For current Jarvis/Byrddynasty faceless videos, use `.agents/skills/jarvis-video-production/SKILL.md` instead. Keep this skill for intentional avatar/talking-head or legacy Remotion maintenance work only.

**Purpose:** Take a HeyGen MP4 (with 1-second silences between scenes and any Nano Banana images baked in) and produce a finished Byrddynasty long-form video using a single Remotion project that respects per-segment avatar position.

**Status:** **PROVEN.** First successful production run was Video 8 (Phase 8: The Second Brain Gets Sharper), shipped 2026-04-30. Reference example lives at `Byrddynasty-Videos/video-8-phase-8/` (or wherever Video 8's project sits).

**Read this skill at the start of any task that involves:**
- Producing a Byrddynasty long-form video from a HeyGen recording
- Modifying or extending the Remotion project for a new video
- Adding a new visual component kind or style
- Debugging timing, avatar position, or rendering issues

---

## Critical learnings from Video 8 — read these first

1. **Stay in terminal. Don't hand off to CC Desktop.** Both run on the same Claude model — the "advantage" of CC Desktop was illusory. The disadvantage is that every handoff loses session context, and you end up re-explaining the project state every time. The user said it bluntly: *"It seems since we are communicating directly, the transitions in the videos are smoothly and not so herky-jerky."* Stay in the same terminal session from script through final render.

2. **Silence detection alone is unreliable.** ffmpeg `silencedetect` at `d=0.92` will catch in-sentence pauses as false positives, shifting all downstream segment boundaries by one. Always validate with **whisper-cpp word-level transcription** by matching opener phrases. See "Verifying segment boundaries" below.

3. **Avatar position has to be done in Remotion, not HeyGen.** HeyGen renders the avatar in one fixed position per scene; it does NOT automatically reposition the avatar per segment based on the script's composition modes (BR-C, SR, SL, etc.). The Remotion `Main.tsx` orchestrator must scale and position the `<OffthreadVideo>` element per segment via the `getVideoStyle(composition)` function. The Remotion graphic renders BEHIND the video; the video's positioned style is the avatar zone.

4. **The recording's segment count may not match the script.** Script seg 29 ("Phase 8 shipped...") was merged into seg 28's CTA during Video 8's recording. Verify segment count via Whisper transcription before authoring.

5. **The whole tool palette idea (Remotion + HyperFrames + Motion Canvas + ExcaliMotion + VHS + Playwright + Nano Banana) was over-engineering.** What works is much simpler: **HeyGen audio + baked-in static images + one monolithic Remotion project**. HyperFrames is integratable (see "Adding HyperFrames clips" below) but optional.

---

## Canonical project layout

Every video lives in `Byrddynasty-Videos/<episode>/` with this structure:

```
video-N-<theme>/
├── 01-script/
│   ├── SCRIPT-AND-PLAN.md          # master script + segment plan (composition, tool, imagery per segment)
│   ├── VO-ONLY.md                  # clean voiceover-only document for HeyGen recording
│   ├── IMAGE-PROMPTS.md            # Nano Banana prompts for static-image segments
│   └── (optional) REMOTION-PRODUCTION-PROMPT.md  # only if using CC Desktop — skip if staying in terminal
├── 02-heygen/
│   ├── heygen-source.mp4           # the recorded HeyGen video (1920×1080, 25fps, ~1s silences between scenes)
│   └── _OLD_*.mp4                  # any superseded recordings (keep as backup)
├── 09-stills/                      # Nano Banana PNGs for image segments
│   ├── 002-segment.png
│   ├── 013-segment.png
│   └── ...
├── 03-remotion/                    # Remotion project — the heart of the pipeline
│   ├── public/
│   │   └── heygen-source.mp4       # symlink or copy of 02-heygen/heygen-source.mp4
│   ├── src/
│   │   ├── index.ts
│   │   ├── Root.tsx                # Composition registry (durationInFrames, fps, 1920×1080)
│   │   ├── Main.tsx                # ★ orchestrator with getVideoStyle(composition) — the most important file
│   │   ├── segmentContent.ts       # segments array — content per segment (kind, style, data, composition, timing)
│   │   ├── types.ts
│   │   └── compositions/
│   │       ├── AnimatedText.tsx    # 3 styles (title / body / highlight)
│   │       └── customSegments.tsx  # 19 specialized component kinds (NumberedBadges, WikiConflict, Flowchart, etc.)
│   ├── package.json
│   ├── tsconfig.json
│   └── out/
│       └── video.mp4               # final render
└── 10-output/
    └── segment-timings.json        # corrected boundaries from whisper-cpp
```

---

## End-to-end workflow

### 1. Write the script + segment plan

`01-script/SCRIPT-AND-PLAN.md` — for each segment, specify:
- **Segment number, title, duration estimate, voiceover text**
- **Composition** (FS / FS-G / BR-C / BR-S / BL-C / BL-S / SL / SR / CS — see vocabulary below)
- **Imagery** — what the graphic shows (or "image" if it's a static segment)

Authoring rules:
- Voice: collective "we" only — never "I". (Avatar speaks for a collective, not one person.) Contractions follow: "we're", "we've", etc.
- Final two segments: **CTA** (Subscribe/Comment/Share) + **emotional close**. Can be merged in HeyGen recording (V8 did this), but plan them as two distinct segments in the script.
- Static images sparingly: 4–7 per long-form video is typical. Reserve for diagrams, roadmaps, dense reference images. Motion-graphics is the default.

### 2. Generate Nano Banana image prompts (for image segments)

For each segment marked as a static image:
- Write a detailed prompt (`01-script/IMAGE-PROMPTS.md`) with brand palette, exact text labels, layout instructions
- Specify: 1920×1080 landscape, Byrddynasty colors (`#0F172A` navy / `#00D4FF` cyan / `#FFD700` gold / `#FFFFFF` white)
- Save outputs to `09-stills/NNN-segment.png` (3-digit segment number, the user's preferred convention)

User generates the images in Nano Banana Pro and drops them in `09-stills/`.

### 3. Generate VO-only document (for HeyGen recording)

`01-script/VO-ONLY.md` — strip everything except the voiceover text. One block per segment. Header reminds the recorder of:
- Exactly 1 second of silence between every segment (this is non-negotiable — it's the segmentation marker)
- One segment at a time, in order

### 4. User records HeyGen with images baked in

User opens HeyGen, creates a 16:9 project, records the 28–29 segments with the static images placed on the segments that need them. HeyGen renders to MP4. User drops the MP4 in `02-heygen/heygen-source.mp4`.

### 5. Detect timings — silence detection PLUS Whisper validation

```bash
# Initial silence detection (will have false positives — don't trust alone)
ffmpeg -i 02-heygen/heygen-source.mp4 -af silencedetect=n=-50dB:d=0.92 -f null - 2>&1 | grep silence_start
```

Then validate with whisper-cpp:

```bash
# Extract audio
ffmpeg -i 02-heygen/heygen-source.mp4 -ar 16000 -ac 1 -c:a pcm_s16le -y /tmp/audio.wav

# Transcribe with word-level timestamps
whisper-cli -m ~/.whisper-models/ggml-base.en.bin -f /tmp/audio.wav --output-json --output-file /tmp/transcript -ml 1
```

Then write a Python script that maps script segment opener phrases ("Quick recap", "Phase 7 caught", "Here's a real one", etc.) to actual timestamps in the transcript. **The Whisper-derived starts are the source of truth.** Ignore silence boundaries that don't correspond to a script-segment opener — those are in-sentence pauses that ffmpeg misclassified.

Whisper transcription gotchas:
- Numbers may render as words: "phase eight" not "phase 8"
- Contractions split: "Here's" → "Here" + "'s" — strip apostrophes when matching
- Match on the first 3-5 distinctive words of each segment opener

Write the corrected `10-output/segment-timings.json` with 28–29 entries (matching the actual recording, not the script).

### 6. Author / update the Remotion project

If this is a **new flavor** of video (e.g., first Phase-9 video), copy `video-8-phase-8/03-remotion/` as a starting template, then update:
- `Root.tsx` — `TOTAL_FRAMES = ceil(totalDuration * fps)`
- `segmentContent.ts` — entries for each segment (kind, style, data, composition, timing)
- (rarely) `customSegments.tsx` — add a NEW component kind only if no existing kind fits

If this is a **subsequent video** of an established flavor, just update `segmentContent.ts` with new content + timings.

`Main.tsx` should usually need NO modification — its `getVideoStyle(composition)` table handles all 9 composition modes already.

### 7. Test render a couple of segments first

```bash
cd 03-remotion
npx remotion render src/index.ts Main out/test-segN.mp4 --frames=START-END --concurrency=4
```

Pick a non-trivial segment (e.g., a side-shifted one + an image segment). Verify:
- Avatar position respects composition mode
- Graphic doesn't collide with avatar zone
- Image segments pass through cleanly with no Remotion overlay

### 8. Full render

```bash
cd 03-remotion
rm -f out/video.mp4
npx remotion render src/index.ts Main out/video.mp4 --concurrency=4
```

Takes 30–60 minutes for a 13-minute video on Apple Silicon. Run in background.

### 9. Spot-check the final render

Extract frames at key timestamps (one per composition type) into a contact sheet, review, and iterate. Common iteration: tweak component sizing, kill unwanted overlays, adjust labels.

---

## The composition mode → avatar position vocabulary

This is the contract `Main.tsx::getVideoStyle()` implements. Every voiceover segment's `composition` field maps to an `<OffthreadVideo>` style. Any new composition mode requires updating `getVideoStyle`.

| Composition | Avatar render | Graphic area |
|---|---|---|
| `FS` | Full 1920×1080 | None — graphic only renders if `kind` is in `FS_GRAPHIC_ON_TOP_KINDS` (lower-third, badges, etc.) |
| `FS-G` | Hidden (`display: none`) | Full 1920×1080 — image-only segment |
| `BR-C` | 384×384 circle PiP, bottom-right, 20px from edges, 3px cyan border | Whole frame except bottom-right ~420×420 |
| `BR-S` | Same as BR-C but rounded square (24px radius) | Same |
| `BL-C` / `BL-S` | Mirror of BR-C/BR-S to bottom-left | Whole frame except bottom-left ~420×420 |
| `SL` | 640×1080, left third | Right two-thirds (x=640..1920) |
| `SR` | 640×1080, right third | Left two-thirds (x=0..1280) |
| `CS` | 600×900 centered (top=90, left=660) with rounded corners | Around the center column — corners and edges only |

For image segments (`type: 'image'`), the avatar scaling is irrelevant — Remotion just plays the HeyGen MP4 full-screen and renders no overlay (the image is already baked into the video).

---

## Component library — what exists (no need to rebuild)

`AnimatedText.tsx` provides 3 visual styles:
- **title** — purple/blue gradient, cyan text, diagonal grid, 30 particles, corner brackets. For phase intros, hero moments.
- **body** — dark navy gradient, white text, vertical grid, 20 particles, side accent line. For explanations.
- **highlight** — teal/green gradient, gold text, dual grid, 30 gold particles, geometric corners. For key takeaways, lists, stats.

`customSegments.tsx` provides 19 specialized component kinds (V8 used all of them):

| Kind | Used for | Example segment in V8 |
|---|---|---|
| `lower-third` | TV-bug-style title sweep at end of FS segment | Seg 1 (PHASE 8 lower-third) |
| `numbered-badges` | One-of-three numbered points appearing left-side, replacing previous | Seg 7 (Phase 8: three additions) |
| `wiki-conflict` | Two wiki page mockups + lightning bolt + CONTRADICTION | Seg 4 (pages disagree) |
| `silo-bridge` | Two clouds of concepts + dashed-line bridge that completes | Seg 5 (knowledge silos) |
| `queue-list` | Scrolling list of color-coded queue items (red/yellow/green) | Seg 6 (queue full of obvious fixes) |
| `three-phase` | Three-phase animated reveal (string-match → LLM read → semantic match) | Seg 8 (contradiction concept) |
| `flowchart` | Boxes connected with cyan particle trails, branching diamond | Seg 9 (how it works) |
| `terminal` | Mock-terminal recording with monospace cyan-on-dark, scrolling | Seg 10, 16 (demos) |
| `bridge-clusters` | Four wiki clusters at corners + cross-cluster bridge animation | Seg 11 (cross-wiki concept) |
| `sketched-bridge` | Two sketched-feel cards with hand-drawn highlight circles + arc between them | Seg 12 (bridge example) |
| `card-sort` | Stack of proposal cards animating into LOW/MEDIUM/HIGH risk buckets | Seg 14 (auto-apply concept) |
| `risk-table` | Three-row table with color bands + stacked bar showing % split | Seg 15 (risk tiers detail) |
| `loop-diagram` | Three-node circular loop with audio-reactive node pulses (DEPRECATED — V8 didn't use; was removed in seg 17) | (removed) |
| `daily-timeline` | Horizontal timeline with time markers + icons | Seg 19 (daily schedule) |
| `cost-dashboard` | Big numerals with counting animation + dollar particles | Seg 20 (cost) |
| `live-queue` | Mock app UI with URL bar, filter pill, queue rows, hover effects | Seg 21 (live queue) |
| `apply-cards` | Three vertical card reveals with title + fields + AUTO-APPLIED badge | Seg 22 (specific examples) |
| `orbiting` | Avatar centered, four large icons + labels orbiting around (CS composition) | Seg 23 (compounding effect) |
| `verb-sweeps` | Faint verbs sweep across at low opacity over avatar | Seg 27 (vision close) |
| `end-card` | SUBSCRIBE button + comment chips + SHARE arrow | Seg 28 (CTA) |
| `none` | No graphic — pure FS avatar | Seg 17, 29 (hero/close moments) |

**Adding a new kind:** create a new exported React component in `customSegments.tsx`, add a `case` to `renderSegment()` in `Main.tsx`, add the kind name to the `SegmentSpec` union in `types.ts`. If it's an FS segment with the graphic on top (rare), also add the kind to `FS_GRAPHIC_ON_TOP_KINDS` in `Main.tsx`.

---

## Brand defaults

**Colors:**
- Background dark navy `#0F172A`
- Primary cyan `#00D4FF`
- Secondary gold `#FFD700`
- Success green `#10B981`
- Warning yellow `#F59E0B`
- Error red `#EF4444`
- Text white `#FFFFFF`

**Spring physics defaults:**
```typescript
title:     { damping: 15, stiffness: 100, mass: 1 }
body:      { damping: 20, stiffness: 80,  mass: 1 }
highlight: { damping: 12, stiffness: 120, mass: 1 }
```

**Animation timing:**
- Entrance: first 1.0–1.2s of segment (spring physics)
- Hold: middle (continuous animations — particles, grid drift, glow pulses)
- Exit: last 0.5s (scale + fade)

---

## Adding HyperFrames clips (optional, when needed)

For effects HyperFrames does well that Remotion struggles with — hand-drawn scribble reveals, audio-reactive beat-sync, sketched-feel diagrams:

1. Render the HyperFrames composition standalone to MP4 (`npx hyperframes render` in a HyperFrames project)
2. Drop the MP4 into `03-remotion/public/clips/segment-NN-hyperframes.mp4`
3. In `segmentContent.ts`, set `kind: 'hyperframes-clip'` with `data: { src: 'clips/segment-NN-hyperframes.mp4' }`
4. Add a `HyperFramesClip` component to `customSegments.tsx` that renders the clip via `<OffthreadVideo>` over the appropriate area (full-screen for FS-G, side-third for SL/SR, etc.)
5. Add a `case 'hyperframes-clip'` to `renderSegment()` in `Main.tsx`

Treat HyperFrames as additive. Default to Remotion components; reach for HyperFrames only when a specific segment genuinely needs it.

---

## Common gotchas (debug recipes)

| Symptom | Likely cause | Fix |
|---|---|---|
| Remotion graphic landing on Nano Banana image segment | Image segment not classified `type: 'image'` in segmentContent | Verify type field; image segments need `kind: 'none'` and `type: 'image'` |
| Avatar covered by Remotion graphic on every segment | `Main.tsx` `getVideoStyle()` not respecting composition; or `<OffthreadVideo>` rendered before graphic | Verify graphic renders FIRST (background), `<OffthreadVideo>` SECOND (on top, positioned per `getVideoStyle`) |
| Segment N+1's graphic appears during segment N's image | Silence detection false positive (in-sentence pause caught as boundary), shifting all downstream timings | Re-run with whisper-cpp + opener-phrase matching; rebuild `segment-timings.json` |
| Avatar looks tiny in PiP showing room/desk visible | Expected — HeyGen renders avatar full-screen; PiP scaling shrinks the whole frame proportionally. Live with it or instruct user to record HeyGen with avatar tighter in frame |
| Number/icon overlapping avatar's face | The overlay layout was designed assuming avatar is in a corner, but avatar is full-screen because composition is FS | Reposition to LEFT or RIGHT side at mid-height (see V8 seg 7's NumberedBadges fix) |
| Text "very light" or hard to read | Opacity too low (<0.6), or color too close to background. | Bump to opacity 1.0, add `textShadow` with strong contrast, increase fontSize |
| Render time too long | Default concurrency=1 | Use `--concurrency=4` (or higher on bigger machines) |

---

## Realistic cadence

| Phase | Time per video |
|---|---|
| Script + segment plan | 1–2 hr |
| Image prompts + generation (Nano Banana) | 30–60 min |
| HeyGen recording + image bake-in | 30–60 min |
| Whisper transcription + timing JSON | 5–10 min (automated in same session) |
| Remotion authoring (mostly content updates) | 15–30 min |
| Test render + full render | 30–60 min |
| Spot-check + iterate on issues | 15–60 min |
| **Total** | **3–6 hours per video** |

Realistic cadence: **1–2 videos per week comfortably; 3+ if scripts are pre-written**. The first video of a new flavor takes longer because of new component kinds; the second video of that flavor is fast.

---

## Reference example

`Byrddynasty-Videos/video-8-phase-8/` is the canonical reference. Every file structure decision and component pattern in this skill came from that production. Read its files before authoring a new video — they're the most up-to-date examples.

Tools required (verify these are installed before starting a new video):
- `ffmpeg` and `ffprobe` (Homebrew)
- `whisper-cpp` (Homebrew) + `~/.whisper-models/ggml-base.en.bin`
- Node + npm (for Remotion)
- Bun (used elsewhere in JARVIS, not strictly required for the Remotion project)
