#!/usr/bin/env python3
"""make-dispatch-endcard.py — generate a "Today's Dispatch" end-card scene.

The connective device for a daily 3-video set. Drops in as the FINAL scene of
each of the day's three videos (last ~12s). It names the day's set and marks the
other two as "watch next" — while leaving the right side clear for YouTube's
CLICKABLE native end-screen elements (the real routing tool). It appears ONLY at
the end, never during the hook.

Faceless conduit standard: dark navy bed with continuous ambient motion, cream/
gold accents, Georgia serif heads, JetBrains-mono kickers. ALL motion on the
registered paused timeline (window.__timelines["root"]) so it renders in
HyperFrames and passes tools/scene-validator.py. No VO required (silent bed).

Usage:
  make-dispatch-endcard.py \
    --theme "The Little Tricks Beating Big AI" \
    --titles "He Doubled His AI's Accuracy With One Line|Why AI Forgets What You Just Told It|His AI Server Got Bored and Became a DJ" \
    --current 1 \
    --dispatch-line "Today's dispatch: three ways a little cleverness beat raw scale." \
    --out /path/to/scenes/99-dispatch-endcard
"""
import argparse
import html
import json
from pathlib import Path


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def build_html(theme, titles, current, dispatch_line, duration):
    # Rows: current one is dimmed ("YOU'RE WATCHING"), others gold ("WATCH NEXT").
    rows = []
    reveal_at = [2.10, 2.70, 3.30]
    for i, t in enumerate(titles):
        is_cur = (i + 1) == current
        badge = "YOU'RE WATCHING" if is_cur else "WATCH NEXT"
        cls = "row cur" if is_cur else "row nxt"
        rows.append(
            f'    <div class="{cls}" id="row{i}">'
            f'<span class="badge">{esc(badge)}</span>'
            f'<span class="rtitle">{esc(t)}</span></div>'
        )
    rows_html = "\n".join(rows)

    # Sequence each row reveal on the timeline.
    row_tweens = "\n".join(
        f"  rise('#row{i}', {reveal_at[i]:.2f});" for i in range(len(titles))
    )

    panel_dur = max(1.0, duration - 4.0)
    dl = esc(dispatch_line) if dispatch_line else ""
    dispatch_block = (
        f'  <div class="dispatchline" id="dline">{dl}</div>' if dl else ""
    )
    dispatch_tween = "  rise('#dline', 5.20, .7);" if dl else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Today's Dispatch end-card — {esc(theme)}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:1920px; height:1080px; overflow:hidden;
    background:#080B10; font-family:Georgia,'Times New Roman',serif; color:#F4F1EA; }}
  .stage {{ position:absolute; inset:0; }}
  /* moving bed — never static */
  .bed {{ position:absolute; inset:-8%;
    background:radial-gradient(ellipse at 32% 40%, #12202f 0%, #0b131d 52%, #070a0f 100%); }}
  .amb {{ position:absolute; border-radius:50%; filter:blur(60px); opacity:.5; }}
  #ambA {{ width:720px; height:720px; left:-120px; top:-160px;
    background:radial-gradient(circle, rgba(224,184,74,.16), transparent 70%); }}
  #ambB {{ width:640px; height:640px; right:-140px; bottom:-180px;
    background:radial-gradient(circle, rgba(74,140,224,.14), transparent 70%); }}
  .grain {{ position:absolute; inset:0; opacity:.05;
    background:radial-gradient(circle at 50% 50%, transparent 60%, #000 100%); }}
  /* content lives on the LEFT — right ~40% stays clear for YouTube end screens */
  .panel {{ position:absolute; left:120px; top:150px; width:940px; }}
  .kicker {{ font-family:'JetBrains Mono',ui-monospace,monospace; font-size:28px;
    letter-spacing:.32em; color:#E0B84A; opacity:0; text-transform:uppercase; }}
  .theme {{ font-size:82px; line-height:1.04; margin-top:18px; opacity:0; font-weight:700; }}
  .setlabel {{ font-family:'JetBrains Mono',ui-monospace,monospace; font-size:24px;
    letter-spacing:.2em; color:#9fb3c8; margin-top:44px; opacity:0; }}
  .row {{ display:flex; align-items:baseline; gap:22px; margin-top:26px; opacity:0; }}
  .badge {{ font-family:'JetBrains Mono',ui-monospace,monospace; font-size:20px;
    letter-spacing:.14em; padding:6px 12px; border-radius:4px; white-space:nowrap; }}
  .cur .badge {{ color:#8aa0b4; border:1px solid #33475b; }}
  .nxt .badge {{ color:#0b131d; background:#E0B84A; font-weight:700; }}
  .rtitle {{ font-size:40px; line-height:1.1; }}
  .cur .rtitle {{ color:#8aa0b4; }}
  .nxt .rtitle {{ color:#F4F1EA; }}
  .dispatchline {{ position:absolute; left:120px; bottom:96px; width:940px;
    font-style:italic; font-size:34px; color:#cdd8e4; opacity:0; }}
  /* subtle marker for the end-screen zone (creator drops clickable elements here) */
  .ezone {{ position:absolute; right:96px; top:210px; width:560px; height:660px;
    border:1px dashed rgba(159,179,200,.16); border-radius:12px; opacity:0; }}
  .ezlabel {{ position:absolute; right:120px; top:170px;
    font-family:'JetBrains Mono',ui-monospace,monospace; font-size:18px;
    letter-spacing:.18em; color:#3b5068; opacity:0; }}
</style>
</head>
<body data-start="0" data-duration="{duration:.2f}">
  <div class="stage">
    <div class="bed" id="bed"></div>
    <div class="amb" id="ambA"></div>
    <div class="amb" id="ambB"></div>
    <div class="grain"></div>

    <div class="ezlabel" id="ezlabel">↳ END-SCREEN ZONE</div>
    <div class="ezone" id="ezone"></div>

    <div class="panel">
      <div class="kicker" id="kicker">Today's Dispatch</div>
      <div class="theme" id="theme">{esc(theme)}</div>
      <div class="setlabel" id="setlabel">TODAY'S SET</div>
{rows_html}
    </div>
{dispatch_block}
  </div>

  <script>
  const tl = gsap.timeline({{paused:true, defaults:{{ease:'power2.out'}}}});

  // continuous ambient motion (nothing static > a few seconds).
  // NOTE: literal durations (not a variable) so the scene-validator's static
  // analysis can see the motion runs the full composition length.
  tl.to('#ambA', {{x:130, y:80, duration:{duration:.2f}, ease:'sine.inOut'}}, 0);
  tl.to('#ambB', {{x:-110, y:-70, duration:{duration:.2f}, ease:'sine.inOut'}}, 0);
  tl.fromTo('#bed', {{scale:1.0}}, {{scale:1.06, duration:{duration:.2f}, ease:'none'}}, 0);

  const rise = (s, t, d=.55) =>
    tl.fromTo(s, {{opacity:0, y:26}}, {{opacity:1, y:0, duration:d}}, Math.max(0, t-.28));

  rise('#kicker', 0.35, .5);
  rise('#theme', 0.80, .7);
  rise('#setlabel', 1.70, .5);
{row_tweens}
  rise('#ezlabel', 3.90, .5);
  tl.fromTo('#ezone', {{opacity:0}}, {{opacity:1, duration:.6}}, 3.90);
{dispatch_tween}
  // gentle drift on the whole panel so the hold never freezes
  tl.to('.panel', {{y:-22, duration:{panel_dur:.2f}, ease:'none'}}, 4.0);

  window.__timelines = window.__timelines || {{}};
  window.__timelines["root"] = tl;
  </script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Generate a Today's Dispatch end-card scene.")
    ap.add_argument('--theme', required=True, help='3-5 word through-line title')
    ap.add_argument('--titles', required=True, help='pipe-separated: "A|B|C"')
    ap.add_argument('--current', type=int, default=1, help='which of the 3 is the current video (1-3)')
    ap.add_argument('--dispatch-line', default='', help='the spoken/shown close line')
    ap.add_argument('--duration', type=float, default=12.0)
    ap.add_argument('--out', required=True, help='scene directory to write index.html into')
    args = ap.parse_args()

    titles = [t.strip() for t in args.titles.split('|') if t.strip()]
    if len(titles) != 3:
        raise SystemExit(f"need exactly 3 titles, got {len(titles)}")
    if not (1 <= args.current <= 3):
        raise SystemExit("--current must be 1, 2, or 3")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    html_str = build_html(args.theme, titles, args.current, args.dispatch_line, args.duration)
    (out / 'index.html').write_text(html_str)
    (out / 'hyperframes.json').write_text(json.dumps({
        "name": out.name, "duration": args.duration, "fps": 30,
        "width": 1920, "height": 1080,
    }, indent=2))
    print(f"✓ wrote {out/'index.html'} ({args.duration:.1f}s, current=video {args.current})")
    print(f"  theme: {args.theme}")
    for i, t in enumerate(titles):
        mark = "  ▶ (this video)" if i + 1 == args.current else "  ▸ watch next"
        print(f"    {i+1}. {t}{mark}")


if __name__ == '__main__':
    main()
