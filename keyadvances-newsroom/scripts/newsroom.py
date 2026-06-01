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
import os
import re
import sqlite3
import subprocess
import textwrap
import time
import urllib.parse
import urllib.error
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
DEFAULT_SCRIPT_DIR = DEFAULT_OUTPUTS / "scripts"
DEFAULT_ASSET_MANIFEST_DIR = DEFAULT_OUTPUTS / "asset-manifests"
DEFAULT_RSS_CONFIG = ROOT.parent / "skills" / "news-aggregator" / "config" / "rss-feeds.json"
DEFAULT_EXTERNAL_SOURCES = ROOT / "sources" / "external-sources.yaml"
DEFAULT_YOUTUBE_REPORT_DIR = ROOT.parent / "skills" / "youtube-monitor" / "reports" / "daily"
DEFAULT_SCORING_CONFIG = ROOT / "config" / "scoring.yaml"
DEFAULT_YOUTUBE_CHANNELS = ROOT / "sources" / "youtube-channels.yaml"
DEFAULT_TRANSCRIPT_DIR = ROOT / "data" / "youtube-transcripts"
DEFAULT_AUDIO_DIR = ROOT / "data" / "youtube-audio"
DEFAULT_WHISPER_MODEL = Path.home() / ".whisper-models" / "ggml-base.en.bin"


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

CREATE TABLE IF NOT EXISTS youtube_transcripts (
  video_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  channel_name TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  transcript_path TEXT,
  transcript_chars INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,
  fetched_at TEXT NOT NULL,
  error TEXT DEFAULT '',
  FOREIGN KEY(event_id) REFERENCES events(event_id)
);

CREATE TABLE IF NOT EXISTS video_drafts (
  draft_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  title TEXT NOT NULL,
  script_path TEXT NOT NULL,
  script_json_path TEXT NOT NULL,
  asset_manifest_path TEXT NOT NULL,
  target_duration_seconds INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(event_id) REFERENCES events(event_id)
);
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


def fetch_json(url: str, timeout: int = 20) -> Any:
    return json.loads(fetch_url(url, timeout).decode("utf-8"))


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int = 30) -> Any:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "KeyadvancesNewsroom/0.1 (+https://youtube.com/@keyadvances)",
            **headers,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


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


def audit_rss_feeds(config_path: Path, max_days: int = 14) -> list[dict[str, Any]]:
    feeds = list(load_rss_config(config_path).items())
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    report = []
    for source_name, feed_url in feeds:
        item: dict[str, Any] = {
            "source": source_name,
            "url": feed_url,
            "ok": False,
            "entries": 0,
            "recent_entries": 0,
            "latest_published_at": None,
            "error": "",
        }
        try:
            entries = parse_feed_entries(fetch_url(feed_url), source_name)
            item["ok"] = True
            item["entries"] = len(entries)
            recent_entries = []
            latest: datetime | None = None
            for entry in entries:
                if not entry.published_at:
                    continue
                try:
                    published = datetime.fromisoformat(entry.published_at)
                except ValueError:
                    continue
                latest = max(latest, published) if latest else published
                if published >= cutoff:
                    recent_entries.append(entry)
            item["recent_entries"] = len(recent_entries)
            item["latest_published_at"] = latest.isoformat(timespec="seconds") if latest else None
        except Exception as exc:
            item["error"] = str(exc)
        report.append(item)
    return report


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


def load_external_sources(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f)


def iter_external_sources(
    registry_path: Path,
    source_type: str | None = None,
    categories: set[str] | None = None,
) -> list[dict[str, Any]]:
    registry = load_external_sources(registry_path)
    rows = []
    for category, sources in registry.get("sources", {}).items():
        if categories and category not in categories:
            continue
        for source in sources:
            if source_type and source.get("type") != source_type:
                continue
            row = dict(source)
            row["category"] = category
            rows.append(row)
    return rows


def ingest_reddit(
    db: sqlite3.Connection,
    registry_path: Path,
    max_days: int = 3,
    limit_sources: int | None = None,
    limit_posts: int = 25,
) -> int:
    sources = [
        s
        for s in iter_external_sources(registry_path, "api", {"communities"})
        if "reddit.com" in s.get("url", "")
    ]
    if limit_sources:
        sources = sources[:limit_sources]

    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    inserted = 0
    for source in sources:
        url = source["url"]
        separator = "&" if "?" in url else "?"
        feed_url = f"{url}{separator}limit={limit_posts}"
        try:
            payload = fetch_json(feed_url)
        except Exception as exc:
            subreddit_match = re.search(r"reddit\.com/r/([^/]+)", url)
            if not subreddit_match:
                print(f"! Reddit fetch failed for {source['name']}: {exc}")
                continue
            rss_url = f"https://www.reddit.com/r/{subreddit_match.group(1)}/new/.rss"
            try:
                entries = parse_feed_entries(fetch_url(rss_url), source["name"])[:limit_posts]
            except Exception as rss_exc:
                print(f"! Reddit fetch failed for {source['name']}: json={exc}; rss={rss_exc}")
                continue
            for entry in entries:
                if entry.published_at:
                    try:
                        published = datetime.fromisoformat(entry.published_at)
                        if published < cutoff:
                            continue
                    except ValueError:
                        pass
                event = Event(
                    "reddit",
                    source["name"],
                    entry.title,
                    entry.url,
                    entry.summary,
                    entry.published_at,
                    {"source_category": source.get("category"), "fallback": "rss"},
                )
                inserted += int(upsert_event(db, event))
            continue

        children = payload.get("data", {}).get("children", [])
        for child in children:
            data = child.get("data", {})
            title = clean_text(data.get("title", ""))
            if not title:
                continue
            created = datetime.fromtimestamp(data.get("created_utc", 0), timezone.utc)
            if created < cutoff:
                continue
            permalink = data.get("permalink", "")
            comments_url = urllib.parse.urljoin("https://www.reddit.com", permalink)
            outbound_url = data.get("url_overridden_by_dest") or data.get("url") or comments_url
            summary = clean_text(data.get("selftext", ""))
            if not summary:
                summary = f"Reddit discussion with score {data.get('score', 0)} and {data.get('num_comments', 0)} comments."
            event = Event(
                "reddit",
                source["name"],
                title,
                comments_url,
                summary,
                created.isoformat(timespec="seconds"),
                {
                    "subreddit": data.get("subreddit"),
                    "score": data.get("score", 0),
                    "num_comments": data.get("num_comments", 0),
                    "outbound_url": outbound_url,
                    "source_category": source.get("category"),
                },
            )
            inserted += int(upsert_event(db, event))
    db.commit()
    return inserted


