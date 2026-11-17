#!/usr/bin/env python3
"""The owner's morning brief: a company app that tells the owner, in two minutes of reading, how yesterday
went and what needs a decision today.

Two layers, on purpose (prototype 2's lesson: put the math in code, leave the words to the model):
  facts()   plain code reads the store database up to yesterday and computes every number: yesterday vs
            a normal day for that weekday, refunds, return-rate spikes per product, products about to run
            out, the customer inbox, lost sales. It also raises ALERTS with simple statistical tests.
  write()   a model turns the facts into a short brief in plain English. It may use only numbers from
            the facts; check_numbers() flags any number in the brief that isn't there.
  grade()   when the simulation planted incidents (incidents.json), checks the brief caught each one,
            and on a normal day counts false alarms.

Usage: brief.py --db out/brief/incident/store.db --today 2026-03-10 [--writer local|claude|none]"""
import argparse
import json
import math
import re
import sqlite3
import subprocess
import urllib.request
from datetime import date, timedelta
from pathlib import Path

LEAD_DAYS = 14   # typical supplier lead time; an item with less cover than this is at risk


def facts(db, today: date) -> dict:
    y = today - timedelta(days=1)
    q = lambda sql, *a: db.execute(sql, a).fetchall()
    one = lambda sql, *a: (db.execute(sql, a).fetchone() or [0])[0] or 0

    def day_stats(d):
        return (one("SELECT COUNT(*) FROM orders WHERE placed = ?", d.isoformat()),
                one("SELECT SUM(subtotal - discount) FROM orders WHERE placed = ?", d.isoformat()))

    orders_y, revenue_y = day_stats(y)
    # "Normal" = the last 7 days' level, adjusted for the weekday (from the last 8 weeks), so seasons and
    # growth don't trigger alarms: after the holidays, January is compared with early January, not December.
    last7 = [day_stats(y - timedelta(days=k)) for k in range(1, 8)]
    eight = [day_stats(y - timedelta(days=k)) for k in range(1, 57)]
    wd = [o for k, (o, _) in enumerate(eight, 1) if (y - timedelta(days=k)).weekday() == y.weekday()]
    wd_factor = (sum(wd) / len(wd)) / (sum(o for o, _ in eight) / len(eight) or 1) if wd else 1
    o_mean = sum(o for o, _ in last7) / 7 * wd_factor
    r_mean = sum(r for _, r in last7) / 7 * wd_factor
    o_sd = math.sqrt(1.5 * max(o_mean, 1))          # Poisson-like day-to-day noise, a bit wider
    z_orders = (orders_y - o_mean) / o_sd

    refunds_y = one("SELECT SUM(refund) FROM returns WHERE requested = ?", y.isoformat())
    returns_y = one("SELECT COUNT(*) FROM returns WHERE requested = ?", y.isoformat())

    # Return spikes, per product, against its own CATEGORY over the same weeks (not against its own past):
    # seasonal waves, like January returns of December gifts, hit the whole category and cancel out; a bad
    # batch doesn't. Numerator: returns requested in the last 3 weeks. Denominator: units delivered 5 to 1
    # weeks ago (the ones those returns mostly come from). Same definition for product and category, so
    # the timing bias cancels. Alert only when it's too big to be chance: z >= 4 for all returns, z >= 3
    # for defective/damaged returns (rarer, and the signature of a bad batch). Never reads past yesterday.
    t = today.isoformat()
    r_from, d_from, d_to = (today - timedelta(days=21)).isoformat(), (today - timedelta(days=35)).isoformat(), (today - timedelta(days=7)).isoformat()
    sold = dict(q("""SELECT oi.product_id, COUNT(*) FROM order_items oi JOIN orders o ON o.id = oi.order_id
                     WHERE o.delivered >= ? AND o.delivered < ? GROUP BY 1""", d_from, d_to))
    rets = dict(q("SELECT product_id, COUNT(*) FROM returns WHERE requested >= ? AND requested < ? GROUP BY 1", r_from, t))
    bads = dict(q("""SELECT product_id, COUNT(*) FROM returns WHERE requested >= ? AND requested < ?
                     AND reason IN ('defective', 'damaged in shipping') GROUP BY 1""", r_from, t))
    prods = q("SELECT id, name, category FROM products")
    cat_tot = {}
    for pid, _, cat in prods:
        c = cat_tot.setdefault(cat, [0, 0, 0])
        c[0] += sold.get(pid, 0); c[1] += rets.get(pid, 0); c[2] += bads.get(pid, 0)

    def z(k, n, p0):
        p0 = min(max(p0, 0.01), 0.95)
        return (k - n * p0) / math.sqrt(n * p0 * (1 - p0))

    spikes = []
    for pid, name, cat in prods:
        n, r, d = sold.get(pid, 0), rets.get(pid, 0), bads.get(pid, 0)
        cn, cr, cd = (x - y for x, y in zip(cat_tot[cat], (n, r, d)))     # the rest of the category
        if n < 10 or cn < 50 or r < 5:
            continue
        z_all, z_bad = z(r, n, cr / cn), z(d, n, cd / cn)
        if z_all >= 4 or (z_bad >= 3 and d >= 5):
            reasons = q("""SELECT reason, COUNT(*) FROM returns WHERE product_id = ? AND requested >= ? AND requested < ?
                           GROUP BY 1 ORDER BY 2 DESC LIMIT 2""", pid, r_from, t)
            spikes.append({"product_id": pid, "product": name, "category": cat,
                           "returns_last_3_weeks": r, "units_delivered_5_to_1_weeks_ago": n,
                           "return_rate_pct": round(100 * r / n), "category_return_rate_pct": round(100 * cr / cn),
                           "defective_last_3_weeks": d, "category_defective_rate_pct": round(100 * cd / cn, 1),
                           "top_reasons": [f"{x} ({k})" for x, k in reasons],
                           "looks_like": "a quality problem (defects)" if z_bad >= 3 and d >= 5 else "more returns than usual"})

    # Products about to run out: stock left vs the last 28 days' pace (sold + wanted but out of stock).
    stock_now = {pid: st for pid, st in q("SELECT id, stock FROM products")}
    # rebuild stock as of this morning: final stock + everything sold since - received since (simulation detail)
    for pid, n in q("""SELECT oi.product_id, COUNT(*) FROM order_items oi JOIN orders o ON o.id = oi.order_id
                       WHERE o.placed >= ? GROUP BY 1""", today.isoformat()):
        stock_now[pid] += n
    for pid, n in q("SELECT product_id, SUM(qty) FROM purchase_orders WHERE arrives >= ? AND received = 1 GROUP BY 1", today.isoformat()):
        stock_now[pid] -= n
    for pid, n in q("SELECT product_id, COUNT(*) FROM returns WHERE requested >= ? AND restocked = 1 GROUP BY 1", today.isoformat()):
        stock_now[pid] -= n
    at_risk = []
    for pid, name in q("SELECT id, name FROM products"):
        pace = (one("""SELECT COUNT(*) FROM order_items oi JOIN orders o ON o.id = oi.order_id
                       WHERE oi.product_id = ? AND o.placed >= ? AND o.placed < ?""", pid,
                    (today - timedelta(days=28)).isoformat(), today.isoformat())
                + one("SELECT COUNT(*) FROM lost_sales WHERE product_id = ? AND day >= ? AND day < ?", pid,
                      (today - timedelta(days=28)).isoformat(), today.isoformat())) / 28
        on_order = one("SELECT SUM(qty) FROM purchase_orders WHERE product_id = ? AND ordered < ? AND arrives >= ?",
                       pid, today.isoformat(), today.isoformat())
        st = max(0, stock_now[pid])
        if pace >= 0.5 and st / pace < LEAD_DAYS and not on_order:
            at_risk.append({"product_id": pid, "product": name, "units_left": st, "selling_per_day": round(pace, 1),
                            "days_left": round(st / pace, 1)})
    at_risk.sort(key=lambda r: r["days_left"])

    inbox = dict(q("""SELECT kind, COUNT(*) FROM emails WHERE sent = ? AND kind IN
                      ('return_request','support_question','stock_question') GROUP BY 1""", y.isoformat()))
    lost_y = q("""SELECT COUNT(*), COALESCE(SUM(p.price), 0) FROM lost_sales l JOIN products p ON p.id = l.product_id
                  WHERE day = ?""", y.isoformat())[0]

    alerts = []
    if z_orders <= -4:
        alerts.append({"type": "orders_drop", "detail": f"{orders_y} orders yesterday vs about {round(o_mean)} on a normal "
                       f"{y:%A}; check checkout, payments and the website"})
    if z_orders >= 4:
        alerts.append({"type": "orders_spike", "detail": f"{orders_y} orders yesterday vs about {round(o_mean)} usually"})
    for s in spikes:
        alerts.append({"type": "return_spike", "detail": f"{s['product']} (#{s['product_id']}): {s['return_rate_pct']}% returned vs "
                       f"{s['category_return_rate_pct']}% for other {s['category']}; {s['defective_last_3_weeks']} came back defective "
                       f"in 3 weeks; looks like {s['looks_like']}; top reasons {', '.join(s['top_reasons'])}"})
    for r in at_risk[:5]:
        alerts.append({"type": "stock_risk", "detail": f"{r['product']} (#{r['product_id']}): {r['units_left']} left, selling "
                       f"{r['selling_per_day']}/day, about {r['days_left']} days, nothing on order"})

    return {"today": today.isoformat(), "yesterday": y.isoformat(), "weekday": f"{y:%A}",
            "orders_yesterday": orders_y, "orders_normal_for_weekday": round(o_mean), "orders_z_score": round(z_orders, 1),
            "revenue_yesterday": round(revenue_y), "revenue_normal_for_weekday": round(r_mean),
            "returns_yesterday": returns_y, "refunds_yesterday": round(refunds_y),
            "lost_sales_yesterday_units": lost_y[0], "lost_sales_yesterday_value": round(lost_y[1]),
            "customer_emails_yesterday": inbox, "alerts": alerts,
            "return_spikes": spikes, "stock_at_risk": at_risk[:5]}


