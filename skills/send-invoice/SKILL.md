---
name: send-invoice
description: Use when the user asks to draft, generate, render, or send an invoice for a client. Handles the full invoice loop end to end — looks up the client, builds the line items from the conversation, renders a PDF from the template, logs the entry to the ledger, and prepares an email body. Triggers on phrases like "send an invoice", "bill the client", "generate an invoice for", "invoice $X to <name>", or any request to produce a billing document.
---

# Send Invoice

The agent's billing-loop skill. One Skill, one procedure: turn a natural-language billing request into a real invoice artifact on disk + a ledger entry + a ready-to-send email.

## Default Position

- **One invoice per invocation.** Multi-client batches require multiple calls.
- **Amount is always in USD** unless the user explicitly states otherwise.
- **Never auto-send.** This skill renders and stages. Sending requires explicit confirmation in the calling session.
- **Every invoice gets a sequential ID** (`INV-NNNN`), monotonic across runs, persisted in the ledger.

## Required Inputs

Extract from the user's request (ask back if missing):

- `client` — client display name (string, required)
- `amount` — total in USD (number, required)
- `description` — what the work was (string, defaults to "Professional services")
- `due_days` — net terms (int, default 14)

## Procedure

1. **Lookup the client.** Confirm the name matches an existing entry in `ledger.csv` (case-insensitive). If new, treat as a fresh client and note it in the run output.

2. **Build the invoice JSON.** Call:

   ```bash
   python3 scripts/build_invoice.py \
     --client "<client>" \
     --amount <amount> \
     --description "<description>" \
     --due-days <due_days>
   ```

   This writes `invoices/INV-NNNN.json` and prints the file path.

3. **Render the PDF.** Call:

   ```bash
   bash scripts/render_pdf.sh invoices/INV-NNNN.json
   ```

   Prints the rendered PDF path (stubbed renderer — real WeasyPrint integration is the next iteration).

4. **Log to the ledger.** Call:

   ```bash
   python3 scripts/log_to_ledger.py invoices/INV-NNNN.json
   ```

   Appends a row to `ledger.csv` with `id, date, client, amount, description, due_date, status`.

5. **Draft the email.** Render `assets/invoice-template.md` with the invoice values and present the rendered email body to the user for review. Do NOT send.

6. **Return a summary** to the user with: invoice ID, PDF path, ledger row, and the staged email body.

## Output Contract

The skill is finished when the agent has produced, in this order:

```
-> matched skill: send-invoice
-> wrote invoices/INV-NNNN.json     OK
-> rendered invoices/INV-NNNN.pdf   OK
-> logged to ledger.csv             OK
OK staged email to <client>  (review and confirm to send)
```

## Files

- `scripts/build_invoice.py` — JSON invoice writer (stdlib only)
- `scripts/render_pdf.sh` — PDF render driver (stub — prints rendered path)
- `scripts/log_to_ledger.py` — append-only ledger writer
- `assets/invoice-template.md` — email + invoice markdown template
- `examples/acme-4200.json` — reference invoice (Acme Corp, $4,200)
- `invoices/` — generated invoices land here
- `ledger.csv` — running log

## Anti-patterns

- Do NOT email the client directly from this skill. Always stage.
- Do NOT pad descriptions with marketing language. The template line item is literal.
- Do NOT renumber `INV-NNNN`. The counter is ledger-derived; once issued, it is final.
