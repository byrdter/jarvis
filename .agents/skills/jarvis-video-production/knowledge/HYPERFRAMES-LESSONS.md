# HyperFrames Production Lessons (hard-won)

These are failure-modes and techniques proven on real videos. Read before authoring or
debugging a HyperFrames scene. Each one cost a re-render (or a round of user feedback) to learn.

## Motion / rendering

### L1 — Free `gsap.to()` does NOT render under HyperFrames
HyperFrames renders by **seeking** a single paused timeline to exact frame times. Only tweens
added to the **registered timeline** (`window.__timelines["root"] = tl`) are driven by the seek.
A bare `gsap.to(el, {...})` (not on `tl`) plays on gsap's own ticker, which the headless renderer
does **not** advance — so it produces **zero motion** in the output.
- Symptom: a scene that "has animation" but `freezedetect` reports identical frames; the legacy
  `.drift` dot fields produced no motion for exactly this reason.
- Rule: **every** animation goes on `tl` via `tl.to/from/fromTo/set(...)`. Never free `gsap.to`.

### L2 — No infinite repeats
`repeat: -1` breaks deterministic seek (and the lint warns `gsap_infinite_repeat`).
Use a finite count sized to duration: `repeat: Math.max(1, Math.ceil(DURATION/cycle))`.

### L3 — Always set `transform-origin` on scaled/rotated elements
Without it, scale/rotate pivots from an arbitrary origin and the element drifts. Set
`transformOrigin:'50% 50%'` (or intended) on every scale/rotate tween.

## The 5-second rule (no static holds)

A completed composition must not sit visually static for >5s. The dark editorial background +
held card is the trap: the content finishes revealing, then just sits while the VO keeps talking.

### Fix: ambient motion layer (the reliable defeater)
Add large, soft, slow-drifting brand glows BEHIND all content, animated on `tl`:
```css
.ambient{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.amb{position:absolute;border-radius:50%;filter:blur(90px);will-change:transform}
```
3 glows (blue/gold/green ~.16–.20 alpha), each `tl.to('#ambX',{x,y,duration:22-26,ease:'sine.inOut',yoyo:true,repeat:finite},0)`.
Sits at z-index:1, content at z-index:3, B-roll at z-index:2.
For beats whose content is opaque enough to hide the glows, add a slow per-beat "breath"
(`scale:1.02` yoyo on the main element) spanning the hold.

### Gate it (these exact commands)
```bash
R=$(ls -t renders/*.mp4|head -1)
# static holds >=5s  -> must print nothing
ffmpeg -hide_banner -nostats -i "$R" -vf freezedetect=n=-50dB:d=5 -an -f null - 2>&1 | grep freeze_duration
# white/blank frames -> must print nothing
ffmpeg -hide_banner -nostats -i "$R" -vf "negate,blackdetect=d=0.06:pix_th=0.02" -an -f null - 2>&1 | grep black_duration
```
NOTE on the dark aesthetic: plain `blackdetect` false-positives on the #0A0E14 navy bg — use
`pix_th=0.02` (only near-pure-black counts). `scene-validator.py --frames` runs all three gates.

## VO-anchored timing (the #1 correctness bug)

Beats must be anchored to **actual transcript word timestamps**, not evenly spaced. The original
build spaced beats evenly and drifted up to 20s out of sync. A beat's content must be on screen
ONLY while the VO discusses it, and exit before the next topic's VO starts.

- Get the per-scene sentence map:
  `python3 -c "import json;w=json.load(open('assets/transcript.json'));..."` (prints `[t] sentence`).
- When the VO cites several different numbers in sequence (e.g. 32%→65%→40%→60%), the foreground
  must CHANGE on each — never hold one stat while the VO has moved to the next.
- Anchor build-ups to lead the word by 0.3–1.0s; land punchlines on the word (lead 0).

## Treatment: imagination over text (the registers)

Default is NOT "headline + bullet text." See `references/PRESENTATION-VARIETY.md` — 11 registers,
use ≥6 per episode, ≤3 consecutive scenes sharing one. Proven upgrades on real beats:
- A "99% of CEOs" stat → **100-figure isotype grid** (99 lit, 1 dim) with count-up; figures
  drop away on the "reduction" line.
- A prose "critical insight" → **self-drawing fork diagram** (node → diverging trust/skepticism paths).
- A conceptual "it's about intent not capability" → **maxed bar (dimmed) vs a fork glyph (gold)**.
- Company beats → scrimmed **B-roll backgrounds** behind the card (register E), exec **headshots**.
- Kicker/eyebrow labels must be readable on mobile: ≥26px, weight 700 (not 14–18px fine print).

## Counters / numbers

- Count-ups: keep them short (~0.5–0.6s) so a number doesn't *dwell* at a value that collides
  with another on-screen number (two 32%s for ~1s reads as a bug). Land on the VO word.

## Production / assembly gotchas (V5, this repo)

### L-Dropbox — renders get evicted to online-only placeholders
This project lives in Dropbox CloudStorage, which **dehydrates** finished render mp4s within minutes
(full logical size, 0 disk blocks). Reading one then HANGS on re-download, so assembling 10 scenes
stalls. **Fix:** stage every scene render to a LOCAL dir off Dropbox (scratchpad/`/tmp`), assemble
there, and copy only the final master back. `du -h` shows 0B for an evicted file even though `ls -l`
shows the real size — that's the tell.

### L-frames — a render can silently truncate; check the frame count, not the container duration
A hyperframes render occasionally stamps the full container duration from the audio but encodes fewer
video frames. Always verify `nb_read_frames ≈ duration × fps` before trusting a render:
`ffprobe -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -show_entries format=duration ...`.

### L-concat — assemble the master with the concat FILTER via a PYTHON script, not a bash-built string
Building the `-filter_complex` string in bash mangles quoting and BALLOONS the master duration
(video time-stretched, audio 6% long). Run the concat-filter from a Python script (per-input
`fps,scale,pad,setsar,format,settb=AVTB,setpts=PTS-STARTPTS` + `-video_track_timescale 30000`).
Inputs summing to 18:35 must produce an 18:35 master — if it's longer, the filter string got mangled.

### L-split — split-heygen per-file: clear the cache, and expect real-take drift
- Running `split-heygen.py` on several single-scene files to the same `--out` **reuses the cached
  `full-transcript.json`** from the first file → wrong anchors. `rm -f <out>/full-transcript.json`
  between files, or slice with explicit `"start":0` (whole file = one scene, no anchor needed).
- Recorded HeyGen takes may **omit the 1.5s scene gaps, compress, or reword** the script (V5 dropped a
  scene's intro line). Split by the largest silence gap or a fuzzy anchor, then **re-derive every cue
  from the actual transcript** — Whisper writes numbers as digits, so look up "42%" as `42`.
- `zsh` arrays are **1-indexed** (`${a[1]}` is the first element) — a loop that worked in bash will
  shift by one in the snapshot shell.

See also: `references/ANTI-PATTERNS.md` (text-on-text, boxes-on-boxes, shape reuse) and
`references/QC-PASS.md`.
