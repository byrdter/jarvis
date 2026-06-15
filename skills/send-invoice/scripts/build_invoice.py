#!/usr/bin/env python3
"""build_invoice.py — write a JSON invoice file from CLI flags.

Stdlib only. Lives inside the send-invoice Skill.

Usage:
    build_invoice.py --client "Acme Corp" --amount 4200 \
        [--description "Website redesign, May sprint"] \
        [--due-days 14]

Writes:
    invoices/INV-NNNN.json  (NNNN is monotonic, derived from existing files)

Prints the written path on stdout.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path


def next_invoice_id(invoices_dir: Path) -> str:
    invoices_dir.mkdir(parents=True, exist_ok=True)
    existing = []
    pat = re.compile(r"INV-(\d{4})\.json$")
    for p in invoices_dir.glob("INV-*.json"):
        m = pat.search(p.name)
        if m:
            existing.append(int(m.group(1)))
    n = (max(existing) + 1) if existing else 1
    return f"INV-{n:04d}"


def build_line_items(amount: float, description: str) -> list[dict]:
    return [
        {
            "description": description,
            "quantity": 1,
            "unit_price": round(amount, 2),
            "subtotal": round(amount, 2),
        }
    ]


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Write a JSON invoice file.")
    ap.add_argument("--client", required=True, help="Client display name")
    ap.add_argument("--amount", required=True, type=float, help="Total in USD")
    ap.add_argument(
        "--description",
        default="Professional services",
        help="Line item description",
    )
    ap.add_argument(
        "--due-days", type=int, default=14, help="Net terms in days (default 14)"
    )
    ap.add_argument(
        "--invoices-dir",
        default=None,
        help="Override invoices directory (default: ../invoices relative to script)",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    invoices_dir = (
        Path(args.invoices_dir) if args.invoices_dir else skill_root / "invoices"
    )

    inv_id = next_invoice_id(invoices_dir)
    today = date.today()
    due = today + timedelta(days=args.due_days)

    items = build_line_items(args.amount, args.description)
    total = round(sum(li["subtotal"] for li in items), 2)

    invoice = {
        "id": inv_id,
        "client": args.client,
        "date": today.isoformat(),
        "due_date": due.isoformat(),
        "currency": "USD",
        "items": items,
        "subtotal": total,
        "tax": 0.00,
        "total": total,
        "status": "draft",
    }

    out_path = invoices_dir / f"{inv_id}.json"
    out_path.write_text(json.dumps(invoice, indent=2) + "\n")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
