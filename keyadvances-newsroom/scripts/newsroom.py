#!/usr/bin/env python3
"""
Keyadvances newsroom CLI.

Creates a canonical event store, ingests RSS/news and YouTube-monitor outputs,
scores video candidates, and generates source-grounded research packs.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import textwrap
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "newsroom.db"
DEFAULT_OUTPUTS = ROOT / "outputs"
DEFAULT_RSS_CONFIG = ROOT.parent / "skills" / "news-aggregator" / "config" / "rss-feeds.json"
DEFAULT_YOUTUBE_REPORT_DIR = ROOT.parent / "skills" / "youtube-monitor" / "reports" / "daily"
DEFAULT_SCORING_CONFIG = ROOT / "config" / "scoring.yaml"
DEFAULT_YOUTUBE_CHANNELS = ROOT / "sources" / "youtube-channels.yaml"


SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  dedupe_hash TEXT NOT NULL UNIQUE,
  source_type TEXT NOT NULL,
  source_name TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  summary TEXT DEFAULT '',
  published_at TEXT,
  first_seen_at TEXT NOT NULL,
  raw_payload_json TEXT DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'discovered'
);

CREATE TABLE IF NOT EXISTS event_scores (
  event_id TEXT PRIMARY KEY,
  impact_score REAL NOT NULL,
  novelty REAL NOT NULL,
  audience_relevance REAL NOT NULL,
  market_importance REAL NOT NULL,
  proof_available REAL NOT NULL,
  visual_potential REAL NOT NULL,
  search_demand REAL NOT NULL,
  tension REAL NOT NULL,
  saturation_penalty REAL NOT NULL,
  uncertainty_penalty REAL NOT NULL,
  reasons_json TEXT NOT NULL,
  scored_at TEXT NOT NULL,
  FOREIGN KEY(event_id) REFERENCES events(event_id)
);

CREATE INDEX IF NOT EXISTS idx_events_published ON events(published_at);
CREATE INDEX IF NOT EXISTS idx_events_source ON events(source_type, source_name);
CREATE INDEX IF NOT EXISTS idx_scores_impact ON event_scores(impact_score DESC);
"""


@dataclass
class Event:
    source_type: str
    source_name: str
    title: str
    url: str
    summary: str = ""
    published_at: str | None = None
    raw_payload: dict[str, Any] | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text: str, max_len: int = 72) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].strip("-") or "event"


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_url(url: str) -> str:
    return (url or "").split("?utm_")[0].rstrip("/")


def event_hash(event: Event) -> str:
    key = f"{normalize_url(event.url)}|{event.title.lower().strip()}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def event_id_for(event: Event) -> str:
    digest = event_hash(event)[:12]
    return f"{event.source_type}-{slugify(event.title, 44)}-{digest}"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def upsert_event(db: sqlite3.Connection, event: Event) -> bool:
    dedupe = event_hash(event)
    event_id = event_id_for(event)
    before = db.total_changes
    db.execute(
        """
        INSERT INTO events (
          event_id, dedupe_hash, source_type, source_name, title, url, summary,
          published_at, first_seen_at, raw_payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(dedupe_hash) DO UPDATE SET
          summary = CASE
            WHEN excluded.summary != '' THEN excluded.summary
            ELSE events.summary
          END,
          published_at = COALESCE(excluded.published_at, events.published_at),
          raw_payload_json = excluded.raw_payload_json
        """,
        (
            event_id,
            dedupe,
            event.source_type,
            event.source_name,
            clean_text(event.title),
            event.url,
            clean_text(event.summary),
            event.published_at,
            utc_now(),
            json.dumps(event.raw_payload or {}, ensure_ascii=True),
        ),
    )
    return db.total_changes > before


def parse_date(value: Any) -> str | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat(timespec="seconds")
    text = str(value).strip()
    for parser in (
        lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")),
        parsedate_to_datetime,
    ):
        try:
            return parser(text).astimezone(timezone.utc).isoformat(timespec="seconds")
        except Exception:
            pass
    return None


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "KeyadvancesNewsroom/0.1 (+https://youtube.com/@keyadvances)"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


