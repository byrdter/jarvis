#!/usr/bin/env python3
"""
visual-fidelity-check.py — proves a build MEANS something.

Companion gate to scene-validator.py (which proves a scene *renders*). This one
enforces knowledge/VISUAL-FIDELITY-RULES.md:

  RULE 1  every clip/still used in a scene must appear in the VISUALS-MAP for that scene
  RULE 4  animation density floor (content >=45 tl.to/tl.fromTo, avatar/cta >=35)
  RULE 5  borrowed-clip caps (<=2 per scene, <=25% of the video)
  RULE 6  no foreign bg-* imports from other episodes

Written after athlete-syndicates-b2b shipped a parrot under "athletes rented out
their faces" while the correct handshake clip sat unused in the library.

Usage:
    python3 visual-fidelity-check.py <project-dir> [--json]
Exit 0 = pass, 1 = fail.
"""
import json
import re
import sys
from pathlib import Path

DENSITY_FLOOR_CONTENT = 45
DENSITY_FLOOR_AVATAR = 35
BORROWED_PER_SCENE = 2
BORROWED_PCT_MAX = 0.25
MEDIA_EXT = {'.mp4', '.mov', '.webm', '.png', '.jpg', '.jpeg', '.webp'}
# assets that are scene plumbing, not story visuals
IGNORE = {'audio.mp3', 'transcript.json', 'avatar.mp4'}

RED, GRN, YEL, DIM, RST = '\033[31m', '\033[32m', '\033[33m', '\033[2m', '\033[0m'


def find_visuals_map(proj: Path):
    cands = list(proj.glob('VISUALS-MAP*.md')) + list(proj.glob('VISUAL-MAP*.md'))
    return cands[0] if cands else None


def scene_dirs(proj: Path):
    for hf in sorted(proj.glob('hyperframes*')):
        sc = hf / 'scenes'
        if sc.is_dir():
            return sorted([d for d in sc.iterdir() if d.is_dir()])
    return []


def is_avatar_scene(name: str) -> bool:
    n = name.lower()
    return any(k in n for k in ('avatar', 'cta', 'close', 'cold-open'))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    as_json = '--json' in sys.argv
    if not args:
        print('usage: visual-fidelity-check.py <project-dir>')
        return 2
    proj = Path(args[0]).expanduser().resolve()
    vmap_path = find_visuals_map(proj)
    if not vmap_path:
        print(f'{RED}FAIL{RST} no VISUALS-MAP*.md found in {proj}')
        return 1
    vmap = vmap_path.read_text(errors='ignore').lower()

    scenes = scene_dirs(proj)
    if not scenes:
        print(f'{RED}FAIL{RST} no hyperframes*/scenes/* found in {proj}')
        return 1

    failures, warnings, report = [], [], []
    total_clips = total_borrowed = 0

    for sd in scenes:
        name = sd.name
        adir = sd / 'assets'
        assets = []
        if adir.is_dir():
            assets = [p for p in adir.iterdir()
                      if p.suffix.lower() in MEDIA_EXT and p.name not in IGNORE]

        # RULE 1 — every asset must be named in the VISUALS-MAP.
        # Maps reference assets either by full filename OR by shorthand token
        # (BG-01, BR-02, GAP-A, C3/V5-C3). Resolve both so the gate doesn't
        # cry wolf — a noisy gate gets ignored, which is how this shipped.
        unspecified = []
        for a in assets:
            stem = a.stem.lower()
            if stem in vmap or a.name.lower() in vmap:
                continue
            if stem.rsplit('.', 1)[0] in vmap:
                continue
            # shorthand: bg-01_foo.png -> "bg-01"/"bg 01"; gap-a_x -> "gap-a";
            # br-03_y -> "br-03"; V5-C2.png -> "c2"/"v5-c2"
            m = re.match(r'^((?:bg|br|gap)-[a-z0-9]+)', stem)
            if m and (m.group(1) in vmap or m.group(1).replace('-', ' ') in vmap):
                continue
            m = re.match(r'^(?:[a-z0-9]+-)?(c\d+)$', stem)
            if m and (m.group(1) in vmap or stem in vmap):
                continue
            unspecified.append(a.name)

        # RULE 5 — borrowed clips (named <other-video>__something)
        borrowed = [a.name for a in assets if '__' in a.name]
        vids = [a for a in assets if a.suffix.lower() in {'.mp4', '.mov', '.webm'}]
        total_clips += len(vids)
        total_borrowed += len([b for b in borrowed if Path(b).suffix.lower() in {'.mp4', '.mov', '.webm'}])

        # RULE 6 — foreign bg-* imports
        foreign_bg = [a.name for a in assets
                      if '__bg-' in a.name.lower() or re.match(r'^[a-z0-9-]+__bg', a.name.lower())]

        # RULE 4 — animation density
        idx = sd / 'index.html'
        anims = 0
        if idx.is_file():
            html = idx.read_text(errors='ignore')
            anims = len(re.findall(r'tl\.(?:to|fromTo)\s*\(', html))
        floor = DENSITY_FLOOR_AVATAR if is_avatar_scene(name) else DENSITY_FLOOR_CONTENT

        row = {'scene': name, 'anims': anims, 'floor': floor,
               'unspecified': unspecified, 'borrowed': borrowed, 'foreign_bg': foreign_bg}
        report.append(row)

        if unspecified:
            failures.append(f'{name}: {len(unspecified)} asset(s) NOT in VISUALS-MAP -> {", ".join(unspecified[:4])}')
        if anims < floor:
            failures.append(f'{name}: animation density {anims} < floor {floor} (under-built)')
        if len(borrowed) > BORROWED_PER_SCENE:
            failures.append(f'{name}: {len(borrowed)} borrowed clips > cap {BORROWED_PER_SCENE}')
        if foreign_bg:
            failures.append(f'{name}: foreign bg import(s) -> {", ".join(foreign_bg)}')

    if total_clips:
        pct = total_borrowed / total_clips
        if pct > BORROWED_PCT_MAX:
            failures.append(f'PROJECT: {total_borrowed}/{total_clips} clips borrowed '
                            f'({pct:.0%}) > cap {BORROWED_PCT_MAX:.0%}')

    if as_json:
        print(json.dumps({'scenes': report, 'failures': failures}, indent=2))
        return 1 if failures else 0

    print(f'\n  visual-fidelity-check — {proj.name}')
    print(f'  {DIM}map: {vmap_path.name} · {len(scenes)} scenes{RST}\n')
    print(f'  {"scene":<40} {"anims":>6} {"spec?":>7} {"borrowed":>9}')
    print(f'  {"-"*40} {"-"*6} {"-"*7} {"-"*9}')
    for r in report:
        ok_anim = GRN if r['anims'] >= r['floor'] else RED
        ok_spec = GRN + 'ok' + RST if not r['unspecified'] else RED + f"{len(r['unspecified'])} bad" + RST
        print(f"  {r['scene']:<40} {ok_anim}{r['anims']:>6}{RST} {ok_spec:>16} {len(r['borrowed']):>9}")
    if total_clips:
        print(f"\n  borrowed clips: {total_borrowed}/{total_clips} ({total_borrowed/total_clips:.0%}, cap {BORROWED_PCT_MAX:.0%})")

    if failures:
        print(f'\n{RED}  FAIL ({len(failures)}){RST}')
        for f in failures:
            print(f'   ✗ {f}')
        print(f'\n  {DIM}See knowledge/VISUAL-FIDELITY-RULES.md{RST}\n')
        return 1
    print(f'\n{GRN}  PASS{RST} — every asset specified, density met, reuse within caps\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
