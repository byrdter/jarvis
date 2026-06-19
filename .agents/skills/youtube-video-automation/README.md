# YouTube Video Automation Skill

**Complete automation pipeline for producing YouTube videos from HeyGen raw footage.**

---

## What This Is

This skill automates the entire production workflow from a raw HeyGen video (avatar speaking) to a final YouTube-ready `.mp4` file with professional B-roll, transitions, and quality assurance.

**It eliminates:**
- ❌ Manual debugging of blank screens
- ❌ Timing drift between VO and visuals
- ❌ B-roll selection guesswork
- ❌ Repetitive scene building
- ❌ Post-render QA discovery (catches issues during production)

**It automates:**
- ✅ VO transcript extraction with word-level timestamps
- ✅ Scene planning and visual treatment board generation
- ✅ B-roll selection from searchable asset catalog
- ✅ HyperFrames scene HTML generation with VO-anchored timing
- ✅ Automated QA validation (blank screens, timing, pacing)
- ✅ Scene concatenation into master video
- ✅ Final quality report with actionable fixes

---

## Quick Start

**For first-time users:**
1. Read [SKILL.md](SKILL.md) — Overview and workflow
2. Read [RUNBOOK.md](RUNBOOK.md) — Step-by-step guide
3. Run your first automated video

**For returning users:**
```bash
cd video-XX-name
./scripts/extract-vo.sh heygen-raw.mp4 .
python3 scripts/generate-scene-plan.py --transcript assets/transcript.json --brief episode-brief.md --output visual-treatment-board.md
# Review visual-treatment-board.md
python3 scripts/resolve-assets.py --treatment visual-treatment-board.md --manifest ../asset-library/MANIFEST.json --output asset-resolution-report.md
python3 scripts/build-hyperframes-scenes.py --treatment visual-treatment-board.md --transcript assets/transcript.json --design DESIGN.md --output-dir scenes/
# Render scenes
python3 tools/scene-validator.py . --frames
.agents/skills/jarvis-video-production/scripts/build-master.sh .
python3 tools/master-qa.py master.mp4
```

---

## Documentation

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | Complete workflow overview, trigger conditions, anti-patterns, success metrics |
| [RUNBOOK.md](RUNBOOK.md) | Step-by-step execution guide with troubleshooting |
| [ASSET-CATALOG-SCHEMA.md](ASSET-CATALOG-SCHEMA.md) | Asset metadata structure, search API, validation rules |
| [QA-VERIFICATION.md](QA-VERIFICATION.md) | Automated QA system, quality gates, error detection |
| [GOAL-PROMPT.txt](GOAL-PROMPT.txt) | The original `/goal` prompt that created this skill |

---

## File Structure

```
youtube-video-automation/
  SKILL.md                      # Main skill documentation
  RUNBOOK.md                    # Execution guide
  ASSET-CATALOG-SCHEMA.md       # Asset catalog spec
  QA-VERIFICATION.md            # QA system docs
  README.md                     # This file
  GOAL-PROMPT.txt               # Original goal prompt
  GOAL.md                       # Detailed goal specification
  
  scripts/                      # Automation scripts
    extract-vo.sh               # Extract audio + transcript from HeyGen video
    generate-scene-plan.py      # Generate visual treatment board
    resolve-assets.py           # Resolve semantic keys to files
    build-hyperframes-scenes.py # Generate HyperFrames HTML compositions
  
  tools/                        # Validation tools
    scene-validator.py          # Validate scenes (lint, duration, frames)
    master-qa.py                # Final QA on master.mp4
```

---

## Key Concepts

### VO-Anchored Timing

Every visual element is timed to transcript word timestamps. **Never** use `tl.timeScale()` to stretch visuals to fit VO.

**Why:** Linear scaling can't match non-uniform speech pacing. Visuals drift 1-3 seconds from words.

**Right approach:**
```javascript
// From transcript.json: "automation" starts at 8.42s
tl.from(".automation-label", { 
  opacity: 0, y: 40, duration: 0.6 
}, 8.42);  // Pin to exact word timestamp
```

### Asset Catalog

Centralized searchable catalog of B-roll, screenshots, web-rolls, and generated clips.

**Semantic keys** (e.g., `office-typing`, `claude-desktop`) resolve to actual file paths with metadata.

