#!/usr/bin/env python3
"""
beatmap.py — derive a scene's BEAT MAP from the build, and detect drift.

WHY THIS EXISTS
The BEAT MAP comment at the top of each scene's index.html is the right artifact, but it was
hand-maintained *beside* the build, so it drifted — always one direction: the scene improves, the
doc doesn't. On the Messi V2 build the map described a design two revisions old (jersey #30 /
"THE INVESTOR" where the render showed #10 / "FORTUNE'S TENTH") and two beats present in the scene
were missing from the map entirely. Granularity also varied per scene, which makes any cross-scene
comparison of the maps meaningless.

This tool reads the timeline itself. The build is the source of truth; the map is generated.

MODES
  extract <scene-dir> [--json BEATMAP.json]   derive events, cluster, bind to VO words
  check   <scene-dir>                          compare the HTML comment against the derived map
  render  <scene-dir> [--write]                render a fresh BEAT MAP comment (--write edits HTML)

PARSING NOTES
- Helper signatures are LEARNED PER SCENE. `show/hide/rise/bed` happen to agree across the Messi
  scenes, but `fill` does NOT: S02 is fill(sel, t, dur, from) with time at index 1, S07 is
  fill(placeholder, newvalue, t) with time at index 2. Assuming a global signature silently
  misreads timings, so we read each scene's own `const NAME=(...)=>` definition and find which
  parameter is passed as the timeline position.
- Arguments are split with a brace/paren/string-aware scanner. A regex cannot survive the nested
  object literals these calls are full of.
"""

import argparse, json, os, re, sys
from pathlib import Path

CLUSTER_TOLERANCE = 0.25   # events within this window are one visual event
TIME_FNS = ("to", "fromTo", "set", "call", "add")


# ---------------------------------------------------------------- arg scanning

def split_args(src, open_idx):
    """Split the argument list of a call whose '(' is at open_idx.
    Returns (list_of_arg_strings, index_after_closing_paren) or (None, None)."""
    depth = 0
    args, cur = [], []
    i = open_idx
    quote = None
    while i < len(src):
        ch = src[i]
        if quote:
            cur.append(ch)
            if ch == "\\":
                if i + 1 < len(src):
                    cur.append(src[i + 1]); i += 2; continue
            elif ch == quote:
                quote = None
            i += 1; continue
        if ch in "\"'`":
            quote = ch; cur.append(ch); i += 1; continue
        if ch in "([{":
            depth += 1
            if depth == 1 and ch == "(":
                i += 1; continue          # don't record the outer paren
            cur.append(ch); i += 1; continue
        if ch in ")]}":
            depth -= 1
            if depth == 0 and ch == ")":
                args.append("".join(cur).strip())
                return [a for a in args if a != ""], i + 1
            cur.append(ch); i += 1; continue
        if ch == "," and depth == 1:
            args.append("".join(cur).strip()); cur = []; i += 1; continue
        cur.append(ch); i += 1
    return None, None


NUM_RE = re.compile(r'^[-+]?\d*\.?\d+$')

def as_time(expr):
    """Resolve an argument to a float when it is a plain numeric literal or a simple
    numeric arithmetic expression. Returns (value|None, raw)."""
    e = expr.strip()
    if NUM_RE.match(e):
        return float(e), e
    # Math.max(0, <num>) / Math.min(...) — take the numeric operand
    m = re.match(r'^Math\.(?:max|min)\s*\(\s*[-+]?[\d.]+\s*,\s*(.+?)\s*\)$', e)
    if m:
        v, _ = as_time(m.group(1))
        return v, e
    # simple arithmetic on literals: 12.4+.08 , 3.9 - 0.26
    if re.match(r'^[\d.\s+\-*/()]+$', e):
        try:
            return float(eval(e, {"__builtins__": {}}, {})), e   # literals only
        except Exception:
            return None, e
    return None, e


# ---------------------------------------------------------------- scene parsing

def script_body(html):
    """Everything from the timeline construction onward (skip CSS/markup)."""
    for anchor in ("gsap.timeline", "window.__timelines"):
        i = html.find(anchor)
        if i != -1:
            return html[i:], i
    return html, 0


