#!/usr/bin/env python3
"""Cartesia TTS -> wav, for Byrddynasty shorts VO.

Usage:
  python3 cartesia-tts.py --text "..."            --out out.wav
  python3 cartesia-tts.py --file script.txt       --out out.wav
  python3 cartesia-tts.py --file s.txt --out o.wav --voice VOICE_ID --speed slow

Voice defaults to TerryByrd1-V3. NOTE: the repo .env defines CARTESIA_VOICE_ID four
times (Terry Trial / V2 / V3 / Steve). A normal dotenv loader keeps the LAST one —
which is Steve's voice — so this tool never reads CARTESIA_VOICE_ID. Pin the id here
or pass --voice explicitly.

The API key is read from .env and never printed.
"""
import argparse, json, os, re, sys, urllib.request

ENV = "/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/.env"
VOICES = {  # name -> id, transcribed from the .env comment blocks
    "TerryByrd1-V3": "c14ff1c8-7cc4-40d1-8f79-f848154a0e22",
    "TerryByrd1-V2": "43f3ba74-1155-48f8-943e-c937d392c1aa",
    "TerryTrial":    "c8bea31c-bc6a-4fe3-be95-6f06fe22eb8d",
    "Steve":         "9fb269e7-70fe-4cbe-aa3f-28bdb67e3e84",
}
DEFAULT_VOICE = VOICES["TerryByrd1-V3"]
API = "https://api.cartesia.ai/tts/bytes"


def api_key(path=ENV):
    for line in open(path):
        if line.startswith("CARTESIA_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("CARTESIA_API_KEY not found in .env")


def model_id(path=ENV):
    for line in open(path):
        if line.startswith("CARTESIA_MODEL_ID="):
            return line.split("=", 1)[1].strip()
    return "sonic-3.5"


def synth(text, out, voice, version, speed=None):
    body = {
        "model_id": model_id(),
        "transcript": text,
        "voice": {"mode": "id", "id": voice},
        "language": "en",
        "output_format": {"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
    }
    if speed:
        body["voice"]["__experimental_controls"] = {"speed": speed}
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"X-API-Key": api_key(), "Cartesia-Version": version,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r, open(out, "wb") as f:
        f.write(r.read())
    return os.path.getsize(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text"); p.add_argument("--file"); p.add_argument("--out", required=True)
    p.add_argument("--voice", default=DEFAULT_VOICE)
    p.add_argument("--version", default="2025-04-16")
    p.add_argument("--speed")
    a = p.parse_args()
    text = a.text if a.text else open(a.file).read()
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        sys.exit("empty text")
    v = VOICES.get(a.voice, a.voice)
    try:
        n = synth(text, a.out, v, a.version, a.speed)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:400]}")
    print(f"wrote {a.out} ({n:,} bytes) · {len(text.split())} words · voice {v[:8]}…")


if __name__ == "__main__":
    main()
