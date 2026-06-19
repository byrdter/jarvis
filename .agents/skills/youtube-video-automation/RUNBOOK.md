# YouTube Video Automation Runbook

Step-by-step execution guide for producing YouTube videos with the automated workflow.

## Before You Start

**Time estimate:** 2-4 hours (setup + automation + review)

**You'll need:**
- [ ] HeyGen video file (`.mp4` with avatar speaking)
- [ ] Episode brief (target runtime, thesis, visual register preferences)
- [ ] Channel DESIGN.md (colors, fonts, branding rules)
- [ ] Asset catalog populated (at least 10-15 B-roll options)
- [ ] Node.js ≥22, FFmpeg, Python 3.10+ installed

## Quick Start (For Returning Users)

If you've done this before and just need a reminder:

```bash
cd video-XX-name
./scripts/extract-vo.sh heygen-raw.mp4 .
python3 scripts/generate-scene-plan.py --transcript assets/transcript.json --brief episode-brief.md --output visual-treatment-board.md
# → Review visual-treatment-board.md
python3 scripts/resolve-assets.py --treatment visual-treatment-board.md --manifest ../asset-library/MANIFEST.json --output asset-resolution-report.md
python3 scripts/build-hyperframes-scenes.py --treatment visual-treatment-board.md --transcript assets/transcript.json --design DESIGN.md --output-dir scenes/
# → Render all scenes
python3 tools/scene-validator.py . --frames
.agents/skills/jarvis-video-production/scripts/build-master.sh .
python3 tools/master-qa.py master.mp4
```

For first-time users or when something goes wrong, follow the detailed guide below.

---

## Part 1: Project Setup (15-20 minutes)

### Step 1.1: Create Project Directory

```bash
cd ~/Library/CloudStorage/Dropbox/jarvis-private/video-production
mkdir video-XX-name  # Replace XX with video number, name with kebab-case title
cd video-XX-name
```

### Step 1.2: Initialize Structure

```bash
mkdir -p scenes assets analysis tools scripts
```

**Expected structure:**
```
video-XX-name/
  scenes/          # HyperFrames scene compositions
  assets/          # Shared assets (audio, transcript, etc.)
  analysis/        # VO analysis, keyword extraction
  tools/           # Validation scripts (symlink or copy)
  scripts/         # Automation scripts (symlink or copy)
  DESIGN.md        # Visual identity
  episode-brief.md # Target runtime, thesis, visual preferences
```

### Step 1.3: Create Episode Brief

Create `episode-brief.md`:

```markdown
# Video XX: [Title]

## Thesis
One-sentence summary of what this video argues/explains.

## Target Audience
Who is this for? What do they already know?

## Target Runtime
- Minimum: 8 minutes (480s)
- Ideal: 10-15 minutes (600-900s)

## Visual Register Preferences
From PRESENTATION-VARIETY.md, which registers should dominate?
- Real tool screenshots (high)
- Code/terminal action (medium)
- Documentary B-roll (low)
- Data visualization (high)
- ... etc.

## Production Risks
What might block this video?
- Missing specific B-roll?
- Complex animations?
- Source proof needed?

## Beads Issue
- Issue ID: #XXX (create before starting work)
```

### Step 1.4: Verify Channel Design Exists

Check if `DESIGN.md` exists in project root or create it:

```bash
# Option A: Use existing channel design
cp ../byrddynasty/DESIGN.md .

# Option B: Create new design from style preset
# (Requires reading ~/.claude/skills/hyperframes/visual-styles.md)
```

**DESIGN.md must include:**
- Style prompt (mood, tone)
- Colors (3-5 hex values with roles)
- Typography (1-2 font families)
- What NOT to Do (3-5 anti-patterns)

### Step 1.5: Place HeyGen Video

Copy or move your raw HeyGen video into the project:

```bash
cp ~/Downloads/heygen-export-2026-06-18.mp4 heygen-raw.mp4
```

**Verify the video:**
```bash
ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name heygen-raw.mp4
```

Expected output:
- Video stream: h264 or similar
- Audio stream: aac or mp3
- Duration: >60 seconds

---

## Part 2: Extract & Analyze VO (5-10 minutes)

### Step 2.1: Run Extract Script

```bash
.agents/skills/youtube-video-automation/scripts/extract-vo.sh heygen-raw.mp4 .
```

