#!/usr/bin/env python3
"""Company lockup card (1920x1080 PNG) for case-study scenes.
Two modes:
  --logo PATH   : center a transparent wordmark on dark, CEO + path tag.
  --photo PATH  : dimmed full-bleed portrait, company + CEO lower-left.

Usage:
  make-logo-card.py --company Block --ceo "Jack Dorsey" --path auto --logo block-logo.png --out block.png
  make-logo-card.py --company Microsoft --ceo "Satya Nadella" --path aug --photo nadella.png --out msft.png
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
DARK  = (13, 17, 23)
CREAM = (244, 241, 234)
DIM   = (190, 190, 190)
ORANGE= (245, 158, 11)
GREEN = (74, 222, 128)

SERIF = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf","/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
MONO  = ["/System/Library/Fonts/Menlo.ttc","/System/Library/Fonts/Courier New Bold.ttf"]
SANS  = ["/System/Library/Fonts/Supplemental/Arial.ttf","/System/Library/Fonts/Helvetica.ttc"]

def font(c,s):
    for p in c:
        if Path(p).exists():
            try: return ImageFont.truetype(p,s)
            except Exception: pass
    return ImageFont.load_default()

def spaced(s): return "   ".join(list(s.upper()))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--company",required=True); ap.add_argument("--ceo",default="")
    ap.add_argument("--path",choices=["auto","aug"],required=True)
    ap.add_argument("--logo",default=""); ap.add_argument("--photo",default="")
    ap.add_argument("--kicker",default="CASE STUDY")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    accent = ORANGE if a.path=="auto" else GREEN
    pathlabel = "AUTOMATION PATH" if a.path=="auto" else "AUGMENTATION PATH"

    f_kick=font(MONO,26); f_path=font(MONO,24); f_co=font(SERIF,96); f_ceo=font(SANS,40)

    if a.photo:
        img=Image.open(a.photo).convert("RGB")
        sc=max(W/img.width,H/img.height)
        img=img.resize((int(img.width*sc),int(img.height*sc)),Image.LANCZOS)
        x=(img.width-W)//2; y=(img.height-H)//2; img=img.crop((x,y,x+W,y+H))
        # left+bottom gradient scrim for text legibility
        scrim=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(scrim)
        for yy in range(H):
            a_b=int(210*max(0,(yy-H*0.45)/(H*0.55)))
            sd.line([(0,yy),(W,yy)],fill=(8,11,16,a_b))
        for xx in range(int(W*0.6)):
            a_l=int(150*(1-xx/(W*0.6)))
            sd.line([(xx,0),(xx,H)],fill=(8,11,16,a_l))
        base=Image.alpha_composite(img.convert("RGBA"),scrim).convert("RGB")
        d=ImageDraw.Draw(base)
        d.text((140,150),spaced(pathlabel),fill=accent,font=f_path)
        d.text((140,H-300),spaced(a.kicker),fill=accent,font=f_kick)
        d.text((136,H-250),a.company,fill=CREAM,font=f_co,stroke_width=2,stroke_fill=CREAM)
        if a.ceo: d.text((140,H-128),a.ceo,fill=DIM,font=f_ceo)
        base.save(a.out,"PNG")
    else:
        base=Image.new("RGB",(W,H),DARK); d=ImageDraw.Draw(base)
        # path tag top-center
        tw=d.textlength(spaced(pathlabel),font=f_path); d.text(((W-tw)//2,170),spaced(pathlabel),fill=accent,font=f_path)
        # logo centered
        logo=Image.open(a.logo).convert("RGBA")
        maxw,maxh=900,360
        sc=min(maxw/logo.width,maxh/logo.height); logo=logo.resize((int(logo.width*sc),int(logo.height*sc)),Image.LANCZOS)
        lx=(W-logo.width)//2; ly=380
        base.paste(logo,(lx,ly),logo)
        # CEO + accent rule
        ry=ly+logo.height+70
        d.rectangle([(W-130)//2,ry,(W+130)//2,ry+5],fill=accent)
        if a.ceo:
            cw=d.textlength(a.ceo,font=f_ceo); d.text(((W-cw)//2,ry+34),a.ceo,fill=DIM,font=f_ceo)
        base.save(a.out,"PNG")
    print(f"wrote {a.out}")

if __name__=="__main__": main()
