#!/usr/bin/env python3
"""
archival-search.py — find REAL material for a beat, with its RIGHTS TIER attached.

WHY THIS EXISTS
Three full shot censuses (2026-08-12, `reports/explorist-nvidia-teardown/`) found the same
thing three times: across a 7.48x outlier and a below-median flop, **material mix is a
constant (84-90% real material) and cutting rhythm is the variable**. The winners run
7.3-24.8 distinct shots per minute. A 26-minute video at 7.3/min needs ~190 distinct
sources; at Explorist's rate, ~280.

Our own stills test scene ran SIX sources per minute. The gating capability is not graphics
and not editing software — it is **finding enough real material, fast, and knowing whether
we may use it**. That is this tool.

TWO RULES BAKED IN, BOTH LEARNED THE EXPENSIVE WAY
  1. **Titles, never bare counts.** Commons reports 54,014 files for "Intel" and 4,072 for
     "Andy Grove" — but the top video hits for those queries were *Rep. Rick Nolan* and
     *Sugar Grove, West Virginia*. A count is not evidence; a count with the drift unread is
     worse than no number. Every row here carries a title and a URL for human judgement.
  2. **Rights tier travels with the row.** Free-to-FIND and free-to-USE are different things
     and conflating them is how a channel ends up with a $19,200 licensing bill or a
     Content ID claim. AP Archive is searchable for nothing and licenses at ~$40/second.

TIERS
  GREEN  free to use. Public domain, CC0, or CC-BY/BY-SA (attribution — and SHARE-ALIKE is
         flagged, because its effect on a monetised video is unresolved and is a question
         for counsel, not for this script).
  AMBER  free to FIND, copyrighted, fair-use dependent. Institutional archives with
         unconfirmed terms, broadcast news, social video, Wayback captures.
  RED    licensed and priced. Findable here so you know it exists and can decide; never
         assume it is affordable.

    python3 archival-search.py "intel foundry losses"
    python3 archival-search.py "data center protest" --sources localnews,ia,commons
    python3 archival-search.py "dropbox 2008" --wayback dropbox.com --era 2008-2010
    python3 archival-search.py "nvidia gpu" --json --ledger assets-considered.jsonl

Needs YOUTUBE_API_KEY in env or jarvis/.env for the youtube-backed providers; every other
provider is keyless. Providers fail independently — a dead one prints a warning to stderr,
not a stack trace, and the rest still return.

WAYBACK RATE-LIMITS HARD. archive.org/wayback/available returns 429 after a handful of
calls and the cooldown runs minutes, not seconds. The provider retries with backoff and
then RAISES rather than returning [], so a throttle can never be misread as "no snapshots
exist". Keep --era narrow (2-3 years) and expect to wait between runs.
"""
import argparse, concurrent.futures as cf, html, json, os, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "jarvis-video-research/1.0 (byrdter@auburn.edu)"}
G, A_, R, DIM, BOLD, Z = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"
TIER_COLOUR = {"GREEN": G, "AMBER": A_, "RED": R}

# YouTube channels worth scoping to, with the tier that applies to their material.
CHANNELS = {
    "chm":       ("UCHDr4RtxwA1KqKGwxgdK4Vg", "Computer History Museum", "AMBER",
                  "reuse terms UNCONFIRMED — ask before building on it"),
    "aparchive": ("UCHTK-2W11Vh1V4uwofOfR4w", "AP Archive", "RED",
                  "licensed, billed in 15-sec increments. NOTE: AP states US content "
                  "published 1963 or earlier was never copyright-renewed — VERIFY per item"),
    "cspan":     ("UCb--64Gl51jIEVE-GLDAVTg", "C-SPAN", "AMBER",
                  "House/Senate FLOOR feed is public domain outright; C-SPAN's own coverage "
                  "is free NON-commercial w/ attribution, or $100 per program per year"),
    "nasa":      ("UCLA_DiR1FfKNvjuUpBHmylQ", "NASA", "GREEN",
                  "US government work — no copyright. No endorsement implication; "
                  "identifiable astronauts need care"),
}
# Local/broadcast news is where the winning video actually sourced its human presence:
# residents on porches, town halls, protest signs. Searched by keyword, not by channel.
NEWS_HINTS = ["news", "abc", "nbc", "cbs", "fox", "wusa", "wjla", "ktla", "wfaa",
              "eyewitness", "action news", "channel", "local", "bloomberg", "cnbc"]


