#!/usr/bin/env python3
"""
motion-scan.py — the DENSITY + BED gate. Run on every scene before Terry sees it.

WHY THIS EXISTS
`deadspace-scan.py` is a RENDER-FAILURE detector (near-black / blown-white frames). It has
never measured motion, and it says so in its own header. So the two rules that matter most to
how this channel LOOKS had no runnable gate at all:

    CONDUIT-VISUAL-SYSTEM.md §7   45-60 change-events/min, no static hold >5s
    CONDUIT-VISUAL-SYSTEM.md §3   every graphic sits over a MOVING PHOTOGRAPHIC BED

Both lived in prose. video-production-standard.md §6 says a gate that isn't a runnable script
does not exist — and on 2026-08-04 that was proven the expensive way: scene S05 shipped to
review with ZERO change events across 51.8s (measured at threshold 0.001, not a typo) and a bed
that was mounted in the DOM, loaded, and rendered as flat black behind 65% opaque panels.
`deadspace-scan` passed it. The author reported "QC clean". Both were true and useless.

    python3 motion-scan.py SCENE.mp4
    python3 motion-scan.py SCENE.mp4 --panels 64,0,448,1080 --panels 500,126,1880,946

WHAT IT CHECKS
  1 DENSITY   change-events/min from a tile-max frame-difference signal (see signal()).
              Measured baselines: strong 56.8 - good 44.0 - weak 28.9. FAIL under 28.9.
  2 STATIC    longest stretch with no detected event. FAIL over 5.0s (the anti-staleness floor).
  3 BED       luma + texture OUTSIDE the declared panel rectangles. A real photographic bed has
              variance; flat fill does not. FAIL if stddev reads as flat.

Pass --panels for each opaque overlay as x,y,x2,y2. With none given it samples the whole frame,
which still catches a dead scene but cannot tell a missing bed from a legitimately full-frame one.
"""
import argparse, subprocess, sys, re, shutil

# CALIBRATED 2026-08-04 against THREE SHIPPED MASTERS, measured with this exact metric:
#   MASTER-ai-layoffs 69.6/min · MASTER-AIDoomed 67.6 · MASTER-AI-DATACENTERS 67.6
#   (their ambient baseline is 2.15-2.60; a static-panel scene sits near 0.20)
# CONDUIT §7's "45-60" does not reproduce on any instrument and is LOWER than what this
# channel actually ships. Do not tune these down to make a scene pass — the whole reason
# this file exists is that a lenient gate passed a scene Terry could see was wrong.
WEAK, GOOD, STATIC_MAX = 55.0, 65.0, 5.0
# CALIBRATED 2026-08-04 against SHIPPED masters, not invented. Measured whole-frame luma:
#   MASTER-ai-layoffs  p10 10  p50 30      MASTER-AIDoomed  p10 11  p50 20
# A bed that reads as a bed sits in that p50 band. The first version of this file used
# mean>=9 — a number pulled from nowhere — and PASSED a scene whose bed Terry could not see
# at all (luma 10.8). If the gate says pass and the eye says black, the gate is wrong.
BED_MIN_STDDEV, BED_MIN_MEAN = 12.0, 20.0
G, R, Y, Z = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def signal(path, fps=10):
    """Per-frame mean-absolute-difference at 10fps, 160x90 grayscale.

    DO NOT go back to ffmpeg's `select=gt(scene,N)`. That metric detects CUTS — it is only
    large when most of the frame changes at once. This channel's whole style is continuous
    motion INSIDE a held frame, which it structurally cannot see: on 2026-08-04 it scored 0
    events on the charts demo (bars growing, 490 dots lighting), the evidence-cards demo and
    the spine-ledger demo. A gate that reads 0 on three visibly-animated references is
    measuring the wrong thing, and trusting it would have been worse than having no gate.
    """
    import tempfile, os, glob
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return None, None
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path,
                        "-vf", f"fps={fps},scale=160:90,format=gray",
                        os.path.join(td, "f%05d.png")], check=True)
        fs = sorted(glob.glob(os.path.join(td, "*.png")))
        arr = [np.asarray(Image.open(f), dtype=np.int16) for f in fs]
    # TILE-MAX, not a whole-frame mean. A frame average dilutes small-area changes into
    # nothing: the spine rail is ~1/25 of the frame, so its 17 documented state changes
    # measured as 1 under a frame mean. Taking the loudest 8x8 tile makes a localized beat
    # register regardless of how much of the screen it occupies.
    T = 8
    d = []
    for i in range(1, len(arr)):
        diff = np.abs(arr[i] - arr[i-1])
        h, w = diff.shape; th, tw = h // T, w // T
        d.append(float(diff[:th*T, :tw*T].reshape(T, th, T, tw).mean(axis=(1, 3)).max()))
    return d, fps


