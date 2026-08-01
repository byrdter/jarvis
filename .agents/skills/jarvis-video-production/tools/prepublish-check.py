#!/usr/bin/env python3
"""
Pre-publish craft gate — implements DECISION-RECORD-2026-08-01.md §3.1.

    python3 prepublish-check.py VO.txt --wpm 145        # before recording (cheapest)
    python3 prepublish-check.py VO.txt --runtime 1200   # fixed runtime, derive wpm
    python3 prepublish-check.py caption.vtt             # after render, real timings
    python3 prepublish-check.py VO.txt --wpm 145 --reference   # reference/impl register

WHY THIS EXISTS
    The craft floor was prose in a decision record, which per our own §6 rule is a claim,
    not a check. `teardown.py` measures videos that ALREADY SHIPPED. This measures the
    script before it costs anything to fix.

    It imports NEGATION / LOOP / hits() / parse_vtt() FROM teardown.py on purpose. If the
    pre-publish ruler differed from the one that scored Mackard at 4.0/min and our own
    Agent Harness at 1.3/min, the floor would be meaningless. Same code path or nothing.

VALIDATED 2026-08-01 against teardown.py's own published figures. Same VTTs, same ruler:
    Mackard  WfjGZCuxl-U  73.03x -> 4.0/min (33 hits), 151 wpm   [teardown: 4.0, 151]  MATCH
    Univ.Res u_5erLilDXY  69.61x -> 3.1/min (71 hits), 136 wpm   [teardown: 3.1, 136]  MATCH
    OURS     Tlqe0A8ED8o   8.00x -> 1.3/min (25 hits), 125 wpm   [teardown: 1.3, 125]  MATCH
    On our own video it FAILS exactly the three things the hand teardown found: negation
    1.3/min, only 3 cold-open data points, and all three forbidden phrases.

WHAT IT CANNOT DO -- read before trusting a PASS
  * It cannot see the render. The persistent on-screen spine (§3.1 item 8) is reported
    MANUAL, always. A PASS here is not a finished QC pass; scene-validator.py and
    deadspace-scan.py still gate the build.
  * THE REVERSAL DENSITY HEURISTIC DOES NOT WORK. Tested against two videos with known,
    hand-identified reversals it missed BOTH (Mackard 4.1 vs 4.0 overall = no meaningful
    spike; Universal Resilience 2.3 vs 3.1 = density went DOWN through its own reversal).
    The check survives only because it PRINTS THE CLAUSES in the window -- on Universal
    Resilience those clauses contained the real turn verbatim ("this doesn't mean we can
    never verify an AI's correctness"). The number is noise; the clauses are the evidence.
    Never let this check PASS anything.
  * CARRIED LOOP over-triggers. It matches descriptive "how"/"why" as if it were a named
    question -- on our own video it flagged "changed HOW the industry thinks", which is not
    a loop at all. That is why it is REVIEW and prints the clause: you can only tell an
    opened loop from ordinary usage by reading it.
  * On a plain VO script the timings are SYNTHETIC (even distribution at the given wpm).
    Good enough for density and ordering; the real curve comes from the recorded VO.
  * Proper-noun detection relies on capitalisation, so it works well on an authored script
    and badly on lowercased auto-captions. That is the right way round for this tool.

EXIT CODES  0 = no FAIL   1 = one or more FAIL   2 = bad usage
"""
import os, re, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import teardown as T          # THE RULER. Do not reimplement these.

# --- floor, from DECISION-RECORD-2026-08-01.md §3.1 ---------------------------------
NEG_PER_MIN   = 3.0
HEDGE_MAX     = 0.60          # winners measured 48% (Mackard) and 54% (UR); Noema 66%. n=3, weak.
WPM_BAND      = (135, 150)    # ADVISORY
COLD_OPEN_PTS = 8             # concrete data points in first 45s
RUNTIME_BAND  = (900, 1500)   # 15-25 min
LOOP_WINDOW   = (15, 45)      # a loop must be NAMED in here
LOOP_CARRY    = 30            # ...and not answered within this many seconds

HEDGE = {"but", "however", "actually", "don't", "doesnt", "doesn't"}

FORBIDDEN = [
    r"welcome back", r"today we(?:'| a)re going to", r"in this video",
    r"on this channel", r"before we dive", r"let's dive in",
    r"part (?:one|two|three|\d+) of (?:our|this)", r"three-part series",
    r"in the last video", r"in my last video", r"as i mentioned in",
    r"don't forget to (?:like|subscribe)", r"smash that",
]
# an ANSWER marker landing within LOOP_CARRY seconds of a loop means the loop was SPENT
ANSWER = {"because", "so", "answer", "reason", "turns", "simply", "basically", "means"}


