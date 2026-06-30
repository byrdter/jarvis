#!/usr/bin/env python3
"""Citation-card-mode master assembly — HARD CUTS via the concat FILTER (not the demuxer).

Why the filter: the concat *demuxer* + `-vsync cfr` duplicates frames at segment timestamp gaps and
BALLOONS the master duration (V2 went 18.9 -> 21.6 min that way). The concat *filter* with per-input
normalization + PTS reset yields the exact summed duration.

Usage:
  assemble-master-concat.py OUT.mp4 scene1.mp4 scene2.mp4 ...
  assemble-master-concat.py OUT.mp4 --list concat.txt      # one "file '<path>'" per line
"""
import subprocess, sys
from pathlib import Path

def parse_list(p):
    out=[]
    for ln in Path(p).read_text().splitlines():
        ln=ln.strip()
        if ln.startswith("file "):
            out.append(ln[5:].strip().strip("'").strip('"'))
        elif ln and not ln.startswith("#"):
            out.append(ln)
    return out

argv=sys.argv[1:]
if len(argv)<2: sys.exit(__doc__)
out=argv[0]
files = parse_list(argv[2]) if (len(argv)>=3 and argv[1]=="--list") else argv[1:]
files=[str(Path(f)) for f in files]
for f in files:
    if not Path(f).exists(): sys.exit(f"missing input: {f}")

args=["ffmpeg","-y","-v","error"]
for f in files: args+=["-i",f]
fc=[]
for i in range(len(files)):
    fc.append(f"[{i}:v:0]fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,"
              f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[{i}:a:0]aresample=48000,asetpts=PTS-STARTPTS[a{i}]")
cat="".join(f"[v{i}][a{i}]" for i in range(len(files)))
fc.append(f"{cat}concat=n={len(files)}:v=1:a=1[v][a]")
args+=["-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
       "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
       "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",out]
print(f"assembling {len(files)} scenes (concat filter) -> {out}")
r=subprocess.run(args)
if r.returncode==0:
    d=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]).decode().strip()
    print(f"done. duration={d}s")
    print("NOTE: portrait shorts → change scale/pad targets to 1080:1920.")
sys.exit(r.returncode)