def learn_helpers(body):
    """Find `const NAME=(p1,p2,...)=>` and determine which param index carries the
    timeline position, by seeing which param name is used as the position argument of a
    tl.<fn>(...) call inside the helper body."""
    helpers = {}
    for m in re.finditer(r'const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>', body):
        name, params = m.group(1), [p.split("=")[0].strip() for p in m.group(2).split(",") if p.strip()]
        # helper body = to the end of the statement (heuristic: next `};` or `;\n`)
        tail = body[m.end(): m.end() + 700]
        pos_idx = None
        for tm in re.finditer(r'\btl\.(%s)\s*\(' % "|".join(TIME_FNS), tail):
            args, _ = split_args(tail, tm.end() - 1)
            if not args:
                continue
            last = args[-1]
            for idx, p in enumerate(params):
                if re.search(r'\b%s\b' % re.escape(p), last):
                    pos_idx = idx; break
            if pos_idx is not None:
                break
        if pos_idx is not None:
            helpers[name] = {"params": params, "time_index": pos_idx}
    return helpers


def trailing_comment(src, end_idx):
    """Capture a // or /* */ comment on the same line as the call."""
    line_end = src.find("\n", end_idx)
    seg = src[end_idx: line_end if line_end != -1 else len(src)]
    m = re.search(r'/\*(.+?)\*/|//\s*(.+)$', seg)
    if not m:
        return None
    txt = (m.group(1) or m.group(2) or "").strip()
    return txt or None


def target_of(args):
    """First string-literal argument = the element/selector this event acts on."""
    for a in args:
        m = re.match(r'''^\s*['"`](.+?)['"`]''', a)
        if m:
            return m.group(1)
    return None


def helper_spans(body, helpers):
    """Byte ranges of each `const NAME=(...)=>...` definition body. tl.* calls inside these are
    the helper's own implementation — their position argument is the parameter `t`, not a real
    timeline position. Counting them as unresolved call sites is double-counting."""
    spans = []
    for name in helpers:
        for m in re.finditer(r'const\s+%s\s*=\s*\([^)]*\)\s*=>' % re.escape(name), body):
            start = m.end()
            # definition ends at the first `};` (block form) or `;` at depth 0 (expression form)
            depth, i = 0, start
            while i < len(body):
                c = body[i]
                if c in "({[": depth += 1
                elif c in ")}]": depth -= 1
                elif c == ";" and depth <= 0:
                    break
                i += 1
            spans.append((start, i))
    return spans


def in_spans(idx, spans):
    return any(a <= idx <= b for a, b in spans)


def extract_events(scene_dir):
    p = Path(scene_dir) / "index.html"
    html = p.read_text(encoding="utf-8", errors="ignore")
    body, offset = script_body(html)
    helpers = learn_helpers(body)
    spans = helper_spans(body, helpers)
    events, unresolved = [], 0

    # direct tl.<fn>(...) calls — skipping helper implementation bodies
    for m in re.finditer(r'\btl\.(%s)\s*\(' % "|".join(TIME_FNS), body):
        if in_spans(m.start(), spans):
            continue
        args, after = split_args(body, m.end() - 1)
        if not args or after is None:
            continue
        t, raw = as_time(args[-1]) if len(args) >= 2 else (None, "")
        if t is None:
            unresolved += 1; continue
        events.append({"t": round(t, 3), "kind": "tl." + m.group(1),
                       "target": target_of(args), "note": trailing_comment(body, after)})

    # helper calls, using each scene's learned signature
    if helpers:
        for m in re.finditer(r'(?<![\w.])(%s)\s*\(' % "|".join(map(re.escape, helpers)), body):
            name = m.group(1)
            # skip the definition itself
            if re.search(r'const\s+%s\s*=\s*$' % re.escape(name), body[max(0, m.start()-30):m.start()]):
                continue
            args, after = split_args(body, m.end() - 1)
            if not args or after is None:
                continue
            idx = helpers[name]["time_index"]
            if idx >= len(args):
                unresolved += 1; continue
            t, raw = as_time(args[idx])
            if t is None:
                unresolved += 1; continue
            events.append({"t": round(t, 3), "kind": name,
                           "target": target_of(args), "note": trailing_comment(body, after)})

    events.sort(key=lambda e: e["t"])
    return events, helpers, unresolved


