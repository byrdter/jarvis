# Business simulator (prototype 1)

A fictional online store, Harbor & Pine, run for simulated years in seconds: customers who buy and
quit on realistic statistical patterns, seasonal demand, returns by category, supplier reorders,
stockouts, and every customer touchpoint written as real email in an mbox file. Everything is fictional,
and all addresses use the reserved `.test` domain, so nothing can ever reach a real person.

```
python3 sim.py --days 730            # 2 years in ~25 s -> out/store.db (SQLite) + out/mail.mbox
python3 llm_emails.py --n 4          # local model (Ollama) writes realistic customer emails + agent replies
```

Findings, design and sources: `jarvis-brain/wiki/concepts/business-simulation.md`.
