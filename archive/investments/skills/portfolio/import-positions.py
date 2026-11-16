#!/usr/bin/env python3
"""Import brokerage position exports into the JARVIS portfolio store.

This is the file portfolio-monitor/run.py has been waiting for. That script
carries hardcoded paper positions (QQQ/USO/BIL, shares: 0) with the comment
"will eventually read from database/file" -- this is that database.

DATA LOCATION: the store lives in jarvis-private, never in the jarvis repo,
which is public on GitHub. Positions, cost basis, and account numbers must not
leave the private tree.

Design notes:
- SNAPSHOT-BASED. Every import records positions as-of a timestamp rather than
  overwriting. That gives a real position history for free, which is what
  performance-tracker needs and what a single mutable "current holdings" table
  could never reconstruct.
- RECONCILED. Each broker file carries its own "Positions Total" row. We parse
  it, compare against the sum of what we parsed, and refuse the import if they
  disagree by more than a cent. A silent parse error in a financial store is
  worse than no import.
- Multi-asset by design: equities, ETFs, money-market funds, cash, and manual
  entries (real-estate syndications, external accounts) share one schema.

Usage:
  ./import-positions.py ~/path/*.csv                 # import, reconcile
  ./import-positions.py --dry-run ~/path/file.csv    # parse and report only
  ./import-positions.py --list                       # show stored snapshots
"""
from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

STORE_DIR = Path.home() / ("Library/CloudStorage/Dropbox/jarvis-private/portfolio")
DB = STORE_DIR / "portfolio.db"

# Broker asset-type strings -> our normalized classes. Anything unrecognized
# is kept verbatim under 'other' rather than guessed at.
ASSET_CLASS = {
    "equity": "equity",
    "etf": "etf",
    "etfs & closed end funds": "etf",
    "cash and money market": "money_market",
    "mutual fund": "mutual_fund",
    "fixed income": "fixed_income",
    "option": "option",
}

# Money-market funds are cash equivalents, not equity holdings. Classifying
# them by symbol keeps a $98k SWVXX position from reading as a stock pick.
MONEY_MARKET_SYMBOLS = {"SWVXX", "SNAXX", "SNVXX", "SPAXX", "FDRXX", "SPRXX",
                        "VMFXX", "VMRXX", "SGOV"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  label         TEXT NOT NULL UNIQUE,
  custodian     TEXT,
  account_type  TEXT,          -- taxable | ira | roth | joint | ...
  owner         TEXT,          -- lets a spouse's accounts live here too
  masked_number TEXT
);
CREATE TABLE IF NOT EXISTS snapshots (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id  INTEGER NOT NULL REFERENCES accounts(id),
  as_of       TEXT NOT NULL,
  source_file TEXT,
  imported_at TEXT NOT NULL,
  total_value REAL,
  UNIQUE(account_id, as_of)
);
CREATE TABLE IF NOT EXISTS positions (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  snapshot_id  INTEGER NOT NULL REFERENCES snapshots(id) ON DELETE CASCADE,
  symbol       TEXT,
  description  TEXT,
  quantity     REAL,
  price        REAL,
  market_value REAL,
  cost_basis   REAL,
  gain_usd     REAL,
  gain_pct     REAL,
  asset_class  TEXT,
  raw_type     TEXT
);
CREATE INDEX IF NOT EXISTS idx_pos_snapshot ON positions(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_pos_symbol   ON positions(symbol);
CREATE INDEX IF NOT EXISTS idx_snap_asof    ON snapshots(as_of);
"""

_HDR_RE = re.compile(
    r'Positions for account\s+(?P<label>.+?)\s*\.\.\.(?P<mask>\w+)\s+'
    r'as of\s+(?P<time>.+?),\s*(?P<date>\d{4}/\d{2}/\d{2})', re.I)


def money(s: str | None) -> float | None:
    """'$1,584.90' / '-$8.28' / '25,000' / '--' -> float or None."""
    if s is None:
        return None
    s = s.strip().replace("$", "").replace(",", "").replace("%", "")
    if s in ("", "--", "N/A", "-"):
        return None
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def classify(symbol: str, raw_type: str, description: str) -> str:
    if symbol and symbol.upper() in MONEY_MARKET_SYMBOLS:
        return "money_market"
    key = (raw_type or "").strip().lower()
    if key in ASSET_CLASS:
        cls = ASSET_CLASS[key]
        # A broker lumps sweep cash and MM funds under one label; separate them
        # so "how much actual cash" stays answerable.
        if cls == "money_market" and "cash" in (description or "").lower():
            return "cash"
        return cls
    return "other"


def infer_account_type(label: str) -> str:
    low = label.lower()
    if "roth" in low:
        return "roth_ira"
    if "ira" in low:
        return "ira"
    if "joint" in low:
        return "joint"
    if "trust" in low:
        return "trust"
    return "taxable"


def parse_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    if not raw:
        raise ValueError("empty file")

    m = _HDR_RE.search(raw[0])
    if not m:
        raise ValueError(f"unrecognized header line: {raw[0][:90]!r}")
    label = m.group("label").strip()
    as_of = datetime.strptime(m.group("date"), "%Y/%m/%d").strftime("%Y-%m-%d")

    # Find the real column header, skipping the blank spacer line.
    hdr_idx = next((i for i, l in enumerate(raw)
                    if l.lstrip('"').startswith("Symbol")), None)
    if hdr_idx is None:
        raise ValueError("no 'Symbol' header row found")

    rows = list(csv.DictReader(raw[hdr_idx:]))
    positions, stated_total = [], None

    for r in rows:
        sym = (r.get("Symbol") or "").strip()
        if not sym:
            continue
        desc = (r.get("Description") or "").strip()
        mv = money(r.get("Mkt Val (Market Value)"))

        if sym.lower().startswith("positions total"):
            stated_total = mv
            continue

        if mv is None:
            continue

        raw_type = (r.get("Asset Type") or "").strip()
        is_cash_row = sym.lower().startswith("cash")
        positions.append({
            "symbol": None if is_cash_row else sym,
            "description": desc if not is_cash_row else "Cash & Cash Investments",
            "quantity": money(r.get("Qty (Quantity)")),
            "price": money(r.get("Price")),
            "market_value": mv,
            "cost_basis": money(r.get("Cost Basis")),
            "gain_usd": money(r.get("Gain $ (Gain/Loss $)")),
            "gain_pct": money(r.get("Gain % (Gain/Loss %)")),
            "asset_class": "cash" if is_cash_row else classify(sym, raw_type, desc),
            "raw_type": raw_type,
        })

    return {"label": label, "masked": m.group("mask"), "as_of": as_of,
            "positions": positions, "stated_total": stated_total,
            "source_file": path.name}


def reconcile(parsed: dict) -> tuple[bool, str]:
    """Compare our sum against the broker's own stated total."""
    got = round(sum(p["market_value"] for p in parsed["positions"]), 2)
    stated = parsed["stated_total"]
    if stated is None:
        return True, f"no stated total in file; parsed ${got:,.2f}"
    delta = round(got - stated, 2)
    if abs(delta) > 0.01:
        return False, (f"MISMATCH parsed ${got:,.2f} vs stated ${stated:,.2f} "
                       f"(delta ${delta:,.2f})")
    return True, f"reconciled ${got:,.2f}"


def connect() -> sqlite3.Connection:
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA)
    return con


