#!/usr/bin/env python3
"""split-heygen.py — PIPELINE Step 1 intake.

Split a raw HeyGen take into per-scene assets/ (audio.mp3 + transcript.json [word-level,
scene-relative] + avatar.mp4 for avatar scenes) + hyperframes.json, ready for authoring.

Transcribes the WHOLE take once (OpenAI whisper-1, word timestamps), then slices by scene
boundaries — given either explicit start/end times OR first-line "anchor" phrases the tool
locates in the transcript (the "hand me the script" path).

Usage:
  python3 split-heygen.py --video heygen.mp4 --spec scenes.json --out <project>/hyperframes-v3/scenes
  [--no-transcribe]  (skip whisper; only slice audio/video — for re-runs)
  [--dry-run]        (transcribe + locate boundaries, print, write nothing)

scenes.json: ordered list, each scene either explicit or anchored:
  [{"name":"01-introduction","avatar":true,"anchor":"CEOs are facing a strategic fork"},
   {"name":"02-strategic-fork","anchor":"Let's look at the data"},
   {"name":"08-closing","avatar":true,"start":784.6,"end":823.4}]
- "anchor": first ~4-8 distinctive words of the scene; start = where they appear, end = next start.
- explicit "start"/"end" (seconds) override anchors. Last scene end defaults to audio end.
- "avatar": true also slices avatar.mp4 for that scene.

Requires OPENAI_API_KEY (env or repo .env) unless --no-transcribe.
"""
import argparse, json, os, re, subprocess, sys, pathlib

def load_key():
    if os.environ.get("OPENAI_API_KEY"): return os.environ["OPENAI_API_KEY"]
    for env in [pathlib.Path.cwd()/".env",
                pathlib.Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/.env")]:
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=",1)[1].strip().strip('"').strip("'")
    return None

def media_dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","csv=p=0",str(p)]).strip())

def norm(s): return re.sub(r"[^a-z0-9 ]","",s.lower()).split()

def transcribe_full(video, out_dir):
    """Whole-take word-level transcript (cached at out_dir/full-transcript.json)."""
    cache = out_dir/"full-transcript.json"
    if cache.exists():
        print(f"  using cached {cache.name}")
        return json.loads(cache.read_text())
    key = load_key()
    if not key: print("❌ OPENAI_API_KEY not found"); sys.exit(1)
    # compact mono 16k mp3 to stay under the 25MB whisper limit
    audio = out_dir/"_full.mp3"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(video),"-ac","1","-ar","16000",
                    "-b:a","64k",str(audio)], check=True)
    from openai import OpenAI
    client = OpenAI(api_key=key)
    print("  transcribing full take (whisper-1, word timestamps)...")
    with open(audio,"rb") as f:
        r = client.audio.transcriptions.create(model="whisper-1", file=f,
            response_format="verbose_json", timestamp_granularities=["word"])
    words = [{"text":w.word,"start":round(w.start,3),"end":round(w.end,3)} for w in r.words]
    cache.write_text(json.dumps(words,indent=0))
    print(f"  {len(words)} words -> {cache.name}")
    return words

def locate(anchor, words, after_idx):
    """Find the word index where `anchor` phrase begins, searching after after_idx."""
    a = norm(anchor)
    wtoks = [norm(w["text"])[0] if norm(w["text"]) else "" for w in words]
    for i in range(after_idx, len(wtoks)-len(a)+1):
        if wtoks[i:i+len(a)] == a:
            return i
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True, help="scenes/ dir to populate")
    ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    video = pathlib.Path(args.video)
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(pathlib.Path(args.spec).read_text())
    total = media_dur(video)

    words = [] if args.no_transcribe else transcribe_full(video, out)

    # resolve start/end for every scene
    idx = 0
    for i,sc in enumerate(spec):
        if "start" in sc:
            sc["_start"] = float(sc["start"])
        elif "anchor" in sc and words:
            j = locate(sc["anchor"], words, idx)
            if j is None:
                print(f"❌ anchor not found for {sc['name']}: {sc['anchor']!r}"); sys.exit(1)
            sc["_start"] = words[j]["start"]; idx = j+1
        else:
            print(f"❌ {sc['name']}: need 'start' or 'anchor' (with transcription)"); sys.exit(1)
    for i,sc in enumerate(spec):
        sc["_end"] = float(sc["end"]) if "end" in sc else (spec[i+1]["_start"] if i+1<len(spec) else total)

    print(f"\n{'SCENE':<26}{'START':>9}{'END':>9}{'DUR':>9}  avatar")
    for sc in spec:
        d = sc["_end"]-sc["_start"]
        print(f"  {sc['name']:<24}{sc['_start']:>9.2f}{sc['_end']:>9.2f}{d:>9.2f}  {bool(sc.get('avatar'))}")
    if args.dry_run:
        print("\n(dry-run: nothing written)"); return

    for sc in spec:
        s,e = sc["_start"], sc["_end"]; d = e-s
        sd = out/sc["name"]; (sd/"assets").mkdir(parents=True, exist_ok=True)
        a = sd/"assets"
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{s}","-to",f"{e}","-i",str(video),
                        "-vn","-b:a","192k",str(a/"audio.mp3")], check=True)
        if sc.get("avatar"):
            subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{s}","-to",f"{e}","-i",str(video),
                            "-an","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",str(a/"avatar.mp4")], check=True)
        if words:
            seg = [{"text":w["text"],"start":round(w["start"]-s,3),"end":round(w["end"]-s,3)}
                   for w in words if w["start"]>=s and w["start"]<e]
            (a/"transcript.json").write_text(json.dumps(seg,indent=0))
        (sd/"hyperframes.json").write_text(json.dumps(
            {"width":1920,"height":1080,"fps":30,"duration":round(d,3)},indent=2))
        print(f"  ✓ {sc['name']}  ({d:.2f}s, {'avatar+' if sc.get('avatar') else ''}audio+transcript)")
    print("\ndone. Next: PIPELINE Step 2 (per-scene VO map) -> author scenes.")

if __name__ == "__main__":
    main()
