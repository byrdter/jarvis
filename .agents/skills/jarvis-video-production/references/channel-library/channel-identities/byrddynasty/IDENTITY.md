# Byrddynasty — Channel Identity

The locked design system for the Byrddynasty YouTube channel. Other channels (faceless or future) get their own identity folder with their own overrides; this one is the reference implementation.

---

## Stage

**Background:** Warm cream paper.
```css
background: radial-gradient(circle at 12% 18%, rgba(20, 209, 189, 0.24), transparent 30%),
            radial-gradient(circle at 90% 28%, rgba(138, 43, 186, 0.22), transparent 32%),
            radial-gradient(circle at 50% 92%, rgba(91, 185, 251, 0.18), transparent 34%),
            radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.7), transparent 50%),
            #F4EFE6;
```

**Gradient orbs** (low-opacity, large blur, never sharp):
```css
.orb-1 { width: 580px; height: 580px; left: -180px; top: 540px; background: #5BB9FB; opacity: 0.35; }
.orb-2 { width: 660px; height: 660px; right: -200px; top: 90px; background: #8A2BBE; opacity: 0.30; }
.orb-3 { width: 380px; height: 380px; left: 1320px; top: 720px; background: #14D1BD; opacity: 0.22; }
/* all orbs: position: absolute; border-radius: 999px; filter: blur(140px); */
```

**Film grain** (always-on, low opacity, multiply blend):
```html
<div class="grain"></div>
```
```css
.grain { position: absolute; inset: 0; opacity: 0.10;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.7'/%3E%3C/svg%3E");
  mix-blend-mode: multiply; pointer-events: none; z-index: 2; }
```

---

## Brand mark

Top-left corner of every frame:
```html
<div class="brand"><span class="brand-mark"></span>BYRDDYNASTY</div>
```
```css
.brand { position: absolute; left: 96px; top: 80px; z-index: 25;
  font-family: Inter, sans-serif; font-weight: 900; font-size: 26px;
  letter-spacing: 0.22em; color: #1A2634; opacity: 0.85; }
.brand-mark { display: inline-block; width: 30px; height: 30px;
  background: linear-gradient(135deg, #14D1BD, #8A2BBE); border-radius: 999px;
  margin-right: 14px; vertical-align: middle; margin-bottom: 6px; }
```

The mark is a small gradient orb (teal → purple) followed by the wordmark in Inter 900 with wide letter-spacing.

---

## Typography stack

```css
font-family: Inter, ui-sans-serif, system-ui, sans-serif;   /* body, eyebrow, captions */
font-family: Fraunces, 'Cormorant Garamond', Georgia, serif; /* headlines */
font-family: 'JetBrains Mono', ui-monospace, monospace;     /* code, counters, ticks */
```

### Signature device — headline with italic period
```html
<h1 class="headline"><em>Tools.</em></h1>
```
```css
.headline { font-family: Fraunces, serif; font-weight: 600;
  font-size: 168px; letter-spacing: -0.02em; line-height: 0.96; color: #1A2634; }
.headline em { font-style: italic; color: #5B4738; font-weight: 500; }
```

The italic on the period in a warm brown is a load-bearing channel signature. Don't drop it.

---

## Color tokens

```css
--stage-cream:  #F4EFE6;
--stage-navy:   #1A2634;
--stage-deep:   #0F1420;
--text-warm:    #5B4738;  /* italic brown for headlines */
--accent-cyan:  #34F5FF;  /* primary accent — borders, glows, focus */
--orb-teal:     #14D1BD;
--orb-purple:   #8A2BBE;
--orb-blue:     #5BB9FB;
--warn-amber:   #FFB037;  /* cost indicators, warnings */
```

---

## Card style (dark cards on cream stage)

```css
background: linear-gradient(180deg, #1A2030 0%, #0F1420 100%);
border: 3px solid #34F5FF;
border-radius: 28px;
box-shadow: 0 0 60px rgba(52, 245, 255, 0.5),
            0 24px 80px rgba(0, 0, 0, 0.5),
            inset 0 0 32px rgba(52, 245, 255, 0.08);
```

The cyan border + cyan glow halo + deep navy gradient is the "this is the subject" treatment.

---

## Z-index conventions

| Layer | Z-index | Use |
|---|---|---|
| Background gradient | 1 | `.bg` |
| Film grain | 2 | `.grain` |
| Background SVG (connections) | 27 | Connection lines, particle streams |
| Satellite cards | 28 | Small secondary cards |
| Centerpiece / hero | 30 | The dominant subject |
| Chapter cards | 40 | Highest-priority overlays |
| Brand mark | 25 | Always visible above stage |

---

## Tone

`educational` (primary) with elevated energy at climax moments. See `reference/TONE-MATRIX.md` for how this fits in the multi-channel matrix.

---

## Proven-in modules

This identity has been proven in:
- Module 03 — Five-component model
- Modules 04–07 — Foundation Model, Perception, Memory, Planning
- Module 08 — Tools (climax)
- Module 09 — Context Window (closer)

Reference implementations in `${JARVIS_HOME}/agent-stack-deep-dive/02-modules/`.