def env_key(name):
    """Read a key from the environment, falling back to jarvis/.env.

    Takes the FIRST match, not the last. The repo .env defines CARTESIA_VOICE_ID four times
    and a normal dotenv loader silently keeps the last one — which is the wrong voice. Same
    trap applies to any key someone appends twice.
    """
    k = os.environ.get(name)
    if k:
        return k
    p = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
    if os.path.exists(p):
        for line in open(p):
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def api_key():
    return env_key("YOUTUBE_API_KEY")


def get(url, timeout=45):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                            timeout=timeout))


def clean(s, n=88):
    s = re.sub(r"<[^>]+>", "", html.unescape(str(s or ""))).strip()
    return (s[:n - 1] + "…") if len(s) > n else s


def row(src, tier, date, title, url, note=""):
    return dict(source=src, tier=tier, date=(date or "")[:10], title=clean(title),
                url=url, note=note)


# ----------------------------------------------------------------- providers
def p_commons(q, limit, era):
    """Wikimedia Commons. Free to use — but the LICENCE varies per file, so report it."""
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        dict(action="query", generator="search", gsrsearch=q, gsrnamespace=6,
             gsrlimit=limit, prop="imageinfo", iiprop="url|extmetadata",
             iiurlwidth=1280, format="json"))
    pages = get(u).get("query", {}).get("pages", {})
    out = []
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        lic = clean(em.get("LicenseShortName", {}).get("value", "unknown"), 30)
        art = clean(em.get("Artist", {}).get("value", ""), 40)
        note = f"{lic} · {art}" if art else lic
        if "share" in lic.lower() or "sa" in lic.lower().split("-"):
            note += "  [SHARE-ALIKE → counsel]"
        out.append(row("commons", "GREEN", em.get("DateTimeOriginal", {}).get("value", ""),
                       pg.get("title", "")[5:], ii.get("descriptionurl") or ii.get("url"), note))
    return out


def p_ia(q, limit, era):
    """Internet Archive. GREEN only when a licence says so; otherwise AMBER."""
    qq = f'({q}) AND mediatype:(movies)'
    if era:
        qq += f" AND date:[{era[0]}-01-01 TO {era[1]}-12-31]"
    u = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": qq, "fl[]": ["identifier", "title", "date", "licenseurl", "collection"],
         "rows": limit, "output": "json"}, doseq=True)
    out = []
    for d in get(u)["response"]["docs"]:
        lic = d.get("licenseurl") or ""
        coll = d.get("collection") or []
        coll = coll if isinstance(coll, list) else [coll]
        pd = "prelinger" in " ".join(coll).lower()
        tier = "GREEN" if (lic or pd) else "AMBER"
        note = ("prelinger (public domain)" if pd else
                (lic.split("/licenses/")[-1].strip("/") if lic else "no licence stated"))
        if "tvarchive" in " ".join(coll).lower():
            tier, note = "AMBER", "TV News Archive — research access, not a licence"
        out.append(row("archive.org", tier, d.get("date", ""), d.get("title", ""),
                       f"https://archive.org/details/{d['identifier']}", note))
    return out


def p_edgar(q, limit, era):
    """SEC EDGAR full-text. Filings are public records — capture them directly."""
    params = {"q": f'"{q}"'}
    if era:
        params.update(dateRange="custom", startdt=f"{era[0]}-01-01", enddt=f"{era[1]}-12-31")
    u = "https://efts.sec.gov/LATEST/search-index?" + urllib.parse.urlencode(params)
    hits = get(u).get("hits", {}).get("hits", [])[:limit]
    out = []
    for h in hits:
        s = h.get("_source", {})
        acc, doc = h.get("_id", ":").split(":", 1)
        cik = (s.get("ciks") or [""])[0].lstrip("0")
        url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/"
               f"{acc.replace('-', '')}/{doc}") if cik else "https://www.sec.gov/edgar"
        name = (s.get("display_names") or [""])[0]
        out.append(row("sec-edgar", "GREEN", s.get("file_date", ""),
                       f"{name} — {s.get('file_type','')}", url, "public filing"))
    return out


def p_nasa(q, limit, era):
    """NASA Image and Video Library — 140,000+ assets, US gov work, no copyright.

    Under-used by business/tech channels: for anything touching space, launch,
    engineering-at-scale or big-infrastructure imagery it is 4K, free and claim-proof.
    """
    params = {"q": q, "media_type": "video,image", "page_size": limit}
    if era:
        params.update(year_start=era[0], year_end=era[1])
    u = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode(params)
    out = []
    for it in get(u).get("collection", {}).get("items", [])[:limit]:
        d = (it.get("data") or [{}])[0]
        nid = d.get("nasa_id", "")
        out.append(row("nasa", "GREEN", d.get("date_created", ""), d.get("title", ""),
                       f"https://images.nasa.gov/details/{urllib.parse.quote(nid)}",
                       f"{d.get('media_type','')} · public domain, no endorsement implication"))
    return out


