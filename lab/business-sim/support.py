#!/usr/bin/env python3
"""Prototype 2: a support agent works the simulated shop's inbox, and a grader checks every answer.

1. cases:  pick real orders from the simulation and build support situations whose correct handling is
           known from the shop's policy (normal return, defective item, too late, not yet delivered,
           wrong order number). The "truth" never goes to the agent.
2. inbox:  a local model writes each customer's email in their own voice; it is SENT by SMTP to
           support@lanternwick.test on the local Mailpit server (watch it at http://127.0.0.1:8025).
3. agent:  reads unread mail through Mailpit's API, looks up the order in the store database (a tool),
           decides under the policy, and replies by SMTP. Agent = local model or Claude (`--agent claude`).
4. grade:  the agent's decision vs the truth: right action, right refund, no photo asked for when the
           policy doesn't require one. Writes out/grades-<agent>.md.

Usage: support.py [--cases 20] [--agent local|claude] [--model qwen3.8:27b] [--seed 3]
Needs: sim.py run first (out/store.db) and Mailpit on 127.0.0.1:1025/8025."""
import argparse
import json
import random
import re
import smtplib
import sqlite3
import subprocess
import time
import urllib.request
from datetime import date, timedelta
from email.message import EmailMessage
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "out" / "store.db"
API = "http://127.0.0.1:8025/api/v1"
SUPPORT = "support@lanternwick.test"

POLICY = """Lanternwick support policy:
- Returns are accepted within 30 days of DELIVERY. After 30 days, politely decline (no refund).
- Normal returns (doesn't fit, changed mind, not as pictured, arrived late): approve, send a free return
  label, refund the item's price within 5 business days of receiving it. No photo needed.
- Defective or damaged items: within 30 days, ask for a photo before approving. Do not approve yet.
- "Where is my order?" before the delivery date: give the expected delivery date. No refund.
- If the order number isn't found, ask the customer to confirm it. Never guess an order.
- Never promise anything this policy doesn't allow."""

ACTIONS = ["approve_return", "request_photo", "decline_return", "status_update", "ask_order_number"]


# ---------------- model calls ----------------
def local(model, system, user, temperature=0.3):
    body = {"model": model, "stream": False, "think": False, "options": {"temperature": temperature},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())["message"]["content"].strip()


def claude(system, user):
    r = subprocess.run(["claude", "-p", f"{system}\n\n{user}", "--no-session-persistence", "--tools", ""],
                       capture_output=True, text=True, timeout=600,
                       env={**__import__("os").environ, "CLAUDE_INVOKED_BY": "business-sim"})
    return r.stdout.strip()


# ---------------- 1. cases with known answers ----------------
def build_cases(db, n, rng):
    orders = db.execute("""SELECT o.id, c.name, c.email, o.placed, o.delivered, oi.product_id, p.category, oi.unit_price
                           FROM orders o JOIN customers c ON c.id = o.customer_id
                           JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
                           ORDER BY RANDOM() LIMIT ?""", (n * 3,)).fetchall()
    kinds = ["normal", "normal", "defective", "late", "wismo", "bad_number"]
    cases = []
    for i, (oid, name, email, placed, delivered, pid, cat, price) in enumerate(orders[:n]):
        kind = kinds[i % len(kinds)]
        dlv = date.fromisoformat(delivered)
        if kind == "normal":
            today = dlv + timedelta(days=rng.randint(3, 25))
            reason = rng.choice(["doesn't fit", "changed my mind", "not as pictured", "arrived too late for the party"])
            truth = ("approve_return", price)
        elif kind == "defective":
            today = dlv + timedelta(days=rng.randint(2, 20))
            reason = rng.choice(["it arrived broken", "the seam came apart after one wash", "it was damaged in the box"])
            truth = ("request_photo", 0.0)
        elif kind == "late":
            today = dlv + timedelta(days=rng.randint(38, 70))
            reason = rng.choice(["doesn't fit", "changed my mind"])
            truth = ("decline_return", 0.0)
        elif kind == "wismo":
            today = date.fromisoformat(placed) + timedelta(days=1)
            reason = "where is my order? it hasn't arrived"
            truth = ("status_update", 0.0)
        else:
            today = dlv + timedelta(days=rng.randint(3, 20))
            reason = rng.choice(["doesn't fit", "changed my mind"])
            truth = ("ask_order_number", 0.0)
        shown_id = oid + 900000 if kind == "bad_number" else oid
        cases.append(dict(n=i + 1, kind=kind, oid=oid, shown_id=shown_id, name=name, email=email, today=today.isoformat(),
                          item=f"{cat} item {pid}", price=price, reason=reason, truth=truth[0], refund=truth[1]))
    return cases


