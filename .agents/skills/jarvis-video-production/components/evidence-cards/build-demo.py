#!/usr/bin/env python3
"""Regenerate demo/index.html from evidence-cards.html. Run after ANY edit, then
`hyperframes check` + `hyperframes render` in demo/ — that pair is the regression test.

Extraction anchors on BLOCK marker comments, and BLOCK B is taken marker-to-marker. Both
traps have cost a debug cycle each already (spine-ledger, annotation-hud, 2026-08-04).

The demo runs the REAL cold open (S01) and the REAL landing (S10) with frozen figures from
the project's claim-source-map.md.
"""
import re, pathlib

HERE = pathlib.Path(__file__).parent
src  = (HERE / "evidence-cards.html").read_text()
body = src.split("============ -->", 1)[1]

style  = re.search(r"<style>(.*?)</style>", body, re.S).group(1)
markup = re.search(r"BLOCK B[^>]*-->\n(.*?)<!-- =+ BLOCK C", body, re.S).group(1).strip()
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)

assert "<style>"  not in style,  "extraction leaked a <style> tag"
assert "<script>" not in script, "extraction leaked a <script> tag"
assert ".ec{position:absolute" in style, "the .ec container rule is missing"
assert 'id="ec-host"' in markup, "BLOCK B extraction dropped the host div"

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

# ---- REAL figures, claim-source-map.md §A/§B (FROZEN 2026-08-02) --------------------
MOUNT = """
const tl = gsap.timeline({paused:true});
window.__timelines = window.__timelines || {};
window.__timelines["root"] = tl;
tl.to("#bgv",{scale:1.07,duration:46,ease:"none"},0);

const money = v => '$' + Math.round(v).toLocaleString('en-US');

// --- S01 cold open: what was paid vs what was consumed, then the gap ------------------
mountDocCard(tl, {
  sceneStart: 0, id: 'paid',
  viewport: {x:500, y:170, w:640, h:520},
  kicker: 'SUBSCRIPTION', head: 'What was paid',
  at: 0.4,
  rows: [
    {k:'PLAN',    v:'Flat monthly'},
    {k:'MONTHS',  v:'8'},
    {k:'PER-TOKEN CHARGE', v:'None'}
  ],
  total: {k:'TOTAL PAID', v:'$1,000', at: 2.6},
  stamp: {text:'PAID', at: 3.6},
  holdOut: 19.0
});

mountDocCard(tl, {
  sceneStart: 0, id: 'used',
  viewport: {x:1200, y:170, w:640, h:520},
  kicker: 'AT PUBLISHED RATES', head: 'What was consumed',
  at: 5.4,
  rows: [
    {k:'TOKENS',   v:'11,346,275,422'},
    {k:'SESSIONS', v:'509'},
    {k:'MESSAGES', v:'33,313'}
  ],
  total: {k:'API-EQUIVALENT', v:'$13,753', at: 7.6,
          count:{from:0, to:13753, dur:1.4, fmt:money}},
  stamp: {text:'NEVER INVOICED', at: 9.0},
  holdOut: 19.0
});

// the subtraction resolving — the cold open's whole claim
mountStatHero(tl, {
  sceneStart: 0,
  viewport: {x:500, y:760, w:1340},
  id: 'gap',
  kicker: 'THE GAP',
  at: 12.4,
  count: {from:0, to:12753, dur:1.5, fmt:money},
  aside: 'One account. One laptop. No bill ever arrived.',
  asideAt: 14.4,
  holdOut: 19.0
});

// --- S07: what we cannot tell you (the credibility beat) -----------------------------
mountDocCard(tl, {
  sceneStart: 0, id: 'unknown',
  viewport: {x:640, y:230, w:1060, h:470},
  kicker: 'NOT PUBLISHED \\u00B7 NOT KNOWABLE FROM OUTSIDE',
  head: 'What we cannot tell you',
  at: 20.6,
  rows: [
    {k:'COST TO SERVE A TOKEN', v:'Unpublished', at:22.2},
    {k:'TOKENS \\u2192 SUBSCRIPTION LIMIT', v:'Unpublished', at:23.4}
  ],
  total: {k:'THEREFORE', v:'Not a prediction', at:25.0},
  stamp: {text:'STATED, NOT HIDDEN', at:26.4},
  holdOut: 30.0
});

// --- S10: the landing. Full-frame text is permitted HERE and nowhere else. ------------
mountLanding(tl, {
  sceneStart: 0, id: 'close',
  viewport: {x:420, y:330, w:1420},
  lines: [
    {text:'Twelve thousand dollars of compute was delivered,', at:31.6},
    {text:'at their own posted rate, and never invoiced.',      at:34.0},
    {text:'The published price has stopped falling.',           at:37.4, accent:true}
  ]
});
"""

html = (
'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8" />\n'
'<title>Evidence cards — DEMO (doc card / stat hero / landing)</title>\n'
'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
'<style>\n' + DEMO_CSS + style + '</style></head>\n<body>\n'
'<div id="root" class="clip" data-composition-id="root" data-width="1920" data-height="1080"'
' data-start="0" data-duration="46">\n'
'  <div class="bgwrap"><img id="bgv" src="assets/bg-open-desk.png" alt=""'
' data-layout-allow-overflow /></div>\n'
'  <div class="bgscrim"></div>\n'
'  <div class="spineghost">spine-ledger<br>sits here<br>—<br>'
'cards must never<br>cross x=448</div>\n'
+ markup + '\n</div>\n'
'<script>' + script + '</script>\n'
'<script>' + MOUNT + '</script>\n</body></html>\n')

assert html.count('<style>') == 1 and html.count('</style>') == 1, "stray style tag"
assert html.count('<script') == 3 and html.count('</script>') == 3, "script tag imbalance"

(HERE / "demo" / "index.html").write_text(html)
print("wrote demo/index.html  %d bytes" % len(html))
