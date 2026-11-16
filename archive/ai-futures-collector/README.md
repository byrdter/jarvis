# AI Futures collector (archived)

The code behind the old daily AI Futures digest (June to September 2026). It ran from
`agent-sdk/` in Dropbox on the old Mac via launchd, collected about 100 sources across the "Five
Lenses" (power and control, economic futures, meaning and identity, strategic choices, social
consequences), filled the AI Futures wiki (5,232 pages, still in `jarvis-private`), and emailed a
digest each morning. It stopped around 2026-09-26, when the Mac changed.

Copied here on 2026-11-15 so git holds a copy; until then Dropbox was its only home. It is not run
anymore. Its replacement is `infra/server/jobs/collect.py` and `curate.py`, which collect for the
agentic-AI focus and curate into the brain wiki.

- `src/fetchers/sources.ts`: the source registry (feeds, tiers, lenses)
- `src/fetchers/ai-futures.ts`, `sweep.ts`, `digest.ts`, `notify.ts`: collect, sweep, digest, email
- `src/fetchers/graph.ts`: the wiki link graph
- `src/knowledge/youtube-scraper.ts`: wrapper for the old transcript scraper
- `launchd/`: the daily schedule on the old Mac
