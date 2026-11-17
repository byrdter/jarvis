#!/usr/bin/env python3
"""Business simulator, prototype 1: a fictional online store ("Harbor & Pine", apparel + home goods).

Runs N simulated days of an ongoing business and fills a SQLite database plus a real mailbox file:
  customers   arrive by a seasonal Poisson process; each gets a hidden purchase rate (Gamma) and a
              chance of quietly leaving after each order (Beta) — the BG/NBD "buy till you die" model
              marketers use to forecast real customers.
  orders      basket size and item choice follow category popularity; prices carry occasional sales.
  returns     per-category return rates and reasons, with a realistic lag after delivery.
  suppliers   stock runs down; at the reorder point a purchase order goes out and arrives after a
              random lead time. Stockouts lose sales and trigger "where's my order" email.
  email       every customer touchpoint is a real RFC 822 message in an mbox file (open it in any mail
              program), and also in the `emails` table. Templated here (fast, free); an LLM can rewrite
              a sample for realism (see llm_emails.py).

Usage: sim.py [--days 730] [--seed 7] [--out out/]   Stdlib + numpy only.
All names and numbers are invented. Rates are labeled ASSUMED where they're placeholders to calibrate."""
import argparse
import mailbox
import sqlite3
import time
from datetime import date, timedelta
from email.message import EmailMessage
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---- the business (ASSUMED values; calibrate later against real data) ----
CATEGORIES = {  # name: (share of demand, price range, margin, return rate, days to return)
    "apparel":     (0.45, (25, 120), 0.55, 0.26, (5, 30)),
    "footwear":    (0.15, (60, 160), 0.50, 0.20, (5, 30)),
    "home":        (0.25, (15, 90),  0.60, 0.08, (5, 30)),
    "accessories": (0.15, (10, 60),  0.65, 0.10, (5, 30)),
}
RETURN_REASONS = {"apparel": [("doesn't fit", .52), ("changed mind", .18), ("not as pictured", .15), ("defective", .08), ("arrived late", .07)],
                  "footwear": [("doesn't fit", .58), ("changed mind", .14), ("not as pictured", .12), ("defective", .10), ("arrived late", .06)],
                  "home": [("damaged in shipping", .35), ("not as pictured", .25), ("changed mind", .25), ("defective", .15)],
                  "accessories": [("changed mind", .40), ("not as pictured", .30), ("defective", .20), ("arrived late", .10)]}
SEASON = [0.80, 0.75, 0.90, 0.95, 1.00, 0.95, 0.90, 0.95, 1.00, 1.05, 1.45, 1.80]  # Jan..Dec
WEEKDAY = [1.05, 1.00, 1.00, 1.00, 1.05, 0.95, 0.95]                                   # Mon..Sun
NEW_CUSTOMERS_PER_DAY = 22.0    # base acquisition, grows 25%/year
SUPPORT_Q_RATE = 0.06           # share of orders that spark a pre/post-sale question
FIRST = ["Ana", "Ben", "Carla", "Dev", "Elena", "Femi", "Grace", "Hugo", "Ines", "Jamal", "Kim", "Luis", "Maya",
         "Noah", "Olga", "Priya", "Quinn", "Rosa", "Sam", "Tara", "Umar", "Vera", "Wes", "Ximena", "Yuki", "Zoe"]
LAST = ["Alvarez", "Brooks", "Chen", "Diaz", "Evans", "Fischer", "Garcia", "Hughes", "Ito", "Jensen", "Khan",
        "Lopez", "Morris", "Nguyen", "Okafor", "Patel", "Reyes", "Silva", "Taylor", "Usman", "Vargas", "Walsh"]
SHOP = "Harbor & Pine <hello@harborpine.test>"   # .test is reserved: these addresses can never reach anyone


