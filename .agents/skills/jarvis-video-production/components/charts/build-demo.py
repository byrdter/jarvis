#!/usr/bin/env python3
"""Regenerate demo/index.html from charts.html. Run after ANY edit, then
`hyperframes check` + `hyperframes render` in demo/ — that pair is the regression test.

Extraction anchors on the BLOCK marker comments, never on bare <style>/<script> tags, and
BLOCK B is taken marker-to-marker rather than "the first div". Both traps have already cost
a debug cycle each on spine-ledger / annotation-hud (2026-08-04).

Demo values are the REAL frozen figures from the project's claim-source-map.md. A chart demo
built on fake numbers teaches you nothing about whether the chart can hold the real ones.
"""
import re, pathlib

HERE = pathlib.Path(__file__).parent
src  = (HERE / "charts.html").read_text()
body = src.split("============ -->", 1)[1]

style  = re.search(r"<style>(.*?)</style>", body, re.S).group(1)
markup = re.search(r"BLOCK B[^>]*-->\n(.*?)<!-- =+ BLOCK C", body, re.S).group(1).strip()
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)

assert "<style>"  not in style,  "extraction leaked a <style> tag"
assert "<script>" not in script, "extraction leaked a <script> tag"
assert ".cv{position:absolute" in style, "the .cv container rule is missing"
for _need in ('id="cv-inv"', 'id="cv-dots"', 'id="cv-ratio"'):
    assert _need in markup, f"BLOCK B extraction dropped {_need}"

DEMO_CSS = """  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1920px;height:1080px;overflow:hidden;background:#0A0E14;
    font-family:'JetBrains Mono',monospace}
  #root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#0A0E14}
  .bgwrap{position:absolute;inset:0;z-index:1;overflow:hidden}
  .bgwrap img{width:100%;height:100%;object-fit:cover;will-change:transform}
  .bgscrim{position:absolute;inset:0;z-index:2;
    background:radial-gradient(ellipse at 30% 50%,rgba(8,11,16,.74),rgba(5,8,12,.93))}
  .spineghost{position:absolute;left:64px;top:50%;transform:translateY(-50%);z-index:9;
    width:384px;height:700px;border:1px dashed rgba(201,178,122,.30);border-radius:5px;
    background:rgba(14,18,25,.55);color:#93A3BC;font-size:14px;letter-spacing:.22em;
    text-transform:uppercase;display:flex;align-items:center;justify-content:center;
    text-align:center;padding:20px;line-height:1.9}
"""

# ---- REAL figures, claim-source-map.md §A (FROZEN 2026-08-02) -----------------------
MOUNT = """
const tl = gsap.timeline({paused:true});
window.__timelines = window.__timelines || {};
window.__timelines["root"] = tl;
tl.to("#bgv",{scale:1.07,duration:56,ease:"none"},0);

// COMPRESSED demo timings, REAL frozen values (claim-source-map.md §A). sceneStart:0 so the
// demo numbers read as-is; the real builds pass MASTER-ABSOLUTE seconds from
// 01-script/scenes-v2-build.json with that scene's sceneStart.

// --- S03: volume is not cost. The reorder at the flip IS the argument. ---------------
mountInversion(tl, {
  sceneStart: 0,
  viewport: {x:500, y:150, w:1340, h:470},
  title: 'WHERE THE TOKENS GO',
  boxIn: 0.4,
  measures: [
    {key:'volume', label:'SHARE OF TOKENS',     at: 1.4},
    {key:'cost',   label:'SHARE OF THE MONEY',  at: 8.4}   // <- the flip
  ],
  bars: [
    {name:'CACHE READ',  volume:92.9, cost:39.9},
    {name:'CACHE WRITE', volume:6.7,  cost:51.3, hero:true},
    {name:'OUTPUT',      volume:0.4,  cost:8.6},
    {name:'INPUT',       volume:0.03, cost:0.2}
  ],
  holdOut: 15.4
});

// --- S03 -> S08: concentration. 490 sessions, 49 carry 89.8%, 4 carry 25.7%. ---------
mountDotGrid(tl, {
  sceneStart: 0,
  viewport: {x:500, y:150, w:1340, h:560},
  total: 490, cols: 35, gap: 7,
  title: '490 SESSIONS WITH USAGE',
  boxIn: 17.0,
  steps: [
    {at:18.4, lit:49,   label:'49 SESSIONS \\u00B7 89.8% OF THE BILL'},
    {at:24.0, flare:4,  label:'4 SESSIONS \\u00B7 25.7%'}
  ],
  holdOut: 31.0
});

// --- S09: the write costs 20x the read. -----------------------------------------------
mountRatio(tl, {
  sceneStart: 0,
  viewport: {x:500, y:250, w:1340, h:420},
  title: 'OPUS TIER \\u00B7 PER MILLION TOKENS',
  boxIn: 32.6,
  rows: [
    {name:'CACHE READ',      value:0.50, at:34.0},
    {name:'BASE INPUT',      value:5.00, at:37.0},
    {name:'1H CACHE WRITE',  value:10.00, at:40.0, hero:true}
  ],
  multiple: {at:44.0, text:'20\\u00D7', sub:'WRITE VS READ'}
});
"""

html = (
'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8" />\n'
'<title>Charts — DEMO (inversion / dot-grid concentration / ratio)</title>\n'
'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
'<style>\n' + DEMO_CSS + style + '</style></head>\n<body>\n'
'<div id="root" class="clip" data-composition-id="root" data-width="1920" data-height="1080"'
' data-start="0" data-duration="56">\n'
'  <div class="bgwrap"><img id="bgv" src="assets/bg-open-desk.png" alt=""'
' data-layout-allow-overflow /></div>\n'
'  <div class="bgscrim"></div>\n'
'  <div class="spineghost">spine-ledger<br>sits here<br>—<br>'
'charts must never<br>cross x=448</div>\n'
+ markup + '\n</div>\n'
'<script>' + script + '</script>\n'
'<script>' + MOUNT + '</script>\n</body></html>\n')

assert html.count('<style>') == 1 and html.count('</style>') == 1, "stray style tag"
assert html.count('<script') == 3 and html.count('</script>') == 3, "script tag imbalance"

(HERE / "demo" / "index.html").write_text(html)
print("wrote demo/index.html  %d bytes" % len(html))
