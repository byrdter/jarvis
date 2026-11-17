#!/usr/bin/env python3
"""The reorder advisor: a company app that decides, every morning, what to order from suppliers.

It sees only what a real shop has: its own sales history, the sales it lost when shelves were empty, and
its past purchase orders. It never sees the simulation's hidden settings (the true seasonal pattern, the
true lead times). Plain statistics, no LLM, so it is free, fast and explainable:

  1. demand per product = units sold + units wanted but out of stock, over the last 28 days
  2. seasonality, learned: once a year of history exists, scale by how the coming weeks went last year
     compared with the weeks just before (the whole store, so one product's noise doesn't swing it)
  3. lead time, learned from past purchase orders (mean and spread)
  4. reorder point = expected demand during the lead time + safety stock for 95% of lead-time demand
  5. when stock + on-order falls to it, order enough to cover the lead time plus COVER_DAYS

The shop's old rule ("at 30 left, order 120", the same for every product) is in sim.py for comparison."""
import math
from datetime import date, timedelta

WINDOW = 28          # days of history used for the demand rate
COVER_DAYS = 21      # how far beyond the lead time each order should last
Z = 1.65             # safety stock for ~95% of lead-time demand
MIN_ORDER = 10


class ReorderAdvisor:
    def __init__(self):
        self.log = []      # (day, product, qty, why) for explaining decisions

    def _demand(self, db, start: date, end: date) -> dict[int, list[int]]:
        """Units wanted per product per day in [start, end): sold + lost."""
        days = (end - start).days
        out: dict[int, list[int]] = {}
        rows = db.execute("""SELECT oi.product_id, o.placed, COUNT(*) FROM order_items oi JOIN orders o ON o.id = oi.order_id
                             WHERE o.placed >= ? AND o.placed < ? GROUP BY 1, 2
                             UNION ALL
                             SELECT product_id, day, COUNT(*) FROM lost_sales WHERE day >= ? AND day < ? GROUP BY 1, 2""",
                          (start.isoformat(), end.isoformat(), start.isoformat(), end.isoformat())).fetchall()
        for pid, d, n in rows:
            out.setdefault(pid, [0] * days)[(date.fromisoformat(d) - start).days] += n
        return out

    def _store_total(self, db, start: date, end: date) -> int:
        return sum(sum(v) for v in self._demand(db, start, end).values())

    def _season_factor(self, db, today: date, horizon: int) -> float:
        """How much busier the next `horizon` days were than the last WINDOW days, a year ago."""
        ly = today - timedelta(days=364)       # same weekday last year
        if ly - timedelta(days=WINDOW) < date(2025, 1, 1):
            return 1.0                         # no year of history yet: no seasonal knowledge
        before = self._store_total(db, ly - timedelta(days=WINDOW), ly) / WINDOW
        ahead = self._store_total(db, ly, ly + timedelta(days=horizon)) / horizon
        return min(3.0, max(0.5, ahead / before)) if before else 1.0

    def _lead_time(self, db) -> tuple[float, float]:
        rows = db.execute("SELECT julianday(arrives) - julianday(ordered) FROM purchase_orders WHERE received = 1").fetchall()
        if len(rows) < 5:
            return 14.0, 4.0                   # a cautious guess until we have our own history
        xs = [r[0] for r in rows[-200:]]
        m = sum(xs) / len(xs)
        return m, math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))

    def recommend(self, db, today: date, products: list[dict]) -> list[tuple[dict, int]]:
        hist = self._demand(db, today - timedelta(days=WINDOW), today)
        lead, lead_sd = self._lead_time(db)
        season = self._season_factor(db, today, int(lead + COVER_DAYS))
        orders = []
        for p in products:
            xs = hist.get(p["id"], [0] * WINDOW)
            mean = sum(xs) / WINDOW
            sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / WINDOW)
            d = mean * season
            safety = Z * math.sqrt(lead * (sd * season) ** 2 + d ** 2 * lead_sd ** 2)
            rop = d * lead + safety
            position = p["stock"] + p.get("on_order", 0)
            if d > 0 and position <= rop:
                qty = max(MIN_ORDER, math.ceil(d * (lead + COVER_DAYS) + safety - position))
                orders.append((p, qty))
                self.log.append((today.isoformat(), p["id"], qty,
                                 f"{d:.1f}/day x {lead:.0f}-day lead, season x{season:.2f}, stock+on-order {position}"))
        return orders
