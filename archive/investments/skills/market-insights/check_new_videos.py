#!/usr/bin/env python3
"""
Check Chris Vermeulen's YouTube channel for new videos.
No API key required - uses web scraping.

Usage:
    python check_new_videos.py

Returns:
    JSON output if new video found, silent exit if no new video
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import requests
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_URL = "https://www.youtube.com/@TheTechnicalTraders/videos"
STATE_FILE = Path(__file__).parent / "last_processed.json"

JARVIS_PRIVATE = Path(os.environ.get(
    "JARVIS_PRIVATE",
    Path.home() / "Library/CloudStorage/Dropbox/jarvis-private"
))
TRANSCRIPT_DIR = JARVIS_PRIVATE / "research/transcripts/vermeulen"
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)


def get_latest_video():
    """
    Fetch latest video from channel (no API needed).

    Returns:
        dict: Video metadata (video_id, title, url)
        None: If no videos found or error
    """
    try:
        response = requests.get(CHANNEL_URL)
        response.raise_for_status()
        html = response.text

        # Extract video ID from page HTML
        # YouTube embeds data in ytInitialData variable
        match = re.search(r'"videoId":"([^"]+)"', html)
        if match:
            video_id = match.group(1)

            # Extract title
            title_match = re.search(r'"title":{"runs":\[{"text":"([^"]+)"', html)
            title = title_match.group(1) if title_match else "Unknown Title"

            return {
                "video_id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }

        return None

    except Exception as e:
        print(f"Error fetching latest video: {e}")
        return None


def get_last_processed():
    """
    Get last processed video ID from state file.

    Returns:
        dict: Last processed video metadata
    """
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"video_id": None, "date": None}


def save_last_processed(video_info):
    """
    Save processed video ID and date to state file.

    Args:
        video_info: Video metadata dict
    """
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({
            "video_id": video_info["video_id"],
            "date": datetime.now().isoformat(),
            "title": video_info["title"]
        }, f, indent=2)


def fetch_transcript(video_id):
    """
    Fetch transcript for video (no API needed).

    Args:
        video_id: YouTube video ID

    Returns:
        str: Full transcript text
        None: If transcript unavailable
    """
    try:
        # Instantiate API
        ytt_api = YouTubeTranscriptApi()

        # Get available transcripts
        transcript_list = ytt_api.list(video_id)

        # Try English first, fall back to any available language
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            # Try generated transcript in English or Spanish
            try:
                transcript = transcript_list.find_generated_transcript(['en', 'es'])
            except:
                # Last resort: get any available transcript
                for transcript in transcript_list:
                    break

        # Fetch the transcript entries
        entries = transcript.fetch()
        full_text = " ".join([entry.text for entry in entries])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def save_transcript(video_id, title, text):
    """
    Save transcript to file.

    Args:
        video_id: YouTube video ID
        title: Video title
        text: Transcript text

    Returns:
        Path: Path to saved transcript file
    """
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"vermeulen-{date_str}-{video_id}.txt"
    filepath = TRANSCRIPT_DIR / filename

    with open(filepath, 'w') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Date: {date_str}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write("\n--- TRANSCRIPT ---\n\n")
        f.write(text)

    return filepath


def main():
    """
    Main execution logic.

    Checks for new videos, fetches transcript if found,
    and outputs JSON for JARVIS to process.
    """
    # Get latest video
    latest = get_latest_video()
    if not latest:
        print("No videos found")
        return

    # Check if already processed
    last_processed = get_last_processed()
    if latest["video_id"] == last_processed.get("video_id"):
        print(f"No new video (latest: {latest['title']})")
        return

    # New video found!
    print(f"New video found: {latest['title']}")
    print(f"URL: {latest['url']}")

    # Fetch transcript
    print("Fetching transcript...")
    transcript = fetch_transcript(latest["video_id"])

    if not transcript:
        print("Could not fetch transcript")
        # Save video metadata even without transcript
        save_last_processed(latest)
        result = {
            "status": "new_video_no_transcript",
            "video_id": latest["video_id"],
            "title": latest["title"],
            "url": latest["url"],
            "note": "Transcript not available - may need manual processing"
        }
        print("\n=== NEW VIDEO (NO TRANSCRIPT) ===")
        print(json.dumps(result, indent=2))
        return

    # Save transcript
    filepath = save_transcript(latest["video_id"], latest["title"], transcript)
    print(f"Transcript saved: {filepath}")

    # Mark as processed
    save_last_processed(latest)

    # Output for JARVIS to process
    result = {
        "status": "new_video",
        "video_id": latest["video_id"],
        "title": latest["title"],
        "url": latest["url"],
        "transcript_file": str(filepath),
        "transcript_preview": transcript[:500] + "..."
    }

    print("\n=== NEW VIDEO READY FOR PROCESSING ===")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