# ---------------------------------------------------------------- VO binding

def load_words(scene_dir):
    for name in ("transcript.json",):
        p = Path(scene_dir) / "assets" / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            words = data.get("words") if isinstance(data, dict) else data
            out = []
            for w in words or []:
                s = w.get("start", w.get("s"))
                t = w.get("word", w.get("text", w.get("w", "")))
                if s is not None:
                    out.append((float(s), str(t)))
            return out
    return []


def phrase_at(words, t, span=6):
    """The VO phrase running at time t — the word at t plus a few following."""
    if not words:
        return None
    idx = 0
    for i, (s, _) in enumerate(words):
        if s <= t:
            idx = i
        else:
            break
    return " ".join(w for _, w in words[idx: idx + span]).strip() or None


def cluster(events, words, tol=CLUSTER_TOLERANCE):
    """Group near-simultaneous tweens into ONE visual event. 866 tl calls must not
    become 866 beat lines — the granularity contract is one line per visual event."""
    out = []
    for e in events:
        if out and e["t"] - out[-1]["t"] <= tol:
            g = out[-1]
            g["calls"] += 1
            if e["target"] and e["target"] not in g["targets"]:
                g["targets"].append(e["target"])
            if e["note"] and not g["note"]:
                g["note"] = e["note"]
        else:
            out.append({"t": e["t"], "calls": 1,
                        "targets": [e["target"]] if e["target"] else [],
                        "note": e["note"]})
    for g in out:
        g["cue"] = phrase_at(words, g["t"])
        g["den_atm"] = None      # filled by a human / the reconciliation pass
    return out



# ---------------------------------------------------------------- DEN / ATM seeding

# Atmospheric = the beat only touches bed / ambient / effect layers. Denotative = it touches
# something that carries the claim (a card, table, chart, chip, label, number, landing line).
# This is a SEED, not truth: a human corrects it. See CONDUIT-VISUAL-SYSTEM.md 6.
ATM_RE = re.compile(r'(^|[#.\s])(bg[A-Z_]|bg$|bgwrap|bed[A-Z]?|amb[A-Z]?|part(icle)?|scrim|vig|'
                    r'grain|glow|flash|sweep|haze|dust|fog|noise)', re.I)

def classify_target(t):
    if not t:
        return None
    return "ATM" if ATM_RE.search(t) else "DEN"

def seed_den_atm(beats):
    """A cluster is DEN if ANY of its targets carries content; ATM only if targets exist and
    every one is a bed/ambient layer; UNKNOWN when we cannot see a target at all."""
    for b in beats:
        kinds = [classify_target(t) for t in b["targets"]]
        kinds = [k for k in kinds if k]
        if not kinds:
            b["den_atm"] = None
        elif "DEN" in kinds:
            b["den_atm"] = "DEN"
        else:
            b["den_atm"] = "ATM"
    return beats

def den_atm_summary(beats, dur):
    """Count-weighted AND duration-weighted. The 90/10 rule in CONDUIT-VISUAL-SYSTEM.md 6 is
    about RUNTIME, so the duration-weighted figure is the one that matters; each beat is held
    until the next one starts."""
    n = {"DEN": 0, "ATM": 0, None: 0}
    held = {"DEN": 0.0, "ATM": 0.0, None: 0.0}
    for i, b in enumerate(beats):
        end = beats[i + 1]["t"] if i + 1 < len(beats) else (dur or b["t"])
        n[b["den_atm"]] += 1
        held[b["den_atm"]] += max(0.0, end - b["t"])
    tot_t = sum(held.values()) or 1.0
    return {
        "counts": {"DEN": n["DEN"], "ATM": n["ATM"], "unknown": n[None]},
        "runtime_seconds": {k or "unknown": round(v, 2) for k, v in held.items()},
        "denotative_pct_by_runtime": round(held["DEN"] / tot_t * 100, 1),
        "atmospheric_pct_by_runtime": round(held["ATM"] / tot_t * 100, 1),
        "unknown_pct_by_runtime": round(held[None] / tot_t * 100, 1),
        "_note": ("SEEDED HEURISTICALLY from target selectors, not verified. The 90/10 rule is "
                  "runtime-based; unknown% is un-classified, so treat DEN% as a floor."),
    }



