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
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests
from difflib import SequenceMatcher
import feedparser

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False

# ---- Persistence layer (mirrors youtube-monitor architecture) -------------
ORICO_ROOT = Path("/Volumes/ORICO/jarvis/news-articles")
LOCAL_INCOMING = Path.home() / ".local/share/jarvis/news-articles/incoming"
KNOWLEDGE_DB = Path(__file__).resolve().parents[2] / "agent-sdk" / "data" / "ai-knowledge.db"
VAULT_ROOT = Path(os.path.expanduser("~/Obsidian/JARVIS/News"))

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(s, maxlen=60):
    s = _SLUG_RE.sub("-", (s or "").lower()).strip("-")
    return s[:maxlen] or "untitled"


def _archive_root():
    # Check the mountpoint (/Volumes/ORICO), not the subdir which we create.
    if Path("/Volumes/ORICO").exists():
        ORICO_ROOT.mkdir(parents=True, exist_ok=True)
        return ORICO_ROOT, True
    LOCAL_INCOMING.mkdir(parents=True, exist_ok=True)
    return LOCAL_INCOMING, False


def _normalize_url(url: str) -> str:
    """Strip tracking params and trailing slash for dedupe stability."""
    if not url:
        return ""
    base = url.split("?")[0].split("#")[0].rstrip("/")
    return base


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


