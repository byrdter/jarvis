# JARVIS Project Guidelines

> **JARVIS** - Just A Rather Very Intelligent System  
> An AI-powered investment management assistant using Claude Code as its intelligent core.

## Project Overview

JARVIS is a personal AI assistant specialized in investment management using Chris Vermeulen's Asset Revesting methodology. Claude Code serves as the "brain" of the system, orchestrating analysis, recommendations, and learning through a sophisticated context system.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE (Brain)                       │
│                                                              │
│  Uses: Context System + Skills + Hooks + CLI Tools/MCP      │
└─────────────────────────────────┬───────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              [Market Data]  [Database]   [Brokerage]
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │   Full-Stack-Foundations    │
                    │   (Future: Voice + Dashboard)│
                    └─────────────────────────────┘
```

## Path Conventions

Documentation in this repo references two roots via placeholders:

- `${JARVIS_HOME}` = `~/Library/CloudStorage/Dropbox/jarvis` (this public repo)
- `${JARVIS_PRIVATE}` = `~/Library/CloudStorage/Dropbox/jarvis-private` (private peer directory, not on GitHub)

When you see those placeholders in any SKILL.md or doc, substitute mentally before navigating.

## Critical: Context System

**ALWAYS** read `${JARVIS_PRIVATE}/context/CLAUDE.md` at the start of every session. This file orchestrates the entire context system including:
- Memory (learnings, preferences, work status)
- Projects (investments, future domains)
- Tools (CLI tools, MCP servers)

The context system uses **progressive disclosure** - only read detailed context when needed for the current task.

## Directory Structure

```
jarvis/                          # Public GitHub repository
├── CLAUDE.md                    # This file - project guidelines
├── README.md                    # Setup, tech stack, getting started
├── .claude/
│   ├── output-style.md          # JARVIS personality/identity
│   ├── settings.json            # Claude Code settings
│   └── hooks/                   # Behavioral steering
├── ecosystem/                   # Core framework
├── skills/                      # Educational example skills
└── cli-tools/                   # Custom tools

../jarvis-private/               # Private data (not on GitHub)
├── context/
│   ├── CLAUDE.md                # Context system orchestrator
│   ├── memory/                  # Persistent learnings
│   ├── projects/                # Domain-specific context
│   └── tools/                   # CLI/MCP documentation
├── apps/                        # Your work products
├── reports/                     # Generated reports
└── logs/                        # Execution logs
    ├── market-analysis/         # Individual ETF deep dive
    ├── etf-screener/            # Screen 14 ETFs, rank opportunities
    ├── portfolio-builder/       # Construct allocations
    ├── portfolio-monitor/       # Daily/weekly monitoring
    ├── performance-tracker/     # Monthly validation
    ├── market-insights/         # Chris Vermeulen automation
    │   ├── check_new_videos.py  # YouTube automation script
    │   └── transcripts/         # Video transcripts
    └── obsidian-manager/        # Vault organization