def count_events(d, fps):
    """Discrete visible changes = local peaks in the difference signal.

    A peak is a frame whose delta exceeds both a floor and its local neighbourhood, so a
    slow continuous drift (which is ambient, not an event) does not inflate the count, and a
    chip landing or a bar growing does.
    """
    # CALIBRATED 2026-08-04 against three references with countable beats:
    #   spine-ledger 17 documented -> 15   charts ~18 -> 19   evidence-cards ~16 -> 25
    # Do not retune without re-running that sweep; an uncalibrated gate is worse than none,
    # which is exactly what the first version of this file was.
    import statistics
    if not d: return [], 0.0
    base = statistics.median(d)
    floor = min(max(base * 1.4, 0.6), 4.5)
    ev, i = [], 1
    while i < len(d) - 1:
        if d[i] >= floor and d[i] >= d[i-1] and d[i] >= d[i+1]:
            ev.append(i / fps)
            i += 3                      # one event, not one per frame of its animation
        else:
            i += 1
    return ev, base


def events(path, thresh=None):
    d, fps = signal(path)
    if d is None: return []
    ev, _ = count_events(d, fps)
    return ev



def blank_runs(path, fps=4):
    """Flag stretches with NOTHING substantive on screen: dark frame AND no bright region.
    A dark abstract clip with no artifact/text reads as blank (Terry, 2026-08-04: ":30-:36
    nothing on the screen ... never have a blank screen, never"). A frame is 'blank' when its
    whole-frame mean luma < 16 AND its brightest 8x8 tile < 62 (no lit subject, no cream
    artifact, no white text). Returns list of (start,end,dur) runs >= 1.5s."""
    import tempfile, os, glob
    from PIL import Image
    import numpy as np
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg","-y","-v","error","-i",path,"-vf",
            f"fps={fps},scale=160:90,format=gray",os.path.join(td,"f%05d.png")],check=True)
        fs=sorted(glob.glob(os.path.join(td,"*.png")))
        blank=[]
        # CALIBRATED 2026-08-04 against real S01 frames: a substantive dark-register frame (a
        # gold count-up number, lit servers, a cream artifact) has >=2 tiles brighter than 34;
        # a truly empty dark frame (abstract clip, no subject/text) has <2. Whole-frame mean
        # alone is useless here — the whole channel is dark. Do NOT revert to a maxtile cut.
        for f in fs:
            a=np.asarray(Image.open(f),dtype=float)
            T=8; h,w=a.shape; th,tw=h//T,w//T
            tiles=a[:th*T,:tw*T].reshape(T,th,T,tw).mean(axis=(1,3))
            blank.append(a.mean()<13 and int((tiles>34).sum())<2)
    runs=[]; i=0
    while i<len(blank):
        if blank[i]:
            j=i
            while j<len(blank) and blank[j]: j+=1
            dur=(j-i)/fps
            if dur>=1.5: runs.append((i/fps,j/fps,dur))
            i=j
        else: i+=1
    return runs