SYSTEM = """You write the owner's morning brief for Harbor & Pine, a small online apparel and home-goods shop.
Plain text, under 200 words, for a busy owner. Three short parts:
1. Yesterday: orders and revenue against a normal day for that weekday; returns and refunds.
2. Needs your decision today: one line per alert, most urgent first, each with the action to take.
3. Quiet: one line on what's fine.
Use ONLY numbers that appear in the facts; never compute new ones or round differently. If there are no
alerts, say so plainly. No headings with #, no tables. American English."""


def write(f: dict, writer: str, model: str) -> str:
    user = "FACTS (JSON):\n" + json.dumps(f, indent=1)
    if writer == "claude":
        r = subprocess.run(["claude", "-p", f"{SYSTEM}\n\n{user}", "--no-session-persistence", "--tools", ""],
                           capture_output=True, text=True, timeout=600,
                           env={**__import__("os").environ, "CLAUDE_INVOKED_BY": "business-sim"})
        return r.stdout.strip()
    body = {"model": model, "stream": False, "think": False, "options": {"temperature": 0.3},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())["message"]["content"].strip()


def check_numbers(text: str, f: dict) -> list[str]:
    """Every number in the brief must come from the facts (dates and list numbering excepted)."""
    allowed = set()
    def walk(v):
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, (int, float)):
            allowed.add(abs(float(v)))          # the text's "-0.5" reads as 0.5 below
        elif isinstance(v, str):
            for n in re.findall(r"\d+(?:\.\d+)?", v.replace(",", "")):
                allowed.add(float(n))
    walk(f)
    text = re.sub(r"\b(19|20)\d\d-\d\d-\d\d\b", "", text)          # ISO dates
    text = re.sub(r"(?m)^\s*\d+[.)]\s", "", text)                    # list numbering
    bad = []
    for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text):
        v = float(n.replace(",", ""))
        if v not in allowed and not (v <= 31 and re.search(rf"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.? {int(v)}\b", text)):
            bad.append(n)
    return bad


