#!/usr/bin/env python3
"""feed-legibility.py — will this graphic still READ once a feed shrinks it?

WHY THIS EXISTS
A dense infographic is a great still and a terrible video frame; a great Pinterest pin and a
terrible Facebook post. One measurable variable decides all four cases: **is the type still
resolvable after the platform scales the image to feed width.** Everything else — density,
beauty, how much you like it — is downstream of that.

Eyeballing does not work. You are looking at a 27-inch monitor; the reader is holding a
phone. So this measures.

THE METHOD — OCR recovery
  1. OCR the graphic at native resolution. That is everything it contains.
  2. Downscale to feed width (what the platform actually does), then upscale ×3 before OCR.
     Upsampling adds NO information — it only gives the OCR engine the pixel scale it
     expects, so the test measures the reader's information, not tesseract's DPI quirks.
  3. recovery = words readable at feed size / words readable at native.

Only words at confidence >= 60 and length >= 2 count, at both scales.

WHY OCR AND NOT AN IMAGE METRIC
Three cheaper metrics were tried and all three failed to reproduce human judgment on the
calibration set: local-contrast ink masks (detect glyph EDGES, so thick headline strokes
register as thin fragments — one image's 40px headline measured as 7.5px), normalized local
contrast (better on texture, still edge-based), and round-trip detail survival (dominated by
large shapes, ranked a known-fail above a known-pass). A number that looks authoritative and
does not track reality is worse than no number. OCR measures the actual question.

Tesseract is a generous stand-in for a human: it reads small type better than eyes do. So a
FAIL here is a strong claim — if the engine cannot recover the words, a person will not.
A PASS is the weaker direction, which is why the sheet exists.

⚠ THRESHOLDS ARE CALIBRATED, NOT DERIVED. Fitted to 8 images judged by eye at 430px first.
They reproduce that judgment on 6 of 8 exactly and put the other 2 in the adjacent bucket.
That is a small honest calibration, not a law. Recalibrate if you change decks or width.

⚠ WHAT IT CANNOT MEASURE. Whether the surviving text still carries the MEANING. Some
graphics keep their gestalt when the labels die — a red-X column beside a green-check column
still reads as "bad vs good" with every word gone. That is a human call, which is what
--sheet is for: it renders every graphic at true feed size so the call takes five seconds.

USAGE
  feed-legibility.py IMG [IMG...] [--feed-width 430] [--csv o.csv] [--sheet o.png] [--sort]

REQUIRES  tesseract  (brew install tesseract)
"""

import argparse
import csv
import io
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw

FEED_W = 430          # a feed photo renders at roughly 400-450 CSS px on a phone
OCR_CONF = 60
PASS_AT, MARG_AT = 0.75, 0.55
COLORS = {"PASS": (76, 175, 80), "MARGINAL": (230, 170, 60), "FAIL": (208, 70, 70)}


def ocr_words(img, conf=OCR_CONF):
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f.name)
        r = subprocess.run(["tesseract", f.name, "stdout", "tsv"],
                           capture_output=True, text=True)
    if r.returncode != 0:
        return []
    words = []
    for row in csv.DictReader(io.StringIO(r.stdout), delimiter="\t", quoting=csv.QUOTE_NONE):
        try:
            c = float(row.get("conf") or -1)
        except ValueError:
            continue
        t = (row.get("text") or "").strip()
        if c >= conf and len(t) >= 2:
            words.append(t)
    return words


def score(path, feed_w=FEED_W):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    native = im if W >= 1000 else im.resize((W * 2, H * 2), Image.LANCZOS)
    fh = max(1, int(H * feed_w / W))
    # downscale exactly as the platform does, then upscale for the engine's sake only
    feed = im.resize((feed_w, fh), Image.LANCZOS).resize((feed_w * 3, fh * 3), Image.LANCZOS)

    n_words, f_words = ocr_words(native), ocr_words(feed)
    n, f = len(n_words), len(f_words)

    if n == 0:
        return dict(file=Path(path).name, native=0, feed=f, recovery=1.0,
                    verdict="PASS", note="no text — image-only")

    rec = min(1.0, f / n)
    verdict = "PASS" if rec >= PASS_AT else "MARGINAL" if rec >= MARG_AT else "FAIL"
    note = ""
    if n >= 60 and rec < MARG_AT:
        note = "text-dense — video/Pinterest asset, not a feed post"
    elif n <= 6:
        note = "very little text — verdict is weak, judge by eye"
    return dict(file=Path(path).name, native=n, feed=f, recovery=round(rec, 3),
                verdict=verdict, note=note)


