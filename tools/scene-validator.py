#!/usr/bin/env python3
"""
Scene validator for V14/MCP-style HyperFrames video pipelines.

Catches the bug classes Terry shouldn't have to:
  A. Audio-vs-composition duration mismatch  → VO bleeds into next scene
  B. Animation event past composition end    → triggers fire after render done
  C. Dead-air gap at scene end                → visuals stop while VO continues
  D. data-duration attrs don't match comp     → audio/bg cut off early
  E. Empty render frames (bg-only stretches) → "no visuals except background"
  F. tl.call / known runtime bugs in lib      → silent timeline death

Run:  python3 tools/scene-validator.py <project-dir>
        e.g. python3 tools/scene-validator.py video-14-three-brains-one-router
             python3 tools/scene-validator.py agent-stack-series/01-mcp/hyperframes
"""
import json, re, sys, subprocess, pathlib, shlex
import argparse, statistics

GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def warn(msg):  print(f"{YELLOW}  ⚠  {msg}{RESET}")
def fail(msg):  print(f"{RED}  ✗  {msg}{RESET}")
def ok(msg):    print(f"{GREEN}  ✓  {msg}{RESET}")
def info(msg):  print(f"{DIM}  ·  {msg}{RESET}")

def media_duration(path):
    """Return duration in seconds via ffprobe, or None."""
    try:
        out = subprocess.run(
            ["ffprobe","-v","error","-show_entries","format=duration",
             "-of","default=noprint_wrappers=1:nokey=1",str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except Exception:
        return None

def parse_hf_json(p, html=None):
    """Composition duration from hyperframes.json (top-level OR compositions[0]),
    falling back to the largest data-duration in index.html (the root clip span).
    The legacy code only read compositions[0].duration, so the common top-level
    {"duration": N} shape returned None and the scene was silently dropped."""
    try:
        d = json.loads(pathlib.Path(p).read_text())
        if isinstance(d, dict):
            if d.get('duration'):
                return float(d['duration'])
            comps = d.get('compositions', [])
            if comps and comps[0].get('duration'):
                return float(comps[0]['duration'])
    except Exception:
        pass
    if html:
        durs = extract_data_durations(html)
        if durs:
            return max(durs)
    return None

def extract_data_durations(html):
    return [float(m.group(1)) for m in re.finditer(r'data-duration="([\d.]+)"', html)]

def extract_animation_ats(html):
    """Find all GSAP `at:` values + helper-call positional args.
    Returns list of (kind, at_value, est_duration). est_duration is taken
    from the same call's `duration:` if present, else 0.5."""
    events = []
    # Pattern 1: BT.helper(tl, ...|target, { at: N.NN, duration: D })  (duration optional)
    for m in re.finditer(
        r'BT\.(\w+)\s*\(\s*tl[^)]*?\bat\s*:\s*([\d.]+)\s*(?:,[^)]*?\bduration\s*:\s*([\d.]+))?',
        html, re.DOTALL):
        kind, at, dur = m.group(1), float(m.group(2)), float(m.group(3) or 0.6)
        events.append((kind, at, dur))
    # Pattern 2: tl.to/from/fromTo/set/add (..., position_at_end)
    for m in re.finditer(
        r'tl\.(to|from|fromTo|set|add)\s*\(([^)]*)\)',
        html, re.DOTALL):
        body = m.group(2)
        # Get last comma-arg as position; only accept bare numbers (skip objects)
        # Also try to find duration:
        dur_m = re.search(r'\bduration\s*:\s*([\d.]+)', body)
        dur = float(dur_m.group(1)) if dur_m else 0.3
        # Trailing numeric position is typical: ", 12.3)"
        pos_m = re.search(r',\s*([\d.]+)\s*$', body.rstrip())
        if pos_m:
            events.append((f"tl.{m.group(1)}", float(pos_m.group(1)), dur))
    return events

def check_lib_bugs(scene_dir, html=""):
    """Known runtime-killing patterns — but only if the lib is actually loaded.
    A byrd-transitions.js copied into lib/ but never <script>-included is inert,
    so flagging it is noise."""
    bugs = []
    if 'byrd-transitions' not in html:
        return bugs
    lib = scene_dir / 'lib' / 'byrd-transitions.js'
    if lib.exists():
        s = lib.read_text()
        if 'tl.call(' in s:
            bugs.append("tl.call(...) present in loaded byrd-transitions.js — throws in HyperFrames GSAP runtime")
    return bugs

def root_audio_durations(html):
    """data-duration on the ROOT composition clip and the <audio> tag only.
    Nested <video> B-roll clips legitimately have their own shorter durations,
    so they must NOT be compared against comp_dur."""
    durs = []
    m = re.search(r'data-composition-id="root"[^>]*?data-duration="([\d.]+)"', html)
    if m: durs.append(float(m.group(1)))
    for m in re.finditer(r'<audio\b[^>]*?data-duration="([\d.]+)"', html):
        durs.append(float(m.group(1)))
    return durs

def frame_variance_sweep(render_path, comp_dur, samples=None):
    """Render keyframes every 2s and report mean pixel std-dev.
    Returns list of (t_seconds, stddev). Low stddev ≈ near-uniform frame."""
    if not render_path.exists():
        return None
    samples = samples or max(int(comp_dur // 2), 3)
    out_dir = pathlib.Path('/tmp/v-sv') / render_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    # Clean previous samples
    for p in out_dir.glob('*.jpg'): p.unlink()
    cmd = ["ffmpeg","-y","-loglevel","error","-i",str(render_path),
           "-vf",f"fps=1/2,scale=320:-1",
           str(out_dir/"f%03d.jpg")]
    subprocess.run(cmd, check=False)
    out = []
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return None
    for jpg in sorted(out_dir.glob('*.jpg')):
        idx = int(jpg.stem.replace('f',''))
        t = (idx - 1) * 2.0
        im = Image.open(jpg).convert('L')
        std = ImageStat.Stat(im).stddev[0]
        out.append((t, std))
    return out

def find_render(scene_dir, render_dir, sn):
    """Newest scenes/NN/renders/*.mp4, else flat render_dir/{sn}.mp4."""
    rd = scene_dir / 'renders'
    if rd.exists():
        mp4s = sorted(rd.glob('*.mp4'), key=lambda p: p.stat().st_mtime)
        if mp4s:
            return mp4s[-1]
    if render_dir:
        cand = render_dir / f"{sn}.mp4"
        if cand.exists():
            return cand
    return None

def _ff_intervals(render, vf, label_start, label_end):
    """Run an ffmpeg detect filter and return (start,duration) pairs."""
    try:
        out = subprocess.run(
            ["ffmpeg","-hide_banner","-nostats","-i",str(render),
             "-vf",vf,"-an","-f","null","-"],
            capture_output=True, text=True).stderr
    except Exception:
        return []
    spans, cur = [], None
    for line in out.splitlines():
        m = re.search(label_start + r":\s*([\d.]+)", line)
        if m: cur = float(m.group(1))
        m = re.search(label_end + r":\s*([\d.]+)", line)
        if m and cur is not None:
            spans.append((cur, float(m.group(1)))); cur = None
    return spans

def render_qc(render, comp_dur):
    """Post-render checks tuned for the dark editorial aesthetic:
       - static holds >5s (freezedetect) — full-but-frozen compositions
       - true white frames (negate+blackdetect) — e.g. blank avatar head/tail
       - true black gaps (blackdetect, strict pix_th so dark navy bg is NOT flagged)
    Returns list of issue tuples."""
    issues = []
    # Static holds >5s (the "no static >5s" rule). freezedetect emits freeze_duration.
    freezes = _ff_intervals(render, "freezedetect=n=-50dB:d=5", "freeze_start", "freeze_duration")
    big = [(s, d) for (s, d) in freezes if d >= 5.0]
    if big:
        for s, d in big[:6]:
            fail(f"STATIC HOLD {d:.1f}s at {s:.1f}s (>5s rule) — add motion/B-roll/animation")
        issues.append(("static_hold", [(round(s,1), round(d,1)) for s, d in big]))
    # True white frames (blank): negate, then blackdetect on near-pure-white only.
    whites = _ff_intervals(render, "negate,blackdetect=d=0.06:pix_th=0.02", "black_start", "black_duration")
    if whites:
        for s, d in whites[:6]:
            fail(f"WHITE/BLANK FRAMES {d:.2f}s at {s:.1f}s — trim or cover (avatar head/tail?)")
        issues.append(("white_frames", [(round(s,2), round(d,2)) for s, d in whites]))
    # True black gaps only (strict pix_th=0.02 so the #0A0E14 navy bg is NOT flagged).
    blacks = _ff_intervals(render, "blackdetect=d=0.10:pix_th=0.02", "black_start", "black_duration")
    blacks = [(s, d) for (s, d) in blacks if d >= 0.10]
    if blacks:
        for s, d in blacks[:6]:
            fail(f"BLACK GAP {d:.2f}s at {s:.1f}s")
        issues.append(("black_gap", [(round(s,2), round(d,2)) for s, d in blacks]))
    return issues

def validate_scene(scene_dir, render_dir=None, sample_frames=False):
    sn = scene_dir.name
    print(f"\n{BOLD}🎬 {sn}{RESET}")
    html_path = scene_dir / 'index.html'
    hf_path   = scene_dir / 'hyperframes.json'
    if not html_path.exists():
        info("not a scene dir, skip"); return None
    html = html_path.read_text()
    comp_dur = parse_hf_json(hf_path, html) if hf_path.exists() else None
    if comp_dur is None:
        comp_dur = max(extract_data_durations(html), default=None)
    if comp_dur is None:
        # Real error — do NOT drop silently (legacy bug: bailed scenes vanished
        # from the summary, producing a false "ALL CLEAN").
        fail("could not determine composition duration (hyperframes.json + index.html)")
        return {"scene": sn, "issues": [("no_duration", True)], "comp_dur": None}
    info(f"composition duration = {comp_dur:.2f}s")

    issues = []
    # A scene backed by a full-duration <video> (avatar passthrough) is "alive"
    # for its whole length even if GSAP events stop early — don't flag dead air.
    video_durs = [float(m.group(1)) for m in re.finditer(r'<video\b[^>]*?data-duration="([\d.]+)"', html)]
    scene_is_video_backed = any(abs(v - comp_dur) < 1.5 for v in video_durs)

    # A. audio duration vs composition
    audio_files = list((scene_dir / 'assets').glob('scene-*.wav')) + \
                  list((scene_dir / 'assets').glob('audio.mp3')) + \
                  list((scene_dir / 'assets').glob('audio.wav'))
    audio_files = [a for a in audio_files if 'v1.' not in a.name and 'v6.' not in a.name and 'v8bak' not in a.name]
    if audio_files:
        ad = media_duration(audio_files[0])
        if ad is None:
            warn(f"could not probe {audio_files[0].name}")
        else:
            delta = ad - comp_dur
            if abs(delta) > 0.3:
                msg = f"audio {audio_files[0].name} = {ad:.2f}s, comp = {comp_dur:.2f}s, Δ {delta:+.2f}s"
                if delta > 0.5:
                    fail(f"VO BLEEDS PAST SCENE END: {msg}")
                    issues.append(("audio_overrun", delta))
                elif delta < -2.5:
                    fail(f"DEAD AIR AT END (audio short): {msg}")
                    issues.append(("audio_short", delta))
                else:
                    warn(f"audio/comp mismatch: {msg}")
                    issues.append(("audio_mismatch", delta))
            else:
                ok(f"audio matches comp ({ad:.2f}s vs {comp_dur:.2f}s)")

    # B. animation events past comp end
    events = extract_animation_ats(html)
    if events:
        overruns = [(k,t,d) for (k,t,d) in events if t + d > comp_dur + 0.1]
        if overruns:
            for k,t,d in overruns[:5]:
                fail(f"animation '{k}' at {t:.2f}+{d:.2f} = {t+d:.2f}s > comp {comp_dur:.2f}s")
            issues.append(("animation_overrun", len(overruns)))
        # C. dead-air gap at end (last anim event end vs comp end)
        last_end = max(t + d for (_,t,d) in events)
        gap = comp_dur - last_end
        if scene_is_video_backed:
            ok(f"video-backed scene — {gap:.2f}s GSAP gap covered by full-length video")
        elif gap > 2.5:
            fail(f"DEAD AIR: last anim ends at {last_end:.2f}s, comp ends at {comp_dur:.2f}s (gap {gap:.2f}s)")
            issues.append(("dead_air", gap))
        elif gap > 1.2:
            warn(f"end-of-scene gap {gap:.2f}s (last anim at {last_end:.2f})")
        else:
            ok(f"timeline ends within {gap:.2f}s of comp end")

    # D. stale data-duration attrs — only the root comp + audio (B-roll clips keep their own)
    durs = root_audio_durations(html)
    if durs:
        bad = [x for x in durs if abs(x - comp_dur) > 0.05]
        if bad:
            warn(f"stale root/audio data-duration: {bad} (expected {comp_dur})")
            issues.append(("stale_data_duration", bad))
        else:
            ok(f"root/audio data-duration matches comp ({len(durs)} checked)")

    # F. lib bugs
    bugs = check_lib_bugs(scene_dir, html)
    for b in bugs:
        fail(f"library bug: {b}")
        issues.append(("lib_bug", b))

    # F2. tl.call in scene HTML (silent timeline killer)
    tlcalls = len(re.findall(r'\btl\.call\b', html))
    if tlcalls > 0:
        fail(f"SCENE HTML has {tlcalls} tl.call(...) — will throw at runtime, kills timeline silently")
        issues.append(("scene_tl_call", tlcalls))

    # G. text overflow heuristic — wide text with white-space: nowrap may exceed 1920px
    # Parse CSS rules: class { ... font-size: NNNpx ... white-space: nowrap ... }
    css_rules = {}
    for m in re.finditer(r'\.(\w[\w\-]*)\s*\{([^}]*)\}', html):
        cls, body = m.group(1), m.group(2)
        fs = re.search(r'font-size:\s*(\d+)px', body)
        nowrap = 'white-space: nowrap' in body or re.search(r'white-space:\s*nowrap', body)
        if fs:
            css_rules[cls] = {'font_size': int(fs.group(1)), 'nowrap': bool(nowrap)}
    # Scan DOM elements with class -> text content
    for m in re.finditer(r'<(div|span|p|h[1-6])\b[^>]*class="([^"]*)"[^>]*>([^<]+)</\1>', html):
        classes = m.group(2).split()
        text = m.group(3).strip()
        # Merge font-size + nowrap across classes (use largest font, OR-ed nowrap)
        fs = 0; nowrap = False
        for c in classes:
            r = css_rules.get(c)
            if r:
                fs = max(fs, r['font_size'])
                nowrap = nowrap or r['nowrap']
        if not (fs and nowrap and text): continue
        # Heuristic: avg char width ≈ 0.55 * font_size for bold sans-serif
        est_w = len(text) * 0.55 * fs
        if est_w > 1920:
            warn(f"text-overflow risk: '{text[:40]}...' at {fs}px nowrap ≈ {int(est_w)}px wide (canvas 1920px)")
            issues.append(("text_overflow", text[:40]))

    # E. (optional) post-render checks — static holds, white/blank frames, black gaps,
    #    plus near-empty frame variance. Resolves the real render path (scenes/NN/renders/).
    if sample_frames:
        render = find_render(scene_dir, render_dir, sn)
        if not render:
            warn("no render found for frame checks (scenes/<scene>/renders/*.mp4)")
        else:
            issues.extend(render_qc(render, comp_dur))
            fv = frame_variance_sweep(render, comp_dur)
            if fv:
                stds = [s for _, s in fv]
                med = statistics.median(stds)
                low = [t for t, s in fv if s < med * 0.55]
                if len(low) >= 2:
                    fail(f"FRAMES NEAR-EMPTY at t≈{low} (std-dev far below median)")
                    issues.append(("empty_frames", low))

    if not issues:
        ok(f"{sn} clean ✨")
    return {"scene": sn, "issues": issues, "comp_dur": comp_dur}

def autofix_overruns(scene_dir, comp_dur):
    """Find BT.foo(tl, ..., { at: X, duration: D, ... }) where X+D > comp_dur
    and rewrite at: to fit. Skips tl.* method calls (harder to parse reliably)."""
    p = scene_dir / 'index.html'
    s = p.read_text()
    n_fixed = 0
    # Match: BT.helper(tl, <target?>, { ... at: X.XX ... duration: Y.YY ... })
    pat = re.compile(
        r"BT\.(\w+)\s*\(\s*tl[^)]*?\{[^}]*?\bat\s*:\s*([\d.]+)[^}]*?\bduration\s*:\s*([\d.]+)[^}]*?\}",
        re.DOTALL)
    out = []
    last = 0
    for m in pat.finditer(s):
        at_val = float(m.group(2)); dur_val = float(m.group(3))
        end = at_val + dur_val
        if end <= comp_dur + 0.05:
            continue  # fits
        new_at = max(0.0, comp_dur - dur_val - 0.05)
        # Replace `at: <oldval>` only in this match's span
        snippet = m.group(0)
        new_snippet = re.sub(rf"\bat\s*:\s*{re.escape(m.group(2))}",
                             f"at: {new_at:.2f}", snippet, count=1)
        # Compose
        out.append(s[last:m.start()])
        out.append(new_snippet)
        last = m.end()
        n_fixed += 1
    out.append(s[last:])
    if n_fixed:
        p.write_text(''.join(out))
    return n_fixed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", help="path to project root (containing scenes/)")
    ap.add_argument("--scenes-glob", default="scenes/*", help="glob for scene dirs")
    ap.add_argument("--render-dir", default="renders", help="path to rendered MP4s")
    ap.add_argument("--frames", action="store_true", help="also do post-render frame variance check")
    ap.add_argument("--fix", action="store_true", help="auto-fix BT.helper overrun animations in place")
    args = ap.parse_args()

    project = pathlib.Path(args.project_dir).resolve()
    render_dir = project / args.render_dir if (project / args.render_dir).exists() else None
    if not render_dir and args.frames:
        warn(f"--frames requested but {args.render_dir} not found")

    scenes = sorted(project.glob(args.scenes_glob))
    scenes = [s for s in scenes if (s/'index.html').exists()]
    if not scenes:
        print(f"No scenes found in {project}/{args.scenes_glob}")
        sys.exit(1)

    print(f"{BOLD}VALIDATING {len(scenes)} scenes in {project.name}{RESET}\n")

    results = []
    for sd in scenes:
        r = validate_scene(sd, render_dir, sample_frames=args.frames)
        if r: results.append(r)
        if args.fix and r:
            n = autofix_overruns(sd, r['comp_dur'])
            if n:
                print(f"  {DIM}[autofix] shifted {n} overrun(s) in {sd.name}{RESET}")

    # Summary
    print(f"\n{BOLD}═══ SUMMARY ═══{RESET}")
    total_issues = 0
    by_kind = {}
    for r in results:
        for kind, _ in r['issues']:
            total_issues += 1
            by_kind[kind] = by_kind.get(kind, 0) + 1
    if total_issues == 0:
        print(f"{GREEN}{BOLD}ALL CLEAN — {len(results)} scenes, 0 issues.{RESET}")
        sys.exit(0)
    print(f"{RED}{BOLD}{total_issues} issue(s) across {len([r for r in results if r['issues']])}/{len(results)} scenes{RESET}")
    for kind, n in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {kind}: {n}")
    sys.exit(1)

if __name__ == "__main__":
    main()