def bed_stats(path, panels, dur):
    """Sample frames and measure luma/texture in the regions no panel covers."""
    try:
        from PIL import Image, ImageStat
        import numpy as np
    except ImportError:
        return None
    import tempfile, os, glob
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate((dur * 0.15, dur * 0.5, dur * 0.85)):
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t}", "-i", path,
                            "-frames:v", "1", os.path.join(td, f"f{i}.png")], check=True)
        means, sds = [], []
        for f in sorted(glob.glob(os.path.join(td, "*.png"))):
            a = np.asarray(Image.open(f).convert("L"), dtype=float)
            mask = np.ones(a.shape, dtype=bool)
            for (x, y, x2, y2) in panels:
                mask[y:y2, x:x2] = False
            vals = a[mask]
            if vals.size < 1000:
                return "NO_ROOM"
            means.append(float(vals.mean())); sds.append(float(vals.std()))
        return sum(means) / len(means), sum(sds) / len(sds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--panels", action="append", default=[],
                    help="opaque overlay rect as x,y,x2,y2 — repeatable")
    ap.add_argument("--threshold", type=float, default=0.02)
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("needs ffmpeg")

    dur = duration(a.video)
    d, fps = signal(a.video)
    if d is None:
        sys.exit("needs pillow + numpy")
    ev, base = count_events(d, fps)
    rate = len(ev) / dur * 60 if dur else 0
    # STATIC = the longest stretch with no discrete event. Ambient drift keeps a frame alive
    # but does not discharge the 5s rule — the rule is about something CHANGING.
    gaps = [0.0] + ev + [dur]
    worst, worst_at = 0.0, 0.0
    for i in range(len(gaps) - 1):
        g = gaps[i + 1] - gaps[i]
        if g > worst:
            worst, worst_at = g, gaps[i]

    fails = []
    print(f"\n  {a.video}   {dur:.1f}s\n")

    tag = G + "PASS" + Z if rate >= GOOD else (Y + "THIN" + Z if rate >= WEAK else R + "FAIL" + Z)
    if rate < WEAK: fails.append("density")
    print(f"  {tag}  density   {len(ev):>3} events  {rate:5.1f}/min"
          f"   (weak {WEAK} · good {GOOD} · strong 56.8)   ambient baseline {base:.2f}")

    tag = G + "PASS" + Z if worst <= STATIC_MAX else R + "FAIL" + Z
    if worst > STATIC_MAX: fails.append("static hold")
    print(f"  {tag}  static    longest {worst:5.1f}s at t={worst_at:.1f}s   (floor {STATIC_MAX}s)")

    runs = blank_runs(a.video)
    if runs:
        fails.append("blank screen")
        print(f"  {R}FAIL{Z}  blank     " +
              " ".join(f"{s0:.1f}-{e0:.1f}s" for s0,e0,_ in runs) +
              f"   {R}nothing substantive on screen — never blank{Z}")
    else:
        print(f"  {G}PASS{Z}  blank     no dead/blank stretches")

    panels = [tuple(int(v) for v in p.split(",")) for p in a.panels]
    st = bed_stats(a.video, panels, dur)
    if st is None:
        print(f"  {Y}SKIP{Z}  bed       needs pillow + numpy")
    elif st == "NO_ROOM":
        fails.append("bed")
        print(f"  {R}FAIL{Z}  bed       panels cover the entire frame — no bed can be visible")
    else:
        mean, sd = st
        ok = sd >= BED_MIN_STDDEV and mean >= BED_MIN_MEAN
        if not ok: fails.append("bed")
        print(f"  {G+'PASS'+Z if ok else R+'FAIL'+Z}  bed       "
              f"luma {mean:5.1f}  texture(stddev) {sd:5.1f}"
              f"   (need mean>={BED_MIN_MEAN}, stddev>={BED_MIN_STDDEV})")
        if not ok:
            print(f"        {R}the bed is mounted but not VISIBLE. Being in the DOM is not the"
                  f" rule — being on screen is.{Z}")

    if fails:
        print(f"\n  {R}FAILED: {', '.join(fails)}{Z}   do not show this to Terry\n")
        sys.exit(1)
    print(f"\n  {G}all checks pass{Z}\n")


if __name__ == "__main__":
    main()
