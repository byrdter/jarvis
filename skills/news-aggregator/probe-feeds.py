#!/usr/bin/env python3
"""Probe candidate feeds and emit a verified config for aggregate.py.

Why this exists: a feed list is only trustworthy on the day it was measured.
Vendor pages and listicles lie -- they list feeds that 404, feeds that return
headlines only, and feeds that were retired years ago. This script fetches
every candidate live and records what actually came back.

The measurement that matters is MEDIAN BODY CHARACTERS PER ITEM, not whether
the URL returns 200. A headline-only feed is a perfectly healthy 200 and is
almost useless to an analysis system: a headline cannot be summarized,
cross-referenced, or embedded into anything.

Outputs (written next to this script's --out path):
  <out>.json  -- {name: url} for feeds at/above --min-tier, ready for aggregate.py
  <out>.csv   -- full measurements for every candidate, including failures

Usage:
  ./venv/bin/python probe-feeds.py --out config/finance-feeds
  ./venv/bin/python probe-feeds.py --out config/finance-feeds --min-tier partial
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

try:
    import trafilatura
except ImportError:
    print("ERROR: trafilatura missing. Run: pip install -r requirements.txt",
          file=sys.stderr)
    raise SystemExit(1)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# Tier thresholds, in extracted body characters per item (median).
FULL_MIN = 1500      # whole article is in the feed; ingest as-is
PARTIAL_MIN = 400    # meaningful extract; enough to triage
TIER_ORDER = {"full": 3, "partial": 2, "headline": 1, "dead": 0}

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


# --------------------------------------------------------------------------
# Candidates. Grouped by what they are FOR, because the tiers get used
# differently downstream: full-text sources are read, headline sources are a
# radar that decides what to go read elsewhere.
# --------------------------------------------------------------------------
CANDIDATES: list[tuple[str, str, str]] = [
    # ---- Named mainstream financial press ----------------------------------
    ("press", "Fortune", "https://fortune.com/feed/fortune-feeds/?id=3230629"),
    ("press", "Forbes Business", "https://www.forbes.com/business/feed/"),
    ("press", "CNBC Top News", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"),
    ("press", "CNBC Markets", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"),
    ("press", "CNBC Finance", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"),
    ("press", "Financial Times Home", "https://www.ft.com/rss/home"),
    ("press", "Financial Times Companies", "https://www.ft.com/companies?format=rss"),
    ("press", "Business Insider Markets", "https://markets.businessinsider.com/rss/news"),
    ("press", "Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("press", "Reuters Business (via Google News)", "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com%2Fbusiness&hl=en-US&gl=US&ceid=US:en"),
    ("press", "AP Business (via Google News)", "https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com%2Fbusiness&hl=en-US&gl=US&ceid=US:en"),
    ("press", "Quartz", "https://qz.com/rss"),
    ("press", "Axios Business", "https://api.axios.com/feed/business"),
    ("press", "Axios Markets", "https://api.axios.com/feed/markets"),

    # ---- Headline radar (body text paywalled; the LINK is the product) -----
    ("radar", "WSJ Markets", "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain"),
    ("radar", "WSJ US Business", "https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness"),
    ("radar", "WSJ Technology", "https://feeds.content.dowjones.io/public/rss/RSSWSJD"),
    ("radar", "WSJ World News", "https://feeds.content.dowjones.io/public/rss/RSSWorldNews"),
    ("radar", "WSJ Opinion", "https://feeds.content.dowjones.io/public/rss/RSSOpinion"),
    ("radar", "MarketWatch Top Stories", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("radar", "MarketWatch Real-time Headlines", "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"),
    ("radar", "MarketWatch Market Pulse", "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"),
    ("radar", "Bloomberg Markets", "https://feeds.bloomberg.com/markets/news.rss"),
    ("radar", "Bloomberg Economics", "https://feeds.bloomberg.com/economics/news.rss"),
    ("radar", "Bloomberg Technology", "https://feeds.bloomberg.com/technology/news.rss"),
    ("radar", "Bloomberg Politics", "https://feeds.bloomberg.com/politics/news.rss"),
    ("radar", "The Economist Finance", "https://www.economist.com/finance-and-economics/rss.xml"),
    ("radar", "The Economist Business", "https://www.economist.com/business/rss.xml"),
    ("radar", "The Economist Latest", "https://www.economist.com/latest/rss.xml"),
    # Historic Barron's paths, kept in so the probe re-confirms they are gone.
    ("radar", "Barron's Real-time", "https://feeds.content.dowjones.io/public/rss/RSSBarronsRealTime"),
    ("radar", "Barron's Most Recent", "https://www.barrons.com/xml/rss/3_7510.xml"),

    # ---- Government + central bank: structured, free, highest signal -------
    ("official", "NY Fed Liberty Street Economics", "https://libertystreeteconomics.newyorkfed.org/feed/"),
    ("official", "Federal Reserve Press: All", "https://www.federalreserve.gov/feeds/press_all.xml"),
    ("official", "Federal Reserve Press: Monetary Policy", "https://www.federalreserve.gov/feeds/press_monetary.xml"),
    ("official", "Federal Reserve Working Papers (FEDS)", "https://www.federalreserve.gov/feeds/feds.xml"),
    ("official", "FRED Announcements", "https://news.research.stlouisfed.org/feed/"),
    ("official", "St. Louis Fed On The Economy", "https://www.stlouisfed.org/on-the-economy/rss"),
    ("official", "BEA News", "https://apps.bea.gov/rss/rss.xml"),
    ("official", "BLS News Releases", "https://www.bls.gov/feed/bls_latest.rss"),
    ("official", "Treasury Press Releases", "https://home.treasury.gov/system/files/126/press_releases.xml"),
    ("official", "SEC Press Releases", "https://www.sec.gov/news/pressreleases.rss"),
    ("official", "SEC Litigation Releases", "https://www.sec.gov/rss/litigation/litreleases.xml"),
    ("official", "CBO Publications", "https://www.cbo.gov/publications/all/rss.xml"),
    ("official", "EIA Today in Energy", "https://www.eia.gov/rss/todayinenergy.xml"),
    ("official", "NBER Working Papers", "https://back.nber.org/rss/new.xml"),
    ("official", "IMF Blog", "https://www.imf.org/en/Blogs/rss"),
    ("official", "BIS Research", "https://www.bis.org/doclist/research.rss"),
    ("official", "ECB Press", "https://www.ecb.europa.eu/rss/press.html"),

    # ---- Independent research: reputation model = open full text ----------
    ("research", "Aswath Damodaran", "https://aswathdamodaran.blogspot.com/feeds/posts/default?alt=rss"),
    ("research", "Noahpinion", "https://www.noahpinion.blog/feed"),
    ("research", "Apricitas Economics", "https://www.apricitas.io/feed"),
    ("research", "QuantSeeker", "https://quantseeker.substack.com/feed"),
    ("research", "Alpha Architect", "https://alphaarchitect.com/feed/"),
    ("research", "Of Dollars and Data", "https://ofdollarsanddata.com/feed/"),
    ("research", "Verdad Research", "https://verdadcap.com/archive?format=rss"),
    ("research", "The Big Picture (Ritholtz)", "https://ritholtz.com/feed/"),
    ("research", "Net Interest (Rubinstein)", "https://www.netinterest.co/feed"),
    ("research", "Doomberg", "https://doomberg.substack.com/feed"),
    ("research", "Calculated Risk", "https://www.calculatedriskblog.com/feeds/posts/default?alt=rss"),
    ("research", "Klement on Investing", "https://klementoninvesting.substack.com/feed"),
    ("research", "Abnormal Returns", "https://abnormalreturns.com/feed/"),
    ("research", "Quantocracy", "https://quantocracy.com/feed/"),
    ("research", "Marginal Revolution", "https://marginalrevolution.com/feed"),
    ("research", "Money Stuff / Matt Levine (Bloomberg)", "https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine.rss"),
    ("research", "A Wealth of Common Sense", "https://awealthofcommonsense.com/feed/"),
    ("research", "The Irrelevant Investor", "https://theirrelevantinvestor.com/feed/"),
    ("research", "Mr. Money Mustache", "https://www.mrmoneymustache.com/feed/"),
    ("research", "Farnam Street", "https://fs.blog/feed/"),
    ("research", "Zero Hedge", "https://feeds.feedburner.com/zerohedge/feed"),
    ("research", "Motley Fool", "https://www.fool.com/a/feeds/foolwatch"),
    ("research", "Seeking Alpha Market Currents", "https://seekingalpha.com/market_currents.xml"),
    ("research", "Morningstar", "https://www.morningstar.com/rss/news"),
    ("research", "CFA Institute Enterprising Investor", "https://blogs.cfainstitute.org/investor/feed/"),
    ("research", "Econbrowser", "https://econbrowser.com/feed"),
    ("research", "Conversable Economist", "https://conversableeconomist.com/feed/"),
    ("research", "The Sounding Line", "https://thesoundingline.com/feed"),
    ("research", "Pragmatic Capitalism", "https://www.pragcap.com/feed/"),

    # ---- Asset-class specific ---------------------------------------------
    ("sector", "OilPrice.com", "https://oilprice.com/rss/main"),
    ("sector", "Kitco Commodities", "https://www.kitco.com/rss/KitcoNews.xml"),
    ("sector", "CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("sector", "Bank Underground (BoE)", "https://bankunderground.co.uk/feed/"),
    ("sector", "Housing Wire", "https://www.housingwire.com/feed/"),
    ("sector", "ETF.com", "https://www.etf.com/rss.xml"),
    ("sector", "ETF Trends", "https://www.etftrends.com/feed/"),
]

# JSON/REST endpoints -- probed for reachability only, since "median body
# chars" is meaningless for a structured API. These are the layer that
# differentiates an analysis system from a news reader.
API_CANDIDATES: list[tuple[str, str, str]] = [
    ("SEC EDGAR full-text search",
     "https://efts.sec.gov/LATEST/search-index?q=%22artificial+intelligence%22&dateRange=custom",
     "https://efts.sec.gov/LATEST/search-index?q=test"),
    ("SEC EDGAR submissions (AAPL)",
     "https://data.sec.gov/submissions/CIK0000320193.json", ""),
    ("SEC XBRL company facts (AAPL)",
     "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", ""),
    ("SEC EDGAR daily index",
     "https://www.sec.gov/Archives/edgar/daily-index/index.json", ""),
    ("Treasury FiscalData",
     "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[size]=1", ""),
    ("FRED series (needs free key)",
     "https://api.stlouisfed.org/fred/series?series_id=GDP", ""),
    ("BLS timeseries",
     "https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000", ""),
    ("Alpha Vantage news sentiment (needs key)",
     "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo", ""),
    ("Frankfurter FX rates",
     "https://api.frankfurter.app/latest?from=USD", ""),
]


def strip_html(s: str) -> str:
    """Extract readable text, preferring trafilatura, falling back to tag-strip."""
    if not s:
        return ""
    if "<" in s:
        try:
            t = trafilatura.extract(s, include_comments=False,
                                    include_tables=False, favor_recall=True)
            if t and len(t.strip()) > 120:
                return t.strip()
        except Exception:
            pass
        s = _TAG_RE.sub(" ", s)
    import html as _h
    return _WS_RE.sub(" ", _h.unescape(s)).strip()


def entry_body(e) -> str:
    """Longest available body field on a feedparser entry."""
    best = ""
    for c in (e.get("content") or []):
        v = strip_html(c.get("value", ""))
        if len(v) > len(best):
            best = v
    for k in ("summary", "description", "subtitle"):
        v = strip_html(e.get(k, "") or "")
        if len(v) > len(best):
            best = v
    return best


def probe_feed(cat: str, name: str, url: str, timeout: int = 25) -> dict:
    rec = {"category": cat, "name": name, "url": url, "status": "", "items": 0,
           "median_chars": 0, "max_chars": 0, "tier": "dead", "note": "",
           "article_chars": 0, "effective_tier": "dead", "_links": []}
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept": "*/*"},
                         timeout=timeout, allow_redirects=True)
        rec["status"] = str(r.status_code)
        if r.status_code >= 400:
            rec["note"] = f"HTTP {r.status_code}"
            return rec
        d = feedparser.parse(r.content)
        entries = d.entries or []
        rec["items"] = len(entries)
        if not entries:
            rec["note"] = "parsed, 0 entries"
            return rec
        lens = [len(entry_body(e)) for e in entries[:40]]
        lens = [n for n in lens if n >= 0]
        rec["median_chars"] = int(statistics.median(lens)) if lens else 0
        rec["max_chars"] = max(lens) if lens else 0
        m = rec["median_chars"]
        rec["tier"] = ("full" if m >= FULL_MIN
                       else "partial" if m >= PARTIAL_MIN
                       else "headline")
        rec["effective_tier"] = rec["tier"]
        rec["_links"] = [l for l in
                         (e.get("link") or "" for e in entries[:6])
                         if l.startswith("http")]
    except requests.exceptions.Timeout:
        rec["status"], rec["note"] = "timeout", f"no response in {timeout}s"
    except Exception as ex:
        rec["status"], rec["note"] = "error", f"{type(ex).__name__}: {ex}"[:140]
    return rec


def deep_probe(rec: dict, sample: int = 3, timeout: int = 25) -> dict:
    """Second stage: fetch the ARTICLE PAGE behind a feed item and extract it.

    The feed tier alone is misleading. Forbes and CNBC publish headline-only
    RSS but serve a fully extractable article page, so a config filtered on
    feed body length drops them even though aggregate.py's fetch_fulltext()
    would have recovered the text. Conversely WSJ and the Economist are
    headline-only in BOTH places -- feed and page -- which is the real reason
    they can only ever be a radar.

    This mirrors aggregate.py's fetch_fulltext() exactly (Chrome UA, then
    trafilatura.extract with url= and favor_recall=True) so the number here
    predicts what the aggregator will actually store.
    """
    links = rec.get("_links") or []
    if not links:
        return rec
    got: list[int] = []
    for link in links[:sample]:
        try:
            r = requests.get(link, headers={"User-Agent": UA},
                             timeout=timeout, allow_redirects=True)
            if r.status_code >= 400 or not r.text:
                got.append(0)
                continue
            t = trafilatura.extract(r.text, url=link, include_comments=False,
                                    include_tables=False, favor_recall=True)
            got.append(len((t or "").strip()))
        except Exception:
            got.append(0)
    if not got:
        return rec
    a = int(statistics.median(got))
    rec["article_chars"] = a
    art_tier = ("full" if a >= FULL_MIN
                else "partial" if a >= PARTIAL_MIN
                else "headline")
    # The aggregator keeps whichever path yields more text, so the effective
    # tier is the better of the two -- never the feed tier alone.
    if TIER_ORDER[art_tier] > TIER_ORDER[rec["effective_tier"]]:
        rec["effective_tier"] = art_tier
        rec["note"] = (rec["note"] + "; " if rec["note"] else "") + \
                      f"article fetch recovers {a:,} ch"
    return rec


def probe_api(name: str, url: str, _alt: str, timeout: int = 25) -> dict:
    rec = {"category": "api", "name": name, "url": url, "status": "",
           "items": 0, "median_chars": 0, "max_chars": 0, "tier": "api",
           "note": "", "article_chars": 0, "effective_tier": "api",
           "_links": []}
    try:
        r = requests.get(url, headers={"User-Agent": UA,
                                       "Accept": "application/json"},
                         timeout=timeout, allow_redirects=True)
        rec["status"] = str(r.status_code)
        rec["max_chars"] = len(r.content)
        body = r.text[:400].replace("\n", " ")
        if r.status_code >= 400:
            rec["tier"] = "dead"
            rec["note"] = f"HTTP {r.status_code}: {body[:90]}"
        elif "api_key" in body.lower() or "apikey" in body.lower():
            rec["note"] = "reachable; needs free key"
        else:
            rec["note"] = f"{len(r.content):,} bytes"
    except Exception as ex:
        rec["status"], rec["tier"] = "error", "dead"
        rec["note"] = f"{type(ex).__name__}: {ex}"[:140]
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="config/finance-feeds",
                    help="output path stem; writes .json and .csv")
    ap.add_argument("--min-tier", default="partial",
                    choices=["full", "partial", "headline"],
                    help="lowest tier written into the .json config")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--deep", action=argparse.BooleanOptionalAction, default=True,
                    help="second stage: fetch article pages behind sub-full "
                         "feeds to see what fetch_fulltext() would recover")
    ap.add_argument("--deep-sample", type=int, default=3,
                    help="articles sampled per feed in the second stage")
    args = ap.parse_args()

    floor = TIER_ORDER[args.min_tier]
    results: list[dict] = []

    print(f"Probing {len(CANDIDATES)} feeds + {len(API_CANDIDATES)} APIs "
          f"({args.workers} workers)...", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(probe_feed, c, n, u, args.timeout)
                for c, n, u in CANDIDATES]
        futs += [ex.submit(probe_api, n, u, a, args.timeout)
                 for n, u, a in API_CANDIDATES]
        for i, f in enumerate(as_completed(futs), 1):
            rec = f.result()
            results.append(rec)
            mark = {"full": "FULL", "partial": "PART", "headline": "HEAD",
                    "api": "API ", "dead": "----"}[rec["tier"]]
            print(f"  [{i:>3}/{len(futs)}] {mark} {rec['median_chars']:>6} "
                  f"{rec['name'][:44]:<44} {rec['note'][:40]}", file=sys.stderr)

    # Stage 2. Only feeds that are not already full-text need it: if the whole
    # article is in the feed there is nothing an article fetch can add, and
    # skipping them avoids pointless traffic to the sources most worth being
    # polite to.
    if args.deep:
        need = [r for r in results
                if r["category"] != "api" and r["tier"] in ("headline", "partial")
                and r["_links"]]
        print(f"\nStage 2: fetching articles behind {len(need)} sub-full feeds "
              f"({args.deep_sample} each)...", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(deep_probe, r, args.deep_sample, args.timeout): r
                    for r in need}
            for i, f in enumerate(as_completed(futs), 1):
                r = f.result()
                if r["effective_tier"] != r["tier"]:
                    print(f"  [{i:>3}/{len(need)}] {r['tier']}->"
                          f"{r['effective_tier']:<8} {r['article_chars']:>6} ch  "
                          f"{r['name'][:44]}", file=sys.stderr)

    order = {"press": 0, "radar": 1, "official": 2, "research": 3,
             "sector": 4, "api": 5}
    results.sort(key=lambda r: (order.get(r["category"], 9),
                                -TIER_ORDER.get(r["effective_tier"], 0),
                                -max(r["median_chars"], r["article_chars"])))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    csv_path = out.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["category", "name", "effective_tier",
                                           "tier", "median_chars",
                                           "article_chars", "max_chars",
                                           "items", "status", "note", "url"])
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in w.fieldnames})

    # aggregate.py consumes a flat {name: url} dict -- match rss-feeds.json
    # exactly so it runs against this config with no code change. Filter on
    # effective_tier, not tier: a headline-only feed whose article pages
    # extract cleanly (Forbes, CNBC) is a full-text source to the aggregator.
    cfg = {r["name"]: r["url"] for r in results
           if r["category"] != "api"
           and TIER_ORDER.get(r["effective_tier"], 0) >= floor}
    json_path = out.with_suffix(".json")
    json_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    live = [r for r in results if r["category"] != "api"]
    by = lambda t: sum(1 for r in live if r["effective_tier"] == t)  # noqa: E731
    promoted = sum(1 for r in live if r["effective_tier"] != r["tier"])
    apis_ok = sum(1 for r in results
                  if r["category"] == "api" and r["tier"] != "dead")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\n  measured {stamp}", file=sys.stderr)
    print(f"  full {by('full')}  partial {by('partial')}  "
          f"headline {by('headline')}  dead {by('dead')}  "
          f"| APIs reachable {apis_ok}/{len(API_CANDIDATES)}", file=sys.stderr)
    if args.deep:
        print(f"  {promoted} feeds promoted a tier by the article fetch",
              file=sys.stderr)
    print(f"  wrote {json_path} ({len(cfg)} feeds at tier >= {args.min_tier})",
          file=sys.stderr)
    print(f"  wrote {csv_path} ({len(results)} rows, incl. failures)",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
