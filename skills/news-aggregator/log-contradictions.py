#!/usr/bin/env python3
"""Extract Section 3 of the daily finance brief into a countable ledger.

WHY THIS EXISTS
    The Ordinary Economics channel bible names two premise engines. The second is
    "Section 3 of the daily finance brief, which detects where weighted sources
    contradict each other," and records its hit rate as "unknown -- n = 2. It needs
    30 days of logging before it can be counted on."

    Nothing was logging. Section 3 was generated fresh each morning into a markdown
    file and never read again, so thirty days of that produces thirty documents and
    still no hit rate. This turns each day's disagreements into rows that can be
    counted, filtered and marked up as they become videos -- or don't.

THE BIBLE'S QUALIFYING TEST, made into fields
    "Two named sources disagreeing about WHY something happened, with a checkable
    mechanism on one side, is a video premise."
      -> source_a / source_b   both named, with their reliability weights
      -> kind                  factual disagreement vs forecasting disagreement
      -> mechanism             is there something checkable on one side? 0/1
    A forecasting disagreement with no checkable mechanism is not a premise. Storing
    the distinction is what lets the hit rate mean anything.

STORAGE
    jarvis-private/finance-ledgers/ledgers.db -- private tree, never the public repo.

USAGE
    log-contradictions.py --brief reports/finance-digests/finance-brief-2026-08-23.md
    log-contradictions.py --all            # backfill every brief on disk
    log-contradictions.py --report         # hit rate to date
    log-contradictions.py --mark 3 premise --note "annuity sequence risk"
"""
from __future__ import annotations
import argparse, json, re, sqlite3, subprocess, sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIEF_DIR = HERE.parents[1] / "reports" / "finance-digests"
LEDGER = (Path.home() /
          "Library/CloudStorage/Dropbox/jarvis-private/finance-ledgers/ledgers.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS contradictions (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  brief_date   TEXT NOT NULL,
  extracted_at TEXT NOT NULL,
  claim        TEXT NOT NULL,
  source_a     TEXT, weight_a REAL,
  source_b     TEXT, weight_b REAL,
  resolution   TEXT,
  kind         TEXT,              -- factual | forecasting
  mechanism    INTEGER DEFAULT 0, -- checkable mechanism on one side?
  plate        TEXT,              -- atlas plate, when identifiable
  outcome      TEXT DEFAULT 'unreviewed',
                                  -- unreviewed | premise | rejected | scripted | published
  note         TEXT,
  pair_key     TEXT               -- normalized source pair, for carrying marks forward
);
CREATE INDEX IF NOT EXISTS idx_contra_outcome ON contradictions(outcome);
CREATE INDEX IF NOT EXISTS idx_contra_date    ON contradictions(brief_date);

-- Every brief PROCESSED, including days that produced no contradictions at all.
-- Without this the hit rate silently uses the wrong denominator: a quiet day
-- disappears instead of counting as a miss, which inflates the rate. Measuring
-- "premises per brief" requires knowing how many briefs there were.
CREATE TABLE IF NOT EXISTS briefs_processed (
  brief_date   TEXT PRIMARY KEY,
  processed_at TEXT NOT NULL,
  found        INTEGER NOT NULL DEFAULT 0
);
"""

EXTRACT_PROMPT = """Below is Section 3 of a daily financial brief, which reports where
the day's sources contradicted each other.

Return ONLY a JSON array. One object per distinct disagreement, with these keys:
  claim       - the disputed point, one sentence
  source_a    - first source name exactly as written
  weight_a    - its reliability weight as a number, or null
  source_b    - second source name exactly as written
  weight_b    - its weight as a number, or null
  resolution  - which the brief found more credible and why, one sentence, or null
  kind        - "factual" if they disagree about what happened or why,
                "forecasting" if they disagree about what will happen
  mechanism   - true if at least one side offers something specific and checkable
                (a named figure, a filing, a documented mechanism); false otherwise

If the section says there were no material contradictions, return [].
No prose, no code fence, just the array.

