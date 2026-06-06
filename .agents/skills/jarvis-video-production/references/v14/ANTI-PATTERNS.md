# V14 Anti-Patterns

Mistakes we made during V14 production, and the rules that came out of them.

**See also:** [`QC-PASS.md`](QC-PASS.md) for the end-of-scene checklist that catches most of these before render. [`MIN-LENGTH.md`](MIN-LENGTH.md) for length and variety rules.

## A1 — `timeScale` stretching instead of VO anchoring

**Symptom:** The visuals don't quite hit the words. The Claude tradeoff card appears 1.2 seconds AFTER the VO says "Claude." The closer slam lands half a second early.

**Cause:** We authored the timeline against guessed durations, then used `tl.timeScale(authoredDur / actualDur)` to fit the visuals to the VO. Linear stretching can't compensate for the non-uniform pacing of natural speech.

**Rule:** Every animation `at` value MUST come from `transcript.json` word timestamps. After running `npx hyperframes transcribe`, open the JSON, find the anchor word for each beat, paste the timestamp into the animation. NEVER use `tl.timeScale()` to fit visuals to VO.

**If the VO is too short or too long for your authored visual rhythm:** rewrite the VO or the visuals — don't squeeze with `timeScale`.

---

## A2 — `Math.random()` in compositions

**Symptom:** `hyperframes lint` errors with `non_deterministic_code: Script contains 'Math.random()'`. Renders may differ frame-to-frame in subtle ways (particle positions, jitter).

**Cause:** Used `Math.random()` for dollar-rain positions, particle scatter, jitter delays.

**Rule:** Paste the `mulberry32` PRNG at the top of every scene with a unique seed:
```js
function mulberry32(s) { return () => { let t = (s += 0x6D2B79F5); t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const rng = mulberry32(NNNNN);
```
Replace every `Math.random()` with `rng()`. Seeds we've used: 202614, 40402. Pick something memorable per scene.

---

## A3 — Symlinking assets

**Symptom:** `[FileServer] 404 Not Found: /assets/person-typing-focused.mp4` during render. Background videos don't appear in the output MP4.

**Cause:** Linked the asset with `ln -s ../../../../video-assets/clip-library/...` to save disk space. HyperFrames' file server does not follow symlinks.

**Rule:** ALWAYS copy assets with `cp`. Each scene's `assets/` directory must be self-contained.

```bash
cp /path/to/source.png scenes/NN-pilot/assets/source.png
# Never:
# ln -s ../../../../path/to/source.png scenes/NN-pilot/assets/source.png
```

---

## A4 — B-roll with embedded audio

**Symptom:** When the rendered scene plays, you hear the VO PLUS background voice / music from the B-roll. Sounds like two people talking at once.

**Cause:** Used the original `person-typing-focused.mp4` instead of `person-typing-focused2.mp4`. The original retains its source audio; the `2` variants are audio-stripped.

**Rule:** Always use the `*2.mp4` B-roll variants. If you need a clip that doesn't have a `2` variant:
```bash
ffmpeg -i original.mp4 -an -c:v copy original-no-audio.mp4
```

---

## A5 — Text wrapping mid-word inside `letterCascade`

**Symptom:** "TRADEOFFS." renders as "T" on one line and "RADEOFFS." on the next.

**Cause:** `BT.letterCascade` splits the text into individual character spans with `display: inline-block`. Without `white-space: nowrap`, those inline-block chars can wrap individually at any boundary.

**Rule:** Wrap every cascade target line in a block-level element with `white-space: nowrap`:
```html
<div class="title-text">
  <div class="title-line line-1">EVERY AI HAS</div>
  <div class="title-line tradeoffs">TRADEOFFS.</div>
</div>
```
```css
.title-line { display: block; white-space: nowrap; }
```

---

## A6 — Pulse target destroyed by cascade

**Symptom:** Console warning `GSAP target .shot-1 .tradeoffs not found`. Expected red pulse on the word "TRADEOFFS" doesn't appear.

**Cause:** `BT.letterCascade` destroys the inner markup of its target — including any `<span class="accent">` wrappers — and rebuilds as character spans. By the time `pulseBloom` runs, the original `.accent` span is gone.

**Rule:** Apply `pulseBloom` to a parent or sibling element that survives the cascade. If you need to pulse a specific word:
- Split the line into two separate elements (one for "EVERY AI HAS", one for "TRADEOFFS.")
- Cascade each independently
- Pulse the second element by ID/class

