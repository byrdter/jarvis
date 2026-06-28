#!/usr/bin/env python3
"""Transparent 6-phase rail overlay (1920x1080 RGBA PNG) for the six-phase scene.
Right-edge vertical rail with the active phase highlighted, plus a left phase header.
Composited over a dimmed phase b-roll clip via ffmpeg.

Usage:
  make-phase-rail.py --path auto --phase 3 --out rail-auto-3.png
  make-phase-rail.py --path aug  --phase 1 --out rail-aug-1.png
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
CREAM = (245, 241, 232)
DIM   = (150, 150, 150)
FAINT = (120, 128, 140)
GOLD  = (224, 184, 74)
ORANGE= (245, 158, 11)
RED   = (239, 68, 68)
GREEN = (74, 222, 128)
BLUE  = (59, 130, 246)

SERIF = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
         "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
MONO  = ["/System/Library/Fonts/Menlo.ttc","/System/Library/Fonts/Courier New Bold.ttf"]
SANS  = ["/System/Library/Fonts/Supplemental/Arial.ttf","/System/Library/Fonts/Helvetica.ttc"]

TITLES = {
  "auto": ["Early resistance","Well-being undermined","Workslop rises",
           "Rising attrition","Employer brand declines","Leadership pipeline erodes"],
  "aug":  ["Trust accelerates","Well-being holds","New capabilities",
           "Retention strengthens","Talent magnet","Pipelines deepen"],
}

def font(cands, size):
    for c in cands:
        if Path(c).exists():
            try: return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

def spaced(s, gap="  "):
    return gap.join(list(s.upper()))

def text_s(d, xy, s, font, fill, sx=2, sy=3, shadow=(0,0,0,190), stroke=0):
    """Text with a drop shadow (legibility) and optional stroke (thicker)."""
    x,y = xy
    d.text((x+sx, y+sy), s, font=font, fill=shadow)
    if stroke:
        d.text((x,y), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=fill)
    else:
        d.text((x,y), s, font=font, fill=fill)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, choices=["auto","aug"])
    ap.add_argument("--phase", required=True, type=int)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    accent = ORANGE if a.path=="auto" else GREEN
    accent2= RED if a.path=="auto" else BLUE
    titles = TITLES[a.path]
    active = a.phase - 1

    img = Image.new("RGBA", (W,H), (0,0,0,0))

    # ---------- SCRIMS (drawn UNDER the text for legibility) ----------
    scrim = Image.new("RGBA", (W,H), (0,0,0,0))
    sd = ImageDraw.Draw(scrim)
    left_w = 980
    for x in range(left_w):                      # left scrim behind header
        al = int(205 * (1 - x/left_w)**1.3)
        sd.line([(x,0),(x,H)], fill=(8,11,16,al))
    rstart = 1170
    for x in range(rstart, W):                    # soft right scrim behind rail
        al = int(160 * ((x-rstart)/(W-rstart))**1.4)
        sd.line([(x,0),(x,H)], fill=(8,11,16,al))
    img = Image.alpha_composite(img, scrim)
    d = ImageDraw.Draw(img)

    f_kick  = font(MONO, 28)
    f_phase = font(MONO, 34)
    f_head  = font(SERIF, 106)
    f_rail  = font(SANS, 30)
    f_railA = font(SERIF, 42)
    f_hint  = font(MONO, 24)

    # ---------- LEFT HEADER ----------
    pathlabel = "AUTOMATION PATH" if a.path=="auto" else "AUGMENTATION PATH"
    text_s(d, (140, 150), spaced(pathlabel, "   "), f_kick, accent, sx=1, sy=2)
    # big phase header, vertically centered-left
    text_s(d, (140, 428), f"PHASE 0{a.phase}", f_phase, accent, sx=1, sy=2)
    # wrap title to ~780px
    title = titles[active]
    words = title.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t, font=f_head) <= 860: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    y=470
    for ln in lines:
        text_s(d, (140, y), ln, f_head, CREAM, sx=3, sy=4, stroke=4)   # bigger + bolder + shadow
        y+=118
    # accent underline
    d.rectangle([140, y+8, 268, y+14], fill=accent)

    # direction hint (brightened for legibility)
    hint = "↓  THE DECLINE COMPOUNDS" if a.path=="auto" else "↑  THE GAINS COMPOUND"
    hint_col = (245,140,120) if a.path=="auto" else (150,235,180)
    text_s(d, (140, y+52), spaced(hint, " "), f_hint, hint_col, sx=1, sy=2)

    # ---------- RIGHT RAIL ----------
    dot_x = 1720
    lab_r = 1672           # labels right-aligned ending here
    y0, y1 = 250, 850
    step = (y1 - y0) / 5
    # connector line
    d.line([(dot_x, y0), (dot_x, y1)], fill=(90,98,110,255), width=3)
    # progress fill up to active
    if active > 0:
        d.line([(dot_x, y0), (dot_x, int(y0+step*active))], fill=accent+(255,), width=3)
    for i in range(6):
        cy = int(y0 + step*i)
        is_active = (i == active)
        done = (i < active)
        # dot
        r = 16 if is_active else 9
        if is_active:
            d.ellipse([dot_x-r-6, cy-r-6, dot_x+r+6, cy+r+6], outline=accent+(255,), width=3)
            d.ellipse([dot_x-r, cy-r, dot_x+r, cy+r], fill=accent+(255,))
        elif done:
            d.ellipse([dot_x-r, cy-r, dot_x+r, cy+r], fill=accent+(180,))
        else:
            d.ellipse([dot_x-r, cy-r, dot_x+r, cy+r], outline=(110,118,130,255), width=3)
        # number tag inside/near dot
        num = f"{i+1}"
        # label (right aligned at lab_r)
        col = CREAM if is_active else (DIM if done else FAINT)
        fnt = f_railA if is_active else f_rail
        lab = titles[i]
        # truncate inactive long labels
        if not is_active and d.textlength(lab, font=fnt) > 360:
            while d.textlength(lab+"…", font=fnt) > 360 and len(lab)>4: lab=lab[:-1]
            lab=lab+"…"
        lw = d.textlength(lab, font=fnt)
        text_s(d, (lab_r-lw, cy-(fnt.size//2)-2), lab, fnt, col, sx=1, sy=2,
               stroke=2 if is_active else 0)

    img.save(a.out, "PNG")
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
