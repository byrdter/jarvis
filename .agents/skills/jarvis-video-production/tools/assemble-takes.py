#!/usr/bin/env python3
"""
assemble-takes.py — keep the LAST take of every paragraph, cut the rest.

The recording pattern this assumes (Terry's, 2026-09-06):
  read a numbered paragraph from VO-RECORD.md → fluff it → pause ~1s →
  read the WHOLE paragraph again from its first word → repeat as needed →
  move to the next paragraph.

Because takes of one paragraph are always CONSECUTIVE, alignment is monotonic:
we never need global search, so repeated wording elsewhere in the script cannot
confuse it. We walk the transcript forward, and for each paragraph we consume
every consecutive match, keeping only the last.

    # 1. plan only — writes a review file, changes nothing
    python3 assemble-takes.py --media take.mp4 --script VO-RECORD.md

    # 2. inspect takes-review.md, then cut
    python3 assemble-takes.py --media take.mp4 --script VO-RECORD.md --apply

READ BEFORE TRUSTING THE OUTPUT
  * The review file is the deliverable. Read it. A paragraph reported with
    1 take when you know you did 3 means alignment slipped — fix before --apply.
  * If you restart MID-paragraph instead of from the first word, the partial is
    not recognized as a take and will survive into the cut. Restart from the top.
  * Cuts snap to detected silence. With no silence between takes the cut lands on
    the word boundary and may clip a breath.
  * On-camera footage: removing a take butts two shots together = a jump cut.
    Expected for this format, but plan b-roll for anywhere it should be hidden.
"""
import argparse, json, os, re, subprocess, sys, difflib
from pathlib import Path

WORD = re.compile(r"[a-z0-9']+")
def norm(t): return WORD.findall(t.lower())

def load_paragraphs(p):
    out = []
    for m in re.finditer(r'\*\*\[(\d{3})\]\*\*  (.+)', Path(p).read_text(encoding="utf8")):
        out.append({"id": m.group(1), "text": m.group(2).strip(), "words": norm(m.group(2))})
    return [x for x in out if x["words"]]

def transcribe_local(media, workdir):
    """Free, offline fallback: whisper.cpp's whisper-cli with word-level output (-ml 1).
    Model: $WHISPER_MODEL, else the best ggml model found in ~/.whisper-models."""
    import shutil, tempfile
    if not shutil.which("whisper-cli"):
        sys.exit("No transcriber: neither the watch skill nor whisper-cli is installed.")
    model = os.environ.get("WHISPER_MODEL")
    if not model:
        for name in ("ggml-large-v3-turbo.bin", "ggml-small.en.bin", "ggml-base.en.bin"):
            p = os.path.expanduser(f"~/.whisper-models/{name}")
            if os.path.exists(p): model = p; break
    if not model: sys.exit("whisper-cli found but no model in ~/.whisper-models")
    print(f"[takes] local whisper.cpp · {Path(model).name}")
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "audio.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(media), "-ac", "1", "-ar", "16000", "-vn", wav], check=True)
        oj = os.path.join(td, "w")
        # -ng = CPU only. On the Intel MacBook (i9-9880H) the default Metal/GPU path decodes to
        # garbage ("the the the", "0 0 0") on real speech; CPU is correct. Verified 2026-10-23.
        subprocess.run(["whisper-cli", "-m", model, "-f", wav, "-ml", "1", "-sow", "-oj", "-of", oj, "-ng",
                        "-t", str(os.cpu_count() or 4)], check=True, capture_output=True)
        data = json.load(open(oj + ".json"))
    flat = []
    for seg in data["transcription"]:
        ws = norm(seg["text"])
        if not ws: continue
        t0, t1 = seg["offsets"]["from"] / 1000.0, seg["offsets"]["to"] / 1000.0
        step = (t1 - t0) / len(ws)
        for i, w in enumerate(ws):
            flat.append({"w": w, "t0": t0 + i * step, "t1": t0 + (i + 1) * step})
    return flat