**What this does:**
1. Extracts audio: `ffmpeg -i heygen-raw.mp4 -vn -acodec copy assets/audio.mp3`
2. Transcribes with word-level timestamps: `npx hyperframes transcribe assets/audio.mp3`
3. Analyzes speaking pace, pauses, keywords → `analysis/vo-analysis.json`

**Expected output:**
```
✓ Extracted audio → assets/audio.mp3 (12.3 MB)
✓ Transcribed → assets/transcript.json (2,847 words)
  - Duration: 596.3s (9m 56s)
  - Speaking pace: 171 words/min
  - Natural pauses: 23 (≥1.5s silence)
✓ Keyword analysis → analysis/vo-analysis.json
  - Top keywords: automation (18), AI (42), workers (15), augment (12)
```

### Step 2.2: Review Transcript

Open `assets/transcript.json` and skim for:
- Accuracy (any major transcription errors?)
- Natural pauses (good scene break points)
- Duration (does it hit target runtime?)

**If transcript has errors:**
```bash
# Re-transcribe with Whisper large model (slower, more accurate)
npx hyperframes transcribe assets/audio.mp3 --model large-v3
```

### Step 2.3: Check VO Analysis

Open `analysis/vo-analysis.json`:

```json
{
  "duration_seconds": 596.3,
  "word_count": 2847,
  "words_per_minute": 171,
  "natural_pauses": [
    { "timestamp": 27.4, "duration": 2.1 },
    { "timestamp": 68.9, "duration": 1.8 },
    ...
  ],
  "top_keywords": {
    "automation": 18,
    "AI": 42,
    "workers": 15,
    "augment": 12,
    "replace": 9
  }
}
```

**Validation:**
- ✓ Duration ≥480s (8 min minimum)
- ✓ Speaking pace 140-180 WPM (ideal for educational content)
- ✓ Natural pauses every 20-40 seconds (good scene break cadence)

**If any validation fails:**
- Duration too short? → Add outro, examples, or deeper explanations
- Speaking too fast (>200 WPM)? → Regenerate HeyGen with slower pace
- No natural pauses? → Rewrite script with intentional breaths

---

## Part 3: Generate Scene Plan (30-45 minutes)

### Step 3.1: Run Scene Plan Generator

```bash
python3 .agents/skills/youtube-video-automation/scripts/generate-scene-plan.py \
  --transcript assets/transcript.json \
  --brief episode-brief.md \
  --output visual-treatment-board.md
```

**What this does:**
1. Segments transcript at natural pauses
2. Extracts VO summary per segment
3. Identifies keywords for B-roll matching
4. Assigns visual register (from PRESENTATION-VARIETY.md)
5. Determines avatar vs B-roll timing
6. Applies variety gate (≥6 registers, no more than 3 consecutive same)

**Expected output:**
```
✓ Segmented transcript into 8 scenes
✓ Applied variety gate: 7 registers used, max 2 consecutive same
✓ Generated visual treatment board → visual-treatment-board.md
```

### Step 3.2: Review Visual Treatment Board

Open `visual-treatment-board.md` and review each scene:

**Check for:**
- [ ] VO summary matches transcript content
- [ ] Keywords are relevant and specific
- [ ] Visual register is appropriate (not all cards/text)
- [ ] Avatar timing makes sense (avatar for intro/outro, B-roll for middle)
- [ ] Scene pacing specified (quick-cut vs breath)
- [ ] Assets needed are listed

**Example scene (well-formed):**
```markdown
## Scene 03: The Automation Dilemma (27.2s)

**VO Summary:** "62% of workers believe their company is trying to augment them, not replace them. But 34% see automation as a threat to their jobs."

**Keywords:** automation, augment, replace, workers, jobs, statistics

**Visual Register:** Data Visualization Beats

**Avatar Timing:** None (full B-roll)

**B-roll Plan:**
- 0-8s: Fork road visual (automation vs augmentation choice)
- 8-15s: Bar chart comparing 62% vs 34% statistics
- 15-22s: Office workers at desks (documentary B-roll)
- 22-27s: Transition graphic (fork returns to unified path)

**Scene Pacing:** Medium (one visual change every 5-7s)

**Assets Needed:**
- `fork-road` (semantic key)
- `office-workers-typing` (semantic key)
- Generated: bar chart with 62/34 split

**Approval:** [ ] Pending
```

