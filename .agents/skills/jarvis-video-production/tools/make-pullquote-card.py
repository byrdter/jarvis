#!/usr/bin/env python3
"""
make-pullquote-card.py — cream typographic citation card (1920x1080), verbatim quote + attribution.

WHY THIS EXISTS AS ITS OWN TOOL
Some sources cannot be captured as a document screenshot: reuters.com bot-blocks the scraper, so
`cards/originals/V2-C5.pdf` and `V2-C7.pdf` are 340-character "Access is temporarily restricted"
pages. For those, the typographic pull-quote is the CORRECT first-class output, not a workaround --
the quote is verbatim and the attribution names the outlet, byline and date.

THE BUG THIS PREVENTS
The pull-quotes were previously rendered with `cli-tools/make-text-card.py --bg cream`, whose
headline size is HARDCODED at 112pt with no fitting logic. When a quote overflows 1080px the tool
does not complain -- it just draws past the frame. So whoever made V2-C5 and V2-C7 passed an
ABRIDGED string ending in "......" to force a fit. The result shipped:

  C5 stopped at "...rather than relying......", cutting the clause that completes the definition
     scene 06 exists to teach ("...on 2D data like flat images or text").
  C7 stopped at "...to advance......", cutting the term the beat delivers ("spatial intelligence").

Both cited Reuters accurately and both under-delivered the claim. DOM text never garbles the way
generative video does, but it can be silently truncated at the worst possible place -- which is
quieter and arguably worse, because nothing announces it. It survived a documented verification pass.

So this tool AUTO-FITS by default and NEVER truncates. If a quote cannot fit even at the minimum
size it exits with an error rather than abridging. Fixing the text is a human decision.

  usage:
    make-pullquote-card.py --quote "..." --attribution "..." --out card.png
                           [--size auto|N] [--source-url URL] [--capture-note "..."]
                           [--scene NAME] [--id V2-C5] [--no-sidecar]

Writes <out>.png and, beside it, <out>.json recording the quote, attribution, source URL, render
settings and a verbatim flag -- so a later pass can verify the card against the pixels rather than
against a manifest that merely asserts it.
"""

import argparse, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
CREAM = (244, 241, 234)      # #F4F1EA — the evidence register
INK = (20, 20, 20)
SUB_INK = (70, 70, 70)
GOLD = (201, 164, 90)
RULE_W = 120
MARGIN_Y = 24                # minimum top/bottom breathing room

SERIF_BOLD = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
              "/Library/Fonts/Georgia Bold.ttf"]
SERIF = ["/System/Library/Fonts/Supplemental/Georgia.ttf",
         "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]

SIZE_MAX, SIZE_MIN, SIZE_STEP = 112, 64, 4
SUB_SIZE = 40


def load(cands, size):
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def layout(draw, quote, attribution, size, sub_size=SUB_SIZE):
    """Returns (head_lines, sub_lines, line_h, sub_h, total_h, y0) or None if it does not fit."""
    hf, sf = load(SERIF_BOLD, size), load(SERIF, sub_size)
    max_w = int(W * 0.80)
    head = wrap(draw, quote, hf, max_w)
    sub = wrap(draw, attribution, sf, max_w) if attribution else []
    line_h, sub_h = int(size * 1.18), int(sub_size * 1.30)
    total = len(head) * line_h + 40 + len(sub) * sub_h
    y0 = (H - total) // 2
    if y0 < MARGIN_Y:
        return None
    return head, sub, line_h, sub_h, total, y0, hf, sf


def render(quote, attribution, out, size="auto"):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    if size == "auto":
        chosen = None
        for s in range(SIZE_MAX, SIZE_MIN - 1, -SIZE_STEP):
            lay = layout(probe, quote, attribution, s)
            if lay:
                chosen, used = lay, s
                break
        if not chosen:
            sys.exit(f"ERROR: this quote does not fit at {SIZE_MIN}pt and this tool will NOT "
                     f"truncate it. Shorten the quote deliberately, or split it across two cards.\n"
                     f"  quote length: {len(quote)} chars")
    else:
        used = int(size)
        chosen = layout(probe, quote, attribution, used)
        if not chosen:
            sys.exit(f"ERROR: quote overflows the frame at {used}pt and this tool will NOT truncate. "
                     f"Use --size auto, or shorten the quote deliberately.")

    head, sub, line_h, sub_h, total, y, hf, sf = chosen
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    for ln in head:
        tw = d.textlength(ln, font=hf)
        d.text(((W - tw) // 2, y), ln, font=hf, fill=INK, stroke_width=3, stroke_fill=INK)
        y += line_h
    d.rectangle([(W - RULE_W) // 2, y + 6, (W + RULE_W) // 2, y + 11], fill=GOLD)
    y += 40
    for ln in sub:
        tw = d.textlength(ln, font=sf)
        d.text(((W - tw) // 2, y), ln, font=sf, fill=SUB_INK)
        y += sub_h
    img.save(out, "PNG")
    return used, len(head), total


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quote", required=True, help="VERBATIM. Do not abridge to make it fit.")
    ap.add_argument("--attribution", default="", help="byline, outlet, date")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="auto", help="auto (default) or a point size")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--capture-note", default="")
    ap.add_argument("--scene", default="")
    ap.add_argument("--id", dest="card_id", default="")
    ap.add_argument("--no-sidecar", action="store_true")
    a = ap.parse_args()

    q = a.quote if a.quote.strip().startswith('"') else f'"{a.quote.strip()}"'
    used, nlines, total = render(q, a.attribution, a.out, a.size)
    print(f"  wrote {a.out}  —  {used}pt, {nlines} lines, text block {total}px of {H}")
    if "…" in a.quote or "......" in a.quote:
        print("  \033[33mWARNING: the quote contains an ellipsis. If that is an abridgement made to "
              "fit, undo it — this tool auto-fits and never needs one.\033[0m")

    if not a.no_sidecar:
        side = Path(a.out).with_suffix(".json")
        side.write_text(json.dumps({
            "id": a.card_id or Path(a.out).stem,
            "typographic": True,
            "renderer": f"jarvis-video-production/tools/make-pullquote-card.py --size {used}",
            "quote": a.quote.strip().strip('"'),
            "verbatim": True,
            "abridged": False,
            "attribution": a.attribution,
            "source_url": a.source_url,
            "capture_note": a.capture_note,
            "scene": a.scene,
            "render": {"size_pt": used, "lines": nlines, "block_px": total,
                       "canvas": [W, H], "ground": "#F4F1EA"},
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  wrote {side}")


if __name__ == "__main__":
    main()
