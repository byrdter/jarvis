#!/usr/bin/env python3
"""make-photo-post.py — conduit-register PHOTO POSTS for Facebook (4:5, 1080x1350).

WHY THIS EXISTS
Facebook Content Monetization pays on PHOTO posts, not just reels (~40% of Meta's 2025
payout pool went to non-reels formats). Our pipeline already mass-produces the exact
artifact class that earns there and gets screenshotted: cream evidence cards, dark-navy
analysis panels, stat heroes, one-row-lit tables. Today those are intermediates we throw
away. This tool makes them a first-class deliverable.

The design contract is knowledge/CONDUIT-VISUAL-SYSTEM.md §2-§4, unchanged:
  * CREAM document register  (#F4F1EA) — EVIDENCE.  "this is on the record."
  * DARK navy panel register (#0A0E14) — ANALYSIS.  "this is what it means."
  * Both sit over a darkened, defocused photographic bed from asset-library.

WHAT IS DIFFERENT FROM VIDEO
The optimization target flips. Video is retention-gated; a Facebook photo is SHARE-gated.
So every card here is built around one forwardable claim, sourced on the face of the card,
legible at feed thumbnail size. No card carries a claim that isn't in a GROUNDED.md ledger.

THE TRUNCATION RULE (inherited from make-pullquote-card.py, and it is the point)
Auto-fit by stepping the type size down. If the text cannot fit at the minimum size this
tool EXITS WITH AN ERROR rather than abridging. A silently truncated citation is worse than
a missing one, because nothing announces it. Shortening a quote is a human decision.

THE BED LEDGER
`--ledger PATH` enforces one-bed-once across a batch (VISUAL SOURCING rule 1). A bed already
recorded in the ledger is refused. Reuse inside a batch is the single most visible tell that
content was mass-produced, and mass-produced is precisely what Meta demotes.

CARD TYPES
  quote    verbatim sentence + attribution              (cream default)
  dossier  label/value rows — a source, stated precisely (cream default)
  stat     one number is the point                       (dark default)
  pair     two findings in tension / a paradox           (dark default)
  ledger   three numbered findings                       (dark default)
  arrow    before -> after                               (dark default)

USAGE
  make-photo-post.py --type stat --bed <img> --out p01.png \
      --kicker "OPENAI · WORK AT THE FRONTIER" \
      --value "43.5%" \
      --caption "of non-generic work messages fall outside the user's own occupation" \
      --aside "Not 'AI took the job.' The job quietly took in someone else's work." \
      --source "OpenAI, How AI is expanding what people do at work, 27 Jul 2026"

Writes <out>.png and <out>.json (the sidecar: claim, source, verbatim flag, bed asset,
render settings) so a later pass can verify the card against PIXELS, not against a manifest
that merely asserts it.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- canvas + palette

W, H = 1080, 1350                 # 4:5 — the tallest photo Facebook renders in feed
MARGIN = 66                       # outer bleed to the panel edge
PAD = 58                          # panel edge to content

CREAM = (244, 241, 234)           # #F4F1EA  evidence register ground
INK = (20, 20, 20)
SUB_INK = (78, 78, 78)
RULE_CREAM = (201, 164, 90)       # muted gold rule on paper

NAVY = (10, 14, 20)               # #0A0E14  analysis register ground
PANEL = (18, 24, 33)              # the raised slate card
GOLD = (224, 184, 74)             # #E0B84A  primary accent
TEAL = (90, 209, 209)             # #5AD1D1  secondary accent
PAPER = (238, 238, 234)
MUTED = (150, 160, 172)
HAIRLINE = (52, 63, 78)

SERIF_B = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
           "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
SERIF = ["/System/Library/Fonts/Supplemental/Georgia.ttf",
         "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]
SERIF_I = ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
           "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf"]

KICKER_PT = 25
SOURCE_PT = 21
TRACK = 5                          # letterspacing for mono kickers, px


def font(cands, size):
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ---------------------------------------------------------------- text primitives

def tracked_w(d, text, f, track=TRACK):
    if not text:
        return 0
    return sum(d.textlength(c, font=f) for c in text) + track * (len(text) - 1)


def draw_tracked(d, xy, text, f, fill, track=TRACK):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return x


def wrap(d, text, f, max_w):
    """Greedy wrap. Also honours explicit \n."""
    out = []
    for para in text.split("\n"):
        lines, cur = [], ""
        for word in para.split():
            t = (cur + " " + word).strip()
            if d.textlength(t, font=f) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        out.extend(lines or [""])
    return out


def block(d, lines, f, x, y, fill, leading=1.24, align="left", max_w=None):
    lh = int(f.size * leading)
    for ln in lines:
        tx = x
        if align == "center" and max_w:
            tx = x + (max_w - d.textlength(ln, font=f)) / 2
        d.text((tx, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- the bed

def make_bed(path, register, blur=16, darken=0.34):
    """asset-library image -> 1080x1350, cover-cropped, defocused, scrimmed.

    Per CONDUIT §3 the bed must not compete with the card, but must not be crushed past
    the luminance floor either — a black rectangle is a dead frame, not a bed.
    """
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = max(W / sw, H / sh)
    new = (max(W, int(sw * scale + 0.5)), max(H, int(sh * scale + 0.5)))
    src = src.resize(new, Image.LANCZOS)
    left = (new[0] - W) // 2
    top = (new[1] - H) // 2
    bed = src.crop((left, top, left + W, top + H))
    bed = bed.filter(ImageFilter.GaussianBlur(blur))

    ground = NAVY if register == "dark" else (28, 26, 24)
    scrim = Image.new("RGB", (W, H), ground)
    bed = Image.blend(bed, scrim, 1.0 - darken)

    # vertical falloff so the kicker (top) and source line (bottom) always read
    grad = Image.new("L", (1, H))
    gp = grad.load()
    for y in range(H):
        t = y / (H - 1)
        edge = max(0.0, 1.0 - t / 0.22) if t < 0.22 else max(0.0, (t - 0.78) / 0.22)
        gp[0, y] = int(120 * edge)
    bed = Image.composite(Image.new("RGB", (W, H), ground), bed,
                          grad.resize((W, H)))
    return bed


def panel(img, register, opacity):
    """The raised card the content sits on."""
    d = ImageDraw.Draw(img, "RGBA")
    box = (MARGIN, MARGIN, W - MARGIN, H - MARGIN)
    if register == "cream":
        d.rectangle(box, fill=CREAM + (255,))
        d.rectangle(box, outline=(206, 199, 186, 255), width=2)
    else:
        d.rectangle(box, fill=PANEL + (int(255 * opacity),))
        d.rectangle(box, outline=HAIRLINE + (255,), width=2)
    return ImageDraw.Draw(img)


# ---------------------------------------------------------------- chrome

def theme(register):
    if register == "cream":
        return dict(head=INK, body=INK, sub=SUB_INK, kick=(120, 104, 70),
                    rule=RULE_CREAM, accent=RULE_CREAM, second=(96, 116, 128),
                    muted=(126, 122, 112), aside=(58, 58, 58))
    # `aside` sits between head and muted — the italic line under a stat is content, not
    # chrome, and MUTED grey lost it entirely at feed thumbnail size.
    return dict(head=PAPER, body=PAPER, sub=MUTED, kick=GOLD,
                rule=GOLD, accent=GOLD, second=TEAL, muted=MUTED, aside=(196, 203, 212))


def draw_kicker(d, text, t):
    """Letterspaced mono kicker, shrunk to fit. A kicker that overruns the panel edge is a
    defect the eye reads instantly at thumbnail size (FB-10 shipped one)."""
    inner = W - 2 * (MARGIN + PAD)
    label = text.upper()
    size = KICKER_PT
    f = font(MONO, size)
    while size > 15 and tracked_w(d, label, f) > inner:
        size -= 1
        f = font(MONO, size)
    if tracked_w(d, label, f) > inner:
        sys.exit(f"ERROR: kicker '{text}' does not fit at 15pt even letterspaced. "
                 f"Shorten it — the kicker is a label, not a sentence.")
    x = y = MARGIN + PAD
    draw_tracked(d, (x, y), label, f, t["kick"])
    d.rectangle([x, y + size + 20, x + 78, y + size + 23], fill=t["rule"])
    return y + size + 23 + 46


def draw_footer(d, source, t, mark="BYRDDYNASTY"):
    """Source line + wordmark, bottom-anchored. Returns the y the content must stop at.

    The rule is drawn ABOVE the wrapped block, not at a fixed offset — a two-line source
    used to get a hairline struck through it.
    """
    f = font(MONO, SOURCE_PT)
    x = MARGIN + PAD
    inner_w = W - 2 * (MARGIN + PAD)
    lh = int(SOURCE_PT * 1.38)
    mw = tracked_w(d, mark, f, 3)
    lines = wrap(d, source, f, inner_w - mw - 40)

    last_y = H - MARGIN - PAD - SOURCE_PT
    top_y = last_y - (len(lines) - 1) * lh
    rule_y = top_y - 30

    d.rectangle([x, rule_y, x + inner_w, rule_y + 1], fill=t["muted"])
    yy = top_y
    for ln in lines:
        d.text((x, yy), ln, font=f, fill=t["sub"])
        yy += lh
    draw_tracked(d, (W - MARGIN - PAD - mw, last_y), mark, f, t["muted"], 3)
    return rule_y


# ---------------------------------------------------------------- card types

def autofit(d, text, cands, max_w, max_h, hi, lo, step=3, leading=1.20):
    """Step type down until the wrapped block fits BOTH axes. Never truncates — returns None.

    The width check is not redundant with wrap(). wrap() force-places a token that is wider
    than the column rather than dropping it, so a single unbreakable string ("$14–$37") will
    silently run off the canvas at a large size while the height check happily passes. That
    shipped once — FB-08 rendered as "$14—$" with the rest outside the frame.
    """
    for s in range(hi, lo - 1, -step):
        f = font(cands, s)
        lines = wrap(d, text, f, max_w)
        if any(d.textlength(ln, font=f) > max_w for ln in lines):
            continue
        if len(lines) * int(s * leading) <= max_h:
            return f, lines, s
    return None


def fail(msg):
    sys.exit(f"ERROR: {msg}\n  This tool auto-fits and will NOT truncate. Shorten the text "
             f"deliberately, or split it across two cards.")


def settle(top, bottom, block_h, bias=0.38):
    """Place a block in the band, biased UP. True centering leaves a void under the kicker
    and reads as an unfinished frame at thumbnail size."""
    return top + max(0, int((bottom - top - block_h) * bias))


def card_quote(d, a, t, top, bottom):
    inner = W - 2 * (MARGIN + PAD)
    attrib = a.attribution or ""
    fa = font(SERIF, 28)
    a_lines = wrap(d, attrib, fa, inner) if attrib else []
    a_h = len(a_lines) * int(28 * 1.34) + (54 if a_lines else 0)

    q = a.value.strip()
    if not q.startswith(("“", '"')):
        q = f"“{q}”"
    fit = autofit(d, q, SERIF_B, inner, bottom - top - a_h, 104, 40, leading=1.22)
    if not fit:
        fail(f"quote does not fit at 40pt ({len(q)} chars)")
    f, lines, size = fit
    y = settle(top, bottom, a_h + len(lines) * int(size * 1.22), 0.44)
    y = block(d, lines, f, MARGIN + PAD, y, t["head"], 1.22)
    if a_lines:
        d.rectangle([MARGIN + PAD, y + 20, MARGIN + PAD + 92, y + 24], fill=t["rule"])
        block(d, a_lines, fa, MARGIN + PAD, y + 54, t["sub"], 1.34)
    return {"quote_pt": size, "lines": len(lines)}


def card_stat(d, a, t, top, bottom):
    inner = W - 2 * (MARGIN + PAD)
    fc = font(SERIF, 34)
    c_lines = wrap(d, a.caption, fc, inner) if a.caption else []
    fi = font(SERIF_I, 29)
    i_lines = wrap(d, a.aside, fi, inner) if a.aside else []
    tail = len(c_lines) * int(34 * 1.30) + (len(i_lines) * int(29 * 1.36) + 44 if i_lines else 0)

    fit = autofit(d, a.value, SERIF_B, inner, bottom - top - tail - 40, 310, 90, step=6, leading=1.06)
    if not fit:
        fail(f"stat value does not fit at 90pt ('{a.value}')")
    f, lines, size = fit
    y = settle(top, bottom, tail + len(lines) * int(size * 1.06) + 40, 0.34)
    y = block(d, lines, f, MARGIN + PAD, y, t["accent"], 1.06)
    y += 26
    if c_lines:
        y = block(d, c_lines, fc, MARGIN + PAD, y, t["head"], 1.30)
    if i_lines:
        y += 24
        d.rectangle([MARGIN + PAD, y, MARGIN + PAD + 3, y + len(i_lines) * int(29 * 1.36)],
                    fill=t["second"])
        block(d, i_lines, fi, MARGIN + PAD + 26, y, t["aside"], 1.36)
    return {"stat_pt": size}


def card_pair(d, a, t, top, bottom):
    """Two findings in tension. The left/right accents are the argument."""
    inner = W - 2 * (MARGIN + PAD)
    rows = a.rows
    if len(rows) != 2:
        fail(f"--type pair needs exactly 2 --row entries, got {len(rows)}")
    fk = font(MONO, 23)
    avail = bottom - top - 40
    half = avail // 2

    meta = []
    for i, (label, text) in enumerate(rows):
        col = t["accent"] if i == 0 else t["second"]
        fit = autofit(d, text, SERIF_B, inner - 8, half - 96, 62, 30, leading=1.24)
        if not fit:
            fail(f"pair row {i + 1} does not fit at 30pt")
        f, lines, size = fit
        # centre each half's own block so the two sides read as a balanced opposition
        blk = 23 + 26 + len(lines) * int(size * 1.24)
        y = top + i * half + max(0, (half - blk) // 2)
        draw_tracked(d, (MARGIN + PAD, y), label.upper(), fk, col, 4)
        block(d, lines, f, MARGIN + PAD, y + 23 + 26, t["head"], 1.24)
        meta.append(size)
        if i == 0:
            mid = top + half
            d.rectangle([MARGIN + PAD, mid, W - MARGIN - PAD, mid + 1],
                        fill=HAIRLINE if t["head"] == PAPER else (214, 207, 194))
    return {"pair_pt": meta}


def card_ledger(d, a, t, top, bottom):
    """Numbered findings. The instrument for 'here are the three things'."""
    inner = W - 2 * (MARGIN + PAD)
    rows = a.rows
    if not rows:
        fail("--type ledger needs at least one --row")
    fn = font(MONO, 30)
    fl = font(MONO, 22)
    slot = (bottom - top) // len(rows)
    y = top
    sizes = []
    for i, (label, text) in enumerate(rows):
        num = f"{i + 1:02d}"
        d.text((MARGIN + PAD, y + 4), num, font=fn, fill=t["accent"])
        xoff = MARGIN + PAD + 74
        if label:
            draw_tracked(d, (xoff, y + 8), label.upper(), fl, t["muted"], 4)
        yy = y + (36 if label else 0)
        fit = autofit(d, text, SERIF, inner - 74, slot - 54 - (36 if label else 0), 38, 24,
                      leading=1.28)
        if not fit:
            fail(f"ledger row {i + 1} does not fit at 24pt")
        f, lines, size = fit
        block(d, lines, f, xoff, yy, t["head"], 1.28)
        sizes.append(size)
        y += slot
        if i < len(rows) - 1:
            d.rectangle([MARGIN + PAD, y - 26, W - MARGIN - PAD, y - 25],
                        fill=HAIRLINE if t["head"] == PAPER else (214, 207, 194))
    return {"ledger_pt": sizes}


def card_arrow(d, a, t, top, bottom):
    """before -> after. The single most forwardable shape for a repricing."""
    inner = W - 2 * (MARGIN + PAD)
    if len(a.rows) != 2:
        fail(f"--type arrow needs exactly 2 --row entries (before, after), got {len(a.rows)}")
    fk = font(MONO, 23)
    fc = font(SERIF, 33)
    c_lines = wrap(d, a.caption, fc, inner) if a.caption else []
    tail = len(c_lines) * int(33 * 1.30) + (34 if c_lines else 0)

    (l0, v0), (l1, v1) = a.rows
    body_h = bottom - top - tail
    y = top + 8

    draw_tracked(d, (MARGIN + PAD, y), l0.upper(), fk, t["muted"], 4)
    y += 23 + 20
    fit0 = autofit(d, v0, SERIF_B, inner, 400, 104, 48, step=4, leading=1.14)
    if not fit0:
        fail(f"arrow 'before' value does not fit at 48pt ('{v0}')")
    f0, l0_lines, s0 = fit0
    y = block(d, l0_lines, f0, MARGIN + PAD, y, t["muted"], 1.14) + 10

    ax = MARGIN + PAD + 6
    d.rectangle([ax, y + 16, ax + 108, y + 21], fill=t["accent"])
    d.polygon([(ax + 104, y + 4), (ax + 136, y + 18), (ax + 104, y + 33)], fill=t["accent"])
    y += 62

    draw_tracked(d, (MARGIN + PAD, y), l1.upper(), fk, t["accent"], 4)
    y += 23 + 20
    room = top + body_h - y
    fit = autofit(d, v1, SERIF_B, inner, room, 205, 80, step=6, leading=1.08)
    if not fit:
        fail(f"arrow 'after' value does not fit at 80pt ('{v1}')")
    f1, lines, size = fit
    y = block(d, lines, f1, MARGIN + PAD, y, t["accent"], 1.08)
    if c_lines:
        block(d, c_lines, fc, MARGIN + PAD, y + 34, t["head"], 1.30)
    return {"arrow_pt": size}


def card_dossier(d, a, t, top, bottom):
    """Label/value rows — a source stated precisely. The credibility instrument."""
    inner = W - 2 * (MARGIN + PAD)
    y = top
    if a.value:
        fit = autofit(d, a.value, SERIF_B, inner, 300, 54, 30, leading=1.22)
        if not fit:
            fail("dossier title does not fit at 30pt")
        f, lines, size = fit
        y = block(d, lines, f, MARGIN + PAD, y, t["head"], 1.22) + 22
        d.rectangle([MARGIN + PAD, y, W - MARGIN - PAD, y + 2],
                    fill=HAIRLINE if t["head"] == PAPER else (214, 207, 194))
        y += 34

    fl = font(MONO, 22)
    label_w = 0
    for label, _ in a.rows:
        label_w = max(label_w, tracked_w(d, label.upper(), fl, 4))
    label_w = int(label_w) + 34
    fv = font(SERIF, 30)
    for label, text in a.rows:
        draw_tracked(d, (MARGIN + PAD, y + 6), label.upper(), fl, t["muted"], 4)
        lines = wrap(d, text, fv, inner - label_w)
        if y + len(lines) * int(30 * 1.28) > bottom:
            fail("dossier rows overflow the panel — drop a row or shorten the values")
        y = block(d, lines, fv, MARGIN + PAD + label_w, y, t["head"], 1.28) + 22
    return {"rows": len(a.rows)}


TYPES = {"quote": card_quote, "stat": card_stat, "pair": card_pair,
         "ledger": card_ledger, "arrow": card_arrow, "dossier": card_dossier}
DEFAULT_REGISTER = {"quote": "cream", "dossier": "cream", "stat": "dark",
                    "pair": "dark", "ledger": "dark", "arrow": "dark"}


# ---------------------------------------------------------------- bed ledger

def claim_bed(ledger_path, bed, out_name):
    if not ledger_path:
        return None
    p = Path(ledger_path)
    led = json.loads(p.read_text()) if p.exists() else {}
    key = Path(bed).name
    if key in led:
        sys.exit(f"ERROR: bed '{key}' was already used by '{led[key]}' in this batch.\n"
                 f"  VISUAL SOURCING rule 1 — one asset, once. Reuse inside a batch is the "
                 f"clearest signal of mass production, which is what Meta demotes.\n"
                 f"  Pick a different bed, or pass --no-ledger deliberately.")
    led[key] = out_name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(led, indent=2, sort_keys=True) + "\n")
    return key


# ---------------------------------------------------------------- main

def render(a):
    register = a.register or DEFAULT_REGISTER[a.type]
    img = make_bed(a.bed, register, blur=a.blur, darken=a.darken)
    d = panel(img, register, a.opacity)
    t = theme(register)

    top = draw_kicker(d, a.kicker, t) if a.kicker else MARGIN + PAD
    bottom = draw_footer(d, a.source, t) - 30
    meta = TYPES[a.type](d, a, t, top, bottom)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out, "PNG")
    return register, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True, choices=sorted(TYPES))
    ap.add_argument("--bed", required=True, help="asset-library image path")
    ap.add_argument("--out", required=True)
    ap.add_argument("--register", choices=["cream", "dark"], default=None)
    ap.add_argument("--kicker", default="", help="mono, letterspaced, uppercased")
    ap.add_argument("--value", default="", help="quote text / stat number / dossier title")
    ap.add_argument("--caption", default="")
    ap.add_argument("--aside", default="", help="italic line under a stat")
    ap.add_argument("--attribution", default="", help="quote byline")
    ap.add_argument("--row", action="append", default=[], metavar="LABEL::TEXT",
                    help="repeatable; 'LABEL::TEXT' for pair/ledger/arrow/dossier")
    ap.add_argument("--source", required=True, help="printed on the card face")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--claim-id", default="", help="GROUNDED card id, e.g. JD-C3")
    ap.add_argument("--verbatim", action="store_true", help="value is a verbatim quote")
    ap.add_argument("--blur", type=int, default=14)
    ap.add_argument("--darken", type=float, default=0.46, help="bed keep-fraction (0=black)")
    ap.add_argument("--opacity", type=float, default=0.90, help="dark panel opacity")
    ap.add_argument("--ledger", default="", help="bed-ledger JSON enforcing one-bed-once")
    ap.add_argument("--no-ledger", action="store_true")
    ap.add_argument("--caption-text", default="", help="the Facebook post copy, into the sidecar")
    a = ap.parse_args()

    a.rows = []
    for r in a.row:
        if "::" not in r:
            sys.exit(f"ERROR: --row must be 'LABEL::TEXT' (got: {r})")
        label, text = r.split("::", 1)
        a.rows.append((label.strip(), text.strip()))

    if not Path(a.bed).exists():
        sys.exit(f"ERROR: bed not found: {a.bed}")
    for bad in ("VisualStudioCode.png", "Scene1Image.png"):
        if Path(a.bed).name == bad:
            sys.exit(f"ERROR: {bad} is Terry's private data and must never be published.")

    bed_key = None if a.no_ledger else claim_bed(a.ledger, a.bed, Path(a.out).name)
    register, meta = render(a)

    side = Path(a.out).with_suffix(".json")
    side.write_text(json.dumps({
        "id": a.claim_id or Path(a.out).stem,
        "surface": "facebook-photo-post",
        "canvas": [W, H],
        "aspect": "4:5",
        "type": a.type,
        "register": register,
        "renderer": "jarvis-video-production/tools/make-photo-post.py",
        "kicker": a.kicker,
        "value": a.value,
        "caption": a.caption,
        "aside": a.aside,
        "attribution": a.attribution,
        "rows": [{"label": l, "text": x} for l, x in a.rows],
        "verbatim": bool(a.verbatim),
        "abridged": False,
        "source": a.source,
        "source_url": a.source_url,
        "bed": {"file": str(a.bed), "name": bed_key or Path(a.bed).name,
                "blur": a.blur, "darken": a.darken},
        "post_copy": a.caption_text,
        "render": meta,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"  {Path(a.out).name:<28} {a.type:<8} {register:<5} "
          f"bed={Path(a.bed).name:<38} {meta}")


if __name__ == "__main__":
    main()
