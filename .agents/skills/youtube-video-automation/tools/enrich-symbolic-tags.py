#!/usr/bin/env python3
"""enrich-symbolic-tags.py — add symbolizes + usable_as tags to assets.

Cheaper than re-running vision: infers the symbolic/usability tags from each asset's
EXISTING metadata (description/mood/setting/people) via a small text model. Supports the
VISUAL-SOURCING.md vision (find a clip by what it can REPRESENT and how it can be USED).

Usage:
  python3 enrich-symbolic-tags.py --db /path/to/assets.db [--limit N] [--all] [--dry-run]
  (default: only rows where symbolizes IS NULL)
Requires ANTHROPIC_API_KEY (read from --db dir's ../.env or repo .env, or the environment).
"""
import argparse, json, os, sqlite3, sys, pathlib

USABLE_VOCAB = {"breather","background","establishing","symbolic","literal"}

def load_key():
    if os.environ.get("ANTHROPIC_API_KEY"): return os.environ["ANTHROPIC_API_KEY"]
    # search a few likely .env locations
    here = pathlib.Path(__file__).resolve()
    candidates = [pathlib.Path.cwd()/".env",
                  pathlib.Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/.env")]
    for env in candidates:
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=",1)[1].strip().strip('"').strip("'")
    return None

PROMPT = """You tag stock assets for a video library so an editor can find non-literal visuals.
Given one asset's existing metadata, infer two things:

1. "symbolizes": 2-5 ABSTRACT ideas this asset could REPRESENT (not literal objects). Examples:
   overwhelm, relief, choice, growth, isolation, momentum, layoffs, collaboration, focus,
   uncertainty, success, burnout, transformation, control, hope. Lowercase, concise.
2. "usable_as": pick ALL that apply from EXACTLY this set:
   - "breather": short atmospheric/human pause to reset pace (calm/reflective clips)
   - "background": works low-opacity behind text/graphics
   - "establishing": opens a scene / sets place
   - "symbolic": stands in for an abstract idea
   - "literal": shows a concrete specific thing (screenshot, data, named object)

Return STRICT JSON only: {"symbolizes":[...],"usable_as":[...]}

ASSET:
type: %(type)s   duration: %(duration)s
description: %(description)s
mood: %(mood)s
setting: %(setting)s
people: %(people)s"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--all", action="store_true", help="re-tag even rows that already have symbolizes")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="claude-haiku-4-5")
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("❌ ANTHROPIC_API_KEY not found (env or .env)"); sys.exit(1)
    import anthropic
    client = anthropic.Anthropic(api_key=key)

    con = sqlite3.connect(args.db); con.row_factory = sqlite3.Row
    where = "" if args.all else "WHERE symbolizes IS NULL OR TRIM(symbolizes)=''"
    rows = con.execute(f"SELECT id,file_name,type,duration,description,mood,setting,people FROM assets {where} ORDER BY id").fetchall()
    if args.limit: rows = rows[:args.limit]
    print(f"enriching {len(rows)} assets (model={args.model}, dry_run={args.dry_run})")

    done=0; fail=0
    for r in rows:
        p = PROMPT % {k:(r[k] if r[k] not in (None,"") else "n/a") for k in
                      ["type","duration","description","mood","setting","people"]}
        try:
            resp = client.messages.create(model=args.model, max_tokens=300,
                                           messages=[{"role":"user","content":p}])
            txt = resp.content[0].text.strip()
            txt = txt[txt.find("{"): txt.rfind("}")+1]
            data = json.loads(txt)
            sym = [s.strip().lower() for s in data.get("symbolizes",[]) if s.strip()][:5]
            use = [u.strip().lower() for u in data.get("usable_as",[]) if u.strip().lower() in USABLE_VOCAB]
            print(f"  [{r['id']:>3}] {r['file_name'][:34]:<34} sym={sym} use={use}")
            if not args.dry_run:
                con.execute("UPDATE assets SET symbolizes=?, usable_as=? WHERE id=?",
                            (", ".join(sym), ", ".join(use), r["id"]))
                con.commit()
            done+=1
        except Exception as e:
            print(f"  [{r['id']}] FAIL: {e}"); fail+=1
    print(f"done: {done} tagged, {fail} failed")

if __name__ == "__main__":
    main()
