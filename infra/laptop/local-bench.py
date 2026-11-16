#!/usr/bin/env python3
"""Local model bench: run each Ollama model on the same six everyday JARVIS tasks, time them, and
write the answers side by side to jarvis-brain/lab/local-models/<date>.md for grading.

The tasks are the jobs a local model would take over (summaries, drafting, grounded answers,
triage, extraction, rewriting), not puzzles. Speed numbers come from Ollama's own counters.
Day 1 of the "30 days on a local model" test is this file's first run.

Usage: local-bench.py [model ...]   (default: every model `ollama list` shows, except embeddings)
       local-bench.py --think ...    (let thinking models think; off by default for everyday tasks)"""
import json
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

BRAIN = Path.home() / "code/jarvis-brain"
OUT = BRAIN / "lab/local-models"
API = "http://localhost:11434/api"


def page(rel: str, n: int = 4000) -> str:
    return (BRAIN / rel).read_text()[:n]


TASKS = [
    ("summarize", "Summarize for a busy business owner in exactly 3 plain-English bullets, no jargon:\n\n"
     + page("wiki/people/zubair-trabzada.md", 3500)),
    ("draft", "Write a short email (under 120 words) inviting a regional accounting firm's partners to a "
     "half-day workshop called 'AI for Your Practice, No Coding Required'. Friendly, plain English, "
     "one clear next step. No subject-line fluff."),
    ("grounded", "Answer ONLY from the notes below. If the notes don't say, reply exactly: I don't know.\n"
     "Q1: What time does the morning brief go out?\nQ2: Which cloud provider hosts the server?\n"
     "Q3: What is Terry's favorite restaurant?\n\nNOTES:\n" + page("wiki/projects/jarvis-server.md", 3000)),
    ("triage", "You sort a news inbox for someone who builds AI apps. For each title reply KEEP or SKIP "
     "and a 5-word reason, one per line, numbered.\n1. Claude Code adds background agents\n"
     "2. Celebrity chef opens AI-themed restaurant\n3. Ollama 0.40.17: fixes typo in help text\n"
     "4. MCP spec adds authorization for remote servers\n5. Uncensored Llama merge tops a leaderboard\n"
     "6. OpenAI Agents SDK ships tracing dashboard\n7. Stock market rallies on chip earnings\n"
     "8. Qwen 3.8 27B released with 256K context"),
    ("extract", "Return only JSON with keys name, company, role, budget_usd (number or null), deadline "
     "(YYYY-MM-DD or null) from: 'Hi, this is Maria Lopez, operations director at Lopez & Sons Plumbing. "
     "We'd like a second brain for our 12 staff, budget around eight thousand dollars, ideally live "
     "before March 15, 2027.'"),
    ("rewrite", "Rewrite in American English, keeping the meaning, and list each word you changed: "
     "'Whilst the organisation's programme centres on behavioural analysis, we realised the colour of "
     "the licence labelling was cancelled towards the end of the travelling season.'"),
]


def models() -> list[str]:
    out = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True).stdout
    return [l.split()[0] for l in out.splitlines()[1:] if l.strip() and "embed" not in l]


def ask(model: str, prompt: str, think: bool) -> dict:
    body = {"model": model, "stream": False, "think": think, "options": {"temperature": 0.2},
            "messages": [{"role": "user", "content": prompt}], "keep_alive": "10m"}
    req = urllib.request.Request(f"{API}/chat", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    t0 = time.time()
    r = json.loads(urllib.request.urlopen(req, timeout=900).read())
    r["wall"] = time.time() - t0
    return r


def main(argv) -> int:
    think = "--think" in argv
    picks = [a for a in argv if not a.startswith("--")] or models()
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%H%M")
    out = OUT / f"{date.today().isoformat()}-{stamp}.md"
    rows, answers = [], []
    for m in picks:
        ask(m, "Say OK.", False)  # load the model first so task 1 isn't charged for loading
        ps = json.loads(urllib.request.urlopen(f"{API}/ps").read())
        size = next((x.get("size_vram", x.get("size", 0)) for x in ps.get("models", []) if x["name"] == m), 0)
        for name, prompt in TASKS:
            try:
                r = ask(m, prompt, think)
            except Exception as e:
                answers.append(f"### {m} · {name}\nFAILED: {e}\n")
                continue
            tps = r.get("eval_count", 0) / max(r.get("eval_duration", 1) / 1e9, 1e-9)
            ttft = (r.get("prompt_eval_duration", 0) + r.get("load_duration", 0)) / 1e9
            rows.append(f"| {m} | {name} | {tps:.0f} | {ttft:.1f} | {r['wall']:.1f} | {size / 2**30:.1f} |")
            answers.append(f"### {m} · {name} ({r['wall']:.1f}s)\n\n{r['message']['content'].strip()}\n")
            print(f"{m:16} {name:10} {tps:5.0f} tok/s  first {ttft:4.1f}s  total {r['wall']:5.1f}s", flush=True)
        subprocess.run(["ollama", "stop", m], capture_output=True)
    out.write_text(
        f"# Local model bench, {date.today().isoformat()}\n\n"
        f"Machine: M5 Pro laptop, 64 GB. Engine: Ollama. Thinking: {'on' if think else 'off'}. "
        f"Temperature 0.2. Script: jarvis/infra/laptop/local-bench.py.\n\n"
        "| Model | Task | tok/s | first token s | total s | memory GB |\n|---|---|---:|---:|---:|---:|\n"
        + "\n".join(rows) + "\n\n## Grades\n\n(to fill in)\n\n## Answers\n\n" + "\n".join(answers))
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
