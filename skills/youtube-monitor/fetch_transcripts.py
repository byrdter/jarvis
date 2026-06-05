#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
Pulls captions for videos discovered by monitor_channels.py and stores them
in a searchable SQLite database on ORICO with FTS5 full-text index.
Local SSD acts as a write-buffer so a missing ORICO never loses data.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

# Optional Whisper fallback
try:
    from whisper_fallback import fetch_with_whisper, whisper_available
except ImportError:
    fetch_with_whisper = None
    def whisper_available():
        return False

# ---- Knowledge-graph integration ------------------------------------------
KNOWLEDGE_DB = Path(__file__).resolve().parents[2] / "agent-sdk" / "data" / "ai-knowledge.db"
VAULT_ROOT = Path(os.path.expanduser("~/Obsidian/JARVIS/YouTube"))

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(s, maxlen=60):
    s = _SLUG_RE.sub("-", (s or "").lower()).strip("-")
    return s[:maxlen] or "untitled"

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
    )
except ImportError:
    print("ERROR: youtube-transcript-api not installed")
    print("Install with: pip install youtube-transcript-api")
    sys.exit(1)

# ---- Storage paths --------------------------------------------------------
ORICO_ROOT = Path("/Volumes/ORICO/jarvis/youtube-transcripts")
LOCAL_ROOT = Path.home() / ".local/share/jarvis/youtube-transcripts"
LOCAL_INCOMING = LOCAL_ROOT / "incoming"


def storage_db_path():
    """Use ORICO when mounted, else local incoming/ as write-buffer."""
    if ORICO_ROOT.exists():
        ORICO_ROOT.mkdir(parents=True, exist_ok=True)
        return ORICO_ROOT / "transcripts.db", True
    LOCAL_INCOMING.mkdir(parents=True, exist_ok=True)
    return LOCAL_INCOMING / "transcripts.db", False


SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    channel_title TEXT,
    channel_id TEXT,
    published_at TEXT,
    duration_seconds INTEGER,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    url TEXT,
    description TEXT,
    transcript_status TEXT,    -- ok | disabled | none | unavailable | error
    transcript_source TEXT,    -- captions | whisper | none
    transcript_language TEXT,
    transcript_chars INTEGER,
    fetched_at TEXT
);