def words_from_text(path, wpm=None, runtime=None):
    """Plain VO script -> [(seconds, word)] with synthetic even timings."""
    raw = open(path, encoding="utf8").read()
    raw = re.sub(r"&[a-z]+;|&#\d+;", " ", raw)
    raw = re.sub(r"^\s*(?:#|//|\[).*$", " ", raw, flags=re.M)   # strip headings/stage dirs
    toks = [w for w in raw.split() if w.strip()]
    if not toks:
        sys.exit("no words found in " + path)
    if runtime:
        dur = float(runtime)
    elif wpm:
        dur = len(toks) / float(wpm) * 60.0
    else:
        sys.exit("plain text needs --wpm or --runtime")
    step = dur / len(toks)
    return [(round(i * step, 2), w) for i, w in enumerate(toks)], dur, True


def load(path, wpm, runtime):
    if path.lower().endswith((".vtt", ".srt")):
        w = T.parse_vtt(path)
        if not w:
            sys.exit("could not parse timings from " + path)
        return w, (runtime or w[-1][0]), False
    return words_from_text(path, wpm, runtime)


DATAPOINT = re.compile(r"\d")
MONEY_PCT = re.compile(r"[$%€£]")


def clean(w):
    return re.sub(r"&[a-z]+;|&#\d+;", "", w)


def concrete_points(words, upto):
    """Count distinct verifiable things: numerals, $/%/currency, and proper nouns.
    Proper noun = capitalised token that is not the first word of a sentence."""
    seg = [(t, w) for t, w in words if t < upto]
    pts, seen = [], set()
    prev_end = True                       # treat first token as sentence-initial
    for _, w in seg:
        core = clean(w).strip("\"'“”‘’(),;:.—-")
        if not core:
            continue
        key = core.lower()
        is_num = bool(DATAPOINT.search(core)) or bool(MONEY_PCT.search(core))
        is_prop = (not prev_end) and core[:1].isupper() and not core.isupper() and len(core) > 2
        if (is_num or is_prop) and key not in seen:
            seen.add(key)
            pts.append(core)
        prev_end = clean(w).endswith((".", "!", "?", ":"))
    return pts


