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

### Phase 0: Terminal Foundation ✅ COMPLETE (Jan 24, 2026)
- [x] Claude Code as brain via terminal
- [x] Context system operational (progressive disclosure working)
- [x] Market Analysis skill (with real data integration)
- [x] Memory system working (autonomous updates)
- [x] **Real market data integration** (CLI tool with yfinance)
- [x] **Live market analysis** (detected first MACD signal in SPY)
- [x] **Level 1 patterns documented** (ready for extraction)

**Key Achievement:** JARVIS detected first real market signal (MACD divergence)
**Documentation:** See `../jarvis-private/research/OPTIONS-A-B-C-D-SUMMARY.md` for complete journey

### Phase 1: Investment Domain Complete ✅ COMPLETE (Feb 13, 2026)
- [x] **ETF Screener skill** - Screen 14 ETFs, rank Stage 2 opportunities
- [x] **Portfolio Builder skill** - Construct allocation with position sizing
- [x] **Portfolio Monitor skill** - Daily stop checks + weekly reviews
- [x] **Performance Tracker skill** - Monthly strategy validation
- [x] **Market Insights skill** - Automated Chris Vermeulen YouTube analysis
- [x] **Obsidian Integration** - Multi-domain second brain (7 domains)
- [x] **Alpaca API Integration** - 200 SMA capable, 256+ days data
- [x] **$100K Portfolio Allocation** - QQQ $25K, USO $10K conditional, BIL $65K
- [~] ~~**Heartbeat System** - Fully autonomous proactive execution~~ **DELETED 2026-08-02.**
  The python scaffold (`scripts/heartbeat/`) and its four launchd jobs were removed. They
  never executed successfully — 129 TCC failures, 0 successes, 0-byte stdout logs — and could
  not have worked regardless: `run_skill()` invoked `skills/<name>/run.py` but only 3 of 21
  skills have one, and 4 of the 10 skills it called never existed. Its working functions are
  covered elsewhere (news/YouTube/arXiv via `~/bin` daily jobs; morning briefing + memory
  consolidation via the agent-sdk daily reflection). **Not covered by anything today: ETF
  stage scan, stop-loss guard, monthly performance tracking.** Recover with
  `git show d1e29a1:scripts/heartbeat/executor.py`.

**Key Achievement:** Complete Asset Revesting workflow automated + expert validation
**Documentation:** `../jarvis-private/context/memory/work-status.md`; audit + rationale in
`reports/JARVIS-SYSTEM-AUDIT-2026-08-01.md`

#### Phase 1 Extended: Content Creation Domain ✅ COMPLETE (Feb 22, 2026)
- [x] **10-Day Promotional Blitz Content Library** - 18,000+ lines of pre-written content
- [x] **Image Catalog System** - 270 images analyzed (95%+ coverage, 90%+ cost savings)
- [x] **URL Management System** - Centralized in .env + automated replacement (134 placeholders)
- [x] **Manual Posting Strategy** - Complete 17-day tactical schedule for 7 platforms
- [x] **Launch Ready** - Monday, February 23, 2026 @ 7:00 AM
  - 234+ content pieces (YouTube, Instagram, TikTok, LinkedIn, Twitter/X, Pinterest, Substack)
  - 70+ pieces complete and ready for copy/paste
  - Templates for remaining pieces (~3 hours to finish)

**Key Achievement:** Complete promotional blitz content library created - multi-platform distribution ready
**Documentation:** See `apps/content-creation/video-generator/projects/byrddynasty/content-library/LAUNCH-READY-SUMMARY.md`

### Phase 2: Agent SDK + Vector Search + API Integrations ✅ COMPLETE (Apr 1, 2026)
- [x] **Phase 2A:** Bun runtime + TypeScript environment
- [x] **Phase 2B:** Hybrid vector + keyword search (local embeddings, $0 cost)
- [x] **Phase 2C:** Gmail + Calendar integrations (OAuth, programmatic access)
- [x] **Phase 2D:** 24/7 heartbeat + specialized subagents

**Key Achievement:** Zero-cost autonomous agent with intelligent memory search and direct API integrations
**Documentation:** See `../jarvis-private/research/PHASE-2-COMPLETE.md` and `agent-sdk/` (its own repo: github.com/byrdter/jarvis_phase2)

**Capabilities Added:**
- Semantic vector search (70% vector + 30% keyword, ~60-200ms, $0 cost)
- Read emails programmatically (search, filter, check broker alerts)
- Access calendar events (today, upcoming, earnings calendar)
- 24/7 autonomous monitoring (survives reboots, CLI-first, $0/month)

### Phase 3: Autonomous Intelligence & Remote Access ⏳ IN PROGRESS (Apr 4, 2026)

#### Phase 3A: Agent SDK ✅ COMPLETE (Apr 4, 2026)
- [x] **Persistent Bun server** - 24/7 execution on port 3000
- [x] **CLI subprocess approach** - Using Claude Code CLI (Cole Medin method)
- [x] **HTTP/WebSocket APIs** - Remote query endpoints
- [x] **Event loop** - Time-based triggers (8 AM, 9:30 AM, 4 PM)
- [x] **Execution logging** - SQLite database tracking
- [x] **$0/month cost** - OAuth token (no API charges)

**Key Achievement:** True persistent autonomous agent using CLI subprocesses instead of expensive API calls  
**Documentation:** See `../jarvis-private/docs/phases/PHASE-3A-COMPLETE.md` and `../jarvis-private/docs/phases/PHASE-3-CLI-SUBPROCESS-APPROACH.md`

