#!/usr/bin/env python3
"""Regenerate demo/index.html from spine-ledger.html. Run after ANY edit to the component,
then `hyperframes check` + `hyperframes render` in demo/ — that pair is the regression test.

Extraction anchors on the BLOCK marker comments, never on bare <style>/<script> tags: the
component's usage notes contain the literal text "<style>", and a naive tag regex matches
THAT, embedding a stray <style> mid-CSS. CSS error-recovery then silently eats the very next
rule (#lg{...}), the panel loses position:absolute/z-index, and every text element reports
text_occluded. That cost a full debug cycle on 2026-08-04 — hence the asserts below.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
src = (HERE / "spine-ledger.html").read_text()
body = src.split("============ -->", 1)[1]        # drop the doc comment first

style  = re.search(r"<style>(.*?)</style>", body, re.S).group(1)
markup = re.search(r'(<div id="lg">.*?\n</div>)', body, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)

assert "<style>"  not in style,  "extraction leaked a <style> tag"
assert "<script>" not in script, "extraction leaked a <script> tag"
assert "#lg{position:absolute" in style, "the #lg container rule is missing"

DEMO_CSS = """  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1920px;height:1080px;overflow:hidden;background:#0A0E14;
    font-family:'JetBrains Mono',monospace}
  #root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#0A0E14}
  .bgwrap{position:absolute;inset:0;z-index:1;overflow:hidden}
  .bgwrap img{width:100%;height:100%;object-fit:cover;will-change:transform}
  .bgscrim{position:absolute;inset:0;z-index:2;
    background:radial-gradient(ellipse at 34% 50%,rgba(8,11,16,.66),rgba(5,8,12,.88))}
  .demo-stage{position:absolute;left:560px;top:50%;transform:translateY(-50%);z-index:8;
    width:1240px;color:#7C8BA3;font-size:23px;letter-spacing:.13em;text-transform:uppercase;
    line-height:1.6}
  .demo-stage b{display:block;color:#93A3BC;font-size:15px;letter-spacing:.30em;
    margin-bottom:18px}
"""

MOUNT = """
const tl = gsap.timeline({paused:true});
window.__timelines = window.__timelines || {};
window.__timelines["root"] = tl;
tl.to("#bgv",{scale:1.10,duration:34,ease:"none"},0);

// COMPRESSED demo timings — 34s to exercise EVERY state, exactly as spine-elimination's
// demo compresses its own. The real build passes MASTER-ABSOLUTE seconds straight out of
// 01-script/scenes-v2-build.json with that scene's real sceneStart. sceneStart:0 here so
// the demo numbers read as-is.
//
// NOTE: sceneStart:0 means NOTHING is in the past, so this demo does NOT exercise the
// mid-video mount path. Use probe-midscene.js for that — see the README.
mountLedger(tl, {
  sceneStart: 0,
  ledger: [
    {label:'PAID', value:'$1,000',  at:0.6},
    {label:'USED', value:'$13,753', at:1.9},
    {label:'GAP',  value:'$12,753', at:3.3, emphasis:true}
  ],
  ghostsIn: 4.6,
  rows: [
    {q:'WHERE DOES IT GO?',     open: 6.0,
     answers:[{text:'LONG SESSIONS \\u00B7 10% = 90%', at: 8.6}]},
    {q:'WHO ABSORBS IT?',       open:10.6,
     answers:[{text:'UNVERIFIABLE FROM OUTSIDE', at:13.0, tone:'closed'}]},
    {q:'DOES IT CLOSE ITSELF?', open:15.2,
     answers:[{text:'YES \\u2014 PRICE FELL 3\\u00D7',   at:17.6, tone:'provisional'},
              {text:'NO \\u2014 THE FALL STOPPED', at:22.4}]},
    {q:'WHAT MOVES FIRST?',     open:25.4,
     answers:[{text:'THE LONG SESSIONS FIRST', at:29.2, verdict:true}]}
  ]
});
"""

html = (
'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8" />\n'
'<title>Open-question ledger spine — DEMO (ghost / open / provisional / struck / answered)</title>\n'
'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
'<style>\n' + DEMO_CSS + style + '</style></head>\n<body>\n'
'<div id="root" class="clip" data-composition-id="root" data-width="1920" data-height="1080"'
' data-start="0" data-duration="34">\n'
'  <div class="bgwrap"><img id="bgv" src="assets/bg-open-desk.png" alt=""'
' data-layout-allow-overflow /></div>\n'
'  <div class="bgscrim"></div>\n'
'  <div class="demo-stage"><b>demo stand-in — scene content sits here</b>\n'
'    the ledger is an overlay: it must stay legible over the moving bed and never collide\n'
'    with a centred 1180px citation card</div>\n'
+ markup + '\n</div>\n'
'<script>' + script + '</script>\n'
'<script>' + MOUNT + '</script>\n</body></html>\n')

assert html.count('<style>') == 1 and html.count('</style>') == 1, "stray style tag"
assert html.count('<script') == 3 and html.count('</script>') == 3, "script tag imbalance"

(HERE / "demo" / "index.html").write_text(html)
print("wrote demo/index.html  %d bytes  |  1 style block, 3 script blocks" % len(html))
