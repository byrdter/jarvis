#!/usr/bin/env python3
"""Dead-space QC gate — citation-card mode. THE citation-mode gate (scene-validator.py is the
determinism gate; both must pass).

Promoted into the skill 2026-07-26. It previously existed only as prose in CITATION-CARD-FORMAT.md
plus an instruction to keep a copy in each project's build-scripts/ — so on the Messi V2 build it had
never run at all, while VISUALS-MAP asserted "must be 0 BEFORE Terry sees anything". A gate that is
not a runnable script does not exist.

CALIBRATION WARNING: the mean<22 floor assumes a lighter base than the deep-navy #0A0E14 register
(luma ~14). Run as specified it flags well-designed, legible frames. See beads jarvis-tfo0.2 — the
floor needs deriving for this register before the output can be read as pass/fail. What it DOES catch
correctly today is the ghosted-hold signature: a panel present with its content not yet revealed.
Spec: CITATION-CARD-FORMAT.md §"QC gate" — sample fps=2, downscale 160x90,
flag any run >=1.2s where stddev<13 AND (mean<22 or mean>234).
Run per-scene AND on the assembled master. Must be 0 runs end-to-end.
  usage: verify-all.py <file.mp4> [more.mp4 ...]      [--fps 3 --minrun 1.0]  (shorts cadence)
"""
import subprocess, sys, math
W, H = 160, 90
FPS, MIN_RUN, SD_MAX, LO, HI = 2.0, 1.2, 13.0, 22.0, 234.0

def scan(path, fps=FPS, min_run=MIN_RUN):
    raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-vf",
                          f"fps={fps},format=gray,scale={W}:{H}","-f","rawvideo","-"],
                         capture_output=True).stdout
    n = W*H
    flagged = []
    for i in range(len(raw)//n):
        f = raw[i*n:(i+1)*n]
        m = sum(f)/n
        sd = math.sqrt(sum((b-m)**2 for b in f)/n)
        if sd < SD_MAX and (m < LO or m > HI):
            flagged.append((i/fps, m, sd))
    runs, cur = [], None
    for t, m, sd in flagged:
        if cur and abs(t - cur[1] - 1/fps) < 1e-6:
            cur = (cur[0], t, min(cur[2], m), max(cur[3], m))
        else:
            if cur: runs.append(cur)
            cur = (t, t, m, m)
    if cur: runs.append(cur)
    return [r for r in runs if (r[1]-r[0]) + 1/fps >= min_run]

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fps = FPS; minrun = MIN_RUN
    if "--fps" in sys.argv:    fps = float(sys.argv[sys.argv.index("--fps")+1])
    if "--minrun" in sys.argv: minrun = float(sys.argv[sys.argv.index("--minrun")+1])
    bad = 0
    for p in args:
        runs = scan(p, fps, minrun)
        name = p.split("/")[-1]
        if runs:
            bad += len(runs)
            print(f"\033[31m✗ {name}: {len(runs)} run(s)\033[0m")
            for a,b,lo,hi in runs:
                print(f"    {a:.1f}s → {b+1/fps:.1f}s  ({b+1/fps-a:.1f}s)  meanY {lo:.0f}–{hi:.0f}")
        else:
            print(f"\033[32m✓ {name}: 0 runs\033[0m")
    sys.exit(1 if bad else 0)
