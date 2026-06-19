# Goal: YouTube Video Production Automation Skill

## Objective

Create a comprehensive `/youtube-video` skill that automates the complete production pipeline from HeyGen raw video to final YouTube-ready `.mp4`, with zero manual debugging of blank screens, timing issues, or missing B-roll.

## Input

- HeyGen video file (`.mp4`) with avatar speaking
- Avatar appears at: beginning, ending, and selective key scenes
- Majority of video uses pre-recorded B-roll, screenshots, web-rolls, and visual assets

## Output

- Final `.mp4` file ready for YouTube upload
- Automated QA verification confirming:
  - Zero blank screens
  - Scene changes every ≤5 seconds (motion or new scene)
  - Audio-visual sync perfect
  - All B-roll properly timed to VO
  - Branding consistent throughout

## Research Sources (MUST INVESTIGATE ALL)

### 1. Jarvis Repository
- `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/`
- Scan ALL subdirectories for video production patterns
- Extract established rules, anti-patterns, quality gates
- Document all reusable components

### 2. Jarvis-Private Repository
- `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/`
- **Critical**: All video production history, learnings, patterns
- Past video projects and their solutions
- B-roll catalogs and metadata systems
- VO timing patterns and proven workflows

### 3. Existing Skills
- `.agents/skills/byrddynasty-video-production/SKILL.md` — Read entire skill
- `.agents/skills/byrddynasty-video-v14/` — If exists, study thoroughly
- `.agents/skills/hyperframes/` — All HyperFrames capabilities
- `.agents/skills/gsap/` — Animation patterns
- Any other video-related skills

### 4. Memory Files
- `~/.claude/projects/.../memory/project_video_workflow_v14.md` — Canonical workflow
- `~/.claude/projects/.../memory/feedback_vo_anchored_timing.md` — Timing rules
- `~/.claude/projects/.../memory/reference_brain_color_palettes.md` — Branding
- `~/.claude/projects/.../memory/reference_video_graphics_skills.md` — Skills to load
- All other video-related memory files

### 5. HyperFrames Documentation
- **Website**: https://hyperframes.io (all documentation pages)
- **GitHub**: https://github.com/hyperframes-io/hyperframes (README, examples, API docs)
- Capabilities to map:
  - Audio synchronization methods
  - Video composition techniques
  - Asset management
  - Timing/sequencing APIs
  - B-roll integration patterns
  - QA/verification hooks

### 6. YouTube Automation Research
- Search for: "YouTube video automation pipeline"
- Search for: "HeyGen video post-production automation"
- Search for: "B-roll automation workflow"
- Extract best practices, common pitfalls, proven patterns

## Key Requirements (From Past Work)

### Quality Gates
- ✅ Zero blank screens (detect via frame analysis)
- ✅ Scene duration ≤5 seconds (motion or scene change required)
- ✅ Audio-visual sync (VO-anchored timing, not `timeScale()` stretching)
- ✅ Complete coverage (every VO second has visual content)
- ✅ Branding consistency (correct logos, colors, lower-thirds)

### B-Roll System
- Pre-recorded asset catalog with metadata
- Searchable by: topic, keyword, visual style, duration
- Types: video clips, images, screenshots, web-rolls
- Metadata includes: description, tags, duration, resolution, usage rights
- Auto-selection based on VO transcript keywords
- Human override capability (specify exact B-roll per segment)

### VO-Anchored Timing (Critical Pattern)
- Every visual element pinned to transcript timestamp
- NEVER use `tl.timeScale()` to stretch visuals to fit VO
- Calculate exact timings from transcript word-level timestamps
- Scene transitions must align with natural VO pauses

### Automation Workflow
1. **Ingest**: Accept HeyGen `.mp4` + optional manifest (B-roll preferences)
2. **Analyze**: Extract VO transcript with word-level timestamps
3. **Plan**: Generate scene-by-scene visual plan (avatar vs B-roll)
4. **Select**: Auto-select B-roll from catalog (or use manifest overrides)
5. **Compose**: Build HyperFrames composition with precise timing
6. **Render**: Generate final `.mp4`
7. **Verify**: Automated QA (blank screens, timing, sync)
8. **Report**: Detailed verification report + final video

