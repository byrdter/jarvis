#!/usr/bin/env python3
"""Regenerate demo/index.html from annotation-hud.html. Run after ANY edit, then
`hyperframes check` + `hyperframes render` in demo/ — that pair is the regression test.

Extraction anchors on the BLOCK marker comments, never on bare <style>/<script> tags: the
component's usage notes contain the literal text "<style>", and a naive tag regex matches
THAT, embedding a stray <style> mid-CSS. CSS error-recovery then silently eats the very next
rule and the whole overlay loses its positioning. (Cost a debug cycle on spine-ledger,
2026-08-04 — same trap, same fix.)

The demo runs the REAL C5 geometry and the REAL row names, on a compressed 44s timeline that
exercises every primitive: kicker, framing move, acquire, bracket, flatline, step, release.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
src  = (HERE / "annotation-hud.html").read_text()
body = src.split("============ -->", 1)[1]          # drop the doc comment FIRST

style  = re.search(r"<style>(.*?)</style>", body, re.S).group(1)
# BLOCK B is everything between its marker and BLOCK C's — not "the first div". A regex
# that stops at the first </div> silently drops any sibling added later (it dropped
# #hud-kick the moment the kicker moved outside the clipped box, 2026-08-04).
markup = re.search(r"BLOCK B[^>]*-->\n(.*?)<!-- =+ BLOCK C", body, re.S).group(1).strip()
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)

assert "<style>"  not in style,  "extraction leaked a <style> tag"
assert "<script>" not in script, "extraction leaked a <script> tag"
assert "#hud{position:absolute" in style, "the #hud container rule is missing"
for _need in ('id="hud"', 'id="hud-cap"', 'id="hud-ann"', 'id="hud-kick"'):
    assert _need in markup, f"BLOCK B extraction dropped {_need}"

GEO = json.loads((HERE / "demo" / "assets" / "C5-table-geometry.json").read_text())
GEO["source"] = "assets/C5-pricing-still.png"

# Band order is NOT semantics. This map was verified against the pixels on 2026-08-04 by
# cropping each band and reading it. Re-verify after any re-capture.
ROWS = {
    "fable-5":    0,   # Claude Fable 5              $10 / $50   <- the new tier above Opus
    "mythos-5":   1,   # Claude Mythos 5 (limited)   $10 / $50
    "opus-5":     2,   # Claude Opus 5               $5  / $25
    "opus-4.8":   3,
    "opus-4.7":   4,
    "opus-4.6":   5,
    "opus-4.5":   6,   # Claude Opus 4.5             $5  / $25
    "opus-4.1":   7,   # Claude Opus 4.1 (deprecated) $15 / $75
    "opus-4":     8,   # Claude Opus 4 (retired)      $15 / $75
    "sonnet-aug": 9,   # Claude Sonnet 5 through August 31, 2026    $2 / $10
    "sonnet-sep": 10,  # Claude Sonnet 5 starting September 1, 2026 $3 / $15
}

DEMO_CSS = """  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1920px;height:1080px;overflow:hidden;background:#0A0E14;
    font-family:'JetBrains Mono',monospace}
  #root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#0A0E14}
  .bgwrap{position:absolute;inset:0;z-index:1;overflow:hidden}
  .bgwrap img{width:100%;height:100%;object-fit:cover;will-change:transform}
  .bgscrim{position:absolute;inset:0;z-index:2;
    background:radial-gradient(ellipse at 30% 50%,rgba(8,11,16,.72),rgba(5,8,12,.92))}
  .spineghost{position:absolute;left:64px;top:50%;transform:translateY(-50%);z-index:9;
    width:384px;height:700px;border:1px dashed rgba(201,178,122,.30);border-radius:5px;
    background:rgba(14,18,25,.55);color:#93A3BC;font-size:14px;letter-spacing:.22em;
    text-transform:uppercase;display:flex;align-items:center;justify-content:center;
    text-align:center;padding:20px;line-height:1.9}
"""

MOUNT = """
const tl = gsap.timeline({paused:true});
window.__timelines = window.__timelines || {};
window.__timelines["root"] = tl;
tl.to("#bgv",{scale:1.08,duration:44,ease:"none"},0);