def transcribe(media, workdir):
    """Whisper with word timestamps via the watch skill's client; falls back to local whisper.cpp
    (the watch skill isn't installed on every machine — added 2026-10-23 on the travel Mac)."""
    if not os.path.isdir(os.path.expanduser("~/.claude/skills/watch/scripts")):
        return transcribe_local(media, workdir)
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/watch/scripts"))
    cfg = os.path.expanduser("~/.config/watch/.env")
    if os.path.exists(cfg):
        for line in open(cfg):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    import whisper as W
    res = W.transcribe_video(Path(media), Path(workdir) / "_audio.mp3")
    segs = res[0] if isinstance(res, tuple) else res
    words = []
    for s in segs:
        sw = s.get("words")
        if sw:
            for w in sw:
                words.append({"w": norm(w.get("word", ""))[:1], "t0": w.get("start"), "t1": w.get("end")})
        else:  # segment-level fallback: distribute evenly
            ws = norm(s.get("text", ""))
            if not ws: continue
            t0, t1 = float(s["start"]), float(s["end"])
            step = (t1 - t0) / len(ws)
            for i, w in enumerate(ws):
                words.append({"w": [w], "t0": t0 + i*step, "t1": t0 + (i+1)*step})
    flat = []
    for x in words:
        if x["w"]: flat.append({"w": x["w"][0], "t0": float(x["t0"]), "t1": float(x["t1"])})
    return flat

def match_at(words, i, target, thresh):
    """Similarity of the transcript window starting at i against target words."""
    n = len(target)
    win = [w["w"] for w in words[i:i+int(n*1.35)+3]][:max(n, 3)]
    if not win: return 0.0
    return difflib.SequenceMatcher(None, win, target).ratio()

def best_match(words, lo, hi, tgt, probe, thresh):
    """FIRST position in [lo,hi) whose FULL-paragraph similarity clears thresh.

    Deliberately not 'best probe position' — that was the 2026-09-06 regression:
    transcription noise can make a spurious position win the opening-words probe,
    and the search then bailed at that position while a real take sat further on.
    The probe is only a cheap pre-filter for which positions are worth scoring."""
    for i in range(lo, min(hi, len(words))):
        pr = difflib.SequenceMatcher(None, [w["w"] for w in words[i:i+len(probe)]], probe).ratio()
        if pr < 0.45:
            continue
        full = match_at(words, i, tgt, 0)
        if full >= thresh:
            return i, full
    return None, 0.0

def restart_point(words, i, tgt, k=4):
    """If the speaker started the line, stopped, and restarted it from the top, return the index of
    the restart; otherwise i. Requires the first k words to recur within one line-length, and the
    words before the recurrence to be (mostly) an opening fragment of the line itself."""
    head = tgt[:k]
    if len(head) < 3: return i
    best = i
    for j in range(i + 2, min(i + len(tgt), len(words) - k)):
        if difflib.SequenceMatcher(None, [w["w"] for w in words[j:j+k]], head).ratio() < 0.75:
            continue
        frag = [w["w"] for w in words[i:j]]
        if difflib.SequenceMatcher(None, frag, tgt[:len(frag)]).ratio() >= 0.7:
            best = j
    return best

def find_takes(words, paras, thresh, lookahead):
    """Monotonic walk. Takes of one paragraph are consecutive, so after the first
    match we keep looking in a tight forward window; each accepted take must clear
    the FULL-paragraph threshold, never the opening probe alone."""
    pos, results, unmatched = 0, [], []
    for para in paras:
        tgt, n = para["words"], len(para["words"])
        probe = tgt[:min(8, n)]
        takes, scan, wide = [], pos, lookahead
        while scan < len(words):
            i, full = best_match(words, scan, scan + wide, tgt, probe, thresh)
            if i is None: break
            # A false start ("In September 2026, the unemp— … In September 2026, the unemployment
            # rate…") clears the threshold from its first word, so the take would start on the
            # stumble. If the line's opening words occur AGAIN shortly after i, and everything
            # between is a prefix of the line, the real take starts at the restart. (2026-10-23)
            i = restart_point(words, i, tgt)
            end = min(len(words) - 1, i + n - 1)
            takes.append((i, end, round(full, 3)))
            scan = end + 1
            wide = n + 30                      # a retake begins soon after the flub
        if takes:
            results.append({"para": para, "takes": takes}); pos = takes[-1][1] + 1
        else:
            unmatched.append(para["id"]); results.append({"para": para, "takes": []})
    return results, unmatched