# ---------------- 2. customers write in ----------------
def send(sender, to, subject, body, headers=None):
    m = EmailMessage()
    m["From"], m["To"], m["Subject"] = sender, to, subject
    for k, v in (headers or {}).items():
        m[k] = v
    m.set_content(body)
    with smtplib.SMTP("127.0.0.1", 1025) as s:
        s.send_message(m)


def customers_write(cases, model):
    persona = ("Write ONE short email body as a real online-shop customer (no subject line, no 'Subject:'). "
               "Vary tone and length; real people are sometimes vague. Mention the order number exactly as given. "
               "Sign with your first name.")
    for c in cases:
        body = local(model, persona, f"You are {c['name']}. Order number {c['shown_id']}, the {c['item']}. "
                                     f"Your situation: {c['reason']}.", temperature=0.9)
        body = re.sub(r"(?im)^subject:.*\n+", "", body)
        send(f"{c['name']} <{c['email']}>", f"Lanternwick Support <{SUPPORT}>", f"Order {c['shown_id']}", body,
             {"X-Sim-Case": str(c["n"]), "X-Sim-Today": c["today"]})


# ---------------- 3. the agent works the inbox ----------------
def get(path):
    return json.loads(urllib.request.urlopen(f"{API}/{path}").read())


DATE_TOOL = False  # --date-tool: the lookup does the date math, so the model doesn't have to


def lookup_order(db, oid, today=None):
    row = db.execute("SELECT id, placed, delivered, subtotal - discount FROM orders WHERE id = ?", (oid,)).fetchone()
    if not row:
        return None
    items = db.execute("""SELECT p.category || ' item ' || p.id, oi.unit_price FROM order_items oi
                          JOIN products p ON p.id = oi.product_id WHERE oi.order_id = ?""", (oid,)).fetchall()
    rec = {"order": row[0], "placed": row[1], "delivery_date": row[2], "total": round(row[3], 2),
           "items": [{"item": i, "price": p} for i, p in items]}
    if DATE_TOOL and today:
        days = (date.fromisoformat(today) - date.fromisoformat(row[2])).days
        rec["delivered_yet"] = days >= 0
        rec["days_since_delivery"] = days if days >= 0 else None
        rec["within_30_day_return_window"] = 0 <= days <= 30
    return rec


def agent_decide(ask, email_text, today, record):
    system = (f"You are the customer-support agent for Lanternwick. Today's date is {today}.\n{POLICY}\n\n"
              "Reply with ONLY a JSON object, no code fence: {\"action\": one of " + json.dumps(ACTIONS) +
              ", \"refund\": number (the refund you are approving now, else 0), \"reply\": \"the email to the customer, under 110 words, "
              "signed Lanternwick Support\"}")
    user = f"Customer email:\n{email_text}\n\nOrder lookup result: {json.dumps(record) if record else 'NOT FOUND'}"
    raw = ask(system, user)
    try:
        return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except ValueError:
        return {"action": "unparseable", "refund": 0, "reply": raw[:300]}


def work_inbox(db, ask, label):
    msgs = get(f"search?query=to:{SUPPORT}%20is:unread&limit=500")["messages"]
    decisions = {}
    for m in msgs:
        full = get(f"message/{m['ID']}")
        hdr = get(f"message/{m['ID']}/headers")
        case_no, today = int(hdr["X-Sim-Case"][0]), hdr["X-Sim-Today"][0]
        text = full["Text"]
        ids = re.findall(r"\b(\d{1,7})\b", m["Subject"] + " " + text)
        record = lookup_order(db, int(ids[0]), today) if ids else None
        t = time.time()
        d = agent_decide(ask, text, today, record)
        d["secs"] = round(time.time() - t, 1)
        decisions[case_no] = d
        send(f"Lanternwick Support <{SUPPORT}>", m["From"]["Address"], f"Re: {m['Subject']}", str(d.get("reply", "")),
             {"X-Sim-Agent": label})
        req = urllib.request.Request(f"{API}/messages", json.dumps({"IDs": [m["ID"]], "Read": True}).encode(),
                                     {"Content-Type": "application/json"}, method="PUT")
        urllib.request.urlopen(req).read()
    return decisions