### Asset Management
- Central catalog: `jarvis-private/video-production/assets/catalog.json` (or similar)
- Per-asset metadata:
  ```json
  {
    "id": "office-broll-001",
    "path": "assets/b-roll/office-typing.mp4",
    "type": "video",
    "duration": 8.5,
    "keywords": ["office", "typing", "productivity", "work"],
    "description": "Close-up of hands typing on laptop keyboard",
    "resolution": "1920x1080",
    "usage": "unrestricted"
  }
  ```
- Search API: Query by keywords, return ranked results
- Validation: Verify all referenced assets exist before render

### HyperFrames Integration
- Use ALL relevant HyperFrames capabilities:
  - Audio extraction and analysis
  - Transcript generation
  - Word-level timing
  - Video composition
  - Scene sequencing
  - Asset management
  - Rendering pipeline
  - QA verification tools

### Verification System
- Frame analysis: Sample every 1 second, detect blank/solid frames
- Audio sync check: Verify VO matches visual content
- Scene duration audit: Flag any scene >5 seconds without change
- Branding check: Verify logos, colors, lower-thirds
- Output: JSON report + pass/fail status

## Success Criteria

The skill is complete when:

1. ✅ A user can run: `/youtube-video path/to/heygen-video.mp4`
2. ✅ Skill auto-generates complete visual plan
3. ✅ Skill auto-selects appropriate B-roll from catalog
4. ✅ Skill renders final `.mp4` with zero manual intervention
5. ✅ Automated QA catches all issues before manual review
6. ✅ Final video passes all quality gates (no blanks, <5s scenes, perfect sync)
7. ✅ Process is repeatable (same input → same quality output)
8. ✅ Documentation is complete (future Terry can run skill without remembering details)

## Anti-Patterns to Avoid

(Extract from jarvis-private and memory files, include in skill documentation)

- Don't use `timeScale()` to stretch visuals
- Don't assume HeyGen video has continuous avatar (it may have cuts)
- Don't hard-code asset paths (use catalog)
- Don't skip QA verification (automate it)
- Don't ignore VO pauses (they're scene transition opportunities)

## Deliverables

1. **SKILL.md**: Complete skill documentation
   - Trigger conditions
   - Workflow steps
   - Asset catalog schema
   - HyperFrames integration patterns
   - QA verification process
   - Examples and edge cases

2. **Runbook**: Step-by-step execution guide
   - How to prepare HeyGen video
   - How to populate asset catalog
   - How to run the skill
   - How to interpret QA report
   - How to fix common issues

3. **Asset Catalog Template**: 
   - JSON schema
   - Example entries
   - Search/query API
   - Validation rules

4. **QA Verification Script**:
   - Frame analysis tool
   - Sync checker
   - Report generator
   - Pass/fail criteria

5. **Example Project**:
   - Sample HeyGen video
   - Complete asset catalog
   - Generated visual plan
   - Final rendered output
   - QA report

## Investigation Checklist

Before writing the skill, confirm you've:

- [ ] Read all video production skills in `.agents/skills/`
- [ ] Read all memory files related to video production
- [ ] Scanned `jarvis-private/video-production/` for patterns
- [ ] Reviewed HyperFrames website documentation
- [ ] Reviewed HyperFrames GitHub repository
- [ ] Extracted all established rules and anti-patterns
- [ ] Documented B-roll system patterns from past work
- [ ] Identified all HyperFrames capabilities relevant to automation
- [ ] Researched YouTube automation best practices
- [ ] Created comprehensive asset catalog schema
- [ ] Designed automated QA verification system
- [ ] Validated workflow against past successful videos

## Timeline

This is a comprehensive skill. Budget appropriate time for:
- **Research**: 2-4 hours (reading all sources)
- **Design**: 1-2 hours (workflow, schemas, integration patterns)
- **Documentation**: 2-3 hours (SKILL.md, runbook, examples)
- **Validation**: 1 hour (test against past video project)

**Total estimate**: 6-10 hours of focused work

## Notes

- This skill should eliminate the "fight this battle over and over" problem
- It should capture ALL accumulated knowledge about video production
- It should be comprehensive enough that future Terry doesn't need to remember details
- It should be automated enough that Claude can verify correctness
- It should be documented well enough that it becomes the new standard workflow

---

**Goal Created**: 2026-06-18  
**Target Skill**: `/youtube-video`  
**Priority**: HIGH (eliminates recurring production issues)