def parse_feed_entries(xml_bytes: bytes, source_name: str) -> list[Event]:
    root = ET.fromstring(xml_bytes)
    events: list[Event] = []

    if root.tag.endswith("rss") or root.find("./channel") is not None:
        for item in root.findall("./channel/item"):
            title = clean_text(item.findtext("title", ""))
            url = clean_text(item.findtext("link", ""))
            summary = clean_text(item.findtext("description", ""))
            published = parse_date(item.findtext("pubDate") or item.findtext("date"))
            if title and url:
                events.append(
                    Event("rss", source_name, title, url, summary, published, {"feed": source_name})
                )
        return events

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns) or root.findall("entry")
    for entry in entries:
        title = clean_text(entry.findtext("atom:title", "", ns) or entry.findtext("title", ""))
        summary = clean_text(
            entry.findtext("atom:summary", "", ns)
            or entry.findtext("atom:content", "", ns)
            or entry.findtext("summary", "")
        )
        url = ""
        for link in entry.findall("atom:link", ns) + entry.findall("link"):
            href = link.attrib.get("href", "")
            rel = link.attrib.get("rel", "alternate")
            if href and rel == "alternate":
                url = href
                break
            if href and not url:
                url = href
        published = parse_date(
            entry.findtext("atom:published", "", ns)
            or entry.findtext("atom:updated", "", ns)
            or entry.findtext("published", "")
        )
        if title and url:
            events.append(Event("rss", source_name, title, url, summary, published, {"feed": source_name}))
    return events


def load_rss_config(path: Path) -> dict[str, str]:
    with path.open() as f:
        return json.load(f)


def ingest_rss(
    db: sqlite3.Connection,
    config_path: Path,
    limit_sources: int | None = None,
    max_days: int = 14,
) -> int:
    feeds = list(load_rss_config(config_path).items())
    if limit_sources:
        feeds = feeds[:limit_sources]

    inserted = 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    for source_name, feed_url in feeds:
        try:
            entries = parse_feed_entries(fetch_url(feed_url), source_name)
        except Exception as exc:
            print(f"! RSS fetch failed for {source_name}: {exc}")
            continue
        for event in entries:
            if event.published_at:
                try:
                    published = datetime.fromisoformat(event.published_at)
                    if published < cutoff:
                        continue
                except ValueError:
                    pass
            inserted += int(upsert_event(db, event))
    db.commit()
    return inserted


YOUTUBE_ENTRY_RE = re.compile(
    r"^### (?P<title>.+?)\n\n"
    r"\*\*Channel:\*\* (?P<channel>.+?)\n\n"
    r".*?\[Watch Video\]\((?P<url>https://www\.youtube\.com/watch\?v=[^)]+)\).*?\n\n"
    r"(?:> (?P<summary>.*?)(?:\n\n|$))?",
    re.MULTILINE | re.DOTALL,
)


def ingest_youtube_report(db: sqlite3.Connection, report_path: Path) -> int:
    text = report_path.read_text()
    inserted = 0
    for match in YOUTUBE_ENTRY_RE.finditer(text):
        title = clean_text(match.group("title"))
        channel = clean_text(match.group("channel"))
        url = clean_text(match.group("url"))
        summary = clean_text(match.group("summary") or "")
        event = Event(
            "youtube",
            channel,
            title,
            url,
            summary,
            raw_payload={"report_path": str(report_path)},
        )
        inserted += int(upsert_event(db, event))
    db.commit()
    return inserted


