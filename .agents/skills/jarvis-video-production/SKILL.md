---
name: jarvis-video-production
description: Use when planning, producing, revising, QAing, or packaging Jarvis/Byrddynasty faceless YouTube videos or future channel videos. This is the canonical repo-visible video workflow for Codex and Claude Code: research intake, visual-first scripting, visual treatment boards, HyperFrames scene production, screenshots/web rolls/B-roll/code/terminal/diagram variety, asset-manifest usage, beads tracking, scene QC, concat/master render, thumbnail/title packaging, and episode command-center handoff. Use this instead of legacy HeyGen/avatar or still-image-only video skills unless the user explicitly asks for those older workflows.
---

# Jarvis Video Production

This is the canonical production operator for Jarvis/Byrddynasty video work. It packages the current faceless-channel workflow so Codex and Claude Code use the same standards.

## Default Position

- **Faceless video is the default.** Use HyperFrames, real screenshots, web artifacts, B-roll, code/terminal simulations, diagrams, data visualization, and cinematic clips.
- **Cinematic WebGL / layered depth is the default visual language.** Treat screenshots, web-rolls, Sites, code, diagrams, data cards, and B-roll as layered objects in a spatial composition with depth, parallax, camera motion, light sweeps, scroll-chapter reveals, and foreground/background contrast. Do not reduce this to generic floating cards.
- **Sites are supporting surfaces.** Use Codex Sites for dashboards, simulators, review boards, command centers, or companion resources; capture them into HyperFrames for final video composition.
- **Talking heads are special appearances.** Use avatars, HeyGen, or Remotion talking-head pipelines only when the user intentionally asks for a guest/talking-head moment.
- **Visual-first beats script-first.** Decide what the viewer sees before locking final VO.
- **Minimum runtime is 8 minutes.** Preferred runtime is 10-15 minutes unless the user explicitly requests a short.
- **Every episode needs variety.** Avoid long runs of the same floating-card/orb/text presentation mode.

## First Read

Read only what the task needs:

- New or resumed episode: [references/WORKFLOW.md](references/WORKFLOW.md)
- Skill routing / legacy status: [references/SKILL-ROUTING.md](references/SKILL-ROUTING.md)
- Visual treatment or monotony concerns: [references/PRESENTATION-VARIETY.md](references/PRESENTATION-VARIETY.md)
- Final render or scene review: [references/QC-PASS.md](references/QC-PASS.md)
- Asset paths, naming, or clip conventions: [references/ASSET-CONTRACT.md](references/ASSET-CONTRACT.md)
- Episode command-center / Site planning: [references/COMMAND-CENTER.md](references/COMMAND-CENTER.md)
- Codex Sites as production tools, on-screen visual sources, or companion assets: [references/SITES.md](references/SITES.md)
- V14-proven palette, tooling, Runway prompts, shot vocabulary, or anti-patterns: [references/v14/INDEX.md](references/v14/INDEX.md)
- Reusable channel shapes, recipes, and interaction vocabulary: [references/channel-library/INDEX.md](references/channel-library/INDEX.md)

## Required Workflow

1. Create or claim a beads issue before implementation work.
2. Build or update the episode command center: script, visual board, assets, scene status, approvals, blockers. For a new episode, run:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

3. Produce a visual treatment board before final VO or scene builds.
4. Use `asset-library/MANIFEST.json` semantic keys for reusable assets. Copy assets into scene folders; do not symlink.
5. Build scenes in HyperFrames by default. Use real screenshots/web artifacts for proof and B-roll/cinematic clips for pacing.
6. Run scene QC on rendered MP4s, not only previews.
7. Validate and stitch scenes with the bundled scripts:

```bash
.agents/skills/jarvis-video-production/scripts/validate-scenes.sh video-XX-name
.agents/skills/jarvis-video-production/scripts/build-master.sh video-XX-name
```

8. Package title, thumbnail brief, description, chapters, sources, and handoff notes.
9. Close beads issues and follow the project session-close protocol, including push.

## Current Supporting Libraries

- `.agents/skills/hyperframes-video-director/` carries HyperFrames visual direction.
- `.agents/skills/remotion-video-qa/` is for legacy/special Remotion or talking-head QA.
- `references/channel-library/` carries the mirrored channel-level shape catalog, recipes, identity, and interaction vocabulary.
- `references/v14/` carries the mirrored Video 14-proven palette, shot vocabulary, tooling, Runway prompts, and anti-patterns.
- `~/.claude/skills/byrddynasty-video-v14/` should delegate to this repo skill. Do not treat it as the source of truth.

## Maintenance Rule

After every shipped episode, update this skill if the production process changed. Add new reusable visual patterns, tooling lessons, asset conventions, or QC failures within the same session so future chats inherit the improvement.