**Search by keywords:**
```python
search_assets(["office", "productivity"], asset_type="video", min_duration=10)
# → Returns ranked results with match scores
```

See [ASSET-CATALOG-SCHEMA.md](ASSET-CATALOG-SCHEMA.md) for details.

### Quality Gates

Automated validation at every stage:

1. **Pre-render:** HyperFrames lint (0 errors required)
2. **Post-render:** Duration + audio stream validation
3. **Frame analysis:** Blank screen detection, scene pacing check
4. **Master validation:** Runtime, transitions, final QA

If any gate fails, the pipeline stops with actionable error messages.

See [QA-VERIFICATION.md](QA-VERIFICATION.md) for details.

### Presentation Variety

Every 8+ minute video must use ≥6 visual registers:

- Real tool screenshots
- Code & terminal action
- Web rolls & source proof
- Self-drawing diagrams
- Documentary B-roll
- Pixel/generated B-roll
- Data visualization
- Generated Sites / interactive surfaces
- Talking-head substitutes
- Audio variety
- Pacing variety

**Gate:** No more than 3 consecutive scenes with same register.

---

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

---

## Time Estimates

**Full workflow:** 2-4 hours

- Setup: 15-20 min
- VO extraction: 5-10 min
- Scene planning: 30-45 min (includes review & approval)
- Asset resolution: 15-20 min
- Scene building: 20-30 min
- Rendering: 30-60 min (depends on scene count)
- QA validation: 15-20 min
- Concatenation: 5 min
- Final QA: 10-15 min

**Manual steps:** ~1-1.5 hours (visual treatment approval, issue fixing, final review)  
**Automated:** ~1-2.5 hours (rendering, validation, concatenation)  
**Ratio:** 40% manual, 60% automated

---

## Dependencies

**Required:**
- Node.js ≥22 (for HyperFrames)
- FFmpeg (for video processing)
- Python 3.10+ (for automation scripts)

**Optional:**
- OpenCV (for frame analysis)
- Whisper API key (for transcription — or use local Whisper)

**Install:**
```bash
# macOS (Homebrew)
brew install node ffmpeg python@3.10

# Verify
node --version  # Should be ≥22
ffmpeg -version
python3 --version
```

---

## Integration with Existing Workflow

This skill extends the [jarvis-video-production](../jarvis-video-production/SKILL.md) workflow.

**When to use this skill:**
- You have a HeyGen video and want automated B-roll + production pipeline
- You're producing 8-15 minute educational/promotional videos
- You want to eliminate manual debugging and QA

**When to use jarvis-video-production directly:**
- You're building custom scenes from scratch (no HeyGen video)
- You want full manual control over every scene
- You're creating experimental visual treatments

**They share:**
- Asset catalog (MANIFEST.json)
- Validation scripts (validate-scenes.sh, build-master.sh)
- HyperFrames + GSAP patterns
- VO-anchored timing rules
- Presentation variety standards

---

## Maintenance

After every shipped video using this skill:

1. **Update asset catalog** if new reusable B-roll was created
2. **Document new patterns** if you solved a novel timing/visual problem
3. **Update anti-patterns** if you discovered a new failure mode
4. **Improve scripts** if manual steps could be automated
5. **Update SKILL.md** so future videos inherit the improvement

---

## Troubleshooting

See [RUNBOOK.md § Troubleshooting](RUNBOOK.md#troubleshooting) for common issues and fixes.

**Quick fixes:**

- **"Blank screen at XX timestamp"** → Add visual content at that timestamp
- **"Lint error: data-composition-id required"** → Add attribute to root `<div>`
- **"Asset not found"** → Check MANIFEST.json path or add asset to catalog
- **"Duration mismatch"** → Update `data-duration` to match actual timeline length

---

## Related Skills

- [jarvis-video-production](../jarvis-video-production/SKILL.md) — Canonical faceless video workflow
- [hyperframes-video-director](../hyperframes-video-director/SKILL.md) — Visual direction standards
- [hyperframes](~/.claude/skills/hyperframes/) — HyperFrames composition authoring
- [hyperframes-cli](~/.claude/skills/hyperframes-cli/) — HyperFrames CLI commands
- [gsap](~/.claude/skills/gsap/) — GSAP animation patterns

---

## License

Internal use only. Not for public distribution.

**Created:** 2026-06-18  
**Last Updated:** 2026-06-18  
**Version:** 1.0
