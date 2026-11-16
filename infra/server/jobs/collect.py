#!/usr/bin/env python3
"""Collect: pull new items from the sources in sources.toml into the inbox, one markdown file each.

The inbox lives on the server (INBOX, outside git). Nobody reads it; curate.py promotes what matters
into the brain wiki, and day folders older than INBOX_DAYS are deleted. It doubles as a searchable
library of the last month for the chat session (`grep -ri <term> ~/.local/share/jarvis/inbox`).

Usage: collect.py [--dry-run] [--only SOURCE_ID]
A source seen for the first time emits only its 2 newest items and remembers the rest, so adding a
source never floods the inbox with its back catalog."""
import gzip
import html
import json
import re
import shutil
import sys
import tomllib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

from jarvis_jobs import CFG, INBOX, github_token, log, now_local, read_state, write_state

JOB = "collect"
HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (compatible; jarvis-collector/1.0)"
FIRST_RUN_KEEP = 2
SEEN_CAP = 600
AI_WORDS = re.compile(
    r"\b(AI|A\.I\.|LLMs?|GPT[-\w.]*|Claude|Anthropic|OpenAI|Gemini|Qwen|Llama|Mistral|DeepSeek|"
    r"agents?|agentic|MCP|model|models|inference|RAG|embeddings?|transformer|Copilot|Cursor|Codex|"
    r"fine-?tun\w*|vibe cod\w*|prompt\w*|chatbot|neural|diffusion|open-?weights?)\b", re.I)


# ---------- helpers ---------------------------------------------------------------------------
def fetch(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":  # some servers gzip even when not asked
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def to_text(s: str, cap: int = 6000) -> str:
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s or "")
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s).strip()
    return s[:cap] + (" [...]" if len(s) > cap else "")


def iso(dt_str: str) -> str:
    """Best-effort ISO date from RSS/Atom date strings; '' when unknown."""
    if not dt_str:
        return ""
    try:
        return parsedate_to_datetime(dt_str).astimezone(timezone.utc).isoformat(timespec="minutes")
    except (TypeError, ValueError):
        pass
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).isoformat(timespec="minutes")
    except ValueError:
        return dt_str[:25]


def slugify(s: str, n: int = 60) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n] or "item"


def item(uid, title, url, published="", text="", extra=""):
    return {"uid": str(uid), "title": (title or "(untitled)").strip(), "url": url,
            "published": published, "text": text, "extra": extra}


# ---------- source kinds ----------------------------------------------------------------------
def k_rss(src):
    root = ET.fromstring(fetch(src["url"]).encode())
    out = []
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag not in ("item", "entry"):
            continue
        f = {}
        for c in el:
            t = c.tag.rsplit("}", 1)[-1]
            if t == "link":
                f.setdefault("link", c.get("href") or (c.text or "").strip())
            elif t in ("encoded", "content") and c.text:
                f["body"] = c.text
            elif t in ("description", "summary") and c.text:
                f.setdefault("body", c.text)
            elif c.text:
                f.setdefault(t, c.text.strip())
        link = f.get("link", "")
        out.append(item(f.get("id") or f.get("guid") or link, f.get("title"), link,
                        iso(f.get("published") or f.get("pubDate") or f.get("updated") or ""),
                        to_text(f.get("body", ""))))
    return out


def k_sitemap(src):
    xml = fetch(src["url"])
    out = []
    for loc, lastmod in re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?", xml):
        if loc.startswith(src["prefix"]) and loc.rstrip("/") != src["prefix"].rstrip("/"):
            out.append(item(loc, "", loc, iso(lastmod or "")))
    out.sort(key=lambda i: i["published"], reverse=True)
    return out


def enrich_page(it):
    """Sitemap items have only a URL: pull title and description from the page itself."""
    try:
        page = fetch(it["url"])
    except Exception:
        return it
    t = re.search(r'<meta property="og:title" content="([^"]+)"', page) or re.search(r"<title>([^<]+)", page)
    d = re.search(r'<meta (?:name="description"|property="og:description") content="([^"]+)"', page)
    it["title"] = html.unescape(t.group(1)) if t else it["url"].rstrip("/").rsplit("/", 1)[-1]
    body = re.search(r"(?is)<article.*?</article>", page) or re.search(r"(?is)<main.*?</main>", page)
    it["text"] = (html.unescape(d.group(1)) + "\n\n" if d else "") + to_text(body.group(0) if body else "", 5000)
    return it


