#!/usr/bin/env python3
"""research-topic.py — SCRIPTING Step 0 research helper.

Given a topic, search the JARVIS wikis (FTS5 index, reused — same index the production
wiki API uses) and return ranked, CITED passages to write a VO script from. Zero-dep
(python3 stdlib only). Reads each hit's frontmatter for a full citation + thesis lens.

Usage:
  python3 research-topic.py "will AI automate or augment jobs" [--wiki ai-futures]
  python3 research-topic.py "AI regulation power" --wiki ai-futures,second-brain --top 15 --json
Default wiki: ai-futures. Multiple allowed (comma-separated). --json for machine output.
"""
import argparse, glob, json, os, re, sqlite3, sys, pathlib

PRIV = pathlib.Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private")

def find_db_for(table):
    for db in glob.glob(str(PRIV/"*-wiki"/"wiki-search.db")):
        try:
            con = sqlite3.connect(db)
            if con.execute("SELECT name FROM sqlite_master WHERE name=? AND type='table'",(table,)).fetchone():
                return db
        except Exception: pass
        finally:
            try: con.close()
            except Exception: pass
    return None

def frontmatter(path):
    """Read YAML-ish frontmatter from a wiki md file (best-effort)."""
    fm = {}
    p = pathlib.Path(path)
    if not p.is_absolute():
        # FTS 'path' may be relative to a wiki dir; try to resolve
        for cand in glob.glob(str(PRIV/"*-wiki"/path)) + glob.glob(str(PRIV/"*-wiki"/"wiki"/path)):
            if os.path.exists(cand): p = pathlib.Path(cand); break
    try:
        txt = p.read_text(errors="ignore")
    except Exception:
        return fm
    if txt.startswith("---"):
        block = txt.split("---",2)[1]
        for line in block.splitlines():
            m = re.match(r'(\w[\w_]*):\s*(.*)', line)
            if m: fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm

def search_wiki(slug, terms, top):
    table = slug.replace("-","_") + "_fts"
    db = find_db_for(table)
    if not db:
        print(f"  (no FTS table {table} found)", file=sys.stderr); return []
    con = sqlite3.connect(db); con.row_factory = sqlite3.Row
    q = " OR ".join(re.sub(r'[^a-z0-9 ]',' ',t.lower()) for t in terms if t.strip())
    try:
        rows = con.execute(
            f"SELECT slug,path,category,title, snippet({table},4,'《','》',' … ',14) AS snip, "
            f"bm25({table}) AS score FROM {table} WHERE {table} MATCH ? ORDER BY score LIMIT ?",
            (q, top)).fetchall()
    except Exception as e:
        print(f"  query error on {table}: {e}", file=sys.stderr); return []
    finally:
        con.close()
    out = []
    for r in rows:
        fm = frontmatter(r["path"])
        out.append({"wiki":slug,"title":r["title"] or fm.get("title",""),
                    "author":fm.get("author",""),"url":fm.get("url",""),
                    "lens":fm.get("thesis_lens",""),"source":fm.get("source_type",fm.get("source","")),
                    "published":fm.get("published",""),"category":r["category"],
                    "snippet":(r["snip"] or "").replace("\n"," ").strip(),
                    "score":round(r["score"],2),"path":r["path"]})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--wiki", default="ai-futures", help="comma-separated wiki slugs")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    terms = args.query.split()
    hits = []
    for slug in [s.strip() for s in args.wiki.split(",") if s.strip()]:
        hits += search_wiki(slug, terms, args.top)
    hits.sort(key=lambda h: h["score"])           # bm25: lower = better
    hits = hits[:args.top]
    if args.json:
        print(json.dumps(hits, indent=2)); return
    if not hits:
        print("No hits. Try broader terms, or re-run the fetchers to seed more content."); return
    print(f"\nTOP {len(hits)} for: {args.query!r}\n" + "="*70)
    for h in hits:
        lens = f"  [{h['lens']}]" if h['lens'] else ""
        print(f"\n● {h['title']}{lens}")
        meta = " · ".join(x for x in [h['author'], h['source'], h['published']] if x)
        if meta: print(f"  {meta}")
        if h['url']: print(f"  {h['url']}")
        if h['snippet']: print(f"  … {h['snippet']} …")
        print(f"  [{h['wiki']} · {h['path']}]")
    # lens balance hint
    from collections import Counter
    c = Counter(h['lens'] for h in hits if h['lens'])
    if c: print("\nlens balance:", dict(c))

if __name__ == "__main__":
    main()
