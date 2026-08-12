#!/usr/bin/env python3
"""
shot-census.py — the SHOT-LEVEL half of a teardown.

`teardown.py` pulls a proven video apart by its CAPTIONS: cold open, beat map, loop
openers, pacing of the WORDS. It never looks at a single pixel. This does the other
half — what is actually ON SCREEN, shot by shot, for the whole runtime:

    how many distinct shots · how long each one holds · how many contain PEOPLE ·
    how many are people TALKING · how much is footage vs captured artifact vs
    graphics the channel built itself

WHY IT EXISTS. On 2026-08-12 an estimate of Explorist's footage/graphics mix was made
from 21 sampled frames and was wrong twice over: it missed that graphics are held ~2x
longer than footage (so the runtime share was nearly double the shot share), and it
could not separate CAPTURED artifacts from ORIGINATED ones — the distinction that
decides how much production work a format actually costs. A census fixed both. Sampling
frames to characterise a house style is fine; sampling them to produce a NUMBER is not.

    python3 shot-census.py <url|id>              # download, detect, sheet
    python3 shot-census.py <url|id> --threshold 0.24
    python3 shot-census.py <url|id> --classify classes.txt   # apply labels, report

THE CLASSIFY STEP IS HUMAN AND IS NOT OPTIONAL. This script produces numbered contact
sheets; an agent (or Terry) reads them and writes the labels. There is no detector here
on purpose — OpenCV Haar was tried on 2026-08-12 and put a face ring on a shirt sleeve
and on a shoulder. Detector confidence is not accuracy, and a census built on a bad
detector is worse than an honest sample.

CLASS CODES (write one line per shot: "<shot> <code>", or ranges "12-19 C")
    A  people TALKING to camera — interview, news anchor, keynote, piece-to-camera
    B  people present, NOT talking to camera — b-roll, crowds, archival, workers
    C  live footage, NO people — product, buildings, machinery, landscape, game
    D1 a CAPTURE of something that already existed — article, webpage, filing,
       broadcast graphic, product page, someone else's slide
    D2 a graphic the CHANNEL BUILT — chapter card, text/quote card, logo ident,
       illustration, its own data-viz

Unlabelled shots default to C. Output: shots.json, sheet_NN.jpg, census.csv.
"""
import argparse, json, math, os, re, subprocess, sys, pathlib

G, R, Y, Z = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
NAMES = {"A": "people TALKING (interview/news/keynote)",
         "B": "people present, not talking to camera",
         "C": "live footage, NO people",
         "D1": "capture of an existing artifact",
         "D2": "graphic ORIGINATED by the channel"}


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def vid_id(s):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else s


def download(vid, d):
    out = d / "video.mp4"
    if out.exists():
        return out
    print(f"  downloading {vid} …")
    r = sh(["yt-dlp", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=360]",
            "-o", str(out), f"https://youtu.be/{vid}"])
    if not out.exists():
        sys.exit(f"{R}download failed{Z}\n{r.stderr[-600:]}")
    return out


def duration(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", str(p)]).stdout.strip())


def detect(video, thr, d):
    cf = d / "cuts.txt"
    if not cf.exists():
        print(f"  detecting cuts (threshold {thr}) — this reads the whole file …")
        r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(video), "-filter:v",
                            f"select='gt(scene,{thr})',showinfo", "-f", "null", "-"],
                           capture_output=True, text=True)
        ts = re.findall(r"pts_time:([0-9.]+)", r.stderr)
        cf.write_text("\n".join(ts))
    return [float(x) for x in cf.read_text().split()]


def build_shots(cuts, dur, min_len=0.35):
    edges = [0.0] + cuts + [dur]
    shots = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if b - a < min_len:
            continue
        shots.append(dict(shot=len(shots) + 1, start=round(a, 2),
                          dur=round(b - a, 2), mid=round(a + (b - a) / 2, 2)))
    return shots


def frames(video, shots, d):
    fd = d / "frames"; fd.mkdir(exist_ok=True)
    todo = [s for s in shots if not (fd / f"{s['shot']:04d}.jpg").exists()]
    for n, s in enumerate(todo, 1):
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss",
                        f"{s['mid']:.2f}", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=300:-1", "-y", str(fd / f"{s['shot']:04d}.jpg")],
                       check=False)
        if n % 100 == 0:
            print(f"    {n}/{len(todo)}")
    return fd


