---
name: jarvis-video-production
description: Use when planning, producing, revising, QAing, or packaging Jarvis, Byrddynasty, KeyAdvances, or future-channel YouTube videos. This is the canonical repo-visible video workflow for Codex and Claude Code: demand validation, pre-script packaging, research intake, visual-first scripting, visual treatment boards, HyperFrames scene production, asset-manifest usage, beads tracking, scene QC, master render, unlisted upload QA, reviewed localization, measurement, and handoff. Use this instead of legacy HeyGen/avatar or still-image-only video skills unless the user explicitly asks for those older workflows.
---

# Jarvis Video Production

This is the canonical production operator for Jarvis video work across channels. It packages one
shared development and production core so Codex and Claude Code use the same standards. **Always load
the active channel profile:** the profile changes editorial scope, audience promise, packaging assets,
cadence, Shorts policy, and measurement baselines without duplicating this workflow. KeyAdvances uses
**[references/channel-profiles/KEYADVANCES.md](references/channel-profiles/KEYADVANCES.md)**.

## Default Position

- **Faceless video is the default.** Use HyperFrames, real screenshots, web artifacts, B-roll, code/terminal simulations, diagrams, data visualization, and cinematic clips.
- **Two production formats — pick by content:** (a) **Citation-card / evidence mode** for research & argument explainers — dark register + cream paper citation cards that land on verified quotes, hard cuts, avatar only for intro/CTA/closing. **This is the current standard for evidence-driven videos** (proven on *The Choice* & *Death of the Junior Engineer*). See **[knowledge/CITATION-CARD-FORMAT.md](knowledge/CITATION-CARD-FORMAT.md)**. (b) **Avatar / xfade mode** for talking-head-led episodes — see [knowledge/ASSEMBLY-AND-AVATAR.md](knowledge/ASSEMBLY-AND-AVATAR.md). Shorts (9:16 promo cuts) are covered in the citation-card doc.
- **Cinematic WebGL / layered depth is the default visual language.** Treat screenshots, web-rolls, Sites, code, diagrams, data cards, and B-roll as layered objects in a spatial composition with depth, parallax, camera motion, light sweeps, scroll-chapter reveals, and foreground/background contrast. Do not reduce this to generic floating cards.
- **Sites are supporting surfaces.** Use Codex Sites for dashboards, simulators, review boards, command centers, or companion resources; capture them into HyperFrames for final video composition.
- **Talking heads are special appearances.** Use avatars, HeyGen, or Remotion talking-head pipelines only when the user intentionally asks for a guest/talking-head moment.
- **Visual-first beats script-first.** Decide what the viewer sees before locking final VO.
- **Target runtime is ~8 minutes** (7:30–9:00) — RETENTION-FIRST (supersedes the old "10–15 min"
  guidance). A small channel's viewers give an unknown creator ≤8 min, and % viewed (what YouTube
  rewards) is structurally higher on a tight 8-min cut; 8:00 also clears the mid-roll threshold. Recut
  longer videos to ~8, keeping every verified fact. See **[knowledge/RETENTION-AND-HOOKS.md](knowledge/RETENTION-AND-HOOKS.md)**.
