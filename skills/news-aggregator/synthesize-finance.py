#!/usr/bin/env python3
"""Turn a day of financial articles into a brief with conclusions.

The digest that aggregate.py produces is a LIST. This is the layer that reads
it: what happened, what it means, and -- the part a list can never give you --
where today's sources contradict each other, weighted by how much each source
has earned.

Runs Claude via the CLI subprocess ($0 on the Max subscription, the Phase 3A
pattern) rather than the API.

Reads:  ai-knowledge.db, domain='finance', for the chosen date
        config/source-weights.json
        config/holdings.csv          (optional -- see --holdings)
Writes: reports/finance-digests/finance-brief-<date>.md

Usage:
  ./venv/bin/python synthesize-finance.py
  ./venv/bin/python synthesize-finance.py --date 2026-08-23 --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config"
DB = HERE.parents[1] / "agent-sdk" / "data" / "ai-knowledge.db"
OUT_DIR = HERE.parents[1] / "reports" / "finance-digests"
HOLDINGS = CONFIG / "holdings.csv"

DEFAULT_WEIGHT = 0.5
# Keep the prompt inside a comfortable context budget. Articles are added
# highest-weight first, so truncation drops the least reliable material rather
# than whatever happens to sort last.
MAX_PROMPT_CHARS = 90_000
PER_ARTICLE_CHARS = 1_200


def load_weights() -> dict:
    p = CONFIG / "source-weights.json"
    if not p.exists():
        return {}
    return {k: v for k, v in json.loads(p.read_text()).items()
            if not k.startswith("_") and isinstance(v, (int, float))}


PORTFOLIO_DB = (Path.home() /
                "Library/CloudStorage/Dropbox/jarvis-private/portfolio/portfolio.db")

# Broker descriptions are truncated and punctuation-free ("BANK NEW YORK
# MELLON COR", "JAZZ PHARMACEUTICALS P F"), so they make poor search terms.
# Map each holding to the names it is actually referred to by in the press.
# Explicit beats clever here: a wrong match puts a story about the wrong
# company into a brief about your money.
NAME_ALIASES = {
    "AAPL": ["Apple"],
    "AIT": ["Applied Industrial Technologies"],
    "AMG": ["Affiliated Managers Group"],
    "ARMK": ["Aramark"],
    "BN": ["Brookfield Corporation", "Brookfield Corp"],
    "BNY": ["BNY Mellon", "Bank of New York Mellon", "BNY"],
    "COR": ["Cencora", "AmerisourceBergen"],
    "DOCU": ["DocuSign", "Docusign"],
    "ECL": ["Ecolab"],
    "FTNT": ["Fortinet"],
    "JAZZ": ["Jazz Pharmaceuticals"],
    "MSGS": ["Madison Square Garden Sports", "Madison Square Garden"],
    "NDAQ": ["Nasdaq Inc", "Nasdaq,"],
    "TD": ["Toronto-Dominion", "Toronto Dominion", "TD Bank"],
    "TJX": ["TJX", "TJ Maxx", "TJMaxx", "T.J. Maxx", "Marshalls"],
}

# Tickers at or under this length are too collision-prone to match on the
# symbol alone -- "TD", "BN", "COR" and "AIT" all appear in ordinary prose and
# in unrelated acronyms. Short tickers match on company name only.
MIN_TICKER_MATCH_LEN = 4


def load_holdings(csv_path: Path) -> list[dict]:
    """Current positions to rank against.

    Primary source is the portfolio store written by
    skills/portfolio/import-positions.py: the latest snapshot of each account,
    consolidated across accounts, cash and money market excluded. A position
    held in two accounts is ONE exposure, so it is summed rather than listed
    twice.

    Falls back to a CSV for anything not yet imported (syndications, external
    accounts) so the brief is never blocked on the store being complete.
    """
    if PORTFOLIO_DB.exists():
        con = sqlite3.connect(str(PORTFOLIO_DB))
        try:
            rows = con.execute("""
                SELECT p.symbol, p.description,
                       SUM(p.quantity), SUM(p.market_value), SUM(p.cost_basis),
                       COUNT(DISTINCT s.account_id)
                FROM positions p
                JOIN snapshots s ON s.id = p.snapshot_id
                WHERE s.as_of = (SELECT MAX(as_of) FROM snapshots s2
                                 WHERE s2.account_id = s.account_id)
                  AND p.asset_class NOT IN ('cash','money_market')
                  AND p.symbol IS NOT NULL
                GROUP BY p.symbol ORDER BY SUM(p.market_value) DESC
            """).fetchall()
        finally:
            con.close()
        invested = sum(r[3] or 0 for r in rows) or 1.0
        return [{"symbol": s, "description": d, "qty": q or 0,
                 "market_value": mv or 0, "cost_basis": cb or 0,
                 "gain": (mv or 0) - (cb or 0),
                 "pct_of_invested": (mv or 0) / invested * 100,
                 "accounts": n}
                for s, d, q, mv, cb, n in rows]

    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as fh:
            return [r for r in csv.DictReader(fh)
                    if any(v.strip() for v in r.values())]
    return []


def holdings_mentioned(text: str, holdings: list[dict]) -> list[str]:
    """Which holdings this text plausibly refers to.

    Matches a ticker only when it is long enough to be unambiguous, or when it
    appears in an explicit $TICKER / (TICKER) form. Otherwise falls back to
    company-name aliases.
    """
    hits = []
    for h in holdings:
        sym = (h.get("symbol") or "").strip().upper()
        if not sym:
            continue
        found = False
        if len(sym) >= MIN_TICKER_MATCH_LEN:
            found = re.search(rf"\b{re.escape(sym)}\b", text) is not None
        if not found:
            found = re.search(rf"[\$\(]{re.escape(sym)}\b", text) is not None
        if not found:
            for alias in NAME_ALIASES.get(sym, []):
                if re.search(rf"\b{re.escape(alias)}", text, re.I):
                    found = True
                    break
        if found:
            hits.append(sym)
    return hits


def fetch_articles(date: str, limit: int) -> list[dict]:
    if not DB.exists():
        raise SystemExit(f"ERROR: database not found: {DB}")
    con = sqlite3.connect(str(DB))
    try:
        cols = {r[1] for r in con.execute("pragma table_info(content_sources)")}
        if "domain" not in cols:
            raise SystemExit(
                "ERROR: content_sources has no `domain` column. Run "
                "migrate-add-domain.py --apply first, or this would synthesize "
                "the AI corpus and the finance corpus together.")
        rows = con.execute(
            "SELECT title, url, author, published_date, metadata "
            "FROM content_sources "
            "WHERE type='article' AND domain='finance' "
            "AND date(indexed_at)=? ORDER BY id DESC LIMIT ?",
            (date, limit)).fetchall()
    finally:
        con.close()

    out = []
    for title, url, author, pub, meta in rows:
        try:
            m = json.loads(meta or "{}")
        except Exception:
            m = {}
        out.append({"title": title or "", "url": url or "",
                    "source": author or "", "published": pub or "",
                    "summary": (m.get("summary") or "").strip(),
                    "chars": m.get("full_text_chars", 0)})
    return out


def _match_terms(sym: str) -> list[str]:
    terms = list(NAME_ALIASES.get(sym, []))
    if len(sym) >= MIN_TICKER_MATCH_LEN:
        terms.append(sym)
    return terms


def excerpt_around(text: str, hits: list[str], holdings: list[dict],
                   width: int = PER_ARTICLE_CHARS) -> str:
    """Excerpt centred on the first holding mention, not the article's head.

    Also reports how many times the holding appears, which is the cheapest
    available signal for whether the piece is ABOUT the company or merely
    name-drops it in passing -- a distinction the reader needs and a raw tag
    cannot make.
    """
    if not text:
        return ""
    first, counts = None, {}
    for sym in hits:
        n = 0
        for term in _match_terms(sym):
            for mm in re.finditer(rf"\b{re.escape(term)}", text, re.I):
                n += 1
                if first is None or mm.start() < first:
                    first = mm.start()
        counts[sym] = n

    if first is None:
        return text[:width]

    half = width // 2
    lo = max(0, first - half)
    hi = min(len(text), lo + width)
    body = text[lo:hi]
    if lo > 0:
        body = "…" + body
    if hi < len(text):
        body = body + "…"

    note = ", ".join(f"{s}×{n}" for s, n in counts.items() if n)
    if note:
        body = (f"[mentions in full article: {note}; excerpt centred on the "
                f"first mention, article is {len(text):,} chars]\n{body}")
    return body


def build_prompt(articles: list[dict], weights: dict,
                 holdings: list[dict], date: str) -> str:
    for a in articles:
        a["weight"] = weights.get(a["source"], DEFAULT_WEIGHT)
        a["hits"] = holdings_mentioned(f"{a['title']}\n{a['summary']}", holdings)

    # Holdings-relevant articles sort FIRST, ahead of source weight. The
    # prompt budget truncates the tail, and an article about a company you own
    # must never be the thing that gets dropped to make room for general
    # market colour from a more reputable outlet.
    articles.sort(key=lambda a: (not a["hits"], -a["weight"], -a["chars"]))

    lines, used, dropped, held_used = [], 0, 0, 0
    for a in articles:
        # For a tagged article, excerpt around the MENTION rather than from
        # the top. `summary` can hold a whole 79k-char essay while only
        # PER_ARTICLE_CHARS of it is sent, so a head-excerpt routinely told the
        # model "HOLDING: AAPL" and then showed it text with no Apple in it --
        # which it correctly called out as a bad tag.
        summary = (excerpt_around(a["summary"], a["hits"], holdings)
                   if a["hits"] else a["summary"][:PER_ARTICLE_CHARS])
        tag = f" | HOLDING: {', '.join(a['hits'])}" if a["hits"] else ""
        block = (f"\n[{a['source']} | reliability {a['weight']:.2f}{tag}]\n"
                 f"{a['title']}\n{summary}\nURL: {a['url']}\n")
        if used + len(block) > MAX_PROMPT_CHARS:
            dropped += 1
            continue
        lines.append(block)
        used += len(block)
        if a["hits"]:
            held_used += 1

    if holdings:
        rows = []
        for h in holdings:
            if "market_value" in h:
                rows.append(
                    f"  {h['symbol']:<6} {h['description'][:28]:<28} "
                    f"${h['market_value']:>9,.0f}  "
                    f"{h['pct_of_invested']:>5.1f}% of invested  "
                    f"{h['gain']:+,.0f} unrealized"
                    + (f"  [held in {h['accounts']} accounts]"
                       if h.get("accounts", 1) > 1 else ""))
            else:
                rows.append(f"  {h}")
        hold_txt = (
            "\nCURRENT POSITIONS — these are real holdings, not a watchlist:\n"
            + "\n".join(rows) +
            "\n\nArticles bearing on one of these are tagged HOLDING: <ticker> "
            "in the list below. Those tags come from name matching, so verify "
            "the article really is about that company before relying on it — "
            "say so if a tag looks wrong.")
        hold_task = (
            "4. YOUR HOLDINGS — go through the tagged articles and state what, "
            "if anything, bears on each position and how. Be specific about "
            "which position and what changed. Where a holding has no news "
            "today, do not mention it at all — a list of 'nothing material' "
            "lines is noise. If NOTHING touches any holding, write one line "
            "saying so.\n"
            "   Do NOT recommend buying, selling, trimming or adding. Report "
            "what happened and what it plausibly means for the business; the "
            "decision is the reader's alone.\n")
    else:
        hold_txt = ("\nCURRENT POSITIONS: not supplied. Skip the holdings "
                    "section entirely rather than guessing at a portfolio.")
        hold_task = ""

    build_prompt.stats = {"held_articles": held_used, "dropped": dropped,
                          "included": len(lines)}

    return f"""You are writing the daily financial brief for {date}.

