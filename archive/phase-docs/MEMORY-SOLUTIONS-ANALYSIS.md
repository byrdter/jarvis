# Short-Term Persistent Memory Solutions - Analysis & Recommendations

**Date:** May 2, 2026  
**Context:** Addressing Claude Code's memory persistence across sessions, context clears, and multiple machines

---

## The Problem

**Symptoms you're experiencing:**
1. Context loss after conversation clear/compaction
2. Having to re-explain the project multiple times
3. Claude "forgetting" even within the same conversation
4. No memory persistence across machines (despite Dropbox sync of codebase)

**Root causes:**
- Claude Code's context window fills up (~200K tokens)
- Context compaction loses details
- Auto-memory exists but needs optimization
- No explicit session continuity mechanism

---

## Current State: What JARVIS Already Has

### ✅ Auto-Memory Active

Located at: `~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis/memory/`

**Current memory files (17 total):**
- `MEMORY.md` (index - first 200 lines auto-load)
- `project_*` files (phase state, plans, designs)
- `feedback_*` files (user preferences, corrections)
- `reference_*` files (wiki registry, DB layout, etc.)

**What's working:**
- Memory persists across NEW Claude Code sessions
- Organized by type (project, feedback, reference)
- Index system in MEMORY.md

**What's NOT working:**
- Doesn't survive **context compaction within a session**
- Doesn't automatically reload context mid-conversation
- Not synced across machines (stored locally in ~/.claude)
- No compression/summarization strategy

---

## Solution 1: Claude-Mem (Local Memory System)

**Repository:** https://github.com/thedotmack/claude-mem.git

### How It Works
- Runs a local web server (localhost)
- Watches Claude Code sessions in real-time
- Auto-captures: bug fixes, decisions, code diffs
- Compresses memories by up to 10x
- Provides search UI and tags

### Architecture
```
Claude Code session → Claude-Mem watcher
                          ↓
                    Compress & categorize
                          ↓
                    SQLite database
                          ↓
              Web UI (localhost:3000)
```

### Installation
```bash
# Inside Claude Code
git clone https://github.com/thedotmack/claude-mem.git
cd claude-mem
npm install  # or bun install
npm start    # Starts watcher + web UI
```

### Pros
✅ **Automatic** - No manual memory saving  
✅ **Local** - All data stays on your machine  
✅ **10x compression** - Token efficient  
✅ **Searchable** - Tags, keywords, file paths  
✅ **Zero API costs** - Runs locally  
✅ **Survives context clear** - External database

### Cons
❌ **Separate service** - Must run alongside Claude  
❌ **Not in Dropbox** - Stores locally (needs manual sync)  
❌ **Beta/experimental** - Relatively new tool  
❌ **Another dependency** - One more thing to maintain  

### Multi-Machine Support
**Workaround needed:**
```bash
# Symlink Claude-Mem DB to Dropbox
ln -s /path/to/claude-mem/data ~/Library/CloudStorage/Dropbox/jarvis-private/claude-mem-data
```

---

## Solution 2: Claude Code Built-in Auto-Memory (Enhanced)

**What you already have, but can optimize**

### Six Memory Layers (in priority order)

1. **Managed Policy** (organization-wide) - Not applicable for personal use
2. **Project Memory** (`CLAUDE.md` in repo) ✅ You have this
3. **Project Rules** (`.claude/rules/` directory) - Can add
4. **User Memory** (`~/.claude/settings.json`) ✅ You have this
5. **Project Local** (`CLAUDE.local.md`) - Can add
6. **Auto-Memory** (`~/.claude/projects/YOUR_REPO/memory/`) ✅ You have this

### Key Features to Leverage

#### Auto-Memory (Already Active)
```bash
# Force enable if not on:
export CLAUDE_CODE_DISABLE_MEMORY=0

# Check current state:
ls ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis/memory/
```

**Critical constraint:** Only first 200 lines of `MEMORY.md` auto-load into system prompt.

#### @ Import Syntax (Powerful!)
In CLAUDE.md or memory files:
```markdown
# Import README for context
@README.md

# Import architecture docs
@docs/architecture.md

# Import package.json for commands
@package.json
```

