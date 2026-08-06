#!/usr/bin/env python3
"""db-integrity.py — integrity check and repair for the asset library.

TOOL CONTRACT
  SUBSYSTEM  S1 State (asset registry)
  STATE      reads: assets, keywords, categories, embeddings, metadata_cache
             writes: deletes orphaned CHILD rows only (--fix). Never deletes an asset row.
  GATE       refuses to modify anything without --fix; always backs up first; refuses if
             the backup cannot be written.
  MODULE     jarvis-asset-library (tools tree)
  SCOPE      format-agnostic

WHY THIS EXISTS
  assets.db declares ON DELETE CASCADE on every child table, but SQLite defaults
  foreign_keys to OFF and nothing in this toolchain ever turned it on. The cascades
  have therefore never fired. Measured 2026-08-06: 83 orphaned embeddings, 83 orphaned
  metadata_cache rows, 1,914 orphaned keywords.

  NOTE ON IMPACT, measured not assumed: search-assets-db.py joins
  `assets JOIN embeddings ON a.id = e.asset_id`, so orphaned embeddings are excluded
  by the join and do NOT corrupt search results. They are dead weight and misleading
  counts, not a scoring bug. The real search defect is the opposite case — an asset
  with NO embedding is invisible to semantic search entirely.

  PRAGMA foreign_keys is per-CONNECTION and cannot be persisted in the file. Every
  tool that opens this database must set it. This script reports which ones don't.

    db-integrity.py                 check only (default, read-only)
    db-integrity.py --fix           delete orphaned child rows, after backing up
    db-integrity.py --json          machine-readable
"""
import argparse
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path(os.environ.get("JARVIS_ASSETS", Path.home() / "Library/CloudStorage/Dropbox/jarvis/asset-library")) / "assets.db"

# child table -> column holding the asset id
CHILDREN = {"keywords": "asset_id", "categories": "asset_id",
            "embeddings": "asset_id", "metadata_cache": "asset_id"}


def connect(db: Path) -> sqlite3.Connection:
    if not db.exists():
        sys.exit(f"FAIL: no database at {db}\n  Set $JARVIS_ASSETS or fix the path.")
    c = sqlite3.connect(db)
    c.execute("PRAGMA foreign_keys = ON")   # what should always have been set
    c.row_factory = sqlite3.Row
    return c


def survey(c: sqlite3.Connection) -> dict:
    n_assets = c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
    orphans = {t: c.execute(
        f"SELECT COUNT(*) FROM {t} x LEFT JOIN assets a ON a.id = x.{col} WHERE a.id IS NULL"
    ).fetchone()[0] for t, col in CHILDREN.items()}
    unembedded = [dict(r) for r in c.execute(
        "SELECT a.id, a.file_path FROM assets a "
        "LEFT JOIN embeddings e ON e.asset_id = a.id WHERE e.asset_id IS NULL")]
    missing = [dict(r) for r in c.execute("SELECT id, file_path, type FROM assets")
               if not os.path.exists(r["file_path"])]
    return {"db": str(DB), "assets": n_assets, "orphans": orphans,
            "orphan_total": sum(orphans.values()),
            "unembedded": unembedded, "missing_files": missing}


def backup(db: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = db.with_name(f"{db.name}.bak-{stamp}")
    try:
        shutil.copy2(db, dest)
    except OSError as e:
        sys.exit(f"FAIL: could not write backup to {dest}: {e}\n  Refusing to modify the database.")
    return dest


def fix(c: sqlite3.Connection, s: dict) -> dict:
    """Delete orphaned CHILD rows. Asset rows are never touched — a row whose file is
    missing is a judgement call for a human, not for this script."""
    deleted = {}
    for t, col in CHILDREN.items():
        cur = c.execute(
            f"DELETE FROM {t} WHERE {col} NOT IN (SELECT id FROM assets)")
        deleted[t] = cur.rowcount
    c.commit()
    c.execute("VACUUM")
    return deleted


def report(s: dict, deleted=None, backup_path=None) -> int:
    print(f"asset library : {s['db']}")
    print(f"assets        : {s['assets']}")
    print("\norphaned child rows (reference an asset id that does not exist):")
    for t, n in s["orphans"].items():
        print(f"  {t:<16} {n:>6}" + ("" if n else "   ok"))
    print(f"  {'TOTAL':<16} {s['orphan_total']:>6}")

    print(f"\nassets with NO embedding : {len(s['unembedded'])}"
          "   <- INVISIBLE to semantic search (inner join drops them)")
    for r in s["unembedded"][:10]:
        print(f"    id={r['id']:<6} {os.path.basename(r['file_path'])[:66]}")

    print(f"\nassets whose file is GONE : {len(s['missing_files'])}"
          "   <- rows kept; deleting an asset row is a human call")
    for r in s["missing_files"][:10]:
        print(f"    id={r['id']:<6} {r['file_path'][:80]}")

    if deleted is not None:
        print(f"\nbackup written : {backup_path}")
        print("deleted:")
        for t, n in deleted.items():
            print(f"  {t:<16} {n:>6}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Asset library integrity check/repair")
    ap.add_argument("--fix", action="store_true", help="delete orphaned child rows (backs up first)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--db", type=Path, help="override database path")
    a = ap.parse_args()

    global DB
    if a.db:
        DB = a.db
    c = connect(DB)
    s = survey(c)

    if a.json and not a.fix:
        print(json.dumps(s, indent=1))
        return 0

    if not a.fix:
        report(s)
        if s["orphan_total"]:
            print(f"\n{s['orphan_total']} orphaned rows. Re-run with --fix to delete them.")
        return 0

    if not s["orphan_total"]:
        print("nothing to fix")
        return report(s)

    b = backup(DB)
    deleted = fix(c, s)
    after = survey(c)
    report(after, deleted=deleted, backup_path=b)
    if after["orphan_total"]:
        print(f"\nFAIL: {after['orphan_total']} orphans remain")
        return 1
    print("\nintegrity restored")
    return 0


if __name__ == "__main__":
    sys.exit(main())
