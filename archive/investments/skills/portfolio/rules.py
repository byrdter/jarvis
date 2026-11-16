#!/usr/bin/env python3
"""Trading rules: record them, monitor them, report what changed.

WHAT THIS IS, AND THE LINE IT KEEPS
    This tool does NOT originate entry or stop prices. It records the rules Terry
    supplies -- from his trending-stock service, from the Asset Revesting stage
    framework, or set by hand -- and then does arithmetic against live prices to
    report what has happened to them. Deciding what to buy and where to place a
    stop stays with Terry; monitoring, measuring and surfacing is the machine's job.

    That split is not only about who is licensed to advise. A rule written down is
    backtestable and auditable; an opaque "recommendation" is neither. If the rule
    is explicit, its hit rate can be measured later -- which is the whole reason to
    have a system rather than a habit.

WHY IT SITS BESIDE portfolio.db
    positions/snapshots record what is OWNED. This records what SHOULD HAPPEN and
    under what condition. A stop that nothing in JARVIS knows about cannot be
    monitored, and cost basis alone never implies a stop.

PRICE-BASED AND EVENT-BASED RULES
    Liquid instruments get price rules (entry / stop / target). Illiquid holdings --
    syndications, private funds -- have no quotable price, so they take event rules
    instead (a capital call, a distribution, a hold-period end). Same ledger, so
    "what needs my attention" is one query across every plate.

USAGE
    rules.py add SNAP --entry 58.40 --stop 52.00 --source "trend service" --plate 01
    rules.py add BNY  --stop 148.00 --status open --note "trailing"
    rules.py list
    rules.py check                 # live prices vs every active rule
    rules.py close SNAP --as stopped --note "gapped through"
"""
from __future__ import annotations
import argparse, json, sqlite3, subprocess, sys
from datetime import datetime
from pathlib import Path

DB = (Path.home() /
      "Library/CloudStorage/Dropbox/jarvis-private/portfolio/portfolio.db")
PRICE_CLI = (Path.home() /
             "Library/CloudStorage/Dropbox/jarvis/cli-tools/jarvis-price")

STATUSES = ("watching", "open", "stopped", "exited", "expired")

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  symbol       TEXT NOT NULL,
  plate        TEXT,
  rule_type    TEXT NOT NULL DEFAULT 'price',   -- price | event
  source       TEXT,                            -- where the rule came from
  signal_date  TEXT,
  entry_price  REAL,
  stop_price   REAL,
  target_price REAL,
  event_desc   TEXT,                            -- for rule_type='event'
  status       TEXT NOT NULL DEFAULT 'watching',
  note         TEXT,
  created_at   TEXT NOT NULL,
  updated_at   TEXT NOT NULL,
  UNIQUE(symbol, signal_date, source)
);
CREATE INDEX IF NOT EXISTS idx_sig_status ON signals(status);
CREATE INDEX IF NOT EXISTS idx_sig_symbol ON signals(symbol);

