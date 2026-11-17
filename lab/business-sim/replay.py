#!/usr/bin/env python3
"""Replay test for a company app: run the same stores twice, with the old rule and with the app, and
compare. Each seed is a different store (customers, catalog, suppliers); within a seed both runs see the
SAME customers wanting the SAME things, so the difference is the app's doing.

Usage: replay.py [--seeds 1 2 3 4 5] [--days 730]   (about 20 s per run)"""
import argparse
import json
import sqlite3
import statistics as st
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out" / "replay"


def lost(db, like):
    return db.execute("SELECT COALESCE(SUM(p.price), 0) FROM lost_sales l JOIN products p ON p.id = l.product_id "
                      "WHERE day LIKE ?", (like,)).fetchone()[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    ap.add_argument("--days", type=int, default=730)
    a = ap.parse_args()
    by = {}
    for s in a.seeds:
        for pol in ("naive", "advisor"):
            r = subprocess.run([sys.executable, str(HERE / "sim.py"), "--seed", str(s), "--policy", pol, "--days", str(a.days),
                                "--no-mbox", "--json", "--out", str(OUT / f"{pol}-{s}")], capture_output=True, text=True, check=True)
            by.setdefault(s, {})[pol] = json.loads(r.stdout)
    keys = [("lost_sales_value", "lost sales $"), ("avg_stock_value", "avg stock $"),
            ("purchase_orders", "supplier orders"), ("profit_after_stock_costs", "profit after stock costs $")]
    print(f"{'store':6}" + "".join(f"{lab:>30}" for _, lab in keys) + "   (old rule -> advisor)")
    for s, d in sorted(by.items()):
        print(f"{s:<6}" + "".join(f"{d['naive'][k]:>13,} -> {d['advisor'][k]:>12,}" for k, _ in keys))
    gain = [d["advisor"]["profit_after_stock_costs"] - d["naive"]["profit_after_stock_costs"] for d in by.values()]
    print(f"\nprofit gain: mean ${st.mean(gain):,.0f} (range ${min(gain):,} to ${max(gain):,}); "
          f"advisor ahead in {sum(g > 0 for g in gain)} of {len(gain)} stores")
    for pol in ("naive", "advisor"):
        yrs = sorted({y for s in by for y in ("2025", "2026")})
        vals = [st.mean(lost(sqlite3.connect(OUT / f"{pol}-{s}" / "store.db"), y + "%") for s in by) for y in yrs]
        print(f"{pol:8} mean lost sales by year: " + ", ".join(f"{y} ${v:,.0f}" for y, v in zip(yrs, vals)))


if __name__ == "__main__":
    main()
