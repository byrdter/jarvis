# Jarvis Faceless Video Workflow

## 1. Research Intake

Gather source material from the active Jarvis knowledge stack:

- YouTube transcripts and monitored channels
- news/RSS/Substack/Reddit/HN aggregator
- arXiv weekly papers
- official docs, product pages, changelogs, and source screenshots
- existing Jarvis memory, scripts, and prior episode folders

Output a research brief with: thesis options, claim/source map, must-show evidence, and unanswered questions.

## 2. Episode Brief

Create or update the episode folder with:

- working title and thesis
- target audience
- target runtime: 8 minute floor, 10-15 minute preference
- source requirements
- production risks
- beads issue IDs

Initialize the command-center files with:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

## 3. Visual-First Script

Plan the visual arc before locking VO. For each scene:

- what the viewer sees
- what changes over time
- what source material supports the claim
- which tool produces the shot
- approximate duration
- approval status

Then write VO to explain the visual, not the reverse.

## 4. Visual Treatment Board

Every scene needs a treatment row:

```text
Scene:
Purpose:
VO summary:
Visual register:
Source assets:
Motion:
Production tool:
Risk:
Approval:
```

Visual register must be selected from the presentation variety catalog, not defaulted to the previous scene.

## 5. Asset Resolution

Use `asset-library/MANIFEST.json` by semantic key. Copy resolved files into each scene's `assets/` directory. Do not reference Dropbox screenshots, one-off session files, or symlinks from final scene HTML.

## 6. Scene Production

Default scene stack:

```text
video-XX-name/
  outline.md
  vo-script.md
  visual-treatment-board.md
  scenes/
    01-short-name/
      hyperframes.json
      index.html
      assets/
      lib/
      renders/
```

Use HyperFrames unless another tool is clearly better. Real source proof beats simulated proof. Simulated UI/code beats generic cards when the topic is technical work.

Codex Sites can be used as supporting production surfaces for dashboards, simulators, evidence explorers, command centers, review boards, and companion resources. Capture Site interactions or screenshots, then bring them into HyperFrames for final VO-synced composition. See [SITES.md](SITES.md).

## 7. Scene QC

Run lint, validator, render, and rendered-video QC before locking any take. Text/layout problems are production blockers, not polish notes.

For HyperFrames projects, run:

```bash
python3 tools/scene-validator.py video-XX-name
python3 tools/scene-validator.py video-XX-name --frames
```

Use the first command before or during scene iteration. Use `--frames` after rendered MP4s exist. The validator must report 0 issues before Terry reviews the scene set unless a specific exception is documented in the QC report.

The validator should catch timing and rendering defects Terry should not have to find manually: VO/composition mismatches, dead-air tails, stale `data-duration` values, animation events scheduled past scene end, `tl.call(...)` timeline killers, and near-empty rendered frames.

## 8. Master Build

When scenes are approved:

```bash
.agents/skills/jarvis-video-production/scripts/validate-scenes.sh video-XX-name
.agents/skills/jarvis-video-production/scripts/build-master.sh video-XX-name
```

Use `renders/LOCKED` files to pin approved takes. The build script writes the final master and manifest.

## 9. Publishing Package

Create:

- title options
- thumbnail brief and prompt/asset notes
- YouTube description
- chapters
- source/provenance list
- final QA summary
- handoff notes for the next session