def check(path, wpm_arg, runtime_arg, reference):
    words, dur, synth = load(path, wpm_arg, runtime_arg)
    mins = dur / 60.0
    wpm = len(words) / mins
    rows = []                                   # (status, label, detail)
    def add(st, label, detail): rows.append((st, label, detail))

    # 5 RUNTIME -----------------------------------------------------------------
    ok = RUNTIME_BAND[0] <= dur <= RUNTIME_BAND[1]
    add("PASS" if ok else "FAIL", "5 runtime 15-25 min",
        f"{T.hms(dur)} ({len(words):,} words){' [synthetic]' if synth else ''}")

    # 2 WPM (advisory) ----------------------------------------------------------
    ok = WPM_BAND[0] <= wpm <= WPM_BAND[1]
    add("PASS" if ok else "WARN", "2 wpm 135-150 (advisory)",
        f"{wpm:.0f} wpm" + ("" if ok else "  -- advisory only, does not block"))

    # 1 NEGATION ----------------------------------------------------------------
    nh = T.hits(words, T.NEGATION.split())
    npm = len(nh) / mins if mins else 0
    ok = npm >= NEG_PER_MIN
    add("PASS" if ok else "FAIL", f"1 negation >={NEG_PER_MIN}/min",
        f"{npm:.2f}/min ({len(nh)} hits)   [ours 1.3 | UR 3.1 | Mackard 4.0]")
    if nh:
        hedge = sum(1 for _, term, _ in nh if term in HEDGE) / len(nh)
        ok = hedge <= HEDGE_MAX
        add("PASS" if ok else "REVIEW", "1b hedge share <=60%",
            f"{100*hedge:.0f}% of negation is but/however/actually/don't"
            + ("" if ok else "  -- conversational hedging, not authored negation (Noema was 66%)"))

    # 3 COLD OPEN ---------------------------------------------------------------
    pts = concrete_points(words, T.COLD_OPEN)
    ok = len(pts) >= COLD_OPEN_PTS
    add("PASS" if ok else "FAIL", f"3 >={COLD_OPEN_PTS} data points in first 45s",
        f"{len(pts)} found: " + ", ".join(pts[:12]) + ("…" if len(pts) > 12 else ""))

    # 4 FORBIDDEN ---------------------------------------------------------------
    text = " ".join(w for _, w in words).lower()
    bad = [p for p in FORBIDDEN if re.search(p, text)]
    if reference and bad:
        add("WARN", "4 forbidden phrases",
            f"{len(bad)} found, ALLOWED in --reference register: {bad}")
    else:
        add("PASS" if not bad else "FAIL", "4 forbidden phrases",
            "none" if not bad else f"{bad}  -- §2 DELETE FOREVER")

    # 6 LOOP named early and carried -------------------------------------------
    lh = T.hits(words, T.LOOP.split())
    early = [h for h in lh if LOOP_WINDOW[0] <= h[0] <= LOOP_WINDOW[1]]
    if not early:
        add("FAIL", "6 loop named in 0:15-0:45",
            f"none in window ({len(lh)} loop-openers total, first at "
            + (T.hms(lh[0][0]) if lh else "n/a") + ")")
    else:
        t0, term, i0 = early[0]
        nxt = [w for tt, w in words if t0 < tt <= t0 + LOOP_CARRY]
        spent = any(re.sub(r"[^a-z']", "", w.lower()) in ANSWER for w in nxt[:40])
        add("REVIEW", "6 loop carried (not spent)",
            f"[{T.hms(t0)}] «{term}» -- "
            + ("answer-marker within 30s: likely SPENT. Read it."
               if spent else "no answer-marker within 30s: looks CARRIED. Confirm."))
        for l in T.context(words, [early[0]], cap=1, span=9):
            add("", "", "    " + l)

    # 7 REVERSAL ----------------------------------------------------------------
    lo, hi = dur * T.REVERSAL[0], dur * T.REVERSAL[1]
    win = [h for h in nh if lo <= h[0] <= hi]
    wmin = (hi - lo) / 60.0
    dens = len(win) / wmin if wmin else 0
    add("REVIEW", "7 reversal at 40-55%",
        f"{T.hms(lo)}-{T.hms(hi)}: negation {dens:.2f}/min vs {npm:.2f}/min overall. "
        "DENSITY IS NOT A RELIABLE SIGNAL HERE -- validated 2026-08-01 against two known-good "
        "reversals (Mackard 4.1 vs 4.0, UR 2.3 vs 3.1) and it missed both. READ THE CLAUSES:")
    for l in T.context(words, win[:3], cap=3, span=9):
        add("", "", "    " + l)

    # 8 SPINE -------------------------------------------------------------------
    add("MANUAL", "8 persistent on-screen spine",
        "not text-detectable -- check the beat map / render yourself")

    # report --------------------------------------------------------------------
    W = {"PASS": "\033[32mPASS\033[0m", "FAIL": "\033[31mFAIL\033[0m",
         "WARN": "\033[33mWARN\033[0m", "REVIEW": "\033[36mREVIEW\033[0m",
         "MANUAL": "\033[35mMANUAL\033[0m", "": "      "}
    print(f"\nPRE-PUBLISH CHECK — {os.path.basename(path)}")
    print("=" * 78)
    for st, label, detail in rows:
        if not st and not label:
            print(f"{'':>8}{detail}")
        else:
            print(f"  {W.get(st,st):<14} {label:<34} {detail}")
    fails = sum(1 for s, _, _ in rows if s == "FAIL")
    revs  = sum(1 for s, _, _ in rows if s in ("REVIEW", "MANUAL"))
    print("=" * 78)
    print(f"  {fails} FAIL · {revs} needing your eyes")
    if fails:
        print("  -> does not clear the floor. Cadence flexes; the floor does not.")
    else:
        print("  -> clears the automated floor. REVIEW/MANUAL items are still yours to confirm.")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="Pre-publish craft gate (DECISION-RECORD §3.1)")
    ap.add_argument("path", help="VO script (.txt/.md) or captions (.vtt/.srt)")
    ap.add_argument("--wpm", type=float, help="target wpm, for plain text")
    ap.add_argument("--runtime", type=float, help="runtime in seconds")
    ap.add_argument("--reference", action="store_true",
                    help="reference/implementation register: forbidden phrases warn, not fail "
                         "(the documented Agent Harness exception)")
    a = ap.parse_args()
    if not os.path.exists(a.path):
        sys.exit(2)
    sys.exit(check(a.path, a.wpm, a.runtime, a.reference))


main()
