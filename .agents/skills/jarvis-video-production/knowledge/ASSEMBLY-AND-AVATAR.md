# Master Assembly + HeyGen Avatar Handling

How to stitch per-scene renders into a master without the artifacts we hit. The proven tool is
`tools/assemble-master.py` (xfade video + matched audio crossfade + white-frame handling). The
legacy `scripts/build-master.sh` does plain concat with hard cuts — **do not use it** for avatar
videos (it reproduces the white flash and offers no transitions).

## HeyGen avatar white frames (the #1 transition artifact)

HeyGen takes often have **blank/white frames** at the head and/or tail of a clip, and the white
head is usually accompanied by a short SILENT lead before the first word.
- Detect: `ffmpeg -ss T -i scene.mp4 -vf signalstats,metadata=print -frames:v 1 -f null -` and
  read `YAVG` (≈235 = white). Find the first/last spoken word with the transcript and
  `silencedetect`.
- Scene 01 (intro) tail: white for ~0.1–0.2s after the last word → **trim the tail** (`-t`).
- Scene 08 (closing) head: white for ~1.5s, silent for the same ~1.5s → **freeze-fill**: replace
  the white video with a clone of the first good frame, KEEP the original (silent) audio:
  ```bash
  ffmpeg -y -i scene8.mp4 -filter_complex \
    "[0:v]trim=start=1.546,setpts=PTS-STARTPTS,tpad=start_duration=1.546:start_mode=clone,fps=30,setsar=1[v]" \
    -map "[v]" -map 0:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy scene8_fixed.mp4
  ```
  (1.546 = where white/silence ends. Result: no white, audio intact, same duration.)
- Trimming alone can clip the first word (white and speech meet at the same instant) — that's why
  freeze-fill, which keeps the silent lead, is preferred for the closing avatar.

## Varied transitions (don't ship the same cut 7 times)

User feedback: a single repeated transition reads as lazy. Rotate tasteful `xfade` types across
boundaries, e.g. `fade, smoothleft, dissolve, smoothright, fade, wipeleft, dissolve`. ~50 are
available. Avatar boundaries (graphics↔avatar) should use gentle `fade`/`dissolve`.

## Audio: crossfade only over silence

`xfade` overlaps video by `D`; audio must overlap by the SAME `D` (use `acrossfade d=D`) or A/V
desyncs — critical for the talking-head avatar (a 0.3s lag is visible on lips).
- The VO is one continuous take split into scenes, so crossfading over SPEECH garbles it.
  Safe only when one side of the boundary is **silent**. Most scene splits land in a sentence gap
  (one side silent) — fine. 
- **Transition-clip fix:** if a scene's VO runs to its very last frame (no trailing room), the
  audio crossfade eats the last word. Fix: PAD that scene's tail with held-frame video + silence
  (`tpad=stop_duration=0.45:stop_mode=clone` on video, `apad=pad_dur=0.45` on audio) so the VO
  finishes BEFORE the crossfade window. (This is what fixed the segment-7→avatar "published" clip.)

## assemble-master.py parameters (tune per video)

The script carries the worked example for video-01. Per new video, set:
- scene list / base dir (auto-discovers `scenes/*/renders/*.mp4`, newest each),
- `T01` (scene-1 tail trim), `PAD7` (which scene needs a trailing pad), `scene8_fixed.mp4`
  (freeze-fill for the closing avatar),
- `trans[]` (transition rotation) and `D[]` (durations; ~0.3–0.4s).
Output is re-encoded (libx264 crf 18) — masters land ~300–365 MB with blur-heavy ambient layers;
offer a CRF-20 delivery copy if size matters.

## Final master gate (before human review)

Run the same two gates on the assembled master (must print nothing):
```bash
ffmpeg -hide_banner -nostats -i master.mp4 -vf freezedetect=n=-50dB:d=5 -an -f null - 2>&1 | grep freeze_duration
ffmpeg -hide_banner -nostats -i master.mp4 -vf "negate,blackdetect=d=0.06:pix_th=0.02" -an -f null - 2>&1 | grep black_duration
```
Plus: confirm `duration` ≈ sum of scenes − transition overlaps, audio stream present, and spot-check
the avatar boundaries + any rebuilt beats by extracting frames.