```

## Core Principles

### 1. Progressive Disclosure
- Don't read all context upfront
- Read detailed files only when needed for the current task
- Use `glob` and `grep` to find specific information

### 2. Memory Management
- Update `../jarvis-private/context/memory/work-status.md` after completing tasks
- Create new learnings in `../jarvis-private/context/memory/learnings.md`
- Respect user preferences in `../jarvis-private/context/memory/user-preferences.md`

### 3. Skill Execution
- Skills are in `skills/` directory
- Always read `SKILL.md` before executing a skill
- Follow design requirements exactly
- Produce high-quality, detailed outputs

### 4. Human-in-the-Loop
- Always confirm before executing trades or financial actions
- Present analysis and recommendations, await approval
- Log all decisions and rationale

## Development Phases

Phases 0–3B are complete. Full details in [`PHASES-ARCHIVE.md`](PHASES-ARCHIVE.md).

| Phase | Shipped | One-liner |
|---|---|---|
| 0 | Jan 2026 | Terminal foundation, market data, first MACD signal |
| 1 | Feb 2026 | Full Asset Revesting workflow (screener → monitor → tracker) |
| 1-Ext | Feb 2026 | Content creation domain, 234+ pieces, multi-platform |
| 2 | Apr 2026 | Agent SDK, vector search, Gmail/Calendar, $0 cost |
| 3A | Apr 2026 | Persistent Bun server, CLI subprocess, 24/7 execution |
| 3B | Apr 2026 | Daily reflection, morning briefings, auto-memory |

**Not covered by anything today:** ETF stage scan, stop-loss guard, monthly performance tracking.

### Phase 3C: Remote Access 🔄 NEXT
- [ ] Chat interface (Slack/Telegram bot for mobile access)
- [ ] Push notifications for portfolio alerts
- [ ] Natural language queries from anywhere

### Phase 3D: Voice Interface (Future)
- Voice interface (Whisper + ElevenLabs + React frontend)

### Phase 4: Full Integration
- Brokerage integration (Alpaca - if needed for trading)
- Database persistence (Supabase)
- Dashboard and reporting

## Language: American English, always (Terry, 2026-08-24)

**Every word JARVIS produces uses American English.** Reports, video scripts and VO, on-screen text,
artifacts, PDFs, documentation, UI strings, code comments, commit messages — no exceptions, no
British spellings anywhere.

realize / organize / standardize · color / favor / behavior · center / meter / fiber ·
license (noun *and* verb) / defense / practice · check (not cheque) · installment / fulfill /
enrollment · traveling / modeling / labeled / canceled · aluminum · gray · while / among / program /
artifact / judgment · toward / forward (no trailing -s). Periods and commas go **inside** closing
quotes.

**This drift is unconscious, so catch it mechanically.** Grep any long-form deliverable before it
ships — the atlas shipped with 13 Britishisms and was already published and rendered to PDF before
Terry caught them:

```
grep -oiE '\b(realis\w*|recognis\w*|organis\w*|standardis\w*|customis\w*|utilis\w*|colour\w*|favour\w*|behaviour\w*|labour\w*|centre\w*|metre\w*|fibre\w*|licence|defence|offence|practise|cheque\w*|grey|whilst|amongst|programme\w*|instalment\w*|travelling|modelling|labelled|cancelled|aluminium|artefact\w*|enrol\b|fulfil\b|judgement|towards|backwards)\b' FILE | sort | uniq -c
```

Read the hits rather than blind-replacing — `specialist` and `analysis` are correct American English
and will show up as false positives.

## Byrddynasty Video Content

**CRITICAL — for ANY video work (Byrddynasty / faceless / "Understanding AI" / produce a video
from a HeyGen take), the canonical skill is `jarvis-video-production`. Read it FIRST:**
- `.agents/skills/jarvis-video-production/SKILL.md` — then its `PIPELINE.md` (the end-to-end
  runbook: raw HeyGen take → finished master) and the `knowledge/` docs.

**MAXIMIZE HYPERFRAMES — do not settle for text + boxes.** Every scene must pick a technique whose
JOB matches the beat (proportion → dot-grid/ring, place → map, chronology → spatial-pan timeline,
relationship → constellation, comparison → split, verdict → ticker) from
`knowledge/HYPERFRAMES-TECHNIQUE-PALETTE.md`; a plain full-frame text card is allowed ONLY for a title
or landing line. The full capability set is installed and active (`hyperframes-animation`,
`hyperframes-keyframes`, `hyperframes-creative`, `hyperframes-registry`, `figma`, + the 142-block
`hyperframes add` registry) — reach into it. **Non-negotiable technical floor:** all motion on the
registered `tl` (a bare `gsap.to`/CSS `@keyframes`/`requestAnimationFrame` renders FROZEN), and every
scene MUST pass `tools/scene-validator.py` (the pre-render determinism gate) before Terry sees it.
Use the PINNED CLI (`hyperframes`, global **0.7.109** — verified 2026-08-15) — never bare
`npx hyperframes`. **This line is the ONE source of truth**: `tools/check-cli-pin.py` parses the
version out of it. Do not restate the number in other docs; point at this line instead.
**The global binary SELF-UPDATES**: 0.7.84 → 0.7.87 inside one session on 2026-08-01, then
0.7.87 → 0.7.88 on 2026-08-02, then 0.7.88 → 0.7.90 on 2026-08-04, then 0.7.90 → 0.7.104 by
2026-08-10 (**14 patch versions while nobody was rendering**), then 0.7.104 → 0.7.107 by 2026-08-14
— caught by the gate at the start of the Ordinary Economics batch — **then 0.7.107 → 0.7.108
roughly twenty minutes later, INSIDE that same session, between stamping the batch and the first
render.** Nothing had rendered at either version, so no batch was mixed and re-pinning forward cost
nothing; the existing stamps read 0.7.90 / 0.7.98 and are complete. **Seven unchosen upgrades in a fortnight — THREE of them on 2026-08-15 alone**, the last
caught mid-batch by `--verify` after the endcard had already rendered at 0.7.108. Stamping at batch start is not ceremony: on 2026-08-14
the drift happened *between* the stamp and the render. — no upgrade was chosen and none would have
been noticed without the gate. So this number records what the current batch was rendered against,
it does not lock anything. Run `python3 tools/check-cli-pin.py --stamp <batch>` at batch start and
`--verify <batch>` before assembly; re-render the whole batch if it moved (PIPELINE.md Step 5).

**When the user asks for:** long-form videos, producing a video from a HeyGen recording, scene/visual
work, revisions, QC, or packaging → load `jarvis-video-production` and follow `PIPELINE.md` (9 steps).
State which skill you're using before acting, then run it; surface to the user at the final review.

**Everything needed lives in that one hub:**
- **`knowledge/RETENTION-AND-HOOKS.md` — READ FIRST when scripting. The channel standard from our real
  YouTube retention data: ~8-MIN target (keep viewers to the end), the **INFORMATION-FIRST** cold open
  that gives viewers a reason to continue (the first frame carries concrete, readable information — a
  named document, a filing, a real number — and the VO is about that thing → named-question loop; NO
  dark-ABSTRACT opens (mood is not information; dark is fine, *vague* is fatal), NO
  38-yr-bio/on-this-channel/today-we'll-explore boilerplate), the curiosity-gap hook rule (reveal
  FACTS, withhold MEANING; prefer a paradox; reveal up to the QUESTION, stop before the ANSWER), and
  the 2-shorts-per-video rule.** Proven on the V6 & V5 8-min recuts.
- **THE CHANNEL IS FACELESS. The avatar is gone — permanently.** Not a test, not a mode, no
  reversion path, no flag. No cold-open avatar, no avatar close, no avatar self-ID line, no HeyGen
  avatar take anywhere in the pipeline. First-person PLURAL throughout, no singular exception.
  Anything in an older doc describing this as a "~1-month test" with a "stop condition" is STALE —
  corrected 2026-08-02 by Terry. Do not reintroduce the avatar, do not add an opt-in for it, and do
  not propose reverting to face-first.
- **`knowledge/CONDUIT-VISUAL-SYSTEM.md` — what a finished video LOOKS like.** Two registers (cream
  evidence card / dark navy analysis panel) over a scrimmed, always-moving bed; a named component
  library (document card, dossier row, one-row-lit table, ghosted-slot grid, stat hero, browser chrome,
  annotation HUD, funding timeline, schematic map + docket, comparison split, stacked papers,
  constellation, landing card); progressive disclosure with **ghosted placeholders** (content must
  resolve within ~1.2s or it reads as a dead frame). **VO BINDING: ≥90% of runtime DENOTATIVE** — the
  visual illustrates the claim being made at that second; ≤10% atmospheric, only at
  transitions/breathers, NEVER on a beat carrying a number, date, name, citation or verdict. Source
  captures ≤35% of runtime — document pull-outs are one instrument, not the format. Density target
  45–60 change-events/min. Reference build = the Messi "Secretly an AI Investor" master.
- `PIPELINE.md` — the runbook. `tools/split-heygen.py` (intake), `tools/scene-validator.py`
  (determinism gate), `tools/deadspace-scan.py` (the citation-mode QC gate — run per scene AND on the
  assembled master), `tools/assemble-master.py` (master assembly).
- **VERIFY AGAINST THE ARTIFACT, NEVER AGAINST THE DOCUMENT.** Learned 2026-07-26: every defect found
  that day was already "documented." The dead-space gate was specified in prose and had never run; a
  card manifest asserted quotes were verbatim while the pixels disagreed; beat maps described a design
  two revisions old; the CLI pin disagreed with the installed binary in three files. Read the rendered
  PNG, not the YAML describing it. A written "verified" line is a claim, not a check. A gate that isn't
  a runnable script does not exist. And measure before asserting — counting lines in a plan is not
  measuring a render.
- `knowledge/HYPERFRAMES-LESSONS.md`, `knowledge/ASSEMBLY-AND-AVATAR.md`, `knowledge/VISUAL-SOURCING.md`
  (don't default to HyperFrames; non-literal/symbolic visuals; breathers).
- **`knowledge/CITATION-CARD-FORMAT.md` — the CURRENT STANDARD for evidence/argument explainers**
  (dark register + cream citation cards, hard-cut concat-FILTER assembly, dead-space QC gate,
  VO-anchored via `tools/cue.py`, and the 9:16 shorts system). Proven on *The Choice* (V1) &
  *Death of the Junior Engineer* (V2). **This is the only production mode** — the old avatar/xfade
  talking-head mode is retired with the avatar (2026-08-02).
- Asset library: canonical `asset-library/assets.db` (query by meaning via `search-assets-db.py`;
  see `references/ASSET-CONTRACT.md`). 196 assets tagged with `symbolizes`/`usable_as`.

**Hard rules learned in production:** all animation on the registered `tl` (free `gsap.to` does NOT
render); no static hold >5s (ambient motion + the freeze gate); VO-anchored timing; kicker labels
≥26px; run the QC gate on every scene before the user sees anything.

**Legacy (removed 2026-06-29):** the old `skills/video-production` (Remotion+HeyGen avatar) and
`skills/video-image-creation` (20–30s still-image) skills were deleted in favor of the single canonical
hub `jarvis-video-production` (git-recoverable if ever needed). The old global `byrddynasty-video-production`
skill is now a redirect to it. For one-off thumbnails/stills use `image-generation` + `cli-tools/make-text-card.py`.

## Key References

- **Context recovery:** `../jarvis-private/context/memory/work-status.md`
- **Market data CLI:** `../jarvis-private/context/tools/market-data-cli.md` (`jarvis-price indicators SPY --json`)
- **Asset Revesting:** `../jarvis-private/context/projects/investments/CLAUDE.md`


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol

## Memory doctrine — the ONE rule (settled 2026-08-07)

**This section supersedes every other statement about where knowledge goes.** Two stores, split by
role. They are not competitors and neither is being retired.

| Store | Holds | Write when |
|---|---|---|
| **`MEMORY.md` + its topic files**<br>`~/.claude/projects/…/memory/` → `jarvis-private/claude-memory/jarvis/memory/` | **Durable facts.** Who Terry is, standing preferences, project state, channel/production standards, pointers to external resources. The things worth re-reading at the *start* of a session. | A fact will still matter in a month, and a future session should load it without being asked. Keep `MEMORY.md` as a one-line-per-entry index, under 200 lines. |
| **`bd remember`**<br>(searchable via `bd memories <keyword>`) | **Build-time insights.** Gotchas, trap notes, "this API does X not Y", things discovered while doing a specific piece of work — tied to the work, not to Terry. | You learn something mid-task that would save time next time, but isn't a standing fact about the project. |

**Prior guidance said "use `bd remember` — do NOT use MEMORY.md files." That line was beads-plugin
boilerplate, not a considered choice here, and it contradicted `.claude/rules/session-continuity.md`,
which auto-loads alongside it.** Both files load every session, so the conflict was unresolvable at
read time. Measured before deciding: 41 curated MEMORY.md files (newest 2026-08-06) and 107 `bd`
memories — **both actively used**, for exactly the two different purposes above. Terry settled it
2026-08-07: keep both, split by role.

Rule of thumb: *would I want this loaded before I know what today's task is?* → `MEMORY.md`.
*Would I only want this once I'm already doing that kind of work?* → `bd remember`.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
