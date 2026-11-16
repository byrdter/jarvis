# Archive

Lanes JARVIS no longer works in, kept for reference. **Nothing here was deleted**; everything was moved
with `git mv`-equivalent renames on 2026-11-15, so `git log --follow <file>` still shows full history.

Why: on 2026-11-08 Terry refocused JARVIS on agentic AI (see `docs/jarvis-2.0/PLAN.md`). Other lanes were
archived, not eliminated, and can be restored by moving a folder back.

| Folder | What it was | Original location |
|---|---|---|
| `investments/skills/` | Asset Revesting workflow (Chris Vermeulen's method): etf-screener, market-analysis, market-insights, performance-tracker, portfolio, portfolio-builder, portfolio-monitor | `skills/` |
| `investments/cli-tools/` | `market-data` (Yahoo Finance) and the `jarvis-price` CLI | `cli-tools/` |
| `investments/output-style.md` | The old "investment assistant" identity, formerly switched on in `.claude/settings.json` (`outputStyle`). Identity now lives in `jarvis-brain/SOUL.md` | `.claude/` |
| `camino/` | Camino channel lane research | `_channel-camino/` |
| `keyadvances/` | KeyAdvances channel: two video projects (6G breakthrough, digital price tags) and four strategy reports | repo root, `reports/` |
| `cartoon-starter/` | Cartoon starter asset pack and its test renders | `asset-library/`, `renders/` |
| `ai-futures-collector/` | Code for the old daily AI Futures collector and digest (Five Lenses sources, sweep, digest email, launchd). Copied from Dropbox, its only home until now | `agent-sdk/` in Dropbox (never in git) |
| `phase-docs/` | Completion and setup notes from Phases 1–3 (memory, three-brain, multi-Claude, Agent SDK, cleanup plan) | repo root |

Not in this repo: Ordinary Economics, macro curriculum, athlete-investor and hallucinations series. Those
live in `jarvis-private` (Dropbox), which the plan makes cold storage. Their memory entries moved to the
archive section of the auto-memory (`memory/ARCHIVE.md`).

Kept, not archived: the `jarvis-video-production` pipeline (its tools serve the AI channel's visuals) and
`_channel-ai/` (the active channel's research).
