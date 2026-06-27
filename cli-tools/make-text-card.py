#!/usr/bin/env python3
"""
HyperFrames-style text card generator (1920x1080 PNG).
Large serif headline + optional kicker/subtitle, on a dark background or over a
dimmed image. Matches the original master's concept-card register
(dark, serif, gold/green accents).

Usage:
  make-text-card.py --headline "Most companies are drifting" \
    --sub "into one model — without deciding" \
    --bg image:/path/office.jpg --dim 0.78 --out card.png
  make-text-card.py --headline "Who's right?" --sub "Often — both." --bg dark --out card.png
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
DARK = (13, 17, 23)
CREAM = (244, 241, 234)
GOLD = (201, 164, 90)

SERIF_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
]
SANS_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Futura.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

def load_font(cands, size):
    for c in cands:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--bg", default="dark", help="dark | cream | image:/path")
    ap.add_argument("--dim", type=float, default=0.78, help="image dim 0..1")
    ap.add_argument("--accent", default="gold")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    if a.bg.startswith("image:"):
        p = a.bg.split(":",1)[1]
        img = Image.open(p).convert("RGB")
        # cover-fit to 1920x1080
        scale = max(W/img.width, H/img.height)
        img = img.resize((int(img.width*scale), int(img.height*scale)), Image.LANCZOS)
        x = (img.width-W)//2; y=(img.height-H)//2
        img = img.crop((x,y,x+W,y+H))
        img = img.filter(ImageFilter.GaussianBlur(6))
        # dim toward dark
        dark = Image.new("RGB",(W,H),DARK)
        img = Image.blend(img, dark, a.dim)
        base = img
    elif a.bg == "cream":
        base = Image.new("RGB",(W,H),CREAM)
    else:
        base = Image.new("RGB",(W,H),DARK)

    draw = ImageDraw.Draw(base)
    text_color = (238,238,238) if a.bg!="cream" else (20,20,20)

    head_font = load_font(SERIF_CANDIDATES, 92)
    sub_font  = load_font(SERIF_CANDIDATES, 54)
    kick_font = load_font(SANS_CANDIDATES, 30)

    max_w = int(W*0.74)
    head_lines = wrap(draw, a.headline, head_font, max_w)
    sub_lines  = wrap(draw, a.sub, sub_font, max_w) if a.sub else []

    # vertical layout, centered
    line_h = 110
    sub_h  = 70
    total = len(head_lines)*line_h + (len(sub_lines)*sub_h if sub_lines else 0)
    if a.kicker: total += 60
    y = (H - total)//2

    if a.kicker:
        kt = a.kicker.upper()
        # letter-spaced kicker
        spaced = "  ".join(list(kt.replace(" ","   ")))
        kw = draw.textlength(spaced, font=kick_font)
        draw.text(((W-kw)//2, y), spaced, fill=GOLD, font=kick_font)
        y += 60

    for ln in head_lines:
        tw = draw.textlength(ln, font=head_font)
        draw.text(((W-tw)//2, y), ln, fill=text_color, font=head_font)
        y += line_h
    # accent rule under headline
    rule_w = 120
    draw.rectangle([ (W-rule_w)//2, y+6, (W+rule_w)//2, y+11 ], fill=GOLD)
    y += 40
    for ln in sub_lines:
        tw = draw.textlength(ln, font=sub_font)
        draw.text(((W-tw)//2, y), ln, fill=(190,190,190) if a.bg!="cream" else (70,70,70), font=sub_font)
        y += sub_h

    base.save(a.out, "PNG")
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
