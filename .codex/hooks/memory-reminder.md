# Memory Reminder Hook

**Trigger:** After every conversation turn (before responding to next user message)

## System Reminder

After completing any task or significant interaction, reflect on:

### 1. Work Status Update
Update `context/memory/work-status.md` with:
- What was accomplished this turn
- Current state of any ongoing tasks
- Next steps if work is incomplete

### 2. New Learnings
If you learned something new about:
- Terry's preferences or communication style
- Investment patterns or insights
- Technical approaches that worked well
- Errors or issues to avoid

Add it to `context/memory/learnings.md`

### 3. User Preferences
If Terry expressed a preference about:
- Risk tolerance
- Communication style
- Analysis depth
- Report formats
- Anything else

Update `context/memory/user-preferences.md`

## Format for Memory Updates

When adding to memory files, use this format:

```markdown
### [Date] - [Topic]
[Concise description of the learning/preference/status]
- Key point 1
- Key point 2
```

## Why This Matters

Your memory is your continuity. Without updating these files, you start fresh every session. With them, you build on previous work and become more effective over time.

## Don't Over-Document

Only save genuinely useful information:
- ✅ "Terry prefers analysis with confidence levels"
- ✅ "QQQ showed Distribution signals on 2026-01-24"
- ❌ "Terry said hello" (not useful)
- ❌ "I used grep to find a file" (routine action)
