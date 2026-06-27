#!/usr/bin/env python3
"""
Citation-card renderer for the Byrddynasty citation-pipeline.

Reads a manifest of cards and produces a 1920x1080 PNG per entry, with the named
quote highlighted on the underlying PDF page in AI-Explained style — yellow rect
+ green underline + hand-drawn jitter + small attribution corner.

The card can also render a whole page with no highlight (page_only: true) for
things like the Mercer "Talent Timebomb" stacked chart where the visual is the
citation.

Manifest format (YAML):

  defaults:
    out_dir: cards/
    width: 1920
    height: 1080
    paper_bg: "#F4F1EA"
    attribution_font: "Inter-Italic 22"

  cards:
    - id: c.aon-case-quote
      pdf: originals/companies/aon--q1-2026-earnings-call-case-on-ai-strategy.pdf
      page: 5
      quote: "winners in the application of AI will lead with a world-class people strategy"
      attribution: "Gregory C. Case, Aon Q1 2026 earnings call · May 1, 2026"

    - id: c.mercer-99pct
      pdf: originals/data-anchors/mercer--global-talent-trends-2026.pdf
      page: 25
      page_only: true
      attribution: "Mercer Global Talent Trends 2026, p.25"

CLI:
  make-citation-card.py --manifest cards.yaml
  make-citation-card.py --pdf X.pdf --page 5 --quote "..." --out card.png  (single)
  make-citation-card.py --manifest cards.yaml --only c.aon-case-quote      (filter)
  make-citation-card.py --manifest cards.yaml --dry-run                    (list)

Output: <out_dir>/<id>.png  plus <out_dir>/<id>.json sidecar with bbox metadata.
"""

import argparse
import json
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import fitz  # pymupdf
import yaml
from PIL import Image, ImageDraw, ImageFont
from rapidfuzz import fuzz

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

WIKI_ROOT = Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki")

# ------------------------------------------------------------------------------
# Style defaults
# ------------------------------------------------------------------------------

# Yellow highlight: warm, ~45% opacity, soft borders.
HIGHLIGHT_FILL_RGBA = (255, 230, 0, 115)
HIGHLIGHT_BORDER_RGBA = (220, 180, 0, 200)
# Green underline: a 3-px line under each highlighted text-line.
UNDERLINE_RGBA = (40, 160, 80, 230)
UNDERLINE_THICKNESS = 3
# Paper background for the 1920x1080 canvas.
PAPER_BG_DEFAULT = "#F4F1EA"
# Hand-drawn jitter so highlights don't read as algorithmic.
HIGHLIGHT_JITTER_PX = 2


@dataclass
class Defaults:
    out_dir: Path
    width: int = 1920
    height: int = 1080
    paper_bg: str = PAPER_BG_DEFAULT
    attribution_font: str = "Inter Italic 22"
    pdf_render_dpi: int = 200          # render PDF page at this DPI before scaling
    crop_pad_factor: float = 0.40      # 40% padding around quote bbox when zooming
    crop_min_pad_px: int = 220         # absolute minimum padding (rendered px) so
                                       # one-line highlights still show paragraph
    margin_px: int = 60                # outer margin on the 1920x1080 canvas
    attribution_corner_padding: int = 40


# ------------------------------------------------------------------------------
# Manifest loading
# ------------------------------------------------------------------------------


@dataclass
class CardSpec:
    id: str
    pdf: str
    page: Optional[int] = None
    quote: Optional[str] = None
    page_only: bool = False
    attribution: Optional[str] = None
    out: Optional[str] = None
    match_threshold: int = 80          # rapidfuzz partial-ratio threshold


def load_manifest(path: Path) -> tuple[Defaults, list[CardSpec]]:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    defaults = Defaults(out_dir=Path(raw.get("defaults", {}).get("out_dir", "cards")))
    for k, v in (raw.get("defaults") or {}).items():
        if hasattr(defaults, k):
            if k == "out_dir":
                setattr(defaults, k, Path(v))
            else:
                setattr(defaults, k, v)
    cards = [CardSpec(**c) for c in raw.get("cards", [])]
    return defaults, cards


# ------------------------------------------------------------------------------
# Text normalization (must match audit-quotes.ts behavior for consistency)
# ------------------------------------------------------------------------------