# Corporate press rooms publish broadcast-quality b-roll of their OWN products, fabs and
# executives, free, explicitly for media use. No stock library has the inside of Tesla's
# factory; Tesla's press site does. There is no common API — this is a curated registry
# that hands you the right door.
PRESSROOMS = {
    # EVERY URL BELOW WAS FETCHED AND CONFIRMED 2026-08-12. The first draft of this
    # registry was written from memory and SIX of fifteen were 404 — including a Tesla
    # path that did not exist. A plausible URL is not a verified one.
    "nvidia":    ("https://nvidianews.nvidia.com/multimedia/search", ""),
    "apple":     ("https://www.apple.com/newsroom/", ""),
    "intel":     ("https://newsroom.intel.com/", ""),
    "microsoft": ("https://news.microsoft.com/", ""),
    "google":    ("https://blog.google/press/", ""),
    "alphabet":  ("https://blog.google/press/", ""),
    "amazon":    ("https://press.aboutamazon.com/", ""),
    "meta":      ("https://about.fb.com/news/", ""),
    "ibm":       ("https://newsroom.ibm.com/", ""),
    "samsung":   ("https://news.samsung.com/global/", ""),
    "amd":       ("https://www.amd.com/en/newsroom.html", ""),
    "boeing":    ("https://www.boeing.com/company/", ""),
    "openai":    ("https://openai.com/news/", ""),
    "tesla":     ("https://www.tesla.com/tesla-gallery",
                  "media use only; every asset must carry 'Courtesy of Tesla, Inc.'"),
    "tsmc":      ("https://pr.tsmc.com/english",
                  "UNVERIFIED — Cloudflare blocks automated checks; confirm by hand"),
}


def p_press(q, limit, era):
    """Match company names in the query to their press/media library."""
    ql = q.lower()
    out = []
    for name, (url, extra) in PRESSROOMS.items():
        if name in ql:
            note = ("free, broadcast-quality, PRESS/EDITORIAL use — safe inside commentary "
                    "about that company; never implies endorsement")
            out.append(row("press-room", "AMBER", "", f"{name.title()} media library", url,
                           note + ("  · " + extra if extra else "")))
    return out


def _yt(params, key):
    u = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(
        dict(part="snippet", type="video", key=key, **params))
    return get(u).get("items", [])