def sheet(rows, paths, out, feed_w=FEED_W, cols=6):
    ims = []
    for r, p in zip(rows, paths):
        im = Image.open(p).convert("RGB")
        ims.append((r, im.resize((feed_w, max(1, int(im.height * feed_w / im.width))),
                                 Image.LANCZOS)))
    rowh = max(i.height for _, i in ims) + 30
    nrows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (feed_w * cols, rowh * nrows), (16, 16, 20))
    d = ImageDraw.Draw(sh)
    for i, (r, im) in enumerate(ims):
        x, y = (i % cols) * feed_w, (i // cols) * rowh
        c = COLORS[r["verdict"]]
        sh.paste(im, (x, y + 30))
        d.rectangle([x, y, x + feed_w - 2, y + 28], fill=c)
        d.text((x + 6, y + 9),
               f"{r['file']}   {r['verdict']}   {int(r['recovery']*100)}%  "
               f"({r['feed']}/{r['native']} words)", fill=(12, 12, 12))
        d.rectangle([x, y + 30, x + feed_w - 2, y + 29 + im.height], outline=c, width=3)
    sh.save(out)
    return sh.size


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--feed-width", type=int, default=FEED_W)
    ap.add_argument("--csv", default="")
    ap.add_argument("--sheet", default="")
    ap.add_argument("--json", dest="js", default="")
    ap.add_argument("--sort", action="store_true", help="best-first")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()

    if not subprocess.run(["which", "tesseract"], capture_output=True).stdout:
        sys.exit("ERROR: tesseract not found. `brew install tesseract`.\n"
                 "  This gate is OCR-based on purpose — see the module docstring for the "
                 "three image metrics that were tried first and did not track reality.")

    paths = [Path(p) for p in a.images
             if not Path(p).name.startswith("._") and Path(p).exists()]
    if not paths:
        sys.exit("ERROR: no readable images")

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        rows = list(ex.map(lambda p: score(p, a.feed_width), paths))

    # Basenames collide across decks (every deck has a 002.png) and every deck's folder is
    # literally called "images", so the immediate parent disambiguates nothing. Walk up to
    # the nearest ancestor that actually names the deck. An ambiguous table is a table
    # nobody can act on.
    def deck(p):
        for anc in p.parents:
            if anc.name and anc.name.lower() not in ("images", "img", "assets", "."):
                return anc.name
        return p.parent.name or "?"

    seen = {}
    for p in paths:
        seen.setdefault(p.name, set()).add(str(p.parent))
    for r, p in zip(rows, paths):
        if len(seen[p.name]) > 1:
            r["file"] = f"{deck(p)[:18]}/{p.name}"
        r["path"] = str(p)

    order = {"PASS": 0, "MARGINAL": 1, "FAIL": 2}
    if a.sort:
        pairs = sorted(zip(rows, paths),
                       key=lambda rp: (order[rp[0]["verdict"]], -rp[0]["recovery"]))
        rows, paths = [x[0] for x in pairs], [x[1] for x in pairs]

    print(f"{'file':<34}{'verdict':<10}{'recov':>7}{'feed':>6}{'native':>8}  note")
    for r in rows:
        print(f"{r['file']:<34}{r['verdict']:<10}{r['recovery']*100:>6.0f}%"
              f"{r['feed']:>6}{r['native']:>8}  {r['note']}")
    t = {v: sum(1 for r in rows if r["verdict"] == v) for v in order}
    print(f"\n  {t['PASS']} PASS · {t['MARGINAL']} MARGINAL · {t['FAIL']} FAIL"
          f"   (feed width {a.feed_width}px)")

    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {a.csv}")
    if a.js:
        Path(a.js).write_text(json.dumps(rows, indent=2) + "\n")
        print(f"  wrote {a.js}")
    if a.sheet:
        print(f"  wrote {a.sheet}  {sheet(rows, paths, a.sheet, a.feed_width)}")


if __name__ == "__main__":
    main()
