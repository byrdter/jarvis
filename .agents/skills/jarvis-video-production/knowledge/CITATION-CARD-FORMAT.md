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

## Evidence-first timing + avatar side-text (V5 review — hard rules)
Every recurring note on V5 reduced to these. Apply by default:
1. **Evidence lands ON the VO stat, THEN elaborate.** When the VO says a number, the highlighted
   article card lands *at that word* (evidence + VO together) and holds until the sentence finishes —
   then cut to a clip/graphic to elaborate. NEVER show a HyperFrames stat first and the same number in
   the article seconds later. If the stat is in the source, **the highlight IS the reveal** — delete
   the redundant HyperFrames stat scene.
2. **One page, moving highlight.** For a passage with several stats (42% → 46% → ⅓ → 73% → 62/63 →
   25%), reuse the SAME source page and **cross-fade between highlight cards** as the VO hits each
   number (one card per stat via `make-citation-card.py`). Reads as "the evidence, line by line."
3. **Label B-roll with a lower-third — don't narrate it in a text box.** A company/example clip gets a
   kicker + one serif line in the corner, not a centred full-screen text card. The lower-third also
   lifts base luminance past the dead-space floor. Reserve full-frame text beats for titles/landings.
4. **Name it, THEN show it.** If a clip is ambiguous (a brain scan, a lab bench), reveal the
   identifying text FIRST ("IBM Watson × MD Anderson · cancer care") and play the clip behind/after it.
5. **Avatar text goes to the SIDE, never over the face.** In avatar scenes (intro/CTA), put brand/
   landing text in a left- (or right-) gradient **side-panel** with the avatar visible and lit — not a
   full-frame scrim + centred text over the face. (See `ASSEMBLY-AND-AVATAR.md`.)
6. **Don't reuse one "hero" clip for two different named examples** (same radiology clip for both the
   IBM cancer beat and the Siemens imaging beat) — the audience notices. Give each a distinct shot; and
   when the VO names a specific example, the visual must be THAT example (not a high-breadth car under a
   "narrow lane" line). See `VISUAL-SOURCING.md`.

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

## Visual density — Terry's standing rule (V-POPE review, 2026-07-07; applies to EVERY video)
- **Clips and images CARRY the presentation; HyperFrames text is an OVERLAY** (lower-thirds + ≤4s
  full-frame landings on a light ~.30 scrim). Text-only beats parked on a dark bg are the #1 rejected
  pattern.
- **HARD CEILING: 5 seconds or less on anything on screen without a perceptible change** — a new
  clip, a new lower-third, a card, a highlight shift, or a re-frame. Slow push-in / ambient drift
  alone does NOT count. A 12s VO stretch = 2–3 visual changes, not one held text card.
- **Citation cards >5s** get a mid-hold change at ~4–5s: second highlight lands, highlight
  cross-fades to the next phrase, or the frame re-crops to the quoted passage.
- **Asset-library FIRST:** before authoring any scene, query `asset-library/assets.db`
  (`symbolizes`/`usable_as`) + the video's custom clip set, and build a beat-by-beat visuals map
  assigning a clip to every concrete noun in the VO. Literal matches beat abstractions ("markets" →
  the trader-at-monitors clip; "ballot" → the ballot-marking clip). Where no adequate clip exists,
  put it on a GAP LIST for Terry to generate — do NOT settle for a text beat.
- **Mine the pixel sets too.** `asset-library/clip-library/pixelvideos/` + `pixelimages/` were
  underused — they carry **transitions** (`trans-glass-shatter`, `trans-light-sweep-cyan`,
  `trans-zoom-through-tunnel`, `bg-particle-field`) that punctuate a beat to satisfy the 5-second rule,
  and **contemplative breathers** (`out-window-city-night-view`, `out-park-walking-thinking`,
  `pov-phone-in-hand-notification`, `tex-paper-stack-raking-light`). Check them before generating new.
- No top-left scene-number/name tag in the chrome.

## Single-use outside visuals + the pre-build variety gate — Terry's standing rule (2026-07-07; EVERY video)
- **An "outside" visual may appear at most ONCE in a video.** Anything **not made specifically for
  this video** — generic `clip-library/videos/` clips, pixel assets, other episodes' `*__br-*` clips,
  product screenshots, stock — gets **exactly one** on-screen appearance. Reusing the same outside
  clip for two beats reads as "they ran out of footage." **Assets MADE for this video** (this episode's
  own `br-*` / `bg-*`) may recur — backgrounds are meant to. When you'd otherwise repeat an outside
  clip, either pick a different one or **make a new episode-specific clip** (addendum, below).
- **Maximize B-roll variety** — no two adjacent beats should share a look; spread clip *kinds*
  (document macro / crowd / civic space / lab / abstract / breather) across the runtime.