**Supports:**
- Relative paths
- Absolute paths
- Recursive imports (up to 5 hops deep)
- Markdown files preferred

#### Modular Rules (`.claude/rules/`)
Create topic-specific memory files:

```
.claude/rules/
├── code-style.md
├── testing.md
├── security.md
└── jarvis-context.md
```

**With path-specific activation:**
```markdown
---
paths:
  - "agent-sdk/**/*.ts"
  - "skills/**/*.py"
---

When working in agent-sdk, remember:
- Use Bun, not Node
- TypeScript for all new files
- ...
```

### Pros
✅ **Native** - Built into Claude Code  
✅ **Zero setup** - Already working  
✅ **Modular** - Topic files load on-demand  
✅ **@ Imports** - Pull in any context  
✅ **Gradual rollout** - Getting better over time  

### Cons
❌ **200-line limit** - MEMORY.md can't be huge  
❌ **Local storage** - `~/.claude` not synced  
❌ **No compression** - Raw text, not optimized  
❌ **Manual mid-session** - Use `/memory` command  

### Multi-Machine Support
**Problem:** Auto-memory stored in `~/.claude/projects/` (local, not synced)

**Solution:** Symlink to Dropbox
```bash
# Back up existing memory
mv ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis \
   ~/Desktop/jarvis-memory-backup

# Create Dropbox location
mkdir -p ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/jarvis

# Symlink it
ln -s ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/jarvis \
      ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis

# Copy backup into new location
cp -r ~/Desktop/jarvis-memory-backup/memory/* \
      ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/jarvis/memory/
```

Now auto-memory syncs across all machines via Dropbox!

---

## Solution 3: Beads (Issue Tracker for AI Agents)

**Repository:** https://github.com/gastownhall/beads.git

### How It Works
- SQLite database of issues/tasks
- Git-synced backup file (`.beads/issues.json`)
- Claude automatically files issues as it discovers them
- Tracks dependencies between tasks
- Updates notes at milestones

### Architecture
```
Claude discovers issue → Beads files it automatically
                             ↓
                        SQLite DB + Git backup
                             ↓
              Next session: Claude reads notes
```

### Installation
```bash
# Install beads
curl -s https://raw.githubusercontent.com/gastownhall/beads/main/install.sh | bash

# Initialize in repo
cd ~/Library/CloudStorage/Dropbox/jarvis
bd init
```

### Usage (Automatic)
Claude runs commands like:
- `bd ready` - Show what's ready to work on
- `bd list` - List all issues
- `bd show <id>` - Show issue details
- `bd update <id>` - Update notes

**You don't run these - Claude does automatically**

### Pros
✅ **Persistent task memory** - Survives sessions  
✅ **Automatic** - Claude files issues as it works  
✅ **Git-synced** - `.beads/` directory commits to repo  
✅ **Dependency tracking** - Knows what blocks what  
✅ **Audit trail** - "While building X, discovered Y"  
✅ **Multi-machine** - Git sync via Dropbox  

### Cons
❌ **Task-focused** - Not general memory (bugs/features only)  
❌ **Another tool** - Need to install + maintain  
❌ **Git workflow** - Needs commits to sync  
❌ **Overkill?** - Better for teams/large projects  

### Multi-Machine Support
✅ **Native!** - `.beads/` directory is in your git repo, syncs via Dropbox automatically

---

## Recommendation: Hybrid Approach

**Use all three, but strategically:**

### 1. **Optimize Auto-Memory (Immediate - 30 minutes)**

#### A. Symlink to Dropbox (Multi-machine sync)
```bash
# Move auto-memory to Dropbox
mkdir -p ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory
mv ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis \
   ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/jarvis

# Symlink back
ln -s ~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/jarvis \
      ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis
```

