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
**Documentation:** See `OPTIONS-A-B-C-D-SUMMARY.md` for complete journey

### Phase 1: Investment Domain Complete ✅ COMPLETE (Feb 13, 2026)
- [x] **ETF Screener skill** - Screen 14 ETFs, rank Stage 2 opportunities
- [x] **Portfolio Builder skill** - Construct allocation with position sizing
- [x] **Portfolio Monitor skill** - Daily stop checks + weekly reviews
- [x] **Performance Tracker skill** - Monthly strategy validation
- [x] **Market Insights skill** - Automated Chris Vermeulen YouTube analysis
- [x] **Obsidian Integration** - Multi-domain second brain (7 domains)
- [x] **Alpaca API Integration** - 200 SMA capable, 256+ days data
- [x] **$100K Portfolio Allocation** - QQQ $25K, USO $10K conditional, BIL $65K
- [x] **Heartbeat System** - Fully autonomous proactive execution (all 3 phases complete)

**Key Achievement:** Complete Asset Revesting workflow automated + expert validation + **Autonomous 24/7 execution**
**Documentation:** See `HEARTBEAT-COMPLETE.md` and `context/memory/work-status.md` for details

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
**Documentation:** See `PHASE-2-COMPLETE.md` and `agent-sdk/` directory

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
**Documentation:** See `PHASE-3A-COMPLETE.md` and `PHASE-3-CLI-SUBPROCESS-APPROACH.md`

#### Phase 3B: Daily Reflection ✅ COMPLETE (Apr 4, 2026)
- [x] **8 AM automatic reflection** - Reviews yesterday's logs
- [x] **Learning extraction** - JARVIS analyzes patterns, extracts insights
- [x] **Memory file updates** - Auto-updates learnings.md and work-status.md
- [x] **Morning briefing** - Market + Portfolio + Calendar + Email + Priorities
- [x] **Zero manual intervention** - Self-improving AI that learns from every execution

**Key Achievement:** JARVIS manages its own memory and delivers actionable morning intelligence daily  
**Documentation:** See `PHASE-3B-COMPLETE.md`

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
Use the PINNED CLI (`hyperframes`, global 0.7.42) — never bare `npx hyperframes`.

**When the user asks for:** long-form videos, producing a video from a HeyGen recording, scene/visual
work, revisions, QC, or packaging → load `jarvis-video-production` and follow `PIPELINE.md` (9 steps).
State which skill you're using before acting, then run it; surface to the user at the final review.

**Everything needed lives in that one hub:**
- **`knowledge/RETENTION-AND-HOOKS.md` — READ FIRST when scripting. The channel standard from our real
  YouTube retention data: ~8-MIN target (keep viewers to the end), the FACE-FIRST cold open that gives
  viewers a reason to continue (hook → avatar-joke → named-question loop; NO dark-abstract opens, NO
  38-yr-bio/on-this-channel/today-we'll-explore boilerplate), the curiosity-gap hook rule (reveal
  FACTS, withhold MEANING; prefer a paradox; reveal up to the QUESTION, stop before the ANSWER), and
  the 2-shorts-per-video rule.** Proven on the V6 & V5 8-min recuts.
- `PIPELINE.md` — the runbook. `tools/split-heygen.py` (intake), `tools/scene-validator.py` (QC gate),
  `tools/assemble-master.py` (master assembly).
- `knowledge/HYPERFRAMES-LESSONS.md`, `knowledge/ASSEMBLY-AND-AVATAR.md`, `knowledge/VISUAL-SOURCING.md`
  (don't default to HyperFrames; non-literal/symbolic visuals; breathers).
- **`knowledge/CITATION-CARD-FORMAT.md` — the CURRENT STANDARD for evidence/argument explainers**
  (dark register + cream citation cards, hard-cut concat-FILTER assembly, dead-space QC gate,
  VO-anchored via `tools/cue.py`, and the 9:16 shorts system). Proven on *The Choice* (V1) &
  *Death of the Junior Engineer* (V2). Use this mode for research videos; avatar/xfade mode is for talking-head episodes.
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
- **`LEVEL-1-PATTERNS.md`** - Domain-agnostic patterns (for extraction)
- **`NINE-SKILLS-MAPPING.md`** - Connection to Nine Essential Skills framework
- **`OPTIONS-A-B-C-D-SUMMARY.md`** - Complete Phase 0 development journey

### For Context Recovery (If Session Lost)
- `../jarvis-private/context/memory/work-status.md` - What was completed, what's next
- `../jarvis-private/context/memory/learnings.md` - All accumulated knowledge
- `SESSION-ACCOMPLISHMENTS.md` - Latest session achievements

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
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

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
