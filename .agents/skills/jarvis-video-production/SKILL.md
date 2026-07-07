---
name: jarvis-video-production
description: Use when planning, producing, revising, QAing, or packaging Jarvis/Byrddynasty faceless YouTube videos or future channel videos. This is the canonical repo-visible video workflow for Codex and Claude Code: research intake, visual-first scripting, visual treatment boards, HyperFrames scene production, screenshots/web rolls/B-roll/code/terminal/diagram variety, asset-manifest usage, beads tracking, scene QC, concat/master render, thumbnail/title packaging, and episode command-center handoff. Use this instead of legacy HeyGen/avatar or still-image-only video skills unless the user explicitly asks for those older workflows.
---

# Jarvis Video Production

This is the canonical production operator for Jarvis/Byrddynasty video work. It packages the current faceless-channel workflow so Codex and Claude Code use the same standards.

## Default Position

- **Faceless video is the default.** Use HyperFrames, real screenshots, web artifacts, B-roll, code/terminal simulations, diagrams, data visualization, and cinematic clips.
- **Two production formats — pick by content:** (a) **Citation-card / evidence mode** for research & argument explainers — dark register + cream paper citation cards that land on verified quotes, hard cuts, avatar only for intro/CTA/closing. **This is the current standard for evidence-driven videos** (proven on *The Choice* & *Death of the Junior Engineer*). See **[knowledge/CITATION-CARD-FORMAT.md](knowledge/CITATION-CARD-FORMAT.md)**. (b) **Avatar / xfade mode** for talking-head-led episodes — see [knowledge/ASSEMBLY-AND-AVATAR.md](knowledge/ASSEMBLY-AND-AVATAR.md). Shorts (9:16 promo cuts) are covered in the citation-card doc.
- **Cinematic WebGL / layered depth is the default visual language.** Treat screenshots, web-rolls, Sites, code, diagrams, data cards, and B-roll as layered objects in a spatial composition with depth, parallax, camera motion, light sweeps, scroll-chapter reveals, and foreground/background contrast. Do not reduce this to generic floating cards.
- **Sites are supporting surfaces.** Use Codex Sites for dashboards, simulators, review boards, command centers, or companion resources; capture them into HyperFrames for final video composition.
- **Talking heads are special appearances.** Use avatars, HeyGen, or Remotion talking-head pipelines only when the user intentionally asks for a guest/talking-head moment.
- **Visual-first beats script-first.** Decide what the viewer sees before locking final VO.
- **Minimum runtime is 8 minutes.** Preferred runtime is 10-15 minutes unless the user explicitly requests a short.
- **Every episode needs variety.** Avoid long runs of the same floating-card/orb/text presentation mode.

**Standing channel rules (apply to EVERY video — details in SCRIPTING.md / CITATION-CARD-FORMAT.md):**
- **Voice = first-person PLURAL** ("we/us/our"). The only singular is the avatar self-ID "I am an
  avatar for Dr. Terry Byrd." Never "I/me/my" anywhere else.
- **The CTA (subscribe/like/bell) is its OWN scene and is AVATARLESS by default** — graphics only, no
  avatar, unless Terry explicitly asks for the avatar on a specific video's CTA. The close is a
  separate avatar scene.
- **No "series" framing.** Each video STANDS ALONE; relate videos only through the Show Bible. No "the
  series / rest of the series" language unless Terry explicitly calls something a series.
- **Outside visuals are single-use** (once per video); only this-video's own `br-*`/`bg-*` may recur.
  Maximize B-roll variety and **plan the 5-second rule BEFORE the visuals map** — short on distinct
  visuals ⇒ add a GAP LIST to the video's `ASSET-GENERATION.md` addendum. Mine the pixel sets too.
- **The "technology is neutral — the choices aren't" tagline is SHARPENED** (Pope-encyclical canon):
  neutral only for a brief upstream moment, in a room you're not in; the choices are poured into the
  artifact before it reaches the viewer. Deploy the sharpened form, consistently.

## First Read