Below are {len(lines)} articles collected today from verified financial feeds.
Each carries a RELIABILITY weight from 0.0 to 1.0 reflecting the source's
institutional rigour and corrections practice. Government statistics agencies
and central banks sit near 0.95; named analysts with checkable track records
near 0.85; wire services near 0.75; outlets with directional bias near 0.25.

Use the weights as follows:
- A claim from a high-weight source outranks a contradicting low-weight one.
- Never let a source below 0.4 settle a disputed fact on its own.
- Sources marked as radar are HEADLINE-ONLY: we have the headline, not the
  article. Treat those claims as unverified and say so when you use them.

Write in markdown, in these sections:

1. WHAT HAPPENED — the day's substantive developments, most consequential
   first. Facts, numbers, named entities. No more than 8 bullets.
2. WHAT IT MEANS — your reading. Connect items where they connect. This is
   the section that justifies the brief existing; be willing to draw a
   conclusion rather than listing considerations.
3. WHERE SOURCES DISAGREE — any place today's material contradicts itself,
   naming both sources and their weights, and which you find more credible
   and why. If there is no genuine contradiction, write "No material
   contradictions today" and stop — do not invent tension for symmetry.
{hold_task}{'5' if hold_task else '4'}. WHAT TO WATCH — specific, checkable things in the next few days.

