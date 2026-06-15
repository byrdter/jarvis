#!/usr/bin/env python3
"""log_to_ledger.py — append a row to ledger.csv from a rendered invoice JSON.

Stdlib only.

Usage:
    log_to_ledger.py invoices/INV-0001.json
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


LEDGER_COLUMNS = [
    "id",
    "date",
    "client",
    "amount",
    "description",
    "due_date",
    "status",
]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: log_to_ledger.py <path-to-invoice.json>", file=sys.stderr)
        return 2

    invoice_path = Path(argv[1])
    if not invoice_path.is_file():
        print(f"error: not a file: {invoice_path}", file=sys.stderr)
        return 1

    inv = json.loads(invoice_path.read_text())
    skill_root = Path(__file__).resolve().parent.parent
    ledger_path = skill_root / "ledger.csv"

    is_new = not ledger_path.exists()
    first_item_desc = inv["items"][0]["description"] if inv.get("items") else ""

    row = {
        "id": inv["id"],
        "date": inv["date"],
        "client": inv["client"],
        "amount": f"{inv['total']:.2f}",
        "description": first_item_desc,
        "due_date": inv["due_date"],
        "status": inv.get("status", "draft"),
    }

    with ledger_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_COLUMNS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)

    print(f"appended {inv['id']} to {ledger_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