# ---------------------------------------------------------------- ghosted-placeholder device

# The channel's signature move (CONDUIT-VISUAL-SYSTEM.md 5): unrevealed rows are VISIBLE BUT
# DIMMED, then resolve. It tells the viewer how much is still coming. It was invented at the
# bench on the Messi build and written down nowhere, so nothing could check it.
# Detectable: an element whose resting CSS opacity is in the ghost band, which the timeline later
# raises toward 1. Elements that never resolve are deliberate permanent ghosts (an unknown slot).
#
# KNOWN LIMITATION: resolve-detection matches the CSS selector against the tween target, so a
# CLASS-based group (.pgrow, .ctrow) whose rows are actually animated by id (#pg1, #pg2) reports
# as "permanent" when it does in fact resolve. The inventory is reliable; the resolve/permanent
# split under-reports resolution for class groups. Read "permanent" as "no direct resolve found",
# not as proof. Fixing it needs id->class mapping from the markup.
GHOST_LO, GHOST_HI = 0.05, 0.60
GHOST_FLOOR = 0.40          # below this over a dark panel it disappears rather than teases
RESOLVE_LIMIT = 1.2         # a ghosted state held longer than this reads as a dead frame

CSS_RULE_RE = re.compile(r'([#.][\w][\w\-. #>:()\[\]="\']*?)\s*\{([^}]*)\}')
OPACITY_RE = re.compile(r'(?<![\w-])opacity\s*:\s*([0-9]*\.?[0-9]+)')

def find_ghosts(scene_dir):
    html = (Path(scene_dir) / "index.html").read_text(encoding="utf-8", errors="ignore")
    css = "\n".join(re.findall(r'<style>(.*?)</style>', html, re.S))
    body, _ = script_body(html)
    ghosts = {}
    for m in CSS_RULE_RE.finditer(css):
        sel, decl = m.group(1).strip(), m.group(2)
        om = OPACITY_RE.search(decl)
        if not om:
            continue
        val = float(om.group(1))
        if GHOST_LO <= val <= GHOST_HI:
            ghosts[sel] = {"selector": sel, "css_opacity": val, "resolves_at": None,
                           "below_floor": val < GHOST_FLOOR}
    # when does the timeline raise it toward 1?
    for sel, g in ghosts.items():
        key = sel.lstrip("#.").split()[0].split(":")[0]
        best = None
        for m in re.finditer(r'\btl\.(to|fromTo)\s*\(', body):
            args, after = split_args(body, m.end() - 1)
            if not args or len(args) < 2:
                continue
            if key not in args[0]:
                continue
            if not re.search(r'opacity\s*:\s*(1|\.9\d|0?\.[6-9]\d?)\b', args[-2]):
                continue
            t, _ = as_time(args[-1])
            if t is not None and (best is None or t < best):
                best = t
        # helper reveals (show/rise/fill) also resolve a ghost
        for hm in re.finditer(r'(?<![\w.])(show|rise|fill)\s*\(', body):
            args, after = split_args(body, hm.end() - 1)
            if not args or key not in args[0]:
                continue
            for a in args[1:]:
                t, _ = as_time(a)
                if t is not None and (best is None or t < best):
                    best = t
                    break
        g["resolves_at"] = round(best, 2) if best is not None else None
    return list(ghosts.values())


# ---------------------------------------------------------------- output

def duration_of(scene_dir):
    p = Path(scene_dir) / "hyperframes.json"
    if p.exists():
        j = json.loads(p.read_text())
        return j.get("duration") or (j.get("compositions") or [{}])[0].get("duration")
    return None


