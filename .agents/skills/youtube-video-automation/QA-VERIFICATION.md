# QA Verification System

Automated quality assurance for YouTube video production. Detects blank screens, timing drift, audio sync issues, and scene pacing problems before manual review.

## Overview

The QA system runs in multiple stages:

1. **Scene-level validation** (during production) — Lint, duration, structure
2. **Post-render validation** (after scene renders) — Frame analysis, blank detection
3. **Pre-concat validation** (before master build) — All scenes pass QA
4. **Master validation** (after concat) — Final checks, sample watching

## Tools

### 1. `tools/scene-validator.py`

Validates HyperFrames scenes for structural and timing issues.

**Usage:**
```bash
python3 tools/scene-validator.py <project-dir>                 # Lint + structure checks
python3 tools/scene-validator.py <project-dir> --frames        # Add frame analysis
python3 tools/scene-validator.py <project-dir> --fix           # Auto-fix safe issues
python3 tools/scene-validator.py <project-dir> --json          # Machine-readable output
```

**What it checks:**

#### A. Lint Pass
- `npx hyperframes lint` on every scene
- No missing `data-composition-id`
- No overlapping tracks
- All timelines registered correctly
- No `tl.call()` (timeline killers)

#### B. Duration Validation
- Rendered duration matches `hyperframes.json` duration ±0.5s
- Scene duration ≥3 seconds (too short is likely an error)
- Total episode runtime ≥480s (8 min minimum)

#### C. Audio Stream Check
- Every rendered scene has an audio stream
- Audio duration matches video duration ±0.1s

#### D. Asset Validation
- All referenced assets exist
- No broken paths or 404s
- Asset durations sufficient for scene requirements

#### E. Frame Analysis (`--frames` flag)

Samples rendered video frames to detect:

**Blank screens:**
```python
def detect_blank_screens(video_path, sample_interval=1.0, variance_threshold=10):
    """
    Extract frames at sample_interval, compute pixel variance.
    Low variance = solid color = likely blank screen.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(0, frame_count, int(fps * sample_interval)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale and compute variance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        variance = gray.var()
        
        if variance < variance_threshold:
            timestamp = i / fps
            frames.append({
                "timestamp": timestamp,
                "variance": variance,
                "severity": "critical" if variance < 5 else "warning"
            })
    
    cap.release()
    return frames
```

**Scene duration violations:**
```python
def check_scene_pacing(scenes, max_static_duration=5.0):
    """
    Ensure no scene holds static for >5 seconds without motion.
    """
    violations = []
    
    for scene in scenes:
        static_holds = find_static_segments(scene.video_path)
        
        for hold in static_holds:
            if hold.duration > max_static_duration:
                violations.append({
                    "scene": scene.name,
                    "timestamp": hold.start,
                    "duration": hold.duration,
                    "severity": "warning" if hold.duration < 7 else "error"
                })
    
    return violations
```

**Example output:**
```
🔍 Scene Validator: video-XX-name

✓ Lint: All scenes passed
✓ Duration: All scenes within ±0.5s tolerance
✓ Audio: All scenes have audio streams

⚠️  Frame Analysis Issues:
  
  Scene 02-strategic-fork:
    ❌ BLANK SCREEN at 72.0s (variance: 3.2)
       Context: During survey results VO segment
       Fix: Add bar chart animation at BT.4 (72-74s)
  
  Scene 05-decision-matrix:
    ⚠️  STATIC HOLD 6.2s (at 24.5s)
       Context: Matrix display after build completes
       Fix: Add subtle parallax or camera push during hold

📊 Summary:
  - Total scenes: 8
  - Passed: 6
  - Issues: 2 critical, 1 warning
  - Total runtime: 596.3s (9m 56s)

❌ FAILED — Fix issues before concat
```

### 2. `tools/master-qa.py`

Final validation on concatenated `master.mp4`.

**Usage:**
```bash
python3 tools/master-qa.py master.mp4 --sample-interval 30 --output qa-report.json
```

**What it checks:**

#### A. File Integrity
- Video stream present (codec, resolution, frame rate)
- Audio stream present (codec, bitrate, sample rate)
- Duration >0
- File size >0

#### B. Runtime Validation
- Total duration ≥480s (8 min minimum)
- Preferred 600-900s (10-15 min)
- Not excessively long (>1800s / 30 min)

#### C. Blank Screen Scan
Same algorithm as scene-validator, but samples entire master at intervals.

#### D. Transition Check
Sample frames around concat points (between scenes) to detect:
- Flash frames (sudden brightness spike)
- Black frames at joins
- Audio glitches (silence or pops)

