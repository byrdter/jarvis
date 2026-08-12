#!/usr/bin/env python3
"""
bed-review.py — turn a bed-source manifest into CONTACT SHEETS so drift can be seen.

WHY. `bed-source.py` returns correctly-licensed rows. Correctly-licensed is not on-topic.
`archival-search.py`'s own record: beat 10 (Pentium recall) returned `X86 Assembly.pdf` and
a smokeview user's guide — both real, both free, both useless. **A title is the first
filter; pixels are the second.** This builds the second one.

This is the same discipline as `shot-census.py`: the tool produces numbered sheets, a human
(or an agent that can read images) writes the verdicts. There is no classifier here on
purpose — the one time a detector was trusted on this pipeline it put a face ring on a
shirt sleeve.

    python3 bed-review.py --manifest bed-manifest.jsonl --outdir sheets/
    python3 bed-review.py --manifest m.jsonl --outdir s/ --section act3
    python3 bed-review.py --manifest m.jsonl --outdir s/ --reject rejects.txt --prune kept.jsonl

REJECT FILE FORMAT — one id per line, or ranges: `12`, `40-44`. Ids are the numbers burned
into the sheets. `--prune` then writes a manifest with those rows removed, so the reject
pass is reproducible and reviewable in diff.

Downloads thumbnails only (the `file` field). Nothing here is a licence to use an asset —
that is `tier` in the manifest, and CC-BY still needs attribution recorded.
"""
import argparse, io, json, os, pathlib, sys, urllib.request, concurrent.futures as cf

UA = {"User-Agent": "jarvis-video-research/1.0 (byrdter@auburn.edu)"}
G, R, Y, Z = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
COLS, THUMB, PAD = 8, 300, 26


def fetch(row, i, d):
    url = row.get("file")
    if not url:
        return None
    p = d / f"{i:04d}.jpg"
    if p.exists():
        return p
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            p.write_bytes(r.read())
        return p
    except Exception as e:  # noqa: BLE001
        print(f"  {Y}skip {i}{Z} {type(e).__name__}", file=sys.stderr)
        return None


def parse_ids(path):
    out = set()
    for ln in pathlib.Path(path).read_text().split():
        if "-" in ln:
            a, b = ln.split("-", 1)
            out |= set(range(int(a), int(b) + 1))
        elif ln.strip().isdigit():
            out.add(int(ln))
    return out


def main():
    ap = argparse.ArgumentParser(description="Contact sheets for a bed manifest.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--section", help="only this section")
    ap.add_argument("--tier", choices=["CLEAR", "FLAGGED"])
    ap.add_argument("--reject", help="file of ids to drop")
    ap.add_argument("--prune", help="write manifest minus rejects here")
    a = ap.parse_args()

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("needs Pillow:  python3 -m pip install Pillow")

    rows = [json.loads(l) for l in open(a.manifest) if l.strip()]
    for i, r in enumerate(rows, 1):
        r["_id"] = i
    sel = [r for r in rows
           if (not a.section or r.get("section") == a.section)
           and (not a.tier or r.get("tier") == a.tier)]
    if not sel:
        sys.exit("no rows matched")

    d = pathlib.Path(a.outdir)
    (d / "thumbs").mkdir(parents=True, exist_ok=True)
    print(f"fetching {len(sel)} thumbnails …")
    with cf.ThreadPoolExecutor(8) as ex:
        paths = list(ex.map(lambda r: fetch(r, r["_id"], d / "thumbs"), sel))

    live = [(r, p) for r, p in zip(sel, paths) if p]
    print(f"  {G}{len(live)}{Z} fetched, {R}{len(sel)-len(live)}{Z} unreachable")

    per = COLS * 6
    for s in range(0, len(live), per):
        chunk = live[s:s + per]
        rowsn = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * THUMB, rowsn * (THUMB + PAD)), (16, 16, 18))
        dr = ImageDraw.Draw(sheet)
        for k, (r, p) in enumerate(chunk):
            x, y = (k % COLS) * THUMB, (k // COLS) * (THUMB + PAD)
            try:
                im = Image.open(p).convert("RGB")
                im.thumbnail((THUMB, THUMB))
                sheet.paste(im, (x + (THUMB - im.width) // 2, y + (THUMB - im.height) // 2))
            except Exception:  # noqa: BLE001
                dr.rectangle([x, y, x + THUMB, y + THUMB], fill=(60, 20, 20))
            tag = f"{r['_id']} {r.get('section','')} {r.get('tier','')[:1]}"
            dr.text((x + 4, y + THUMB + 6), tag[:46], fill=(210, 210, 210))
        out = d / f"bed_{s//per+1:02d}.jpg"
        sheet.save(out, quality=86)
        print(f"  sheet → {out}")

    idx = d / "index.tsv"
    with open(idx, "w") as f:
        f.write("id\tsection\ttier\tlicense\tcreator\ttitle\turl\n")
        for r, _ in live:
            f.write("\t".join(str(r.get(k, "")).replace("\t", " ") for k in
                              ("_id", "section", "tier", "license", "creator", "title", "url")) + "\n")
    print(f"  index → {idx}")

    if a.reject and a.prune:
        drop = parse_ids(a.reject)
        kept = [r for r in rows if r["_id"] not in drop]
        with open(a.prune, "w") as f:
            for r in kept:
                r.pop("_id", None)
                f.write(json.dumps(r) + "\n")
        print(f"\n  rejected {len(drop)} → kept {len(kept)} → {a.prune}")


if __name__ == "__main__":
    main()
