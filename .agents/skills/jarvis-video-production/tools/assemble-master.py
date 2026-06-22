#!/usr/bin/env python3
"""Assemble video-01 master from newest per-scene renders with varied crossfade
transitions + matched audio crossfades.

White-frame handling:
- Scene 01: trim white tail (T01).
- Scene 08: use scene8_fixed.mp4 (white head freeze-filled, silent lead kept) — no trim.

Transition-clip handling:
- Scene 07's VO ends exactly at its last frame, so it gets a trailing pad (held last
  frame + silence) so the final word completes BEFORE the 07->08 crossfade, which then
  overlaps silence->silence (scene 8's freeze-filled silent lead). No word clipped.

Run from project root: python3 assemble-master.py [out.mp4]
"""
import subprocess, os, glob, sys
base="hyperframes-v3/scenes"
scenes=["01-introduction","02-strategic-fork","03-research-evidence","04-six-phase",
        "05-companies","06-key-insight","07-cta","08-closing"]
def newest(d): return sorted(glob.glob(f"{base}/{d}/renders/*.mp4"), key=os.path.getmtime)[-1]
files=[newest(d) for d in scenes]
if os.path.exists("scene8_fixed.mp4"): files[7]="scene8_fixed.mp4"   # freeze-filled head
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).strip())
d=[dur(f) for f in files]
T01=68.58            # scene 01 white-tail trim
PAD7=0.45            # scene 07 trailing pad so VO finishes before the crossfade
d[0]=T01
d[6]=d[6]+PAD7
trans=["fade","smoothleft","dissolve","smoothright","fade","wipeleft","dissolve"]
D=[0.30,0.35,0.35,0.35,0.35,0.35,0.40]
out_file=sys.argv[1] if len(sys.argv)>1 else "master.mp4"
args=["ffmpeg","-y"]
for i,f in enumerate(files):
    if i==0: args+=["-t",f"{T01}","-i",f]
    else: args+=["-i",f]
fc=[]
for i in range(8):
    v=f"[{i}:v]fps=30,format=yuv420p,setsar=1,settb=AVTB"
    if i==6: v+=f",tpad=stop_duration={PAD7}:stop_mode=clone"
    fc.append(v+f"[v{i}]")
for i in range(8):
    a=f"[{i}:a]aresample=48000"
    if i==6: a+=f",apad=pad_dur={PAD7}"
    fc.append(a+f"[a{i}]")
prev="v0"; merged=d[0]
for i in range(7):
    fc.append(f"[{prev}][v{i+1}]xfade=transition={trans[i]}:duration={D[i]}:offset={merged-D[i]:.3f}[vx{i}]")
    merged+=d[i+1]-D[i]; prev=f"vx{i}"
aprev="a0"
for i in range(7):
    fc.append(f"[{aprev}][a{i+1}]acrossfade=d={D[i]}:c1=tri:c2=tri[ax{i}]"); aprev=f"ax{i}"
args+=["-filter_complex",";".join(fc),"-map",f"[{prev}]","-map",f"[{aprev}]",
       "-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out_file]
print("target duration:",round(merged,2),"s ->",out_file)
sys.exit(subprocess.run(args).returncode)