CREATE TABLE IF NOT EXISTS transcripts (
    video_id TEXT PRIMARY KEY REFERENCES videos(video_id),
    text TEXT,
    segments_json TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS transcripts_fts USING fts5(
    video_id UNINDEXED,
    title,
    channel_title,
    text,
    tokenize='porter unicode61'
);
"""


def open_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


def upsert_video(conn, v, status, source, lang, chars):
    conn.execute(
        """INSERT INTO videos(video_id, title, channel_title, channel_id,
                              published_at, duration_seconds, views, likes,
                              comments, url, description, transcript_status,
                              transcript_source, transcript_language,
                              transcript_chars, fetched_at)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(video_id) DO UPDATE SET
               transcript_status=excluded.transcript_status,
               transcript_source=excluded.transcript_source,
               transcript_language=excluded.transcript_language,
               transcript_chars=excluded.transcript_chars,
               fetched_at=excluded.fetched_at""",
        (
            v["video_id"], v["title"], v["channel_title"], v.get("channel_id", ""),
            v["published_at"], v["duration"], v["views"], v["likes"],
            v["comments"], v["url"], v.get("description", ""),
            status, source, lang, chars, datetime.utcnow().isoformat(),
        ),
    )


def store_transcript(conn, video_id, text, segments, title, channel_title):
    conn.execute(
        "INSERT OR REPLACE INTO transcripts(video_id, text, segments_json) VALUES(?,?,?)",
        (video_id, text, json.dumps(segments) if segments else None),
    )
    conn.execute("DELETE FROM transcripts_fts WHERE video_id = ?", (video_id,))
    conn.execute(
        "INSERT INTO transcripts_fts(video_id, title, channel_title, text) VALUES(?,?,?,?)",
        (video_id, title, channel_title, text),
    )


def write_vault_markdown(v, text, source, lang):
    """Write a markdown file to ~/Obsidian/JARVIS/YouTube/YYYY-MM-DD/ so the
    Phase 2B vector indexer (index-vault.ts) picks it up automatically.
    """
    try:
        pub = v.get("published_at") or datetime.utcnow().isoformat()
        date_dir = VAULT_ROOT / pub[:10]
        date_dir.mkdir(parents=True, exist_ok=True)
        slug = _slug(v["channel_title"]) + "--" + _slug(v["title"]) + "--" + v["video_id"]
        path = date_dir / f"{slug}.md"

        title = (v.get("title") or "").replace('"', "'")
        frontmatter = (
            "---\n"
            f"video_id: {v['video_id']}\n"
            f"title: \"{title}\"\n"
            f"channel: \"{v.get('channel_title','')}\"\n"
            f"channel_id: {v.get('channel_id','')}\n"
            f"published: {v.get('published_at','')}\n"
            f"url: {v.get('url','')}\n"
            f"duration_seconds: {v.get('duration', 0)}\n"
            f"views: {v.get('views', 0)}\n"
            f"transcript_source: {source}\n"
            f"transcript_language: {lang}\n"
            f"transcript_chars: {len(text)}\n"
            "tags: [youtube, transcript, ai]\n"
            "---\n\n"
        )
        body = (
            f"# {v.get('title','')}\n\n"
            f"**Channel:** {v.get('channel_title','')}  \n"
            f"**Watch:** {v.get('url','')}  \n"
            f"**Published:** {v.get('published_at','')}\n\n"
            f"## Transcript ({source}, {lang})\n\n"
            f"{text}\n"
        )
        path.write_text(frontmatter + body)
        return path
    except Exception as e:
        print(f"    ⚠️  vault write failed for {v.get('video_id')}: {e}")
        return None


def mirror_to_knowledge_db(v, text, source, lang, transcript_path):
    """Insert into ai-knowledge.db so JARVIS sees this in its
    unified knowledge graph (content_sources + segments)."""
    if not KNOWLEDGE_DB.exists():
        return False
    try:
        kdb = sqlite3.connect(str(KNOWLEDGE_DB))
        # Dedupe by URL
        existing = kdb.execute(
            "SELECT id FROM content_sources WHERE url = ?", (v.get("url", ""),)
        ).fetchone()
        if existing:
            kdb.execute(
                """UPDATE content_sources
                   SET transcript_path=?, last_updated=datetime('now'),
                       metadata=? WHERE id=?""",
                (
                    str(transcript_path) if transcript_path else None,
                    json.dumps({
                        "channel_id": v.get("channel_id", ""),
                        "channel_title": v.get("channel_title", ""),
                        "transcript_source": source,
                        "transcript_language": lang,
                        "transcript_chars": len(text),
                        "views": v.get("views", 0),
                    }),
                    existing[0],
                ),
            )
            sid = existing[0]
        else:
            cur = kdb.execute(
                """INSERT INTO content_sources
                   (type, title, url, author, published_date, duration_seconds,
                    transcript_path, indexed_at, last_updated, metadata)
                   VALUES('youtube', ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), ?)""",
                (
                    v.get("title", ""),
                    v.get("url", ""),
                    v.get("channel_title", ""),
                    (v.get("published_at") or "")[:10],
                    v.get("duration", 0),
                    str(transcript_path) if transcript_path else None,
                    json.dumps({
                        "channel_id": v.get("channel_id", ""),
                        "channel_title": v.get("channel_title", ""),
                        "video_id": v["video_id"],
                        "transcript_source": source,
                        "transcript_language": lang,
                        "transcript_chars": len(text),
                        "views": v.get("views", 0),
                        "likes": v.get("likes", 0),
                    }),
                ),
            )
            sid = cur.lastrowid
        kdb.commit()
        kdb.close()
        return True
    except Exception as e:
        print(f"    ⚠️  knowledge-db mirror failed for {v.get('video_id')}: {e}")
        return False


_API = YouTubeTranscriptApi()


def _to_text_and_segments(fetched):
    """Normalize FetchedTranscript -> (text, segments list of dicts, lang)."""
    snippets = list(fetched)  # FetchedTranscript is iterable of FetchedTranscriptSnippet
    text = " ".join(s.text.replace("\n", " ").strip() for s in snippets if s.text)
    segments = [{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]
    lang = getattr(fetched, "language_code", "en")
    return text, segments, lang


def fetch_one(video_id):
    """Return (text, segments, lang) or (None, None, status_string)."""
    try:
        fetched = _API.fetch(video_id, languages=["en", "en-US", "en-GB"])
        return _to_text_and_segments(fetched)
    except TranscriptsDisabled:
        return None, None, "disabled"
    except NoTranscriptFound:
        # Try any available language
        try:
            tl = _API.list(video_id)
            t = next(iter(tl), None)
            if t is None:
                return None, None, "none"
            fetched = t.fetch()
            return _to_text_and_segments(fetched)
        except Exception:
            return None, None, "none"
    except VideoUnavailable:
        return None, None, "unavailable"
    except Exception as e:
        return None, None, f"error:{type(e).__name__}"


def _persist_success(conn, v, text, segments, source, lang):
    """Write to all surfaces: SQLite/FTS5, vault markdown, knowledge DB."""
    upsert_video(conn, v, "ok", source, lang, len(text))
    store_transcript(conn, v["video_id"], text, segments, v["title"], v["channel_title"])
    md_path = write_vault_markdown(v, text, source, lang)
    mirror_to_knowledge_db(v, text, source, lang, md_path)


def process_videos(videos, verbose=True, use_whisper=True):
    db_path, on_orico = storage_db_path()
    if verbose:
        loc = "ORICO" if on_orico else "LOCAL incoming/"
        print(f"📦 DB: {db_path}  ({loc})")
        if use_whisper and whisper_available():
            print(f"🗣  Whisper fallback: enabled (base.en)")
        elif use_whisper:
            print(f"🗣  Whisper fallback: requested but tools missing")

    conn = open_db(db_path)
    stats = {"ok": 0, "whisper": 0, "disabled": 0, "none": 0,
             "unavailable": 0, "error": 0, "skipped": 0}

    # Skip ones we already have a transcript for
    have = {r[0] for r in conn.execute(
        "SELECT video_id FROM transcripts WHERE LENGTH(text) > 0"
    )}

    for v in videos:
        vid = v["video_id"]
        if vid in have:
            stats["skipped"] += 1
            continue

        text, segments, status = fetch_one(vid)

        # Whisper fallback for captions-missing cases
        if not text and use_whisper and status in ("disabled", "none") \
                and fetch_with_whisper and whisper_available():
            if verbose:
                print(f"  … whisper fallback for {vid} ({v['title'][:50]})")
            wtext, wsegs, wstatus = fetch_with_whisper(vid, v.get("url", ""), verbose=verbose)
            if wtext:
                text, segments, status = wtext, wsegs, "en"
                _persist_success(conn, v, text, segments, "whisper", status)
                stats["whisper"] += 1
                if verbose:
                    print(f"  ✓ {v['channel_title'][:25]:25} | {len(text):6d} chars | "
                          f"(whisper) {v['title'][:50]}")
                time.sleep(0.2)
                continue
            else:
                status = wstatus

        if text:
            _persist_success(conn, v, text, segments, "captions", status)
            stats["ok"] += 1
            if verbose:
                print(f"  ✓ {v['channel_title'][:25]:25} | {len(text):6d} chars | {v['title'][:60]}")
        else:
            key = status.split(":")[0]
            stats[key if key in stats else "error"] += 1
            upsert_video(conn, v, status, "none", "", 0)
            if verbose:
                print(f"  ✗ {v['channel_title'][:25]:25} | {status:12} | {v['title'][:60]}")

        time.sleep(0.2)

        if (stats["ok"] + stats["whisper"]) % 25 == 0:
            conn.commit()

    conn.commit()
    conn.close()
    return stats, db_path, on_orico


def main():
    parser = argparse.ArgumentParser(description="Fetch transcripts for harvested videos")
    parser.add_argument("--videos-json", required=True,
                        help="Path to JSON file with the video list from monitor_channels.py")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-whisper", action="store_true",
                        help="Skip Whisper fallback for caption-less videos")
    args = parser.parse_args()

    videos = json.loads(Path(args.videos_json).read_text())
    if not videos:
        print("No videos to process.")
        return

    print(f"📼 Processing {len(videos)} videos...")
    stats, db_path, on_orico = process_videos(
        videos, verbose=not args.quiet, use_whisper=not args.no_whisper
    )

    print(f"\n📊 Transcript fetch complete:")
    for k, v in stats.items():
        if v:
            print(f"   {k}: {v}")
    print(f"   DB: {db_path} ({'ORICO' if on_orico else 'LOCAL'})")


if __name__ == "__main__":
    main()