SCHEMA = """
CREATE TABLE suppliers(id INTEGER PRIMARY KEY, name TEXT, category TEXT, lead_mean REAL);
CREATE TABLE products(id INTEGER PRIMARY KEY, sku TEXT, name TEXT, category TEXT, price REAL, cost REAL,
  supplier_id INT, stock INT, reorder_point INT, reorder_qty INT, popularity REAL);
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, email TEXT, joined TEXT, city TEXT,
  hidden_rate REAL, hidden_dropout REAL, churned_on TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INT, placed TEXT, delivered TEXT, status TEXT,
  subtotal REAL, discount REAL);
CREATE TABLE order_items(order_id INT, product_id INT, qty INT, unit_price REAL);
CREATE TABLE returns(id INTEGER PRIMARY KEY, order_id INT, product_id INT, requested TEXT, reason TEXT,
  refund REAL, restocked INT);
CREATE TABLE purchase_orders(id INTEGER PRIMARY KEY, supplier_id INT, product_id INT, qty INT, ordered TEXT,
  arrives TEXT, received INT);
CREATE TABLE lost_sales(day TEXT, product_id INT, customer_id INT);
CREATE TABLE emails(id INTEGER PRIMARY KEY, sent TEXT, sender TEXT, recipient TEXT, subject TEXT, body TEXT,
  kind TEXT, customer_id INT, order_id INT);
"""


