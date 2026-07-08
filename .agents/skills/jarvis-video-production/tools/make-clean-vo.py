#!/usr/bin/env python3
"""
make-clean-vo.py — strip a VO-SCRIPT.md down to a clean, HeyGen-paste-ready script.

Channel standard (Terry's rule, 2026-07-08): every video needs a "clean" VO alongside
the annotated VO-SCRIPT.md. HeyGen records LITERALLY everything pasted into it, so the
clean version must contain ONLY spoken words — no [CITE-n], no [beat], no silence/stage
directions, and NO markdown emphasis (*, **, _, `) because HeyGen renders those as junk
symbols in the read. Numbers stay spelled-out (TTS), and letter-hyphenations like A-I /
U-S / C-E-O / I-B-E-W are intentional (HeyGen reads them as letters) — left untouched.

Per-scene blocks are preserved with a plain "SCENE NN — Title" label so Terry can copy one
scene at a time (per-scene recording is the cleaner split-pipeline path). The label lines are
obviously meta — paste only the paragraph text beneath each.

Usage:
    python3 make-clean-vo.py <VO-SCRIPT.md> [-o <output.md>]
    # default output: sibling VO-CLEAN.md
"""
import argparse
import os
import re
import sys

# --- strippers -------------------------------------------------------------

CITE_RE   = re.compile(r"\[CITE-[^\]]*\]", re.IGNORECASE)   # [CITE-1], [CITE-12]
BEAT_RE   = re.compile(r"\[beat\]", re.IGNORECASE)          # [beat]
BRACKET_STAGE_RE = re.compile(r"\[[^\]]*\]")                # any leftover [..] stage dir
EMPHASIS_CHARS = re.compile(r"[*_`]")                       # ** * _ ` -> gone
MULTISPACE_RE = re.compile(r"[ \t]{2,}")

# lines that are pure stage direction even after emphasis is stripped
STAGE_LINE_RE = re.compile(r"^\s*\[?\s*(?:\d+(?:\.\d+)?s\s*silence|\d+(?:\.\d+)?s|END)\s*\]?\s*$",
                           re.IGNORECASE)

SCENE_RE = re.compile(r"^##\s+SCENE\s+(.+?)\s*$", re.IGNORECASE)
# sections after the body that must be dropped entirely
STOP_HEADINGS = ("## CITE CARD CUES", "## FACT-CHECK", "## CITE-CARD")


def clean_line(line: str) -> str:
    line = CITE_RE.sub("", line)
    line = BEAT_RE.sub("", line)
    line = EMPHASIS_CHARS.sub("", line)
    line = BRACKET_STAGE_RE.sub("", line)      # kill any remaining [..]
    line = MULTISPACE_RE.sub(" ", line)
    # tidy space left before punctuation by a removed inline marker
    line = re.sub(r"\s+([,.;:!?…])", r"\1", line)
    return line.strip()


def convert(text: str) -> str:
    out_blocks = []          # list of (scene_label, [paragraph, ...])
    current_label = None
    current_paras = []
    buf = []                 # current paragraph line-accumulator

    def flush_para():
        if buf:
            joined = clean_line(" ".join(buf))
            if joined:
                current_paras.append(joined)
            buf.clear()

    def flush_scene():
        flush_para()
        if current_label is not None:
            out_blocks.append((current_label, list(current_paras)))
        current_paras.clear()

    started = False
    for raw in text.splitlines():
        stripped = raw.strip()

        # stop at the citation/fact-check appendix
        if any(stripped.upper().startswith(h) for h in STOP_HEADINGS):
            break

        m = SCENE_RE.match(raw)
        if m:
            flush_scene()
            started = True
            # normalize the scene label: drop leading "##", keep title + any AVATAR tag
            label = m.group(1).strip()
            current_label = "SCENE " + EMPHASIS_CHARS.sub("", label)
            continue

        if not started:
            continue  # skip title, front-matter, recording instructions

        if stripped.startswith(">"):        # blockquote channel-standard notes
            flush_para()
            continue
        if stripped.startswith("---"):      # scene divider rule
            flush_para()
            continue
        if not stripped:                    # blank line = paragraph break
            flush_para()
            continue

        # pure stage-direction line? (e.g. **[1.5s silence]**, [END])
        probe = EMPHASIS_CHARS.sub("", stripped)
        if STAGE_LINE_RE.match(probe):
            flush_para()
            continue

        buf.append(stripped)

    flush_scene()

    # render
    lines = [
        "# CLEAN HEYGEN SCRIPT — paste-ready (auto-generated from VO-SCRIPT.md)",
        "#",
        "# Paste ONLY the paragraphs under each SCENE label. No [beat]/[CITE]/emphasis to delete.",
        "# Numbers are pre-spelled for TTS (read as written). A-I / U-S / C-E-O hyphenation = letters.",
        "# Record each scene, leaving ~1.5s of silence between scenes (or deliver per-scene files).",
        "",
    ]
    for label, paras in out_blocks:
        lines.append("=" * 4 + " " + label + " " + "=" * 4)
        lines.append("")
        for p in paras:
            lines.append(p)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Strip VO-SCRIPT.md to a clean HeyGen script.")
    ap.add_argument("script", help="path to VO-SCRIPT.md")
    ap.add_argument("-o", "--out", help="output path (default: sibling VO-CLEAN.md)")
    args = ap.parse_args()

    if not os.path.isfile(args.script):
        sys.exit(f"not found: {args.script}")
    with open(args.script, encoding="utf-8") as fh:
        text = fh.read()

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.script)), "VO-CLEAN.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(convert(text))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