- **END-TO-END RUN (raw HeyGen take → finished master): [PIPELINE.md](PIPELINE.md)** — the canonical
  9-step runbook. Start here when producing a full video from a HeyGen recording.
- **SCRIPTING (topic → VO script, PIPELINE Step 0): [SCRIPTING.md](SCRIPTING.md)** — research the
  wikis (`tools/research-topic.py`), write in the Show Bible voice/lenses, structure into
  anchor-tagged scenes, scaffold the folder (`tools/scaffold-script.py`). Produces the script +
  `scenes.json` that the production pipeline consumes.
- **Hard-won production lessons: [knowledge/HYPERFRAMES-LESSONS.md](knowledge/HYPERFRAMES-LESSONS.md)
  and [knowledge/ASSEMBLY-AND-AVATAR.md](knowledge/ASSEMBLY-AND-AVATAR.md)** — read before authoring
  or assembling. Cover motion-must-be-on-`tl`, the 5-second rule + QC gate commands, VO-anchored
  timing, treatment registers, HeyGen avatar white-frame handling, and varied transitions.
- **Visual sourcing (DON'T default to HyperFrames): [knowledge/VISUAL-SOURCING.md](knowledge/VISUAL-SOURCING.md)**
  — HyperFrames is one register among many; visuals need not be literal. Standalone B-roll breathers,
  symbolic/atmospheric clips, screenshots, web-rolls, real/fabricated documents — and how the asset
  database's metadata drives selection.
- **Tools: [tools/scene-validator.py](tools/scene-validator.py)** (avatar-mode QC gate) and
  **[tools/assemble-master.py](tools/assemble-master.py)** (xfade + white-frame master assembly) —
  these supersede the legacy `scripts/build-master.sh` / `scripts/validate-scenes.sh`.
- **Citation-card-mode tools:** **[tools/cue.py](tools/cue.py)** (exact Whisper word-start for any cue
  phrase — VO-anchoring) and **[tools/assemble-master-concat.py](tools/assemble-master-concat.py)**
  (hard-cut master via the concat FILTER — avoids the demuxer+cfr duration-balloon bug). The
  citation-card QC gate is the **dead-space scan** (see CITATION-CARD-FORMAT.md). Card generators live
  in `jarvis/cli-tools/`: `make-citation-card.py`, `make-text-card.py`, `make-logo-card.py`,
  `make-phase-rail.py`, `verify-vo-sync.py`.

Then read only what the task needs:

- New or resumed episode: [references/WORKFLOW.md](references/WORKFLOW.md)
- Skill routing / legacy status: [references/SKILL-ROUTING.md](references/SKILL-ROUTING.md)
- Visual treatment or monotony concerns: [references/PRESENTATION-VARIETY.md](references/PRESENTATION-VARIETY.md)
- Final render or scene review: [references/QC-PASS.md](references/QC-PASS.md)
- Asset paths, naming, or clip conventions: [references/ASSET-CONTRACT.md](references/ASSET-CONTRACT.md)
- Episode command-center / Site planning: [references/COMMAND-CENTER.md](references/COMMAND-CENTER.md)
- Codex Sites as production tools, on-screen visual sources, or companion assets: [references/SITES.md](references/SITES.md)
- V14-proven palette, tooling, Runway prompts, shot vocabulary, or anti-patterns: [references/v14/INDEX.md](references/v14/INDEX.md)
- Reusable channel shapes, recipes, and interaction vocabulary: [references/channel-library/INDEX.md](references/channel-library/INDEX.md)
- **Parameterized HyperFrames blocks for code editors, terminals, UI mockups, 3D, character SVG, shader BGs, callouts, audio-reactive elements: `byrddynasty-blocks/README.md`** — drop-in alternative to building these scenes from scratch every time. ALWAYS check the block library before authoring a new scene of one of those categories.

## Required Workflow

1. Create or claim a beads issue before implementation work.
2. Build or update the episode command center: script, visual board, assets, scene status, approvals, blockers. For a new episode, run:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

3. Produce a visual treatment board before final VO or scene builds.
4. Use `asset-library/MANIFEST.json` semantic keys for reusable assets. Copy assets into scene folders; do not symlink.
5. Build scenes in HyperFrames by default. Use real screenshots/web artifacts for proof and B-roll/cinematic clips for pacing.
6. Run scene QC on rendered MP4s, not only previews. Run the canonical gate
   `python3 .agents/skills/jarvis-video-production/tools/scene-validator.py <project>/hyperframes-v3 --frames`
   (static-hold + white-frame + duration checks) and fix every flag before Terry reviews.
7. Assemble the master with `tools/assemble-master.py` (varied xfade transitions + HeyGen avatar
   white-frame handling). See [PIPELINE.md](PIPELINE.md) Step 7 + [knowledge/ASSEMBLY-AND-AVATAR.md](knowledge/ASSEMBLY-AND-AVATAR.md).
   (The legacy `scripts/build-master.sh` plain-concat path is superseded — do not use it for avatar videos.)

8. Package title, thumbnail brief, description, chapters, sources, and handoff notes.
9. Close beads issues and follow the project session-close protocol, including push.

## Current Supporting Libraries

- `.agents/skills/hyperframes-video-director/` carries HyperFrames visual direction.
- `.agents/skills/remotion-video-qa/` is for legacy/special Remotion or talking-head QA.
- `references/channel-library/` carries the mirrored channel-level shape catalog, recipes, identity, and interaction vocabulary.
- `references/v14/` carries the mirrored Video 14-proven palette, shot vocabulary, tooling, Runway prompts, and anti-patterns.
- `byrddynasty-blocks/` — production block library of 19 parameterized sub-compositions covering 8 capability categories we previously underused (code editor / terminal / UI mockup / 3D / character SVG / shader BG / callout / audio-reactive). Drop these into any video project to escape the "box + arrow + headline" default.
- `~/.claude/skills/byrddynasty-video-v14/` should delegate to this repo skill. Do not treat it as the source of truth.

## Block Library Usage (byrddynasty-blocks/)

When the script calls for a code-editor scene, terminal session, browser/iPhone mockup, 3D object, animated character, shader background, hand-drawn callout, or audio-reactive element — **reach into `byrddynasty-blocks/blocks/` first.** Do not author from scratch.

1. Copy the block(s) you need into the episode's HyperFrames project:
   ```bash
   cp byrddynasty-blocks/blocks/<block-name>.html video-XX/blocks/
   cp byrddynasty-blocks/assets/three.min.js video-XX/assets/  # only if using a 3D block
   ```
2. Reference from the root composition with a `data-variable-values` JSON override:
   ```html
   <div data-composition-id="ep14-yaml-scene"
        data-composition-src="blocks/editor-typewriter.html"
        data-start="40" data-duration="8"
        data-width="1920" data-height="1080" data-track-index="1"
        data-variable-values='{"filename":"config.yaml","lines":"video:\n  name: Episode 14","language":"yaml"}'></div>
   ```
3. Variables and defaults for every block are in the file's header comment. Read it before overriding.

**Block inventory:**
- Code editor: `editor-typewriter`, `editor-diff`, `editor-debugger`
- Terminal: `terminal-stream`, `terminal-session`
- UI mockup: `ui-chrome-browser`, `ui-vscode`, `ui-iphone-messages`
- 3D: `three-rotating-object`, `three-exploded-layers`
- Character SVG: `character-svg-pointer`, `character-svg-typing`
- Shader BG: `bg-liquid-glass`, `bg-animated-gradient`, `bg-nebula-reactive`
- Callout: `callout-marker-circle`, `callout-scribble-arrow`
- Audio-reactive: `audio-bars`, `audio-pulse`
- Utility: `utility-title-card`, `utility-end-card`

**When you improve a block during production**, push the improvement back to `byrddynasty-blocks/blocks/` so the next video inherits it (per Maintenance Rule).

## Maintenance Rule

After every shipped episode, update this skill if the production process changed. Add new reusable visual patterns, tooling lessons, asset conventions, or QC failures within the same session so future chats inherit the improvement.