```python
def check_transitions(master_path, scene_manifest):
    """
    Sample ±1s around each scene boundary.
    """
    issues = []
    scene_times = get_scene_timestamps(scene_manifest)
    
    for i in range(len(scene_times) - 1):
        transition_point = scene_times[i]["end"]
        
        # Sample frames at transition ±1s
        before_frames = extract_frames(master_path, transition_point - 1, transition_point)
        after_frames = extract_frames(master_path, transition_point, transition_point + 1)
        
        # Check for flash frames
        for frame in before_frames + after_frames:
            brightness = frame.mean()
            if brightness > 240 or brightness < 15:
                issues.append({
                    "type": "flash_frame",
                    "timestamp": frame.timestamp,
                    "brightness": brightness
                })
        
        # Check for audio glitches
        audio_sample = extract_audio_segment(master_path, transition_point - 0.5, transition_point + 0.5)
        if has_audio_glitch(audio_sample):
            issues.append({
                "type": "audio_glitch",
                "timestamp": transition_point
            })
    
    return issues
```

#### E. Watch Samples

Auto-generates watch commands for key moments:
```bash
# Intro
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30

# Middle
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325

# Ending
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 565 --end 596
```

**Example output:**
```
🔍 Master QA: master.mp4

✓ File Integrity:
  - Video: h264, 1920x1080, 30fps
  - Audio: aac, 192kbps, 48kHz
  - Duration: 596.3s (9m 56s)
  - Size: 238 MB

✓ Runtime: 596.3s — within ideal range (10-15 min)

✓ Blank Screen Scan:
  - Sampled 20 frames (every 30s)
  - 0 blank screens detected

✓ Transition Check:
  - 7 scene boundaries analyzed
  - 0 flash frames
  - 0 audio glitches

📊 Quality Score: 98/100

✅ PASSED — Ready for upload

Watch samples:
  python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30
  python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325
  python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 565 --end 596

📋 Report saved: final-qa-report.json
```

## QA Report Format

**JSON schema:**
```json
{
  "timestamp": "2026-06-18T22:45:00Z",
  "project": "video-01-the-choice",
  "master_path": "master.mp4",
  "total_scenes": 8,
  "passed": 6,
  "failed": 2,
  "warnings": 3,
  "runtime": {
    "duration_seconds": 596.3,
    "formatted": "9m 56s",
    "target_min": 600,
    "target_max": 900,
    "status": "acceptable"
  },
  "file_integrity": {
    "video_codec": "h264",
    "resolution": "1920x1080",
    "fps": 30,
    "audio_codec": "aac",
    "bitrate": "192kbps",
    "sample_rate": 48000,
    "file_size_mb": 238
  },
  "issues": [
    {
      "scene": "02-strategic-fork",
      "type": "blank_screen",
      "severity": "critical",
      "timestamp": 72.0,
      "description": "Blank screen detected at 1:12 during survey results section",
      "variance": 3.2,
      "fix": "Add bar chart animation at BT.4 (72-74s)",
      "context": "VO says '62 percent believe...' but no visual present"
    },
    {
      "scene": "05-decision-matrix",
      "type": "scene_duration",
      "severity": "warning",
      "timestamp": 24.5,
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
      "description": "Runtime 596.3s (9:56) — 4s short of 10min target but within acceptable range"
    }
  ],
  "assets": {
    "total": 42,
    "missing": 0,
    "low_quality": 1,
    "details": [
      {
        "asset": "office-typing.mp4",
        "issue": "resolution 1280x720 (prefer 1920x1080+)",
        "severity": "info"
      }
    ]
  },
  "quality_score": 98,
  "pass": true,
  "recommendations": [
    "Fix blank screen in scene 02 before shipping",
    "Consider adding motion to scene 05 hold for better pacing"
  ]
}
```

## Quality Gates

These gates MUST pass before moving to the next workflow stage.

### Gate 1: Pre-Render (Scene Lint)

**Requirement:** All scenes pass `npx hyperframes lint` with 0 errors.

**Blocks:** Rendering

**Bypass:** Not allowed (lint errors indicate broken compositions)

### Gate 2: Post-Render (Duration + Audio)

**Requirement:**
- All scenes render successfully
- Rendered duration matches declared duration ±0.5s
- All scenes have audio streams

**Blocks:** Concatenation

**Bypass:** Only with explicit approval for edge cases

### Gate 3: Frame Analysis

**Requirement:**
- Zero blank screens (variance >10 on all sampled frames)
- No scene holds static >5s without motion

**Blocks:** Concatenation

**Bypass:** Allowed for intentional static holds (must be noted in visual treatment board)

### Gate 4: Master Validation

**Requirement:**
- Runtime ≥480s (8 min minimum)
- Zero blank screens in master
- All transition points clean (no flash frames)
- Audio stream present and synced

**Blocks:** Upload

**Bypass:** Not recommended (indicates production error)

## Auto-Fix Capabilities

