# Episode Command Center

## Identity

- Working title: China's 6G Breakthrough Is Real. Faster Phones Are the Least of It
- Channel: KeyAdvances
- Channel profile: `.agents/skills/jarvis-video-production/references/channel-profiles/KEYADVANCES.md`
- Episode folder: `video-ka01-6g-breakthrough`
- Owner: Terry Byrd
- Beads issue: `jarvis-2q9k`
- Status: narration locked; S00 HyperFrames build passes; S01–S11 construction next

## Thesis

China's photonic 6G experiment is a real and important laboratory advance, but its most consequential implication is not a faster phone: it is a future network that can help machines perceive, locate, and coordinate activity in physical space.

## Audience

- Primary viewer: A curious non-specialist who wants near-future technology translated into consequences for ordinary life and work.
- What they already know: 5G was marketed around speed, coverage, and futuristic consumer experiences; many people experienced a smaller change than the advertising suggested.
- What they should understand by the end: What China actually demonstrated, what it did not, why sensing and coordination may matter more than peak speed, where effects may appear first, and what remains speculative.
- Why this matters now: The experiment is being flattened into a speed headline while the 6G standards process is defining sensing, positioning, AI integration, and coverage as first-class capabilities.

## Runtime

- Target runtime: 9:20–9:45
- Whole-runtime carried payoff: If speed is not the life-changing part of 6G, what is—and where will a normal person encounter it first?
- Persistent spine: The five-node **6G Impact Map**—SPEED, REACH, INTELLIGENCE, SENSING, COORDINATION—orbiting a human silhouette. One node activates per act; the order reorganizes at the reversal.
- Planned reversal position: 4:10–4:50, approximately 45–50% of runtime
- Current audio-derived runtime: 9:04.9 including 0.7-second scene transitions; inside the KeyAdvances 8–10 minute profile

## Production Strategy

- Default format: faceless mixed-register video
- Talking-head/guest appearance planned: no
- Primary visual system: HyperFrames with real paper/source captures and restrained documentary or generated B-roll
- Codex Sites planned: no
- Site role: none
- External clip tools: Terry's I2V renders are returned; five clean intervals are reviewed and locked under `02-assets/approved-clips/`
- Still-image owner: Codex creates and locally freezes every required original still
- I2V owner: Terry generates requested clips from Codex-supplied approved stills and complete prompt packets
- I2V handoff: `I2V-PROMPT-PACK.md`; prompts include subject motion, camera, duration, end state, negatives, filename, cue, and acceptance test
- TTS/VO tool: Cartesia Sonic 3.5, Steve voice, explicit voice ID frozen in `02-audio/voice/audio_meta.json`; speed 0.86
- Evidence language: Every future-facing application receives an on-screen state—DEMONSTRATED, STANDARD TARGET, PLAUSIBLE, or SPECULATIVE
- Motion contract: Meaningful visual change every 2–4 seconds; no unchanged state reaches five seconds; every scene and master must pass `freezedetect`
- Asset floor: One unique real background and at least three single-use clips per scene, sourced from `asset-library/assets.db` before generation

## Required Decisions

| Decision | Owner | Status | Notes |
|---|---|---|---|
| Demand evidence passed | Terry / Codex | approved | Repeated China-6G outliers; generic explainer and speed-record formulations rejected |
| Pre-script title/thumbnail package approved | Terry | approved | Locked title and `IT CAN SEE` thumbnail direction |
| Thesis locked | Terry / Codex | approved | Human-consequence thesis; speed is the initial suspect, not the verdict |
| Runtime target locked | Terry / Codex | approved | 9:20–9:45; long enough for a reversal and human consequence, short enough to avoid an essay-shaped middle |
| Visual treatment approved | Terry | approved | Terry approved the visual-first narrative and asked production to start |
| VO approved | Terry | approved by production continuation | Cartesia narration generated directly from `01-script/VO-CLEAN.md` using Steve's selected voice |
| Scene renders locked | Terry | pending | |
| Master render approved | Terry | pending | |
| Final package verified against finished video | Terry / Codex | pending | Promise changes return to pre-script gate |
| Unlisted upload QA passed | Terry | pending | Required before public/scheduled release |
| Optional dubs reviewed | Terry | not-applicable | Manual publication only |

## Open Blockers

| Blocker | Owner | Needed By | Resolution |
|---|---|---|---|
| Ordinary-life applications vary in maturity | Script / Visuals | Scene build | Preserve DEMONSTRATED / STANDARD TARGET / PLAUSIBLE / SPECULATIVE badges |
| Remaining institutional proof cards | Production | Scene build | Create focused ITU, NICT, CityUHK, and NIST cards at mobile-readable size |

## Current Next Action

- Continue S01–S11 HyperFrames construction from `.hyperframes/expanded-prompt.md`, using `02-audio/scene-timings.json` and the per-scene Cartesia word timestamps; complete remaining institutional proof cards before their evidence scenes render.
