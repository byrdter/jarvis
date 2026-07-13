#!/usr/bin/env python3
"""Transcribe a media file to a flat word-level transcript.json ({text,start,end} list).
Usage: python3 transcribe.py input.(mp4|wav|mp3) output.json [start_offset_seconds]
Uses whisper-cli (whisper.cpp) with ggml-base.en, -ml 1 -sow for word-level output.
"""
import json, subprocess, sys, os, tempfile

MODEL = os.path.expanduser("~/.whisper-models/ggml-base.en.bin")

def main():
    src, out = sys.argv[1], sys.argv[2]
    offset = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "audio.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                        "-ac", "1", "-ar", "16000", "-vn", wav], check=True)
        oj = os.path.join(td, "whisper")
        subprocess.run(["whisper-cli", "-m", MODEL, "-f", wav,
                        "-ml", "1", "-sow", "-oj", "-of", oj],
                       check=True, capture_output=True)
        data = json.load(open(oj + ".json"))
    words = []
    for seg in data["transcription"]:
        text = seg["text"].strip()
        if not text:
            continue
        start = seg["offsets"]["from"] / 1000.0 + offset
        end = seg["offsets"]["to"] / 1000.0 + offset
        words.append({"text": text, "start": round(start, 3), "end": round(end, 3)})
    json.dump(words, open(out, "w"), indent=0)
    print(f"{len(words)} words -> {out}  [{words[0]['start']:.2f} .. {words[-1]['end']:.2f}]")

if __name__ == "__main__":
    main()
