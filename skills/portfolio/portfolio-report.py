#!/usr/bin/env python3
"""Consolidated view across every account in the portfolio store.

Answers the "what is what" question: total value, split by asset class, and
each holding rolled up across accounts -- because a position held in two
accounts is one economic exposure, and looking at either account alone
understates it.

Reports FACTS ONLY: what you hold, what it cost, what it is worth. It does not
rank, score, or suggest. Those are your decisions.

Usage:
  ./portfolio-report.py                 # latest snapshot per account
  ./portfolio-report.py --as-of 2026-08-23
  ./portfolio-report.py --markdown      # write to jarvis-private/portfolio/
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

STORE_DIR = Path.home() / "Library/CloudStorage/Dropbox/jarvis-private/portfolio"
DB = STORE_DIR / "portfolio.db"

CLASS_LABEL = {
    "equity": "Equities",
    "etf": "ETFs",
    "money_market": "Money market funds",
    "cash": "Cash",
    "mutual_fund": "Mutual funds",
    "fixed_income": "Fixed income",
    "real_estate_syndication": "Real estate syndications",
    "other": "Other",
}
# Cash equivalents, for the invested-vs-uninvested split.
CASHLIKE = {"cash", "money_market"}


def latest_snapshots(con, as_of: str | None) -> list[tuple]:
    if as_of:
        return con.execute(
            "SELECT s.id, a.label, s.as_of FROM snapshots s "
            "JOIN accounts a ON a.id=s.account_id WHERE s.as_of=? "
            "ORDER BY a.label", (as_of,)).fetchall()
    return con.execute(
        "SELECT s.id, a.label, s.as_of FROM snapshots s "
        "JOIN accounts a ON a.id=s.account_id "
        "WHERE s.as_of=(SELECT MAX(as_of) FROM snapshots s2 "
        "               WHERE s2.account_id=s.account_id) "
        "ORDER BY a.label").fetchall()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of")
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args()

    if not DB.exists():
        print(f"No portfolio store at {DB}. Run import-positions.py first.",
              file=sys.stderr)
        return 1

    con = sqlite3.connect(str(DB))
    snaps = latest_snapshots(con, args.as_of)
    if not snaps:
        print("No snapshots found.", file=sys.stderr)
        return 1

    rows, by_account = [], {}
    for sid, label, as_of in snaps:
        pos = con.execute(
            "SELECT symbol, description, quantity, price, market_value, "
            "cost_basis, gain_usd, asset_class FROM positions "
            "WHERE snapshot_id=?", (sid,)).fetchall()
        by_account[label] = (as_of, sum(p[4] for p in pos))
        for p in pos:
            rows.append((label,) + p)
    con.close()

    total = sum(r[5] for r in rows)
    by_class = defaultdict(float)
    for r in rows:
        by_class[r[8]] += r[5]
    cashlike = sum(v for k, v in by_class.items() if k in CASHLIKE)
    invested = total - cashlike

    # Roll each symbol up across accounts.
    agg = defaultdict(lambda: {"qty": 0.0, "mv": 0.0, "cb": 0.0,
                               "desc": "", "accts": set(), "cls": ""})
    for label, sym, desc, qty, price, mv, cb, gain, cls in rows:
        if cls in CASHLIKE:
            continue
        key = sym or desc
        a = agg[key]
        a["qty"] += qty or 0
        a["mv"] += mv or 0
        a["cb"] += cb or 0
        a["desc"] = desc
        a["cls"] = cls
        a["accts"].add(label)

    out = []
    w = out.append
    stamp = snaps[0][2]
    w(f"# Portfolio — consolidated as of {stamp}\n")
    w(f"**Total across {len(by_account)} accounts: ${total:,.2f}**\n")

    w("\n## By account\n")
    w(f"| Account | As of | Value | % of total |")
    w(f"|---|---|---:|---:|")
    for label, (as_of, v) in sorted(by_account.items()):
        w(f"| {label} | {as_of} | ${v:,.2f} | {v/total*100:.1f}% |")

    w("\n## By asset class\n")
    w("| Class | Value | % of total |")
    w("|---|---:|---:|")
    for cls, v in sorted(by_class.items(), key=lambda kv: -kv[1]):
        w(f"| {CLASS_LABEL.get(cls, cls)} | ${v:,.2f} | {v/total*100:.1f}% |")
    w(f"| **Invested** | **${invested:,.2f}** | **{invested/total*100:.1f}%** |")
    w(f"| **Cash + money market** | **${cashlike:,.2f}** "
      f"| **{cashlike/total*100:.1f}%** |")

    w(f"\n## Holdings, consolidated across accounts\n")
    w("| Symbol | Description | Qty | Market value | Cost basis | Gain/loss | % of total | % of invested | Accounts |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for key, a in sorted(agg.items(), key=lambda kv: -kv[1]["mv"]):
        gain = a["mv"] - a["cb"]
        gpct = (gain / a["cb"] * 100) if a["cb"] else 0.0
        n = len(a["accts"])
        w(f"| {key} | {a['desc'][:30]} | {a['qty']:,.0f} | ${a['mv']:,.2f} "
          f"| ${a['cb']:,.2f} | ${gain:,.2f} ({gpct:+.1f}%) "
          f"| {a['mv']/total*100:.2f}% | {a['mv']/invested*100:.2f}% "
          f"| {n} |")

    inv_cb = sum(a["cb"] for a in agg.values())
    inv_gain = invested - inv_cb
    w(f"\n**Invested sleeve:** ${invested:,.2f} against ${inv_cb:,.2f} cost "
      f"— ${inv_gain:,.2f} ({inv_gain/inv_cb*100:+.1f}%) unrealized.\n")

    dupes = [k for k, a in agg.items() if len(a["accts"]) > 1]
    if dupes:
        w(f"**Held in more than one account ({len(dupes)}):** "
          f"{', '.join(sorted(dupes))}. Each is a single economic exposure; "
          f"the per-account view understates it.\n")

    text = "\n".join(out)
    print(text)
    if args.markdown:
        p = STORE_DIR / f"portfolio-consolidated-{stamp}.md"
        p.write_text(text + "\n", encoding="utf-8")
        print(f"\n✓ wrote {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