def ingest_github_trending(
    db: sqlite3.Connection,
    registry_path: Path,
    since: str = "daily",
    language: str = "",
) -> int:
    sources = [
        s
        for s in iter_external_sources(registry_path, "html", {"developer_and_agent_ecosystem"})
        if "github.com/trending" in s.get("url", "")
    ]
    if not sources:
        return 0
    query = {"since": since}
    base_url = sources[0]["url"].split("?", 1)[0]
    path = f"/{urllib.parse.quote(language.strip())}" if language.strip() else ""
    url = f"{base_url}{path}?{urllib.parse.urlencode(query)}"
    try:
        html_text = fetch_url(url).decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"! GitHub Trending fetch failed: {exc}")
        return 0

    articles = re.findall(r"<article\b.*?</article>", html_text, flags=re.DOTALL | re.IGNORECASE)
    inserted = 0
    for article in articles:
        link_match = re.search(r'<h2[^>]*>.*?<a[^>]+href="(?P<href>/[^"]+)"', article, flags=re.DOTALL)
        if not link_match:
            continue
        repo_path = clean_text(link_match.group("href").strip("/"))
        if "/" not in repo_path:
            continue
        desc_match = re.search(r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(?P<desc>.*?)</p>', article, flags=re.DOTALL)
        language_match = re.search(r'<span[^>]*itemprop="programmingLanguage"[^>]*>(?P<lang>.*?)</span>', article, flags=re.DOTALL)
        stars_match = re.search(r"(?P<stars>[\d,]+)\s+stars\s+today", clean_text(article), flags=re.IGNORECASE)
        description = clean_text(desc_match.group("desc")) if desc_match else ""
        repo_language = clean_text(language_match.group("lang")) if language_match else ""
        title = f"GitHub Trending: {repo_path}"
        summary_parts = []
        if description:
            summary_parts.append(description)
        if repo_language:
            summary_parts.append(f"Language: {repo_language}.")
        if stars_match:
            summary_parts.append(f"Stars today: {stars_match.group('stars')}.")
        event = Event(
            "github",
            "GitHub Trending",
            title,
            f"https://github.com/{repo_path}",
            " ".join(summary_parts),
            utc_now(),
            {
                "repo": repo_path,
                "language": repo_language,
                "stars_today": stars_match.group("stars") if stars_match else "",
                "since": since,
            },
        )
        inserted += int(upsert_event(db, event))
    db.commit()
    return inserted


def product_hunt_token(explicit_token: str | None = None, force_client_credentials: bool = False) -> str:
    if explicit_token:
        return explicit_token
    env = load_env(ROOT.parent / ".env")
    token = os.getenv("PRODUCT_HUNT_TOKEN") or env.get("PRODUCT_HUNT_TOKEN", "")
    if token and not force_client_credentials:
        return token

    client_id = os.getenv("PRODUCT_HUNT_CLIENT_ID") or env.get("PRODUCT_HUNT_CLIENT_ID", "")
    client_secret = os.getenv("PRODUCT_HUNT_CLIENT_SECRET") or env.get("PRODUCT_HUNT_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return ""

    try:
        payload = post_json(
            "https://api.producthunt.com/v2/oauth/token",
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            {},
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise SystemExit(
                "Product Hunt rejected PRODUCT_HUNT_CLIENT_ID/PRODUCT_HUNT_CLIENT_SECRET. "
                "Check that these are real API dashboard credentials, not the example values from the docs."
            ) from exc
        raise
    return payload.get("access_token", "")


def ingest_product_hunt(
    db: sqlite3.Connection,
    registry_path: Path,
    token: str | None = None,
    limit: int = 20,
) -> int:
    source = next(
        (
            s
            for s in iter_external_sources(registry_path, "api", {"news_and_aggregators"})
            if "producthunt.com" in s.get("url", "")
        ),
        None,
    )
    if not source:
        return 0
    bearer = product_hunt_token(token)
    if not bearer:
        raise SystemExit(
            "Product Hunt ingestion requires PRODUCT_HUNT_TOKEN or "
            "PRODUCT_HUNT_CLIENT_ID plus PRODUCT_HUNT_CLIENT_SECRET."
        )

    query = """
    query KeyadvancesProductHunt($first: Int!) {
      posts(first: $first) {
        edges {
          node {
            id
            name
            tagline
            description
            url
            votesCount
            commentsCount
            createdAt
          }
        }
      }
    }
    """
    request_payload = {"query": query, "variables": {"first": limit}}
    try:
        payload = post_json(source["url"], request_payload, {"Authorization": f"Bearer {bearer}"})
    except urllib.error.HTTPError as exc:
        if exc.code != 401 or token:
            raise
        refreshed = product_hunt_token(None, force_client_credentials=True)
        if not refreshed or refreshed == bearer:
            raise
        payload = post_json(source["url"], request_payload, {"Authorization": f"Bearer {refreshed}"})
    if payload.get("errors"):
        raise SystemExit(f"Product Hunt API error: {payload['errors']}")
    inserted = 0
    edges = payload.get("data", {}).get("posts", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        name = clean_text(node.get("name", ""))
        if not name:
            continue
        tagline = clean_text(node.get("tagline", ""))
        description = clean_text(node.get("description", ""))
        summary = " ".join(part for part in [tagline, description] if part)
        event = Event(
            "product_hunt",
            source["name"],
            name,
            node.get("url", ""),
            summary,
            parse_date(node.get("createdAt")),
            {
                "product_hunt_id": node.get("id"),
                "votes": node.get("votesCount", 0),
                "comments": node.get("commentsCount", 0),
            },
        )
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
    proof_available = 0.85 if source_type in {"rss", "youtube", "github", "reddit", "product_hunt", "api"} else 0.55
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


def split_sentences(text: str, limit: int = 8) -> list[str]:
    clean = clean_text(text)
    if not clean:
        return []
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [p.strip() for p in parts if len(p.strip()) > 20][:limit]


def script_clean_text(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    blocked = [
        "join here",
        "get a free",
        "strategy session",
        "masterclass",
        "skool.com",
        "prompts",
        "opt-in",
        "subscribe",
    ]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    useful = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(term in lower for term in blocked):
            continue
        if len(sentence) < 20:
            continue
        useful.append(sentence.strip())
    return " ".join(useful) if useful else text


def candidate_summary(row: sqlite3.Row, max_sentences: int = 4) -> list[str]:
    summary = script_clean_text(row["summary"] or "")
    sentences = split_sentences(summary, max_sentences)
    if sentences:
        return sentences
    return [
        f"{row['title']} is a new candidate item from {row['source_name']}.",
        "The next step is to verify the primary source and decide whether it deserves a full Keyadvances video.",
    ]


def extract_transcript_excerpt(row: sqlite3.Row) -> str:
    summary = row["summary"] or ""
    marker = "Transcript excerpt:"
    if marker not in summary:
        return ""
    return script_clean_text(summary.split(marker, 1)[1])[:650]


def draft_video_sections(row: sqlite3.Row) -> list[dict[str, Any]]:
    title = row["title"]
    source = row["source_name"]
    summary = candidate_summary(row, 5)
    angle = suggest_angle(row)
    transcript_excerpt = extract_transcript_excerpt(row)
    cues = visual_cues_for(row)

    hook_title = title.rstrip(".!?")
    hook = (
        f"{hook_title}. That is the signal today. The question is not just whether it is interesting. "
        "The question is whether it changes a real workflow."
    )
    proof = (
        f"The source is {source}. Start by showing the original page or video, then separate what is confirmed "
        "from what still needs verification."
    )
    breakdown = " ".join(summary[:3])
    if transcript_excerpt:
        breakdown += f" Competitor transcript signal: {transcript_excerpt}"
    why = (
        f"{angle} For Keyadvances, the useful part is the practical consequence: who can use this, "
        "what gets faster, and what becomes easier to automate."
    )
    skeptic = (
        "The caution is simple: do not repeat the headline as fact until the primary source, docs, release notes, "
        "or product page confirms it. If the claim is only from a creator video, treat it as a lead."
    )
    verdict = (
        "The draft verdict: this is worth tracking if the proof is strong and the visuals can show the change clearly. "
        "Next, capture the source page, any product or GitHub evidence, and build the final script around those receipts."
    )

    return [
        {
            "id": "cold-open",
            "target_seconds": 18,
            "voiceover": hook,
            "visual_cues": [cues[0], "{{ASSET: keyadvances.title-card WRAP: screenshotFrame}}"],
        },
        {
            "id": "source-proof",
            "target_seconds": 28,
            "voiceover": proof,
            "visual_cues": cues[:2],
        },
        {
            "id": "breakdown",
            "target_seconds": 55,
            "voiceover": breakdown,
            "visual_cues": cues,
        },
        {
            "id": "why-it-matters",
            "target_seconds": 40,
            "voiceover": why,
            "visual_cues": ["{{ASSET: keyadvances.impact-map WRAP: screenshotFrame}}", cues[-1]],
        },
        {
            "id": "skeptic-check",
            "target_seconds": 30,
            "voiceover": skeptic,
            "visual_cues": ["{{ASSET: keyadvances.claim-check WRAP: screenshotFrame}}", cues[0]],
        },
        {
            "id": "verdict",
            "target_seconds": 25,
            "voiceover": verdict,
            "visual_cues": ["{{ASSET: keyadvances.verdict-card WRAP: screenshotFrame}}"],
        },
    ]


ASSET_CUE_RE = re.compile(
    r"\{\{ASSET:\s*(?P<asset>[^\s}]+)(?:\s+URL:\s*(?P<url>\S+))?(?:\s+WRAP:\s*(?P<wrap>\w+))?\s*\}\}"
)


def asset_capture_manifest(row: sqlite3.Row, sections: list[dict[str, Any]]) -> dict[str, Any]:
    assets: dict[str, dict[str, Any]] = {}
    for section in sections:
        for cue in section["visual_cues"]:
            match = ASSET_CUE_RE.search(cue)
            if not match:
                continue
            asset_id = match.group("asset")
            url = match.group("url") or row["url"]
            wrap = match.group("wrap") or "screenshotFrame"
            if asset_id in assets:
                continue
            capture_type = "synthetic"
            if asset_id.startswith("source.") or asset_id.startswith("youtube.") or asset_id.startswith("github."):
                capture_type = "screenshot"
            if "scroll" in asset_id:
                capture_type = "scroll-video"
            assets[asset_id] = {
                "asset_id": asset_id,
                "capture_type": capture_type,
                "source_url": url,
                "wrap": wrap,
                "status": "pending",
            }
    return {
        "event_id": row["event_id"],
        "title": row["title"],
        "source": {"type": row["source_type"], "name": row["source_name"], "url": row["url"]},
        "assets": list(assets.values()),
    }


def write_script_draft(
    db: sqlite3.Connection,
    row: sqlite3.Row,
    script_dir: Path,
    manifest_dir: Path,
) -> dict[str, Path]:
    script_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(row["title"])
    draft_id = f"draft-{row['event_id']}"
    sections = draft_video_sections(row)
    target_duration = sum(s["target_seconds"] for s in sections)
    manifest = asset_capture_manifest(row, sections)

    script_path = script_dir / f"{slug}.md"
    json_path = script_dir / f"{slug}.json"
    manifest_path = manifest_dir / f"{slug}.asset-manifest.json"

    md_lines = [
        f"# Keyadvances Draft Script: {row['title']}",
        "",
        f"Generated: {utc_now()}",
        f"Source: {row['source_name']} ({row['source_type']})",
        f"URL: {row['url']}",
        f"Target duration: {target_duration} seconds",
        "",
        "## Editorial Angle",
        "",
        suggest_angle(row),
        "",
        "## Script",
        "",
    ]
    for section in sections:
        md_lines.extend(
            [
                f"### {section['id']} ({section['target_seconds']}s)",
                "",
                section["voiceover"],
                "",
                "Visual cues:",
            ]
        )
        md_lines.extend(f"- `{cue}`" for cue in section["visual_cues"])
        md_lines.append("")
    script_path.write_text("\n".join(md_lines).strip() + "\n")

    json_payload = {
        "draft_id": draft_id,
        "event_id": row["event_id"],
        "title": row["title"],
        "source_url": row["url"],
        "target_duration_seconds": target_duration,
        "sections": sections,
        "asset_manifest": str(manifest_path),
    }
    json_path.write_text(json.dumps(json_payload, indent=2) + "\n")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    db.execute(
        """
        INSERT INTO video_drafts (
          draft_id, event_id, title, script_path, script_json_path,
          asset_manifest_path, target_duration_seconds, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(draft_id) DO UPDATE SET
          script_path = excluded.script_path,
          script_json_path = excluded.script_json_path,
          asset_manifest_path = excluded.asset_manifest_path,
          target_duration_seconds = excluded.target_duration_seconds,
          created_at = excluded.created_at
        """,
        (
            draft_id,
            row["event_id"],
            row["title"],
            str(script_path),
            str(json_path),
            str(manifest_path),
            target_duration,
            utc_now(),
        ),
    )
    db.commit()
    return {"script": script_path, "json": json_path, "manifest": manifest_path}


def generate_script_drafts(
    db: sqlite3.Connection,
    script_dir: Path,
    manifest_dir: Path,
    limit: int,
) -> list[dict[str, Path]]:
    outputs = []
    for row in top_candidates(db, limit):
        outputs.append(write_script_draft(db, row, script_dir, manifest_dir))
    return outputs


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
        cap_key = "max_new_videos_per_day" if cadence == "daily" else "max_new_videos_per_week"
        queue.append(
            {
                "name": channel["name"],
                "channel_url": channel["channel_url"],
                "channel_id": channel["channel_id"],
                "category": channel.get("category", "unknown"),
                "priority": channel.get("priority", 2),
                "lookback_hours": policy.get("lookback_hours", 30),
                "max_new_videos": channel.get(cap_key, policy.get("max_new_videos_per_channel", 5)),
                "transcript_strategy": policy.get("transcript_strategy", "captions_first_audio_fallback"),
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(queue, indent=2) + "\n")
    return queue


def export_youtube_monitor_config(registry_path: Path, output_path: Path) -> None:
    registry = load_youtube_registry(registry_path)
    categories: dict[str, list[dict[str, str]]] = {"keyadvances_daily": [], "keyadvances_weekly": []}
    daily_priorities = set(registry.get("monitoring_policy", {}).get("daily", {}).get("priority", [1]))
    weekly_priorities = set(registry.get("monitoring_policy", {}).get("weekly", {}).get("priority", []))
    max_channel_cap = 5
    for channel in registry.get("channels", []):
        if not channel.get("channel_id"):
            continue
        targets = []
        if channel.get("priority") in daily_priorities:
            targets.append("keyadvances_daily")
        if channel.get("priority") in weekly_priorities:
            targets.append("keyadvances_weekly")
        for target in targets:
            cap = channel.get(
                "max_new_videos_per_day" if target == "keyadvances_daily" else "max_new_videos_per_week",
                registry.get("monitoring_policy", {})
                .get("daily" if target == "keyadvances_daily" else "weekly", {})
                .get("max_new_videos_per_channel", 5),
            )
            max_channel_cap = max(max_channel_cap, cap)
            categories[target].append(
                {
                    "name": channel["name"],
                    "channel_id": channel["channel_id"],
                    "max_new_videos": cap,
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
            "max_videos_per_channel": max_channel_cap,
            "max_total_videos": 200,
            "sort_by": "engagement",
            "include_stats": True,
            "include_description": True,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False))


def export_audio_fallback_queue(db: sqlite3.Connection, output_path: Path, limit: int = 25) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT yt.*, e.raw_payload_json, e.published_at
        FROM youtube_transcripts yt
        JOIN events e ON e.event_id = yt.event_id
        WHERE yt.status NOT IN ('cached', 'fetched_api', 'fetched_ytdlp')
        ORDER BY e.published_at DESC, yt.fetched_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    queue: list[dict[str, Any]] = []
    for row in rows:
        raw = json.loads(row["raw_payload_json"] or "{}")
        queue.append(
            {
                "video_id": row["video_id"],
                "title": row["title"],
                "channel_name": row["channel_name"],
                "url": row["url"],
                "published_at": row["published_at"],
                "duration_seconds": raw.get("duration_seconds"),
                "target_transcript_path": str(
                    DEFAULT_TRANSCRIPT_DIR
                    / f"{row['video_id']}-{slugify(row['title'], 52)}.txt"
                ),
                "preferred_fallback": "audio_download_then_whisper_or_assemblyai",
                "caption_failure": row["error"],
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(queue, indent=2) + "\n")
    return queue


def download_youtube_audio(video_id: str, title: str, audio_dir: Path) -> Path:
    audio_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(audio_dir.glob(f"{video_id}.*"))
    for path in existing:
        if path.suffix.lower() in {".wav", ".m4a", ".mp3"} and path.stat().st_size > 0:
            return path
    output_template = str(audio_dir / f"{video_id}.%(ext)s")
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format",
        "wav",
        "--audio-quality",
        "5",
        "--output",
        output_template,
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if result.returncode != 0:
        raise RuntimeError(clean_text(result.stderr or result.stdout)[:700])
    wav = audio_dir / f"{video_id}.wav"
    if wav.exists() and wav.stat().st_size > 0:
        return wav
    candidates = sorted(audio_dir.glob(f"{video_id}.*"), key=lambda p: p.stat().st_size, reverse=True)
    if not candidates:
        raise RuntimeError("yt-dlp completed but no audio file was produced")
    return candidates[0]


def whisper_transcribe(audio_path: Path, output_stem: Path, model_path: Path) -> str:
    if not model_path.exists():
        raise RuntimeError(f"Whisper model not found: {model_path}")
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "whisper-cli",
        "-m",
        str(model_path),
        "-f",
        str(audio_path),
        "--output-txt",
        "--output-file",
        str(output_stem),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if result.returncode != 0:
        raise RuntimeError(clean_text(result.stderr or result.stdout)[:700])
    txt_path = output_stem.with_suffix(".txt")
    if not txt_path.exists():
        raise RuntimeError("whisper-cli completed but no transcript txt was produced")
    return clean_text(txt_path.read_text(errors="ignore"))


def process_audio_fallbacks(
    db: sqlite3.Connection,
    limit: int,
    audio_dir: Path,
    transcript_dir: Path,
    model_path: Path,
) -> dict[str, int]:
    rows = db.execute(
        """
        SELECT yt.*, e.raw_payload_json
        FROM youtube_transcripts yt
        JOIN events e ON e.event_id = yt.event_id
        WHERE yt.status NOT IN ('cached', 'fetched_api', 'fetched_ytdlp', 'audio_whisper')
        ORDER BY yt.fetched_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    stats = {"queued": len(rows), "transcribed": 0, "failed": 0}
    for row in rows:
        target = transcript_dir / f"{row['video_id']}-{slugify(row['title'], 52)}.txt"
        try:
            audio_path = download_youtube_audio(row["video_id"], row["title"], audio_dir)
            text = whisper_transcribe(
                audio_path,
                transcript_dir / ".whisper" / f"{row['video_id']}-{slugify(row['title'], 52)}",
                model_path,
            )
            if not text:
                raise RuntimeError("whisper transcript was empty")
            transcript_dir.mkdir(parents=True, exist_ok=True)
            target.write_text(text + "\n")
            db.execute(
                """
                UPDATE youtube_transcripts
                SET transcript_path = ?, transcript_chars = ?, status = ?,
                    fetched_at = ?, error = ''
                WHERE video_id = ?
                """,
                (str(target), len(text), "audio_whisper", utc_now(), row["video_id"]),
            )
            excerpt = text[:900]
            db.execute(
                """
                UPDATE events
                SET summary = CASE
                  WHEN summary LIKE '%Transcript excerpt:%' THEN summary
                  ELSE summary || char(10) || char(10) || 'Transcript excerpt: ' || ?
                END
                WHERE event_id = ?
                """,
                (excerpt, row["event_id"]),
            )
            stats["transcribed"] += 1
        except Exception as exc:
            db.execute(
                """
                UPDATE youtube_transcripts
                SET status = ?, fetched_at = ?, error = ?
                WHERE video_id = ?
                """,
                ("audio_failed", utc_now(), str(exc)[:700], row["video_id"]),
            )
            stats["failed"] += 1
    db.commit()
    return stats


def youtube_api_key(explicit_key: str | None = None) -> str:
    if explicit_key:
        return explicit_key
    env = load_env(ROOT.parent / "agent-sdk" / ".env")
    env.update(load_env(ROOT.parent / ".env"))
    key = env.get("YOUTUBE_API_KEY")
    if not key:
        raise SystemExit("YOUTUBE_API_KEY not found in agent-sdk/.env or repo .env")
    return key


def youtube_api_get(api_key: str, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({**params, "key": api_key})
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?{query}"
    return json.loads(fetch_url(url, timeout=30).decode("utf-8"))


def parse_iso8601_duration(value: str) -> int:
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def discover_channel_videos(
    api_key: str,
    channel: dict[str, Any],
    lookback_hours: int,
    max_results: int,
) -> list[dict[str, Any]]:
    published_after = (
        datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    ).isoformat(timespec="seconds").replace("+00:00", "Z")
    search = youtube_api_get(
        api_key,
        "search",
        {
            "part": "snippet",
            "channelId": channel["channel_id"],
            "publishedAfter": published_after,
            "type": "video",
            "order": "date",
            "maxResults": max_results,
        },
    )
    ids = [item["id"]["videoId"] for item in search.get("items", []) if item.get("id", {}).get("videoId")]
    if not ids:
        return []
    details = youtube_api_get(
        api_key,
        "videos",
        {
            "part": "snippet,contentDetails,statistics",
            "id": ",".join(ids),
            "maxResults": len(ids),
        },
    )
    videos = []
    for item in details.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        duration_seconds = parse_iso8601_duration(item.get("contentDetails", {}).get("duration", ""))
        videos.append(
            {
                "video_id": item["id"],
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "published_at": parse_date(snippet.get("publishedAt")),
                "channel_title": snippet.get("channelTitle") or channel["name"],
                "channel_id": channel["channel_id"],
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "thumbnail": (snippet.get("thumbnails", {}).get("high") or {}).get("url", ""),
                "duration_seconds": duration_seconds,
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
            }
        )
    return videos


def vtt_to_text(path: Path) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "Kind:", "Language:")):
            continue
        if "-->" in line or re.fullmatch(r"\d+", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = clean_text(line)
        if not line or line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return "\n".join(lines).strip()


def fetch_transcript_api_text(video_id: str) -> tuple[str, str]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return "", "youtube-transcript-api is not installed"

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        snippets = []
        for item in transcript:
            text = getattr(item, "text", None)
            if text is None and isinstance(item, dict):
                text = item.get("text")
            if text:
                snippets.append(clean_text(text))
        return "\n".join(snippets).strip(), ""
    except Exception as exc:
        return "", f"{type(exc).__name__}: {str(exc)[:500]}"


def fetch_youtube_transcript(video_id: str, title: str, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title, 52)
    txt_path = output_dir / f"{video_id}-{slug}.txt"
    if txt_path.exists() and txt_path.stat().st_size > 0:
        return {"status": "cached", "path": str(txt_path), "chars": txt_path.stat().st_size, "error": ""}

    api_text, api_error = fetch_transcript_api_text(video_id)
    if api_text:
        txt_path.write_text(api_text + "\n")
        return {"status": "fetched_api", "path": str(txt_path), "chars": len(api_text), "error": ""}

    tmp_dir = output_dir / ".tmp" / video_id
    tmp_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        "en,en-US,en.*",
        "--sub-format",
        "vtt",
        "--output",
        str(tmp_dir / "%(id)s.%(ext)s"),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if result.returncode != 0:
        return {
            "status": "failed",
            "path": "",
            "chars": 0,
            "error": clean_text(api_error + " | " + (result.stderr or result.stdout))[:500],
        }

    vtts = sorted(tmp_dir.glob("*.vtt"), key=lambda p: p.stat().st_size, reverse=True)
    if not vtts:
        return {"status": "missing", "path": "", "chars": 0, "error": api_error or "No VTT subtitles produced"}

    text = vtt_to_text(vtts[0])
    if not text:
        return {"status": "empty", "path": "", "chars": 0, "error": api_error or "Subtitle file produced no text"}
    txt_path.write_text(text + "\n")
    return {"status": "fetched_ytdlp", "path": str(txt_path), "chars": len(text), "error": ""}


def store_youtube_transcript(
    db: sqlite3.Connection,
    event_id: str,
    video: dict[str, Any],
    transcript: dict[str, Any],
) -> None:
    db.execute(
        """
        INSERT INTO youtube_transcripts (
          video_id, event_id, channel_name, title, url, transcript_path,
          transcript_chars, status, fetched_at, error
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
          event_id = excluded.event_id,
          transcript_path = excluded.transcript_path,
          transcript_chars = excluded.transcript_chars,
          status = excluded.status,
          fetched_at = excluded.fetched_at,
          error = excluded.error
        """,
        (
            video["video_id"],
            event_id,
            video["channel_title"],
            video["title"],
            video["url"],
            transcript.get("path", ""),
            transcript.get("chars", 0),
            transcript.get("status", "unknown"),
            utc_now(),
            transcript.get("error", ""),
        ),
    )


def ingest_youtube_competitors(
    db: sqlite3.Connection,
    registry_path: Path,
    cadence: str,
    fetch_transcripts: bool,
    transcript_dir: Path,
    api_key_value: str | None = None,
    max_channels: int | None = None,
) -> dict[str, int]:
    api_key = youtube_api_key(api_key_value)
    queue = build_youtube_transcript_queue(
        registry_path,
        DEFAULT_OUTPUTS / "youtube-transcript-queue.json",
        cadence,
    )
    if max_channels:
        queue = queue[:max_channels]

    stats = {"channels": len(queue), "videos": 0, "events": 0, "transcripts": 0, "transcript_failures": 0}
    for channel in queue:
        videos = discover_channel_videos(
            api_key,
            channel,
            channel["lookback_hours"],
            channel["max_new_videos"],
        )
        for video in videos:
            if not (120 <= video["duration_seconds"] <= 7200):
                continue
            summary = video["description"][:1200]
            raw = {
                "video_id": video["video_id"],
                "channel_id": video["channel_id"],
                "thumbnail": video["thumbnail"],
                "duration_seconds": video["duration_seconds"],
                "views": video["views"],
                "likes": video["likes"],
                "comments": video["comments"],
                "registry_category": channel["category"],
            }
            transcript = {"status": "not_requested", "path": "", "chars": 0, "error": ""}
            if fetch_transcripts:
                transcript = fetch_youtube_transcript(video["video_id"], video["title"], transcript_dir)
                raw["transcript"] = transcript
                ok_statuses = {"cached", "fetched_api", "fetched_ytdlp"}
                stats["transcripts"] += int(transcript["status"] in ok_statuses)
                stats["transcript_failures"] += int(transcript["status"] not in ok_statuses)
                if transcript.get("path"):
                    try:
                        transcript_excerpt = Path(transcript["path"]).read_text(errors="ignore")[:900]
                        summary = f"{summary}\n\nTranscript excerpt: {transcript_excerpt}"
                    except OSError:
                        pass

            event = Event(
                "youtube",
                video["channel_title"],
                video["title"],
                video["url"],
                summary,
                video["published_at"],
                raw,
            )
            inserted = upsert_event(db, event)
            event_id = event_id_for(event)
            if fetch_transcripts:
                store_youtube_transcript(db, event_id, video, transcript)
            stats["videos"] += 1
            stats["events"] += int(inserted)
    db.commit()
    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Keyadvances newsroom pipeline")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize the event database")

    rss = sub.add_parser("ingest-rss", help="Fetch RSS sources into the event store")
    rss.add_argument("--config", type=Path, default=DEFAULT_RSS_CONFIG)
    rss.add_argument("--limit-sources", type=int)
    rss.add_argument("--max-days", type=int, default=14)

    rss_audit = sub.add_parser("audit-rss", help="Check RSS feed health and recency")
    rss_audit.add_argument("--config", type=Path, default=DEFAULT_RSS_CONFIG)
    rss_audit.add_argument("--max-days", type=int, default=14)
    rss_audit.add_argument("--output", type=Path)

    reddit = sub.add_parser("ingest-reddit", help="Fetch Reddit community sources into the event store")
    reddit.add_argument("--registry", type=Path, default=DEFAULT_EXTERNAL_SOURCES)
    reddit.add_argument("--max-days", type=int, default=3)
    reddit.add_argument("--limit-sources", type=int)
    reddit.add_argument("--limit-posts", type=int, default=25)

    github_trending = sub.add_parser("ingest-github-trending", help="Fetch GitHub Trending into the event store")
    github_trending.add_argument("--registry", type=Path, default=DEFAULT_EXTERNAL_SOURCES)
    github_trending.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily")
    github_trending.add_argument("--language", default="")

    product_hunt = sub.add_parser("ingest-product-hunt", help="Fetch Product Hunt launches into the event store")
    product_hunt.add_argument("--registry", type=Path, default=DEFAULT_EXTERNAL_SOURCES)
    product_hunt.add_argument("--token")
    product_hunt.add_argument("--limit", type=int, default=20)

    yt = sub.add_parser("ingest-youtube-report", help="Ingest a YouTube markdown report")
    yt.add_argument("--report", type=Path)
    yt.add_argument("--report-dir", type=Path, default=DEFAULT_YOUTUBE_REPORT_DIR)

    score = sub.add_parser("score", help="Score all events")
    score.add_argument("--config", type=Path, default=DEFAULT_SCORING_CONFIG)

    packs = sub.add_parser("research-packs", help="Generate research packs for top candidates")
    packs.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUTS / "research-packs")
    packs.add_argument("--limit", type=int, default=5)
    packs.add_argument("--candidates-json", type=Path, default=DEFAULT_OUTPUTS / "candidates.json")

    drafts = sub.add_parser("script-drafts", help="Generate draft scripts and asset manifests for top candidates")
    drafts.add_argument("--script-dir", type=Path, default=DEFAULT_SCRIPT_DIR)
    drafts.add_argument("--manifest-dir", type=Path, default=DEFAULT_ASSET_MANIFEST_DIR)
    drafts.add_argument("--limit", type=int, default=3)

    yt_queue = sub.add_parser("youtube-transcript-queue", help="Export daily/weekly transcript queue from channel registry")
    yt_queue.add_argument("--registry", type=Path, default=DEFAULT_YOUTUBE_CHANNELS)
    yt_queue.add_argument("--cadence", choices=["daily", "weekly"], default="daily")
    yt_queue.add_argument("--output", type=Path, default=DEFAULT_OUTPUTS / "youtube-transcript-queue.json")

    yt_config = sub.add_parser("export-youtube-monitor-config", help="Export API-ready YouTube monitor config")
    yt_config.add_argument("--registry", type=Path, default=DEFAULT_YOUTUBE_CHANNELS)
    yt_config.add_argument("--output", type=Path, default=DEFAULT_OUTPUTS / "keyadvances-youtube-monitor.yaml")

    audio_queue = sub.add_parser("audio-fallback-queue", help="Export videos whose caption transcript fetch failed")
    audio_queue.add_argument("--output", type=Path, default=DEFAULT_OUTPUTS / "audio-fallback-queue.json")
    audio_queue.add_argument("--limit", type=int, default=25)

    audio_fallback = sub.add_parser("process-audio-fallbacks", help="Download audio and transcribe failed caption fetches with whisper-cpp")
    audio_fallback.add_argument("--limit", type=int, default=3)
    audio_fallback.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    audio_fallback.add_argument("--transcript-dir", type=Path, default=DEFAULT_TRANSCRIPT_DIR)
    audio_fallback.add_argument("--model", type=Path, default=DEFAULT_WHISPER_MODEL)

    yt_competitors = sub.add_parser("ingest-youtube-competitors", help="Discover recent videos and fetch transcripts")
    yt_competitors.add_argument("--registry", type=Path, default=DEFAULT_YOUTUBE_CHANNELS)
    yt_competitors.add_argument("--cadence", choices=["daily", "weekly"], default="daily")
    yt_competitors.add_argument("--fetch-transcripts", action="store_true")
    yt_competitors.add_argument("--transcript-dir", type=Path, default=DEFAULT_TRANSCRIPT_DIR)
    yt_competitors.add_argument("--api-key")
    yt_competitors.add_argument("--max-channels", type=int)

    daily = sub.add_parser("run-daily", help="Run RSS, latest YouTube report ingestion, scoring, and packs")
    daily.add_argument("--limit-rss-sources", type=int)
    daily.add_argument("--max-days", type=int, default=14)
    daily.add_argument("--pack-limit", type=int, default=5)
    daily.add_argument("--youtube-transcripts", action="store_true")
    daily.add_argument("--process-audio-fallbacks", action="store_true")
    daily.add_argument("--max-youtube-channels", type=int)
    daily.add_argument("--script-drafts", action="store_true")
    daily.add_argument("--skip-reddit", action="store_true")
    daily.add_argument("--skip-github-trending", action="store_true")
    daily.add_argument("--product-hunt", action="store_true")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    db = connect(args.db)

    if args.command == "init":
        print(f"initialized {args.db}")
    elif args.command == "ingest-rss":
        count = ingest_rss(db, args.config, args.limit_sources, args.max_days)
        print(f"rss events upserted: {count}")
    elif args.command == "audit-rss":
        report = audit_rss_feeds(args.config, args.max_days)
        failed = [item for item in report if not item["ok"]]
        stale = [item for item in report if item["ok"] and item["recent_entries"] == 0]
        text = json.dumps(report, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text)
            print(f"rss audit written: {args.output}")
        else:
            print(text, end="")
        print(f"rss audit complete: feeds={len(report)}, failed={len(failed)}, stale={len(stale)}")
    elif args.command == "ingest-reddit":
        count = ingest_reddit(db, args.registry, args.max_days, args.limit_sources, args.limit_posts)
        print(f"reddit events upserted: {count}")
    elif args.command == "ingest-github-trending":
        count = ingest_github_trending(db, args.registry, args.since, args.language)
        print(f"github trending events upserted: {count}")
    elif args.command == "ingest-product-hunt":
        count = ingest_product_hunt(db, args.registry, args.token, args.limit)
        print(f"product hunt events upserted: {count}")
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
    elif args.command == "script-drafts":
        outputs = generate_script_drafts(db, args.script_dir, args.manifest_dir, args.limit)
        print(f"script drafts generated: {len(outputs)}")
        for item in outputs:
            print(item["script"])
            print(item["manifest"])
    elif args.command == "youtube-transcript-queue":
        queue = build_youtube_transcript_queue(args.registry, args.output, args.cadence)
        print(f"youtube transcript queue exported: {len(queue)} channels -> {args.output}")
    elif args.command == "export-youtube-monitor-config":
        export_youtube_monitor_config(args.registry, args.output)
        print(f"youtube monitor config exported -> {args.output}")
    elif args.command == "audio-fallback-queue":
        queue = export_audio_fallback_queue(db, args.output, args.limit)
        print(f"audio fallback queue exported: {len(queue)} videos -> {args.output}")
    elif args.command == "process-audio-fallbacks":
        stats = process_audio_fallbacks(
            db,
            args.limit,
            args.audio_dir,
            args.transcript_dir,
            args.model,
        )
        print(
            "audio fallback processing complete: "
            f"queued={stats['queued']}, transcribed={stats['transcribed']}, failed={stats['failed']}"
        )
    elif args.command == "ingest-youtube-competitors":
        stats = ingest_youtube_competitors(
            db,
            args.registry,
            args.cadence,
            args.fetch_transcripts,
            args.transcript_dir,
            args.api_key,
            args.max_channels,
        )
        print(
            "youtube competitor ingest complete: "
            f"channels={stats['channels']}, videos={stats['videos']}, "
            f"events={stats['events']}, transcripts={stats['transcripts']}, "
            f"transcript_failures={stats['transcript_failures']}"
        )
    elif args.command == "run-daily":
        rss_count = ingest_rss(db, DEFAULT_RSS_CONFIG, args.limit_rss_sources, args.max_days)
        reddit_count = 0 if args.skip_reddit else ingest_reddit(db, DEFAULT_EXTERNAL_SOURCES)
        github_count = 0 if args.skip_github_trending else ingest_github_trending(db, DEFAULT_EXTERNAL_SOURCES)
        product_hunt_count = 0
        if args.product_hunt:
            product_hunt_count = ingest_product_hunt(db, DEFAULT_EXTERNAL_SOURCES)
        report = latest_youtube_report(DEFAULT_YOUTUBE_REPORT_DIR)
        yt_count = ingest_youtube_report(db, report) if report else 0
        competitor_stats = ingest_youtube_competitors(
            db,
            DEFAULT_YOUTUBE_CHANNELS,
            "daily",
            args.youtube_transcripts,
            DEFAULT_TRANSCRIPT_DIR,
            None,
            args.max_youtube_channels,
        )
        scored = score_events(db, DEFAULT_SCORING_CONFIG)
        build_youtube_transcript_queue(
            DEFAULT_YOUTUBE_CHANNELS,
            DEFAULT_OUTPUTS / "youtube-transcript-queue.json",
            "daily",
        )
        export_audio_fallback_queue(db, DEFAULT_OUTPUTS / "audio-fallback-queue.json")
        audio_stats = {"queued": 0, "transcribed": 0, "failed": 0}
        if args.process_audio_fallbacks:
            audio_stats = process_audio_fallbacks(
                db,
                3,
                DEFAULT_AUDIO_DIR,
                DEFAULT_TRANSCRIPT_DIR,
                DEFAULT_WHISPER_MODEL,
            )
            scored = score_events(db, DEFAULT_SCORING_CONFIG)
        packs = generate_research_packs(db, DEFAULT_OUTPUTS / "research-packs", args.pack_limit)
        export_candidates(db, DEFAULT_OUTPUTS / "candidates.json", args.pack_limit)
        drafts = []
        if args.script_drafts:
            drafts = generate_script_drafts(
                db,
                DEFAULT_SCRIPT_DIR,
                DEFAULT_ASSET_MANIFEST_DIR,
                min(args.pack_limit, 3),
            )
        print(
            f"daily run complete: rss={rss_count}, reddit={reddit_count}, "
            f"github_trending={github_count}, product_hunt={product_hunt_count}, "
            f"youtube_report={yt_count}, "
            f"youtube_competitor_videos={competitor_stats['videos']}, "
            f"caption_transcripts={competitor_stats['transcripts']}, "
            f"audio_transcripts={audio_stats['transcribed']}, scored={scored}, "
            f"packs={len(packs)}, script_drafts={len(drafts)}"
        )


if __name__ == "__main__":
    main()
