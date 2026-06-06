# V14 Shot Vocabulary

The 11 reusable composition patterns proven across Video 14. Each entry: CSS class name, structure, GSAP animation pattern, and which scenes use it.

Use this as a reference — copy the CSS skeleton and adapt. Don't reinvent.

---

## 1. Title slam — `.shot-1 .title-text` + `.title-line`

**Job:** Open a scene with a hard typographic punch. Used in nearly every scene's opening shot.

**Structure:**
- Full-bleed background (B-roll video or solid color), darkened with `filter: brightness(0.3) blur(2px)`
- Optional `.kicker` (26px, `letter-spacing: 0.4em`, brand-colored, uppercase)
- One or more `.title-line` blocks (160–200px, weight 900, `white-space: nowrap`)
- Last line typically brand-colored for accent

**Animation:**
```js
BT.letterCascade(tl, '#kicker', { at: 0.05, stagger: 0.035, overshoot: 1.04, fromY: 18, fromBlur: 10, duration: 0.45, ease: 'back.out(1.8)' });
BT.letterCascade(tl, '#title', { at: WORD_TIME, stagger: 0.03, overshoot: 1.04, fromY: 30, fromBlur: 14, duration: 0.55, ease: 'back.out(1.8)' });
BT.pulseBloom(tl, '#title', { at: ACCENT_WORD, color: '#d97757', intensity: 22, duration: 0.7 });
```

**Lesson:** Use `display: block; white-space: nowrap;` on each line. Without it, the cascade splits characters that can wrap individually — you'll see "T" on one line and "RADEOFFS" on the next.

**Used in:** Scenes 1, 2, 4, 5, 6, 8, 10.

---

## 2. Hero card — `.hero-card`

**Job:** Introduce a "brain" (Claude, Codex, Gemini) with brand identity. Comes right after the title slam.

**Structure:**
- 1500×700 grid, `grid-template-columns: 540px 1fr`
- Left: `.brain-img` (460px wide, brand-colored `drop-shadow`)
- Right: `.content` stack with `.badge` (brand-colored small tag) + `.title` (76–84px/900) + `.sub` (30–32px/600 at 65% white)

**Animation:**
```js
tl.to('#badge', { opacity: 1, duration: 0.4 }, ANTHROPIC_WORD);
tl.fromTo('#title', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: 'power2.out' }, NAME_WORD);
tl.fromTo('#sub', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' }, DESC_WORD);
```

**Used in:** Scenes 4, 5, 6.

---

## 3. Tradeoff card — `.tradeoff-card` + `.row.strength` / `.row.weakness`

**Job:** Show strength vs. weakness of a model. The Scene 2 vocabulary cornerstone.

**Structure:**
- 1500×600 grid, `grid-template-columns: 460px 1fr`
- Left: `.brain-wrap` (img 320px + `.brain-name` 48px/800)
- Right: `.rows` of `.row` blocks, each with `border-left: 4px solid` colored `#4ADE80` (strength) or `#FF5050` (weakness)
- Each row: `.row-label` (16px 0.25em tracking, color-matched) + `.row-text` (38px/600)

**Animation:**
```js
tl.to('#strengthRow', { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }, STRENGTH_VERB);
tl.to('#weaknessRow', { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }, BUT_WORD);
```

**Optional:** For Codex's "expensive" weakness, add a `.dollar-sweep` overlay (`$` symbols sweeping across the row on the word "expensive").

**Used in:** Scene 2 (3 instances, one per brain).

---

## 4. Real-screenshot overlay — `.cc-shot-wrap`

**Job:** Show a real product UI (Claude Code Desktop, Codex Desktop, Gemini hero) with subtle animation.

**Structure:**
- 1700×1063 wrapper, `border-radius: 14px`, deep shadow `0 40px 100px rgba(0,0,0,0.85)`
- `<img>` filling the wrapper with `object-fit: cover`
- Optional overlay: `.cc-input-glow` (brand-tinted radial gradient over the input field) + `.cc-typing` (typewriter animation overlay positioned via percentage coords)

**Animation:**
```js
// Slow ken-burns
tl.fromTo('#wrap', { scale: 1.0 }, { scale: 1.045, duration: 2.5, ease: 'power1.inOut' }, AT);
// Glow draws eye to input
tl.to('#glow', { opacity: 1, duration: 0.5 }, AT + 0.4);
// Typewriter — steps() ease + width animation
tl.fromTo('#typed', { width: 0 }, { width: '440px', duration: 1.6, ease: 'steps(40)' }, AT + 0.7);
// Blinking caret
tl.to('#caret', { opacity: 0, duration: 0.4, repeat: 3, yoyo: true, ease: 'steps(1)' }, AT + 0.7);
```

**Lesson:** The typing overlay is positioned by percentage (`left: 16.5%, top: 81.5%`) over the image. If the overlay drifts off the actual input field, nudge those percentages. Native screenshot dimensions matter — scale the wrap proportionally.

**Used in:** Scenes 4 (Claude Code Desktop), 5 (Codex Desktop with stat stamps), 6 (Gemini hero).

---

## 5. N-tile spec grid — `.spec-grid` / `.sig-grid`

