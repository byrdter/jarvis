#!/usr/bin/env python3
"""make-quote-card.py — generate a source-card quote scene (human presence, faceless).

The competitor's highest-ROI move: put a real person's words on screen without any
host or interview footage. A dark-navy conduit card with the quote typing in
word-by-word, the speaker's name + title/source, an optional date, and an OPTIONAL
circular photo. It's how a faceless video re-introduces a human voice.

Photo is optional by design (see references/USING-REAL-PEOPLE.md for the rules):
  --photo PATH   real press / public-domain / official photo (circular-cropped)
  --icon         a clean generic silhouette (no real likeness)
  (default)      no photo at all — an elegant attributed quote (safest, on-brand)

Faceless conduit standard: dark navy bed with continuous ambient motion, cream/gold
accents, Georgia serif quote, JetBrains-mono kicker. ALL motion on the registered
paused timeline so it renders in HyperFrames and passes tools/scene-validator.py.
Silent by default (no VO). If you have per-scene VO, anchor the reveal window with
--reveal-start / --reveal-window from the transcript (tools/cue.py).

Usage:
  make-quote-card.py \
    --quote "Piracy is almost always a service problem, not a pricing problem." \
    --name "Gabe Newell" --title "Co-founder, Valve" --date "IGN interview, 2011" \
    --out <project>/hyperframes-v3/scenes/07-quote-newell
  # add  --photo press/newell.jpg   or  --icon   for a headshot slot
"""
import argparse
import html
import shutil
from pathlib import Path
import json


def esc(s: str) -> str:
    return html.escape(s, quote=True)


SILHOUETTE_SVG = (
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="50" cy="50" r="50" fill="#16222f"/>'
    '<circle cx="50" cy="40" r="16" fill="#3b5068"/>'
    '<path d="M22 82c0-15 12-24 28-24s28 9 28 24z" fill="#3b5068"/></svg>'
)