The `--fix` flag can auto-repair certain safe issues:

### What Can Be Auto-Fixed

**1. Overrun BT.* helper animations**
```python
# If animation is scheduled past composition end, shift it backward
if animation_end > composition_duration:
    new_start = composition_duration - animation_duration - 0.5  # -0.5s buffer
    update_animation_timing(animation, new_start)
```

**2. Stale data-duration attributes**
```python
# If hyperframes.json duration != index.html data-duration, update HTML
declared = get_data_duration(html_path)
actual = get_composition_duration(json_path)
if abs(declared - actual) > 0.1:
    update_data_duration(html_path, actual)
```

**3. Missing timeline registration**
```python
# If timeline exists but not registered, add registration
if timeline_exists and not registered:
    add_timeline_registration(html_path, composition_id)
```

### What Cannot Be Auto-Fixed

❌ Blank screens (requires new content)  
❌ Audio sync issues (requires re-rendering with correct timing)  
❌ Text overflow (requires layout changes)  
❌ Missing assets (requires asset resolution)  
❌ Scene pacing violations (requires animation changes)  

**For these:** QA reports the issue with suggested manual fix.

## Error Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| `critical` | Blocker. Video cannot ship with this issue. | MUST FIX before proceeding |
| `error` | Significant quality issue. Viewer will notice. | SHOULD FIX before shipping |
| `warning` | Minor issue. May affect polish but not watchability. | Consider fixing |
| `info` | Informational note. Not actually a problem. | No action needed |

**Examples:**
- Blank screen → `critical`
- Text overflow off screen → `error`
- Static hold 6s → `warning`
- Runtime 596s (4s short of 10min target) → `info`

## Integration with Workflow

### During Scene Production

```bash
# 1. Write HyperFrames composition
# 2. Lint before rendering
npx hyperframes lint

# 3. Render
npx hyperframes render

# 4. Run scene validator
python3 tools/scene-validator.py . --frames

# 5. Fix any issues
# 6. Re-render if needed
# 7. Re-validate until clean
```

### Before Concatenation

```bash
# 1. Validate all scenes
python3 tools/scene-validator.py . --frames

# 2. Must pass with 0 critical issues
# 3. Then run concat
.agents/skills/jarvis-video-production/scripts/build-master.sh .
```

### After Concatenation

```bash
# 1. Run master QA
python3 tools/master-qa.py master.mp4 --sample-interval 30

# 2. Watch key samples
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 0 --end 30
python3 ~/.claude/skills/watch/scripts/watch.py master.mp4 --start 295 --end 325

# 3. Must pass before upload
```

## Continuous Improvement

After every shipped video:

1. **Review QA reports** — What issues were caught? What was missed?
2. **Update thresholds** — Are variance thresholds too strict/loose?
3. **Add new checks** — Did manual review catch something QA didn't?
4. **Document patterns** — If same issue appears multiple times, add detection
5. **Improve auto-fix** — Can any manual fixes be automated?

**Example:** After Video 14, we discovered that `tl.call()` kills timelines. Added lint check to detect and flag this pattern.

## Performance Considerations

**Frame analysis is slow** (samples every 1-30 seconds of video).

**Optimization strategies:**
1. **Adjust sample interval** — Use 30s for master (fast), 1s for critical scenes (thorough)
2. **Parallel processing** — Analyze multiple scenes concurrently
3. **Early exit** — Stop on first critical error (for fast feedback loop)
4. **Cache results** — Don't re-analyze unchanged renders

**Typical timing:**
- Scene lint: <1 second
- Scene duration check: <1 second
- Frame analysis (10s scene, 1s interval): ~3 seconds
- Frame analysis (600s master, 30s interval): ~10 seconds
- Full QA suite (8 scenes + master): ~1-2 minutes

## Future Enhancements

### Version 2.0 (Planned)

- **Audio level normalization check** — Detect scenes with mismatched audio levels
- **Text legibility analysis** — Use OCR to verify text is readable at YouTube mobile size
- **Accessibility scoring** — Check contrast ratios, caption sync, readability
- **Engagement prediction** — ML model to predict retention based on pacing patterns

### Version 3.0 (Future)

- **Real-time preview QA** — Run checks in HyperFrames preview mode (pre-render)
- **Smart suggestions** — AI suggests specific fixes for detected issues
- **Auto-repair more issues** — Extend --fix to handle layout and timing problems
- **Integration with YouTube Analytics** — Correlate QA scores with actual viewer retention

## Related Documentation

- [SKILL.md](SKILL.md) — Full workflow overview
- [RUNBOOK.md](RUNBOOK.md) — Step-by-step execution guide
- [ASSET-CATALOG-SCHEMA.md](ASSET-CATALOG-SCHEMA.md) — Asset metadata structure
