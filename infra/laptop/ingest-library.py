#!/usr/bin/env python3
"""Library ingest: drop a document in ~/JARVIS-Library and JARVIS files it in the brain.

Put files in a subfolder named for the creator or topic (~/JARVIS-Library/Nate Herk/pack.pdf);
files at the top level go under "misc". Each new or changed PDF, markdown or text file is extracted
to jarvis-brain/raw/sources/<folder>/<name>.md and listed in raw/sources/PENDING.md. The server's
curator reads PENDING.md on its next 07:00 run and writes the knowledge into the wiki (a page per
creator in wiki/people/, plus tools and concepts pages where it fits), then clears the list.

Originals stay where you dropped them. The brain is text only.
Why here and not Dropbox: launchd jobs on macOS can't read Dropbox (TCC), but can read ~/JARVIS-Library.

Usage: ingest-library.py [--dry-run]"""
import hashlib
import os
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

HOME = Path.home()
LIBRARY = Path(os.environ.get("JARVIS_LIBRARY", HOME / "JARVIS-Library"))
BRAIN = Path(os.environ.get("JARVIS_BRAIN", HOME / "code/jarvis-brain"))
OUT = BRAIN / "raw/sources"
STATE = Path(os.environ.get("JARVIS_LIBRARY_STATE", HOME / ".local/state/jarvis/library-ingest.json"))
LOG = HOME / "Library/Logs/jarvis-library-ingest.log"
KINDS = {".pdf", ".md", ".txt", ".markdown"}
MAX_MB = 60


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:80] or "doc"


def extract(p: Path) -> tuple[str, int]:
    if p.suffix.lower() != ".pdf":
        return p.read_text(errors="replace"), 1
    from pypdf import PdfReader
    r = PdfReader(str(p))
    pages = [(pg.extract_text() or "").strip() for pg in r.pages]
    text = "\n\n".join(f"<!-- page {i + 1} -->\n{t}" for i, t in enumerate(pages) if t)
    return re.sub(r"[ \t]+\n", "\n", text), len(r.pages)


def main(argv) -> int:
    dry = "--dry-run" in argv
    LIBRARY.mkdir(exist_ok=True)
    readme = LIBRARY / "README.txt"
    if not readme.exists():
        readme.write_text("Drop PDFs, markdown or text files here, in a folder named for the creator or topic\n"
                          "(for example 'Nate Herk/'). Within the hour JARVIS copies the text into its brain;\n"
                          "the next morning the curator writes what matters into the wiki.\n")
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    new = []
    for p in sorted(LIBRARY.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in KINDS or p.name.startswith(".") or p == readme:
            continue
        if p.stat().st_size > MAX_MB * 2**20:
            log(f"skip {p.name}: over {MAX_MB} MB")
            continue
        h = hashlib.md5(p.read_bytes()).hexdigest()
        if h in state:
            continue  # already ingested (also catches the same file dropped twice)
        rel = p.relative_to(LIBRARY)
        group = slug(rel.parts[0]) if len(rel.parts) > 1 else "misc"
        dest = OUT / group / f"{slug(p.stem)}.md"
        if dry:
            print(f"would ingest {rel} -> {dest.relative_to(BRAIN)}")
            continue
        try:
            text, pages = extract(p)
        except Exception as e:
            log(f"FAIL {rel}: {type(e).__name__}: {e}")
            continue
        if len(text.strip()) < 200:
            log(f"skip {rel}: almost no text (a scanned PDF needs OCR first)")
            state[h] = {"file": str(rel), "skipped": "no text"}
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f"# {p.stem.replace('-', ' ').replace('_', ' ')}\n\n"
                        f"- source: {rel.parts[0] if len(rel.parts) > 1 else 'unsorted'} (from ~/JARVIS-Library; "
                        f"someone else's work: keep private, never republish)\n"
                        f"- original: ~/JARVIS-Library/{rel}\n- pages: {pages}\n"
                        f"- extracted: {date.today().isoformat()}\n\n{text}\n")
        state[h] = {"file": str(rel), "brain": str(dest.relative_to(BRAIN))}
        new.append(str(dest.relative_to(BRAIN)))
        log(f"ingested {rel} -> {dest.relative_to(BRAIN)} ({pages} pages, {len(text)} chars)")
    if new and not dry:
        pending = OUT / "PENDING.md"
        with pending.open("a") as fh:
            if fh.tell() == 0:
                fh.write("# New library documents for the curator\n\nThe curator clears this list after "
                         "writing them into the wiki.\n\n")
            fh.write("".join(f"- {n}\n" for n in new))
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=1))
        subprocess.run(["bash", str(BRAIN / "scripts/brain-sync.sh")], capture_output=True, timeout=180)
    elif not dry:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