def build_html(quote, name, title, date, photo_mode, photo_rel,
               duration, reveal_start, reveal_window):
    panel_dur = max(1.0, duration - 3.0)
    words = quote.split()
    # word spans — a REAL space (text node) between spans so the quote wraps.
    spans = " ".join(
        f'<span class="w" id="w{i}">{esc(w)}</span>' for i, w in enumerate(words)
    )
    # reveal each word across the reveal window (loop → variable positions; the
    # full-length ambient tween below covers the validator's dead-air check).
    n = max(1, len(words))
    step = (reveal_window / n)
    word_tweens = "\n".join(
        f"  tl.fromTo('#w{i}', {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.34}}, "
        f"{reveal_start + i * step:.3f});"
        for i in range(len(words))
    )

    if photo_mode == 'photo':
        photo_html = f'<div class="photo" id="photo"><img src="{esc(photo_rel)}" alt=""/></div>'
        photo_tween = "  tl.fromTo('#photo', {opacity:0, scale:.86}, {opacity:1, scale:1, duration:.5}, 0.30);"
        id_left = 'photo'
    elif photo_mode == 'icon':
        photo_html = f'<div class="photo" id="photo">{SILHOUETTE_SVG}</div>'
        photo_tween = "  tl.fromTo('#photo', {opacity:0, scale:.86}, {opacity:1, scale:1, duration:.5}, 0.30);"
        id_left = 'photo'
    else:
        photo_html = ''
        photo_tween = ''
        id_left = 'attrib'

    date_html = f'<div class="qdate" id="qdate">{esc(date)}</div>' if date else ''
    date_tween = "  tl.fromTo('#qdate', {opacity:0}, {opacity:1, duration:.4}, %.3f);" % (
        reveal_start + reveal_window + 0.25) if date else ''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Quote card — {esc(name)}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:1920px; height:1080px; overflow:hidden;
    background:#080B10; font-family:Georgia,'Times New Roman',serif; color:#F4F1EA; }}
  .stage {{ position:absolute; inset:0; }}
  .bed {{ position:absolute; inset:-8%;
    background:radial-gradient(ellipse at 38% 42%, #12202f 0%, #0b131d 54%, #070a0f 100%); }}
  .amb {{ position:absolute; border-radius:50%; filter:blur(64px); opacity:.5; }}
  #ambA {{ width:700px; height:700px; left:-120px; top:-150px;
    background:radial-gradient(circle, rgba(224,184,74,.15), transparent 70%); }}
  #ambB {{ width:620px; height:620px; right:-140px; bottom:-170px;
    background:radial-gradient(circle, rgba(74,140,224,.13), transparent 70%); }}
  .grain {{ position:absolute; inset:0; opacity:.05;
    background:radial-gradient(circle at 50% 50%, transparent 60%, #000 100%); }}
  .card {{ position:absolute; left:210px; right:210px; top:50%; transform:translateY(-50%); }}
  .qmark {{ font-size:150px; line-height:.5; color:#E0B84A; opacity:.55; height:70px; }}
  .quote {{ font-size:58px; line-height:1.32; margin-top:6px; max-width:1360px; font-style:italic; }}
  .w {{ display:inline; }}
  .attrib {{ display:flex; align-items:center; gap:26px; margin-top:52px; }}
  .photo {{ width:110px; height:110px; border-radius:50%; overflow:hidden; flex:0 0 auto;
    border:1px solid rgba(224,184,74,.4); }}
  .photo img, .photo svg {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .who {{ display:flex; flex-direction:column; gap:6px; }}
  .name {{ font-size:38px; font-weight:700; font-style:normal; }}
  .title {{ font-family:'JetBrains Mono',ui-monospace,monospace; font-size:24px;
    letter-spacing:.16em; color:#E0B84A; text-transform:uppercase; }}
  .qdate {{ position:absolute; left:210px; bottom:88px;
    font-family:'JetBrains Mono',ui-monospace,monospace; font-size:20px;
    letter-spacing:.14em; color:#7f93a6; }}
</style>
</head>
<body data-start="0" data-duration="{duration:.2f}">
  <div class="stage">
    <div class="bed" id="bed"></div>
    <div class="amb" id="ambA"></div>
    <div class="amb" id="ambB"></div>
    <div class="grain"></div>

    <div class="card">
      <div class="qmark" id="qmark">&ldquo;</div>
      <div class="quote" id="quote">{spans}</div>
      <div class="attrib" id="attrib">
        {photo_html}
        <div class="who">
          <div class="name" id="qname">{esc(name)}</div>
          <div class="title" id="qtitle">{esc(title)}</div>
        </div>
      </div>
    </div>
    {date_html}
  </div>

  <script>
  const tl = gsap.timeline({{paused:true, defaults:{{ease:'power2.out'}}}});

  // continuous ambient motion — literal durations so the validator sees motion
  // run the full composition length (no dead-air false positive).
  tl.to('#ambA', {{x:120, y:70, duration:{duration:.2f}, ease:'sine.inOut'}}, 0);
  tl.to('#ambB', {{x:-100, y:-60, duration:{duration:.2f}, ease:'sine.inOut'}}, 0);
  tl.fromTo('#bed', {{scale:1.0}}, {{scale:1.05, duration:{duration:.2f}, ease:'none'}}, 0);

  tl.fromTo('#qmark', {{opacity:0, y:12}}, {{opacity:.55, y:0, duration:.5}}, 0.15);
{photo_tween}
  tl.fromTo('#qname', {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.5}}, 0.42);
  tl.fromTo('#qtitle', {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.5}}, 0.58);
{date_tween}
  // the quote types in word-by-word
{word_tweens}
  // gentle drift so the hold never freezes
  tl.to('.card', {{y:'-=18', duration:{panel_dur:.2f}, ease:'none'}}, 2.0);

  window.__timelines = window.__timelines || {{}};
  window.__timelines["root"] = tl;
  </script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Generate a source-card quote scene.")
    ap.add_argument('--quote', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--title', default='', help='role / source, e.g. "Co-founder, Valve"')
    ap.add_argument('--date', default='', help='e.g. "IGN interview, 2011"')
    ap.add_argument('--photo', default='', help='path to a REAL press/public-domain photo (circular)')
    ap.add_argument('--icon', action='store_true', help='use a generic silhouette instead of a photo')
    ap.add_argument('--duration', type=float, default=8.0)
    ap.add_argument('--reveal-start', type=float, default=0.9, help='when the quote begins typing')
    ap.add_argument('--reveal-window', type=float, default=None,
                    help='seconds over which the quote types in (default: ~55%% of duration)')
    ap.add_argument('--out', required=True, help='scene directory to write into')
    args = ap.parse_args()

    out = Path(args.out)
    (out / 'assets').mkdir(parents=True, exist_ok=True)

    photo_mode, photo_rel = 'none', ''
    if args.photo:
        src = Path(args.photo)
        if not src.exists():
            raise SystemExit(f"--photo not found: {src}")
        ext = src.suffix.lower() or '.jpg'
        dest = out / 'assets' / f'quote-photo{ext}'
        shutil.copy(src, dest)
        photo_mode, photo_rel = 'photo', f'assets/quote-photo{ext}'
    elif args.icon:
        photo_mode = 'icon'

    reveal_window = args.reveal_window if args.reveal_window is not None else max(1.5, args.duration * 0.55)

    html_str = build_html(args.quote, args.name, args.title, args.date,
                          photo_mode, photo_rel, args.duration,
                          args.reveal_start, reveal_window)
    (out / 'index.html').write_text(html_str)
    (out / 'hyperframes.json').write_text(json.dumps({
        "name": out.name, "duration": args.duration, "fps": 30, "width": 1920, "height": 1080,
    }, indent=2))
    print(f"✓ wrote {out/'index.html'} ({args.duration:.1f}s, photo={photo_mode})")
    print(f"  “{args.quote[:60]}{'…' if len(args.quote) > 60 else ''}”")
    print(f"  — {args.name}{' · ' + args.title if args.title else ''}")
    if photo_mode == 'photo':
        print("  ⚠ photo in use — confirm it is real & rightsable (press/public-domain/CC). See references/USING-REAL-PEOPLE.md")


if __name__ == '__main__':
    main()
