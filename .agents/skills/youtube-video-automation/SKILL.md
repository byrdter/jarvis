---
name: youtube-video-automation
description: Automated YouTube video production from HeyGen raw video to final master.mp4. Automates transcript extraction, B-roll selection, HyperFrames scene generation, timing synchronization, concatenation, and QA verification. Eliminates manual debugging of blank screens, timing drift, and asset selection. Use when producing long-form educational/promotional videos (8-15 minutes) with HeyGen avatar segments and pre-recorded B-roll.
---

# YouTube Video Automation

This skill automates the complete production pipeline from HeyGen raw video to final YouTube-ready `.mp4`, eliminating manual debugging of blank screens, timing issues, and B-roll selection.

## When to Use This Skill

**Trigger conditions:**
- User provides a HeyGen video file and wants a complete YouTube video
- User asks to "automate video production" or "build a YouTube video"
- User references the "YouTube video workflow" or "automated video pipeline"
- User wants to add B-roll, transitions, and polish to raw HeyGen footage

**This skill is NOT for:**
- Creating HeyGen videos from scratch (use HeyGen API/interface first)
- One-off scene edits (use hyperframes skill directly)
- Avatar-only videos without B-roll (HeyGen output is already final)
- Short-form content <3 minutes (manual editing is faster)

## Prerequisites

Before running this skill, ensure:

1. **HeyGen video exists**: Raw `.mp4` file with avatar speaking
2. **Asset catalog populated**: B-roll, screenshots, web-rolls cataloged with metadata
3. **Project structure ready**: Episode folder with command center initialized
4. **Visual identity defined**: DESIGN.md or channel style guide exists

If any prerequisite is missing, this skill will guide you to complete it first.

## Workflow Overview

```
Input: HeyGen video (.mp4)
  ↓
[1] Extract & Analyze VO → transcript.json (word-level timestamps)
  ↓
[2] Generate Scene Plan → visual-treatment-board.md (VO → B-roll mapping)
  ↓
[3] Select Assets → Resolve semantic keys from asset catalog
  ↓
[4] Build HyperFrames Scenes → Generate HTML compositions per segment
  ↓
[5] Render Scenes → Individual .mp4 files per scene
  ↓
[6] Run QA Validation → Detect blank screens, timing issues, sync problems
  ↓
[7] Concatenate Master → Stitch scenes into master.mp4
  ↓
[8] Final QA Report → Frame analysis, duration check, quality gates
  ↓
Output: master.mp4 + QA report + manifest
```

## Detailed Steps

### Step 1: Extract & Analyze VO

**Input:** HeyGen video file (`heygen-raw.mp4`)

**Process:**
1. Extract audio stream: `ffmpeg -i heygen-raw.mp4 -vn -acodec copy audio.mp3`
2. Transcribe with word-level timestamps: `npx hyperframes transcribe audio.mp3`
3. Analyze transcript for:
   - Natural pauses (for scene breaks)
   - Keyword density (for B-roll matching)
   - Total duration (for runtime validation)
   - Speaking pace (words per minute)

**Output:**
- `assets/audio.mp3` — extracted audio
- `assets/transcript.json` — word-level timestamps
- `analysis/vo-analysis.json` — speaking pace, pauses, keywords

**Example transcript.json structure:**
```json
{
  "words": [
    { "text": "Welcome", "start": 0.12, "end": 0.58 },
    { "text": "to", "start": 0.62, "end": 0.78 },
    { "text": "artificial", "start": 0.82, "end": 1.32 },
    { "text": "intelligence", "start": 1.36, "end": 2.08 }
  ],
  "duration": 596.3
}
```

### Step 2: Generate Scene Plan

**Input:** 
- `assets/transcript.json`
- Episode brief (target runtime, thesis, visual register preferences)

