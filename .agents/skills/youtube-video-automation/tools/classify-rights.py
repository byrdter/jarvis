#!/usr/bin/env python3
"""classify-rights.py — populate rights / provenance on the asset library.

TOOL CONTRACT
  SUBSYSTEM  S1 State (asset registry)
  STATE      reads:  assets.file_path, file_name
             writes: assets.rights, license, provenance, rights_basis  (adds the columns if absent)
  GATE       dry-run by default; --apply to write. NEVER overwrites a row a human has
             reviewed (rights_reviewed_at IS NOT NULL). Never guesses: anything not matched
             by an explicit rule stays 'unknown'.
  MODULE     jarvis-asset-library (tools tree) — assets.db is the lane's WORKING COPY, and
             the lane needs rights more than the studio does: it assembles monetised videos.
  SCOPE      format-agnostic

WHY THE COLUMNS LIVE HERE AND NOT IN studio.db
  studio.db is a MIRROR (decided 2026-08-07). migrate-registry.py rebuilds it with
  INSERT OR REPLACE, so anything written only to the mirror is destroyed on the next
  --force. Rights are a property of the asset, so they belong with the asset.

WHAT IS AND IS NOT DERIVABLE — measured 2026-08-08, not assumed
  Two candidate signals were tested and REJECTED as false positives:
    * description containing "ai-generated"  -> describes what is IN the image
      ("a man reviewing AI-generated content"), not the image's origin. 221 rows matched;
      the signal is worthless.
    * description containing "stock photo/footage" -> matched pixel-art illustrations.
  Only PATH and NAMING CONVENTION survive as evidence. Everything else is 'unknown', and
  'unknown' is treated as BLOCKING by rights-check.py, never as safe.

    classify-rights.py            dry run — show what would change
    classify-rights.py --apply    write it
    classify-rights.py --review   list what still needs a human decision
"""
import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

DB = Path(os.environ.get("JARVIS_ASSETS",
                         Path.home() / "Library/CloudStorage/Dropbox/jarvis/asset-library")) / "assets.db"

NEW_COLS = {
    "rights": "TEXT NOT NULL DEFAULT 'unknown'",   # owned|editorial|licensed|generated|unknown
    "license": "TEXT",                             # actual terms, when known
    "provenance": "TEXT",                          # where it came from / what it was made for
    "rights_basis": "TEXT",                        # path-rule|declared|unclassified
    "rights_reviewed_at": "TEXT",                  # set by a human; blocks re-classification
}

PROJECT_RE = re.compile(r"^(?P<proj>[a-z0-9][a-z0-9\-]*?)__")


def add_columns(c: sqlite3.Connection) -> list[str]:
    have = {r[1] for r in c.execute("PRAGMA table_info(assets)")}
    added = []
    for col, decl in NEW_COLS.items():
        if col not in have:
            c.execute(f"ALTER TABLE assets ADD COLUMN {col} {decl}")
            added.append(col)
    c.commit()
    return added


def classify(path: str, name: str) -> tuple[str | None, str | None, str | None]:
    """(rights, provenance, basis). rights=None means 'leave unknown'.

    Ordered most-specific first. Every rule must be defensible from the path alone.
    """
    p = path.lower()

    # Files whose source is gone — cannot be assessed, must not be assumed safe.
    if "/var/folders/" in p or "/t/tmp." in p:
        return None, "source file missing (temp dir, purged)", "path-rule"

    # Screen captures of third-party product UI. Vendor is the directory under products/.
    if "/products/" in p:
        seg = path.split("/products/", 1)[1].split("/")
        vendor = seg[0] if seg and seg[0] else "unknown-vendor"
        return "editorial", f"third-party UI capture: {vendor}", "path-rule"

    # Terry's own pixel-art series. Backed by an explicit standing note, not inference.
    if re.search(r"/(pixel[a-z\-]*|addpixelimages)/", p):
        return "owned", "Terry original — pixel-art series", "path-rule"

    # Produced for a named project. Factual and useful, but says nothing about RIGHTS:
    # a project asset may have been generated OR sourced. Provenance only.
    m = PROJECT_RE.match(name)
    if m:
        return None, f"produced for project: {m.group('proj')}", "path-rule"

    return None, None, "unclassified"


def run(c: sqlite3.Connection, apply: bool) -> dict:
    rows = c.execute(
        "SELECT id, file_path, file_name, rights_reviewed_at FROM assets").fetchall()
    tally, updates, locked = {}, [], 0
    for r in rows:
        if r["rights_reviewed_at"]:
            locked += 1
            continue
        rights, prov, basis = classify(r["file_path"], r["file_name"])
        key = rights or "unknown"
        tally[key] = tally.get(key, 0) + 1
        updates.append((rights or "unknown", prov, basis, r["id"]))

    if apply:
        c.executemany(
            "UPDATE assets SET rights=?, provenance=?, rights_basis=? WHERE id=?", updates)
        c.commit()
    return {"tally": tally, "n": len(updates), "human_locked": locked}


def report_review(c: sqlite3.Connection) -> int:
    rows = c.execute(
        "SELECT provenance, COUNT(*) n FROM assets WHERE rights='unknown' "
        "GROUP BY provenance ORDER BY n DESC").fetchall()
    total = c.execute("SELECT COUNT(*) FROM assets WHERE rights='unknown'").fetchone()[0]
    print(f"{total} assets need a human rights decision:\n")
    for r in rows:
        print(f"  {r['n']:>5}  {r['provenance'] or '(no provenance derivable)'}")
    print("\nTo clear a group once you know its origin, e.g.:")
    print("  UPDATE assets SET rights='generated', rights_basis='declared',")
    print("    rights_reviewed_at=datetime('now') WHERE provenance LIKE 'produced for project: ka-ep01%';")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Populate rights/provenance on the asset library")
    ap.add_argument("--apply", action="store_true", help="write (default is a dry run)")
    ap.add_argument("--review", action="store_true", help="list what still needs a human decision")
    ap.add_argument("--db", type=Path)
    a = ap.parse_args()

    db = a.db or DB
    if not db.exists():
        sys.exit(f"FAIL: no database at {db}")
    c = sqlite3.connect(db)
    c.execute("PRAGMA foreign_keys = ON")
    c.row_factory = sqlite3.Row

    added = add_columns(c)
    if added:
        print(f"added columns: {', '.join(added)}\n")

    if a.review:
        return report_review(c)

    res = run(c, apply=a.apply)
    print(f"{'APPLIED' if a.apply else 'DRY RUN'} — {res['n']} assets classified"
          + (f", {res['human_locked']} skipped (human-reviewed)" if res["human_locked"] else ""))
    print()
    for k in sorted(res["tally"], key=lambda x: -res["tally"][x]):
        n = res["tally"][k]
        pct = 100.0 * n / max(1, res["n"])
        note = "  <- BLOCKING for commercial use until reviewed" if k == "unknown" else ""
        print(f"  {k:<10} {n:>5}  ({pct:4.1f}%){note}")
    if not a.apply:
        print("\nre-run with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
