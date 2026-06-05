#!/usr/bin/env python3
"""
Check Claude Code YouTube channels for new videos (Sunday scraper).

Uses each channel's RSS feed (https://www.youtube.com/feeds/videos.xml?channel_id=...)
which returns the latest ~15 entries with reliable titles and publish dates. This
catches every video published since the last check, not just the most recent one,
and avoids the HTML-scraping title bug from the prior implementation.

Channels monitored:
- Cole Medin
- nateherk
- Chase H A I
- Greg Isenberg
- simonscrapes
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests
from youtube_transcript_api import YouTubeTranscriptApi

JARVIS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(JARVIS_ROOT / "agent-sdk"))

try:
    from bun import sqlite
    USE_BUN = True
except ImportError:
    import sqlite3
    USE_BUN = False

CHANNELS = {
    "cole-medin": {
        "name": "Cole Medin",
        "channel_id": "UCMwVTLZIRRUyyVrkjDpn4pA",
    },
    "nateherk": {
        "name": "nateherk",
        "channel_id": "UC2ojq-nuP8ceeHqiroeKhBA",
    },
    "chase-h-ai": {
        "name": "Chase H A I",
        "channel_id": "UCoy6cTJ7Tg0dqS-DI-_REsA",
    },
    "greg-isenberg": {
        "name": "Greg Isenberg",
        "channel_id": "UCPjNBjflYl0-HQtUvOx0Ibw",
    },
    "simonscrapes": {
        "name": "simonscrapes",
        "channel_id": "UCdCR4-uYOg5ju-IUuDnfnQA",
    },
}

JARVIS_PRIVATE = Path(os.environ.get(
    "JARVIS_PRIVATE",
    Path.home() / "Library/CloudStorage/Dropbox/jarvis-private",
))

STATE_FILE = Path(__file__).parent / "claude-code-last-check.json"
DB_PATH = JARVIS_ROOT / "agent-sdk/data/ai-knowledge.db"
WIKI_ROOT = JARVIS_PRIVATE / "claude-code-wiki/raw/transcripts"

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

# When a channel has no prior state (first run, or after a state reset), how many
# of its most recent RSS entries to consider. Each entry still goes through the
# URL-dedupe check in add_to_database, so already-ingested videos won't re-insert.
FIRST_RUN_LIMIT = 5


def get_new_videos(channel_id, last_video_id):
    """Return videos to ingest, chronological (oldest -> newest).

    Walks the RSS feed (newest-first) collecting entries until we hit
    last_video_id, then reverses so the last item we ingest becomes the new
    state pointer. If last_video_id is None we cap at FIRST_RUN_LIMIT.
    """
    url = RSS_URL.format(channel_id=channel_id)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"  ⚠️  RSS fetch failed: {e}")
        return []

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"  ⚠️  RSS parse failed: {e}")
        return []

    collected = []
    for entry in root.findall("atom:entry", ATOM_NS):
        vid_el = entry.find("yt:videoId", ATOM_NS)
        title_el = entry.find("atom:title", ATOM_NS)
        pub_el = entry.find("atom:published", ATOM_NS)
        if vid_el is None or title_el is None:
            continue
        video_id = vid_el.text
        if video_id == last_video_id:
            break
        collected.append({
            "video_id": video_id,
            "title": (title_el.text or "Untitled").strip(),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "published": pub_el.text if pub_el is not None else None,
        })

    if last_video_id is None:
        collected = collected[:FIRST_RUN_LIMIT]

    return list(reversed(collected))


def get_last_check_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_check_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def fetch_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        try:
            transcript = transcript_list.find_transcript(["en"])
        except Exception:
            try:
                transcript = transcript_list.find_generated_transcript(["en", "es"])
            except Exception:
                transcript = next(iter(transcript_list))
        entries = transcript.fetch()
        return " ".join(
            (e.get("text", "") if isinstance(e, dict) else e.text) for e in entries
        )
    except Exception as e:
        print(f"  ❌ Transcript fetch failed for {video_id}: {e}")
        return None


def add_to_database(video_info, channel_name, transcript):
    """Insert source + segmented transcript. Returns True if newly inserted."""
    db = None
    try:
        if USE_BUN:
            db = sqlite.Database(str(DB_PATH))
            exists = db.query("SELECT id FROM content_sources WHERE url = ?").get(video_info["url"])
        else:
            db = sqlite3.connect(str(DB_PATH))
            exists = db.execute(
                "SELECT id FROM content_sources WHERE url = ?", (video_info["url"],)
            ).fetchone()

        if exists:
            print(f"  ⏭️  Already in database: {video_info['title']}")
            return False

        metadata = json.dumps({"video_id": video_info["video_id"]})
        published = video_info.get("published") or datetime.now().isoformat()
        now_iso = datetime.now().isoformat()

        if USE_BUN:
            db.run(
                """
                INSERT INTO content_sources (title, author, url, type, metadata, published_date, indexed_at)
                VALUES (?, ?, ?, 'youtube', ?, ?, ?)
                """,
                video_info["title"], channel_name, video_info["url"], metadata, published, now_iso,
            )
            source_id = db.query("SELECT last_insert_rowid()").get()[0]
        else:
            cur = db.execute(
                """
                INSERT INTO content_sources (title, author, url, type, metadata, published_date, indexed_at)
                VALUES (?, ?, ?, 'youtube', ?, ?, ?)
                """,
                (video_info["title"], channel_name, video_info["url"], metadata, published, now_iso),
            )
            source_id = cur.lastrowid

        segment_size = 500
        current = []
        current_len = 0
        segment_index = 0
        for word in transcript.split():
            current.append(word)
            current_len += len(word) + 1
            if current_len >= segment_size:
                _insert_segment(db, source_id, segment_index, " ".join(current))
                current, current_len, segment_index = [], 0, segment_index + 1
        if current:
            _insert_segment(db, source_id, segment_index, " ".join(current))

        if not USE_BUN:
            db.commit()
        print(f"  ✅ DB insert: {video_info['title']}")
        return True
    except Exception as e:
        print(f"  ❌ DB error: {e}")
        return False
    finally:
        if db is not None and not USE_BUN:
            db.close()


def _insert_segment(db, source_id, segment_index, text):
    if USE_BUN:
        db.run(
            "INSERT INTO segments (source_id, segment_index, text) VALUES (?, ?, ?)",
            source_id, segment_index, text,
        )
    else:
        db.execute(
            "INSERT INTO segments (source_id, segment_index, text) VALUES (?, ?, ?)",
            (source_id, segment_index, text),
        )


def export_to_wiki(video_info, channel_name, channel_slug, transcript):
    try:
        channel_dir = WIKI_ROOT / channel_slug
        channel_dir.mkdir(parents=True, exist_ok=True)
        title_slug = re.sub(r"[^a-z0-9\s]", "", video_info["title"][:50].lower()).strip().replace(" ", "-")
        filepath = channel_dir / f"{video_info['video_id']}-{title_slug}.md"
        published = video_info.get("published") or datetime.now().isoformat()
        markdown = f"""---