def sheets(shots, fd, d, per=48, cols=8):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit(f"{R}needs Pillow: pip install Pillow{Z}")
    TW, TH = 300, 169
    n = math.ceil(len(shots) / per)
    for s in range(n):
        grp = shots[s * per:(s + 1) * per]
        rows = math.ceil(len(grp) / cols)
        im = Image.new("RGB", (cols * (TW + 6) + 6, rows * (TH + 22) + 6), (20, 20, 24))
        dr = ImageDraw.Draw(im)
        for k, sh_ in enumerate(grp):
            r, c = divmod(k, cols)
            f = fd / f"{sh_['shot']:04d}.jpg"
            if not f.exists():
                continue
            im.paste(Image.open(f).resize((TW, TH)), (6 + c * (TW + 6), 6 + r * (TH + 22)))
            dr.text((9 + c * (TW + 6), 6 + r * (TH + 22) + TH + 4),
                    f"{sh_['shot']}  {int(sh_['start']//60)}:{int(sh_['start']%60):02d}"
                    f"  {sh_['dur']:.1f}s", fill=(235, 220, 180))
        im.save(d / f"sheet_{s+1:02d}.jpg", quality=82)
    return n


def parse_classes(path):
    out = {}
    for line in open(path):
        line = line.split("#")[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2:
            continue
        rng, code = parts
        code = code.upper()
        if code not in NAMES:
            continue
        if "-" in rng:
            a, b = rng.split("-")
            for i in range(int(a), int(b) + 1):
                out[i] = code
        else:
            out[int(rng)] = code
    return out


def report(shots, cls):
    for s in shots:
        s["cls"] = cls.get(s["shot"], "C")
    tot, T = len(shots), sum(s["dur"] for s in shots)
    print(f"\n  {tot} shots · {T/60:.1f} min · {60*tot/(T/60):.0f} shots/hour "
          f"({tot/(T/60):.1f} per minute)")
    lens = sorted(s["dur"] for s in shots)
    print(f"  median shot {lens[tot//2]:.1f}s · mean {T/tot:.1f}s · longest {lens[-1]:.1f}s\n")
    print(f"  {'class':44} {'shots':>6} {'%sh':>6} {'time':>8} {'%time':>7}")
    for k in ["A", "B", "C", "D1", "D2"]:
        g = [s for s in shots if s["cls"] == k]
        if not g:
            continue
        sec = sum(s["dur"] for s in g)
        print(f"  {NAMES[k][:44]:44} {len(g):>6} {100*len(g)/tot:>5.1f}% "
              f"{sec:>7.0f}s {100*sec/T:>6.1f}%")

    def band(lab, keys, colour=""):
        g = [s for s in shots if s["cls"] in keys]
        sec = sum(s["dur"] for s in g)
        print(f"  {colour}{lab:44} {len(g):>6} {100*len(g)/tot:>5.1f}% "
              f"{sec:>7.0f}s {100*sec/T:>6.1f}%{Z}")
    print()
    band("any PEOPLE visible (A+B)", ("A", "B"))
    band("real-world FOOTAGE (A+B+C)", ("A", "B", "C"))
    band("REAL MATERIAL (A+B+C+D1)", ("A", "B", "C", "D1"), G)
    band("ORIGINATED by the channel (D2)", ("D2",), Y)
    return shots


def main():
    ap = argparse.ArgumentParser(description="Shot-level census of a video.")
    ap.add_argument("video")
    ap.add_argument("--threshold", type=float, default=0.28,
                    help="ffmpeg scene score. Lower = more cuts. 0.28 default.")
    ap.add_argument("--min-len", type=float, default=0.35,
                    help="merge splits shorter than this (flicker, not cuts)")
    ap.add_argument("--classify", help="file of '<shot|a-b> <A|B|C|D1|D2>' lines")
    ap.add_argument("--outdir")
    a = ap.parse_args()

    vid = vid_id(a.video)
    d = pathlib.Path(a.outdir or f"census-{vid}")
    d.mkdir(parents=True, exist_ok=True)

    video = download(vid, d)
    dur = duration(video)
    cuts = detect(video, a.threshold, d)
    shots = build_shots(cuts, dur, a.min_len)
    json.dump(shots, open(d / "shots.json", "w"))
    print(f"  {len(cuts)} raw cuts → {G}{len(shots)} shots{Z} over {dur/60:.1f} min")

    fd = frames(video, shots, d)
    n = sheets(shots, fd, d)
    print(f"  {n} contact sheet(s) → {d}/sheet_NN.jpg")

    if a.classify:
        shots = report(shots, parse_classes(a.classify))
        import csv
        with open(d / "census.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["shot", "start", "dur", "cls"],
                               extrasaction="ignore")
            w.writeheader(); w.writerows(shots)
        print(f"\n  -> {d}/census.csv")
    else:
        print(f"\n  NEXT: read the sheets, write '<shot> <A|B|C|D1|D2>' lines to a file,")
        print(f"        then re-run with --classify <file>. No detector does this step —")
        print(f"        see the header for why.")


if __name__ == "__main__":
    main()