- **The 5-second rule is a PRE-BUILD PLANNING GATE, not just a QC check.** *Before* you write the
  visuals map: take the scene's runtime, divide by 5s, and confirm you have that many **distinct**
  visual changes available (clip cut, new lower-third, card, highlight shift, re-frame, transition —
  ambient drift does NOT count). If the count comes up short, you don't have enough visuals yet — put
  the missing ones on the **GAP LIST** and add them to the video's `ASSET-GENERATION.md` in an
  **`## ADDENDUM`** section at the bottom (house-style prompts) for Terry to generate. Never paper over
  a shortfall with a held text card.
- **Rethink the asset plan against these rules every time.** The first-pass asset list (written before
  the VO was final) usually under-supplies variety — re-derive the beat-by-beat map from the *locked*
  VO and reconcile it with single-use + 5s before building any scene HTML.

## Production hardening (learned on the Pope encyclical, V-POPE, 2026-07)
- **Dead-space remedy that reliably works = raise the luminance FLOOR, not just the beat content.**
  The gate flags `stddev<13 AND (mean<22 or mean>234)` for ≥1.2s. Dark scenes trip it wherever only a
  dim bg-still or a small/dimmed label shows. Fix by lightening the bgscrim, lifting bg-still opacity
  from ~.30 to ~.50–.62, and brightening+enlarging the ambient glows (a reusable `brighten.py` patch).
  This clears "black" holes AND makes the moody bg-stills read as intentional atmosphere. Residual
  transition dips still need targeted fixes: overlap adjacent beats (never fade one fully out before
  the next starts), raise/extend the B-roll opacity and lighten the `.broll-scrim`, or land the cream
  card ~1s earlier to cover a title→card gap. A lone eyebrow/kicker on dark bg for >~1s always trips it.
- **Fan-out is great for AUTHORING, unreliable for self-QC.** Parallel subagents build strong scenes
  against a locked reference, but they race their own edit→render→scan loop and will claim "ALL CLEAN"
  on a stale/failed render. The operator MUST re-run `verify-all.py` on every FINAL render and own the
  fixes. Stop stragglers (TaskStop) before assembling so nothing re-renders under you.
- **Dropbox online-only eviction corrupts assets under heavy parallel render load.** A copied card/bg
  can end up the right SIZE but unreadable → `hyperframes render` silently FAILS on the asset and
  leaves the OLD render (so a scene's dead runs "won't change" no matter what you edit). Detect with
  `hyperframes validate` (`net::ERR_CONTENT_LENGTH_MISMATCH`) and a stale render mtime. Fix: re-copy
  from the verified-good source, `sync`, re-render. **Verify card PRESENCE in the render** (sample the
  frame at the card cue; a real cream card reads mean-luma >200) — a missing card still passes the
  dead-space gate, so the gate alone won't catch it.
- **`<video data-start>` is the TIMELINE position, not a media offset** (V-POPE V2 rework: 3 of 6
  scene subagents set `data-start="0"` on clips revealed at t=40–99s → the clip played at t=0,
  froze on its last frame long before its GSAP reveal → dark dead runs + lost motion). Every clip's
  `data-start`/`data-duration` must equal its visible GSAP window (and stay ≤ the source's real
  length — ffprobe it); reusing one source at two moments needs TWO elements on separate tracks.
  Audit fast: list all `data-start` values — clustered near 0 with reveals spread across the scene =
  the bug. Auto-fix: `fix-media-windows.py` (V-POPE `build-scripts/`) aligns windows to `clip()`
  calls and clones reused elements.
- **VO-SYNC verification (do a pass before shipping).** Text that fades in over ~0.5s and is
  triggered AT its cue word only becomes readable ~0.5s AFTER the word — reads as "late." Aim to set
  each text reveal ~0.3–0.4s BEFORE its cue word (Δ = reveal−spoken ≈ −0.35). Verify with a
  sync-report that extracts every `line()`/`lt()` reveal, maps it to the transcript word, and reports
  the delta (see V-POPE `build-scripts/sync-report.py`). **Its distinctive-word match is noisy** on
  multi-word lines and repeated words — confirm any flagged beat with ground-truth `cue.py` on the
  exact phrase before moving it. The reliable signal is LATE beats (positive Δ); most "early" flags
  are the tool matching a later word in the same line. Subagents systematically drift here — one
  V-POPE scene ran its whole middle 5–8s AHEAD of the VO ("pulled forward to fill a gap"), another ran
  2–4s LATE from bad cue estimates. Re-anchor clips AND their text together to the true cue.
- **Run renders SEQUENTIALLY.** 6 concurrent `hyperframes render` processes (load avg 400+)
  corrupted one scene's output mp4 (97% decode-error rate — probes fine by duration, fails on
  decode) and killed other renders mid-mux. Queue renders one at a time; verify outputs with a
  decode pass (`ffmpeg -v error -i out -f null -`), not just ffprobe duration.
