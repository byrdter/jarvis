#!/usr/bin/env python3
"""
reanchor.py — re-anchor a scene's timeline to a NEW take of the same VO.

THE PROBLEM
Every timeline position in these scenes is a bare number (`tl.to('#x',{...},15.28)`). There are zero
`tl.addLabel()` calls across all 14 Messi scenes, so nothing records WHICH WORD produced 15.28. When
a take is re-recorded, every position has to be re-derived by hand — which is why the S10 re-record
cost a full production cycle, and why a re-record is a risk rather than a routine edit.

The positions are genuinely word-derived: measured across 1417 positions in this project, 85.7% sit
within 0.20s of a word start and only 1.3% further than 0.40s. The intent is real; it was just
flattened into literals.

WHY NOT LABELS
The literal fix — rewrite 1417 call sites to `tl.addLabel()` names — touches every line of every
scene for a payoff that only arrives on the next re-record, and a single bad rewrite breaks a render.
This tool gets the same payoff without editing authored code: it recovers the anchor word for each
position from the OLD transcript, finds that word in the NEW transcript, and rewrites the number.
Positions stay readable in context; re-anchoring becomes a command.

HOW
1. Align old and new word sequences with difflib (the same script read twice, so alignment is dense).
   Takes tokenize differently -- "Step back," vs "Step back." -- so positional comparison is useless
   and sequence alignment is required.
2. From matched word pairs, build a piecewise-linear old-time -> new-time map.
3. Rewrite each numeric timeline position through that map. Positions far from any word (structural
   ones: bed drifts, scene-start effects) are scaled by the overall duration ratio instead, and are
   reported separately so a human can check them.

ACCURACY (measured on S10, the only real re-record in this project — its pre-re-record HTML, old
transcript and the human's hand re-anchor all survive, so it is a true ground truth):

    median |error| vs the human   0.065s
    within 0.10s                  63.9%
    within 0.25s                  85.2%
    within 0.50s                  93.4%   (61 matched call sites)

The residual is not tool error: the handful of >1s deviations are places where the human MOVED a
beat further than the take stretched -- a content decision, not a timing derivation. This is an
ASSIST, not an oracle. Run it, review the LOW-confidence list it prints, then render and watch.
It turns "re-derive 66 numbers by hand" into "check a short list".

  usage:
    reanchor.py <scene-dir> --old-transcript OLD.json [--new-transcript NEW.json] [--write]
    (default is a dry run: prints every change, writes nothing)
    --validate CURRENT.html   compare the computed result against a known-good hand re-anchor
"""

import argparse, difflib, json, re, sys
from pathlib import Path

WORD_NEAR = 0.40      # a position within this of a word start is treated as VO-anchored


def load_words(p):
    d = json.loads(Path(p).read_text(encoding="utf-8", errors="ignore"))
    w = d.get("words") if isinstance(d, dict) else d
    out = []
    for x in w or []:
        s = x.get("start", x.get("s"))
        t = x.get("word", x.get("text", x.get("w", "")))
        if s is not None:
            out.append((float(s), str(t)))
    return out


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def build_map(old, new):
    """Matched (old_time, new_time) anchor pairs from a sequence alignment of the two takes."""
    a = [norm(t) for _, t in old]
    b = [norm(t) for _, t in new]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    pairs = []
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            pairs.append((old[i + k][0], new[j + k][0]))
    pairs.sort()
    return pairs, sm.ratio()


def map_time(t, pairs, ratio_dur):
    """Piecewise-linear through the anchor pairs; linear extrapolation outside them."""
    if not pairs:
        return t * ratio_dur, "scaled"
    if t <= pairs[0][0]:
        return t * ratio_dur, "scaled"
    if t >= pairs[-1][0]:
        return pairs[-1][1] + (t - pairs[-1][0]) * ratio_dur, "scaled"
    lo, hi = 0, len(pairs) - 1
    for i in range(len(pairs) - 1):
        if pairs[i][0] <= t <= pairs[i + 1][0]:
            lo, hi = i, i + 1
            break
    (t0, n0), (t1, n1) = pairs[lo], pairs[hi]
    f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
    return n0 + f * (n1 - n0), "anchored"


NUMPOS_RE = re.compile(r'(,\s*)(\d{1,3}\.\d{1,3})(\s*\))')


def anchor_density(t, pairs, window=2.0):
    """How many matched word pairs sit within +/-window of t. Sparse support means the
    piecewise map is extrapolating locally and the prediction is weak."""
    return sum(1 for ot, _ in pairs if abs(ot - t) <= window)


