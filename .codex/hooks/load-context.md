# Load Context Hook

**Trigger:** Every user message

## Action

At the start of every conversation turn, read the context system orchestrator:

```
context/CLAUDE.md
```

This file explains the full context system structure and guides you on when to read additional context files.

## Purpose

This ensures you always have awareness of:
- The memory system (learnings, preferences, work status)
- Available projects and their context
- Tool documentation locations
- How to use progressive disclosure effectively

## Important

Do NOT read all context files upfront. The orchestrator will guide you on what to read based on the current task. This keeps token usage efficient while maintaining comprehensive knowledge access.
