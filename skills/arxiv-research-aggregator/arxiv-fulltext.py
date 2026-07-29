#!/usr/bin/env python3
"""arxiv-fulltext.py — on-demand full-text capture for a single arXiv paper.

The weekly arXiv digest stores abstracts + PDF links only (Option C). When you
want the WHOLE paper in the knowledge base, point this at it — by arXiv id, an
abs/pdf URL, or (as a convenience) the paper's title from the digest. It:
  1. resolves the arXiv id,
  2. pulls the full text (arXiv native HTML → ar5iv → PDF+pdftotext fallback),
  3. writes a full-text markdown into the Obsidian vault so the next reindex
     embeds it into the searchable KB,
  4. archives a plain-text copy.

Usage (any of these):
  arxiv-fulltext.py 2607.16903
  arxiv-fulltext.py https://arxiv.org/abs/2607.16903
  arxiv-fulltext.py "A Method for Learning Value Systems in Generative AI"

Needs a python with requests + trafilatura (the news-aggregator venv has both);
falls back to pdftotext (system) for PDFs.
"""
import argparse
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

try:
    import trafilatura
    HAS_TRAFI = True
except Exception:
    HAS_TRAFI = False

UA = "JARVIS-arxiv-fulltext/1.0 (byrdter@auburn.edu)"
VAULT = Path.home() / "Obsidian/JARVIS/arXiv-FullText"
ARCHIVE = Path.home() / "Library/CloudStorage/Dropbox/jarvis-private/reports/arxiv-fulltext"
ARXIV_API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}
ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def arxiv_api(params: dict, tries: int = 5) -> str:
    """GET the arXiv API, retrying on the plain-text 'Rate exceeded' throttle.
    arXiv asks for ~3s between hits; this backs off politely."""
    for i in range(tries):
        try:
            r = requests.get(ARXIV_API, params=params, headers={"User-Agent": UA}, timeout=45)
            if r.text.lstrip().startswith("<?xml"):
                return r.text
        except requests.RequestException:
            pass
        time.sleep(3 * (i + 1))  # 3,6,9,12s
    raise SystemExit("arXiv API is rate-limiting or unavailable — wait ~30s and retry.")


def resolve_id(arg: str) -> str:
    """Return a bare arXiv id from an id, abs/pdf URL, or title search."""
    m = ID_RE.search(arg)
    if m and ("arxiv.org" in arg or arg.strip().startswith(m.group(0)) or re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", arg.strip())):
        return m.group(1)
    # treat as a title → search arXiv
    print(f"  → searching arXiv by title: {arg[:70]}…")
    root = ET.fromstring(arxiv_api({"search_query": f'ti:"{arg}"', "max_results": 1}))
    entry = root.find("atom:entry", NS)
    if entry is None:
        raise SystemExit(f"No arXiv match for: {arg}")
    idu = entry.find("atom:id", NS).text
    mm = ID_RE.search(idu)
    if not mm:
        raise SystemExit(f"Could not parse id from {idu}")
    print(f"  → matched: {entry.find('atom:title', NS).text.strip()[:70]}")
    return mm.group(1)


def metadata(aid: str) -> dict:
    e = ET.fromstring(arxiv_api({"id_list": aid})).find("atom:entry", NS)
    if e is None:
        return {"title": aid, "authors": "", "abstract": "", "published": ""}
    authors = ", ".join(a.find("atom:name", NS).text for a in e.findall("atom:author", NS))
    return {
        "title": (e.find("atom:title", NS).text or "").strip().replace("\n", " "),
        "authors": authors,
        "abstract": (e.find("atom:summary", NS).text or "").strip(),
        "published": (e.find("atom:published", NS).text or "")[:10],
    }


def fetch_fulltext(aid: str) -> tuple[str, str]:
    """Return (full_text, method). Try HTML then PDF."""
    if HAS_TRAFI:
        for url in (f"https://arxiv.org/html/{aid}", f"https://ar5iv.labs.arxiv.org/html/{aid}"):
            try:
                r = requests.get(url, headers={"User-Agent": UA}, timeout=45, allow_redirects=True)
                if r.status_code == 200 and len(r.text) > 3000:
                    t = trafilatura.extract(r.text, include_comments=False, favor_recall=True)
                    if t and len(t) > 2000:
                        return t.strip(), f"html ({'arxiv' if 'arxiv.org/html' in url else 'ar5iv'})"
            except requests.RequestException:
                pass
    # PDF fallback
    try:
        r = requests.get(f"https://arxiv.org/pdf/{aid}", headers={"User-Agent": UA}, timeout=90)
        if r.status_code == 200 and r.content[:4] == b"%PDF":
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                f.write(r.content)
                pdf_path = f.name
            out = subprocess.run(["pdftotext", "-nopgbrk", pdf_path, "-"],
                                 capture_output=True, text=True, timeout=120)
            txt = re.sub(r"\n{3,}", "\n\n", out.stdout).strip()
            if len(txt) > 1000:
                return txt, "pdf (pdftotext)"
    except Exception as e:
        print(f"  PDF fallback error: {e}")
    return "", "none"


def main():
    ap = argparse.ArgumentParser(description="On-demand full-text capture for one arXiv paper.")
    ap.add_argument("paper", help="arXiv id, abs/pdf URL, or paper title")
    ap.add_argument("--no-vault", action="store_true", help="don't write to the KB vault")
    args = ap.parse_args()

    aid = resolve_id(args.paper)
    meta = metadata(aid)
    print(f"  paper: {meta['title'][:72]}")
    full, method = fetch_fulltext(aid)
    if not full:
        raise SystemExit(f"✗ could not get full text for {aid} (tried HTML + PDF).")
    words = len(full.split())
    print(f"  ✓ full text via {method}: {words:,} words")

    stamp = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", meta["title"].lower())[:60].strip("-") or aid
    fm = (
        "---\n"
        f'title: "{meta["title"].replace(chr(34), chr(39))}"\n'
        f"authors: {meta['authors']}\n"
        f"arxiv_id: {aid}\n"
        f"url: https://arxiv.org/abs/{aid}\n"
        f"pdf_url: https://arxiv.org/pdf/{aid}\n"
        f"source: \"arXiv (full text)\"\n"
        f"published: {meta['published']}\n"
        f"captured: {stamp}\n"
        f"full_text_extracted: true\n"
        f"full_text_chars: {len(full)}\n"
        f"extraction: {method}\n"
        "tags: [arxiv, research, full-text]\n"
        "---\n\n"
    )
    body = (f"# {meta['title']}\n\n**Authors:** {meta['authors']}\n\n"
            f"**arXiv:** [{aid}](https://arxiv.org/abs/{aid})\n\n"
            f"## Abstract\n\n{meta['abstract']}\n\n## Full Text\n\n{full}\n")
    doc = fm + body

    # archive copy (always)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / f"{aid}--{slug}.md").write_text(doc)
    # vault copy → embedded into the KB on next reindex
    if not args.no_vault:
        vdir = VAULT / stamp
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / f"{aid}--{slug}.md").write_text(doc)
        print(f"  ✓ vault: {vdir / (aid + '--' + slug + '.md')}")
        print("  → will be searchable after the next reindex "
              "(cd agent-sdk && bun run scripts/index-vault.ts)")
    print(f"  ✓ archive: {ARCHIVE / (aid + '--' + slug + '.md')}")


if __name__ == "__main__":
    main()