Rules: cite sources inline as [Source]. Distinguish what a source REPORTED
from what you INFER. If the day's material is thin, say so plainly rather
than padding — a short honest brief beats a long hollow one.
{hold_txt}

ARTICLES:
{''.join(lines)}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--model", default="claude-sonnet-5")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--dry-run", action="store_true",
                    help="build the prompt and report on it; call nothing")
    ap.add_argument("--holdings", default=str(HOLDINGS),
                    help="CSV of current positions (optional)")
    args = ap.parse_args()

    articles = fetch_articles(args.date, args.limit)
    if not articles:
        print(f"No finance articles indexed on {args.date}. Nothing to do.",
              file=sys.stderr)
        return 0

    weights = load_weights()
    holdings = load_holdings(Path(args.holdings))
    prompt = build_prompt(articles, weights, holdings, args.date)

    srcs = sorted({a["source"] for a in articles})
    unweighted = [s for s in srcs if s not in weights]
    st = getattr(build_prompt, "stats", {})
    src = ("portfolio.db" if PORTFOLIO_DB.exists() else str(args.holdings))
    print(f"date            : {args.date}", file=sys.stderr)
    print(f"articles        : {len(articles)} from {len(srcs)} sources",
          file=sys.stderr)
    print(f"holdings        : {len(holdings) or 'none'} "
          f"({src if holdings else 'no source'})", file=sys.stderr)
    print(f"holdings-tagged : {st.get('held_articles', 0)} articles mention a "
          f"position", file=sys.stderr)
    print(f"prompt          : {len(prompt):,} chars "
          f"({st.get('included', 0)} articles in, "
          f"{st.get('dropped', 0)} over budget)", file=sys.stderr)
    if unweighted:
        print(f"unweighted srcs : {len(unweighted)} defaulting to "
              f"{DEFAULT_WEIGHT} -> {', '.join(unweighted[:6])}"
              f"{'...' if len(unweighted) > 6 else ''}", file=sys.stderr)

    if args.dry_run:
        print("\nDRY RUN -- prompt built, Claude not called.", file=sys.stderr)
        return 0

    print("calling claude...", file=sys.stderr)
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", args.model],
                           capture_output=True, text=True, timeout=args.timeout)
    except FileNotFoundError:
        raise SystemExit("ERROR: `claude` CLI not on PATH.")
    except subprocess.TimeoutExpired:
        raise SystemExit(f"ERROR: claude timed out after {args.timeout}s.")
    if r.returncode != 0:
        raise SystemExit(f"ERROR: claude exited {r.returncode}\n{r.stderr[:600]}")

    body = (r.stdout or "").strip()
    if not body:
        raise SystemExit("ERROR: claude returned nothing.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"finance-brief-{args.date}.md"
    header = (f"# Financial Brief — {args.date}\n\n"
              f"*Synthesized from {len(articles)} articles across {len(srcs)} "
              f"sources, weighted by source reliability. "
              f"{'Holdings-ranked.' if holdings else 'No holdings supplied.'}*\n\n"
              f"---\n\n")
    out.write_text(header + body + "\n", encoding="utf-8")
    print(f"\n✓ wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