### Step 3.3: Edit and Approve Scenes

**Common edits:**
- Merge scenes that are too short (<10s)
- Split scenes that are too long (>40s)
- Adjust visual register if too repetitive
- Refine asset semantic keys to be more specific

**Mark approved scenes:**
```markdown
**Approval:** [x] Approved by Terry
```

---

## Part 4: Resolve Assets (15-20 minutes)

### Step 4.1: Run Asset Resolver

```bash
python3 .agents/skills/youtube-video-automation/scripts/resolve-assets.py \
  --treatment visual-treatment-board.md \
  --manifest ../asset-library/MANIFEST.json \
  --output asset-resolution-report.md
```

**What this does:**
1. Extracts semantic keys from visual treatment board
2. Queries `MANIFEST.json` for matching assets
3. Ranks by keyword match score
4. Validates files exist and meet requirements
5. Reports missing assets as blockers

**Expected output:**
```
✓ Resolved 14 / 16 semantic keys
✗ Missing 2 assets:
  - fork-road-transition (scene 03) — no close match found
  - decision-matrix-3d (scene 07) — no close match found

Suggested actions:
  1. Generate missing assets with Runway/Higgsfield
  2. Use alternative assets from catalog
  3. Simplify scene to use available assets
```

### Step 4.2: Review Asset Resolution Report

Open `asset-resolution-report.md`:

```markdown
# Asset Resolution Report

## Resolved (14 assets)

| Semantic Key | Resolved Path | Match Score | Duration | Resolution |
|--------------|---------------|-------------|----------|------------|
| office-workers-typing | b-roll/office-typing--silent.mp4 | 0.92 | 12.5s | 1920x1080 |
| claude-desktop | products/claude-code/desktop/ClaudeCodeDesktop.png | 1.00 | N/A | 3584x2240 |
| ...

## Missing (2 assets)

| Semantic Key | Scene | Suggested Alternatives |
|--------------|-------|------------------------|
| fork-road-transition | 03 | Use `fork-road` (static) + GSAP path animation |
| decision-matrix-3d | 07 | Generate with Runway using prompt: "3D decision matrix..." |

## Recommendations

1. **Approve alternatives**: Replace missing assets with suggested alternatives
2. **Generate new assets**: Use Runway/Higgsfield for specific needs
3. **Update MANIFEST.json**: Add new assets to catalog after generation
```

### Step 4.3: Handle Missing Assets

**Option A: Use alternative assets**
```bash
# Edit visual-treatment-board.md
# Replace `fork-road-transition` with `fork-road` + animation note
```

**Option B: Generate new assets**
```bash
# Use Runway to generate specific clip
# (See Runway prompt suggestions in asset-resolution-report.md)
```

**Option C: Simplify scenes**
```bash
# Rewrite scene to use only available assets
```

### Step 4.4: Re-run Resolver (if changes made)

```bash
python3 .agents/skills/youtube-video-automation/scripts/resolve-assets.py \
  --treatment visual-treatment-board.md \
  --manifest ../asset-library/MANIFEST.json \
  --output asset-resolution-report.md
```

**Must pass:** 100% resolved (0 missing assets)

---

## Part 5: Build HyperFrames Scenes (20-30 minutes)

### Step 5.1: Run Scene Builder

```bash
python3 .agents/skills/youtube-video-automation/scripts/build-hyperframes-scenes.py \
  --treatment visual-treatment-board.md \
  --transcript assets/transcript.json \
  --design DESIGN.md \
  --output-dir scenes/
```

**What this does:**
1. For each scene in visual treatment board:
   - Creates HyperFrames project: `scenes/NN-scene-name/`
   - Generates `index.html` composition
   - Copies resolved assets to `scenes/NN-scene-name/assets/`
   - Generates GSAP timeline with VO-anchored timing
   - Applies DESIGN.md colors, fonts, branding

**Expected output:**
```
✓ Generated 8 HyperFrames scenes
  - 01-introduction (avatar + lower-third)
  - 02-the-problem (B-roll + text overlays)
  - 03-automation-dilemma (B-roll + data viz)
  - 04-solution-overview (B-roll + animated diagram)
  - 05-technical-details (code + terminal + screenshots)
  - 06-real-world-example (screenshot + web-roll)
  - 07-decision-matrix (3D viz + comparison)
  - 08-conclusion (avatar + end card)
```

