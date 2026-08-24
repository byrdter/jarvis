#!/usr/bin/env python3
"""Add a `domain` column to content_sources and tag existing rows.

Why: the aggregator was built for one source set, so every row landed in one
undifferentiated corpus. Running it against the financial feeds on 2026-08-23
put 394 finance articles beside the AI articles in the same table, with only
the feed name in `author` to tell them apart. Without a domain tag the AI
digest dedupes against finance articles and can surface them.

The column defaults to 'ai' so every pre-existing row keeps its meaning, and
finance rows are identified by feed name against the two finance configs.
That is safe because the AI and finance configs share no feed names -- checked
before writing this, and re-checked at runtime below.

Idempotent: safe to run more than once.

Usage:
  ./venv/bin/python migrate-add-domain.py            # dry run, shows the plan
  ./venv/bin/python migrate-add-domain.py --apply    # back up, then migrate
"""
from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config"
DB = HERE.parents[1] / "agent-sdk" / "data" / "ai-knowledge.db"

FINANCE_CONFIGS = ["finance-feeds.json", "finance-radar.json"]
AI_CONFIG = "rss-feeds.json"


def load_names(fname: str) -> set[str]:
    p = CONFIG / fname
    if not p.exists():
        raise SystemExit(f"ERROR: missing config {p}")
    return set(json.loads(p.read_text()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="actually migrate (default is a dry run)")
    ap.add_argument("--db", default=str(DB))
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        raise SystemExit(f"ERROR: database not found: {db}")

    finance = set()
    for f in FINANCE_CONFIGS:
        finance |= load_names(f)
    ai = load_names(AI_CONFIG)

    # Re-check the assumption this migration depends on. If a feed name ever
    # appears in both configs, tagging by name is ambiguous and this script
    # must not guess.
    clash = ai & finance
    if clash:
        raise SystemExit(
            f"ERROR: {len(clash)} feed name(s) in BOTH the AI and finance "
            f"configs, so rows cannot be tagged by name: {sorted(clash)}")

    con = sqlite3.connect(db)
    cur = con.cursor()

    cols = {r[1] for r in cur.execute("pragma table_info(content_sources)")}
    has_domain = "domain" in cols

    total = cur.execute("select count(*) from content_sources").fetchone()[0]
    qmarks = ",".join("?" * len(finance))
    fin_rows = cur.execute(
        f"select count(*) from content_sources where author in ({qmarks})",
        sorted(finance)).fetchone()[0]

    print(f"database      : {db}")
    print(f"total rows    : {total:,}")
    print(f"finance feeds : {len(finance)} names")
    print(f"rows matching : {fin_rows:,}  -> domain='finance'")
    print(f"rows remaining: {total - fin_rows:,}  -> domain='ai'")
    print(f"domain column : {'already present' if has_domain else 'will be added'}")

    if not args.apply:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = db.with_name(f"{db.stem}.pre-domain-{stamp}.bak")
    print(f"\nbacking up -> {backup}")
    con.close()
    shutil.copy2(db, backup)

    con = sqlite3.connect(db)
    cur = con.cursor()
    try:
        if not has_domain:
            # DEFAULT 'ai' is the load-bearing part: every row that existed
            # before the finance feeds were ever run keeps its original
            # meaning without a second pass.
            cur.execute("alter table content_sources "
                        "add column domain TEXT NOT NULL DEFAULT 'ai'")
            cur.execute("create index if not exists idx_content_domain "
                        "on content_sources(domain)")
        cur.execute(
            f"update content_sources set domain='finance' "
            f"where author in ({qmarks})", sorted(finance))
        changed = cur.rowcount
        con.commit()
    except Exception:
        con.rollback()
        print("FAILED -- rolled back; database unchanged. "
              f"Backup is at {backup}", file=sys.stderr)
        raise

    print(f"tagged {changed:,} rows as domain='finance'")
    for dom, n in cur.execute(
            "select domain, count(*) from content_sources group by domain"):
        print(f"  {dom:<8} {n:,}")
    con.close()
    print("\nOK. Backup retained; delete it once the next digests look right.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