class Store:
    def __init__(self, days: int, seed: int, out: Path):
        self.rng = np.random.default_rng(seed)
        self.days, self.start = days, date(2025, 1, 1)
        out.mkdir(parents=True, exist_ok=True)
        for f in ("store.db", "mail.mbox"):
            (out / f).unlink(missing_ok=True)
        self.db = sqlite3.connect(out / "store.db")
        self.db.executescript(SCHEMA)
        self.mbox = mailbox.mbox(str(out / "mail.mbox"))
        self.customers: list[dict] = []
        self.pending_deliveries: dict[date, list] = {}
        self.pending_returns: dict[date, list] = {}
        self.pending_pos: dict[date, list] = {}
        self.email_count = 0
        self._catalog()

    # ---------- setup ----------
    def _catalog(self):
        r = self.rng
        cats = list(CATEGORIES)
        for i, c in enumerate(cats, 1):
            self.db.execute("INSERT INTO suppliers VALUES(?,?,?,?)", (i, f"{c.title()} Source Co.", c, float(r.uniform(6, 18))))
        self.products = []
        pid = 0
        for si, c in enumerate(cats, 1):
            share, (lo, hi), margin, *_ = CATEGORIES[c]
            n = int(40 * share / 0.25)
            pop = r.pareto(1.3, n) + 1          # a few products sell most of the volume (long tail)
            pop = pop / pop.sum() * share
            for j in range(n):
                pid += 1
                price = round(float(r.uniform(lo, hi)), 2) - 0.01
                p = dict(id=pid, cat=c, price=price, cost=round(price * (1 - margin), 2), supplier=si,
                         stock=int(r.integers(40, 160)), rop=30, rq=120, pop=float(pop[j]))
                self.products.append(p)
                self.db.execute("INSERT INTO products VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                (pid, f"{c[:3].upper()}-{pid:04d}", f"{c.title()} item {pid}", c, price, p["cost"],
                                 si, p["stock"], 30, 120, p["pop"]))
        self.pop = np.array([p["pop"] for p in self.products])
        self.pop /= self.pop.sum()

    # ---------- email ----------
    def mail(self, day: date, sender, recipient, subject, body, kind, cust=None, order=None):
        m = EmailMessage()
        m["From"], m["To"], m["Subject"] = sender, recipient, subject
        hour = int(self.rng.integers(7, 23))
        m["Date"] = format_datetime(datetime(day.year, day.month, day.day, hour, int(self.rng.integers(0, 60)), tzinfo=timezone.utc))
        m["X-Sim-Kind"] = kind
        m.set_content(body)
        self.mbox.add(m)
        self.email_count += 1
        self.db.execute("INSERT INTO emails(sent,sender,recipient,subject,body,kind,customer_id,order_id) VALUES(?,?,?,?,?,?,?,?)",
                        (day.isoformat(), sender, recipient, subject, body, kind, cust, order))

    def addr(self, c):
        return f"{c['name']} <{c['email']}>"

    # ---------- daily tick ----------
    def new_customers(self, day: date, t: int):
        r = self.rng
        lam = NEW_CUSTOMERS_PER_DAY * (1.25 ** (t / 365)) * SEASON[day.month - 1] * WEEKDAY[day.weekday()]
        for _ in range(r.poisson(lam)):
            cid = len(self.customers) + 1
            first, last = r.choice(FIRST), r.choice(LAST)
            c = dict(id=cid, name=f"{first} {last}", email=f"{first.lower()}.{last.lower()}{cid}@mail.test",
                     rate=float(r.gamma(0.5, 1 / 90)),      # orders per day; mean ~0.0056 => ~2/yr while active (ASSUMED)
                     drop=float(r.beta(2.0, 2.0)),
                     basket=float(r.gamma(1.2, 1 / 1.2)),    # own spend level: some always buy one thing, some fill a cart (Gamma-Gamma idea)           # chance of leaving after each order, incl. the first (ASSUMED)
                     alive=True, joined=day)
            self.customers.append(c)
            self.db.execute("INSERT INTO customers VALUES(?,?,?,?,?,?,?,NULL)",
                            (cid, c["name"], c["email"], day.isoformat(), r.choice(["Austin", "Denver", "Portland", "Atlanta", "Chicago", "Boston"]),
                             c["rate"], c["drop"]))
            self.place_order(day, c, first_order=True)

    def place_order(self, day: date, c: dict, first_order=False):
        r = self.rng
        n_items = 1 + r.poisson(0.7 * c.get("basket", 1.0) ** 1.6)
        picks = r.choice(len(self.products), size=n_items, p=self.pop)
        sale = day.month == 11 and day.day >= 24 or r.random() < 0.08
        items, missing = [], []
        for i in picks:
            p = self.products[i]
            if p["stock"] <= 0:
                missing.append(p)
                self.db.execute("INSERT INTO lost_sales VALUES(?,?,?)", (day.isoformat(), p["id"], c["id"]))
                continue
            p["stock"] -= 1
            items.append(p)
            self.check_reorder(day, p)
        if missing and not items:
            self.mail(day, self.addr(c), SHOP, "Is this back in stock?",
                      f"Hi, I wanted {missing[0]['cat']} item {missing[0]['id']} but it says sold out. Any idea when it's back?\n{c['name']}",
                      "stock_question", c["id"])
            return
        if not items:
            return
        subtotal = round(sum(p["price"] for p in items), 2)
        discount = round(subtotal * 0.2, 2) if sale else 0.0
        delivered = day + timedelta(days=int(r.integers(2, 8)))
        cur = self.db.execute("INSERT INTO orders(customer_id,placed,delivered,status,subtotal,discount) VALUES(?,?,?,?,?,?)",
                              (c["id"], day.isoformat(), delivered.isoformat(), "placed", subtotal, discount))
        oid = cur.lastrowid
        self.db.executemany("INSERT INTO order_items VALUES(?,?,?,?)", [(oid, p["id"], 1, p["price"]) for p in items])
        lines = "\n".join(f"  - {p['cat'].title()} item {p['id']}  ${p['price']:.2f}" for p in items)
        self.mail(day, SHOP, self.addr(c), f"Order #{oid} confirmed",
                  f"Hi {c['name'].split()[0]},\n\nThanks for your order!\n{lines}\nTotal: ${subtotal - discount:.2f}\n\nHarbor & Pine", "order_confirmation", c["id"], oid)
        self.pending_deliveries.setdefault(delivered, []).append((oid, c, items))
        if r.random() < SUPPORT_Q_RATE:
            q = r.choice(["Can I change the shipping address?", "Does this run true to size?", "Can I add a gift note?",
                          "My discount code didn't apply.", "When will this ship?"])
            self.mail(day, self.addr(c), SHOP, f"Question about order #{oid}", f"Hi, {q}\nThanks, {c['name']}", "support_question", c["id"], oid)
        if r.random() < c["drop"]:
            c["alive"] = False
            self.db.execute("UPDATE customers SET churned_on=? WHERE id=?", ((day + timedelta(days=1)).isoformat(), c["id"]))

    def deliver(self, day: date):
        r = self.rng
        for oid, c, items in self.pending_deliveries.pop(day, []):
            self.db.execute("UPDATE orders SET status='delivered' WHERE id=?", (oid,))
            self.mail(day, SHOP, self.addr(c), f"Order #{oid} delivered", "Your order has arrived. Enjoy!", "delivered", c["id"], oid)
            for p in items:
                _, _, _, rate, (lo, hi) = CATEGORIES[p["cat"]]
                if r.random() < rate:
                    when = day + timedelta(days=int(min(hi, r.gamma(2.0, 4.0) + lo)))
                    self.pending_returns.setdefault(when, []).append((oid, c, p))

    def process_returns(self, day: date):
        r = self.rng
        for oid, c, p in self.pending_returns.pop(day, []):
            reasons = RETURN_REASONS[p["cat"]]
            reason = reasons[r.choice(len(reasons), p=[w for _, w in reasons])][0]
            restock = reason not in ("defective", "damaged in shipping")
            if restock:
                p["stock"] += 1
            self.db.execute("INSERT INTO returns(order_id,product_id,requested,reason,refund,restocked) VALUES(?,?,?,?,?,?)",
                            (oid, p["id"], day.isoformat(), reason, p["price"], int(restock)))
            self.mail(day, self.addr(c), SHOP, f"Return request, order #{oid}",
                      f"Hi, I'd like to return the {p['cat']} item {p['id']}. Reason: {reason}.\n{c['name']}", "return_request", c["id"], oid)
            self.mail(day, SHOP, self.addr(c), f"Your return for order #{oid}",
                      f"Hi {c['name'].split()[0]}, your return label is attached. Refund of ${p['price']:.2f} once it arrives.", "return_label", c["id"], oid)

    def check_reorder(self, day: date, p: dict):
        if p["stock"] <= p["rop"] and not p.get("on_order"):
            lead = max(2, int(self.rng.normal(12, 4)))
            arrives = day + timedelta(days=lead)
            cur = self.db.execute("INSERT INTO purchase_orders(supplier_id,product_id,qty,ordered,arrives,received) VALUES(?,?,?,?,?,0)",
                                  (p["supplier"], p["id"], p["rq"], day.isoformat(), arrives.isoformat()))
            p["on_order"] = True
            self.pending_pos.setdefault(arrives, []).append((cur.lastrowid, p))
            self.mail(day, SHOP, f"{p['cat'].title()} Source Co. <orders@{p['cat']}-source.test>", f"PO #{cur.lastrowid}",
                      f"Please ship {p['rq']} units of SKU {p['id']}. Thanks, Harbor & Pine purchasing", "purchase_order")

    def receive_pos(self, day: date):
        for po, p in self.pending_pos.pop(day, []):
            p["stock"] += p["rq"]
            p["on_order"] = False
            self.db.execute("UPDATE purchase_orders SET received=1 WHERE id=?", (po,))

    def repeat_orders(self, day: date):
        r = self.rng
        mult = SEASON[day.month - 1] * WEEKDAY[day.weekday()]
        for c in self.customers:
            if c["alive"] and r.random() < c["rate"] * mult:
                self.place_order(day, c)

    def run(self):
        t0 = time.time()
        for t in range(self.days):
            day = self.start + timedelta(days=t)
            self.receive_pos(day)
            self.deliver(day)
            self.process_returns(day)
            self.repeat_orders(day)
            self.new_customers(day, t)
        self.db.execute("UPDATE products SET stock=stock")  # final stock written below
        self.db.executemany("UPDATE products SET stock=? WHERE id=?", [(p["stock"], p["id"]) for p in self.products])
        self.db.commit()
        self.mbox.flush()
        return time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default=str(Path(__file__).parent / "out"))
    a = ap.parse_args()
    s = Store(a.days, a.seed, Path(a.out))
    secs = s.run()
    q = lambda sql: s.db.execute(sql).fetchone()[0]
    print(f"simulated {a.days} days in {secs:.1f}s")
    for t in ("customers", "orders", "order_items", "returns", "purchase_orders", "lost_sales", "emails"):
        print(f"  {t:16} {q(f'SELECT COUNT(*) FROM {t}'):>8,}")


if __name__ == "__main__":
    main()