def latest_youtube_report(report_dir: Path) -> Path | None:
    reports = sorted(report_dir.glob("ai-youtube-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def load_scoring_config(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f)


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term.lower() in text for term in terms)


def term_count(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term.lower() in text)


def score_event(row: sqlite3.Row, config: dict[str, Any]) -> dict[str, Any]:
    title = row["title"] or ""
    summary = row["summary"] or ""
    text = f"{title} {summary}".lower()
    source_type = row["source_type"]
    source_name = (row["source_name"] or "").lower()
    weights = config["weights"]
    high = config.get("high_value_terms", [])
    visual = config.get("visual_terms", [])
    tension_terms = config.get("tension_terms", [])
    saturation_terms = config.get("saturation_terms", [])

    high_hits = term_count(text, high)
    visual_hits = term_count(text, visual)
    tension_hits = term_count(text, tension_terms)

    novelty = 1.0 if any(w in text for w in ["new", "launch", "released", "update", "beta", "leak"]) else 0.55
    audience_relevance = min(1.0, 0.2 + high_hits * 0.16)
    market_importance = 0.85 if contains_any(text, ["openai", "anthropic", "google", "meta", "microsoft", "nvidia", "github"]) else 0.45
    proof_available = 0.85 if source_type in {"rss", "youtube", "github", "api"} else 0.55
    visual_potential = min(1.0, 0.35 + visual_hits * 0.18 + (0.15 if source_type == "youtube" else 0))
    search_demand = min(1.0, 0.25 + high_hits * 0.12 + (0.2 if source_type == "youtube" else 0))
    tension = min(1.0, 0.1 + tension_hits * 0.2)
    saturation_penalty = min(1.0, 0.15 + term_count(text, saturation_terms) * 0.25)
    uncertainty_penalty = 0.55 if contains_any(text, ["rumor", "leak", "unconfirmed"]) else 0.1

    if any(name in source_name for name in ["openai", "anthropic", "deepmind", "hugging face", "langchain"]):
        proof_available = max(proof_available, 0.9)
        market_importance = max(market_importance, 0.75)

    components = {
        "novelty": novelty,
        "audience_relevance": audience_relevance,
        "market_importance": market_importance,
        "proof_available": proof_available,
        "visual_potential": visual_potential,
        "search_demand": search_demand,
        "tension": tension,
        "saturation_penalty": saturation_penalty,
        "uncertainty_penalty": uncertainty_penalty,
    }
    impact_score = sum(components[name] * weights[name] for name in components)
    reasons = []
    if high_hits:
        reasons.append(f"{high_hits} high-value AI/agent terms")
    if visual_hits:
        reasons.append(f"{visual_hits} visual capture terms")
    if tension_hits:
        reasons.append(f"{tension_hits} tension/hook terms")
    if source_type == "youtube":
        reasons.append("competitor video source")
    if not reasons:
        reasons.append("baseline AI/news relevance")
    return {"impact_score": round(impact_score, 2), "components": components, "reasons": reasons}


def score_events(db: sqlite3.Connection, config_path: Path) -> int:
    config = load_scoring_config(config_path)
    rows = db.execute("SELECT * FROM events").fetchall()
    scored_at = utc_now()
    for row in rows:
        result = score_event(row, config)
        c = result["components"]
        db.execute(
            """
            INSERT INTO event_scores (
              event_id, impact_score, novelty, audience_relevance,
              market_importance, proof_available, visual_potential,
              search_demand, tension, saturation_penalty, uncertainty_penalty,
              reasons_json, scored_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
              impact_score = excluded.impact_score,
              novelty = excluded.novelty,
              audience_relevance = excluded.audience_relevance,
              market_importance = excluded.market_importance,
              proof_available = excluded.proof_available,
              visual_potential = excluded.visual_potential,
              search_demand = excluded.search_demand,
              tension = excluded.tension,
              saturation_penalty = excluded.saturation_penalty,
              uncertainty_penalty = excluded.uncertainty_penalty,
              reasons_json = excluded.reasons_json,
              scored_at = excluded.scored_at
            """,
            (
                row["event_id"],
                result["impact_score"],
                c["novelty"],
                c["audience_relevance"],
                c["market_importance"],
                c["proof_available"],
                c["visual_potential"],
                c["search_demand"],
                c["tension"],
                c["saturation_penalty"],
                c["uncertainty_penalty"],
                json.dumps(result["reasons"]),
                scored_at,
            ),
        )
    db.commit()
    return len(rows)


def top_candidates(db: sqlite3.Connection, limit: int) -> list[sqlite3.Row]:
    return db.execute(
        """
        SELECT e.*, s.impact_score, s.reasons_json, s.visual_potential,
               s.proof_available, s.uncertainty_penalty
        FROM events e
        JOIN event_scores s ON s.event_id = e.event_id
        ORDER BY s.impact_score DESC, e.first_seen_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def visual_cues_for(row: sqlite3.Row) -> list[str]:
    url = row["url"]
    title = row["title"]
    cues = [f"{{{{ASSET: source.screenshot_url URL: {url} WRAP: browserFrame}}}}"]
    if row["source_type"] == "youtube":
        cues.append(f"{{{{ASSET: youtube.video-card URL: {url} WRAP: screenshotFrame}}}}")
    if "github" in url.lower() or "github" in title.lower():
        cues.append(f"{{{{ASSET: github.release-or-repo URL: {url} WRAP: screenshotFrame}}}}")
    cues.append("{{ASSET: keyadvances.explainer-diagram WRAP: screenshotFrame}}")
    return cues


def write_research_pack(row: sqlite3.Row, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    reasons = json.loads(row["reasons_json"])
    slug = slugify(row["title"])
    path = output_dir / f"{slug}.md"
    cues = "\n".join(f"- `{cue}`" for cue in visual_cues_for(row))
    summary = row["summary"] or "Summary not available yet. Pull transcript/article content in the next enrichment phase."
    if len(summary) > 1400:
        summary = summary[:1400].rsplit(" ", 1)[0] + "..."
    md = f"""# Research Pack: {row['title']}

Generated: {utc_now()}

## Candidate

- Source: {row['source_name']} ({row['source_type']})
- URL: {row['url']}
- Published: {row['published_at'] or 'unknown'}
- Impact score: {row['impact_score']}
- Reasons: {', '.join(reasons)}

## What Happened

{summary}

## Why It Might Matter

- Potentially relevant to AI automation, agentic workflows, AI assistants, or current product developments.
- Verify the source directly before scripting claims.
- Compare against competitor coverage before deciding whether to publish.

## Proof To Gather

- Primary source page or announcement.
- Product screenshots, changelog, docs, GitHub release, or demo material.
- If sourced from YouTube, transcript excerpts and the creator's core angle.
- Independent confirmation from official/company/repo sources when possible.

## Suggested Video Angle

{suggest_angle(row)}

## Visual Cues

{cues}

## Script Skeleton

1. Cold open: what changed and why viewers should care.
2. Source proof: show the original page/video/release.
3. Breakdown: what is new, who it affects, and what workflows it enables.
4. Skeptic check: what is unproven, missing, or likely overstated.
5. Verdict: what builders/creators/businesses should watch next.
"""
    path.write_text(md)
    return path


def suggest_angle(row: sqlite3.Row) -> str:
    text = f"{row['title']} {row['summary']}".lower()
    if "agent" in text or "mcp" in text or "automation" in text:
        return "Frame this as a practical agent-workflow update: what the tool changes, where it fits, and whether it reduces real work."
    if "model" in text or "gpt" in text or "claude" in text or "gemini" in text:
        return "Frame this as a model capability update: what changed, what evidence exists, and which use cases become more realistic."
    if row["source_type"] == "youtube":
        return "Frame this as competitor intelligence: extract the useful claim, verify it from primary sources, then produce a clearer Keyadvances version."
    return "Frame this as an AI product/current-events explainer with source proof and a clear builder/business takeaway."


def generate_research_packs(db: sqlite3.Connection, output_dir: Path, limit: int) -> list[Path]:
    paths = []
    for row in top_candidates(db, limit):
        paths.append(write_research_pack(row, output_dir))
    return paths


def export_candidates(db: sqlite3.Connection, output_path: Path, limit: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = top_candidates(db, limit)
    payload = []
    for row in rows:
        payload.append({k: row[k] for k in row.keys() if k != "raw_payload_json"})
    output_path.write_text(json.dumps(payload, indent=2) + "\n")


def load_youtube_registry(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f)


def build_youtube_transcript_queue(
    registry_path: Path,
    output_path: Path,
    cadence: str = "daily",
) -> list[dict[str, Any]]:
    registry = load_youtube_registry(registry_path)
    policy = registry.get("monitoring_policy", {}).get(cadence, {})
    priorities = set(policy.get("priority", [1]))
    queue = []
    for channel in registry.get("channels", []):
        if channel.get("priority") not in priorities:
            continue
        if not channel.get("channel_id"):
            continue
        queue.append(
            {
                "name": channel["name"],
                "channel_url": channel["channel_url"],
                "channel_id": channel["channel_id"],
                "category": channel.get("category", "unknown"),
                "priority": channel.get("priority", 2),
                "lookback_hours": policy.get("lookback_hours", 30),
                "max_new_videos": policy.get("max_new_videos_per_channel", 3),
                "transcript_strategy": policy.get("transcript_strategy", "captions_first_audio_fallback"),
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(queue, indent=2) + "\n")
    return queue


def export_youtube_monitor_config(registry_path: Path, output_path: Path) -> None:
    registry = load_youtube_registry(registry_path)
    categories: dict[str, list[dict[str, str]]] = {"keyadvances_daily": [], "keyadvances_weekly": []}
    for channel in registry.get("channels", []):
        if not channel.get("channel_id"):
            continue
        target = "keyadvances_daily" if channel.get("priority") == 1 else "keyadvances_weekly"
        categories[target].append(
            {
                "name": channel["name"],
                "channel_id": channel["channel_id"],
                "focus": channel.get("rationale", channel.get("category", "")),
            }
        )

    payload = {
        "categories": categories,
        "filters": {
            "min_duration_seconds": 120,
            "max_duration_seconds": 7200,
            "exclude_keywords": ["LIVE", "livestream", "podcast"],
            "priority_keywords": [
                "agent",
                "agentic",
                "automation",
                "Claude",
                "GPT",
                "Gemini",
                "MCP",
                "new model",
                "released",
            ],
        },
        "report": {
            "max_videos_per_channel": 3,
            "max_total_videos": 40,
            "sort_by": "engagement",
            "include_stats": True,
            "include_description": True,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Keyadvances newsroom pipeline")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize the event database")

    rss = sub.add_parser("ingest-rss", help="Fetch RSS sources into the event store")
    rss.add_argument("--config", type=Path, default=DEFAULT_RSS_CONFIG)
    rss.add_argument("--limit-sources", type=int)
    rss.add_argument("--max-days", type=int, default=14)

    yt = sub.add_parser("ingest-youtube-report", help="Ingest a YouTube markdown report")
    yt.add_argument("--report", type=Path)
    yt.add_argument("--report-dir", type=Path, default=DEFAULT_YOUTUBE_REPORT_DIR)

    score = sub.add_parser("score", help="Score all events")
    score.add_argument("--config", type=Path, default=DEFAULT_SCORING_CONFIG)

    packs = sub.add_parser("research-packs", help="Generate research packs for top candidates")
    packs.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUTS / "research-packs")
    packs.add_argument("--limit", type=int, default=5)
    packs.add_argument("--candidates-json", type=Path, default=DEFAULT_OUTPUTS / "candidates.json")

    yt_queue = sub.add_parser("youtube-transcript-queue", help="Export daily/weekly transcript queue from channel registry")
    yt_queue.add_argument("--registry", type=Path, default=DEFAULT_YOUTUBE_CHANNELS)
    yt_queue.add_argument("--cadence", choices=["daily", "weekly"], default="daily")
    yt_queue.add_argument("--output", type=Path, default=DEFAULT_OUTPUTS / "youtube-transcript-queue.json")

    yt_config = sub.add_parser("export-youtube-monitor-config", help="Export API-ready YouTube monitor config")
    yt_config.add_argument("--registry", type=Path, default=DEFAULT_YOUTUBE_CHANNELS)
    yt_config.add_argument("--output", type=Path, default=DEFAULT_OUTPUTS / "keyadvances-youtube-monitor.yaml")

    daily = sub.add_parser("run-daily", help="Run RSS, latest YouTube report ingestion, scoring, and packs")
    daily.add_argument("--limit-rss-sources", type=int)
    daily.add_argument("--max-days", type=int, default=14)
    daily.add_argument("--pack-limit", type=int, default=5)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    db = connect(args.db)

    if args.command == "init":
        print(f"initialized {args.db}")
    elif args.command == "ingest-rss":
        count = ingest_rss(db, args.config, args.limit_sources, args.max_days)
        print(f"rss events upserted: {count}")
    elif args.command == "ingest-youtube-report":
        report = args.report or latest_youtube_report(args.report_dir)
        if not report:
            raise SystemExit(f"No YouTube report found in {args.report_dir}")
        count = ingest_youtube_report(db, report)
        print(f"youtube events upserted: {count} from {report}")
    elif args.command == "score":
        count = score_events(db, args.config)
        print(f"events scored: {count}")
    elif args.command == "research-packs":
        paths = generate_research_packs(db, args.output_dir, args.limit)
        export_candidates(db, args.candidates_json, args.limit)
        print(f"research packs generated: {len(paths)}")
        for path in paths:
            print(path)
    elif args.command == "youtube-transcript-queue":
        queue = build_youtube_transcript_queue(args.registry, args.output, args.cadence)
        print(f"youtube transcript queue exported: {len(queue)} channels -> {args.output}")
    elif args.command == "export-youtube-monitor-config":
        export_youtube_monitor_config(args.registry, args.output)
        print(f"youtube monitor config exported -> {args.output}")
    elif args.command == "run-daily":
        rss_count = ingest_rss(db, DEFAULT_RSS_CONFIG, args.limit_rss_sources, args.max_days)
        report = latest_youtube_report(DEFAULT_YOUTUBE_REPORT_DIR)
        yt_count = ingest_youtube_report(db, report) if report else 0
        scored = score_events(db, DEFAULT_SCORING_CONFIG)
        build_youtube_transcript_queue(
            DEFAULT_YOUTUBE_CHANNELS,
            DEFAULT_OUTPUTS / "youtube-transcript-queue.json",
            "daily",
        )
        packs = generate_research_packs(db, DEFAULT_OUTPUTS / "research-packs", args.pack_limit)
        export_candidates(db, DEFAULT_OUTPUTS / "candidates.json", args.pack_limit)
        print(
            f"daily run complete: rss={rss_count}, youtube={yt_count}, "
            f"scored={scored}, packs={len(packs)}"
        )


if __name__ == "__main__":
    main()
