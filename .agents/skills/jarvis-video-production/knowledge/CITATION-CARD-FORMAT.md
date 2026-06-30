# Citation-Card Format (the "AI-Explained" evidence format) — the V1/V2 standard

**This is the current standard for evidence/argument-driven explainers** (proven on the
"Strategic Pivot" set: V1 *The Choice* 16 min, V2 *Death of the Junior Engineer* 19 min, June 2026).
It is a distinct PRODUCTION MODE from the avatar/HeyGen-xfade pipeline in `ASSEMBLY-AND-AVATAR.md`.
Pick the mode by the content:

- **Citation-card mode (this doc):** research/argument videos where verified quotes & documents ARE
  the proof. Dark editorial register + **cream paper citation cards** that land full-frame on each
  verified quote. Hard cuts. Avatar only for intro/CTA/closing.
- **Avatar/xfade mode (`ASSEMBLY-AND-AVATAR.md`):** talking-head-led episodes; xfade transitions +
  HeyGen white-frame handling via the xfade `tools/assemble-master.py`.

---

## The look
- **Dark register** (navy `#0A0E14` family) per-scene HyperFrames composition: bg-still with slow
  Ken-Burns, ambient brand glows, big Georgia-serif heads, JetBrains-mono kickers, gold `#E0B84A` /
  green / red / blue accents. Per-video color register is allowed (V2 used slate/crimson/umber/teal).
- **Cream citation cards** (`#F4F1EA` paper): a real source page (HBR, arXiv, Microsoft, Bloomberg,
  a LinkedIn post…) with the quoted passage highlighted, source footer bottom-right. The card LANDS
  full-frame on the cue where the VO reads/【names the quote, holds with a slow push-in, then exits.
  Dark → cream → dark is the signature rhythm ("the evidence lands").
- **Citation cards self-identify** — do NOT put an eyebrow label over the card (it overlaps the doc).

## Scene construction (per content scene)
Each content scene is ONE HyperFrames composition (`hyperframes-v3/scenes/<name>/index.html`):
1. Reuse/author a dark concept composition for the scene's argument (ledger, sandwich diagram, fork,
   timeline, exec lockups, etc.). For V2 we **re-used the existing dark comps and re-timed them** to
   the (longer) locked VO — big reuse win.
2. Insert `.cite` full-frame cream card beats at each verified-quote cue (image = the card PNG, with a
   continuous slow push-in scale 1.0→~1.085 over its full hold so it's never static).
3. Anchor EVERY beat to an exact Whisper word-start (see timing below); add any ending beat the longer
   VO needs.
4. All animation on the registered timeline: `window.__timelines["root"] = tl` (free `gsap.to` does NOT
   render). No static hold >5s. Keep ambient motion + content motion through any gap.

## VO-anchored timing (non-negotiable)
- Per-scene `assets/audio.mp3` + word-level `transcript.json` (flat list of `{text,start,end}`).
- `tools/cue.py <transcript.json> "phrase" …` → exact word-start for each beat trigger; pin the beat
  there with a small ~0.3s lead. Whisper renders numbers as digits ("62%") and mis-hears names
  (Kuyda→"Kaida", Skip→"Skimp") — match the transcribed tokens, not the script spelling.

## Card & overlay toolkit (shared, in `jarvis/cli-tools/`)
- `make-citation-card.py` — PDF page → highlighted document card (the cream evidence card).
- `make-text-card.py` — dark/serif/gold text card (`--bg dark|transparent|cream|image:PATH --dim N`).
- `make-logo-card.py` — company/exec lockup (`--photo` portrait or `--logo` wordmark + path tag).
- `make-phase-rail.py` — persistent N-phase rail overlay.
- `verify-vo-sync.py` — flags a cut that doesn't match the VO (reads a scene `timeline.json`).

## Assembly — use the concat FILTER, NOT the demuxer
Citation-card masters are **hard cuts** (no xfade). Assemble with the concat **filter** + per-input
normalization (`tools/assemble-master-concat.py`). 
**Hard-won bug:** the concat *demuxer* + `-vsync cfr` BALLOONS duration (V2 went 18.9→21.6 min from
duplicated frames at segment timestamp gaps). The concat **filter** with `fps=30,setsar=1,settb=AVTB,
setpts=PTS-STARTPTS` per input gives the exact summed duration. Re-encode the master ONCE per batch.

## QC gate — dead-space scan (must be 0 runs end-to-end)
Sample at fps=2, downscale 160×90, flag any run ≥1.2s where `stddev<13 AND (mean<22 or mean>234)`
(near-black OR near-white/cream holds). Run per-scene AND on the assembled master (the master samples
scenes at a different phase and catches boundary fades the per-scene pass misses).
- The recurring offender is an **eyebrow-label-alone moment** → fill it with the scene's photo accent,
  lift bg-still opacity (~.32 + lightened scrim), or pull the beat's main content in within ~1.2s.
- A near-black SCENE BOUNDARY = two fades meeting → lighten the next scene's opening / overlap, OR
  bring its title in faster.
(`scene-validator.py` is the avatar-mode gate; the dead-space scan is the citation-card-mode gate —
inline Python, kept in each project's `build-scripts/verify-all.py`.)

## Per-video working files (the pattern that worked)
- `RESUME-<vid>.md` — direction + per-scene status + the exact rebuild/assemble/QC commands. Write/keep
  this; it survives context resets and is the fastest re-entry point.
- `VISUALS-MAP-V3.md` — beat-by-beat plan (t · VO snippet · backdrop · concept · evidence card · transition).
- `01-script/VO-LOCKED-*.md` — the locked VO; `cards-v3/` — generated citation cards; `cues-v3/` — cue→card map.
- `build-scripts/` — per-video: `cue.py`, `assemble-master.py` (concat-filter), `verify-all.py`
  (dead-space), `gen-cards.py`, `bake-hfbg.py` (bake an HF concept clip over a faded backdrop).

## SHORTS (9:16 vertical promo) — proven on V1's 4 shorts
- 1080×1920 HyperFrames, same dark register + gold/green/red, big serif heads + mono kickers, **rapid
  kinetic cuts** (a new visual every ~2-4s) pinned to the VO word.
- Record the VO in HeyGen (blank-screen MP4); extract audio, transcribe, anchor cuts with the same
  `cue.py`. `.stage` safe-area = top/bottom 210px clear of platform UI.
- Lock ONE short as the template (V1-S1 "62/34 gap"), then build siblings on it. Dead-space scan with
  a faster cadence (fps=3, gaps ≥1.0s). Stage finished shorts to `shorts/out/`.
- Per-short brief lives in `SHORTS-VO.md` (scripts) + `SHORTS-PRODUCTION.md` (shot-by-shot storyboard).

## Reuse > rebuild
V2's whole win was re-using the existing strong dark scene comps, re-timing them to the locked VO, and
inserting cream citation cards — not rebuilding from scratch. Check for an existing comp/asset first.