SECTION 3:
"""


def _pair_key(a: str | None, b: str | None) -> str:
    """Order- and case-insensitive key for a pair of disagreeing sources."""
    parts = sorted((a or "").strip().lower() + "|" + (b or "").strip().lower())
    return "|".join(sorted([(a or "").strip().lower(), (b or "").strip().lower()]))


def connect() -> sqlite3.Connection:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(LEDGER))
    con.executescript(SCHEMA)
    return con


def section_three(md: str) -> str | None:
    """Pull Section 3 out of a brief. Tolerates numbered and unnumbered headings."""
    m = re.search(r"^##\s*(?:\d+\.\s*)?WHERE SOURCES DISAGREE\s*$(.*?)(?=^##\s|\Z)",
                  md, re.M | re.S | re.I)
    return m.group(1).strip() if m else None


def structure(section: str, model: str, timeout: int) -> list[dict]:
    r = subprocess.run(["claude", "-p", EXTRACT_PROMPT + section, "--model", model],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"claude exited {r.returncode}: {r.stderr[:300]}")
    out = (r.stdout or "").strip()
    out = re.sub(r"^```(?:json)?\s*|\s*```$", "", out).strip()
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", out, re.S)
        if not m:
            raise
        data = json.loads(m.group(0))
    return data if isinstance(data, list) else []


def ingest(path: Path, con, model: str, timeout: int) -> tuple[int, int]:
    md = path.read_text(encoding="utf-8")
    date = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    date = date.group(1) if date else "unknown"
    sec = section_three(md)
    if not sec:
        print(f"  {path.name}: no Section 3 found", file=sys.stderr)
        return 0, 0
    rows = structure(sec, model, timeout)

    # Reprocessing a brief REPLACES that day's rows rather than adding to them.
    # The model rewrites the claim, renames the sources and reorders the pair on
    # every extraction, so no natural key survives a re-run -- a UNIQUE constraint
    # on claim text or on the source pair both leaked duplicates in testing. The
    # only reliable guarantee is that one brief maps to exactly one set of rows.
    # Human review marks are carried across on the normalized source pair.
    prior = {k: (o, n) for k, o, n in con.execute(
        "SELECT pair_key, outcome, note FROM contradictions WHERE brief_date=?",
        (date,)) if k}
    con.execute("DELETE FROM contradictions WHERE brief_date=?", (date,))

    new = dup = 0
    for r in rows:
        pk = _pair_key(r.get("source_a"), r.get("source_b"))
        outcome, note = prior.get(pk, ("unreviewed", None))
        if pk in prior:
            dup += 1
        con.execute(
            "INSERT INTO contradictions(brief_date, extracted_at, claim, "
            "source_a, weight_a, source_b, weight_b, resolution, kind, mechanism, "
            "pair_key, outcome, note) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (date, datetime.now().isoformat(timespec="seconds"),
             (r.get("claim") or "").strip(),
             r.get("source_a"), r.get("weight_a"),
             r.get("source_b"), r.get("weight_b"),
             r.get("resolution"), r.get("kind"),
             1 if r.get("mechanism") else 0, pk, outcome, note))
        new += 1
    con.execute("INSERT INTO briefs_processed(brief_date, processed_at, found) "
                "VALUES(?,?,?) ON CONFLICT(brief_date) DO UPDATE SET "
                "processed_at=excluded.processed_at, found=excluded.found",
                (date, datetime.now().isoformat(timespec="seconds"), len(rows)))
    con.commit()
    return new, dup


def report(con) -> None:
    tot = con.execute("SELECT count(*) FROM contradictions").fetchone()[0]
    if not tot:
        print("Ledger empty. Run --all to backfill.")
        return
    days = con.execute("SELECT count(*) FROM briefs_processed").fetchone()[0] or 1
    quiet = con.execute("SELECT count(*) FROM briefs_processed WHERE found=0").fetchone()[0]
    qual = con.execute("SELECT count(*) FROM contradictions "
                       "WHERE kind='factual' AND mechanism=1").fetchone()[0]
    print(f"Ledger: {LEDGER}")
    print(f"  briefs processed   {days}   (bible asks for 30 before counting on it)")
    print(f"    of which quiet   {quiet}   no contradictions at all")
    print(f"  disagreements      {tot}")
    print(f"  QUALIFYING         {qual}   factual + checkable mechanism")
    print(f"  rate               {qual/days:.2f} premises per brief "
          f"({days} briefs in denominator)")
    print("\n  by outcome:")
    for o, n in con.execute("SELECT outcome, count(*) FROM contradictions "
                            "GROUP BY outcome ORDER BY 2 DESC"):
        print(f"    {o:<12} {n}")
    print("\n  unreviewed and qualifying:")
    for i, d, c in con.execute(
            "SELECT id, brief_date, claim FROM contradictions "
            "WHERE outcome='unreviewed' AND kind='factual' AND mechanism=1 "
            "ORDER BY brief_date DESC LIMIT 10"):
        print(f"    [{i}] {d}  {c[:88]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--mark", nargs=2, metavar=("ID", "OUTCOME"))
    ap.add_argument("--note", default=None)
    ap.add_argument("--model", default="claude-sonnet-5")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()
    con = connect()

    if a.mark:
        i, outcome = a.mark
        if outcome not in ("unreviewed", "premise", "rejected", "scripted", "published"):
            raise SystemExit(f"bad outcome: {outcome}")
        con.execute("UPDATE contradictions SET outcome=?, note=COALESCE(?,note) "
                    "WHERE id=?", (outcome, a.note, int(i)))
        con.commit()
        print(f"marked {i} -> {outcome}")
        return 0

    if a.report:
        report(con); return 0

    files = ([a.brief] if a.brief
             else sorted(BRIEF_DIR.glob("finance-brief-*.md")) if a.all else [])
    if not files:
        ap.error("give --brief, --all, --report or --mark")

    tn = td = 0
    for f in files:
        n, d = ingest(f, con, a.model, a.timeout)
        tn += n; td += d
        print(f"  {f.name}: {n} rows ({d} kept prior review marks)")
    print(f"\n{tn} new rows, {td} duplicates skipped")
    report(con)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
