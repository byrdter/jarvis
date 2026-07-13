#!/usr/bin/env python3
"""Typeset a caption-style talk transcript (.md) into a clean document PDF so
make-citation-card.py can highlight quotes on real-looking pages.
Usage: typeset-transcript.py input.md output.pdf "Title line" "Source line"
Prints the 1-based page number of any quote passed as extra args afterward.
"""
import re, sys
import fitz

inp, outp, title, source = sys.argv[1:5]
quotes = sys.argv[5:]

raw = open(inp).read().splitlines()
# join caption lines into flowing paragraphs; blank line or speaker tag starts new para
paras, cur = [], []
for ln in raw:
    s = ln.strip()
    if not s:
        if cur:
            paras.append(" ".join(cur)); cur = []
        continue
    cur.append(s)
    # end paragraph on sentence end + length heuristic
    if len(" ".join(cur)) > 700 and s.endswith((".", "?", "!")):
        paras.append(" ".join(cur)); cur = []
if cur:
    paras.append(" ".join(cur))

doc = fitz.open()
W, H = 612, 792  # letter
M = 64
page = doc.new_page(width=W, height=H)
y = M
# header
page.insert_text((M, y + 14), title, fontname="tibo", fontsize=15)
y += 26
page.insert_text((M, y + 10), source, fontname="tiit", fontsize=10, color=(.35, .35, .35))
y += 24
page.draw_line((M, y), (W - M, y), color=(.6, .6, .6), width=0.7)
y += 16

fs, lh = 10.5, 15.2
for para in paras:
    # wrap text manually
    words = para.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fitz.get_text_length(t, fontname="tiro", fontsize=fs) > W - 2 * M:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    need = len(lines) * lh + 8
    if y + need > H - M and len(lines) * lh < H - 2 * M:
        page = doc.new_page(width=W, height=H)
        y = M
    for ln in lines:
        if y > H - M:
            page = doc.new_page(width=W, height=H)
            y = M
        page.insert_text((M, y + fs), ln, fontname="tiro", fontsize=fs)
        y += lh
    y += 8

doc.save(outp)
print(f"{outp}: {len(doc)} pages")

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

d2 = fitz.open(outp)
for q in quotes:
    found = None
    nq = norm(q)[:120]
    for i, pg in enumerate(d2):
        if nq in norm(pg.get_text()):
            found = i + 1
            break
    print(f"page {found}: {q[:70]}...")
