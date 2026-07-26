#!/usr/bin/env python3
"""
deadspace-scan.py — RENDER-FAILURE detector (near-black / blown-white frames).

READ THIS BEFORE CHANGING THE THRESHOLDS.

This tool used to be specified as the "dead-space gate": fps=2, 160x90, flag runs >=1.2s where
stddev<13 AND (mean<22 or mean>234). On the deep-navy #0A0E14 register that specification is
WRONG, and not by a little:

    the Messi V2 master's MEDIAN frame luma is 23.5, against a floor of 22.

The threshold sat at the median of the register's own distribution, so it flagged ~half the video
by construction — 28 runs on a finished, good master, including frames confirmed legible by eye
(the World Labs funding chart, the Europe schematic, the Play Time entity record). A gate that
fails a good video gets ignored, which is worse than no gate.

WHAT WAS TRIED, AND RULED OUT (2026-07-26, beads jarvis-tfo0.2)
Labelled set: 8 known-dead frames (the three ghosted-hold beats later fixed, plus the cap-table
header hold and the skeleton-row hold) against 12 known-good frames (including two the old gate
falsely flagged, the Mbappe dossier, and the closing landing card).

  mean luma      WRONG AXIS. Dead frames measured 17.9-21.8; good frames the gate flagged measured
                 13.9-14.3. The dead frames were BRIGHTER than the good ones it rejected.
  edge density   Separated the first labelled set cleanly (dead <=2.9%, good >=4.3%) but collapsed
                 as soon as the dossier and landing cards were added as good examples.
  peak contrast  edge p99 / p99.5 / max / strong-pixel fraction — all overlap.
  beat gaps      Overlap, and MISS the worst case outright: the S12 opening had beats firing
                 continuously for ~7s while its panel content stayed unresolved.

CONCLUSION: the defect those runs stood for is SEMANTIC — "a panel is present whose content has
not resolved yet" — and no single-frame photometric statistic sees it. A held, resolved dossier
card and an unresolved ghosted panel are statistically identical in one frame. That defect is
detected STRUCTURALLY instead, from the build, by `beatmap.py ghosts` (a ghost must resolve within
~1.2s — CONDUIT-VISUAL-SYSTEM.md section 5).

So this tool keeps only the job it can do honestly: catching frames that are actually broken — a
black hole in the render, a blown white flash, a missing asset leaving an empty frame. At the
thresholds below it fires ZERO times on both the pre-fix and post-fix Messi masters (observed luma
range 12.9 to 218.0), and would fire immediately on a genuine failure.

  usage: deadspace-scan.py <file.mp4> [more.mp4 ...] [--fps 3] [--minrun 1.0]
                           [--floor 10] [--ceil 245]
"""

import subprocess, sys, math

W, H = 160, 90
FPS, MIN_RUN = 2.0, 1.2
FLOOR, CEIL = 10.0, 245.0     # near-black / blown-white. NOT a dead-space threshold — see above.


def scan(path, fps=FPS, min_run=MIN_RUN, floor=FLOOR, ceil=CEIL):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf",
                          f"fps={fps},format=gray,scale={W}:{H}", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    n = W * H
    flagged = []
    for i in range(len(raw) // n):
        f = raw[i * n:(i + 1) * n]
        m = sum(f) / n
        if m < floor or m > ceil:
            sd = math.sqrt(sum((b - m) ** 2 for b in f) / n)
            flagged.append((i / fps, m, sd))
    runs, cur = [], None
    for t, m, sd in flagged:
        if cur and abs(t - cur[1] - 1 / fps) < 1e-6:
            cur = (cur[0], t, min(cur[2], m), max(cur[3], m))
        else:
            if cur:
                runs.append(cur)
            cur = (t, t, m, m)
    if cur:
        runs.append(cur)
    return [r for r in runs if (r[1] - r[0]) + 1 / fps >= min_run]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    def opt(name, default):
        return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default

    fps, minrun = opt("--fps", FPS), opt("--minrun", MIN_RUN)
    floor, ceil = opt("--floor", FLOOR), opt("--ceil", CEIL)
    if not args:
        sys.exit(__doc__)
    bad = 0
    for p in args:
        runs = scan(p, fps, minrun, floor, ceil)
        name = p.split("/")[-1]
        if runs:
            bad += len(runs)
            print(f"\033[31m✗ {name}: {len(runs)} render-failure run(s)\033[0m")
            for a, b, lo, hi in runs:
                print(f"    {a:.1f}s → {b + 1/fps:.1f}s  ({b + 1/fps - a:.1f}s)  meanY {lo:.0f}–{hi:.0f}")
        else:
            print(f"\033[32m✓ {name}: no black/blown frames\033[0m")
    if bad:
        print("\nNOTE: this detects RENDER FAILURE only. For the ghosted-hold defect "
              "(a panel present, content unresolved) run: beatmap.py ghosts <scene>")
    sys.exit(1 if bad else 0)
