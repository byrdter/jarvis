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

1. Canonical event store: implemented in `scripts/newsroom.py`.
2. RSS event ingestion: implemented in `scripts/newsroom.py ingest-rss`.
3. YouTube report ingestion: implemented in `scripts/newsroom.py
   ingest-youtube-report`.
4. Impact scoring: implemented in `scripts/newsroom.py score` with weights in
   `config/scoring.yaml`.
5. Research-pack generation: implemented in `scripts/newsroom.py
   research-packs`.
6. Add daily YouTube competitor transcript ingestion:
   detect new videos, fetch transcripts, summarize angles, and emit richer
   candidate events instead of only markdown report entries.
   The first bridge is implemented: `youtube-transcript-queue` exports a daily
   queue of high-priority channels with verified channel IDs, and
   `export-youtube-monitor-config` exports an API-ready monitor config.
7. Generate script-with-visual-cues, resolve assets through `asset-library`, and
   render a faceless HyperFrames/Remotion draft.

## CLI

Recommended local runtime:

```bash
python3 -m venv ~/.local/share/jarvis/keyadvances-newsroom/venv
~/.local/share/jarvis/keyadvances-newsroom/venv/bin/pip install -r keyadvances-newsroom/requirements.txt
```

Initialize the local SQLite event store:

```bash
python3 keyadvances-newsroom/scripts/newsroom.py init
```

Run the current daily pipeline:

```bash
python3 keyadvances-newsroom/scripts/newsroom.py run-daily
```

Run individual stages:

```bash
python3 keyadvances-newsroom/scripts/newsroom.py ingest-rss --max-days 14
python3 keyadvances-newsroom/scripts/newsroom.py ingest-youtube-report
python3 keyadvances-newsroom/scripts/newsroom.py score
python3 keyadvances-newsroom/scripts/newsroom.py research-packs --limit 5
python3 keyadvances-newsroom/scripts/newsroom.py youtube-transcript-queue
python3 keyadvances-newsroom/scripts/newsroom.py export-youtube-monitor-config
python3 keyadvances-newsroom/scripts/newsroom.py ingest-youtube-competitors --fetch-transcripts
python3 keyadvances-newsroom/scripts/newsroom.py audio-fallback-queue
python3 keyadvances-newsroom/scripts/newsroom.py process-audio-fallbacks --limit 1
```

Default outputs:

- Event DB: `keyadvances-newsroom/data/newsroom.db`
- Candidate JSON: `keyadvances-newsroom/outputs/candidates.json`
- Research packs: `keyadvances-newsroom/outputs/research-packs/`
- Transcript queue: `keyadvances-newsroom/outputs/youtube-transcript-queue.json`
- Exported YouTube monitor config:
  `keyadvances-newsroom/outputs/keyadvances-youtube-monitor.yaml`
- YouTube transcripts: `keyadvances-newsroom/data/youtube-transcripts/`
- YouTube audio cache: `keyadvances-newsroom/data/youtube-audio/`
- Audio fallback queue: `keyadvances-newsroom/outputs/audio-fallback-queue.json`

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
