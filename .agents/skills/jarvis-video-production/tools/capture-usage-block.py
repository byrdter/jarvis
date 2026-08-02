#!/usr/bin/env python3
"""Emit ONE clean, pretty-printed `usage` block for on-screen capture (C2).

    python3 capture-usage-block.py            # pick a representative block
    python3 capture-usage-block.py --big      # one from a large session

WHY: the raw .jsonl line that carries `usage` also carries the MESSAGE CONTENT — your
actual conversation. Screen-recording a raw line would put private text on camera. This
extracts the usage object ALONE, so what is filmed is exactly what the VO describes and
nothing else.
"""
import json, glob, os, sys
ROOT = os.path.expanduser("~/.claude/projects")
big = "--big" in sys.argv
best = None
for f in glob.glob(os.path.join(ROOT, "*", "*.jsonl")):
    for line in open(f, encoding="utf8", errors="ignore"):
        if '"usage"' not in line:
            continue
        try:
            u = (json.loads(line).get("message") or {}).get("usage")
        except Exception:
            continue
        if not isinstance(u, dict):
            continue
        cr = u.get("cache_read_input_tokens") or 0
        # representative = has all four fields non-trivially populated
        if not (u.get("cache_creation_input_tokens") and cr and u.get("output_tokens")):
            continue
        score = cr if big else -abs(cr - 20000)
        if best is None or score > best[0]:
            best = (score, u)
if not best:
    sys.exit("no suitable usage block found")
u = best[1]
clean = {k: u[k] for k in ("input_tokens", "cache_creation_input_tokens",
                           "cache_read_input_tokens", "output_tokens") if k in u}
if "cache_creation" in u:
    clean["cache_creation"] = u["cache_creation"]
print(json.dumps(clean, indent=2))