-- Append-only audit trail. The point of writing rules down is being able to ask
-- later whether they worked; that needs the history, not just current state.
CREATE TABLE IF NOT EXISTS signal_events (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  signal_id  INTEGER NOT NULL REFERENCES signals(id),
  at         TEXT NOT NULL,
  kind       TEXT NOT NULL,       -- created | entry_hit | stop_hit | target_hit | closed
  price      REAL,
  note       TEXT
);
"""


def con():
    if not DB.exists():
        raise SystemExit(f"portfolio store not found: {DB}\nRun import-positions.py first.")
    c = sqlite3.connect(str(DB)); c.executescript(SCHEMA); return c


def now(): return datetime.now().isoformat(timespec="seconds")


def price(symbol: str) -> dict | None:
    """Live indicators from the existing market-data CLI."""
    try:
        r = subprocess.run([str(PRICE_CLI), "indicators", symbol, "--json"],
                           capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def cmd_add(a, c):
    rt = "event" if a.event else "price"
    c.execute("INSERT OR REPLACE INTO signals(symbol, plate, rule_type, source, "
              "signal_date, entry_price, stop_price, target_price, event_desc, "
              "status, note, created_at, updated_at) "
              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (a.symbol.upper(), a.plate, rt, a.source,
               a.date or datetime.now().strftime("%Y-%m-%d"),
               a.entry, a.stop, a.target, a.event, a.status, a.note, now(), now()))
    sid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.execute("INSERT INTO signal_events(signal_id, at, kind, note) VALUES(?,?,?,?)",
              (sid, now(), "created", a.note))
    c.commit()
    bits = [f"entry {a.entry}" if a.entry else "", f"stop {a.stop}" if a.stop else "",
            f"target {a.target}" if a.target else "", a.event or ""]
    print(f"[{sid}] {a.symbol.upper()} {a.status} — " + " · ".join(b for b in bits if b))


def cmd_list(a, c):
    q = "SELECT id,symbol,plate,status,entry_price,stop_price,target_price,source,event_desc FROM signals"
    p = ()
    if not a.all:
        q += " WHERE status IN ('watching','open')"
    q += " ORDER BY status, symbol"
    rows = c.execute(q, p).fetchall()
    if not rows:
        print("No rules recorded. Add one with:  rules.py add SYM --entry X --stop Y")
        return
    print(f"{'ID':>3}  {'SYM':<6} {'PLATE':<5} {'STATUS':<9} {'ENTRY':>9} {'STOP':>9} {'TARGET':>9}  SOURCE")
    for i, s, pl, st, e, stp, t, src, ev in rows:
        f = lambda v: f"{v:,.2f}" if v is not None else "—"
        print(f"{i:>3}  {s:<6} {(pl or '—'):<5} {st:<9} {f(e):>9} {f(stp):>9} {f(t):>9}  {src or ev or ''}")


def cmd_check(a, c):
    rows = c.execute(
        "SELECT id,symbol,status,entry_price,stop_price,target_price FROM signals "
        "WHERE status IN ('watching','open') AND rule_type='price'").fetchall()
    if not rows:
        print("No active price rules to check.")
        return
    print(f"{'SYM':<6} {'LAST':>9} {'STATUS':<9} {'TO STOP':>9} {'TO ENTRY':>9}  NOTE")
    alerts = []
    for sid, sym, st, entry, stop, target in rows:
        d = price(sym)
        if not d or d.get("current_price") is None:
            print(f"{sym:<6} {'no data':>9}")
            continue
        p = d["current_price"]
        to_stop = (p - stop) / stop * 100 if stop else None
        to_entry = (p - entry) / entry * 100 if entry else None
        flag = ""
        if stop and p <= stop:
            flag = "*** AT OR BELOW STOP"
            alerts.append((sid, sym, "stop_hit", p))
        elif st == "watching" and entry and p <= entry:
            flag = "*** AT OR BELOW ENTRY"
            alerts.append((sid, sym, "entry_hit", p))
        elif target and p >= target:
            flag = "*** AT TARGET"
            alerts.append((sid, sym, "target_hit", p))
        fs = lambda v: f"{v:+.1f}%" if v is not None else "—"
        print(f"{sym:<6} {p:>9,.2f} {st:<9} {fs(to_stop):>9} {fs(to_entry):>9}  {flag}")

    for sid, sym, kind, p in alerts:
        c.execute("INSERT INTO signal_events(signal_id, at, kind, price) VALUES(?,?,?,?)",
                  (sid, now(), kind, p))
    c.commit()
    if alerts:
        print(f"\n{len(alerts)} rule(s) triggered — logged to signal_events.")
        print("These are YOUR rules being reported, not recommendations.")


def cmd_close(a, c):
    n = c.execute("UPDATE signals SET status=?, updated_at=?, note=COALESCE(?,note) "
                  "WHERE symbol=? AND status IN ('watching','open')",
                  (a.as_status, now(), a.note, a.symbol.upper())).rowcount
    for (sid,) in c.execute("SELECT id FROM signals WHERE symbol=?", (a.symbol.upper(),)):
        c.execute("INSERT INTO signal_events(signal_id, at, kind, note) VALUES(?,?,?,?)",
                  (sid, now(), "closed", a.note))
    c.commit(); print(f"{a.symbol.upper()}: {n} rule(s) -> {a.as_status}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Record and monitor YOUR trading rules.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add"); p.add_argument("symbol")
    p.add_argument("--entry", type=float); p.add_argument("--stop", type=float)
    p.add_argument("--target", type=float); p.add_argument("--plate")
    p.add_argument("--source"); p.add_argument("--date"); p.add_argument("--note")
    p.add_argument("--event", help="event-based rule (illiquid holdings)")
    p.add_argument("--status", default="watching", choices=STATUSES)
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("list"); p.add_argument("--all", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("check"); p.set_defaults(fn=cmd_check)

    p = sub.add_parser("close"); p.add_argument("symbol")
    p.add_argument("--as", dest="as_status", required=True, choices=STATUSES)
    p.add_argument("--note"); p.set_defaults(fn=cmd_close)

    a = ap.parse_args(); c = con()
    try: a.fn(a, c)
    finally: c.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