_SMART_SINGLE = dict.fromkeys(map(ord, "‘’‚‛"), "'")
_SMART_DOUBLE = dict.fromkeys(map(ord, "“”„‟"), '"')
_DASHES = dict.fromkeys(map(ord, "–—−"), "-")
_LIGATURES = {ord("ﬁ"): "fi", ord("ﬂ"): "fl"}
_SOFT_HYPHEN = ord("­")


def normalize(s: str) -> str:
    """Lowercase + alphanumeric-only. Identical to the JS audit normalizer."""
    s = s.translate(_SMART_SINGLE).translate(_SMART_DOUBLE).translate(_DASHES).translate(_LIGATURES)
    s = s.replace(chr(_SOFT_HYPHEN), "")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


# ------------------------------------------------------------------------------
# Quote location (pymupdf word boxes + rapidfuzz fuzzy match)
# ------------------------------------------------------------------------------


def find_quote_rects(page: "fitz.Page", quote: str, threshold: int = 80) -> list[fitz.Rect]:
    """
    Locate the bounding rects of the quoted text on a page.

    Strategy:
      1. Try pymupdf's native search_for() first (fast, handles smart quotes well).
      2. If that fails, walk word-by-word, build a sliding window of N normalized
         words, and find the contiguous span whose normalized concatenation has
         the highest partial-ratio against the normalized quote.
    """
    # Try native first — handles many cases. pymupdf 1.27 dropped the hit_max
    # kwarg; the call returns all hits by default which is fine for our use.
    hits = page.search_for(quote)
    if hits:
        return list(hits[:8])

    # Fuzzy fallback. word tuples: (x0, y0, x1, y1, "text", block_no, line_no, word_no)
    words = page.get_text("words")
    if not words:
        return []

    norm_quote = normalize(quote)
    if len(norm_quote) < 20:
        return []

    # Quote target length, used to size the search window.
    target_chars = len(norm_quote)
    # Build cumulative-normalized so we can slice quickly.
    norm_word_lens = [len(normalize(w[4])) for w in words]

    best_score = 0
    best_start = -1
    best_end = -1
    n = len(words)

    for start in range(n):
        running = 0
        for end in range(start, n):
            running += norm_word_lens[end]
            if running < target_chars * 0.6:
                continue
            if running > target_chars * 1.6:
                break
            # Score this window.
            window = "".join(normalize(words[w][4]) for w in range(start, end + 1))
            score = fuzz.partial_ratio(window, norm_quote)
            if score > best_score:
                best_score = score
                best_start = start
                best_end = end
            if score >= 97:
                break
        if best_score >= 97:
            break

    if best_score < threshold or best_start < 0:
        return []

    # Group consecutive words on the same line into per-line rects so multi-line
    # quotes get separate highlight boxes.
    rects_by_line: dict[tuple[int, int], fitz.Rect] = {}
    for i in range(best_start, best_end + 1):
        x0, y0, x1, y1, _txt, block, line, _wno = words[i]
        key = (block, line)
        r = fitz.Rect(x0, y0, x1, y1)
        if key in rects_by_line:
            rects_by_line[key].include_rect(r)
        else:
            rects_by_line[key] = r
    return list(rects_by_line.values())


# ------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------


