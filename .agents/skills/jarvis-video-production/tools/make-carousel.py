#!/usr/bin/env python3
"""make-carousel.py — wrap an ordered set of graphics into a LinkedIn document carousel (PDF).

WHY THIS EXISTS
A LinkedIn document post renders a PDF as a swipeable carousel, and it is that platform's
highest-performing format — roughly 600% the engagement of plain text and 2.5x the shares of
image or video posts. A deck of graphics that already exists is therefore a carousel that
already exists, minus the frame.

THE ASPECT PROBLEM, AND WHY THIS OUTPUTS 1:1
Video decks are 16:9. LinkedIn carousels want square or portrait, because a landscape page
renders as a thin strip in feed and loses the scroll. Neither square nor portrait fits 16:9,
so some canvas is always wasted; the question is only how much.

  4:5 (1080x1350): a 1000px-wide graphic occupies 38% of the canvas
  1:1 (1080x1080): the same graphic occupies 48%

1:1 wastes less and is still a full-size LinkedIn format, so it is the default. Override with
--aspect 4:5 if you would rather have the extra feed height and can fill it.

WHAT IT DOES NOT DO
It does not invent per-slide captions. These decks already carry their own headline and
bottom takeaway; a second caption in the frame would restate what is inside the image. The
frame carries only what the image cannot: deck label, position, and the wordmark. If a slide
needs a caption, the slide is the thing to fix.

USAGE
  make-carousel.py --out deck.pdf --title "..." --subtitle "..." \
      --kicker "CLAUDE CODE HOOKS" --cta "..." --cta-sub "..." IMG [IMG...]

Order is argv order. Emits <out>.pdf, a pages/ directory of PNGs, and a contact sheet.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASPECTS = {"1:1": (1080, 1080), "4:5": (1080, 1350), "16:9": (1920, 1080)}

NAVY = (10, 14, 20)
PANEL = (17, 23, 32)
GOLD = (224, 184, 74)
PAPER = (238, 238, 234)
MUTED = (140, 152, 166)
HAIRLINE = (46, 57, 72)

SERIF_B = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
           "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
SERIF = ["/System/Library/Fonts/Supplemental/Georgia.ttf",
         "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/SFNSMono.ttf"]


def font(cands, size):
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def tracked(d, xy, text, f, fill, track=5):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def tracked_w(d, text, f, track=5):
    return sum(d.textlength(c, font=f) for c in text) + track * max(0, len(text) - 1)


def wrap(d, text, f, max_w):
    out = []
    for para in text.split("\n"):
        lines, cur = [], ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        out.extend(lines or [""])
    return out


def fit(d, text, cands, max_w, max_h, hi, lo, leading=1.18, step=3):
    for s in range(hi, lo - 1, -step):
        f = font(cands, s)
        lines = wrap(d, text, f, max_w)
        if any(d.textlength(l, font=f) > max_w for l in lines):
            continue
        if len(lines) * int(s * leading) <= max_h:
            return f, lines, s
    raise SystemExit(f"ERROR: text does not fit at {lo}pt and this tool will not truncate:\n"
                     f"  {text[:90]}...")


def chrome(img, kicker, pos, total, W, H, mark="BYRDDYNASTY"):
    d = ImageDraw.Draw(img)
    fk, fm = font(MONO, 22), font(MONO, 20)
    pad = 54
    tracked(d, (pad, pad), kicker.upper(), fk, GOLD, 5)
    if pos:
        lab = f"{pos:02d} / {total:02d}"
        d.text((W - pad - d.textlength(lab, font=fm), pad + 2), lab, font=fm, fill=MUTED)
    d.rectangle([pad, H - pad - 26, W - pad, H - pad - 25], fill=HAIRLINE)
    mw = tracked_w(d, mark, fm, 3)
    tracked(d, (W - pad - mw, H - pad - 14), mark, fm, MUTED, 3)
    return d


def slide(path, kicker, pos, total, W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = chrome(img, kicker, pos, total, W, H)
    src = Image.open(path).convert("RGB")
    inner = W - 2 * 40
    g = src.resize((inner, max(1, int(src.height * inner / src.width))), Image.LANCZOS)
    top, bottom = 54 + 34, H - 54 - 44
    y = top + max(0, (bottom - top - g.height) // 2)
    d.rectangle([40 - 2, y - 2, 40 + inner + 1, y + g.height + 1], outline=HAIRLINE, width=2)
    img.paste(g, (40, y))
    return img


def cover(title, subtitle, kicker, total, W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = chrome(img, kicker, 0, total, W, H)
    pad = 54
    inner = W - 2 * pad
    ft, tl, _ = fit(d, title, SERIF_B, inner, int(H * 0.46), 108, 46, 1.16)
    fs = font(SERIF, 32)
    sub = wrap(d, subtitle, fs, inner) if subtitle else []
    blk = len(tl) * int(ft.size * 1.16) + (44 + len(sub) * 42 if sub else 0)
    y = pad + 70 + max(0, (H - pad * 2 - 140 - blk) // 3)
    for l in tl:
        d.text((pad, y), l, font=ft, fill=PAPER)
        y += int(ft.size * 1.16)
    d.rectangle([pad, y + 22, pad + 104, y + 27], fill=GOLD)
    y += 60
    for l in sub:
        d.text((pad, y), l, font=fs, fill=MUTED)
        y += 42
    fsw = font(MONO, 24)
    sw = "SWIPE →"
    tracked(d, (pad, H - pad - 90), sw, fsw, GOLD, 6)
    return img


def outro(cta, cta_sub, kicker, total, W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = chrome(img, kicker, 0, total, W, H)
    pad = 54
    inner = W - 2 * pad
    fc, cl, _ = fit(d, cta, SERIF_B, inner, int(H * 0.40), 84, 40, 1.18)
    fs = font(SERIF, 30)
    sub = wrap(d, cta_sub, fs, inner) if cta_sub else []
    blk = len(cl) * int(fc.size * 1.18) + (44 + len(sub) * 40 if sub else 0)
    y = pad + 80 + max(0, (H - pad * 2 - 160 - blk) // 3)
    for l in cl:
        d.text((pad, y), l, font=fc, fill=PAPER)
        y += int(fc.size * 1.18)
    d.rectangle([pad, y + 22, pad + 104, y + 27], fill=GOLD)
    y += 58
    for l in sub:
        d.text((pad, y), l, font=fs, fill=MUTED)
        y += 40
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", required=True, help="output .pdf")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--cta", default="")
    ap.add_argument("--cta-sub", default="")
    ap.add_argument("--aspect", default="1:1", choices=sorted(ASPECTS))
    ap.add_argument("--dpi", type=float, default=150.0)
    a = ap.parse_args()

    W, H = ASPECTS[a.aspect]
    paths = [Path(p) for p in a.images if not Path(p).name.startswith("._")]
    missing = [p for p in paths if not p.exists()]
    if missing:
        raise SystemExit("ERROR: missing images:\n  " + "\n  ".join(str(m) for m in missing))

    total = len(paths)
    pages = [cover(a.title, a.subtitle, a.kicker, total, W, H)]
    for i, p in enumerate(paths, 1):
        pages.append(slide(p, a.kicker, i, total, W, H))
    if a.cta:
        pages.append(outro(a.cta, a.cta_sub, a.kicker, total, W, H))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pdir = out.parent / "pages"
    pdir.mkdir(exist_ok=True)
    for i, pg in enumerate(pages):
        pg.save(pdir / f"{i:02d}.png")
    pages[0].save(out, "PDF", save_all=True, append_images=pages[1:], resolution=a.dpi)

    tw, cols = 260, 6
    ims = [pg.resize((tw, int(tw * H / W))) for pg in pages]
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (tw * cols, ims[0].height * rows), (18, 18, 22))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % cols) * tw, (i // cols) * im.height))
    sheet = out.with_name(out.stem + "-contact.png")
    sh.save(sheet)

    mb = out.stat().st_size / 1e6
    print(f"  {out}  —  {len(pages)} pages, {a.aspect} ({W}x{H}), {mb:.1f} MB")
    print(f"  {pdir}/  —  page PNGs")
    print(f"  {sheet}")
    if mb > 100:
        print("  WARNING: LinkedIn's document limit is 100 MB.")
    # Count PAGES, not content slides. The reader swipes the cover and the outro too, and an
    # earlier deck was labelled "tight" at 13 slides while actually being 15 pages — right at
    # the cliff. Published 2026 benchmarks: 8-12 pages is the engagement/dwell/save sweet
    # spot, high performers run 3-10, and completion drops sharply past ~15.
    n = len(pages)
    if n > 15:
        print(f"  WARNING: {n} pages. Completion drops sharply past ~15. Cut it.")
    elif n > 12:
        print(f"  NOTE: {n} pages — above the 8-12 sweet spot. Justify every page or trim.")
    elif n < 5:
        print(f"  NOTE: {n} pages — thin for a document post; a single image may do better.")
    else:
        print(f"  {n} pages — inside the 8-12 sweet spot.")


if __name__ == "__main__":
    main()
