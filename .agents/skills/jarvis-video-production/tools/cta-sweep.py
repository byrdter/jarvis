#!/usr/bin/env python3
"""
cta-sweep — where does the CTA sit, across every build we have on disk?

Companion to narrative-measure.py (which does one video). This walks every
`*/scenes/` directory under a root, reconstructs each build's scene map from its
render durations, and reports where the CTA lands as a percentage of runtime —
plus what scene follows it, which is the part that matters (NARRATIVE-STRUCTURE §7:
a CTA ahead of the verdict interrupts the one thing the viewer stayed for).

    python3 cta-sweep.py [root]        # default: ~/…/Dropbox/jarvis-private
    python3 cta-sweep.py root --full   # also print the scene that follows the CTA

Run 2026-08-02 over 36 builds: every single one placed the CTA between 75.5% and
89.6%, median 84.0%. 29 of the 30 with a dedicated CTA scene had exactly one scene
after it — the verdict. Re-run after the fix; the number should move.

Reads nothing but scene folder names and media durations, so it works on builds
with no transcript.
"""
import os, re, subprocess, sys, glob, statistics as st

DEFAULT_ROOT = os.path.expanduser(
    "~/Library/CloudStorage/Dropbox/jarvis-private")
CTA_DIR = re.compile(r"cta", re.I)


def dur(p):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
        return float(out)
    except Exception:
        return None


def scene_duration(scene_dir):
    rd = os.path.join(scene_dir, "renders")
    if os.path.isdir(rd):
        mp4 = [f for f in os.listdir(rd) if f.endswith(".mp4")]
        if mp4:
            d = dur(os.path.join(rd, sorted(mp4)[-1]))
            if d:
                return d
    for cand in ("assets/avatar.mp4", "assets/avatar-padded.mp4", "assets/vo.wav"):
        p = os.path.join(scene_dir, cand)
        if os.path.exists(p):
            d = dur(p)
            if d:
                return d
    return 0.0


def ts(s):
    return f"{int(s//60)}:{int(s%60):02d}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else DEFAULT_ROOT
    full = "--full" in sys.argv
    rows = []
    for sd in sorted({d for d in glob.glob(root + "/**/scenes", recursive=True)
                      if os.path.isdir(d)}):
        names = sorted(d for d in os.listdir(sd)
                       if os.path.isdir(os.path.join(sd, d)) and re.match(r"^\d", d))
        if len(names) < 4:
            continue
        segs, t = [], 0.0
        for n in names:
            d = scene_duration(os.path.join(sd, n))
            segs.append((n, t, t + d))
            t += d
        if t < 120:
            continue
        proj = sd.replace(root.rstrip("/") + "/", "").split("/hyperframes")[0].split("/heygen")[0]
        cta = next(((n, a, b) for n, a, b in segs if CTA_DIR.search(n)), None)
        rows.append((proj, t, segs, cta))

    rows.sort(key=lambda r: -(r[3][1] / r[1]) if r[3] else 0)
    print(f"{'build':46s} {'run':>6s}  {'CTA scene':16s} {'at':>7s} {'len':>6s}  after")
    print("-" * 112)
    pcts, lens, one_after = [], [], 0
    for proj, t, segs, cta in rows:
        if not cta:
            print(f"{proj[:46]:46s} {ts(t):>6s}  {'— none —':16s} {'':>7s} {'':>6s}  "
                  f"(check the VO — the ask may be inline)")
            continue
        n, a, b = cta
        after = [s for s, _, _ in segs[[x[0] for x in segs].index(n) + 1:]]
        pcts.append(a / t * 100)
        lens.append(b - a)
        if len(after) == 1:
            one_after += 1
        tail = ", ".join(after) if after else "(CTA IS LAST)"
        print(f"{proj[:46]:46s} {ts(t):>6s}  {n[:16]:16s} {a/t*100:6.1f}% {b-a:5.0f}s  "
              f"{tail if full else (tail[:40])}")
    if pcts:
        print(f"\n{len(pcts)} builds with a dedicated CTA scene")
        print(f"  position: min {min(pcts):.1f}% · median {st.median(pcts):.1f}% · "
              f"mean {st.mean(pcts):.1f}% · max {max(pcts):.1f}%")
        print(f"  length  : min {min(lens):.0f}s · median {st.median(lens):.0f}s · "
              f"max {max(lens):.0f}s")
        print(f"  exactly ONE scene after the CTA: {one_after}/{len(pcts)} "
              f"— that scene is normally the verdict")


if __name__ == "__main__":
    main()