# Preservation is DEFAULT-KEEP. A first attempt matched only FACTS/RIGHTS/LIKENESS prefixes and
# silently dropped authored lines in 7 of 14 scenes — including S09's "LIKENESS: no Messi/Mbappe
# photo or face", S12's "NO avatar in this faceless cut", S11's "NO platform logos". Those are
# exactly the lines that must survive. A machine cannot tell an important constraint from a stray
# note, so it keeps everything it did not itself generate.
BEAT_LINE_RE = re.compile(r'^\s*\d{1,3}\.\d')
# NB: do NOT add constraint prefixes here. LIKENESS-FREE: was briefly in this list and it
# deleted the likeness rule from 7 scenes. Only the generator's own header lines belong.
OLD_HEADER_RE = re.compile(r'^\s*(BEAT MAP —|BEAT MAP \(|\(VO-anchored|re-run `beatmap|scene=\S)', re.I)

def preserved_human_lines(old):
    """Keep every line the generator did not produce: constraints, semantic beat names, notes.
    Drops only beat-entry lines (a leading timestamp) and the previous generated header."""
    if not old:
        return []
    keep = []
    for ln in old.splitlines():
        s = ln.rstrip()
        if not s.strip():
            continue
        if BEAT_LINE_RE.match(s) or OLD_HEADER_RE.match(s):
            continue
        if s.strip().startswith("--- AUTHORED CONSTRAINTS"):
            continue
        keep.append(s.strip())
    return keep


def render_comment(scene, beats, dur, preserved=None):
    lines = [f"BEAT MAP — GENERATED from the build by tools/beatmap.py. Do not hand-edit;",
             f"re-run `beatmap.py render {scene} --write` after changing the timeline.",
             f"scene={scene}  duration={dur}s  visual-events={len(beats)}"
             + (f"  DEN {den_atm_summary(beats,dur)['denotative_pct_by_runtime']}% / ATM "
                f"{den_atm_summary(beats,dur)['atmospheric_pct_by_runtime']}% of runtime (seeded)")
             + (f"  timeline-events/min={len(beats)/dur*60:.1f}" if dur else "")]
    for b in beats:
        cue = f'  "{b["cue"]}"' if b["cue"] else ""
        tg = (" · " + ", ".join(b["targets"][:3])) if b["targets"] else ""
        note = f"   [{b['note']}]" if b["note"] else ""
        tag = {"DEN": " DEN", "ATM": " ATM"}.get(b["den_atm"], " ?  ")
        lines.append(f'{b["t"]:7.2f}{tag} ({b["calls"]:>2} tween{"s" if b["calls"]!=1 else " "}){tg}{note}{cue}')
    if preserved:
        lines.append("")
        lines.append("--- AUTHORED (preserved verbatim; beatmap.py never generates or edits these) ---")
        lines.extend(preserved)
    return "\n".join(lines)