### Step 5.2: Lint All Scenes

```bash
for scene in scenes/*; do
  echo "Linting $scene..."
  cd "$scene"
  npx hyperframes lint
  cd ../..
done
```

**Must pass:** All scenes lint clean (0 errors)

**Common lint errors:**
- Missing `data-composition-id`
- Overlapping tracks
- Unregistered timeline
- Animation scheduled past composition end

**Fix errors before proceeding.**

### Step 5.3: Preview Sample Scenes

Pick 2-3 scenes to preview in browser:

```bash
cd scenes/03-automation-dilemma
npx hyperframes preview
# → Opens http://localhost:3002
```

**Check for:**
- [ ] Colors match DESIGN.md
- [ ] Text is legible (not too small, good contrast)
- [ ] Animations land on correct timing
- [ ] No layout overflow or overlap
- [ ] Assets loaded correctly

**If preview looks wrong:**
- Edit `index.html` directly
- Re-lint: `npx hyperframes lint`
- Refresh browser

---

## Part 6: Render Scenes (30-60 minutes)

### Step 6.1: Render All Scenes

```bash
for scene in scenes/*; do
  scene_name=$(basename "$scene")
  echo "Rendering $scene_name..."
  cd "$scene"
  npx hyperframes render --output "renders/${scene_name}_$(date +%Y-%m-%d_%H-%M-%S).mp4"
  cd ../..
done
```

**Render settings** (automatic via HyperFrames):
- Codec: H.264
- Resolution: 1920x1080
- Frame rate: 30fps
- Audio: AAC 192kbps

**Expected time:** 2-5 minutes per scene (depending on duration and complexity)

**Watch for errors:**
- FFmpeg failures (missing codec, corrupted source)
- Out of memory (scenes with complex WebGL)
- Timeline sync issues (animations past composition end)

### Step 6.2: Verify Renders

```bash
for scene in scenes/*; do
  latest=$(ls -t "$scene/renders"/*.mp4 | head -1)
  echo "Checking $latest..."
  ffprobe -v error -show_entries format=duration "$latest"
done
```

**All scenes should have:**
- Duration matching `hyperframes.json` ±0.5s
- Video stream (h264)
- Audio stream (aac)
- File size >0 bytes

---

## Part 7: QA Validation (15-20 minutes)

### Step 7.1: Run Scene Validator

```bash
python3 .agents/skills/youtube-video-automation/tools/scene-validator.py .
```

**What this checks:**
- Duration validation (rendered vs declared)
- Audio stream presence
- Lint pass (HyperFrames structure)
- Scene count vs visual treatment board

**Expected output:**
```
🔍 validating scenes in video-XX-name

  ✓ 01-intro      01-intro_2026-06-18_14-23-11.mp4 — exp 18.5s / got 18.48s (Δ0.02s)
  ✓ 02-problem    02-problem_2026-06-18_14-26-42.mp4 — exp 32.1s / got 32.08s (Δ0.02s)
  ✓ 03-dilemma    03-dilemma_2026-06-18_14-29-15.mp4 — exp 27.2s / got 27.24s (Δ0.04s)
  ...

📊 total runtime: 596.3s (9m 56s)
✅ all scenes valid
```

### Step 7.2: Run Frame Analysis

```bash
python3 .agents/skills/youtube-video-automation/tools/scene-validator.py . --frames
```

**What this checks:**
- Blank screen detection (low variance frames)
- Scene duration pacing (no >5s static holds)
- End-of-scene visual gaps

**If errors found:**
```
  ❌ 03-dilemma — blank screen at 72.0s (survey results section)
     Fix: Add bar chart animation at BT.4 (72-74s)
  
  ⚠️  05-details — static hold for 6.2s without change
     Fix: Add subtle parallax or camera push during hold
```

**Fix errors:**
1. Edit `scenes/XX-name/index.html`
2. Re-lint: `npx hyperframes lint`
3. Re-render
4. Re-run validator with `--frames`

### Step 7.3: Watch Key Scenes

Use the `/watch` skill to verify critical scenes:

```bash
# Watch intro
python3 ~/.claude/skills/watch/scripts/watch.py scenes/01-intro/renders/01-intro_latest.mp4

# Watch a middle scene
python3 ~/.claude/skills/watch/scripts/watch.py scenes/04-solution/renders/04-solution_latest.mp4

# Watch conclusion
python3 ~/.claude/skills/watch/scripts/watch.py scenes/08-conclusion/renders/08-conclusion_latest.mp4
```

**Check for:**
- Avatar motion smooth (no jitter)
- B-roll matches VO content
- Text appears at right moments
- Transitions are clean
- Audio synced to visuals

---

## Part 8: Concatenate Master (5 minutes)

### Step 8.1: Lock Scene Takes (Optional)

If you've iterated on specific scenes and want to pin the best take:

```bash
# Example: lock scene 03's best take
echo "03-dilemma_2026-06-18_15-42-33.mp4" > scenes/03-dilemma/renders/LOCKED
```

**Without LOCKED files:** build-master.sh uses most recent render by mtime.

### Step 8.2: Validate Before Concat

```bash
.agents/skills/jarvis-video-production/scripts/validate-scenes.sh .
```

**Must pass:** 0 problems before proceeding.

### Step 8.3: Build Master

```bash
.agents/skills/jarvis-video-production/scripts/build-master.sh .
```

**What this does:**
1. Collects all scene renders (respecting LOCKED files)
2. Generates ffmpeg concat list
3. Re-encodes for codec consistency (H.264 CRF 18)
4. Writes `master.mp4`
5. Generates `master.mp4.manifest.json`

**Expected output:**
```
📂 V14 master build — video-XX-name

  ✓ 01-intro      01-intro_2026-06-18_14-23-11.mp4 (18.48s) [latest]
  ✓ 02-problem    02-problem_2026-06-18_14-26-42.mp4 (32.08s) [latest]
  ✓ 03-dilemma    03-dilemma_2026-06-18_15-42-33.mp4 (27.24s) [🔒 LOCKED]
  ...

🔧 ffmpeg concat (re-encoded for codec consistency)...

✅ master.mp4 — 596.3s (238 MB)
✅ Within V14 ideal range (10–15 min).
📋 wrote master.mp4.manifest.json
```

---

## Part 9: Final QA (10-15 minutes)

### Step 9.1: Run Master QA

```bash
python3 .agents/skills/youtube-video-automation/tools/master-qa.py master.mp4 \
  --sample-interval 30 \
  --output final-qa-report.json
```

**What this checks:**
- Total runtime ≥480s (8 min)
- Zero blank screens
- Scene transitions clean (no flash frames)
- Audio stream present and synced
- Resolution 1920x1080
- Codec H.264 / AAC

**Expected output:**
```
🔍 Final QA: master.mp4

✓ Runtime: 596.3s (9m 56s) — within ideal range
✓ Resolution: 1920x1080
✓ Codec: h264 / aac
✓ Blank screen check: 0 issues (sampled 20 frames)
✓ Transition check: all clean
✓ Audio sync: ±0.08s max drift

📊 Quality Score: 98/100
✅ PASSED — ready for upload

📋 Report: final-qa-report.json
```

### Step 9.2: Watch Master Samples

```bash
# Intro (first 30s)
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30

# Middle (5 minutes in)
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325

# Ending (last 30s)
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 565 --end 596
```

**Final check:**
- [ ] Intro avatar smooth (not jittery)
- [ ] B-roll scenes engaging (not generic)
- [ ] Text legible on mobile (simulate with small window)
- [ ] Audio clear and synced
- [ ] Ending doesn't cut mid-word
- [ ] No unexpected blank frames

### Step 9.3: Generate Publishing Package

Create `YOUTUBE-PUBLISH.md`:

```markdown
# Video XX: [Title] — Publishing Package

## Title Options
1. [Primary option — 60-70 chars with keywords]
2. [Alternative 1]
3. [Alternative 2]

## Description
[Full YouTube description with timestamps, links, sources]

## Chapters
0:00 Introduction
0:32 The Problem
1:08 The Automation Dilemma
...

## Thumbnail Brief
[Description of what thumbnail should show]

## Tags
[Comma-separated YouTube tags]

## Sources
- [Source 1 with URL]
- [Source 2 with URL]
...

## Upload Checklist
- [ ] Title finalized
- [ ] Description written
- [ ] Thumbnail created
- [ ] master.mp4 uploaded
- [ ] Chapters added
- [ ] End screen configured
- [ ] Visibility set (public/unlisted)
```