#### Phase 3B: Daily Reflection ✅ COMPLETE (Apr 4, 2026)
- [x] **8 AM automatic reflection** - Reviews yesterday's logs
- [x] **Learning extraction** - JARVIS analyzes patterns, extracts insights
- [x] **Memory file updates** - Auto-updates learnings.md and work-status.md
- [x] **Morning briefing** - Market + Portfolio + Calendar + Email + Priorities
- [x] **Zero manual intervention** - Self-improving AI that learns from every execution

**Key Achievement:** JARVIS manages its own memory and delivers actionable morning intelligence daily  
**Documentation:** See `../jarvis-private/docs/phases/PHASE-3B-COMPLETE.md`

**Capabilities Added:**
- CLI subprocess execution (full JARVIS context, $0 cost)
- Daily learning cycle (3-7 insights per day)
- Automatic memory management (no human updates needed)
- Morning briefings (portfolio alerts, priorities, calendar awareness)

#### Phase 3C: Remote Access 🔄 NEXT
- [ ] Chat interface (Slack/Telegram bot for mobile access)
- [ ] Push notifications for portfolio alerts
- [ ] Natural language queries from anywhere

#### Phase 3D: Voice Interface (Future)
- Voice interface (Whisper + ElevenLabs + React frontend)

### Phase 4: Full Integration
- Brokerage integration (Alpaca - if needed for trading)
- Database persistence (Supabase)
- Dashboard and reporting

## Commands Reference

```bash
# Start JARVIS session
claude

# Continue previous session
claude --continue

# Resume specific session
claude --resume

# Run in YOLO mode (if not set in settings.json)
claude --dangerously-skip-permissions
```

## Key Files to Read

### Every Session
1. `../jarvis-private/context/CLAUDE.md` - Context system orchestrator (always read first)
2. `../jarvis-private/context/memory/work-status.md` - Current state and recent work

### When Needed
3. `../jarvis-private/context/projects/investments/CLAUDE.md` - Asset Revesting methodology
4. `skills/market-analysis/SKILL.md` - When performing market analysis
5. `../jarvis-private/context/tools/market-data-cli.md` - When using market data tool
6. `../jarvis-private/context/memory/learnings.md` - Past insights and patterns
7. `../jarvis-private/context/memory/user-preferences.md` - Terry's preferences

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
Use the PINNED CLI (`hyperframes`, global **0.7.90** — verified 2026-08-04) — never bare
`npx hyperframes`. **This line is the ONE source of truth**: `tools/check-cli-pin.py` parses the
version out of it. Do not restate the number in other docs; point at this line instead.
**The global binary SELF-UPDATES**: 0.7.84 → 0.7.87 inside one session on 2026-08-01, then
0.7.87 → 0.7.88 on 2026-08-02, then 0.7.88 → 0.7.90 on 2026-08-04. **Three unchosen upgrades in four
days** — no upgrade was chosen and none would have
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

## Important Documentation

### For Understanding the System
- **`README.md`** - Overview, architecture, getting started
- **`../jarvis-private/research/LEVEL-1-PATTERNS.md`** - Domain-agnostic patterns (for extraction)
- **`../jarvis-private/MiscGuides/NINE-SKILLS-MAPPING.md`** - Connection to Nine Essential Skills framework
- **`../jarvis-private/research/OPTIONS-A-B-C-D-SUMMARY.md`** - Complete Phase 0 development journey

### For Context Recovery (If Session Lost)
- `../jarvis-private/context/memory/work-status.md` - What was completed, what's next
- `../jarvis-private/context/memory/learnings.md` - All accumulated knowledge
- `../jarvis-private/research/SESSION-ACCOMPLISHMENTS.md` - Latest session achievements

## Current Capabilities

### Market Analysis
- **Real-time data** via `jarvis-price` CLI tool (Yahoo Finance, 15-20 min delay)
- **4-stage detection** (Accumulation, Markup, Distribution, Decline)
- **Technical indicators** (SMAs, RSI, MACD)
- **Composite scoring** with grades
- **Actionable recommendations** with entry/exit points

### Tools Available (Phase 0)
- `jarvis-price indicators SPY --json` - Get all technical indicators
- `jarvis-price stage QQQ --json` - Quick stage assessment
- `jarvis-price current SYMBOL` - Current price and market data
- `jarvis-price history SYMBOL --days N` - Historical data

See `../jarvis-private/context/tools/market-data-cli.md` for complete documentation.

### MCP Integration (Phase 3+)
- **Lazy loading enabled** in `.claude/settings.json` (`enableToolSearch: true`)
- **Claude Code 2.17+** supports on-demand MCP tool loading
- **Future expansion ready**: Can add 100+ MCP servers with zero context bloat
- **Strategy**: Keep custom CLI tools for investment domain, add MCP servers for new domains (research, social, productivity)

## What JARVIS Can Do Now

1. **Analyze any stock/ETF** using Asset Revesting 4-stage framework
2. **Detect market signals** from real Yahoo Finance data
3. **Generate professional reports** saved to `../jarvis-private/reports/`
4. **Update its own memory** after completing tasks
5. **Learn from experience** via `learnings.md`
6. **Maintain continuity** across sessions
7. **Ready for MCP expansion** when adding new domains (future)


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
