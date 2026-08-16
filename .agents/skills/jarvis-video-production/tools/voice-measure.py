#!/usr/bin/env python3
"""voice-measure.py — is this script inside the business-explainer prose register?

    python3 voice-measure.py SCRIPT-v1.md [--json]

WHAT THIS CHECKS, AND WHAT IT CANNOT
------------------------------------
The bands below were measured on 67 Modern MBA transcripts (2023-2026), split by
outcome. The register metrics are CONSTANTS: they do not separate that channel's
winners from its flops. An 18.3x matched pair sits on top of each other on
sentence length, pause rhythm, punch rate, and number framing.

So a PASS here means "this reads like the lane" — a floor, an entry requirement.
It is NOT a performance predictor and must never be used as one. What actually
separated winners from flops in the same corpus was the ANCHOR (consumer-felt:
rho +0.51, ~2.9x median views/day), which is a judgement no script metric can make.

See docs/VOICE-AND-REGISTER.md for the measurement and its limits.
"""
import argparse
import json
import re
import statistics as st
import sys

# (p10, median, p90) from the Modern MBA corpus.
# Sentence-dependent metrics: n=49 punctuated transcripts. Lexical: n=67.
BANDS = {
    "sent_mean":      (15.0, 19.8, 23.0),
    "sent_median":    (13.0, 19.0, 22.0),
    "sent_sd":        (8.6,  9.9,  10.9),
    "short_rate":     (2.0,  4.8,  19.4),
    "long_rate":      (7.8,  14.8, 25.8),
    "punch_per_100s": (1.6,  2.6,  3.7),
    "num_per1k":      (3.0,  5.6,  12.5),   # CHECKABLE only: carries a unit/scale
    "allnum_per1k":   (13.9, 20.7, 32.9),   # every numeric token incl. dates/ordinals
    "num_framed_pct": (72.1, 85.7, 95.2),
    "contrast_per1k": (6.1,  8.5,  10.0),
    "neg_per1k":      (5.5,  8.1,  11.0),
    "hedge_per1k":    (0.4,  1.1,  2.4),
    "absolute_per1k": (5.5,  7.6,  9.5),
    "proper_per1k":   (32.9, 56.2, 92.4),
}

# Ordinary Economics writes in neutral third person by deliberate choice, so the
# pronoun metrics are reported but never failed against Modern MBA's first person.
INFORMATIONAL = {"you_per1k", "we_per1k", "i_per1k", "question_per1k",
                 "first_num_word", "words"}

NUMWORD = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
           r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
           r"thousand|million|billion|trillion|half|double|triple|quarter)")
GLUE = {"and", "point", "a", "of"}

COMPARE = set("""from to than versus vs compared compare against while whereas
more less fewer higher lower up down grew fell rose dropped doubled tripled halved
means meaning which that's thats translates equals roughly about nearly almost only just
under over above below within outside worth costs cost pays paid""".split())

CONTRAST = ["but", "yet", "however", "although", "though", "instead", "actually",
            "in fact", "turns out", "except", "despite", "whereas", "meanwhile",
            "on paper", "in reality", "the problem", "the catch"]
NEG = ["not", "isn't", "isnt", "doesn't", "doesnt", "don't", "dont", "never",
       "no one", "nobody", "nothing", "can't", "cant", "won't", "wont",
       "wasn't", "wasnt", "aren't", "arent", "didn't", "didnt", "hardly", "rarely"]
HEDGE = ["maybe", "perhaps", "might", "could be", "seems", "arguably", "likely",
         "probably", "somewhat", "tends to", "generally", "in some cases", "possibly"]
ABSOLUTE = ["never", "always", "every", "nobody", "no one", "entirely", "completely",
            "simply", "exactly", "the only", "all of", "none of", "everyone", "everything"]

SENT_END = re.compile(r"[.!?]+[\"')\]]*$")
CAP_RE = re.compile(r"^[A-Z][a-zA-Z&.'-]+$")

DROP_LINE = re.compile(r"""
      ^\s*\#            | ^\s*>            | ^\s*[-*_]{3,}\s*$ | ^\s*\|
    | ^\s*`?\[(SCREEN|SPINE|CARD|SFX|MUSIC|B-ROLL|NOTE|TODO)\b
    | ^\s*\*\*[A-Z][^*]{0,40}:\*\*
    | ^\s*\(.*\)\s*$
""", re.X)
INLINE_DROP = [(re.compile(r"`[^`]*`"), " "),
               (re.compile(r"\[(P|SCREEN|SPINE)\]"), " "),
               (re.compile(r"\[([^\]]*)\]\([^)]*\)"), r"\1"),
               (re.compile(r"\*\*|\*|__|_"), ""),
               (re.compile(r"\s+"), " ")]
SECTION = re.compile(r"^\s*#{1,3}\s*(BEAT|ACT|SCENE|SECTION|COLD OPEN)\b", re.I)


def spoken_text(path):
    """Strip everything that is not read aloud."""
    lines = open(path, encoding="utf-8").readlines()
    started = not any(SECTION.search(x) for x in lines)
    out = []
    for line in lines:
        if not started:
            started = bool(SECTION.search(line))
            continue
        if DROP_LINE.search(line):
            continue
        s = line.strip()
        for pat, rep in INLINE_DROP:
            s = pat.sub(rep, s)
        s = s.strip()
        if len(s.split()) >= 3:
            out.append(s)
    return " ".join(out)


def tok_clean(w):
    return re.sub(r"[^\w$%'-]", "", w).lower()