def k_hn(src):
    since = int((datetime.now(timezone.utc) - timedelta(days=1)).timestamp())
    q = urllib.parse.urlencode({"tags": "story", "hitsPerPage": 100,
                                "numericFilters": f"points>={src.get('min_points', 150)},created_at_i>{since}"})
    hits = json.loads(fetch(f"https://hn.algolia.com/api/v1/search?{q}"))["hits"]
    out = []
    for h in sorted(hits, key=lambda h: -h.get("points", 0)):
        if not AI_WORDS.search(h.get("title", "")):
            continue
        disc = f"https://news.ycombinator.com/item?id={h['objectID']}"
        out.append(item(h["objectID"], h["title"], h.get("url") or disc, iso(h.get("created_at", "")),
                        to_text(h.get("story_text") or ""),
                        f"{h.get('points')} points, {h.get('num_comments')} comments. Discussion: {disc}"))
    return out


def k_github_trending(src):
    since = (datetime.now(timezone.utc) - timedelta(days=14)).date().isoformat()
    headers = {"Accept": "application/vnd.github+json"}
    tok = github_token()
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    repos = {}
    for topic in ("ai-agents", "agents", "llm", "mcp", "claude-code", "agentic-ai"):
        q = urllib.parse.urlencode({"q": f"topic:{topic} created:>{since} stars:>100",
                                    "sort": "stars", "order": "desc", "per_page": 10})
        for r in json.loads(fetch(f"https://api.github.com/search/repositories?{q}", headers))["items"]:
            repos[r["full_name"]] = r
    out = []
    for r in sorted(repos.values(), key=lambda r: -r["stargazers_count"]):
        out.append(item(r["full_name"], f"{r['full_name']}: {r.get('description') or ''}"[:150],
                        r["html_url"], iso(r.get("created_at", "")), to_text(r.get("description") or ""),
                        f"{r['stargazers_count']} stars, language {r.get('language')}, "
                        f"topics: {', '.join(r.get('topics', [])[:8])}"))
    return out


def k_hf_trending(src):
    models = json.loads(fetch("https://huggingface.co/api/models?sort=trendingScore&limit=30"))
    out = []
    for m in models:
        out.append(item(m["id"], f"Trending model: {m['id']}", f"https://huggingface.co/{m['id']}",
                        iso(m.get("createdAt", "")), "",
                        f"task {m.get('pipeline_tag')}, {m.get('likes')} likes, "
                        f"{m.get('downloads')} downloads, library {m.get('library_name')}"))
    return out


YT_HEADERS = {"Accept-Language": "en-US", "Cookie": "SOCS=CAI"}


def _walk(o, key):
    if isinstance(o, dict):
        if key in o:
            yield o[key]
        for v in o.values():
            yield from _walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v, key)


def _json_after(page: str, marker: str):
    i = page.find(marker)
    if i < 0:
        return None
    try:
        return json.JSONDecoder().raw_decode(page[page.index("{", i):])[0]
    except ValueError:
        return None


def k_youtube(src):
    page = fetch(f"https://www.youtube.com/channel/{src['channel_id']}/videos", YT_HEADERS)
    data = _json_after(page, "ytInitialData") or {}
    out = []
    for vr in _walk(data, "videoRenderer"):  # older page layout
        vid = vr.get("videoId")
        title = "".join(r.get("text", "") for r in vr.get("title", {}).get("runs", []))
        if vid and title:
            out.append(item(vid, title, f"https://www.youtube.com/watch?v={vid}"))
    for lv in _walk(data, "lockupViewModel"):  # layout as of 2026-11
        if lv.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO":
            continue
        title = lv.get("metadata", {}).get("lockupMetadataViewModel", {}).get("title", {}).get("content")
        if lv.get("contentId") and title:
            out.append(item(lv["contentId"], title, f"https://www.youtube.com/watch?v={lv['contentId']}"))
    return out