def p_archives(q, limit, era, key=None):
    """Institutional archive channels. Findable free; REUSE TERMS ARE NOT ESTABLISHED."""
    if not key:
        raise RuntimeError("no YOUTUBE_API_KEY")
    out = []
    # era MUST reach this provider too. Without it a 2024 beat returned 2015 AP rows,
    # which looks like coverage and is not.
    window = {}
    if era:
        window = dict(publishedAfter=f"{era[0]}-01-01T00:00:00Z",
                      publishedBefore=f"{era[1]}-12-31T23:59:59Z")
    for _, (cid, name, tier, note) in CHANNELS.items():
        for it in _yt(dict(channelId=cid, q=q, maxResults=max(2, limit // 2), **window), key):
            sn = it["snippet"]
            out.append(row(name, tier, sn["publishedAt"], sn["title"],
                           "https://youtu.be/" + it["id"]["videoId"], note))
    return out


def p_localnews(q, limit, era, key=None):
    """Local/broadcast news — where the winning video got its human presence.

    Residents on porches, town halls, protest signs. Fair-use dependent, always.
    """
    if not key:
        raise RuntimeError("no YOUTUBE_API_KEY")
    params = dict(q=f"{q} news", maxResults=limit, order="relevance")
    if era:
        params.update(publishedAfter=f"{era[0]}-01-01T00:00:00Z",
                      publishedBefore=f"{era[1]}-12-31T23:59:59Z")
    out = []
    for it in _yt(params, key):
        sn = it["snippet"]
        ch = sn["channelTitle"]
        looks_news = any(h in ch.lower() for h in NEWS_HINTS)
        out.append(row(f"yt:{clean(ch,22)}", "AMBER", sn["publishedAt"], sn["title"],
                       "https://youtu.be/" + it["id"]["videoId"],
                       "broadcast news — fair use" if looks_news else "not obviously a news outlet"))
    return out


def p_wayback(domain, era):
    """Period-correct web pages — the browser-chrome register, for free.

    NOTE the retry/backoff and the RAISE at the end. An earlier version swallowed every
    exception and returned []. The Wayback API rate-limits at 429 under a tight loop, so
    the tool reported "no snapshots" when it meant "I was throttled" — a silent zero that
    reads as evidence of absence. Same failure class as the bogus "0 of 24 beats have free
    video" result on 2026-08-12. A provider that fails must SAY so.
    """
    import time
    out, errs = [], []
    years = list(range(int(era[0]), int(era[1]) + 1)) if era else [2008, 2012, 2016, 2020, 2024]
    for i, y in enumerate(years):
        for attempt in range(3):
            try:
                r = get(f"https://archive.org/wayback/available?url="
                        f"{urllib.parse.quote(domain)}&timestamp={y}0601")
                snap = (r.get("archived_snapshots") or {}).get("closest")
                if snap and snap.get("available"):
                    out.append(row("wayback", "AMBER", snap["timestamp"][:8],
                                   f"{domain} as archived {snap['timestamp'][:4]}", snap["url"],
                                   "capture of a third-party page — fair use"))
                errs = []
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    time.sleep(1.5 * (attempt + 1)); continue
                errs.append(f"{y}:{str(e)[:24]}"); break
        time.sleep(0.4)
    if errs and not out:
        raise RuntimeError("wayback failed for every year (" + "; ".join(errs[:3]) +
                           ") — this is NOT 'no snapshots exist'")
    return out


def p_pexels(q, limit, era=None):     # era is ignored: stock has no meaningful period filter
    """Pexels — free stock STILLS AND VIDEO, licensed for commercial use.

    Worth a provider of its own because it fills the exact hole the CC pools leave: modern,
    high-resolution, people-present interiors. Commons and Openverse are strong on monuments,
    documents and historical images and weak on "someone browsing a shop", which is most of
    what a business explainer actually needs on screen.

    TIER IS GREEN, WITH TWO CONDITIONS THAT ARE NOT CC CONDITIONS. The Pexels License allows
    free commercial use and does not require attribution — but it forbids selling unaltered
    copies, and it forbids depicting identifiable people in a way that is offensive or that
    implies endorsement. That second one binds us: a stock face used under a line about people
    being cheated is an implied claim about that person. Credit the photographer anyway; it
    costs a line and it is what the ATTRIBUTION ledger is for.
    """
    key = env_key("PEXELS_API_KEY")
    if not key:
        raise RuntimeError("PEXELS_API_KEY not set (env or jarvis/.env) — add it once; "
                           "a duplicated line is read as the first occurrence here")
    hdr = {"Authorization": key, "User-Agent": UA.get("User-Agent", "jarvis")}
    out = []
    for kind, url, pick in (
        ("still", "https://api.pexels.com/v1/search?per_page=%d&query=%s",
         lambda m: (m["url"], m.get("alt") or "untitled", m.get("photographer", ""))),
        ("video", "https://api.pexels.com/videos/search?per_page=%d&query=%s",
         lambda m: (m["url"], (m.get("alt") or "").strip() or f"video {m.get('duration','?')}s",
                    (m.get("user") or {}).get("name", ""))),
    ):
        try:
            req = urllib.request.Request(url % (limit, urllib.parse.quote(q)), headers=hdr)
            data = json.load(urllib.request.urlopen(req, timeout=45))
        except Exception as e:
            print(f"  ! pexels {kind}: {e}", file=sys.stderr)
            continue
        for m in (data.get("photos") or data.get("videos") or []):
            page, title, who = pick(m)
            out.append(row("pexels/" + kind, "GREEN", "", title, page,
                           f"Pexels License · {who} · commercial use OK, no attribution "
                           f"required; NO unaltered resale; no endorsement implication"))
    return out


PROVIDERS = {"commons": p_commons, "ia": p_ia, "edgar": p_edgar, "nasa": p_nasa,
             "press": p_press, "archives": p_archives, "localnews": p_localnews,
             "pexels": p_pexels}


def spoken_word_handoffs(q):
    """Deep links to the tools that search WHAT WAS SAID, not titles and metadata.

    This tool matches on titles/descriptions. Finding "the moment Jensen Huang says X"
    is a different problem, and Filmot (1.7bn transcripts across 1.5bn YouTube videos)
    and YouGlish solve it. NEITHER EXPOSES A USABLE FREE API — every filmot.com endpoint
    302s — so these are honest handoffs, not results. Faking rows would be worse than
    linking out.
    """
    e = urllib.parse.quote(f'"{q}"')
    return [
        ("filmot   — exact spoken phrase across 1.5bn YouTube videos",
         f"https://filmot.com/search/{e}/1"),
        ("youglish — spoken phrase with in-context playback",
         f"https://youglish.com/search/{urllib.parse.quote(q)}/all"),
        ("yt CC    — Creative Commons filter (~4M CC-BY videos, remixable w/ attribution)",
         "https://www.youtube.com/results?search_query="
         + urllib.parse.quote(q) + "&sp=EgIwAQ%253D%253D"),
    ]


def main():
    ap = argparse.ArgumentParser(
        description="Find real material for a beat, with rights tier attached.")
    ap.add_argument("query")
    ap.add_argument("--sources", default="commons,ia,edgar,nasa,press,archives,localnews",
                    help="comma list: " + ",".join(PROVIDERS))
    ap.add_argument("--limit", type=int, default=6, help="rows per provider")
    ap.add_argument("--era", help="YYYY-YYYY, filters where the provider supports it")
    ap.add_argument("--wayback", metavar="DOMAIN",
                    help="also pull period snapshots of this domain")
    ap.add_argument("--tier", choices=["GREEN", "AMBER", "RED"],
                    help="only show this tier")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ledger", help="append every row to this JSONL (what we CONSIDERED)")
    a = ap.parse_args()

    era = None
    if a.era:
        m = re.match(r"(\d{4})-(\d{4})$", a.era)
        if not m:
            sys.exit("--era must be YYYY-YYYY")
        era = (m.group(1), m.group(2))

    key = api_key()
    want = [s.strip() for s in a.sources.split(",") if s.strip() in PROVIDERS]
    rows, warned = [], []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {}
        for name in want:
            fn = PROVIDERS[name]
            kw = dict(key=key) if name in ("archives", "localnews") else {}
            futs[ex.submit(fn, a.query, a.limit, era, **kw)] = name
        if a.wayback:
            futs[ex.submit(p_wayback, a.wayback, era)] = "wayback"
        for f in cf.as_completed(futs):
            n = futs[f]
            try:
                rows.extend(f.result())
            except Exception as e:
                warned.append(f"{n}: {str(e)[:70]}")

    if a.tier:
        rows = [r for r in rows if r["tier"] == a.tier]
    order = {"GREEN": 0, "AMBER": 1, "RED": 2}
    rows.sort(key=lambda r: (order[r["tier"]], r["source"], r["date"]))

    if a.json:
        print(json.dumps(rows, indent=1))
    else:
        print(f"\n  {BOLD}{a.query}{Z}" + (f"   era {a.era}" if a.era else ""))
        print(f"  {DIM}{len(rows)} candidates. Titles are here so you can judge relevance —"
              f" a count alone is not evidence.{Z}\n")
        for r in rows:
            c = TIER_COLOUR[r["tier"]]
            print(f"  {c}{r['tier']:<5}{Z} {DIM}{r['source'][:20]:<20} {r['date']:<10}{Z} "
                  f"{r['title']}")
            print(f"        {DIM}{r['url']}{Z}")
            if r["note"]:
                print(f"        {c}{r['note']}{Z}")
        print(f"  {DIM}── spoken-word search (this tool matches titles; these match WORDS)"
              f" ──{Z}")
        for lab, url in spoken_word_handoffs(a.query):
            print(f"  {DIM}handoff{Z} {lab}\n        {DIM}{url}{Z}")
        print()
        n = {t: sum(1 for r in rows if r["tier"] == t) for t in order}
        print(f"\n  {G}GREEN {n['GREEN']}{Z} free to use · {A_}AMBER {n['AMBER']}{Z} "
              f"fair-use dependent · {R}RED {n['RED']}{Z} licensed")
        print(f"  {DIM}GREEN still carries attribution duties; share-alike on a monetised"
              f" video is unresolved and is a question for counsel.{Z}")
    for w in warned:
        print(f"  {A_}warn{Z} {w}", file=sys.stderr)

    if a.ledger:
        with open(a.ledger, "a") as f:
            for r in rows:
                f.write(json.dumps(dict(r, query=a.query)) + "\n")
        print(f"  {DIM}-> appended {len(rows)} to {a.ledger}{Z}", file=sys.stderr)


if __name__ == "__main__":
    main()