def grade(text: str, incidents: dict | None, f: dict) -> dict:
    t = text.lower()
    out = {}
    if incidents and incidents.get("defect_batch"):
        pid = incidents["defect_batch"]["product_id"]
        out["caught_bad_batch"] = (f"#{pid}" in t or f"item {pid}" in t) and ("defect" in t or "return" in t)
    if incidents and incidents.get("checkout_outage") == f["yesterday"]:
        out["caught_outage"] = any(w in t for w in ("checkout", "outage", "website", "payment", "down")) and str(f["orders_yesterday"]) in t
    out["alerts_raised_by_facts"] = len(f["alerts"])
    out["stock_risks_mentioned"] = sum(1 for r in f["stock_at_risk"] if f"#{r['product_id']}" in t or f"item {r['product_id']}" in t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--today", required=True)
    ap.add_argument("--writer", choices=["local", "claude", "none"], default="local")
    ap.add_argument("--model", default="qwen3.8:27b")
    a = ap.parse_args()
    db = sqlite3.connect(a.db)
    f = facts(db, date.fromisoformat(a.today))
    inc_file = Path(a.db).parent / "incidents.json"
    incidents = json.loads(inc_file.read_text()) if inc_file.exists() else None
    if a.writer == "none":
        print(json.dumps(f, indent=1))
        return
    text = write(f, a.writer, a.model)
    print(text)
    print("\n---")
    print("numbers not in the facts:", check_numbers(text, f) or "none")
    print("grade:", json.dumps(grade(text, incidents, f)))


if __name__ == "__main__":
    main()