---

## A7 — Missing `id` / `data-start` / `data-duration` on media

**Symptom:** `media_missing_data_start` or `media_missing_id` lint error. Background video appears frozen on the first frame.

**Rule:** Every `<video>` and `<audio>` element needs ALL THREE: `id`, `data-start`, `data-duration`. The renderer uses these to manage media playback. Without them, you get a static frame.

```html
<video id="shot1Video" class="bg-video"
       src="assets/person-typing-focused2.mp4"
       data-start="0"
       data-duration="3"
       muted playsinline loop></video>
```

---

## A8 — Per-brain color mixed mid-scene

**Symptom:** Scene reads as "branded confusion" — Codex green pulse appears in a Claude-color hero card, badges and accents don't match.

**Cause:** Copy-pasted CSS from another scene without updating brand colors throughout.

**Rule:** When you create a new scene that introduces or focuses on a single brain, do a global find-replace on the brand color (e.g., replace every `#d97757` with `#10a37f` if you're cloning a Claude scene into a Codex scene). Check:
- `.kicker` color
- `.title-line` color
- `.badge` background + color
- `.brain-img` filter rgba
- `.spec-tile .num` color
- `.spec-tile` border-left
- `.rot-card` border
- `.rot-card .verb` color
- `.final-stage .brain-glow` filter rgba
- `.caption .accent` (and the pulseBloom color value)
- `text-shadow` on slams

---

## A9 — AI-voice generation slop

**Symptom:** Generated VO sounds robotic, monotone, or distinctively "AI." Listener disengages immediately.

**Cause:** Started with the wrong voice. We initially used Cartesia sonic-2 and an older ElevenLabs voice; both produced clearly synthetic-sounding output. Slider tuning didn't fix it.

**Rule:** Voice CHOICE dominates voice settings. If the voice sounds wrong, swap voice IDs first. Only after you've found a voice that reads naturally should you fine-tune stability/style/speed.

Current canonical voice: `gPiEpcKoaZywgOzc0Zn9` (in `.env`).

---

## A10 — Skipping transcription, eyeballing timing

**Symptom:** Cumulative drift across a 12-scene video. By Scene 5 the cuts are 2–3 seconds off the words. Renders feel "off" without an obvious cause.

**Cause:** Estimated VO timing by counting words × 0.4 sec, or by listening to the VO and noting timestamps by ear.

**Rule:** Always transcribe. `npx -y hyperframes transcribe assets/audio.mp3` takes ~30 seconds and gives word-perfect timestamps. There is no scenario in which eyeballing beats this.

---

## A11 — Lint warnings ignored across many scenes

**Symptom:** Final renders have inconsistent typography because fallback fonts loaded for some scenes and not others.

**Cause:** Ignored `font_family_without_font_face` warning across 11 scenes.

**Rule:** It's OK to ignore this warning for individual pilot renders, but before final production, add `@font-face` declarations for any monospace font (Menlo, Consolas) used in code panels. Or switch to a guaranteed-available font like `monospace`.

---

## A12 — Misjudging Runway clip impact timing

**Symptom:** Title slam fires before or after the Runway audio impact. The visual punch doesn't sync with the sound design.

**Cause:** Assumed the impact would land at exactly the timing in our SFX brief (e.g., "impact at 4.0s"). Runway's audio generation drifts ±1 second from prompted timing.

**Rule:** After you receive the Runway clip:
1. Open it in Quicktime
2. Scrub to the impact moment
3. Note the EXACT timestamp
4. Pin the title slam, pulseBloom, and screenShake to that exact timestamp (not the brief's estimate)

If the impact is at 4.7s instead of 4.0s, adjust:
```js
tl.to('#titleB', { opacity: 1, scale: 1.0, duration: 0.35, ease: 'back.out(2.6)' }, 4.7);
BT.pulseBloom(tl, '#titleB', { at: 4.75, color: '#FFD700', intensity: 28, duration: 0.85 });
BT.screenShake(tl, '#root', { at: 4.7, duration: 0.45, intensity: 9 });
```

---

## A13 — Stale brand colors after a brand refresh

**Symptom:** Anthropic / OpenAI / Google updates their brand color and our videos look dated.

**Cause:** Hard-coded hex values throughout all scenes.

**Rule (preventive):** Before a long-form video, define brand colors as JavaScript constants at the top of EACH scene's script block, then reference them. Lets you global-find-replace across scenes if needed.

```js
const CLAUDE = '#d97757';
const CODEX  = '#10a37f';
const GEMINI = '#4285f4';
const JARVIS = '#FFD700';
```

For pilots we used inline hex throughout — fine for the first production, costly if we ever need to change.

---

## A14 — Adjacent words run together without spaces

**Symptom:** Text reads as `Andyoudon't` instead of `And you don't`. Usually only one or two collision points per video but they jump out on watch-through.

**Cause:** Three common origins:
- Copy-pasting HTML that collapsed `&nbsp;` to nothing
- Manually deleting an `<br>` and forgetting to add the surrounding space
- A `<span>` boundary with no whitespace on either side of it (e.g. `<span>And</span><span>you</span>`)

**Rule:** During the QC pass, eyeball every text node in every shot. Specifically the seams between `<span>` boundaries. The fix is always a single space character.

**How to catch in bulk:**
```bash
# Heuristic — find any place where two `>` characters are adjacent in text content
grep -nE ">[A-Za-z]+<" scenes/NN-pilot/index.html | grep -vE ">(/?(div|span|p|h[1-6]|li|td|th|button|a))<"
```
Not foolproof, but flags suspicious adjacencies.

---

## A15 — Body text below the legibility floor

**Symptom:** Kickers ("BRAIN ONE"), badges, sub-headings render too small to read on phone playback. Viewer scans past without absorbing the words.

**Cause:** V14 pilot defaulted to font sizes from print-design intuition (16–32px). 1920×1080 video downscales to 1280×720 / 640×360 on most viewers, so those sizes read as fine print.

**Rule:** Use the [`QC-PASS.md`](QC-PASS.md#sizing-legibility-at-youtube-playback) sizing table as a hard floor. Specifically:
- Kicker (BRAIN ONE) ≥ 40px (we shipped at 26px in V14 pilots — fixed)
- Sub / sub-heading ≥ 36px
- Body / row text ≥ 36px

When in doubt, scale UP. The cost of "slightly too big" is much lower than the cost of "unreadable on phone."

---

## A16 — Brain icons below 360px in hero shots

**Symptom:** The brain icon — the most distinctive visual asset we have — reads as a small decoration instead of the focal point.

**Cause:** Pilot defaults set brain `width: 240–360px` in the three-brains-row shot. On 1920×1080 that's 12–19% of the frame width. For an element that's supposed to BE the shot, that's underweight.

**Rule:**
- Hero card brain (single brain, brand intro): **≥ 460px** (24% frame width)
- Row layout (three brains side by side): **≥ 380px each** (20% frame width)
- Mini brain (orbiting an orb): **≥ 200px**
- Final hero glow brain: **≥ 380px** with `drop-shadow(0 0 80px brand)`

A 240px brain orbits the periphery of the viewer's attention. A 420px brain commands it.

---

## A17 — Declaring "done" before watching the rendered MP4 on a phone

**Symptom:** Issues that are invisible in the desktop preview surface immediately on phone playback — text too small, dim accents, missing audio sync, text wrapping at narrower display widths.

**Cause:** Trusting the Studio preview as the final word. It runs at desktop scale with clean audio routing — neither matches YouTube mobile playback.

**Rule:** Before marking a scene done:
1. Open the rendered MP4 file (not the live preview)
2. Watch it at full screen on a laptop or monitor
3. Watch it on a phone (Airdrop / iCloud / cloud sync)
4. Listen on phone speaker (not headphones)
5. Only after all four checks pass: declare done

If you don't have time for step 3, the scene is not done. Bundle it for later.

---

## A18 — Shipping under 8 minutes

**Symptom:** A V14 video lands at 5–7 minutes. Algorithm under-promotes it. Audience feels short-changed.

**Cause:** Treated each scene independently and built only the scenes the script called for. Didn't audit total length against the 8-minute floor before declaring complete.

**Rule:** See [`MIN-LENGTH.md`](MIN-LENGTH.md) for the full discipline. The short version:
- Every V14 video must be ≥ 8 minutes
- Target 10–15 minutes
- If draft lands under, add interlude segments / expand existing scenes / add deep-dive moments — but NEVER pad with slowed pacing or `timeScale` stretching
- Audit length BEFORE rendering individual scenes — if the script is short, fix it now, not after
