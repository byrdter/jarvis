#!/usr/bin/env python3
"""rights-check.py — can these assets go in a monetised video?

TOOL CONTRACT
  SUBSYSTEM  Q (Quality), gating P8 Distribution
  STATE      reads: assets.rights, license, provenance  ·  writes: nothing
  GATE       exits 1 if any asset is BLOCKED. 'unknown' is BLOCKED, never assumed safe —
             that is the whole point of the column.
  MODULE     jarvis-asset-library (tools tree). Lives with the lane deliberately: the lane
             publishes monetised videos and must be able to run this WITHOUT the umbrella
             or ORICO (federation rule 1 — a module never depends upward).
  SCOPE      format-agnostic

VERDICTS
  SAFE    owned · generated · licensed WITH terms recorded
  REVIEW  editorial (third-party UI capture — standard practice in commentary, but it is a
          judgement call, not a fact) · licensed with no terms recorded
  BLOCK   unknown — origin was never established. Most free-tier generators forbid
          commercial use, so an unverified asset in a monetised video is a real exposure.

    rights-check.py --all                     posture of the whole library
    rights-check.py --project ka-ep01         everything produced for one project
    rights-check.py path/one.mp4 path/two.png specific files
    rights-check.py --paths list.txt          one path per line
    rights-check.py --strict                  REVIEW also fails (exit 1)
"""
import argparse
import os
import sqlite3
import sys
from pathlib import Path

DB = Path(os.environ.get("JARVIS_ASSETS",
                         Path.home() / "Library/CloudStorage/Dropbox/jarvis/asset-library")) / "assets.db"

SAFE, REVIEW, BLOCK = "SAFE", "REVIEW", "BLOCK"


def verdict(rights: str, license_: str | None) -> str:
    if rights in ("owned", "generated"):
        return SAFE
    if rights == "licensed":
        return SAFE if (license_ or "").strip() else REVIEW
    if rights == "editorial":
        return REVIEW
    return BLOCK          # unknown, null, or anything unrecognised


def fetch(c, args) -> list[sqlite3.Row]:
    if args.all:
        return c.execute("SELECT * FROM assets").fetchall()
    if args.project:
        return c.execute("SELECT * FROM assets WHERE provenance LIKE ?",
                         (f"produced for project: {args.project}%",)).fetchall()
    paths = list(args.paths_pos)
    if args.paths:
        paths += [l.strip() for l in open(args.paths, encoding="utf8") if l.strip()]
    if not paths:
        sys.exit("nothing to check — pass --all, --project, or one or more paths")
    # Resolve on file_path first. A bare basename is only accepted when it is UNIQUE:
    # 49 filenames are duplicated across directories (measured 2026-08-08), and
    # env-doorway-into-office.png exists BOTH in addition-images/ (unknown) and
    # pixeladdition-images/ (owned). Picking either one would silently clear or block the
    # wrong file. A rights gate must refuse to guess.
    rows, unresolved = [], []
    for p in paths:
        r = c.execute("SELECT * FROM assets WHERE file_path=?", (p,)).fetchone()
        if r:
            rows.append(r)
            continue
        cands = c.execute("SELECT * FROM assets WHERE file_name=?",
                          (os.path.basename(p),)).fetchall()
        if len(cands) == 1:
            rows.append(cands[0])
        elif not cands:
            unresolved.append((p, "NOT IN REGISTRY"))
        else:
            unresolved.append((p, f"AMBIGUOUS — {len(cands)} files share this name; pass the full path"))
    for p, why in unresolved:
        print(f"  BLOCK   {why}  {p}")
    if unresolved:
        print(f"\n{len(unresolved)} asset(s) could not be resolved — cannot be cleared.\n")
    return rows + [None] * len(unresolved)


def main() -> int:
    ap = argparse.ArgumentParser(description="Rights gate for monetised use")
    ap.add_argument("paths_pos", nargs="*", metavar="PATH")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--project")
    ap.add_argument("--paths", help="file with one path per line")
    ap.add_argument("--strict", action="store_true", help="REVIEW also fails")
    ap.add_argument("--db", type=Path)
    a = ap.parse_args()

    db = a.db or DB
    if not db.exists():
        sys.exit(f"FAIL: no database at {db}")
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    if "rights" not in {r[1] for r in c.execute("PRAGMA table_info(assets)")}:
        sys.exit("FAIL: no rights column — run classify-rights.py --apply first")

    rows = fetch(c, a)
    buckets: dict[str, list] = {SAFE: [], REVIEW: [], BLOCK: []}
    for r in rows:
        if r is None:
            buckets[BLOCK].append(None)
            continue
        buckets[verdict(r["rights"], r["license"])].append(r)

    total = len(rows)
    print(f"checked {total} asset(s)\n")
    for v in (SAFE, REVIEW, BLOCK):
        n = len(buckets[v])
        if n:
            print(f"  {v:<7} {n:>5}  ({100.0*n/max(1,total):4.1f}%)")

    for v in (REVIEW, BLOCK):
        sample = [r for r in buckets[v] if r is not None][:5]
        if sample:
            print(f"\n  --- {v} (first {len(sample)}) ---")
            for r in sample:
                print(f"    {r['rights']:<10} {r['provenance'] or '(no provenance)':<44} {r['file_name'][:36]}")

    failed = len(buckets[BLOCK]) + (len(buckets[REVIEW]) if a.strict else 0)
    if failed:
        print(f"\nFAIL: {failed} asset(s) not cleared"
              f"{' (--strict: REVIEW counts as failure)' if a.strict else ''}.")
        print("  Establish origin, then record it:")
        print("    UPDATE assets SET rights='generated', rights_basis='declared',")
        print("      rights_reviewed_at=datetime('now') WHERE id=...;")
        print("  See what needs deciding:  classify-rights.py --review")
        return 1
    print("\nall clear")
    return 0


if __name__ == "__main__":
    sys.exit(main())
