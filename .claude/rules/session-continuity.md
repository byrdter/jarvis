---
name: Session Continuity
description: Auto-reload context after clear/compaction, persist across sessions
type: behavior
---

# Session Continuity Protocol

## Automatic Context Recovery

**When to trigger:**
- Starting a new Claude Code session
- After context compaction
- After context clear
- User mentions memory loss
- User asks "where were we?" or "what were we working on?"

## Recovery Steps (Auto-Execute)

### 1. Check Auto-Memory First
```
Location: ~/.claude/projects/-Users-terrybyrd-Library-CloudStorage-Dropbox-jarvis/memory/
Read: MEMORY.md (index - first 200 lines auto-load)
```

**Critical files to check:**
1. `project_jarvis_phase_state.md` — What phase are we in? What's current?
2. `MEMORY.md` — Index of all memory files
3. Phase-specific project files

### 2. Identify Current Work
From phase state, determine:
- **Current phase:** What are we building? (e.g., Phase 10: Remote Terminal)
- **Last completed:** What shipped recently?
- **Next task:** What's the immediate next step?
- **Open decisions:** What needs user input?

### 3. Load Relevant Context
Based on current phase, load:
- Project files (plans, designs)
- Feedback files (user preferences)
- Reference files (technical details)

### 4. Resume Work
**Don't ask Terry to re-explain.**
Instead:
- State what you found: "I see we're working on Phase 10 (remote terminal + voice)"
- Confirm current task: "Last update shows we completed voice input. Next: test the bot?"
- Offer to continue: "Ready to proceed with testing, or need something else?"

## Terry's Working Patterns

**Multi-Machine:**
- Desktop, laptop, iPad (all Dropbox-synced)
- Memory persists across all machines
- Git worktrees for parallel work

**Communication Style:**
- Concise, action-oriented
- "We" voice (collective builder)
- Dislikes repetition
- Values efficiency

**Workflow:**
- Works in phases (Phase 1-10+)
- Documents in videos (Byrddynasty channel)
- Simultaneous: code + video production + business automation
- Expects Claude to remember context

## What NOT to Do

❌ **Don't** ask "What were we working on?" if memory exists  
❌ **Don't** make Terry re-explain the project setup  
❌ **Don't** forget across context clears  
❌ **Don't** ignore auto-memory files  
❌ **Don't** start from scratch when context exists  

## What TO Do

✅ **Do** check MEMORY.md first  
✅ **Do** read phase state automatically  
✅ **Do** resume from last known state  
✅ **Do** update memory after completing tasks  
✅ **Do** maintain continuity across sessions  

## Memory doctrine

**`CLAUDE.md` § "Memory doctrine" is the single source of truth.** Short version: `MEMORY.md`
holds durable facts you want loaded *before* you know today's task; `bd remember` holds build-time
insights you only want once you're already doing that kind of work. Both stores are live — the
old "do NOT use MEMORY.md" line in CLAUDE.md was plugin boilerplate and contradicted this file.
Settled 2026-08-07.

## Memory Update Protocol

**After completing significant work:**
1. Update `project_jarvis_phase_state.md` with new status
2. Create/update relevant project file if needed
3. Update MEMORY.md if structure changes
4. Commit to memory (files auto-save)

**Example:**
```
# Just completed Phase 10A (voice input)
Update: project_jarvis_phase_state.md
  - Set Phase 10A status to "✅ Complete"
  - Set next focus to "Phase 10 testing & deployment"
  - Note files changed: telegram-phase10.ts, remote-terminal.ts
```

## Context Size Management

**When approaching context limits:**
1. Summarize current work to phase file
2. Link to detailed files (don't inline)
3. Use @imports to pull specific sections
4. Trust memory - don't repeat full context

**Balance:**
- Enough context to work effectively
- Not so much we hit limits
- Memory files are the safety net

## Emergency: If Memory Seems Lost

**Checklist:**
1. Check `~/.claude/projects/.../memory/MEMORY.md` — Does it exist?
2. Check symlink: `ls -la ~/.claude/projects/.../memory/` — Is it pointing to Dropbox?
3. Check Dropbox sync: Files should be in `~/Library/CloudStorage/Dropbox/jarvis-private/claude-memory/`
4. If all exists: Re-read MEMORY.md and phase state
5. If missing: Alert Terry immediately

## Multi-Session Coordination

**If Terry has multiple Claude sessions open:**
- Each session has same memory (Dropbox-synced)
- Updates may take 1-2 seconds to sync
- If conflicts: check file timestamps, use newest
- Terry may work on different phases in parallel (git worktrees)

## Session Start Checklist

**Every time Claude Code starts in JARVIS repo:**
1. ✅ Auto-load MEMORY.md (first 200 lines)
2. ✅ Check current phase
3. ✅ Identify active task
4. ✅ Ready to resume

**Terry shouldn't need to:**
- Re-explain project
- Repeat recent work
- Manually reload context

---

**Implementation:** This rule activates automatically in all JARVIS sessions.  
**Location:** `.claude/rules/session-continuity.md`  
**Last Updated:** 2026-05-02
