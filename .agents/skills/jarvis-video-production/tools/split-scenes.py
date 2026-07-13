#!/usr/bin/env python3
"""Split a continuous HeyGen take into per-scene assets with boundary refinement.

Usage: python3 split-scenes.py take.mp4 spec.json out_dir
spec.json: {"scenes":[{"name","anchor" (first words of scene) or "start":0,
                       "avatar":true?}, ...], "end": <take VO end or null>}
For each boundary anchor: re-whisper a 20s local window to pin the anchor word start
(long-file whisper drift fix), cut at midpoint of the gap before the anchor word.
Then per scene: extract assets/audio.mp3 (+ avatar.mp4 if avatar), re-transcribe
the slice -> assets/transcript.json (scene-relative).
"""
import json, os, re, subprocess, sys, tempfile

MODEL = os.path.expanduser("~/.whisper-models/ggml-base.en.bin")

def sh(*a, **kw):
    return subprocess.run(a, check=True, capture_output=True, text=True, **kw)

def whisper_words(src, t0=None, dur=None):
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "w.wav")
        cmd = ["ffmpeg", "-y", "-v", "error"]
        if t0 is not None:
            cmd += ["-ss", str(t0)]
        if dur is not None:
            cmd += ["-t", str(dur)]
        cmd += ["-i", src, "-ac", "1", "-ar", "16000", "-vn", wav]
        sh(*cmd)
        oj = os.path.join(td, "out")
        sh("whisper-cli", "-m", MODEL, "-f", wav, "-ml", "1", "-sow", "-oj", "-of", oj)
        data = json.load(open(oj + ".json"))
    words = []
    for seg in data["transcription"]:
        t = seg["text"].strip()
        if t:
            words.append({"text": t,
                          "start": seg["offsets"]["from"] / 1000.0,
                          "end": seg["offsets"]["to"] / 1000.0})
    return words

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def find_phrase(words, phrase):
    pw = [norm(x) for x in phrase.split() if norm(x)]
    J = [norm(w["text"]) for w in words]
    for i in range(len(J) - len(pw) + 1):
        if J[i:i + len(pw)] == pw:
            return i
    n = min(3, len(pw))
    for i in range(len(J) - n + 1):
        if J[i:i + n] == pw[:n]:
            return i
    return None

def main():
    take, specf, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = json.load(open(specf))
    dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                   "-of", "csv=p=0", take).stdout.strip())
    full = json.load(open(spec["full_words"])) if spec.get("full_words") else whisper_words(take)

    scenes = spec["scenes"]
    bounds = []  # start time per scene
    for sc in scenes:
        if "start" in sc:
            bounds.append(float(sc["start"]))
            continue
        i = find_phrase(full, sc["anchor"])
        assert i is not None, f"anchor not found: {sc['anchor']}"
        coarse = full[i]["start"]
        # refine with a local whisper window
        w0 = max(0, coarse - 10)
        loc = whisper_words(take, w0, 20)
        j = find_phrase(loc, sc["anchor"])
        assert j is not None, f"anchor not refound locally: {sc['anchor']}"
        t = w0 + loc[j]["start"]
        gap_before = w0 + (loc[j - 1]["end"] if j > 0 else loc[j]["start"])
        cut = max(gap_before, t - 0.25)  # cut just before the anchor word
        bounds.append(round(cut, 3))
        print(f"  {sc['name']}: coarse {coarse:.2f} -> refined start {t:.2f}, cut {cut:.2f}")
    ends = bounds[1:] + [float(spec.get("end") or dur)]

    for sc, t0, t1 in zip(scenes, bounds, ends):
        d = os.path.join(outdir, sc["name"], "assets")
        os.makedirs(d, exist_ok=True)
        seg = round(t1 - t0, 3)
        sh("ffmpeg", "-y", "-v", "error", "-ss", str(t0), "-t", str(seg), "-i", take,
           "-vn", "-c:a", "libmp3lame", "-q:a", "2", os.path.join(d, "audio.mp3"))
        if sc.get("avatar"):
            sh("ffmpeg", "-y", "-v", "error", "-ss", str(t0), "-t", str(seg), "-i", take,
               "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
               "-pix_fmt", "yuv420p", os.path.join(d, "avatar.mp4"))
        words = whisper_words(os.path.join(d, "audio.mp3"))
        json.dump(words, open(os.path.join(d, "transcript.json"), "w"), indent=0)
        meta = {"name": sc["name"], "take_start": t0, "take_end": t1, "duration": seg}
        json.dump(meta, open(os.path.join(outdir, sc["name"], "slice.json"), "w"), indent=1)
        print(f"  {sc['name']}: [{t0:.2f} .. {t1:.2f}] = {seg:.2f}s, {len(words)} words")

if __name__ == "__main__":
    main()