def enrich_youtube(it):
    try:
        page = fetch(it["url"], YT_HEADERS)
    except Exception:
        return it
    pr = _json_after(page, "ytInitialPlayerResponse") or {}
    vd = pr.get("videoDetails", {})
    mf = pr.get("microformat", {}).get("playerMicroformatRenderer", {})
    it["published"] = mf.get("publishDate", "") or it["published"]
    mins = int(vd.get("lengthSeconds", 0) or 0) // 60
    it["extra"] = f"{vd.get('author', '')}, {mins} min, {vd.get('viewCount', '?')} views"
    it["text"] = to_text(vd.get("shortDescription", ""), 4000)
    return it


KINDS = {"rss": k_rss, "sitemap": k_sitemap, "hn": k_hn, "github-trending": k_github_trending,
         "hf-trending": k_hf_trending, "youtube": k_youtube}
ENRICH = {"sitemap": enrich_page, "youtube": enrich_youtube}


# ---------- main ------------------------------------------------------------------------------
def write_item(day_dir: Path, src: dict, it: dict) -> Path:
    name = f"{src['id']}--{slugify(it['title'])}.md"
    p = day_dir / name
    lines = [f"# {it['title']}", "", f"- source: {src['name']} ({src['id']})", f"- url: {it['url']}"]
    if it["published"]:
        lines.append(f"- published: {it['published']}")
    if it["extra"]:
        lines.append(f"- notes: {it['extra']}")
    lines += [f"- collected: {datetime.now(timezone.utc).isoformat(timespec='minutes')}", "", it["text"]]
    p.write_text("\n".join(lines).rstrip() + "\n")
    return p


def expire(days: int) -> int:
    cutoff = (now_local() - timedelta(days=days)).date().isoformat()
    gone = 0
    for d in INBOX.glob("20??-??-??"):
        if d.is_dir() and d.name < cutoff:
            shutil.rmtree(d)
            gone += 1
    return gone


def main(argv) -> int:
    dry = "--dry-run" in argv
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    sources = tomllib.loads((HERE / "sources.toml").read_text())["source"]
    seen = read_state("collect-seen", {})
    today = now_local().date().isoformat()
    day_dir = INBOX / today
    if not dry:
        day_dir.mkdir(parents=True, exist_ok=True)
    report, total, failed = [], 0, []
    for src in sources:
        if only and src["id"] != only:
            continue
        try:
            items = KINDS[src["kind"]](src)
        except Exception as e:
            failed.append(src["id"])
            log(JOB, f"FAIL {src['id']}: {type(e).__name__}: {str(e)[:200]}")
            continue
        known = set(seen.get(src["id"], []))
        first = src["id"] not in seen
        new = [i for i in items if i["uid"] not in known]
        keep = new[:FIRST_RUN_KEEP if first else int(src.get("max", 5))]
        if src["kind"] in ENRICH:
            keep = [ENRICH[src["kind"]](i) for i in keep]
        if dry:
            print(f"[{src['id']}] {len(items)} listed, {len(new)} new, keeping {len(keep)}"
                  f"{' (first run)' if first else ''}")
            for i in keep:
                print(f"   - {i['title'][:100]} | {i['published']} | {i['url']}")
            continue
        for i in keep:
            write_item(day_dir, src, i)
            report.append(f"- [{src['name']}] {i['title']} ({i['url']})")
        # Remember everything listed (not just what we kept), so a busy feed doesn't resurface
        # yesterday's overflow tomorrow.
        seen[src["id"]] = (list(dict.fromkeys([i["uid"] for i in items] + seen.get(src["id"], []))))[:SEEN_CAP]
        total += len(keep)
    if dry:
        return 0
    write_state("collect-seen", seen)
    idx = day_dir / "INDEX.md"
    with idx.open("a") as fh:
        if idx.stat().st_size == 0:
            fh.write(f"# Inbox {today}\n\nOne line per collected item. Files sit next to this index.\n\n")
        fh.write("\n".join(report) + ("\n" if report else ""))
    gone = expire(int(CFG.get("INBOX_DAYS", "30")))
    write_state(JOB, {"last_run": today, "items": total, "failed": failed})
    log(JOB, f"collected {total} items into {day_dir} ({len(failed)} sources failed: "
             f"{', '.join(failed) or 'none'}; expired {gone} old day folders)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