- **Every episode needs variety.** Avoid long runs of the same floating-card/orb/text presentation mode.
- **PER-SCENE ASSET FLOOR (Terry's rule, 2026-07-17) — non-negotiable:** every scene must carry
  **(a) a REAL background** — a generated bg still or a library image, each scene a DIFFERENT one; never
  ship the flat ambient gradient/basefill as the only background across the video — and
  **(b) AT LEAST THREE video clips**, drawn from the video's own generated assets or
  `asset-library/clip-library/` (query `asset-library/assets.db` by meaning FIRST; stage copies into each
  scene's `assets/`). Clips are single-use across the video.
  **Anti-pattern that keeps recurring: abstract data-viz text+boxes floating on one dull gradient in every
  scene.** If a scene has 0 clips or reuses the same backdrop, it is not done.

**Standing channel rules (apply to EVERY video — details in SCRIPTING.md / CITATION-CARD-FORMAT.md):**
- **RETENTION-FIRST (see [knowledge/RETENTION-AND-HOOKS.md](knowledge/RETENTION-AND-HOOKS.md) — READ
  when scripting):** ~8-min target; **INFORMATION-FIRST cold open** — the first frame carries concrete,
  specific information the viewer can read (a named document, a filing, a real number, a labelled
  chart) and the VO is about that thing → a named-question loop. **NEVER open on a dark ABSTRACT
  graphic** — mood is not information; dark is fine, vague is what killed our first-30s retention.
  DELETE the "38-years bio + on-this-channel-we-keep-asking + welcome-back + today-we'll-explore"
  boilerplate. Hooks **reveal facts, withhold meaning** (prefer a paradox; reveal up to the QUESTION,
  stop before the ANSWER). End every scene on a pull; plant a mid-video reversal.
  Shorts follow the active channel profile; never generate them automatically from every long-form video.
- **FACELESS MODE (current, from 2026-07-26 — ~1-month test).** No avatar anywhere: no cold-open
  avatar, no avatar close, no avatar self-ID line. Every competitor in our set is faceless or genuinely
  on-screen; none uses an avatar. Faceless is also far cheaper to produce automatically. See
  RETENTION-AND-HOOKS.md §2 for the stop condition — if first-30s retention drops against the
  face-first videos, face-first returns.
- **Voice = first-person PLURAL** ("we/us/our") throughout. In faceless mode there is no avatar self-ID,
  so there is no singular exception. Never "I/me/my."
- **The CTA (subscribe/like/bell) is its OWN scene**, graphics only.
- **CITATION CARDS — two renderers.** `cli-tools/make-citation-card.py` for DOCUMENT captures
  (highlighted source screenshot from a PDF). `tools/make-pullquote-card.py` for the cream
  TYPOGRAPHIC pull-quote used when a source bot-blocks capture (reuters.com does). The
  pull-quote tool **auto-fits and never truncates** — the previous renderer had a hardcoded
  112pt size and no fitting logic, so quotes were abridged with `……` to force a fit and two
  shipped cut mid-claim. Pass quotes verbatim, em dashes and typographic quote marks included.
- **REAL PEOPLE — [knowledge/CELEBRITY-USE-CHECKLIST.md](knowledge/CELEBRITY-USE-CHECKLIST.md).** Run
  it before scripting or sourcing any beat that names, shows or discusses a living public figure. It
  separates the three risks people collapse into one: **copyright** (the photo, owned by the agency —
  solved by sourcing), **right of publicity** (the likeness — state law, strongest CA/NY/TN), and
  **defamation / false light** (imputing wrongdoing — the dangerous one, and it's about the *sentence*,
  not the photo). Governs the per-video PERSON IDENTIFICATION tier tables.
- **VISUAL SYSTEM — [knowledge/CONDUIT-VISUAL-SYSTEM.md](knowledge/CONDUIT-VISUAL-SYSTEM.md).** Two
  registers (cream evidence / dark analysis) over a moving scrimmed bed; a named component library;
  progressive disclosure with ghosted placeholders; **≥90% of runtime DENOTATIVE** (the visual
  illustrates the claim being made at that second), ≤10% atmospheric and only at transitions/breathers,
  never on a beat carrying a number, date, name, citation or verdict. Source captures ≤35% of runtime —
  document pull-outs are one instrument, not the format.
- **No "series" framing.** Each video STANDS ALONE; relate videos only through the Show Bible. No "the
  series / rest of the series" language unless Terry explicitly calls something a series.
- **Outside visuals are single-use** (once per video); only this-video's own `br-*`/`bg-*` may recur.
  Maximize B-roll variety and **plan the 5-second rule BEFORE the visuals map** — short on distinct
  visuals ⇒ add a GAP LIST to the video's `ASSET-GENERATION.md` addendum. Mine the pixel sets too.
- **The "technology is neutral — the choices aren't" tagline is SHARPENED** (Pope-encyclical canon):
  neutral only for a brief upstream moment, in a room you're not in; the choices are poured into the
  artifact before it reaches the viewer. Deploy the sharpened form, consistently.

## First Read

- **SHARED DEVELOPMENT CORE: [references/WORKFLOW.md](references/WORKFLOW.md)** — demand evidence,
  pre-script title/thumbnail approval, research, originality firewall, visual-first scripting,
  rendered QC, unlisted upload QA, reviewed localization, and measurement. Load the active channel
  profile before applying it.
- **KEYADVANCES PROFILE: [references/channel-profiles/KEYADVANCES.md](references/channel-profiles/KEYADVANCES.md)** —
  near-future human-usefulness scope, packaging identity, no-routine-Shorts rule, revival baseline,
  upload/dubbing policy, scorecard, and operating rhythm. Required for every KeyAdvances task.
- **RETENTION & HOOKS — the channel standard (READ FIRST when scripting): [knowledge/RETENTION-AND-HOOKS.md](knowledge/RETENTION-AND-HOOKS.md)** —
  the ~8-min rule, the information-first cold-open template, the curiosity-gap "reveal facts / withhold
  meaning / reveal-up-to-the-question" hook rule, and mid-video reversals. Shorts policy comes from the
  active channel profile.
  Derived from the channel's real Studio retention data; governs every video and short.
  Its §7 covers IDEATION — choosing what to make, upstream of everything else. Two tools:
  `tools/outlier-scan.py` (which competitor ideas out-travelled their distribution) and
  `tools/teardown.py` (why — pull a proven video apart into a reusable structural spec).
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
- **HyperFrames technique palette — STOP settling for text + boxes: [knowledge/HYPERFRAMES-TECHNIQUE-PALETTE.md](knowledge/HYPERFRAMES-TECHNIQUE-PALETTE.md)**
  — the reach-for menu when authoring a scene: real data-viz (count-up + ring, dot-grid/waffle, growth
  bars, trend draw-on, comparison-split), diagrams/networks (constellation-hub, spatial-pan timeline,
  power-ladder, flowchart, **maps** via `us-map`/`us-map-bubble`), kinetic type (typewriter/terminal,
  ticker-takeover, overwhelm-surround, keyword-glow), and generative/canvas/3D + the `hyperframes add`
  registry. Pick the technique that matches the beat's JOB; a plain text card is only for a true title.
- **Text container palette — WHAT OBJECT HOLDS THE WORDS: [knowledge/TEXT-CONTAINER-PALETTE.md](knowledge/TEXT-CONTAINER-PALETTE.md)**
  — the companion to the technique palette. Paper/record artifacts (citation card, filing, docket,
  paper page, redaction, personnel record), screen artifacts (12 terminal profiles, 12 VS Code themes,
  9 code-motion behaviors, browser/search chrome, x-post/reddit-post, 3D device with live HTML in the
  screen), broadcast furniture (11 lower-thirds, ticker, camcorder HUD, annotation HUD), data surfaces,
  kinetic type, and composited text — plus the 12 containers we should BUILD. **The container is a
  rhetorical act:** a terminal says "happening now," a filing says "on the record," a redaction says
  "someone hid this." Every beat gets a CONTAINER tag alongside its JOB tag at Step 3.
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
2. Load the active channel profile, then follow [references/WORKFLOW.md](references/WORKFLOW.md).
   **Demand evidence and the pre-script title/thumbnail package must pass before full research,
   final VO, asset generation, or scene production.**
3. Build or update the episode command center: script, visual board, assets, scene status, approvals, blockers. For a new episode, run:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

4. Produce a visual treatment board before final VO or scene builds.
5. Use `asset-library/MANIFEST.json` semantic keys for reusable assets. Copy assets into scene folders; do not symlink.
6. Build scenes in HyperFrames by default. Use real screenshots/web artifacts for proof and B-roll/cinematic clips for pacing.
7. Run scene QC on rendered MP4s, not only previews. **TWO gates — both mandatory, fix every ERROR before Terry reviews:**
   (a) Determinism/static-hold/white-frame:
   `python3 .agents/skills/jarvis-video-production/tools/scene-validator.py <project>/hyperframes-v3 --frames`
   (b) **Text-over-text / occlusion (scene-validator does NOT catch this):**
   `hyperframes layout <scene-dir> --at-transitions --json` — run PER SCENE, parse `errorCount`, it MUST be 0.
   It samples every tween start/end seam and reports `text_occluded` / `content_overlap` / `text_overlap`
   with time+selector+fixHint. Never trust a scene-build agent's "no-overlap" self-report — run this gate.
   (Genuinely-intentional layering can be marked `data-layout-allow-overlap` / `data-layout-allow-occlusion`
   on the element, per the tool's own fixHint.)
8. Assemble the master with `tools/assemble-master.py` (varied xfade transitions + HeyGen avatar
   white-frame handling). See [PIPELINE.md](PIPELINE.md) Step 7 + [knowledge/ASSEMBLY-AND-AVATAR.md](knowledge/ASSEMBLY-AND-AVATAR.md).
   (The legacy `scripts/build-master.sh` plain-concat path is superseded — do not use it for avatar videos.)

9. Verify the pre-approved title/thumbnail against the final cut; prepare description, chapters,
   sources, and handoff notes. A fundamental promise change returns to the pre-script gate.
10. Upload unlisted for processing and operational QA. Review optional automatic dubs before
    publication. Then publish/schedule and record the channel-profile scorecard checkpoints.
11. Close beads issues and follow the project session-close protocol, including push.

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