title: "{video_info['title']}"
author: {channel_name}
url: {video_info['url']}
video_id: {video_info['video_id']}
channel: {channel_slug}
published: {published}
indexed: {datetime.now().isoformat()}
---

# {video_info['title']}

**Channel:** {channel_name}
**Video ID:** {video_info['video_id']}
**URL:** {video_info['url']}
**Published:** {published}
**Indexed:** {datetime.now().strftime('%Y-%m-%d')}

## Transcript

{transcript}
"""
        with open(filepath, "w") as f:
            f.write(markdown)
        print(f"  📝 Wiki: {filepath.name}")
    except Exception as e:
        print(f"  ❌ Wiki export error: {e}")


def main():
    print("🔍 Checking Claude Code channels for new videos (RSS-based)...\n")
    state = get_last_check_state()
    new_state = dict(state)
    total_new = 0

    for slug, channel in CHANNELS.items():
        print(f"📺 {channel['name']}")
        last_video_id = state.get(slug, {}).get("video_id")
        new_videos = get_new_videos(channel["channel_id"], last_video_id)

        if not new_videos:
            print("  ✓ No new videos\n")
            continue

        print(f"  🎉 {len(new_videos)} new video(s) since last check")
        latest_ingested = None
        for video in new_videos:
            print(f"  → {video['title']}")
            transcript = fetch_transcript(video["video_id"])
            if not transcript:
                continue
            inserted = add_to_database(video, channel["name"], transcript)
            if inserted:
                export_to_wiki(video, channel["name"], slug, transcript)
                total_new += 1
            latest_ingested = video

        if latest_ingested:
            new_state[slug] = {
                "video_id": latest_ingested["video_id"],
                "title": latest_ingested["title"],
                "published": latest_ingested.get("published"),
                "date": datetime.now().isoformat(),
            }
        print()

    save_check_state(new_state)
    print(f"\n{'='*60}")
    print(f"✅ Done. New videos ingested: {total_new}")
    print(f"💾 State saved: {STATE_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