---

## Troubleshooting

### "Extract-vo.sh fails: command not found"

**Cause:** Script not found or not executable.

**Fix:**
```bash
# Make scripts executable
chmod +x .agents/skills/youtube-video-automation/scripts/*.sh

# Or run with bash explicitly
bash .agents/skills/youtube-video-automation/scripts/extract-vo.sh heygen-raw.mp4 .
```

### "Transcribe fails: Whisper API error"

**Cause:** HyperFrames transcribe requires Whisper API key or local Whisper.

**Fix:**
```bash
# Use local Whisper (slower but free)
npx hyperframes transcribe assets/audio.mp3 --local

# OR set Whisper API key
export OPENAI_API_KEY="sk-..."
npx hyperframes transcribe assets/audio.mp3
```

### "Scene validator reports missing hyperframes.json"

**Cause:** Scene was not initialized with `npx hyperframes init`.

**Fix:**
```bash
cd scenes/XX-problem-scene
npx hyperframes init . --non-interactive
# Then re-generate scene HTML
```

### "Lint error: data-composition-id required"

**Cause:** Root `<div>` missing `data-composition-id` attribute.

**Fix:**
Edit `index.html`:
```html
<!-- WRONG -->
<div>...</div>

<!-- RIGHT -->
<div data-composition-id="03-automation-dilemma" data-width="1920" data-height="1080">
  ...
</div>
```

### "Render produces blank video"

**Cause:** Assets not copied to scene folder OR `<template>` used on root composition.

**Fix:**
```bash
# 1. Verify assets exist
ls scenes/XX-name/assets/

# 2. Check index.html for <template> wrapper (should NOT exist on root)
head -5 scenes/XX-name/index.html
```

### "Master concat fails: No such file or directory"

**Cause:** No rendered `.mp4` files in `scenes/*/renders/`.

**Fix:**
```bash
# Render all scenes first
for scene in scenes/*; do
  cd "$scene"
  npx hyperframes render
  cd ../..
done
```

### "QA reports blank screens at transition points"

**Cause:** Scene endings don't hold final frame OR scene transitions have timing gaps.

**Fix:**
1. Check scene HTML: final frame should hold ≥0.5s before composition ends
2. Verify `data-duration` matches actual content duration
3. Re-render scene with adjusted timing

---

## Common Pitfalls

### ❌ Skipping visual treatment board
Jumping straight to HyperFrames scene generation without a plan leads to mismatched timing and wrong B-roll.

**Fix:** Always complete visual-treatment-board.md and get approval before building scenes.

### ❌ Not locking good takes
Rendering new iterations without locking previous good takes → build-master.sh picks wrong version.

**Fix:** Create `scenes/XX-name/renders/LOCKED` file pointing to best take.

### ❌ Using Math.random() in compositions
Non-deterministic code → every render produces different output.

**Fix:** Use seeded PRNG (mulberry32) or static values.

### ❌ Forgetting to copy assets to scene folders
HyperFrames file server doesn't follow symlinks → broken renders.

**Fix:** Always copy assets into `scenes/*/assets/` (scripts do this automatically).

### ❌ Not running QA before concat
Concatenating scenes with blank screens or timing issues → entire master needs rework.

**Fix:** Always run `scene-validator.py --frames` before build-master.sh.

---

## Next Steps After Completion

1. **Upload to YouTube** (use YOUTUBE-PUBLISH.md)
2. **Update asset catalog** if new reusable B-roll was created
3. **Close beads issues** for this video
4. **Push to git** (session close protocol)
5. **Update SKILL.md** if you discovered new patterns or anti-patterns

---

**Estimated Total Time:** 2-4 hours

- Setup: 15-20 min
- VO extraction: 5-10 min
- Scene planning: 30-45 min
- Asset resolution: 15-20 min
- Scene building: 20-30 min
- Rendering: 30-60 min
- QA validation: 15-20 min
- Concatenation: 5 min
- Final QA: 10-15 min

**Manual steps:** ~1-1.5 hours  
**Automated:** ~1-2.5 hours  
**Ratio:** 40% manual, 60% automated