**Process:**
1. Segment transcript into natural scenes (based on pauses, topic shifts)
2. For each segment:
   - Extract VO summary (what's being said)
   - Identify keywords for B-roll matching
   - Determine visual register (from PRESENTATION-VARIETY.md)
   - Specify avatar vs B-roll timing
   - Calculate duration from transcript timestamps

3. Apply variety gate:
   - Ensure ≥6 registers across episode
   - No more than 3 consecutive scenes with same register
   - Include at least one quick-cut montage
   - Include at least one 4-6 second breath

**Output:** `visual-treatment-board.md`

**Example scene entry:**
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

### Step 3: Select Assets

**Input:**
- `visual-treatment-board.md` (semantic keys for needed assets)
- `asset-library/MANIFEST.json` (catalog of available assets)

**Process:**
1. For each semantic key in visual treatment:
   - Query MANIFEST.json for matching assets
   - Rank by keyword match score
   - Validate file exists and is accessible
   - Check duration (for video B-roll)
   - Check resolution (prefer 1920x1080 or higher)

2. For missing assets:
   - Log as blocker with description
   - Suggest Runway/Higgsfield prompts for generation
   - OR flag for user to provide/approve alternatives

3. Copy resolved assets to scene folders:
   ```bash
   cp asset-library/b-roll/office-typing--silent.mp4 scenes/03-automation-dilemma/assets/
   ```

**Output:**
- `asset-resolution-report.md` (which assets resolved, which are missing)
- Populated `scenes/*/assets/` directories

**Asset selection algorithm:**
```python
def select_broll(keywords, catalog, duration_needed):
    # 1. Semantic matching
    candidates = []
    for asset in catalog:
        score = keyword_match_score(keywords, asset.tags + asset.description)
        if score > 0.3:  # threshold
            candidates.append((asset, score))
    
    # 2. Duration filtering (for video B-roll)
    candidates = [c for c in candidates if c[0].duration >= duration_needed]
    
    # 3. Rank by score
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Return top match
    return candidates[0][0] if candidates else None
```

### Step 4: Build HyperFrames Scenes

**Input:**
- `visual-treatment-board.md` (scene plan)
- `assets/transcript.json` (VO timing)
- Resolved assets in `scenes/*/assets/`
- Channel `DESIGN.md` (colors, fonts, brand rules)

**Process:**

For each scene:

1. **Initialize scene structure:**
   ```bash
   npx hyperframes init scenes/03-automation-dilemma --non-interactive
   ```

2. **Generate composition HTML** using these patterns:

**A. Avatar scenes** (HeyGen video visible):
```html
<div data-composition-id="03-automation-dilemma" data-width="1920" data-height="1080">
  <!-- Avatar video (from HeyGen, trimmed to this scene's segment) -->
  <video id="avatar" data-start="0" data-duration="27.2" data-track-index="0" 
         src="assets/heygen-segment.mp4" muted playsinline></video>
  
  <!-- Audio (same source, not muted) -->
  <audio id="vo" data-start="0" data-duration="27.2" data-track-index="2" 
         src="assets/heygen-segment.mp4"></audio>
  
  <!-- Lower-third branding (animated in/out) -->
  <div class="lower-third">
    <img src="assets/logo.png" class="logo">
    <span class="channel-name">Byrddynasty - Understanding AI</span>
  </div>
  
  <style>/* CSS from DESIGN.md */</style>
  <script>/* GSAP timeline from transcript timestamps */</script>
</div>
```

**B. B-roll scenes** (full coverage, no avatar):
```html
<div data-composition-id="03-automation-dilemma" data-width="1920" data-height="1080">
  <!-- Background B-roll video -->
  <video id="broll" data-start="0" data-duration="27.2" data-track-index="0"
         src="assets/office-typing.mp4" muted playsinline data-media-start="3"></video>
  
  <!-- Audio (from HeyGen VO, extracted per-scene) -->
  <audio id="vo" data-start="0" data-duration="27.2" data-track-index="2"
         src="assets/vo-segment.mp3"></audio>
  
  <!-- Animated text overlays (timed to VO) -->
  <div class="stat-card">
    <div class="stat-number">62%</div>
    <div class="stat-label">Believe in augmentation</div>
  </div>
  
  <div class="stat-card">
    <div class="stat-number">34%</div>
    <div class="stat-label">Fear automation</div>
  </div>
  
  <style>/* CSS from DESIGN.md */</style>
  <script>
    // VO-anchored timing from transcript.json
    const tl = gsap.timeline({ paused: true });
    
    // Stat 1 appears when VO says "62 percent" (at 8.4s based on transcript)
    tl.from(".stat-card:nth-child(1)", { 
      y: 60, opacity: 0, duration: 0.6, ease: "power3.out" 
    }, 8.4);
    
    // Stat 2 appears when VO says "34 percent" (at 15.2s based on transcript)
    tl.from(".stat-card:nth-child(2)", { 
      y: 60, opacity: 0, duration: 0.6, ease: "power3.out" 
    }, 15.2);
    
    // Both exit together before scene ends
    tl.to(".stat-card", { 
      y: -40, opacity: 0, duration: 0.5, ease: "power2.in", stagger: 0.1 
    }, 25);
    
    window.__timelines["03-automation-dilemma"] = tl;
  </script>
</div>
```

3. **Critical timing rules** (from VO-anchored timing memory):
   - ✅ Every animation `at` value MUST come from `transcript.json` word timestamps
   - ❌ NEVER use `tl.timeScale()` to stretch authored visuals
   - ✅ If VO is too short/long, REWRITE visual timing — don't squeeze
   - ✅ Scene changes every ≤5 seconds (new visual element or motion)
   - ❌ No blank screens (every second must have visual content)

4. **Lint before rendering:**
   ```bash
   cd scenes/03-automation-dilemma
   npx hyperframes lint
   ```

### Step 5: Render Scenes

**Input:** HyperFrames compositions in `scenes/*/`

**Process:**
```bash
for scene in scenes/*; do
  cd "$scene"
  npx hyperframes render --output renders/$(basename $scene)_$(date +%Y-%m-%d_%H-%M-%S).mp4
  cd ../..
done
```

**Output:** Rendered `.mp4` files in `scenes/*/renders/`

**Render settings (baked into hyperframes render):**
- Codec: H.264
- Resolution: 1920x1080
- Frame rate: 30fps
- Audio: AAC 192kbps 48kHz

### Step 6: Run QA Validation

**Input:** Rendered scene `.mp4` files

**Process:**

Run validation on each scene:
```bash
python3 tools/scene-validator.py <project-dir>
python3 tools/scene-validator.py <project-dir> --frames
```

**Validation checks:**

**A. Duration validation:**
- Rendered duration matches `hyperframes.json` duration ±0.5s
- Total episode runtime ≥480s (8 min minimum)
- Prefer 600-900s (10-15 min ideal)

**B. Blank screen detection:**
```python
def detect_blank_screens(video_path, sample_interval=1.0):
    """Sample frames every 1 second, flag low-variance frames"""
    frames = extract_frames(video_path, interval=sample_interval)
    blank_segments = []
    
    for i, frame in enumerate(frames):
        variance = frame.var()  # pixel variance
        if variance < 10:  # threshold for "blank" (solid color)
            timestamp = i * sample_interval
            blank_segments.append({
                "timestamp": timestamp,
                "variance": variance,
                "severity": "critical"
            })
    
    return blank_segments
```

**C. Audio sync check:**
- VO audio stream present
- Audio duration matches video duration ±0.1s
- No silence >2 seconds (unless intentional breath)

**D. Scene duration check:**
```python
def validate_scene_pacing(scenes):
    """Ensure scene changes every ≤5 seconds"""
    violations = []
    
    for scene in scenes:
        if scene.duration > 5 and scene.visual_changes == 0:
            violations.append({
                "scene": scene.name,
                "duration": scene.duration,
                "issue": "No visual change for >5 seconds"
            })
    
    return violations
```

**E. Text legibility check:**
- No text split mid-letters
- No adjacent words joined
- Font sizes ≥32px for body text
- Headlines ≥72px
- Safe margins respected (no overflow)

**F. HyperFrames lint:**
```bash
npx hyperframes lint --json
```
- No missing `data-composition-id`
- No overlapping tracks
- All timelines registered
- No `tl.call()` (kills timeline)
- No animations scheduled past composition end

**Output:** `qa-report.json`

**Example QA report:**
```json
{
  "timestamp": "2026-06-18T22:45:00Z",
  "project": "video-01-the-choice",
  "total_scenes": 8,
  "passed": 6,
  "failed": 2,
  "warnings": 3,
  "issues": [
    {
      "scene": "02-strategic-fork",
      "type": "blank_screen",
      "severity": "critical",
      "timestamp": 72.0,
      "description": "Blank screen detected at 1:12 during survey results section",
      "fix": "Add bar chart animation at BT.4 (72-74s)"
    },
    {
      "scene": "05-decision-matrix",
      "type": "scene_duration",
      "severity": "warning",
      "duration": 6.2,
      "description": "Static hold for 6.2s without visual change",
      "fix": "Add subtle parallax or camera push during hold"
    },
    {
      "scene": "master",
      "type": "runtime",
      "severity": "info",
      "total_duration": 596.3,
      "target_min": 600,
      "description": "Runtime 596.3s (9:56) — within acceptable range"
    }
  ],
  "assets": {
    "total": 42,
    "missing": 0,
    "low_quality": 1
  }
}
```

### Step 7: Concatenate Master

**Input:**
- Validated scene renders in `scenes/*/renders/`
- Optional `LOCKED` files to pin specific takes

**Process:**
```bash
.agents/skills/jarvis-video-production/scripts/validate-scenes.sh <project-dir>
.agents/skills/jarvis-video-production/scripts/build-master.sh <project-dir>
```

**How scene selection works:**
1. If `scenes/XX/renders/LOCKED` exists → use that filename
2. Otherwise → use most recent `.mp4` by mtime

**Concatenation:**
```bash
# Generate concat list
for scene in scenes/*-pilot; do
  chosen=$(get_locked_or_latest "$scene/renders")
  echo "file '$(realpath $chosen)'" >> concat-list.txt
done

# Concat with re-encode for codec consistency
ffmpeg -f concat -safe 0 -i concat-list.txt \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  master.mp4
```

**Output:**
- `master.mp4` — final concatenated video
- `master.mp4.manifest.json` — scene list with timestamps

### Step 8: Final QA Report

**Input:** `master.mp4`

**Process:**

Run final validation pass:
```bash
# Frame analysis (sample every 30s)
python3 tools/master-qa.py master.mp4 --sample-interval 30

# Duration check
ffprobe -v error -show_entries format=duration master.mp4

# Watch key moments
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325  # middle
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 565 --end 596  # end
```

**Validation checklist:**
- [ ] Runtime ≥480s (8 min minimum)
- [ ] Zero blank screens detected
- [ ] Scene changes every ≤5 seconds
- [ ] Audio stream present and synced
- [ ] Intro avatar smooth (no jitter)
- [ ] Transition points clean (no flash frames)
- [ ] Ending holds briefly (not cut mid-word)
- [ ] Resolution 1920x1080
- [ ] Codec H.264 / AAC

**Output:** `final-qa-report.md`

## Asset Catalog Schema

The asset catalog uses a JSON manifest at `asset-library/MANIFEST.json`.

**Full schema:** See [ASSET-CATALOG-SCHEMA.md](ASSET-CATALOG-SCHEMA.md)

**Key fields:**
```json
{
  "version": "1.0",
  "roots": {
    "asset_library": ".",
    "video_assets": "../video-assets"
  },
  "brains": { /* brain icons, colors */ },
  "screenshots": { /* product screenshots with metadata */ },
  "broll": [
    {
      "id": "office-typing",
      "path": "b-roll/office-typing--silent.mp4",
      "type": "video",
      "duration": 12.5,
      "resolution": "1920x1080",
      "keywords": ["office", "typing", "productivity", "work", "desk"],
      "description": "Close-up of hands typing on laptop in modern office",
      "variants": {
        "silent": "office-typing--silent.mp4",
        "audio": "office-typing--audio.mp4"
      },
      "usage": "unrestricted",
      "source": "Pexels",
      "added": "2026-06-01"
    }
  ],
  "screenshots": { /* web screenshots with annotations */ },
  "generated": { /* Runway/Higgsfield clips */ }
}
```

**Search API (concept):**
```python
def search_assets(query_keywords, asset_type=None, min_duration=None):
    """
    Query asset catalog by keywords.
    
    Args:
        query_keywords: List of keywords to match
        asset_type: Filter by 'video', 'image', 'screenshot', etc.
        min_duration: Minimum duration for video assets (seconds)
    
    Returns:
        List of assets ranked by keyword match score
    """
    results = []
    for asset in catalog:
        if asset_type and asset.type != asset_type:
            continue
        if min_duration and asset.duration < min_duration:
            continue
        
        score = keyword_match_score(query_keywords, asset.keywords + [asset.description])
        if score > 0.3:
            results.append((asset, score))
    
    return sorted(results, key=lambda x: x[1], reverse=True)
```

## Quality Gates (Auto-Enforced)

These checks run automatically during the workflow. If any fail, the pipeline stops with actionable error messages.

### Gate 1: Input Validation
- HeyGen video file exists and is readable
- Video has both video and audio streams
- Duration >60 seconds (too short for this workflow)

### Gate 2: Asset Resolution
- All semantic keys from visual treatment board resolve to existing files
- No missing assets (blocks scene generation)
- Asset durations sufficient for scene requirements

### Gate 3: Scene Lint
- All HyperFrames compositions pass `npx hyperframes lint`
- No missing `data-composition-id`
- No timeline registration errors
- No animations scheduled past composition end

### Gate 4: Render Validation
- Every scene renders successfully (no ffmpeg errors)
- Rendered duration matches declared duration ±0.5s
- No blank/corrupted output files

### Gate 5: QA Pass
- Zero blank screens detected
- All scene durations ≤5 seconds OR have motion/changes
- Audio sync verified (no drift >0.2s)
- Text legibility check passed

### Gate 6: Master Validation
- Concatenation succeeds
- Master duration = sum of scene durations ±1s
- Final runtime ≥480s (8 min minimum)
- Watch samples at intro/middle/end confirm quality

## Anti-Patterns (Never Do This)

From accumulated video production learnings:

### ❌ Don't use timeScale() to stretch visuals
**Why:** Linear scaling cannot match non-uniform speech pacing. Visuals drift 1-3 seconds from VO.

**Right:** Pin every animation to transcript word timestamps.

### ❌ Don't leave blank screens
**Why:** YouTube retention drops instantly on blank frames.

**Right:** Every second must have visual content (avatar, B-roll, text overlay, transition graphic).

### ❌ Don't hold static visuals >5 seconds
**Why:** Viewers perceive it as frozen/broken video.

**Right:** Add motion (parallax, camera push, text fade, object scale) or change scene.

### ❌ Don't use generic B-roll
**Why:** Weak visual connection to VO content = low engagement.

**Right:** Select B-roll with high keyword match score OR generate specific clips with Runway/Higgsfield.

### ❌ Don't skip the visual treatment board
**Why:** Generating scenes without a plan leads to mismatched timing, wrong B-roll, and rework.

**Right:** Always create visual-treatment-board.md BEFORE building HyperFrames scenes.

### ❌ Don't reference assets outside scene folders
**Why:** HyperFrames file server doesn't follow symlinks.

**Right:** Copy assets into `scenes/*/assets/` folders.

### ❌ Don't use Math.random() or Date.now() in compositions
**Why:** Non-deterministic → every render produces different output.

**Right:** Use seeded PRNG (mulberry32) or static values.

## Tools and Scripts

This skill provides these automation tools:

### 1. `scripts/extract-vo.sh`
Extracts audio and generates transcript from HeyGen video.

```bash
./scripts/extract-vo.sh heygen-raw.mp4 output-dir
# → output-dir/audio.mp3
# → output-dir/transcript.json
```

### 2. `scripts/generate-scene-plan.py`
Generates visual-treatment-board.md from transcript.

```bash
python3 scripts/generate-scene-plan.py \
  --transcript assets/transcript.json \
  --brief episode-brief.md \
  --output visual-treatment-board.md
```

### 3. `scripts/resolve-assets.py`
Resolves semantic keys to actual files from MANIFEST.json.

```bash
python3 scripts/resolve-assets.py \
  --treatment visual-treatment-board.md \
  --manifest asset-library/MANIFEST.json \
  --output asset-resolution-report.md
```

### 4. `scripts/build-hyperframes-scenes.py`
Generates HyperFrames HTML compositions from visual treatment + transcript.

```bash
python3 scripts/build-hyperframes-scenes.py \
  --treatment visual-treatment-board.md \
  --transcript assets/transcript.json \
  --design DESIGN.md \
  --output-dir scenes/
```

### 5. `tools/scene-validator.py`
Validates rendered scenes for QA issues.

```bash
python3 tools/scene-validator.py <project-dir>
python3 tools/scene-validator.py <project-dir> --frames
python3 tools/scene-validator.py <project-dir> --fix  # auto-fix safe issues
```

### 6. `tools/master-qa.py`
Final QA pass on concatenated master.mp4.

```bash
python3 tools/master-qa.py master.mp4 --sample-interval 30 --output qa-report.json
```

## Example End-to-End Run

```bash
# 1. Set up project
cd video-01-the-choice
mkdir -p scenes assets analysis

# 2. Extract VO
./scripts/extract-vo.sh heygen-raw.mp4 .
# → assets/audio.mp3
# → assets/transcript.json

# 3. Generate scene plan
python3 scripts/generate-scene-plan.py \
  --transcript assets/transcript.json \
  --brief episode-brief.md \
  --output visual-treatment-board.md

# 4. Review and approve visual treatment
# (Manual step: Terry reviews visual-treatment-board.md)

# 5. Resolve assets
python3 scripts/resolve-assets.py \
  --treatment visual-treatment-board.md \
  --manifest ../asset-library/MANIFEST.json \
  --output asset-resolution-report.md

# 6. Build HyperFrames scenes
python3 scripts/build-hyperframes-scenes.py \
  --treatment visual-treatment-board.md \
  --transcript assets/transcript.json \
  --design DESIGN.md \
  --output-dir scenes/

# 7. Render all scenes
for scene in scenes/*; do
  cd "$scene"
  npx hyperframes render --output renders/$(basename $scene).mp4
  cd ../..
done

# 8. Run scene QA
python3 tools/scene-validator.py .
python3 tools/scene-validator.py . --frames

# 9. Fix any issues (if validator found problems)
# (Manual step or auto-fix with --fix flag)

# 10. Concatenate master
.agents/skills/jarvis-video-production/scripts/build-master.sh .

# 11. Final QA
python3 tools/master-qa.py master.mp4 --sample-interval 30

# 12. Watch key moments
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325
```

**Total time:** ~2-4 hours (depending on scene count and render time)

**Manual steps:**
- Visual treatment approval (10-20 min)
- Issue fixing if QA fails (varies)
- Final watch/approval (15-30 min)

**Everything else:** Automated

## Maintenance

After every shipped video using this skill:

1. **Update asset catalog** if new reusable B-roll was created
2. **Document new patterns** if you solved a novel timing/visual problem
3. **Update anti-patterns** if you discovered a new failure mode
4. **Improve scripts** if manual steps could be automated
5. **Update SKILL.md** so future videos inherit the improvement

## Related Skills

- `hyperframes` — HyperFrames composition authoring (loaded automatically)
- `hyperframes-cli` — HyperFrames CLI commands (loaded automatically)
- `gsap` — GSAP animation patterns (loaded automatically)
- `jarvis-video-production` — Canonical faceless video workflow (superset)
- `hyperframes-video-director` — Visual direction standards (superset)
- `byrddynasty-video-v14` — V14-specific patterns (reference)

## Success Metrics

A video produced with this skill is successful when:

✅ Zero blank screens detected in QA  
✅ All scene changes ≤5 seconds  
✅ Audio-visual sync perfect (no drift >0.2s)  
✅ Runtime 8-15 minutes (minimum 8, prefer 10-15)  
✅ Visual variety: ≥6 registers used  
✅ Asset catalog search found appropriate B-roll for ≥80% of scenes  
✅ Manual intervention required ≤3 times during workflow  
✅ Final QA pass on first render (no rework needed)  

If any metric fails, investigate the root cause and update this skill.