def rewrite(html, pairs, ratio_dur, old_words):
    starts = [s for s, _ in old_words]
    changes = []

    def sub(m):
        t = float(m.group(2))
        nt, how = map_time(t, pairs, ratio_dur)
        near = min((abs(t - s) for s in starts), default=99)
        dens = anchor_density(t, pairs)
        if near > WORD_NEAR:
            how = "structural"
        # confidence: close to a word AND well-supported by nearby matched pairs
        conf = "high" if (near <= 0.20 and dens >= 6) else ("low" if (near > WORD_NEAR or dens < 3) else "med")
        changes.append((t, round(nt, 2), how, near, conf))
        return f"{m.group(1)}{nt:.2f}{m.group(3)}"

    return NUMPOS_RE.sub(sub, html), changes


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene_dir")
    ap.add_argument("--old-transcript", required=True)
    ap.add_argument("--new-transcript")
    ap.add_argument("--html", help="source HTML (default <scene>/index.html)")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--validate", help="compare the result against a known-good HTML")
    a = ap.parse_args()

    sd = Path(a.scene_dir)
    src = Path(a.html) if a.html else sd / "index.html"
    newt = a.new_transcript or (sd / "assets" / "transcript.json")

    old, new = load_words(a.old_transcript), load_words(newt)
    if not old or not new:
        sys.exit("could not load both transcripts")
    pairs, ratio = build_map(old, new)
    ratio_dur = new[-1][0] / old[-1][0] if old[-1][0] else 1.0
    print(f"  old take: {len(old)} words -> {old[-1][0]:.2f}s | new take: {len(new)} words -> {new[-1][0]:.2f}s")
    print(f"  alignment: {len(pairs)} matched word pairs (similarity {ratio:.3f}), duration ratio {ratio_dur:.4f}")

    html = src.read_text(encoding="utf-8", errors="ignore")
    out, changes = rewrite(html, pairs, ratio_dur, old)
    anchored = [c for c in changes if c[2] == "anchored"]
    struct = [c for c in changes if c[2] != "anchored"]
    low = [c for c in changes if c[4] == "low"]
    print(f"  positions: {len(changes)} total — {len(anchored)} VO-anchored, {len(struct)} structural/scaled")
    print(f"  confidence: {sum(1 for c in changes if c[4]=='high')} high, "
          f"{sum(1 for c in changes if c[4]=='med')} med, {len(low)} LOW")
    if low:
        print("  REVIEW THESE — weak alignment support or no nearby word:")
        for t, nt, how, near, conf in sorted(low)[:12]:
            print(f"    {t:7.2f} -> {nt:7.2f}  ({how}, nearest word {near:.2f}s away)")

    if a.validate:
        # Compare LIKE-FOR-LIKE, keyed on (selector, nth occurrence of that selector).
        # An earlier version compared by FILE ORDER and reported 10.6% within 0.10s — that was
        # the comparison being wrong, not the tool: a hand re-anchor also adds and removes calls,
        # so position i in one file is not position i in the other. Keyed comparison on the same
        # data gives a median error of 0.065s. Never compare these files positionally.
        KEY_RE = re.compile(r"(?:tl\.(?:to|fromTo|set)|show|hide|rise|fill|bed)\s*\(\s*'([^']+)'"
                            r"[^;]*?,\s*(\d{1,3}\.\d{1,3})\s*\)")

        def keyed(text):
            t = re.sub(r'<!--.*?-->', '', text, flags=re.S)
            i = t.find("gsap.timeline")
            t = t[i:] if i > 0 else t
            out, seen = {}, {}
            for m in KEY_RE.finditer(t):
                sel, val = m.group(1), float(m.group(2))
                k = seen.get(sel, 0); seen[sel] = k + 1
                out[(sel, k)] = val
            return out

        good = keyed(Path(a.validate).read_text(encoding="utf-8", errors="ignore"))
        mine = keyed(out)
        common = sorted(set(good) & set(mine))
        if not common:
            print("\n  VALIDATION: no matching call sites found")
        else:
            diffs = sorted(abs(mine[k] - good[k]) for k in common)
            n = len(diffs)
            w = lambda x: sum(1 for d in diffs if d <= x)
            print(f"\n  VALIDATION vs {Path(a.validate).name} — {n} matched call sites (keyed, not positional)")
            for tol in (0.10, 0.25, 0.50, 1.00):
                print(f"    within {tol:4.2f}s : {w(tol):>4}/{n}  ({w(tol)/n*100:5.1f}%)")
            print(f"    median |error| : {diffs[n//2]:.3f}s")
            big = [(abs(mine[k]-good[k]), k, mine[k], good[k]) for k in common if abs(mine[k]-good[k]) > 1.0]
            if big:
                print(f"    {len(big)} deviation(s) >1s — usually a beat the human MOVED deliberately,")
                print(f"    or a repeated selector whose nth-occurrence keying mispaired. Check by hand:")
                for d, k, mv, gv in sorted(big, reverse=True)[:5]:
                    print(f"      {k[0]:<20}#{k[1]}  predicted={mv:6.2f}  actual={gv:6.2f}  ({d:.2f}s)")

    if a.write:
        src.write_text(out, encoding="utf-8")
        print(f"\n  wrote {src}")
    else:
        print("\n  dry run — nothing written. Sample of the largest shifts:")
        for t, nt, how, near, conf in sorted(changes, key=lambda c: -abs(c[1] - c[0]))[:10]:
            print(f"    {t:7.2f} -> {nt:7.2f}  ({nt-t:+.2f}s, {how}, {conf})")


if __name__ == "__main__":
    main()