def render_page(page: "fitz.Page", dpi: int) -> Image.Image:
    """Render PDF page as a PIL Image at the given DPI."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def union_rect(rects: list[fitz.Rect]) -> fitz.Rect:
    r = fitz.Rect(rects[0])
    for x in rects[1:]:
        r.include_rect(x)
    return r


def page_rect_to_image(rect: fitz.Rect, dpi: int) -> tuple[int, int, int, int]:
    scale = dpi / 72
    return (int(rect.x0 * scale), int(rect.y0 * scale), int(rect.x1 * scale), int(rect.y1 * scale))


def crop_with_padding(img: Image.Image, bbox: tuple[int, int, int, int], pad_factor: float, min_pad_px: int = 220) -> tuple[Image.Image, tuple[int, int]]:
    """Crop with `pad_factor` padding around the bbox (clamped to image bounds),
    enforcing a minimum absolute padding so narrow one-line highlights still
    show ~3-4 lines of surrounding paragraph context.
    Returns (cropped_img, (offset_x, offset_y)) so highlight coords can be
    translated into the cropped frame.
    """
    iw, ih = img.size
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    pad_x = max(int(bw * pad_factor), min_pad_px)
    pad_y = max(int(bh * pad_factor), min_pad_px)
    cx0 = max(0, x0 - pad_x)
    cy0 = max(0, y0 - pad_y)
    cx1 = min(iw, x1 + pad_x)
    cy1 = min(ih, y1 + pad_y)
    return img.crop((cx0, cy0, cx1, cy1)), (cx0, cy0)


def fit_into(canvas_w: int, canvas_h: int, page_img: Image.Image, margin: int) -> tuple[Image.Image, tuple[int, int], float]:
    """Resize page_img to fit inside (canvas_w - 2*margin, canvas_h - 2*margin) preserving aspect.
    Returns (resized_img, (paste_x, paste_y), scale).
    """
    avail_w = canvas_w - 2 * margin
    avail_h = canvas_h - 2 * margin
    iw, ih = page_img.size
    scale = min(avail_w / iw, avail_h / ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)
    resized = page_img.resize((new_w, new_h), Image.LANCZOS)
    paste_x = (canvas_w - new_w) // 2
    paste_y = (canvas_h - new_h) // 2
    return resized, (paste_x, paste_y), scale


def draw_highlights(canvas: Image.Image, rects_canvas: list[tuple[int, int, int, int]]) -> None:
    """Draw yellow filled rects + green underlines on the canvas. Each rect is
    given small ±N px jitter so the result reads as a hand-drawn highlight, not
    an algorithmic overlay."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rng = random.Random(0xC9A45A)  # deterministic per channel-id colour
    for x0, y0, x1, y1 in rects_canvas:
        # Padding around the text so the highlight doesn't kiss the glyph edges.
        pad = 4
        jx0 = x0 - pad + rng.randint(-HIGHLIGHT_JITTER_PX, HIGHLIGHT_JITTER_PX)
        jy0 = y0 - pad + rng.randint(-HIGHLIGHT_JITTER_PX, HIGHLIGHT_JITTER_PX)
        jx1 = x1 + pad + rng.randint(-HIGHLIGHT_JITTER_PX, HIGHLIGHT_JITTER_PX)
        jy1 = y1 + pad + rng.randint(-HIGHLIGHT_JITTER_PX, HIGHLIGHT_JITTER_PX)
        draw.rectangle([jx0, jy0, jx1, jy1], fill=HIGHLIGHT_FILL_RGBA, outline=HIGHLIGHT_BORDER_RGBA, width=2)
        # Underline along the bottom.
        uy = jy1 + 2
        draw.line([(jx0 + 4, uy), (jx1 - 4, uy)], fill=UNDERLINE_RGBA, width=UNDERLINE_THICKNESS)
    # Multiply blend would be ideal; PIL doesn't have it natively but alpha
    # composite gets close enough because the highlight is semi-transparent.
    composed = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    canvas.paste(composed.convert("RGB"))


