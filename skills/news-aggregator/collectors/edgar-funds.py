#!/usr/bin/env python3
"""
EDGAR fund-filing collector for JARVIS finance domain.

WHY THIS EXISTS
    The finance RSS pipeline knows what is being SAID about funds. This knows what
    funds actually FILED. Those are different capabilities and only the second one
    settles an argument on screen.

    N-PX   proxy voting records  -> proves an "index" fund makes discretionary choices
    NPORT-P monthly holdings     -> what you actually own when you buy the ticker
    485BPOS prospectus           -> fees, share classes, stated strategy
    N-CEN  annual fund census    -> structure, service providers, board

RATE LIMITS
    SEC allows 10 req/sec with a declared User-Agent carrying a real contact address.
    We run at 5/sec. A missing/!generic UA gets you blocked, not throttled.

STORAGE
    Writes into agent-sdk/data/ai-knowledge.db as type='documentation', domain='finance'.
    That table has a CHECK constraint on type, so 'documentation' is deliberate -- do not
    "fix" it to 'filing' without migrating the constraint first.
    Raw primary documents land in --out so a scene can screenshot the actual page.

USAGE
    edgar-funds.py registry
    edgar-funds.py filings --cik 0001100663 --form N-PX --limit 5 --store
    edgar-funds.py search "proxy voting" --forms N-PX --limit 20
    edgar-funds.py fetch --accession 0001104659-25-083826 --cik 0000102909
"""
import argparse, json, sqlite3, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

UA = "JARVIS-research/1.0 (byrdter@auburn.edu)"
KNOWLEDGE_DB = Path(__file__).resolve().parents[3] / "agent-sdk" / "data" / "ai-knowledge.db"
OUT_DEFAULT  = Path(__file__).resolve().parents[3] / "reports" / "finance-digests" / "filings"
DOMAIN = "finance"
_last = [0.0]

# Verified live 2026-08-24 against data.sec.gov/submissions/. Filing counts in comments
# are the 'recent' window (~1000 most recent), not lifetime.
REGISTRY = {
    "ishares":  ("0001100663", "iSHARES TRUST",            "1433 NPORT-P, 11 N-PX, 28 485BPOS"),
    "vanguard": ("0000102909", "VANGUARD GROUP INC",       "adviser entity -- N-PX lives here"),
    "spdr":     ("0000884394", "SPDR S&P 500 ETF TRUST",   "27 NPORT-P, 27 485BPOS"),
    "qqq":      ("0001067839", "INVESCO QQQ TRUST SERIES 1","27 NPORT-P, 29 485BPOS"),
}

def _get(url, as_json=True, timeout=30):
    """Rate-limited SEC fetch. 5 req/sec ceiling against their stated 10."""
    gap = time.time() - _last[0]
    if gap < 0.2: time.sleep(0.2 - gap)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Encoding": "gzip, deflate", "Host": urllib.parse.urlparse(url).netloc})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip; raw = gzip.decompress(raw)
    return json.loads(raw) if as_json else raw.decode("utf-8", "replace")

