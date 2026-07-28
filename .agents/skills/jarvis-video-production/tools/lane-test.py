#!/usr/bin/env python3
"""
Test Terry's hypothesis: does NEWS-PEGGED coverage outperform EVERGREEN
on outlier score, at reachable channel sizes?

Two axes, labelled from the title:
  PEG    -- names a specific dated thing (a model, a lab, a paper, a person,
            a public claim). "DeepSeek V4", "o3", "ChatGPT physics result".
  STANCE -- takes a position or poses a paradox, vs reports/explains.
            "Wrong about", "The Biggest Lie", "How did a 27M model beat ChatGPT?"

Cells: PEG+STANCE, PEG+REPORT, EVERGREEN+STANCE, EVERGREEN+REPORT
"""
import csv, os, statistics, sys
from collections import defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else "outliers.csv"

# Our own subscriber count -- set via env so the real number stays out of this
# public repo. Only affects the illustrative "what would that median be for us" line.
OUR_SUBS = int(os.environ.get("BYRDDYNASTY_SUBS", "1000"))

# Named entities = a dated peg. If the title carries one, a viewer could ask
# "when did that happen?" and get an answer.
PEG = [
    "deepseek", "chatgpt", "openai", "gpt", "claude", "anthropic", "gemini",
    "google", "microsoft", "meta", "qwen", "kimi", "nvidia", "amazon", "o3",
    "llama", "mistral", "alphaevolve", "alphafold", "vaultgemma", "coconut",
    "arc-agi", "jepa", "lecun", "glasswing", "mythos", "turboquant", "dspark",
    "scishow", "kurzgesagt", "sora", "grok", "v3.2", "v4", "k2.5", "s1:",
    "transformer", "warp", "cosine", "doordash", "acl 2025", "engram",
]

# Stance markers = the video argues, contradicts, or poses a paradox.
STANCE = [
    "wrong", "lie", "lying", "reality check", "no,", "not ", "isn't", "aren't",
    "don't", "doesn't", "actually", "myth", "illusion", "misread", "stunt",
    "trap", "dumbest", "bad for", "too broken", "problem", "even ", "how did",
    "why can't", "?!", "vs reality", "still not", "never", "already", "biggest",
    "insane", "absurd", "impossible", "death of", "implosion", "irony",
    "deflector", "threaten", "mistake", "just stupid", "we're stupid",
    "was there", "final boss", "can't ", "won't", "may have been wrong",
]


def label(title):
    t = title.lower()
    return (any(k in t for k in PEG), any(k in t for k in STANCE))


def main():
    rows = list(csv.DictReader(open(SRC)))
    for r in rows:
        r["outlier"] = float(r["outlier"])
        r["subs"] = int(r["subs"])
        r["views"] = int(r["views"])

    band = [r for r in rows if r["subs"] <= 300000]
    cells = defaultdict(list)
    for r in band:
        peg, stance = label(r["title"])
        cells[("PEG" if peg else "EVERGREEN", "STANCE" if stance else "REPORT")].append(r)

    print(f"{'cell':>22} {'n':>4} {'median':>8} {'mean':>8} {'max':>8}  {'>=1.0x':>7}")
    order = [("PEG", "STANCE"), ("PEG", "REPORT"), ("EVERGREEN", "STANCE"), ("EVERGREEN", "REPORT")]
    for k in order:
        v = cells[k]
        if not v:
            continue
        o = [x["outlier"] for x in v]
        hits = sum(1 for x in o if x >= 1.0)
        print(f"{k[0] + '+' + k[1]:>22} {len(o):>4} {statistics.median(o):>7.2f}x "
              f"{statistics.mean(o):>7.2f}x {max(o):>7.2f}x {hits:>7}")

    print("\n--- every video >= 1.0x in the band, with its label ---")
    for r in sorted(band, key=lambda r: -r["outlier"]):
        if r["outlier"] < 1.0:
            break
        peg, stance = label(r["title"])
        tag = ("PEG" if peg else "EVERGREEN") + "+" + ("STANCE" if stance else "REPORT")
        print(f"{r['outlier']:6.2f}x {tag:>18}  [{r['channel'][:16]:16}] {r['title'][:68]}")

    # The pure-news channels, for contrast -- these are the ones Terry envies.
    print("\n--- pure news-cycle channels (all sizes) ---")
    news = ["TheAIGRID", "Wes Roth", "Matthew Berman", "The AI Advantage", "AI Explained"]
    for c in news:
        o = [r["outlier"] for r in rows if r["channel"] == c]
        if o:
            subs = next(r["subs"] for r in rows if r["channel"] == c)
            print(f"{c:>18} {subs:>9,} subs  n={len(o):<3} median {statistics.median(o):>5.2f}x  "
                  f"max {max(o):>5.2f}x   -> at OUR_SUBS subs that median is "
                  f"{statistics.median(o) * OUR_SUBS:>5.0f} views")


main()
