# INVOICE {{id}}

**Bill to:** {{client}}
**Date:** {{date}}
**Due:** {{due_date}}

---

| Description | Qty | Unit | Subtotal |
|---|---:|---:|---:|
| {{description}} | 1 | ${{amount}} | ${{amount}} |

---

**Total due: ${{amount}} USD**

---

## Email body

Subject: Invoice {{id}} — {{client}}

Hi {{client}},

Please find invoice **{{id}}** attached, dated **{{date}}**, in the amount of
**${{amount}} USD**, net {{due_days}} (due **{{due_date}}**).

For: {{description}}.

Reply to this thread with any questions. Thanks for the work.

— Terry