def submissions(cik):
    return _get(f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json")

def list_filings(cik, form=None, limit=20):
    d = submissions(cik)
    rec = d.get("filings", {}).get("recent", {})
    cols = ("accessionNumber","filingDate","reportDate","form","primaryDocument","primaryDocDescription")
    rows = list(zip(*[rec.get(c, []) for c in cols]))
    out = []
    for acc, fdate, rdate, frm, pdoc, pdesc in rows:
        if form and frm != form: continue
        c = str(int(cik))
        out.append(dict(cik=str(cik).zfill(10), company=d.get("name",""), accession=acc, form=frm,
                        filed=fdate, period=rdate, doc=pdoc, desc=pdesc,
                        url=f"https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace('-','')}/{pdoc}",
                        index_url=f"https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace('-','')}/{acc}-index.htm"))
        if len(out) >= limit: break
    return out

def fulltext(q, forms=None, limit=20, start=None, end=None, ciks=None):
    """EDGAR full-text search. Covers 2001-present. Returns scored hits with CIK + accession."""
    p = {"q": q, "from": 0, "size": min(limit, 100)}
    if forms: p["forms"] = ",".join(forms)
    if ciks: p["ciks"] = ",".join(str(c).zfill(10) for c in ciks)
    if start and end: p.update(dateRange="custom", startdt=start, enddt=end)
    d = _get("https://efts.sec.gov/LATEST/search-index?" + urllib.parse.urlencode(p))
    hits = d.get("hits", {}).get("hits", [])
    out = []
    for h in hits:
        s = h.get("_source", {}); ident = h.get("_id", "")
        acc = ident.split(":")[0]; doc = ident.split(":")[1] if ":" in ident else ""
        ciks = s.get("ciks", []) or [""]
        c = str(int(ciks[0])) if ciks[0] else ""
        out.append(dict(cik=ciks[0], company=(s.get("display_names") or [""])[0], accession=acc,
                        form=s.get("root_form") or s.get("file_type",""), filed=s.get("file_date",""),
                        period=s.get("period_ending",""), doc=doc, score=h.get("_score"),
                        url=f"https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace('-','')}/{doc}" if c and doc else "",
                        index_url=f"https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace('-','')}/{acc}-index.htm" if c else ""))
    return dict(total=d.get("hits",{}).get("total",{}).get("value",0), hits=out[:limit])

def classify(items):
    """Fetch each N-PX cover page and tag reportType + covered series.

    THE TRAP: most N-PX filings from a big fund family are 'FUND NOTICE REPORT' --
    bond//money-market series that cast no proxies. The votes live in the
    'FUND VOTING REPORT' variant, which is usually a SMALLER filing covering fewer
    series. Verified 2026-08-24: iShares 0001438934-25-002331 is a NOTICE covering
    157 bond ETFs; 0001438934-25-002330 is a VOTING REPORT covering 2 series, one of
    which is the iShares Core S&P 500 ETF. Filter on reportType or you will read the
    wrong document.
    """
    import re
    for it in items:
        c = str(int(it["cik"])); acc = it["accession"].replace("-", "")
        try:
            x = _get(f"https://www.sec.gov/Archives/edgar/data/{c}/{acc}/primary_doc.xml", as_json=False)
        except Exception as e:
            it["report_type"] = f"ERR {e}"; continue
        m = re.search(r"<reportType>([^<]*)", x)
        names = re.findall(r"<nameOfSeries>([^<]*)", x)
        it["report_type"] = (m.group(1) if m else "?")
        it["series_count"] = len(names)
        it["series_sample"] = [n.replace("&amp;", "&") for n in names[:5]]
    return items


def store(items, out_dir=None, fetch_docs=False):
    """Upsert into ai-knowledge.db. Dedupes on url. Returns (new, skipped)."""
    if not KNOWLEDGE_DB.exists():
        print(f"! knowledge db missing: {KNOWLEDGE_DB}", file=sys.stderr); return (0, 0)
    conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=15)
    have = {r[0] for r in conn.execute(
        "SELECT url FROM content_sources WHERE domain=? AND type='documentation'", (DOMAIN,)) if r[0]}
    now = datetime.now(timezone.utc).isoformat(); new = skip = 0
    for it in items:
        u = it.get("index_url") or it.get("url")
        if not u or u in have: skip += 1; continue
        path = None
        if fetch_docs and out_dir and it.get("url"):
            try:
                body = _get(it["url"], as_json=False)
                out_dir.mkdir(parents=True, exist_ok=True)
                path = out_dir / f"{it['accession']}_{it.get('form','?')}.txt"
                path.write_text(body, encoding="utf-8"); path = str(path)
            except Exception as e:
                print(f"  ! doc fetch failed {it['accession']}: {e}", file=sys.stderr)
        title = f"{it.get('form','?')} — {it.get('company','?')} — filed {it.get('filed','?')}"
        conn.execute(
            "INSERT INTO content_sources (type,title,url,author,published_date,content_path,"
            "indexed_at,last_updated,metadata,domain) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ("documentation", title, u, it.get("company",""), it.get("filed",""), path, now, now,
             json.dumps({k: it.get(k) for k in ("cik","accession","form","period","doc","score","url",
                                                 "report_type","series_count","series_sample")}), DOMAIN))
        have.add(u); new += 1
    conn.commit(); conn.close()
    return (new, skip)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("registry")
    f = sub.add_parser("filings"); f.add_argument("--cik", required=True); f.add_argument("--form")
    f.add_argument("--limit", type=int, default=20)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--forms", nargs="*")
    s.add_argument("--limit", type=int, default=20); s.add_argument("--start"); s.add_argument("--end")
    s.add_argument("--ciks", nargs="*", help="scope to CIKs or registry keys -- unscoped N-PX search returns 2004 micro-funds")
    for p in (f, s):
        p.add_argument("--store", action="store_true"); p.add_argument("--fetch-docs", action="store_true")
        p.add_argument("--classify", action="store_true", help="tag N-PX reportType (NOTICE vs VOTING REPORT)")
        p.add_argument("--voting-only", action="store_true", help="implies --classify; keep only FUND VOTING REPORT")
        p.add_argument("--out", default=str(OUT_DEFAULT)); p.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.cmd == "registry":
        print(f"{'key':<10}{'CIK':<14}{'name':<30}notes")
        for k,(c,n,note) in REGISTRY.items(): print(f"{k:<10}{c:<14}{n[:28]:<30}{note}")
        return

    if a.cmd == "filings":
        cik = REGISTRY.get(a.cik, (a.cik,))[0]
        items = list_filings(cik, a.form, a.limit); total = len(items)
    else:
        r = fulltext(a.query, a.forms, a.limit, a.start, a.end,
                     [REGISTRY.get(c,(c,))[0] for c in (a.ciks or [])] or None)
        items = r["hits"]; total = r["total"]
        print(f"full-text total matches: {total:,}  (showing {len(items)})")

    if getattr(a, "classify", False) or getattr(a, "voting_only", False):
        items = classify(items)
        if getattr(a, "voting_only", False):
            items = [i for i in items if "VOTING" in str(i.get("report_type","")).upper()]
            print(f"kept {len(items)} FUND VOTING REPORT filings")

    if a.json: print(json.dumps(items, indent=2))
    else:
        for it in items:
            rt = f"  [{it['report_type']} · {it.get('series_count','?')} series]" if it.get("report_type") else ""
            print(f"  {it.get('form','?'):<8} {it.get('filed','?')}  {it.get('company','?')[:30]:<32}{it.get('accession')}{rt}")
            if it.get("series_sample"): print(f"             covers: {'; '.join(it['series_sample'][:3])}")
            if it.get("index_url"): print(f"             {it['index_url']}")
    if getattr(a, "store", False):
        n, sk = store(items, Path(a.out), a.fetch_docs)
        print(f"\nstored {n} new, skipped {sk} already present -> {KNOWLEDGE_DB.name} (domain={DOMAIN})")

if __name__ == "__main__":
    main()