**Job:** Reveal N specifications or signals one-by-one as the VO names them.

**Structure:**
- `display: grid; grid-template-columns: repeat(N, 290–380px); gap: 20–22px`
- Each `.spec-tile`: 280px tall, gradient `linear-gradient(180deg, #1a1c20 0%, #0e0f12 100%)`, optional brand `border-left: 4px solid`
- Inside: `.num` (18–22px, 0.3em tracking, brand-colored), `.label` (38–42px/900 uppercase), `.desc` or `.key` (16px Menlo)
- Optional `.spec-header` (28–32px 0.3em tracking, 55% white) above the grid

**Animation:**
```js
function revealTile(id, at) {
  tl.to(id, { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.8)' }, at);
}
revealTile('#t1', WORD_1);  // e.g. "surgeon" 7.84
revealTile('#t2', WORD_2);  // e.g. "agentic" 9.08
revealTile('#t3', WORD_3);  // e.g. "careful" 9.51
revealTile('#t4', WORD_4);  // e.g. "MCP-native" 10.35
```

**Used in:** Scene 4 (5-tile Claude specs), Scene 6 (4-tile Gemini stats), Scene 10 (4-tile signal cascade).

---

## 6. Punch-in phrase — `.punch-stage` + `.punch-prefix` / `.punch-slam`

**Job:** Lead with a small setup line, then SLAM a single huge word on the VO beat.

**Structure:**
- Column flex, centered
- `.punch-prefix` (44px/700, 0.18em tracking, 55% white, uppercase)
- `.punch-slam` (200–220px/900, brand-colored, `text-shadow: 0 0 60px rgba(brand, 0.35)`)

**Animation:**
```js
BT.letterCascade(tl, '#prefix', { at: PREFIX_WORD, stagger: 0.04, overshoot: 1.03, fromY: 16, fromBlur: 8, duration: 0.4, ease: 'back.out(1.6)' });
tl.to('#slam', { opacity: 1, scale: 1, duration: 0.35, ease: 'back.out(2.5)' }, SLAM_WORD);
BT.pulseBloom(tl, '#slam', { at: SLAM_WORD + 0.25, color: '#10a37f', intensity: 24, duration: 0.6 });
BT.screenShake(tl, '.punch-stage', { at: SLAM_WORD, duration: 0.4, intensity: 8 });
```

**Lesson:** The slam element starts at `opacity: 0; transform: scale(1.25)`. The back-out ease delivers the punch. Pair with `screenShake` always.

**Used in:** Scene 2 ("EXCEPT WE WEREN'T"), Scene 4 ("BUILDING."), Scene 5 ("THINKING."), Scene 11 ("THE PRICE." with strike-through).

---

## 7. 3-card rotation — `.rot-stage` + `.rot-card`

**Job:** Show three rapid examples in sequence. Each card 1.3–1.7s, no overlap.

**Structure:**
- Three absolute-stacked 1300×600 `.rot-card` elements
- Each card: grid `1fr 600px`
- Left: `.verb` (26px brand-colored, 0.25em tracking, uppercase) + `.what` (76–84px/900)
- Right `.vis`: 480px pane with VSCode-style monospace, classed spans for syntax (`.kw .fn .var .str .com .err .add .rem .file.new .h`)

**Animation:**
```js
// Card A
tl.to('#rotA', { opacity: 1, duration: 0.35, ease: 'power2.out' }, VERB_A);
tl.to('#rotA', { opacity: 0, duration: 0.25, ease: 'power2.in' }, VERB_A + 1.5);
// Card B
tl.to('#rotB', { opacity: 1, duration: 0.35, ease: 'power2.out' }, VERB_B);
tl.to('#rotB', { opacity: 0, duration: 0.25, ease: 'power2.in' }, VERB_B + 1.5);
// Card C
tl.to('#rotC', { opacity: 1, duration: 0.35, ease: 'power2.out' }, VERB_C);
tl.to('#rotC', { opacity: 0, duration: 0.25, ease: 'power2.in' }, VERB_C + 1.5);
```

**Used in:** Scene 4 (Refactor / Implement / Debug), Scene 5 (Planning / Reasoning / Research), Scene 6 (PDF / Video / Codebase).

---

## 8. Orb-and-paths SVG routing — `.route-stage`

**Job:** Visualize the router routing a prompt to one of the three brains. THE signature V14 motion — earns its keep here.

**Structure:**
- Full-frame `.route-stage`
- Absolute SVG layer `<svg class="route-svg" viewBox="0 0 1920 1080">` with one `<path>` per destination, each with `stroke-dasharray="L" stroke-dashoffset="L"` (length = path length so it starts hidden)
- Central `.route-orb` (320px, gold drop-shadow)
- Endpoints `.route-brain.{claude|codex|gemini}` positioned at corners (e.g. `left: 14%; top: 28%` for Claude top-left)
- Brand-color `.route-label` under each brain
- `.route-cond` chips (Menlo font, brand-colored `border-left`) appear on the condition phrase

