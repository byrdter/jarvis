#!/usr/bin/env python3
"""
YouTube AI Channels Monitor
Fetches latest videos from curated AI YouTube channels and generates daily reports.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import yaml
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: google-api-python-client not installed")
    print("Install with: pip install google-api-python-client")
    sys.exit(1)


class YouTubeMonitor:
    """Monitor YouTube channels for new AI content."""

    def __init__(self, config_path='config/channels.yaml'):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in .env file")

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Load config
        config_file = Path(__file__).parent / config_path
        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.filters = self.config.get('filters', {})
        self.report_prefs = self.config.get('report', {})

        # Per-channel ingestion caps (e.g. Julian Goldie posts 12+/day)
        self._per_channel_cap = {}
        for channels in self.config['categories'].values():
            for ch in channels:
                if ch.get('channel_id') and ch.get('daily_cap'):
                    self._per_channel_cap[ch['channel_id']] = ch['daily_cap']

        # Per-channel email digest cap (default 3, full corpus still gets all)
        self._digest_cap_default = self.report_prefs.get('digest_max_per_channel', 3)

        self.handle_cache_path = Path(__file__).parent / 'config' / 'handle-cache.json'
        try:
            self.handle_cache = json.loads(self.handle_cache_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            self.handle_cache = {}

        self._resolve_handles()

    def _resolve_handles(self):
        """Resolve any `handle:` entries to channel IDs via channels.list (1 unit each, cached)."""
        dirty = False
        for channels in self.config['categories'].values():
            for ch in channels:
                if ch.get('channel_id'):
                    continue
                handle = ch.get('handle')
                if not handle:
                    continue
                cached = self.handle_cache.get(handle)
                if cached:
                    ch['channel_id'] = cached
                    continue
                try:
                    resp = self.youtube.channels().list(part='id', forHandle=handle).execute()
                    items = resp.get('items', [])
                    if items:
                        ch['channel_id'] = items[0]['id']
                        self.handle_cache[handle] = items[0]['id']
                        dirty = True
                    else:
                        print(f"⚠️  Could not resolve handle {handle} for {ch.get('name')}")
                except HttpError as e:
                    print(f"⚠️  Handle resolution failed for {handle}: {e}")
        if dirty:
            self.handle_cache_path.write_text(json.dumps(self.handle_cache, indent=2, sort_keys=True))

    def get_channel_videos(self, channel_id, hours=24):
        """Fetch recent videos from a channel via its uploads playlist.

        Uses playlistItems.list (1 quota unit) + a single batched videos.list
        (1 unit per 50 ids) instead of search.list (100 units). ~100x cheaper.
        """
        try:
            # Channel uploads playlist id is 'UU' + the part after 'UC'
            uploads_playlist = 'UU' + channel_id[2:]
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            # per_channel can be overridden per-channel via daily_cap in yaml
            per_channel = self._per_channel_cap.get(channel_id,
                                                   self.report_prefs.get('max_videos_per_channel', 5))

            request = self.youtube.playlistItems().list(
                part='contentDetails,snippet',
                playlistId=uploads_playlist,
                maxResults=max(per_channel * 2, 10),
            )
            response = request.execute()

            recent_ids = []
            for item in response.get('items', []):
                published = item['contentDetails'].get('videoPublishedAt')
                if not published:
                    continue
                published_dt = datetime.fromisoformat(published.replace('Z', '+00:00')).replace(tzinfo=None)
                if published_dt < cutoff:
                    continue
                recent_ids.append(item['contentDetails']['videoId'])
                if len(recent_ids) >= per_channel:
                    break

            if not recent_ids:
                return []

            return self.get_video_details_batch(recent_ids)

        except HttpError as e:
            print(f"Error fetching videos for channel {channel_id}: {e}")
            return []

    def get_video_details_batch(self, video_ids):
        """Fetch full details for up to 50 videos in one quota unit."""
        try:
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids),
                maxResults=50,
            )
            response = request.execute()

            videos = []
            for video in response.get('items', []):
                duration = self.parse_duration(video['contentDetails']['duration'])
                details = {
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'channel_title': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'thumbnail': video['snippet']['thumbnails']['high']['url'],
                    'duration': duration,
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'url': f"https://www.youtube.com/watch?v={video['id']}",
                }
                if self.should_include(details):
                    videos.append(details)
            return videos

        except HttpError as e:
            print(f"Error fetching video details batch: {e}")
            return []

    def get_video_details(self, video_id):
        """Get detailed information about a video."""
        try:
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            )

            response = request.execute()

            if not response.get('items'):
                return None

            video = response['items'][0]

            # Parse duration (ISO 8601 format)
            duration = self.parse_duration(video['contentDetails']['duration'])

            return {
                'video_id': video_id,
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'channel_title': video['snippet']['channelTitle'],
                'published_at': video['snippet']['publishedAt'],
                'thumbnail': video['snippet']['thumbnails']['high']['url'],
                'duration': duration,
                'views': int(video['statistics'].get('viewCount', 0)),
                'likes': int(video['statistics'].get('likeCount', 0)),
                'comments': int(video['statistics'].get('commentCount', 0)),
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }

        except HttpError as e:
            print(f"Error fetching video details for {video_id}: {e}")
            return None

    def parse_duration(self, duration_str):
        """Parse ISO 8601 duration to seconds."""
        import re

        # Format: PT#H#M#S
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)

        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds

    def should_include(self, video):
        """Filter videos based on preferences."""
        # Duration filters
        min_duration = self.filters.get('min_duration_seconds', 0)
        max_duration = self.filters.get('max_duration_seconds', float('inf'))

        if not (min_duration <= video['duration'] <= max_duration):
            return False

        # Keyword exclusions
        exclude_keywords = self.filters.get('exclude_keywords', [])
        title_lower = video['title'].lower()

        for keyword in exclude_keywords:
            if keyword.lower() in title_lower:
                return False

        return True

    def calculate_engagement_score(self, video):
        """Calculate engagement score for ranking."""
        views = max(video['views'], 1)
        likes = video['likes']
        comments = video['comments']

        # Engagement rate
        engagement_rate = (likes + comments * 2) / views

        # Recency bonus (prefer recent videos)
        published = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
        hours_old = (datetime.now(published.tzinfo) - published).total_seconds() / 3600
        recency_bonus = max(0, 1 - (hours_old / 24))

        # Priority keyword bonus
        priority_keywords = self.filters.get('priority_keywords', [])
        keyword_bonus = sum(1 for kw in priority_keywords if kw.lower() in video['title'].lower())

        return engagement_rate * 10000 + recency_bonus * 100 + keyword_bonus * 50

    def generate_report(self, hours=24):
        """Generate daily report of latest AI videos."""
        print(f"Fetching videos from last {hours} hours...")

        all_videos = []

        # Fetch videos from all channels
        for category_name, channels in self.config['categories'].items():
            print(f"\nProcessing {category_name}...")

            for channel in channels:
                channel_name = channel['name']
                channel_id = channel.get('channel_id')
                if not channel_id:
                    print(f"  - {channel_name}... SKIPPED (no channel_id)")
                    continue

                print(f"  - {channel_name}...", end=' ')

                videos = self.get_channel_videos(channel_id, hours)

                for video in videos:
                    video['category'] = category_name
                    video['channel_focus'] = channel['focus']
                    video['engagement_score'] = self.calculate_engagement_score(video)

                all_videos.extend(videos)
                print(f"{len(videos)} videos")

        # Sort by engagement score
        all_videos.sort(key=lambda v: v['engagement_score'], reverse=True)

        report_date = datetime.now().strftime('%Y-%m-%d')
        report_dir = Path(__file__).parent / 'reports' / 'daily'
        report_dir.mkdir(parents=True, exist_ok=True)

        # Dump FULL corpus (uncapped) for the transcript fetcher
        corpus_path = report_dir / f'corpus-{report_date}.json'
        import json as _json
        with open(corpus_path, 'w') as f:
            _json.dump(all_videos, f, indent=2)
        print(f"\n💾 Corpus dump ({len(all_videos)} videos): {corpus_path}")

        # Apply per-channel digest cap so Julian's 12/day doesn't bury the email
        digest_videos = self._apply_digest_caps(all_videos)
        max_total = self.report_prefs.get('max_total_videos', 40)
        digest_videos = digest_videos[:max_total]

        # Generate markdown report (digest view)
        report = self.format_markdown_report(digest_videos, hours)
        report_path = report_dir / f'ai-youtube-{report_date}.md'
        with open(report_path, 'w') as f:
            f.write(report)

        print(f"✅ Report saved to: {report_path}")
        print(f"📊 Digest videos: {len(digest_videos)}  |  Corpus videos: {len(all_videos)}")

        return report_path, all_videos, corpus_path

    def _apply_digest_caps(self, videos):
        """Limit each channel to N videos in the email digest (corpus keeps all)."""
        seen = {}
        out = []
        for v in videos:
            cap = self._digest_cap_default
            n = seen.get(v['channel_title'], 0)
            if n >= cap:
                continue
            seen[v['channel_title']] = n + 1
            out.append(v)
        return out

    def format_markdown_report(self, videos, hours):
        """Format videos as markdown report."""
        report = f"# AI YouTube Daily Report\n\n"
        report += f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n"
        report += f"**Period:** Last {hours} hours\n"
        report += f"**Videos Found:** {len(videos)}\n\n"
        report += "---\n\n"

        if not videos:
            report += "No new videos found in the specified time period.\n"
            return report

        # Group by category
        categories = {}
        for video in videos:
            cat = video['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(video)

        # Format each category
        for category, cat_videos in categories.items():
            report += f"## {category.replace('_', ' ').replace('tier', 'Tier ').title()}\n\n"

            for video in cat_videos:
                report += self.format_video_entry(video)
                report += "\n"

        # Summary stats
        report += "---\n\n"
        report += "## 📊 Summary\n\n"

        total_views = sum(v['views'] for v in videos)
        total_duration = sum(v['duration'] for v in videos)

        report += f"- **Total videos:** {len(videos)}\n"
        report += f"- **Total views:** {total_views:,}\n"
        report += f"- **Total watch time:** {self.format_duration(total_duration)}\n"
        report += f"- **Most active channel:** {self.get_most_active_channel(videos)}\n"

        return report

    def format_video_entry(self, video):
        """Format a single video entry."""
        entry = f"### {video['title']}\n\n"
        entry += f"**Channel:** {video['channel_title']}\n\n"
        entry += f"📹 [Watch Video]({video['url']}) | "
        entry += f"⏱️ {self.format_duration(video['duration'])} | "
        entry += f"👁️ {video['views']:,} views | "
        entry += f"👍 {video['likes']:,} likes | "
        entry += f"💬 {video['comments']:,} comments\n\n"

        if self.report_prefs.get('include_description', True):
            limit = self.report_prefs.get('description_chars', 350)
            raw = (video.get('description') or '').strip()
            if raw:
                summary = raw[:limit].strip()
                if len(raw) > limit:
                    summary = summary.rsplit(' ', 1)[0] + '...'
                entry += f"**Summary:** {summary}\n\n"
            else:
                entry += "**Summary:** _(no description provided by the channel)_\n\n"

        return entry

    def format_duration(self, seconds):
        """Format duration in human-readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def get_most_active_channel(self, videos):
        """Find the channel with most videos."""
        from collections import Counter
        channels = Counter(v['channel_title'] for v in videos)
        if channels:
            most_common = channels.most_common(1)[0]
            return f"{most_common[0]} ({most_common[1]} videos)"
        return "N/A"


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Monitor AI YouTube channels')
    parser.add_argument('--hours', type=int, default=24,
                       help='Hours to look back (default: 24)')
    parser.add_argument('--config', default='config/channels.yaml',
                       help='Config file path')
    parser.add_argument('--email', action='store_true',
                       help='Send report via email')
    parser.add_argument('--transcripts', action='store_true',
                       help='Also fetch transcripts into the ORICO corpus')

    args = parser.parse_args()

    try:
        monitor = YouTubeMonitor(config_path=args.config)
        report_path, videos, corpus_path = monitor.generate_report(hours=args.hours)

        # Print top 5 videos
        if videos:
            print("\n🔥 Top 5 Videos:\n")
            for i, video in enumerate(videos[:5], 1):
                print(f"{i}. {video['title']}")
                print(f"   {video['channel_title']} | {video['views']:,} views")
                print(f"   {video['url']}\n")

        # Fetch transcripts into corpus
        if args.transcripts and videos:
            try:
                from fetch_transcripts import process_videos
                print("\n📼 Fetching transcripts...")
                tstats, db_path, on_orico = process_videos(videos, verbose=True)
                print(f"📊 Transcripts: {tstats}  (DB: {db_path})")
            except Exception as e:
                print(f"⚠️  Transcript fetch failed: {e}")

        # Send email if requested
        if args.email:
            try:
                from email_sender import EmailSender
                sender = EmailSender()
                sender.send_report(report_path)
            except Exception as e:
                print(f"⚠️  Could not send email: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
