# Skill Routing

Use this file to avoid obsolete video workflows.

## Canonical

`jarvis-video-production` is the current default for Jarvis/Byrddynasty video production.

Use it for:

- faceless videos
- Video 14-style or later workflows
- HyperFrames scene production
- screenshots, web rolls, B-roll, code, terminal, diagrams, data visualization, cinematic clips
- episode command centers
- multi-scene concat/master rendering
- packaging titles, thumbnails, descriptions, chapters, and sources

## Supporting

- `hyperframes-video-director`: visual direction and HyperFrames scene standards.
- `hyperframes`: composition authoring.
- `hyperframes-cli`: lint, preview, render, transcribe, and CLI operations.
- `gsap`: animation implementation patterns.
- `remotion-video-qa`: only when a Remotion/talking-head project is active.

## Legacy / Special Case

- `skills/video-production/SKILL.md`: legacy HeyGen + Remotion + avatar pipeline. Use only for intentional talking-head/avatar work.
- `skills/video-image-creation/SKILL.md`: legacy still-image prompt workflow. Use only for thumbnails, concept frames, or one-off generated still assets.
- `~/.claude/skills/byrddynasty-video-v14`: first proven faceless implementation. Reference it for examples, but this repo skill is the canonical entry point.
- `~/.claude/skills/byrddynasty-video-production`: larger vocabulary library. Reference useful patterns until the library is mirrored into `.agents/skills`.

## Rule

When a task says "video production," "new episode," "future channel," "faceless channel," "HyperFrames video," or "Video 14 style," start here unless the user explicitly asks for a legacy avatar/still-image workflow.
