#!/usr/bin/env python3
"""Make a sample of the simulator's customer emails sound real, then have a "support agent" draft replies.

Both steps run on a local model through Ollama (free, nothing leaves the machine), grounded in the
store database so the agent sees the real order. Times every call, which is the number that decides
how much of a simulation can be LLM-written.

Usage: llm_emails.py [--n 6] [--model qwen3.8:27b]"""
import argparse
import json
import sqlite3
import time
import urllib.request
from pathlib import Path

DB = Path(__file__).parent / "out" / "store.db"


def chat(model, system, user):
    body = {"model": model, "stream": False, "think": False, "options": {"temperature": 0.8},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    t = time.time()
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    return r["message"]["content"].strip(), time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--model", default="qwen3.8:27b")
    a = ap.parse_args()
    db = sqlite3.connect(DB)
    rows = db.execute("""SELECT e.kind, e.body, c.name, c.city, o.id, o.placed, o.delivered, o.subtotal - o.discount
                         FROM emails e JOIN customers c ON c.id = e.customer_id LEFT JOIN orders o ON o.id = e.order_id
                         WHERE e.kind IN ('return_request','support_question','stock_question')
                         ORDER BY RANDOM() LIMIT ?""", (a.n,)).fetchall()
    times = []
    for kind, body, name, city, oid, placed, delivered, total in rows:
        persona = ("You write ONE short email as a real online-shop customer. Plain text, no subject line. "
                   "Vary tone: some polite, some rushed, some annoyed; real people ramble or omit details. "
                   "Keep every fact given; invent nothing about the order.")
        cust, t1 = chat(a.model, persona, f"You are {name} from {city}. Situation (from the shop's records): {body}\n"
                                          f"Order {oid}, placed {placed}, delivered {delivered}, total ${total or 0:.2f}.")
        agent = ("You are the customer-support agent for Lanternwick, an online apparel and home-goods shop. "
                 "Policy: 30-day returns, free return label, refunds within 5 business days of receipt; "
                 "defective or damaged items need a photo; size exchanges are free. Use only the order facts "
                 "given. Reply in under 120 words, warm and specific. Sign as 'Lanternwick Support'.")
        reply, t2 = chat(a.model, agent, f"Order record: #{oid}, placed {placed}, delivered {delivered}, total ${total or 0:.2f}.\n\n"
                                         f"Customer email:\n{cust}")
        times += [t1, t2]
        print(f"=== {kind} · order #{oid} · customer {t1:.1f}s · agent {t2:.1f}s\n--- customer:\n{cust}\n--- agent:\n{reply}\n")
    print(f"{len(times)} LLM calls, mean {sum(times) / len(times):.1f}s each on {a.model}")


if __name__ == "__main__":
    main()
