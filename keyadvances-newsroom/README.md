# Keyadvances Newsroom

This directory is the source-monitoring foundation for the @Keyadvances faceless
current-events/product channel.

## Goal

Detect important AI automation, agentic AI, AI assistant, and AI product
developments early enough to turn them into useful videos.

## Source Registries

- `sources/youtube-channels.yaml` - top YouTube channels to monitor for topic
  discovery, transcripts, competing angles, and title/thumbnail intelligence.
- `sources/external-sources.yaml` - RSS, API, community, research, GitHub, and
  future browser/authenticated sources.

## Current Local Reuse Points

- `../skills/youtube-monitor/monitor_channels.py` already finds recent videos
  from configured YouTube channel IDs and writes daily reports.
- `../agent-sdk/src/knowledge/youtube-scraper.ts` already wraps the transcript
  scraper and supports captions-first/audio-fallback ingestion.
- `../skills/news-aggregator/aggregate.py` now loads RSS feeds from
  `../skills/news-aggregator/config/rss-feeds.json`.
- `../skills/arxiv-research-aggregator/aggregate-arxiv.py` already queries
  arXiv categories for AI/ML papers.
- `../asset-library/` already defines the asset cue convention and Playwright
  capture runner for web screenshots and scroll footage.

## Next Implementation Phases

1. Create a canonical event store for all monitors:
   `event_id`, `source_type`, `source_name`, `url`, `title`, `published_at`,
   `summary`, `raw_payload_path`, `first_seen_at`, and `dedupe_hash`.
2. Add daily YouTube competitor ingestion:
   detect new videos, fetch transcripts, summarize angles, and emit candidate
   events instead of only markdown reports.
3. Add impact scoring:
   novelty, relevance, market importance, proof availability, visual potential,
   search demand, tension, saturation penalty, and uncertainty penalty.
4. Generate research packs for the top candidates:
   confirmed facts, claims, source links, transcript excerpts, visual captures,
   risk notes, and recommended video format.
5. Generate script-with-visual-cues, resolve assets through `asset-library`, and
   render a faceless HyperFrames/Remotion draft.

## Operational Notes

The YouTube monitor now uses a local runtime at:

`~/.local/share/jarvis/youtube-monitor/venv`

The wrapper at `~/bin/jarvis-youtube-daily.sh` points to that runtime instead of
the Dropbox CloudStorage `.venv`, avoiding the Python import deadlocks seen in
the old logs. The LaunchAgent `com.jarvis.youtube-aggregator` is bootstrapped in
the user GUI domain and scheduled for 10:00.

The news aggregator wrapper already points to a local runtime, but older logs
showed permission/import errors. Re-test that job separately before relying on
it for daily production.