#### B. Optimize MEMORY.md (Stay under 200 lines)
```markdown
# JARVIS Memory Index

## Critical Context (Always Load)
- [Phase State](project_jarvis_phase_state.md) — Current phase, last shipped, next up
- [Video Workflow](project_video_workflow_proven.md) — V8 production pipeline
- [JARVIS Overview](@CLAUDE.md) — Project guidelines

## Active Work (Load on Demand)
- [Phase 10 Plan](project_phase_10_telegram_terminal.md)
- [Phase 9 Plan](project_phase_9_youtube_integration.md)
- [Video Automation](project_video_automation_design.md)

## Feedback (User Preferences)
- [Image Generation](feedback_image_generation_nana_banana.md)
- [Timelines](feedback_realistic_timelines.md)
- [Multi-Domain](feedback_multi_domain_focus.md)

## Reference (Technical Details)
- [Wiki Registry](reference_wiki_registry.md)
- [DB Layout](reference_jarvis_db_layout.md)
- [Video Graphics Skills](reference_video_graphics_skills.md)
```

Use `@import` to pull in full files when needed.

#### C. Add Session Continuity File
Create `.claude/rules/session-continuity.md`:

```markdown
---
name: Session Continuity
description: Automatically reload context after clear/compaction
type: user
---

## When Context Clears

If the user mentions context was cleared, compacted, or you detect memory loss:

1. **Check memory first:** Read `~/.claude/projects/.../memory/MEMORY.md`
2. **Load active work:** Check `project_jarvis_phase_state.md` for current focus
3. **Resume from there:** Don't ask user to re-explain

## Current Work Status

**Auto-check on session start:**
- What phase are we in? (Read phase state)
- What was the last thing completed? (Read work-status if exists)
- What's next? (Read from phase plans)

## User's Pattern

Terry works on JARVIS in phases. He's currently building Phase 10 (remote terminal + voice).
- He uses Dropbox for code sync across machines
- He has multiple Claude Code sessions (worktrees)
- Memory must persist across context clears
- He values concise, action-oriented responses

**When in doubt:** Check `MEMORY.md` first, ask questions second.
```

### 2. **Add Claude-Mem for Rich Context (Week 1 - 2 hours)**

**Why:** Captures detailed decisions, bug fixes, code evolution that auto-memory might miss.

```bash
# Install
cd ~/Library/CloudStorage/Dropbox/jarvis
git clone https://github.com/thedotmack/claude-mem.git .claude-mem
cd .claude-mem
bun install

# Symlink data to Dropbox
mkdir -p ../jarvis-private/claude-mem-data
ln -s ~/Library/CloudStorage/Dropbox/jarvis-private/claude-mem-data ./data

# Start (in tmux or pm2)
bun start
```

**Usage:**
- Runs in background
- Web UI at localhost:3000
- Search memories when you need to recall specific decisions
- Use compressed summaries in MEMORY.md

### 3. **Add Beads for Task Tracking (Week 2 - 1 hour)**

**Why:** Phase 10, 11, 12+ are multi-week projects. Beads tracks what's done, what's next, what blocks what.

```bash
# Install beads
curl -s https://raw.githubusercontent.com/gastownhall/beads/main/install.sh | bash

# Initialize in JARVIS
cd ~/Library/CloudStorage/Dropbox/jarvis
bd init
git add .beads/
git commit -m "feat: add beads issue tracking"
```

**Claude will automatically:**
- File issues as it discovers them
- Track dependencies
- Update notes at milestones
- Read its own notes on new sessions

---

## Implementation Plan

### Phase 1: Immediate (Today - 30 minutes)

**Goal:** Fix multi-machine memory sync + optimize existing auto-memory

**Steps:**
1. ✅ Symlink `~/.claude/projects/jarvis/` to Dropbox
2. ✅ Optimize `MEMORY.md` (stay under 200 lines, use @imports)
3. ✅ Add `.claude/rules/session-continuity.md`
4. ✅ Test on second machine (auto-memory should sync)

**Expected result:** Memory persists across machines and context clears

---

### Phase 2: Enhanced Context (Week 1 - 2 hours)

**Goal:** Add Claude-Mem for rich decision/bug tracking

