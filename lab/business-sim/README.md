# Business simulator (prototype 1)

A fictional online store, Harbor & Pine, run for simulated years in seconds: customers who buy and
quit on realistic statistical patterns, seasonal demand, returns by category, supplier reorders,
stockouts, and every customer touchpoint written as real email in an mbox file. Everything is fictional,
and all addresses use the reserved `.test` domain, so nothing can ever reach a real person.

```
python3 sim.py --days 730            # 2 years in ~25 s -> out/store.db (SQLite) + out/mail.mbox
python3 llm_emails.py --n 4          # local model (Ollama) writes realistic customer emails + agent replies
python3 calibrate.py                 # same statistics on the sim and on UCI Online Retail II (download to out/data/)

# Prototype 2: a support agent works the shop's inbox; a grader checks each answer against policy.
mailpit --smtp 127.0.0.1:1025 --listen 127.0.0.1:8025 --database out/mailpit.db --max 100000   # brew install mailpit
python3 support.py --cases 18 --agent local            # customers write in, the local agent answers, graded
python3 support.py --reuse --agent local --date-tool   # same inbox, lookup does the date math
python3 support.py --reuse --agent claude              # same inbox, Claude as the agent
```

Result on 18 cases: local 27B 15/18 (fails every late return), local + date tool 18/18, Claude 18/18.

```
# First company app: the reorder advisor (advisor.py), replay-tested against the shop's fixed rule.
python3 sim.py --policy advisor      # one store, the advisor decides supplier orders
python3 replay.py                    # 5 stores x 2 years, old rule vs advisor on identical customers (~4 min)
```

Replay result (5 stores, 2 years each): the advisor earns more in all 5, mean +$191K (range +$38K to
+$439K); lost sales down 64% on average, average stock down 40%, at the cost of 3–4x more supplier orders.
Its December stockouts fall 70% in year 2 once it has learned last year's holiday rush.

```
# Second company app: the owner's morning brief (brief.py), tested with planted problems.
python3 sim.py --days 450 --seed 7 --no-mbox --out out/brief/incident --defect-from 2026-02-01 --outage-on 2026-03-09
python3 sim.py --days 450 --seed 7 --no-mbox --out out/brief/normal
python3 brief.py --db out/brief/incident/store.db --today 2026-03-10 --writer local    # or --writer claude / none
```

Result: both the local model and Claude caught all three planted problems (bad batch, checkout outage,
stock risk) with every number traced to the facts; 5 false alarms in 85 days on the normal store.

Findings, design and sources: `jarvis-brain/wiki/concepts/business-simulation.md`.