def is_number(w):
    c = tok_clean(w)
    return bool(re.match(r"^\$?\d", c) or re.match(rf"^{NUMWORD}$", c, re.I))


def number_starts(toks):
    """Runs collapse to one number: '160%' and 'one hundred and sixty percent' both count once."""
    idx, i, n = [], 0, len(toks)
    while i < n:
        if is_number(toks[i]):
            idx.append(i)
            i += 1
            while i < n and (is_number(toks[i]) or (tok_clean(toks[i]) in GLUE
                             and i + 1 < n and is_number(toks[i + 1]))):
                i += 1
        else:
            i += 1
    return idx


UNIT = re.compile(r"^(percent|%|dollars?|cents?|million|billion|trillion|thousand|"
                  r"times|points?|basis|bucks?|pounds?|euros?|units?)$", re.I)


def checkable_starts(toks):
    """Numbers that carry a unit or scale — the ones that are evidence.

    'four systems make this hold' and 'the eighteenth of May' are structure, not
    data. Counting them is what inflated the old '33 per 1,000 words' figure.
    """
    out = []
    for i in number_starts(toks):
        j = i
        while j < len(toks) and (is_number(toks[j]) or tok_clean(toks[j]) in GLUE):
            j += 1
        if any("$" in w or "%" in w for w in toks[i:j]):
            out.append(i)
        elif any(UNIT.match(tok_clean(w) or "") for w in toks[j:j + 2]):
            out.append(i)
        elif i > 0 and "$" in toks[i - 1]:
            out.append(i)
    return out


def count_phrases(text, phrases):
    return sum(len(re.findall(r"\b" + re.escape(p) + r"\b", text)) for p in phrases)


def measure(text):
    toks = text.split()
    n = len(toks)
    if n < 200:
        sys.exit("error: fewer than 200 spoken words found — check the script format")
    low = " ".join(toks).lower()
    p1k = lambda x: round(1000.0 * x / n, 1)

    slens, cur = [], 0
    for w in toks:
        cur += 1
        if SENT_END.search(w):
            slens.append(cur)
            cur = 0
    if cur:
        slens.append(cur)
    if n / max(len(slens), 1) > 40:
        sys.exit("error: no sentence punctuation detected — sentence metrics impossible")

    punches = sum(1 for a, b in zip(slens, slens[1:]) if a >= 25 and b <= 8)

    all_idx = number_starts(toks)
    num_idx = checkable_starts(toks)
    framed = sum(1 for i in num_idx
                 if COMPARE & {tok_clean(x) for x in toks[max(0, i - 12): i + 13]})

    initials, k = set(), 0
    for L in slens:
        initials.add(k)
        k += L
    props = sum(1 for i, w in enumerate(toks)
                if i not in initials and CAP_RE.match(w.strip(".,;:!?\"'—")) and w != "I")

    return {
        "words": n,
        "sent_mean": round(st.mean(slens), 1),
        "sent_median": round(st.median(slens), 1),
        "sent_sd": round(st.pstdev(slens), 1),
        "short_rate": round(100.0 * sum(1 for x in slens if x <= 6) / len(slens), 1),
        "long_rate": round(100.0 * sum(1 for x in slens if x >= 30) / len(slens), 1),
        "punch_per_100s": round(100.0 * punches / len(slens), 2),
        "num_per1k": p1k(len(num_idx)),
        "allnum_per1k": p1k(len(all_idx)),
        "num_framed_pct": round(100.0 * framed / len(num_idx), 1) if num_idx else 0.0,
        "contrast_per1k": p1k(count_phrases(low, CONTRAST)),
        "neg_per1k": p1k(count_phrases(low, NEG)),
        "hedge_per1k": p1k(count_phrases(low, HEDGE)),
        "absolute_per1k": p1k(count_phrases(low, ABSOLUTE)),
        "proper_per1k": p1k(props),
        "you_per1k": p1k(count_phrases(low, ["you", "your", "you're", "youre"])),
        "we_per1k": p1k(count_phrases(low, ["we", "our", "us"])),
        "i_per1k": p1k(count_phrases(low, ["i", "my", "me"])),
        "question_per1k": p1k(sum(1 for w in toks if w.endswith("?"))),
        "first_num_word": num_idx[0] if num_idx else n,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    m = measure(spoken_text(a.script))
    if a.json:
        print(json.dumps(m, indent=1))
        return 0

    print(f"\n  {a.script}")
    print(f"  {m['words']} spoken words\n")
    print(f"  {'metric':<17}{'value':>8}   {'band (p10-p90)':<18} verdict")
    print("  " + "-" * 62)

    out = 0
    for k, (lo, med, hi) in BANDS.items():
        v = m[k]
        if v < lo:
            verdict, out = f"BELOW  (med {med})", out + 1
        elif v > hi:
            verdict, out = f"ABOVE  (med {med})", out + 1
        else:
            verdict = "in band"
        print(f"  {k:<17}{v:>8}   {f'{lo}-{hi}':<18} {verdict}")

    print("\n  reported, not gated (channel writes third person by choice):")
    for k in ["you_per1k", "we_per1k", "i_per1k", "question_per1k", "first_num_word"]:
        print(f"  {k:<17}{m[k]:>8}")

    print(f"\n  {len(BANDS) - out}/{len(BANDS)} in band.")
    print("  Reminder: this is a FLOOR check. It does not predict performance —")
    print("  the anchor does. See docs/VOICE-AND-REGISTER.md.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