// COMPRESSED demo timings — 44s to exercise EVERY primitive on the REAL capture and the
// REAL rows. The video splits these across S05 (abs 306.8) and S06 (abs 358.6); the real
// builds pass MASTER-ABSOLUTE seconds from 01-script/scenes-v2-build.json with that
// scene's sceneStart. sceneStart:0 here so demo numbers read as-is.
//
// NOTE: sceneStart:0 means nothing is in the past, so this does NOT exercise the mid-video
// mount path. Use probe-midscene.js for that — see the README.
mountHUD(tl, {
  sceneStart: 0,
  capture:  'assets/C5-pricing-still.png',
  geometry: C5_GEO,
  rows:     C5_ROWS,
  viewport: {x:500, y:126, w:1380, h:820},
  framings: {
    wide:  {sx:680,  sy:40,   sw:2380},   // browser chrome + page head — it is a REAL page
    // sw is WIDER than the table's 1643px on purpose: the extra ~340px of the page's own
    // right margin becomes the chip gutter. Framed tight to the table, every chip lands
    // past x=1920 and the layout checker flags canvas_overflow. 0.70x — still a downscale.
    //
    // sy=925 starts ABOVE the column header band (944-1004) so "Base Input Tokens" and
    // "Output Tokens" are readable — the viewer needs them to parse the rows. Paired with
    // h:820 the bottom lands in the gap after Sonnet 4.5, so no row is sliced in half.
    // Both edges were chosen from the MEASURED bands, not by eye.
    table: {sx:1049, sy:925, sw:1980}
  },
  start: 'wide',
  boxIn: 0.3,
  moves: [{to:'table', at:3.0, dur:1.9}],
  cues: [
    {t:'kicker',   at:0.9,  text:'ANTHROPIC \\u00B7 PUBLISHED RATES'},

    // Labels are SEMANTIC, never a re-typing of the rate. The numbers are the capture's
    // own pixels — repeating them in a chip is both redundant and the thing the component
    // header forbids. It is also what made every chip overflow the canvas.

    // --- S05, the reversal: it has not been climbing -------------------------------
    {t:'acquire',  at:6.0,  row:'opus-4',    label:'A YEAR AGO'},
    {t:'acquire',  at:9.4,  row:'opus-5',    label:'TODAY'},
    {t:'bracket',  at:12.8, from:'opus-5', to:'opus-4', label:'3\\u00D7 CHEAPER'},
    {t:'release',  at:17.4},

    // --- S06, the second reversal: the fall stopped --------------------------------
    {t:'flatline', at:19.6, from:'opus-5', to:'opus-4.5', label:'NO CHANGE'},
    {t:'release',  at:24.4},
    {t:'acquire',  at:26.4, row:'sonnet-aug', label:'UNTIL AUG 31'},
    {t:'acquire',  at:30.0, row:'sonnet-sep', label:'FROM SEP 1', tone:'rise'},
    {t:'step',     at:33.4, from:'sonnet-aug', to:'sonnet-sep', label:'+50%', tone:'rise'},
    {t:'release',  at:37.0},
    {t:'acquire',  at:38.8, row:'fable-5', label:'NEW TIER', tone:'rise'}
  ]
});
"""

html = (
'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8" />\n'
'<title>Annotation HUD — DEMO (kicker / push / acquire / bracket / flatline / step)</title>\n'
'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
'<style>\n' + DEMO_CSS + style + '</style></head>\n<body>\n'
'<div id="root" class="clip" data-composition-id="root" data-width="1920" data-height="1080"'
' data-start="0" data-duration="44">\n'
'  <div class="bgwrap"><img id="bgv" src="assets/bg-open-desk.png" alt=""'
' data-layout-allow-overflow /></div>\n'
'  <div class="bgscrim"></div>\n'
'  <div class="spineghost">spine-ledger<br>sits here<br>—<br>'
'the HUD viewport must never<br>cross x=448</div>\n'
+ markup + '\n</div>\n'
'<script>const C5_GEO = ' + json.dumps(GEO) + ';\n'
'const C5_ROWS = ' + json.dumps(ROWS) + ';</script>\n'
'<script>' + script + '</script>\n'
'<script>' + MOUNT + '</script>\n</body></html>\n')

assert html.count('<style>') == 1 and html.count('</style>') == 1, "stray style tag"
assert html.count('<script') == 4 and html.count('</script>') == 4, "script tag imbalance"

(HERE / "demo" / "index.html").write_text(html)
print("wrote demo/index.html  %d bytes  |  %d rows mapped, %d row bands measured"
      % (len(html), len(ROWS), len(GEO["rows"])))
