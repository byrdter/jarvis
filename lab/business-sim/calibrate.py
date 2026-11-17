#!/usr/bin/env python3
"""Compare the simulated store with a real one: UCI Online Retail II (a UK online retailer, Dec 2009 to
Dec 2011, ~1M invoice lines, CC BY 4.0: https://archive.ics.uci.edu/dataset/502/online+retail+ii).

Prints the same statistics for both, side by side. The first run converts the spreadsheet to SQLite
(out/data/retail.db), which takes a minute or two; later runs are instant.

Caveat: that retailer sells gifts and many of its customers are small shops buying wholesale, so it
repeats more than a consumer store would. It's a sanity bound, not a target to copy.

Usage: calibrate.py   (expects out/data/online_retail_II.xlsx and out/store.db)"""
import sqlite3
import statistics
from pathlib import Path

HERE = Path(__file__).parent
XLSX = HERE / "out/data/online_retail_II.xlsx"
REAL = HERE / "out/data/retail.db"
SIM = HERE / "out/store.db"


def load_real() -> sqlite3.Connection:
    if REAL.exists():
        return sqlite3.connect(REAL)
    import openpyxl
    db = sqlite3.connect(REAL)
    db.execute("CREATE TABLE lines(invoice TEXT, sku TEXT, qty INT, day TEXT, price REAL, customer TEXT, country TEXT)")
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    for ws in wb.worksheets:
        rows = ws.iter_rows(min_row=2, values_only=True)
        db.executemany("INSERT INTO lines VALUES(?,?,?,?,?,?,?)",
                       ((str(r[0]), str(r[1]), r[3], r[4].date().isoformat() if r[4] else None, r[5],
                         str(int(r[6])) if r[6] else None, r[7]) for r in rows))
    db.commit()
    return db


def stats(orders: list[tuple]) -> dict:
    """orders: (customer, day, value, n_lines) for completed purchases."""
    per_cust, value = {}, {}
    for c, d, v, n in orders:
        per_cust[c] = per_cust.get(c, 0) + 1
        value[c] = value.get(c, 0) + v
    vals = sorted(value.values(), reverse=True)
    top = sum(vals[: max(1, len(vals) // 5)]) / sum(vals)
    by_month = {}
    for _, d, _, _ in orders:
        by_month[d[5:7]] = by_month.get(d[5:7], 0) + 1
    peak = max(by_month.values()) / min(by_month.values())
    return {"customers": len(per_cust), "orders": len(orders),
            "repeat buyers %": 100 * sum(1 for n in per_cust.values() if n > 1) / len(per_cust),
            "orders per customer (mean)": statistics.mean(per_cust.values()),
            "orders per customer (median)": statistics.median(per_cust.values()),
            "top 20% revenue share %": 100 * top,
            "busiest / quietest month": peak,
            "lines per order (median)": statistics.median(n for *_, n in orders)}


def main():
    real = load_real()
    # one year (2010) of completed invoices from identified customers; "C" invoices are cancellations
    r_orders = real.execute("""SELECT customer, MIN(day), SUM(qty*price), COUNT(*) FROM lines
                               WHERE customer IS NOT NULL AND invoice NOT LIKE 'C%' AND day LIKE '2010-%'
                               GROUP BY invoice""").fetchall()
    r_cancel = real.execute("""SELECT -SUM(CASE WHEN invoice LIKE 'C%' THEN qty*price END) /
                                      SUM(CASE WHEN invoice NOT LIKE 'C%' THEN qty*price END)
                               FROM lines WHERE day LIKE '2010-%' AND customer IS NOT NULL""").fetchone()[0]
    sim = sqlite3.connect(SIM)
    s_orders = sim.execute("""SELECT o.customer_id, o.placed, o.subtotal - o.discount, COUNT(*) FROM orders o
                              JOIN order_items i ON i.order_id = o.id WHERE o.placed LIKE '2025-%' GROUP BY o.id""").fetchall()
    s_ret = sim.execute("""SELECT SUM(refund) / (SELECT SUM(subtotal - discount) FROM orders WHERE placed LIKE '2025-%')
                           FROM returns r JOIN orders o ON o.id = r.order_id WHERE o.placed LIKE '2025-%'""").fetchone()[0]
    a, b = stats(r_orders), stats(s_orders)
    a["returned/canceled value %"], b["returned/canceled value %"] = 100 * r_cancel, 100 * s_ret
    print(f"{'one year':30} {'UK retailer 2010':>17} {'simulation 2025':>16}")
    for k in a:
        fmt = "{:>17,.0f}" if k in ("customers", "orders") else "{:>17.1f}"
        print(f"{k:30} {fmt.format(a[k])} {fmt.format(b[k]).rjust(16)}")


if __name__ == "__main__":
    main()