# ---------------- 4. grade ----------------
def grade(cases, decisions, label):
    rows, ok_n = [], 0
    for c in cases:
        d = decisions.get(c["n"], {"action": "missing", "refund": 0, "reply": ""})
        problems = []
        if d.get("action") != c["truth"]:
            problems.append(f"action {d.get('action')} (should be {c['truth']})")
        try:
            refund = float(d.get("refund") or 0)
        except (TypeError, ValueError):
            refund = -1
        if abs(refund - c["refund"]) > 0.01:
            problems.append(f"refund {refund} (should be {c['refund']})")
        reply = str(d.get("reply", "")).lower()
        asks_photo = "photo" in re.sub(r"\bno (photo|photos|pictures?)\b[^.]*", "", reply)
        if c["truth"] != "request_photo" and asks_photo:
            problems.append("asked for a photo the policy doesn't require")
        ok = not problems
        ok_n += ok
        rows.append(f"| {c['n']} | {c['kind']} | {'✅' if ok else '❌ ' + '; '.join(problems)} | {d.get('secs', '')} |")
    score = f"{ok_n}/{len(cases)}"
    out = HERE / "out" / f"grades-{label}.md"
    out.write_text(f"# Support agent grades: {label}\n\nScore: **{score}**\n\n| Case | Kind | Result | Seconds |\n|---|---|---|---|\n"
                   + "\n".join(rows) + "\n")
    return score, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=18)
    ap.add_argument("--agent", choices=["local", "claude"], default="local")
    ap.add_argument("--model", default="qwen3.8:27b")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--db", default=str(DB), help="store database to draw cases from")
    ap.add_argument("--date-tool", action="store_true", help="order lookup computes days since delivery")
    ap.add_argument("--reuse", action="store_true", help="grade a new agent on the cases already in the inbox")
    a = ap.parse_args()
    global DATE_TOOL
    DATE_TOOL = a.date_tool
    db = sqlite3.connect(a.db)
    rng = random.Random(a.seed)
    cases_file = HERE / "out" / "cases.json"
    if a.reuse:
        cases = json.loads(cases_file.read_text())
        # mark the customers' messages unread again so this agent works the same inbox
        ids = [m["ID"] for m in get(f"search?query=to:{SUPPORT}&limit=500")["messages"]]
        req = urllib.request.Request(f"{API}/messages", json.dumps({"IDs": ids, "Read": False}).encode(),
                                     {"Content-Type": "application/json"}, method="PUT")
        urllib.request.urlopen(req).read()
    else:
        urllib.request.urlopen(urllib.request.Request(f"{API}/messages", method="DELETE")).read()  # fresh inbox
        cases = build_cases(db, a.cases, rng)
        cases_file.write_text(json.dumps(cases, indent=1))
        t = time.time()
        customers_write(cases, a.model)
        print(f"{len(cases)} customer emails written and sent in {time.time() - t:.0f}s")
    ask = (lambda s, u: claude(s, u)) if a.agent == "claude" else (lambda s, u: local(a.model, s, u))
    label = ("claude" if a.agent == "claude" else a.model.replace(":", "-")) + ("+date-tool" if a.date_tool else "")
    t = time.time()
    decisions = work_inbox(db, ask, label)
    print(f"agent ({label}) answered {len(decisions)} emails in {time.time() - t:.0f}s")
    (HERE / "out" / f"decisions-{label}.json").write_text(json.dumps(decisions, indent=1))
    score, out = grade(cases, decisions, label)
    print(f"score {score} -> {out}")


if __name__ == "__main__":
    main()