def fetch_rss_feed(source_name: str, feed_url: str, max_days: float = 5.0) -> List[Dict]:
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
        cutoff_date = datetime.now() - timedelta(days=float(max_days))

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

                # NOTE: Relevance filtering moved to main() so that AI-dedicated
                # sources (Substacks, Reddit AI subs) can bypass keyword matching.
                articles.append({
                    'title': title,
                    'url': url,
                    'source': source_name,
                    'summary': summary,  # keep full RSS summary; fetcher gets the body
                    'published_at': pub_date.isoformat() if pub_date else '',
                    'date': pub_date.strftime('%Y-%m-%d') if pub_date else datetime.now().strftime('%Y-%m-%d'),
                    'guid': entry.get('id') or entry.get('guid') or '',
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


# ===========================================================================
# Persistence + full-text extraction
# ===========================================================================

def open_knowledge_db():
    """Open ai-knowledge.db. Returns None if missing (we'll log and proceed)."""
    if not KNOWLEDGE_DB.exists():
        return None
    return sqlite3.connect(str(KNOWLEDGE_DB))


def filter_already_seen(articles: List[Dict]) -> List[Dict]:
    """Persistent dedupe: drop articles whose URL is already in ai-knowledge.db."""
    conn = open_knowledge_db()
    if conn is None:
        return articles
    try:
        seen = {row[0] for row in conn.execute(
            "SELECT url FROM content_sources WHERE type='article'"
        )}
    finally:
        conn.close()

    fresh = []
    dropped = 0
    for a in articles:
        if _normalize_url(a.get('url', '')) in seen or a.get('url', '') in seen:
            dropped += 1
            continue
        fresh.append(a)
    if dropped:
        print(f"  Persistent dedupe: dropped {dropped} previously-seen articles")
    return fresh


_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def extract_full_text(url: str, timeout: int = 15) -> str:
    """Fetch and extract main article body. Returns empty string on failure.

    Uses requests with a real Chrome UA (trafilatura's default UA is blocked
    by most modern sites) and hands the HTML to trafilatura.extract.
    """
    if not HAS_TRAFILATURA or not url:
        return ""
    try:
        r = requests.get(url, headers={"User-Agent": _USER_AGENT},
                         timeout=timeout, allow_redirects=True)
        if r.status_code >= 400 or not r.text:
            return ""
        text = trafilatura.extract(
            r.text,
            url=url,
            include_comments=False,
            include_tables=False,
            favor_recall=True,
        )
        return (text or "").strip()
    except requests.exceptions.RequestException:
        return ""
    except Exception as e:
        print(f"    extract_full_text error for {url[:60]}: {e}")
        return ""


def write_archive(article: Dict, full_text: str):
    """Write the full article text to ORICO (or local fallback)."""
    if not full_text:
        return None
    try:
        root, on_orico = _archive_root()
        date_dir = root / article.get('date', datetime.now().strftime('%Y-%m-%d'))
        date_dir.mkdir(parents=True, exist_ok=True)
        h = hashlib.sha1(_normalize_url(article['url']).encode()).hexdigest()[:10]
        path = date_dir / f"{_slug(article['source'])}--{_slug(article['title'])}--{h}.txt"
        path.write_text(full_text)
        return path
    except Exception as e:
        print(f"    write_archive failed: {e}")
        return None


def write_vault_markdown(article: Dict, full_text: str) -> Optional[Path]:
    """Write to ~/Obsidian/JARVIS/News/YYYY-MM-DD/ so Phase 2B indexer sees it."""
    try:
        date_dir = VAULT_ROOT / article.get('date', datetime.now().strftime('%Y-%m-%d'))
        date_dir.mkdir(parents=True, exist_ok=True)
        h = hashlib.sha1(_normalize_url(article['url']).encode()).hexdigest()[:10]
        slug = _slug(article['source']) + "--" + _slug(article['title']) + "--" + h
        path = date_dir / f"{slug}.md"

        body_text = full_text if full_text else article.get('summary', '')
        title = (article.get('title') or '').replace('"', "'")
        fm = (
            "---\n"
            f"source: \"{article.get('source','')}\"\n"
            f"title: \"{title}\"\n"
            f"url: {article.get('url','')}\n"
            f"published: {article.get('published_at','')}\n"
            f"captured_chars: {len(body_text)}\n"
            f"full_text_extracted: {bool(full_text)}\n"
            f"topics: {categorize_article(article.get('title',''), article.get('summary',''))}\n"
            "tags: [news, ai, article]\n"
            "---\n\n"
        )
        body = (
            f"# {article.get('title','')}\n\n"
            f"**Source:** {article.get('source','')}  \n"
            f"**Published:** {article.get('published_at','')}  \n"
            f"**Read original:** {article.get('url','')}\n\n"
            f"## Article\n\n{body_text}\n"
        )
        path.write_text(fm + body)
        return path
    except Exception as e:
        print(f"    vault write failed: {e}")
        return None


def persist_to_knowledge(article: Dict, full_text: str, vault_path: Optional[Path]) -> bool:
    """Insert into ai-knowledge.db as type='article'."""
    conn = open_knowledge_db()
    if conn is None:
        return False
    try:
        conn.execute(
            """INSERT INTO content_sources
               (type, title, url, author, published_date, transcript_path,
                indexed_at, last_updated, metadata)
               VALUES('article', ?, ?, ?, ?, ?, datetime('now'), datetime('now'), ?)""",
            (
                article.get('title', ''),
                article.get('url', ''),
                article.get('source', ''),
                (article.get('published_at') or '')[:10],
                str(vault_path) if vault_path else None,
                json.dumps({
                    'source': article.get('source', ''),
                    'guid': article.get('guid', ''),
                    'summary': article.get('summary', ''),
                    'full_text_chars': len(full_text or ''),
                    'topics': categorize_article(article.get('title',''), article.get('summary','')),
                }),
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # url uniqueness collision; benign
    except Exception as e:
        print(f"    knowledge-db write failed: {e}")
        return False
    finally:
        conn.close()


def categorize_article(title: str, summary: str = '') -> List[str]:
    """Categorize article by topic."""
    text = (title + ' ' + summary).lower()
    tags = []

    for topic, keywords in TOPICS.items():
        if any(keyword in text for keyword in keywords):
            tags.append(topic)

    return tags if tags else ['General AI']


def generate_digest(
    articles: List[Dict],
    date: str,
    max_total: int = 40,
    per_source_quota: int = 3,
    dead_feeds: Optional[List[str]] = None,
) -> str:
    """Generate markdown digest with per-source diversity.

    Picks up to ``per_source_quota`` highest-scoring articles per source,
    then fills the rest in score order, capped at ``max_total``. Corpus still
    contains all articles — this only affects email rendering.
    """
    by_source: Dict[str, List[Dict]] = {}
    for a in sorted(articles, key=lambda x: x.get('score', 0), reverse=True):
        by_source.setdefault(a['source'], []).append(a)

    # Stage 1: take up to per_source_quota from each source (round-robin)
    digest_pool: List[Dict] = []
    pools = {src: list(lst) for src, lst in by_source.items()}
    while len(digest_pool) < max_total:
        progressed = False
        for src in list(pools.keys()):
            if not pools[src]:
                continue
            # Count how many of this source we've already taken
            taken = sum(1 for d in digest_pool if d['source'] == src)
            if taken >= per_source_quota:
                continue
            digest_pool.append(pools[src].pop(0))
            progressed = True
            if len(digest_pool) >= max_total:
                break
        if not progressed:
            break

    md = f"# AI News Digest - {date}\n\n"
    md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    md += f"- **New articles today:** {len(articles)} across {len(by_source)} sources\n"
    md += f"- **Showing top {len(digest_pool)}** (max {per_source_quota}/source for diversity)\n"
    md += f"- **All {len(articles)} stored in ai-knowledge.db** — query JARVIS for the full set\n\n"

    if dead_feeds:
        md += f"⚠️  **Feeds with no items in last 5 days:** {', '.join(dead_feeds)}\n\n"

    md += "---\n\n"
    md += "## 📰 Today's Stories\n\n"

    # Group display by source so you can scan
    shown_by_source: Dict[str, List[Dict]] = {}
    for a in digest_pool:
        shown_by_source.setdefault(a['source'], []).append(a)

    for source, items in sorted(shown_by_source.items(), key=lambda kv: -len(kv[1])):
        md += f"### {source} ({len(items)})\n\n"
        for article in items:
            title = article.get('title', 'Untitled')
            url = article.get('url', '#')
            summary = article.get('summary', '')
            topics = categorize_article(title, summary)
            md += f"- **[{title}]({url})**  \n"
            if topics:
                md += f"  *Topics:* {', '.join(topics)}  \n"
            if summary:
                snippet = summary[:280].replace('\n', ' ').strip()
                if len(summary) > 280:
                    snippet = snippet.rsplit(' ', 1)[0] + '…'
                md += f"  {snippet}\n"
            md += "\n"
        md += "\n"

    md += "---\n\n"
    md += "## 📊 Today's Source Breakdown\n\n"

    source_counts = {}
    for article in articles:
        src = article['source']
        source_counts[src] = source_counts.get(src, 0) + 1

    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        shown = sum(1 for d in digest_pool if d['source'] == src)
        md += f"- **{src}:** {count} new ({shown} shown)\n"

    md += "\n*Generated by JARVIS news-aggregator skill*\n"

    return md


def backfill_full_text(limit: int = 100):
    """One-shot: re-extract full body for stored articles whose full_text_chars=0."""
    conn = open_knowledge_db()
    if conn is None:
        print("No ai-knowledge.db — nothing to backfill")
        return
    rows = conn.execute(
        """SELECT id, title, url, author, published_date, transcript_path, metadata
           FROM content_sources
           WHERE type='article' AND (metadata IS NULL OR metadata NOT LIKE '%full_text_chars\": [1-9]%')
           ORDER BY id DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    print(f"Backfilling {len(rows)} articles with missing full text...")
    fixed = 0
    for rid, title, url, source, pub_date, vault_path, meta_json in rows:
        full_text = extract_full_text(url)
        if not full_text:
            continue
        article = {
            'title': title, 'url': url, 'source': source,
            'published_at': pub_date or '', 'date': pub_date or datetime.now().strftime('%Y-%m-%d'),
            'summary': '',
        }
        archive_path = write_archive(article, full_text)
        new_vault_path = write_vault_markdown(article, full_text)
        try:
            md = json.loads(meta_json) if meta_json else {}
        except Exception:
            md = {}
        md['full_text_chars'] = len(full_text)
        conn.execute(
            "UPDATE content_sources SET transcript_path=?, metadata=?, last_updated=datetime('now') WHERE id=?",
            (str(new_vault_path) if new_vault_path else vault_path, json.dumps(md), rid),
        )
        fixed += 1
        if fixed % 10 == 0:
            conn.commit()
            print(f"  {fixed}/{len(rows)}")
    conn.commit()
    conn.close()
    print(f"✓ Backfilled {fixed}/{len(rows)} articles")


def main():
    parser = argparse.ArgumentParser(description='Aggregate AI news from multiple sources')
    parser.add_argument('mode', choices=['daily', 'backfill'], help='Aggregation mode')
    parser.add_argument('--date', help='Date (YYYY-MM-DD), default: today')
    parser.add_argument('--output', help='Output file path', default='digest.md')
    parser.add_argument('--limit', type=int, default=100, help='Backfill limit')

    args = parser.parse_args()

    if args.mode == 'backfill':
        backfill_full_text(limit=args.limit)
        return

    # Parse date
    if args.date:
        target_date = args.date
    else:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"AI News Aggregator - {target_date}")
    print("=" * 60)

    # ── Aggregate from all sources ────────────────────────────────────────
    all_articles: List[Dict] = []
    per_source_raw: Dict[str, int] = {}

    # Hacker News (API - fast and reliable)
    hn_articles = fetch_hackernews()
    all_articles.extend(hn_articles)
    per_source_raw['Hacker News'] = len(hn_articles)

    # Fetch all RSS feeds (includes Reddit subs and Substacks)
    rss_feeds = load_rss_feeds()
    print(f"Fetching RSS feeds: {len(rss_feeds)} configured sources")

    for source_name, feed_url in rss_feeds.items():
        rss_articles = fetch_rss_feed(source_name, feed_url)
        all_articles.extend(rss_articles)
        per_source_raw[source_name] = len(rss_articles)

    print()
    print(f"Total articles collected: {len(all_articles)}")

    # ── Filter for relevance ──────────────────────────────────────────────
    # Sources whose entire feed is AI-by-definition bypass the keyword filter.
    print("Filtering for AI relevance...")
    AI_DEDICATED_SOURCES = {
        'Hacker News',  # already pre-filtered upstream
        'Import AI (Jack Clark)',
        'Latent Space (swyx)',
        'AI Snake Oil (Narayanan)',
        'One Useful Thing (Mollick)',
        'The Algorithmic Bridge',
        'Last Week in AI',
        'OpenAI News',
        'Anthropic News',
        'Anthropic Research',
        'Google DeepMind',
        'Google AI Blog',
        'Hugging Face Blog',
        'LangChain Changelog',
        'BAIR Blog',
        'ChinAI Newsletter',
    }
    def _passes_relevance(a):
        src = a.get('source', '')
        if src.startswith('Reddit:'):
            return True
        if src in AI_DEDICATED_SOURCES:
            return True
        return is_ai_relevant(a.get('title', ''))
    relevant_articles = [a for a in all_articles if _passes_relevance(a)]
    print(f"  Relevant articles: {len(relevant_articles)}")

    # ── Within-batch dedupe (same article, multiple feeds) ────────────────
    print("Within-batch dedupe...")
    unique_articles = deduplicate_articles(relevant_articles)

    # ── Persistent dedupe vs ai-knowledge.db ──────────────────────────────
    print("Persistent dedupe (vs ai-knowledge.db)...")
    fresh_articles = filter_already_seen(unique_articles)
    print(f"  Fresh articles: {len(fresh_articles)}")

    # ── Compute relevance score (used by digest's diversity sort) ─────────
    for a in fresh_articles:
        a['score'] = calculate_relevance_score(a.get('title', ''), a.get('summary', ''))

    # ── Full-text fetch + persist to all 3 surfaces ───────────────────────
    print(f"Full-text fetch + persist ({len(fresh_articles)} articles)...")
    persisted = 0
    extracted = 0
    for i, a in enumerate(fresh_articles, 1):
        # Reddit self-posts: use selftext directly (no need to refetch).
        # Reddit link posts: fall through to trafilatura against external URL.
        if a.get('_is_self') and a.get('_selftext'):
            full_text = a['_selftext']
        else:
            full_text = extract_full_text(a.get('url', ''))
        if full_text:
            extracted += 1
        archive_path = write_archive(a, full_text)
        vault_path = write_vault_markdown(a, full_text)
        if persist_to_knowledge(a, full_text, vault_path):
            persisted += 1
        a['full_text_chars'] = len(full_text)
        a['archive_path'] = str(archive_path) if archive_path else ''
        if i % 10 == 0:
            print(f"  {i}/{len(fresh_articles)} ({extracted} with full body, {persisted} stored)")
    print(f"  ✓ {extracted}/{len(fresh_articles)} articles got full body via trafilatura")
    print(f"  ✓ {persisted} rows written to ai-knowledge.db (type='article')")

    # ── Flag dead feeds (0 articles raw) ──────────────────────────────────
    dead_feeds = [s for s, n in per_source_raw.items() if n == 0]
    if dead_feeds:
        print(f"  ⚠️  0-article feeds today: {', '.join(dead_feeds)}")

    # ── Generate digest with per-source quota (40 total, max 3/source) ────
    print("Generating digest (per-source quota: 3, max total: 40)...")
    digest_md = generate_digest(
        fresh_articles,
        target_date,
        max_total=40,
        per_source_quota=3,
        dead_feeds=dead_feeds,
    )

    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(digest_md)

    print(f"\n✓ Digest saved to: {output_path}")
    print(f"  Articles in digest pool: {min(40, len(fresh_articles))}")
    print(f"  Articles in corpus: {persisted}")


if __name__ == '__main__':
    main()
