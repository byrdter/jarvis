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

See also: `references/ANTI-PATTERNS.md` (text-on-text, boxes-on-boxes, shape reuse) and
`references/QC-PASS.md`.