def existing_comment(scene_dir):
    html = (Path(scene_dir) / "index.html").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<!--\s*(BEAT MAP.*?)-->', html, re.S)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["extract", "check", "render", "ghosts"])
    ap.add_argument("scene_dir")
    ap.add_argument("--json", help="write BEATMAP.json here (default: <scene>/BEATMAP.json)")
    ap.add_argument("--write", action="store_true", help="render mode: rewrite the HTML comment")
    ap.add_argument("--tol", type=float, default=CLUSTER_TOLERANCE)
    a = ap.parse_args()

    sd = Path(a.scene_dir)
    if not (sd / "index.html").exists():
        sys.exit(f"no index.html in {sd}")

    events, helpers, unresolved = extract_events(sd)
    words = load_words(sd)
    beats = seed_den_atm(cluster(events, words, a.tol))
    dur = duration_of(sd)
    scene = sd.name

    if a.mode == "extract":
        out = {"scene": scene, "duration": dur,
               "helpers_learned": helpers,
               "raw_calls": len(events), "unresolved_positions": unresolved,
               "visual_events": len(beats),
               "timeline_events_per_min": round(len(beats) / dur * 60, 1) if dur else None,
               "_metric_note": ("timeline_events_per_min counts CLUSTERED TIMELINE EVENTS from the "
                                "build. It is NOT the ffmpeg scene-detect change-events/min figure "
                                "in CONDUIT-VISUAL-SYSTEM.md 7 (45-60 target). Different measures; "
                                "do not compare them. Conflating two granularities is the bug that "
                                "created this tool."),
               "den_atm": den_atm_summary(beats, dur),
               "beats": beats}
        dest = Path(a.json) if a.json else sd / "BEATMAP.json"
        dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{scene}: {len(events)} timed calls -> {len(beats)} visual events"
              + (f", {len(beats)/dur*60:.1f} timeline-events/min" if dur else "")
              + (f"  [{unresolved} unresolved]" if unresolved else ""))
        print(f"  helpers learned: " + (", ".join(f"{k}(t@{v['time_index']})" for k, v in helpers.items()) or "none"))
        print(f"  wrote {dest}")

    elif a.mode == "render":
        block = render_comment(scene, beats, dur, preserved_human_lines(existing_comment(sd)))
        if a.write:
            p = sd / "index.html"
            html = p.read_text(encoding="utf-8", errors="ignore")
            if re.search(r'<!--\s*BEAT MAP.*?-->', html, re.S):
                html = re.sub(r'<!--\s*BEAT MAP.*?-->', "<!--\n" + block + "\n-->", html, count=1, flags=re.S)
            else:
                html = html.replace("<style>", "<!--\n" + block + "\n-->\n<style>", 1)
            p.write_text(html, encoding="utf-8")
            print(f"{scene}: BEAT MAP comment rewritten ({len(beats)} events)")
        else:
            print(block)

    elif a.mode == "ghosts":
        gs = find_ghosts(sd)
        resolving = [g for g in gs if g["resolves_at"] is not None]
        permanent = [g for g in gs if g["resolves_at"] is None]
        thin = [g for g in resolving if g["below_floor"]]
        print(f"{scene}: {len(gs)} ghosted element(s) — {len(resolving)} resolve, {len(permanent)} permanent")
        for g in sorted(resolving, key=lambda x: x["resolves_at"]):
            flag = "  \033[33mBELOW FLOOR\033[0m" if g["below_floor"] else ""
            print(f"   {g['resolves_at']:7.2f}  {g['selector']:<34} opacity {g['css_opacity']}{flag}")
        for g in permanent:
            print(f"    perm.   {g['selector']:<34} opacity {g['css_opacity']}   (never resolves — deliberate?)")
        if thin:
            print(f"  \033[33m{len(thin)} resolve from below the {GHOST_FLOOR} floor — may read as absent, not ghosted\033[0m")

    elif a.mode == "check":
        old = existing_comment(sd)
        if not old:
            print(f"\033[33m? {scene}: no BEAT MAP comment present\033[0m"); sys.exit(1)
        # ONLY line-leading timestamps count as beat entries. A header line such as
        # "VO ends 48.44, D=48.55" is metadata, not a beat — counting it produced false phantoms.
        old_times = sorted({float(m.group(1))
                            for m in re.finditer(r'^\s*(\d{1,3}\.\d{1,2})\b', old, re.M)
                            if dur is None or float(m.group(1)) <= dur + 1})
        new_times = [b["t"] for b in beats]
        missing = [t for t in new_times if not any(abs(t - o) <= 0.4 for o in old_times)]
        phantom = [o for o in old_times if not any(abs(o - t) <= 0.4 for t in new_times)]
        print(f"{scene}: doc {len(old_times)} timestamps · build {len(new_times)} visual events")
        if phantom:
            print(f"  \033[31mPHANTOM (in the doc, not in the build): {len(phantom)}\033[0m  "
                  + ", ".join(f"{t:.2f}" for t in phantom[:12]))
        if missing:
            print(f"  \033[31mUNDOCUMENTED (in the build, not in the doc): {len(missing)}\033[0m  "
                  + ", ".join(f"{t:.2f}" for t in missing[:12]))
        if not phantom and not missing:
            print("  \033[32mno drift\033[0m")
        sys.exit(1 if (phantom or missing) else 0)


if __name__ == "__main__":
    main()
