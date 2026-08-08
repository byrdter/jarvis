#!/usr/bin/env python3
"""Measure the row and column geometry of a TABLE inside a screen capture.

For any beat where an annotation HUD must lock onto specific rows/cells of a real captured
page. Hand-copied pixel coordinates drift the moment the capture is re-taken; this emits a
geometry JSON the HUD reads instead, so a re-capture is one re-run rather than an edit pass.

    python3 measure-capture-table.py CAPTURE.png OUT.json --x0 1049 --x1 2692 --y0 800

Detects text bands by ink density per scanline (rows) and per column (columns), so it works
on any light-background page without OCR. It does NOT know what the rows MEAN — pair the
output with a hand-authored label map and VERIFY that map against the pixels by cropping the
bands and reading them. Never trust the band order alone.

Emits: {"source":..., "size":[w,h], "x0","x1", "rows":[{i,y0,y1,mid,h}], "cols":[{i,x0,x1}]}
"""
import argparse, json, sys
try:
    from PIL import Image
    import numpy as np
except ImportError:
    sys.exit("needs pillow + numpy:  pip3 install pillow numpy")


def bands(sig, lo, hi, thresh, min_run):
    """contiguous runs where sig > thresh, within [lo,hi)"""
    out, run = [], None
    for i in range(lo, hi):
        if sig[i] > thresh:
            run = i if run is None else run
        else:
            if run is not None and i - run >= min_run:
                out.append((run, i - 1))
            run = None
    if run is not None and hi - 1 - run >= min_run:
        out.append((run, hi - 1))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capture"); p.add_argument("out")
    p.add_argument("--x0", type=int, required=True, help="left edge of the table column")
    p.add_argument("--x1", type=int, required=True, help="right edge of the table column")
    p.add_argument("--y0", type=int, default=0,  help="start scanning below this y")
    p.add_argument("--y1", type=int, default=0,  help="stop at this y (0 = image height)")
    p.add_argument("--ink", type=int, default=140, help="pixel < this counts as ink")
    a = p.parse_args()

    im = Image.open(a.capture).convert("L")
    W, H = im.size
    y1 = a.y1 or H
    arr = np.asarray(im, dtype=np.int16)
    strip = arr[:, a.x0:a.x1]

    rows = [{"i": i, "y0": int(r0), "y1": int(r1), "mid": int((r0 + r1) // 2),
             "h": int(r1 - r0)}
            for i, (r0, r1) in enumerate(bands((strip < a.ink).sum(axis=1), a.y0, y1, 3, 8))]

    # columns: measure only inside the detected rows, so page prose above/below can't leak in
    if rows:
        ry0, ry1 = rows[0]["y0"], rows[-1]["y1"]
        colink = (arr[ry0:ry1, :] < a.ink).sum(axis=0)
        cols = [{"i": i, "x0": int(c0), "x1": int(c1)}
                for i, (c0, c1) in enumerate(bands(colink, a.x0, a.x1, 0, 20))]
    else:
        cols = []

    geo = {"source": a.capture, "size": [W, H], "x0": a.x0, "x1": a.x1,
           "rows": rows, "cols": cols}
    json.dump(geo, open(a.out, "w"), indent=1)
    print(f"{a.capture}  {W}x{H}")
    print(f"  {len(rows)} row bands, {len(cols)} column bands -> {a.out}")
    for r in rows:
        print(f"    row {r['i']:>2}  y {r['y0']:>5}-{r['y1']:<5} mid {r['mid']:>5}  h {r['h']:>3}")
    for c in cols:
        print(f"    col {c['i']:>2}  x {c['x0']:>5}-{c['x1']:<5} w {c['x1']-c['x0']:>4}")
    print("\n  VERIFY the semantic mapping by cropping these bands and READING them.")


if __name__ == "__main__":
    main()