def _load_attribution_font(size: int = 22) -> Optional[ImageFont.FreeTypeFont]:
    candidates = [
        "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        "/Library/Fonts/Inter-Italic.otf",
        "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return None


def draw_attribution(canvas: Image.Image, text: str, defaults: Defaults) -> None:
    font = _load_attribution_font(22)
    draw = ImageDraw.Draw(canvas)
    if font is None:
        # PIL's load_default isn't great but functional.
        font = ImageFont.load_default()
    pad = defaults.attribution_corner_padding
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = canvas.width - tw - pad
    y = canvas.height - th - pad
    draw.text((x, y), text, fill=(100, 100, 100), font=font)


# ------------------------------------------------------------------------------
# Main per-card render
# ------------------------------------------------------------------------------


def resolve_pdf_path(pdf: str) -> Path:
    p = Path(pdf)
    if not p.is_absolute():
        # Try relative to wiki root (originals/ paths).
        candidate = WIKI_ROOT / p
        if candidate.exists():
            return candidate
    return p


def render_card(spec: CardSpec, defaults: Defaults) -> dict:
    pdf_path = resolve_pdf_path(spec.pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        page_num = (spec.page or 1) - 1
        if page_num < 0 or page_num >= len(doc):
            raise ValueError(f"page {spec.page} out of range (doc has {len(doc)} pages)")
        page = doc[page_num]

        page_img = render_page(page, defaults.pdf_render_dpi)

        bbox_pdf: Optional[fitz.Rect] = None
        rects_pdf: list[fitz.Rect] = []
        if not spec.page_only and spec.quote:
            rects_pdf = find_quote_rects(page, spec.quote, spec.match_threshold)
            if not rects_pdf:
                # Soft-fail: render the whole page so the operator can see and fix.
                print(f"  ⚠️  {spec.id}: quote not located, falling back to whole-page render", file=sys.stderr)
                bbox_pdf = None
            else:
                bbox_pdf = union_rect(rects_pdf)

        # Decide what region of the page image to use.
        if bbox_pdf is not None:
            crop_box_img = page_rect_to_image(bbox_pdf, defaults.pdf_render_dpi)
            cropped, (off_x, off_y) = crop_with_padding(page_img, crop_box_img, defaults.crop_pad_factor, defaults.crop_min_pad_px)
            # Translate per-line highlight rects into the cropped image's frame.
            highlight_rects_img = []
            for r in rects_pdf:
                ix0, iy0, ix1, iy1 = page_rect_to_image(r, defaults.pdf_render_dpi)
                highlight_rects_img.append((ix0 - off_x, iy0 - off_y, ix1 - off_x, iy1 - off_y))
        else:
            cropped = page_img
            highlight_rects_img = []

        # Compose onto the 1920x1080 paper canvas.
        canvas = Image.new("RGB", (defaults.width, defaults.height), defaults.paper_bg)
        resized, paste_xy, scale = fit_into(defaults.width, defaults.height, cropped, defaults.margin_px)
        canvas.paste(resized, paste_xy)

        # Translate highlight rects into canvas coords.
        rects_canvas = []
        for x0, y0, x1, y1 in highlight_rects_img:
            rects_canvas.append((
                int(x0 * scale) + paste_xy[0],
                int(y0 * scale) + paste_xy[1],
                int(x1 * scale) + paste_xy[0],
                int(y1 * scale) + paste_xy[1],
            ))
        if rects_canvas:
            draw_highlights(canvas, rects_canvas)

        if spec.attribution:
            draw_attribution(canvas, spec.attribution, defaults)

        out_dir = defaults.out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = Path(spec.out) if spec.out else out_dir / f"{spec.id}.png"
        canvas.save(out_path, "PNG", optimize=True)

        meta = {
            "id": spec.id,
            "pdf": str(pdf_path),
            "page": spec.page,
            "quote": spec.quote,
            "page_only": spec.page_only,
            "attribution": spec.attribution,
            "out": str(out_path),
            "matched": bool(rects_pdf),
            "rects_canvas": rects_canvas,
        }
        with open(out_path.with_suffix(".json"), "w") as f:
            json.dump(meta, f, indent=2)
        return meta
    finally:
        doc.close()


# ------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest")
    ap.add_argument("--only", help="Comma-separated list of card ids to render")
    ap.add_argument("--pdf")
    ap.add_argument("--page", type=int)
    ap.add_argument("--quote")
    ap.add_argument("--attribution", default=None)
    ap.add_argument("--page-only", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--out-dir", default="cards")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.manifest:
        defaults, cards = load_manifest(Path(args.manifest))
        if args.only:
            wanted = {x.strip() for x in args.only.split(",")}
            cards = [c for c in cards if c.id in wanted]
    elif args.pdf and args.page:
        defaults = Defaults(out_dir=Path(args.out_dir))
        cards = [CardSpec(
            id=Path(args.pdf).stem + f"-p{args.page}",
            pdf=args.pdf, page=args.page, quote=args.quote,
            page_only=args.page_only or not args.quote,
            attribution=args.attribution, out=args.out,
        )]
    else:
        ap.error("provide --manifest or both --pdf and --page")

    if args.dry_run:
        for c in cards:
            print(f"  {c.id}  pdf={c.pdf}  page={c.page}  page_only={c.page_only}")
            print(f"    quote={(c.quote or '')[:80]}")
        print(f"\n[plan] {len(cards)} card(s) → {defaults.out_dir}")
        return

    ok, fail = 0, 0
    for c in cards:
        try:
            meta = render_card(c, defaults)
            ok += 1
            print(f"  ✓ {c.id}{'  (page-only)' if c.page_only else '  (matched)' if meta['matched'] else '  (fallback)'}")
        except Exception as e:
            fail += 1
            print(f"  ✗ {c.id}: {e}", file=sys.stderr)

    print(f"\n[done] ok={ok} fail={fail} out={defaults.out_dir}")


if __name__ == "__main__":
    main()