- **Splitting a continuous HeyGen take:** local `whisper-cli` (small.en, `-ml 1 -sow`) gives
  word-level timings with no API key. Split by first-line ANCHOR phrases, not silence (a HeyGen take
  is often gap-free). Strip apostrophes when matching (Whisper writes "Alright"→"All right", numbers
  as digits). HeyGen may put a ~1s WHITE frame at a mid-take scene boundary while audio already
  speaks — cover it with an opaque opening graphic (don't trim; that desyncs the VO).

## Elevated-graphics review — Terry's standing rules (V03/V04/V05 flagship review, 2026-07-08)
Locked while reviewing the first "beyond text+boxes" flagships. Apply to EVERY scene:
- **NO four-corner chrome text.** Drop the top-right channel mark and both bottom footer captions/rule —
  Terry cut them ("not needed"). Keep the frame clean; the content carries it.
- **Never text OVER the avatar, never text OVER other text.** In avatar scenes (intro/CTA/close) text
  goes to a side panel, never across the face (see `ASSEMBLY-AND-AVATAR.md`). In graphic scenes,
  stacked labels must **FLOW** (block children with margins), never be absolutely positioned at the same
  coordinates — the V04 bug was a big number's multi-line caption colliding with a note pinned beneath it.
- **Faded background as needed.** A bare gradient reads as "no background." Put the scene's `bg-*` still
  behind the graphics at ~.30-.34 opacity with a scrim + slow ken-burns (the `.bgstill`+`.bgscrim`
  pattern) — it adds depth and variety and helps the luminance floor. Full-frame-hero scenes are the
  exception (the V05 map needed none).
- **Raise the luminance floor on code/graphic scenes.** Pure-navy scenes trip the dead-space gate at
  the floor (mean ~21). Add a persistent `.stagelight` radial + brighter/enlarged ambient glows +
  lighter base gradient -> mean ~40. Bake this into the scene chrome from the start.
- **Variety is required** — no long stretch in one layout. Rotate devices (grid -> ledger -> comparison
  -> breather -> closer), and cut in real footage or a **still image** for beats, especially **fast
  idea-to-idea transitions** (a still is fine when the beat is short and fast-moving — no clip needed for
  a <~3s hit). Re-confirm the 5-second rule as a pre-build gate.
- **Model the STORYTELLING on V05** — Terry singled out how the datacenter scene *told the story*
  (title -> build the map -> scale it up -> the money -> the human twist). Carry that narrative
  escalation into every scene: each beat advances the argument, not just displays a stat.
- **Lean on the HyperFrames repos/skills for innovation** — `~/.claude/skills/hyperframes*` +
  `~/.claude/plugins/cache/.../hyperframes/*/registry` (maps, `data-chart`, `flowchart`, `constellation`,
  code/terminal, shader transitions, VFX). Reach past text+cards every scene.

## Full-batch fan-out production lessons (V03/V04/V05 build, 2026-07-09)
Building 3 whole videos (32 scenes) via parallel subagents + operator render/QC. Hard-won:
- **Avatar-scene layering:** the avatar `<video>` fills the frame at a positive z-index; a positive
  z-index PAINTS OVER auto/`z:0` children, so side-panel text put at auto z is INVISIBLE in the render
  (validate still "sees" it → looks fine, renders blank). Put the avatar `.av` at z1, the gradient
  side-panel at z3, and ALL text at **z≥6** (matches the working b-roll layering). Verify with a rendered
  frame, not just validate.
- **Renders must run SEQUENTIALLY and ALONE.** Concurrent `hyperframes render`, OR many subagents each
  running `hyperframes validate` (headless Chrome) *during* a render, starve/HANG it (an avatar 117s
  scene hung >30 min under 7 concurrent authoring agents; killed + re-ran solo = ~3 min). Fan out
  AUTHORING with subagents but tell them **"do NOT validate or render"** while an operator render is in
  flight; the operator validates + renders solo afterward. (`load avg` from the user's own Chrome tabs
  is a normal baseline — don't kill their browser; only the render's own headless Chrome is yours.)
- **A render can silently drop the audio track.** Before assembling, `ffprobe -select_streams a` every
  scene render; if missing, mux the scene's t=0-aligned `assets/audio.mp3`
  (`ffmpeg -i v.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest`). The concat FILTER
  errors out ("`:a:0` matches no streams") if any input lacks audio.
- **Dark cinematic beats trip the dead-space gate even with content+motion** (terminal typing, a dim
  b-roll). Lift by brightening the dominant panel (terminal body → `#27394f`), raising bg-still opacity,
  and/or landing a bright headline. Counter-intuitive: a DARK b-roll clip at high opacity LOWERS luma
  (footage is darker than the gradient bg) — keep dark clips ≤~.45 and let the brighter bg/graphics show.
- **Assemble via the concat list-file** (`--list concat.txt` with `file '<abs path>'` per line) — shell
  `$FILES` word-splitting mangles a long inline arg list.
- Whisper mis-hears proper names (Kathryn Anne Edwards → "Catherine Ann"); match the transcript token
  for CUE timing but put the CORRECT spelling on screen.