def store(con: sqlite3.Connection, parsed: dict) -> tuple[int, bool]:
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO accounts(label, custodian, account_type, owner, "
        "masked_number) VALUES(?,?,?,?,?)",
        (parsed["label"], None, infer_account_type(parsed["label"]),
         "terry", parsed["masked"]))
    acct = cur.execute("SELECT id FROM accounts WHERE label=?",
                       (parsed["label"],)).fetchone()[0]

    existing = cur.execute(
        "SELECT id FROM snapshots WHERE account_id=? AND as_of=?",
        (acct, parsed["as_of"])).fetchone()
    if existing:
        # Re-importing the same day replaces that day rather than doubling it.
        cur.execute("DELETE FROM positions WHERE snapshot_id=?", (existing[0],))
        cur.execute("DELETE FROM snapshots WHERE id=?", (existing[0],))
        replaced = True
    else:
        replaced = False

    total = round(sum(p["market_value"] for p in parsed["positions"]), 2)
    cur.execute(
        "INSERT INTO snapshots(account_id, as_of, source_file, imported_at, "
        "total_value) VALUES(?,?,?,datetime('now'),?)",
        (acct, parsed["as_of"], parsed["source_file"], total))
    snap = cur.lastrowid
    cur.executemany(
        "INSERT INTO positions(snapshot_id, symbol, description, quantity, "
        "price, market_value, cost_basis, gain_usd, gain_pct, asset_class, "
        "raw_type) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        [(snap, p["symbol"], p["description"], p["quantity"], p["price"],
          p["market_value"], p["cost_basis"], p["gain_usd"], p["gain_pct"],
          p["asset_class"], p["raw_type"]) for p in parsed["positions"]])
    con.commit()
    return snap, replaced


def list_snapshots() -> int:
    if not DB.exists():
        print("No portfolio store yet.", file=sys.stderr)
        return 0
    con = connect()
    rows = con.execute(
        "SELECT a.label, s.as_of, s.total_value, count(p.id) "
        "FROM snapshots s JOIN accounts a ON a.id=s.account_id "
        "LEFT JOIN positions p ON p.snapshot_id=s.id "
        "GROUP BY s.id ORDER BY s.as_of DESC, a.label").fetchall()
    con.close()
    print(f"{'ACCOUNT':<34} {'AS OF':<12} {'TOTAL':>14}  POS")
    for label, as_of, total, n in rows:
        print(f"{label:<34} {as_of:<12} {total:>14,.2f}  {n}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        return list_snapshots()
    if not args.files:
        ap.error("give at least one CSV, or --list")

    con = None if args.dry_run else connect()
    failed = 0
    for f in args.files:
        if not f.exists():
            print(f"✗ {f.name}: not found", file=sys.stderr)
            failed += 1
            continue
        try:
            parsed = parse_file(f)
        except Exception as e:
            print(f"✗ {f.name}: {e}", file=sys.stderr)
            failed += 1
            continue

        ok, msg = reconcile(parsed)
        mark = "✓" if ok else "✗"
        print(f"{mark} {parsed['label']} ({parsed['as_of']}) "
              f"{len(parsed['positions'])} positions — {msg}")
        if not ok:
            print("   refusing to import a file that does not reconcile.",
                  file=sys.stderr)
            failed += 1
            continue
        if not args.dry_run:
            _, replaced = store(con, parsed)
            if replaced:
                print(f"   (replaced existing {parsed['as_of']} snapshot)")

    if con:
        con.close()
        print(f"\nstore: {DB}")
    else:
        print("\nDRY RUN — nothing written.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