def silences(media, workdir, noise="-32dB", dur=0.28):
    out = subprocess.run(["ffmpeg","-i",str(media),"-af",f"silencedetect=noise={noise}:d={dur}",
                          "-f","null","-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return sorted(zip(st, en + [None]*(len(st)-len(en))), key=lambda x: x[0])

def snap(t, sils, before=True, pad=0.12, media_end=None):
    """Move a cut into the nearest pause. Word timestamps from whisper.cpp can be ~1s off, so a cut
    placed on a word edge clips words; a cut placed in a pause never does.
    keep-in  → just before speech resumes at the END of the nearest preceding pause;
    keep-out → just after speech stops at the START of the nearest following pause.
    Pauses of ≥0.5s are preferred over the short ones between sentences inside a line.
    (Rewritten 2026-10-23: the old version only snapped when the estimate already sat inside a pause.)"""
    # whisper.cpp word times run LATE on CPU (measured 0.5–2s on 2026-10-23, both on first and last
    # words), so search a window centred ~0.8s EARLIER than the estimate.
    centre, half = t - 0.8, 1.8
    cands = []
    for s0, s1 in sils:
        if s1 is None: s1 = s0 + 0.3
        edge = s1 if before else s0
        if abs(edge - centre) <= half:
            cands.append((s1 - s0 < 0.5, abs(edge - centre), s0, s1))
    if not cands:
        if before and t <= 2.5: return 0.0                       # speech starts at the top of the file
        if not before and media_end and media_end - t <= 2.5: return media_end   # last line of the file
        return t - pad if before else t + pad
    short_only, _, s0, s1 = min(cands)
    if short_only and not before and media_end and media_end - t <= 2.5:
        return media_end      # only sentence-gaps nearby and the file is ending: keep to the end
    return max(s0, s1 - pad) if before else min(s1, s0 + pad)

def aligned_end(words, s_i, tgt):
    """Index of the transcript word aligned to the line's LAST matched word. Using s_i + n - 1
    drifts whenever whisper splits or merges words ("4.2" → "4","2"), which clipped line endings."""
    win = [w["w"] for w in words[s_i:s_i + int(len(tgt) * 1.5) + 6]]
    blocks = [b for b in difflib.SequenceMatcher(None, win, tgt, autojunk=False).get_matching_blocks() if b.size]
    return s_i + (blocks[-1].a + blocks[-1].size - 1 if blocks else len(tgt) - 1)

def selftest(script):
    """Synthetic retakes + transcription noise. Proves the alignment behavior the
    tool claims, so the claim is checkable rather than asserted."""
    import random
    allp = load_paragraphs(script)
    if not allp: sys.exit("selftest: no paragraphs found in " + script)
    print(f"[selftest] {len(allp)} paragraphs available; using first 40\n")
    worst_over = 0
    for seed, noise in [(11,0.06),(3,0.10),(7,0.15),(5,0.20)]:
        random.seed(seed); paras = allp[:40]; truth={}; words=[]; t=0.0
        for p in paras:
            k = random.choice([1,1,1,2,2,3,4]); truth[p["id"]] = k
            for _ in range(k):
                for w in p["words"]:
                    ww = w
                    if random.random() < noise:
                        ww = random.choice([w[:-1] or w, w+"s", "uh", ""])
                    if ww: words.append({"w": ww, "t0": t, "t1": t+0.35})
                    t += 0.36
                t += 1.0
        res, un = find_takes(words, paras, 0.62, 900)
        exact = sum(1 for r in res if len(r["takes"]) == truth[r["para"]["id"]])
        under = sum(1 for r in res if 0 < len(r["takes"]) < truth[r["para"]["id"]])
        over  = sum(1 for r in res if len(r["takes"]) > truth[r["para"]["id"]])
        worst_over = max(worst_over, over)
        starts = [r["takes"][-1][0] for r in res if r["takes"]]
        mono = all(b > a for a, b in zip(starts, starts[1:]))
        print(f"  {int(noise*100):>3}% word noise: exact {exact}/{len(paras)}  under {under}  "
              f"over {over}  unmatched {len(un)}  monotonic {mono}")
    print("\n[selftest] OVER-COUNT must be 0 at every level — an over-count is the only")
    print("           failure that could cut good audio. Under-counts leave a stray")
    print("           retake in the output, which you hear and fix by hand.")
    print(f"[selftest] worst over-count: {worst_over}")
    sys.exit(0 if worst_over == 0 else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--media"); ap.add_argument("--script", required=True)
    ap.add_argument("--out"); ap.add_argument("--apply", action="store_true")
    ap.add_argument("--thresh", type=float, default=0.62)
    ap.add_argument("--lookahead", type=int, default=900)
    ap.add_argument("--pad", type=float, default=0.12)
    a = ap.parse_args()
    if a.selftest: selftest(a.script)
    if not a.media: sys.exit("--media required (or use --selftest)")
    media = Path(a.media); wd = media.parent
    paras = load_paragraphs(a.script)
    print(f"[takes] {len(paras)} paragraphs in {Path(a.script).name}")
    print(f"[takes] transcribing {media.name} …")
    words = transcribe(media, wd)
    print(f"[takes] {len(words)} words transcribed")
    res, unmatched = find_takes(words, paras, a.thresh, a.lookahead)
    sils = silences(media, wd)
    media_end = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(media)],capture_output=True,text=True).stdout or 0) or None
    print(f"[takes] {len(sils)} silence regions")

    keeps, rows, retakes = [], [], 0
    for r in res:
        p, tk = r["para"], r["takes"]
        if not tk:
            rows.append((p["id"], 0, "—", "—", "⚠️ NOT FOUND", p["text"][:60])); continue
        if len(tk) > 1: retakes += len(tk) - 1
        s_i, e_i, sim = tk[-1]
        e_i = aligned_end(words, s_i, p["words"])
        t0 = max(0.0, snap(words[s_i]["t0"], sils, before=True, pad=a.pad))
        t1 = snap(words[e_i]["t1"], sils, before=False, pad=a.pad, media_end=media_end)
        if keeps and t0 < keeps[-1][1]:          # never overlap the previous kept line
            t0 = keeps[-1][1]
        keeps.append((t0, t1))
        rows.append((p["id"], len(tk), f"{t0:8.2f}", f"{t1:8.2f}", f"sim {sim}", p["text"][:60]))

    rep = Path(a.out or wd / "takes-review.md")
    L = [f"# Take assembly review — {media.name}", "",
         f"- paragraphs: **{len(paras)}**",
         f"- discarded retakes: **{retakes}**",
         f"- not found: **{len(unmatched)}**" + (f" → {', '.join(unmatched)}" if unmatched else ""),
         f"- kept runtime: **{sum(b-a2 for a2,b in keeps)/60:.1f} min** of {words[-1]['t1']/60:.1f} min recorded",
         "", "**Read the `takes` column.** If a paragraph says 1 and you know you did 3, alignment",
         "slipped — do not `--apply` until it reads correctly.", "",
         "| para | takes | keep-in | keep-out | match | first words |","|---|---:|---:|---:|---|---|"]
    for r in rows: L.append("| " + " | ".join(str(x) for x in r) + " |")
    rep.write_text("\n".join(L), encoding="utf8")
    print(f"[takes] review → {rep}")
    print(f"[takes] {retakes} retakes to discard; {len(unmatched)} paragraphs unmatched")

    if not a.apply:
        print("[takes] plan only. Read the review, then re-run with --apply."); return
    if unmatched:
        sys.exit("[takes] REFUSING --apply with unmatched paragraphs. Fix alignment first.")
    sel = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in keeps)
    outp = wd / f"{media.stem}-assembled.mp4"
    cmd = ["ffmpeg","-y","-i",str(media),
           "-vf",f"select='{sel}',setpts=N/FRAME_RATE/TB",
           "-af",f"aselect='{sel}',asetpts=N/SR/TB", str(outp)]
    print("[takes] cutting …"); subprocess.run(cmd, check=True)
    print(f"[takes] → {outp}")

if __name__ == "__main__":
    main()