**Steps:**
1. ⏭️ Install Claude-Mem
2. ⏭️ Configure to store data in Dropbox
3. ⏭️ Run in background (tmux/pm2)
4. ⏭️ Work on Phase 10, let it capture everything
5. ⏭️ After context clear, search Claude-Mem UI for specific decisions
6. ⏭️ Extract summaries into MEMORY.md weekly

**Expected result:** Never lose detailed technical decisions

---

### Phase 3: Task Persistence (Week 2 - 1 hour)

**Goal:** Add Beads for multi-phase project tracking

**Steps:**
1. ⏭️ Install Beads
2. ⏭️ Initialize in JARVIS repo
3. ⏭️ Let Claude file issues automatically
4. ⏭️ Commit `.beads/` to git (syncs via Dropbox)
5. ⏭️ Test: start new session, Claude should read beads notes

**Expected result:** Cross-session project continuity

---

## Testing the Solution

### Test 1: Context Clear Recovery
```
1. Work on Phase 10 for 30 minutes
2. Clear context or compact
3. Start new message
4. Claude should auto-reload from MEMORY.md
5. Ask: "What were we just working on?"
6. Claude should know without re-explaining
```

### Test 2: Multi-Machine Sync
```
1. Work on desktop, make progress
2. Sync Dropbox (automatic)
3. Open Claude on laptop
4. Memory should be identical
5. Continue where you left off
```

### Test 3: Session Gaps (Days Later)
```
1. Work Monday, complete Phase 10A
2. Don't touch JARVIS Tuesday-Wednesday
3. Thursday: Open Claude
4. Claude should remember Monday's work via:
   - Auto-memory (phase state)
   - Claude-Mem (detailed decisions)
   - Beads (task status)
```

---

## Alternative: Custom JARVIS Memory System

**If the above tools don't fit, build your own:**

### Concept: `jarvis-remember` Skill

```bash
# Auto-save context to Dropbox
jarvis remember "Completed Phase 10A - voice input working"

# Auto-load on new sessions
jarvis recall --latest

# Search memory
jarvis recall --search "Phase 10"
```

**Implementation:**
- SQLite database in `jarvis-private/memory/sessions.db`
- Captures: timestamp, phase, summary, files changed, decisions
- Claude Code hook: auto-save on `/exit` or context compact
- Auto-load on session start

**Pros:**
✅ Fully custom to JARVIS workflow  
✅ Dropbox-synced by default  
✅ Integrated with existing skills  

**Cons:**
❌ Have to build it (2-3 days)  
❌ Maintenance burden  

**Recommendation:** Try the hybrid approach first, build custom only if needed.

---

## Summary & Next Steps

### Immediate Actions (Today)

1. **Symlink auto-memory to Dropbox** (30 min)
   ```bash
   # See "Optimize Auto-Memory" section above
   ```

2. **Optimize MEMORY.md** (15 min)
   - Keep under 200 lines
   - Use @imports for details
   - Link to phase-specific files

3. **Add session-continuity rule** (15 min)
   - Create `.claude/rules/session-continuity.md`
   - Tell Claude to auto-reload context

**Test:** Clear context, see if Claude remembers

### This Week

4. **Install Claude-Mem** (2 hours)
   - Background service for rich context
   - Dropbox-synced data directory

5. **Install Beads** (1 hour)
   - Task tracking across sessions
   - Git-synced via Dropbox

### Maintenance

- **Weekly:** Review MEMORY.md, keep it tight
- **Monthly:** Archive old memories to topic files
- **Per phase:** Update phase state in auto-memory

---

## Expected Outcomes

**After Phase 1 (Immediate):**
✅ Memory persists across machines  
✅ Context clears don't lose everything  
✅ Claude auto-reloads on new sessions  

**After Phase 2 (Week 1):**
✅ Detailed decisions never lost  
✅ Bug fixes tracked with full context  
✅ Searchable memory archive  

**After Phase 3 (Week 2):**
✅ Multi-week projects tracked automatically  
✅ Task dependencies clear  
✅ "What's next?" always answered  

---

**Built:** May 2, 2026  
**Ready for:** Immediate implementation  
**Priority:** Phase 1 today, Phase 2-3 this week

Want me to start with Phase 1 (symlink + optimize auto-memory) right now?
