#!/usr/bin/env python3
"""wordlock.py — align a document's word boxes to the VO that reads them.

    python3 wordlock.py boxes.json words.json --key span --from 5 --to 19 -o times.json

Emits one start time per BOX, so a karaoke highlight can light each word as it is
spoken. Written after hand-rolling this five times (17 U.S.C. §109, the EKU signing
bonus, the EKU clawback, the EKU cover letter, the Cote opinion) and getting a
different failure each time.

THE TWO FAILURES THIS EXISTS TO PREVENT
---------------------------------------
1. RUNAWAY MATCH. A token printed on the page but not spoken — "and" where the VO
   breaks the sentence — makes a greedy scan hunt forward and match a LATER identical
   word, swallowing everything between. Bounded lookahead fixes it.
2. LOST START. Bounded lookahead alone then fails from token one, because the quote
   begins somewhere inside the paragraph and the bound never reaches it. So the start
   is found by an UNBOUNDED search for the first few display words, and only the walk
   after it is bounded.

Unmatched boxes (printed but unspoken: "($3,300,000)", "(15)", "and") are interpolated
across their neighbours, which is correct — a number phrase is spoken as one run.
Exit code 1 if the anchor rate is below --min-anchors, because a silently bad
alignment renders as a highlight drifting off its words.
"""
import argparse
import json
import re
import sys

def norm(s):
    """Normalise for comparison. '&' becomes 'and' because that is how it is SPOKEN —
    stripping it to an empty string silently drops the token from seed windows, which
    cost EKU spanA four anchor matches before this was caught."""
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", " and "))


def align(boxes, words, lookahead=5, seed=3):
    disp = [norm(b["t"]) for b in boxes]
    ws = words
    if not disp or not ws:
        sys.exit("error: empty boxes or words")

    # 1. find where the quote starts: an unbounded search for `seed` consecutive
    #    display words. The seed SLIDES, because the first display token is often the
    #    one the transcript will not reproduce — a hyphenated compound the ASR splits
    #    ("digital-first" -> "digital first", "hardcopy" -> "hard copy"). Anchoring on
    #    a fixed first-three window fails outright on those spans.
    start = d_start = None
    for off in range(0, min(len(disp) - seed + 1, 12)):
        seed_toks = [d for d in disp[off:off + seed] if d]
        if len(seed_toks) < seed:
            continue
        for i in range(len(ws)):
            if all(i + k < len(ws) and norm(ws[i + k]["text"]) == seed_toks[k]
                   for k in range(seed)):
                start, d_start = i, off
                break
        if start is not None:
            break
    if start is None:                      # fall back to the first single-token hit
        d_start = 0
        start = next((i for i, w in enumerate(ws) if norm(w["text"]) == disp[0]), 0)

    # 2. walk forward with a BOUNDED window so an unspoken token cannot run away
    times = [None] * len(disp)
    j = start
    for i, d in enumerate(disp[d_start:], start=d_start):
        if not d:
            continue
        hi = min(j + lookahead, len(ws))
        k = j
        while k < hi and norm(ws[k]["text"]) != d:
            k += 1
        if k < hi:
            times[i] = round(ws[k]["start"], 3)
            j = k + 1

    anchors = [i for i, t in enumerate(times) if t is not None]
    if not anchors:
        sys.exit("error: no anchors matched — check the time window and the box text")

    # 3. interpolate the unspoken tokens across their neighbours
    for a, b in zip(anchors, anchors[1:]):
        if b - a > 1:
            for m in range(1, b - a):
                times[a + m] = round(times[a] + (times[b] - times[a]) * m / (b - a), 3)
    for i in range(anchors[0]):
        times[i] = times[anchors[0]]
    for i in range(anchors[-1] + 1, len(times)):
        times[i] = times[anchors[-1]]
    return times, anchors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("boxes")
    ap.add_argument("words")
    ap.add_argument("--key", default="span", help="key holding the box list")
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=1e9)
    ap.add_argument("--offset", type=float, default=0.0,
                    help="subtract from every emitted time (VO time -> scene-local)")
    ap.add_argument("--lookahead", type=int, default=5)
    ap.add_argument("--min-anchors", type=float, default=0.60)
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    bj = json.load(open(a.boxes))
    boxes = bj[a.key] if isinstance(bj, dict) else bj
    words = [w for w in json.load(open(a.words)) if a.t0 <= w["start"] <= a.t1]

    times, anchors = align(boxes, words, a.lookahead)
    rate = len(anchors) / len(boxes)
    mono = all(b >= x for x, b in zip(times, times[1:]))

    print(f"  {len(boxes)} boxes · {len(anchors)} exact anchors ({rate*100:.0f}%) · "
          f"{times[0]:.2f} -> {times[-1]:.2f}s · monotonic={mono}")
    miss = [boxes[i]["t"] for i in range(len(boxes)) if i not in anchors]
    if miss:
        print(f"  interpolated (printed but not spoken): {' '.join(miss)}")

    if not mono:
        sys.exit("FAIL: times are not monotonic — the highlight would jump backwards")
    if rate < a.min_anchors:
        sys.exit(f"FAIL: only {rate*100:.0f}% anchored (need {a.min_anchors*100:.0f}%). "
                 f"Wrong time window, or the VO does not read this span verbatim.")

    out = [round(t - a.offset, 2) for t in times]
    if a.out:
        json.dump(out, open(a.out, "w"))
        print(f"  -> {a.out}")
    else:
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
