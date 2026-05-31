#!/usr/bin/env python3
"""
aggregate.py - AI News Aggregator

Aggregates AI news from multiple sources using agent-browser and APIs.
Generates daily digest in markdown format.

Usage:
    python3 aggregate.py daily --date 2026-01-28 --output digest.md
    python3 aggregate.py daily  # Uses today's date
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests
from difflib import SequenceMatcher
import feedparser


# AI relevance keywords
AI_KEYWORDS = [
    'artificial intelligence', 'machine learning', 'deep learning',
    'neural network', 'llm', 'large language model',
    'gpt', 'claude', 'gemini', 'llama', 'mistral',
    'transformer', 'attention', 'rag', 'fine-tuning',
    'chatbot', 'openai', 'anthropic', 'google ai'
]

# Topic categories
TOPICS = {
    'LLMs': ['llm', 'language model', 'gpt', 'claude', 'gemini', 'chatbot'],
    'Computer Vision': ['vision', 'image', 'video', 'dall-e', 'stable diffusion'],
    'Research': ['arxiv', 'paper', 'research', 'study'],
    'Business': ['funding', 'acquisition', 'revenue', 'startup', 'series'],
    'Regulation': ['regulation', 'policy', 'law', 'ethics', 'safety'],
}

DEFAULT_RSS_FEEDS = {
    'VentureBeat AI': 'https://venturebeat.com/category/ai/feed/',
    'TechCrunch AI': 'https://techcrunch.com/category/artificial-intelligence/feed/',
    'OpenAI News': 'https://openai.com/news/rss.xml',
    'Google DeepMind': 'https://deepmind.google/blog/rss.xml',
    'Hugging Face Blog': 'https://huggingface.co/blog/feed.xml',
    'LangChain Blog': 'https://blog.langchain.com/rss/',
}


def load_rss_feeds() -> Dict[str, str]:
    """Load RSS feeds from config, falling back to a small built-in set."""
    config_path = Path(__file__).parent / 'config' / 'rss-feeds.json'
    if not config_path.exists():
        return DEFAULT_RSS_FEEDS

    try:
        with config_path.open() as f:
            feeds = json.load(f)
        return {name: url for name, url in feeds.items() if name and url}
    except Exception as e:
        print(f"  Warning: Could not load RSS feed config: {e}")
        return DEFAULT_RSS_FEEDS


def run_agent_browser(command: str, timeout: int = 30) -> str:
    """Run agent-browser command and return output."""
    try:
        result = subprocess.run(
            f"agent-browser {command}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  Warning: Command timed out: {command}")
        return ""
    except Exception as e:
        print(f"  Error running agent-browser: {e}")
        return ""


def fetch_rss_feed(source_name: str, feed_url: str, max_days: int = 14) -> List[Dict]:
    """Fetch articles from an RSS feed."""
    print(f"Fetching {source_name}...")

    articles = []

    try:
        # Parse RSS feed
        feed = feedparser.parse(feed_url)

        # Check for critical parsing errors (but allow minor warnings if we have entries)
        if feed.bozo and len(feed.entries) == 0:
            error_msg = str(feed.bozo_exception) if hasattr(feed, 'bozo_exception') else "Unknown error"
            print(f"  Warning: Feed parsing error for {source_name}: {error_msg}")
            return articles
        elif feed.bozo:
            # Minor parsing issue but we have entries - log but continue
            print(f"  Note: Minor parsing warning for {source_name} (continuing with {len(feed.entries)} entries)")

        # Get cutoff date (only include recent articles)
        cutoff_date = datetime.now() - timedelta(days=max_days)

        for entry in feed.entries:
            try:
                # Extract publication date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                # Skip if too old
                if pub_date and pub_date < cutoff_date:
                    continue

                # Extract article info
                title = entry.get('title', '').strip()
                url = entry.get('link', '').strip()
                summary = entry.get('summary', '').strip()

                if not title or not url:
                    continue

                # Only include AI-relevant articles
                if not is_ai_relevant(title + ' ' + summary):
                    continue

                articles.append({
                    'title': title,
                    'url': url,
                    'source': source_name,
                    'summary': summary[:200] if summary else '',
                    'date': pub_date.strftime('%Y-%m-%d') if pub_date else datetime.now().strftime('%Y-%m-%d')
                })

            except Exception as e:
                continue

        print(f"  Found {len(articles)} relevant articles from {source_name}")

    except Exception as e:
        print(f"  Error fetching {source_name}: {e}")

    return articles


def scrape_techcrunch() -> List[Dict]:
    """Scrape TechCrunch AI category using agent-browser."""
    print("Scraping TechCrunch AI...")

    articles = []

    try:
        # Open TechCrunch AI category
        run_agent_browser('open "https://techcrunch.com/category/artificial-intelligence/" --load networkidle')

        # Get snapshot
        snapshot_json = run_agent_browser('snapshot -i -c --json')

        if not snapshot_json:
            print("  Warning: Empty snapshot from TechCrunch")
            return articles

        snapshot = json.loads(snapshot_json)
        refs = snapshot.get('data', {}).get('refs', {})

        # Extract article links - look for longer titles (likely articles)
        for ref_id, ref_data in refs.items():
            role = ref_data.get('role', '')
            name = ref_data.get('name', '')

            # Filter for article links:
            # - Role is 'link'
            # - Name is long enough to be an article title (>50 chars)
            # - Not navigation/UI elements
            if (role == 'link' and
                name and
                len(name) > 50 and
                not name.startswith('TechCrunch') and
                'Logo' not in name):

                # Skip duplicate detection - add all candidates
                articles.append({
                    'title': name,
                    # TODO: Extract actual article URLs
                    # Currently using placeholder - need to get href attribute from refs
                    'url': f'https://techcrunch.com/',
                    'source': 'TechCrunch AI',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })

        # Close browser
        run_agent_browser('close')

        print(f"  Found {len(articles)} articles from TechCrunch")

    except Exception as e:
        print(f"  Error scraping TechCrunch: {e}")

    return articles


def fetch_hackernews() -> List[Dict]:
    """Fetch AI-related stories from Hacker News API."""
    print("Fetching Hacker News...")

    articles = []
    debug_titles = []

    try:
        # Get top stories
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
        top_stories = response.json()[:50]  # Top 50

        for story_id in top_stories:
            try:
                story_response = requests.get(
                    f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                    timeout=5
                )
                story = story_response.json()

                if not story:
                    continue

                title = story.get('title', '')
                url = story.get('url', f'https://news.ycombinator.com/item?id={story_id}')

                # Debug: collect first 10 titles
                if len(debug_titles) < 10:
                    debug_titles.append(title)

                # Filter for AI-related
                if is_ai_relevant(title):
                    articles.append({
                        'title': title,
                        'url': url,
                        'source': 'Hacker News',
                        'score': story.get('score', 0),
                        'date': datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d')
                    })

            except Exception as e:
                continue

        print(f"  Found {len(articles)} AI articles from Hacker News")
        if len(articles) == 0:
            print("  Sample titles checked:")
            for i, title in enumerate(debug_titles[:5], 1):
                print(f"    {i}. {title}")

    except Exception as e:
        print(f"  Error fetching Hacker News: {e}")

    return articles


def is_ai_relevant(text: str, threshold: float = 0.2) -> bool:
    """Check if text is AI-relevant based on keywords."""
    text_lower = text.lower()
    score = 0

    for keyword in AI_KEYWORDS:
        if keyword in text_lower:
            score += 0.2

    return score >= threshold


def calculate_relevance_score(title: str, summary: str = '') -> float:
    """Calculate relevance score for article."""
    text = (title + ' ' + summary).lower()
    score = 0

    # High-value terms
    if any(term in text for term in ['gpt-', 'claude-', 'gemini']):
        score += 0.3

    # Core AI terms
    if any(term in text for term in ['ai', 'llm', 'machine learning']):
        score += 0.2

    # Technical terms
    if any(term in text for term in ['transformer', 'neural network']):
        score += 0.2

    # Companies
    if any(term in text for term in ['openai', 'anthropic', 'google ai']):
        score += 0.1

    return min(score, 1.0)


def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """Remove duplicate articles based on URL and title similarity."""
    seen_urls = set()
    seen_titles = []
    unique_articles = []

    for article in articles:
        url = article.get('url', '').split('?')[0].rstrip('/')

        # Check URL
        if url in seen_urls:
            continue

        # Check title similarity
        title = article.get('title', '')
        is_duplicate = False

        for seen_title in seen_titles:
            similarity = SequenceMatcher(None, title.lower(), seen_title.lower()).ratio()
            if similarity > 0.85:
                is_duplicate = True
                break

        if is_duplicate:
            continue

        # Not a duplicate
        seen_urls.add(url)
        seen_titles.append(title)
        unique_articles.append(article)

    duplicates_removed = len(articles) - len(unique_articles)
    if duplicates_removed > 0:
        print(f"  Removed {duplicates_removed} duplicates")

    return unique_articles


def categorize_article(title: str, summary: str = '') -> List[str]:
    """Categorize article by topic."""
    text = (title + ' ' + summary).lower()
    tags = []

    for topic, keywords in TOPICS.items():
        if any(keyword in text for keyword in keywords):
            tags.append(topic)

    return tags if tags else ['General AI']


def generate_digest(articles: List[Dict], date: str) -> str:
    """Generate markdown digest from articles."""
    # Sort by relevance/score
    articles_sorted = sorted(
        articles,
        key=lambda x: x.get('score', 0),
        reverse=True
    )

    # Generate markdown
    md = f"# AI News Digest - {date}\n\n"
    md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"Articles: {len(articles)}\n"
    md += f"Sources: {len(set(a['source'] for a in articles))}\n\n"
    md += "---\n\n"

    md += "## 📰 Top Stories\n\n"

    for article in articles_sorted[:20]:  # Top 20
        title = article.get('title', 'Untitled')
        url = article.get('url', '#')
        source = article.get('source', 'Unknown')
        summary = article.get('summary', '')
        topics = categorize_article(title, summary)

        md += f"### {title}\n"
        md += f"**Source:** {source} | **Topics:** {', '.join(topics)}\n\n"

        # Include summary if available
        if summary:
            md += f"{summary}\n\n"

        md += f"[Read more →]({url})\n\n"
        md += "---\n\n"

    # Statistics
    md += "## 📊 Statistics\n\n"
    md += f"- **Total articles:** {len(articles)}\n"

    source_counts = {}
    for article in articles:
        source = article['source']
        source_counts[source] = source_counts.get(source, 0) + 1

    md += f"- **Sources:** {', '.join(f'{source} ({count})' for source, count in source_counts.items())}\n\n"

    md += "---\n\n"
    md += "*Generated by JARVIS news-aggregator skill*\n"

    return md


def main():
    parser = argparse.ArgumentParser(description='Aggregate AI news from multiple sources')
    parser.add_argument('mode', choices=['daily'], help='Aggregation mode')
    parser.add_argument('--date', help='Date (YYYY-MM-DD), default: today')
    parser.add_argument('--output', help='Output file path', default='digest.md')

    args = parser.parse_args()

    # Parse date
    if args.date:
        target_date = args.date
    else:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"AI News Aggregator - {target_date}")
    print("=" * 60)

    # Aggregate from all sources
    all_articles = []

    # Hacker News (API - fast and reliable)
    hn_articles = fetch_hackernews()
    all_articles.extend(hn_articles)

    # Fetch all RSS feeds
    rss_feeds = load_rss_feeds()
    print(f"Fetching RSS feeds: {len(rss_feeds)} configured sources")

    for source_name, feed_url in rss_feeds.items():
        rss_articles = fetch_rss_feed(source_name, feed_url)
        all_articles.extend(rss_articles)

    print()
    print(f"Total articles collected: {len(all_articles)}")

    # Filter for relevance
    print("Filtering for AI relevance...")
    relevant_articles = [a for a in all_articles if is_ai_relevant(a.get('title', ''))]
    print(f"  Relevant articles: {len(relevant_articles)}")

    # Deduplicate
    print("Removing duplicates...")
    unique_articles = deduplicate_articles(relevant_articles)

    # Generate digest
    print("Generating digest...")
    digest_md = generate_digest(unique_articles, target_date)

    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(digest_md)

    print(f"\n✓ Digest saved to: {output_path}")
    print(f"  Articles included: {len(unique_articles)}")


if __name__ == '__main__':
    main()