**Animation:**
```js
// Brain appears
tl.fromTo('#brClaude', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5 }, INTRO_TIME);
// Condition chip appears
tl.fromTo('#condClaude', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.4 }, COND_VERB);
// Path draws
tl.to('#pathClaude', { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' }, SENT_TO_WORD);
// Brain pulses brand color
BT.pulseBloom(tl, '#brClaude', { at: BRAIN_NAME, color: '#d97757', intensity: 24, duration: 0.7 });
```

**Lesson:** Path length must match `stroke-dasharray`. Calculate path length once (the SVG path's actual pixel length) and use it as both dasharray AND initial dashoffset.

**Used in:** Scene 8 (router reveal), Scene 9 (3 live decision examples), Scene 10 (architecture diagram).

---

## 9. Bridge / final hero — `.final-stage` / `.close-stage`

**Job:** Close a scene with brand emphasis. Brain or orb centered, caption below, accent pulse on the punch word.

**Structure:**
- Vertical flex center, gap 36–50px
- `.brain-glow` (240–380px, `drop-shadow(0 0 80px rgba(brand, 0.55))`)
- `.caption` (72–110px/900) with `<span class="accent">` (brand-colored) for the punch word
- Optional `.kicker-line` (32px/800, 0.25em tracking, brand-colored) above the caption

**Animation:**
```js
tl.fromTo('#brain', { scale: 0.85, opacity: 0 }, { scale: 1.0, opacity: 1, duration: 0.6, ease: 'back.out(1.6)' }, BRAIN_WORD);
tl.fromTo('#caption', { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, CAPTION_START);
BT.pulseBloom(tl, '#caption .accent', { at: PUNCH_WORD, color: '#10a37f', intensity: 22, duration: 0.7 });
```

**Used in:** Scene 4, 5, 6, 8, 9, 12 (always as the closer).

---

## 10. Whip-pan exit — universal

**Job:** Cut to the next scene cleanly. Fires at `scene_end - 0.5s` on every non-final scene.

```js
BT.whipPan(tl, {
  at: SCENE_END - 0.5,
  target: '#shotLAST',    // the visible shot at the moment
  direction: 'left',
  duration: 0.45,
  distance: 800,
  blur: 26
});
```

Always `direction: 'left'`. Always `duration: 0.45`. Always `blur: 26`. Continuity.

**Don't use on:** Scene 12 (final outro — gentle held state instead).

---

## 11. Helper usage idioms

The ByrdTransitions library is the workhorse. These are the only four helpers used 90% of the time:

```js
const BT = window.ByrdTransitions;

// Reveal text letter-by-letter
BT.letterCascade(tl, '#sel', {
  at, stagger: 0.025, overshoot: 1.04,
  fromY: 22, fromBlur: 10,
  duration: 0.5, ease: 'back.out(1.8)'
});

// Punctuate a word with a colored glow
BT.pulseBloom(tl, '#sel .accent', {
  at, color: '#FFD700',  // brand-colored
  intensity: 22, duration: 0.7
});

// Pair with slam scale-ins for physical impact
BT.screenShake(tl, '.stage', {
  at, duration: 0.4, intensity: 8
});

// Scene-end transition
BT.whipPan(tl, {
  at: scene_end - 0.5,
  target: '#shotLAST',
  direction: 'left',
  duration: 0.45,
  distance: 800,
  blur: 26
});
```

**Rules:**
- `cascade` opens text reveals (NEVER use plain `fromTo` for headlines)
- `pulseBloom` lands ON the VO word in brand color
- `screenShake` pairs with slam scale-ins
- `whipPan` only at scene end

Other ByrdTransitions helpers exist but are rarely used in V14: `smokeReveal`, `maskWipeCircle`, `zoomPunch`, `glitchSplit`, `rgbSplit`, `lightLeakFlash`, `particleShatter`, `letterBurn`. See the library source for full signatures.

---

## mulberry32 PRNG — paste at the top of every scene

```js
function mulberry32(s) {
  return () => {
    let t = (s += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(NNNNN);  // unique seed per scene (e.g. 202614, 40402)
```

Use `rng()` anywhere you'd use `Math.random()` — dollar rain positions, jitter delays, particle randomness. Deterministic across renders.

## Audio + media data attributes

```html
<audio id="voAudio" src="assets/audio.mp3" data-start="0" data-duration="N.NN"></audio>
<video id="shot1Video" class="bg-video" src="assets/person-typing-focused2.mp4"
       data-start="0" data-duration="N" muted playsinline loop></video>
```

Root carries:
```html
<div id="root"
     data-composition-id="main"
     data-start="0"
     data-duration="N"
     data-width="1920"
     data-height="1080">
```

Every `<video>` and `<audio>` needs `id`, `data-start`, `data-duration`. Lint will catch you if you forget.

## B-roll filename convention

Files ending in `2.mp4`:
- `person-typing-focused2.mp4`
- `person-pointing-at-screen2.mp4`
- `person-frustrated-debugging2.mp4`
- `person-reacting-amazed2.mp4`
- `person-leaning-back-satisfied2.mp4`

…are the audio-stripped variants. Safe to play under VO without doubling speech. Originals (no "2") retain their own audio and are used only when bare.

Located at `video-assets/clip-library/pixelvideos/`.
