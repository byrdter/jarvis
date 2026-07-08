# HyperFrames Technique Palette — stop settling for text + boxes

**Terry's standing rule (2026-07-08):** our citation-card videos had collapsed to three moves —
full-frame type, a cream number card, and b-roll-behind-a-scrim. HyperFrames can do far more, and a
data-dense argument video should USE it. This is the menu. Before building any scene, pick the
technique that MATCHES the beat's job (show a proportion? plot a place? walk a timeline? weigh A vs B?)
instead of defaulting to a text card.

> Everything here still lives inside the citation-card house rules (`CITATION-CARD-FORMAT.md`):
> dark register, cream cards for verified quotes, hard-cut concat assembly, dead-space QC gate,
> VO-anchored timing, ≤5s on anything without a change. These techniques are how you FILL those
> beats — not a new format.

## The one hard constraint (why "just paste a chart lib" fails)
HyperFrames renders from ONE paused GSAP timeline, seeked frame-by-frame — deterministic, no wall clock.
- **All motion attaches to the registered timeline** (`window.__timelines["root"] = tl`). A bare
  `gsap.to()`, a CSS `animation` on wall-clock, or a free-running `requestAnimationFrame` does **NOT**
  render in capture.
- **No `Date.now()` / `performance.now()` / `Math.random()`** — use `tl.time()`, a GSAP proxy tween,
  and a seeded PRNG (`mulberry32`) as our S02 scene already does.
- **Non-GSAP runtimes** (Three.js, Lottie, Anime, WAAPI, CSS, TypeGPU) are driven by their adapter's
  seek — register on the `window.__hf*` array / listen for the `hf-seek` event; the adapter sets each
  instance's `currentTime`. See `~/.claude/skills/hyperframes-animation/adapters/`.
- **`<video data-start>` is the TIMELINE position, not a media offset** (the V-POPE bug). It must equal
  the clip's visible GSAP window and be ≤ the source's real length.
- **`data-in-motion.md` law:** NO pie charts, NO multi-axis, NO dashboards, NO gridlines/legends, NO
  chart-lib output. Build charts with GSAP + SVG/CSS. Every number gets a paired visual (fill/ring/
  shape/color). Same concept = same visual space, only the value changes.

## The families (reach-for menu)

### Data-viz — for every statistic (our #1 gap)
Our stats are all static number cards. They should be:
- **Count-up with dynamic scale** — number tallies 0→N, font grows with the value (`tabular-nums`).
  Rule: `rules/counting-dynamic-scale.md`. THE default for a hero stat.
- **Ring / arc fill** — circular sweep to a % (tween `strokeDashoffset`). Pair beside the count-up.
  `rules/stat-bars-and-fills.md`.
- **Dot-grid / waffle proportion** — render "64%" as 100 dots, 64 lit + 36 dimmed. Visceral, seek-safe,
  no new capability. Compose `center-outward-expansion` (stagger into baked slots) + `depth-of-field-blur`
  (dim the remainder). Use it for "4% said yes. Four."
- **Growth bars / column stagger** — `scaleY` stagger. Compare magnitudes (blocked vs stalled $).
- **Trend / area line draw-on** — a path traces itself L→R (`stroke-dashoffset`), area fill under.
  `rules/svg-path-draw.md`, registry `data-chart` (NYT-style bar+line). For "worsening / growing."
- **Comparison-split** — two equal-weight cards book-open from opposite wings, mirrored tilts, inner
  badges pop. `blueprints/comparison-split.md`. For A/B, before/after, "60% fear vs a measured trickle."

### Diagrams & networks — for structure/relationships
- **Constellation-hub** — iconned nodes spring into a ring around a center, connectors draw hub→node,
  camera pushes in. `blueprints/constellation-hub.md` + `rules/avatar-cloud-network.md`. For "Amazon =
  investor + distributor + competitor," coalitions, who-funds-whom.
- **Timeline as a spatial pan** — pre-place milestones on one oversized canvas, a virtual camera pans
  stop-to-stop, each callout spring-pops, held on "now." `blueprints/spatial-pan-stations.md`. For any
  chronology (the 19-day Fable saga; the Digital Gateway fight).
- **Power-ladder / hierarchy** — vertical stations or stacked list with `svg-path-draw` rungs drawing
  on tier-by-tier, panned upward. For "power moves up: county → state → federal."
- **Flowchart / decision tree** — SVG connectors draw on, sticky-note nodes. Registry `flowchart` /
  `flowchart-vertical` (9:16). For a logic cascade ("no foreign nationals → can't verify → shut ALL down").
- **Maps** — registry `us-map` (choropleth, staggered state reveals), `us-map-bubble` (proportional
  city markers + connection lines), `us-map-flow` (O-D arcs), `us-map-hex`, `world-map`. Pure inline
  SVG+GSAP (us-map) — **no image asset needed**. For "300 towns / 80,000 sq mi." The single biggest
  untapped move for any geographic claim.

### Kinetic typography — when the words ARE the shot
- **Typewriter** — a caret types (and can backspace) a line. `blueprints/typewriter-reveal.md`, registry
  `code-typing` + the 24 terminal/VS-Code themes. For "fix this code" in a real terminal register.
- **Scramble / decode flip** — per-glyph 3D flip with a decrypt flicker. `rules/hacker-flip-3d.md`.
  For a key term "resolving" into place.
- **Kinetic beat-slam** — short phrases slam in on a shared beat array, distinct entrances each.
  `blueprints/kinetic-type-beats.md`. The workhorse for argument beats and CTAs.
- **Ticker takeover** — a slot-machine word roll, then a hero crashes in and shoves the text aside
  (collision, not fade). `blueprints/ticker-takeover.md`, registry `news-ticker`. For "GOVERNMENT /
  COMPANY / — BOTH" ("who blinked").
- **Overwhelm-surround** — surfaces/headlines assemble and close in from all sides. `blueprints/
  overwhelm-surround.md`. For "fear compounds / you're surrounded" (NOT for a metric).
- **ASR keyword glow** — load-bearing words glow+scale exactly as the VO hits them. `rules/
  asr-keyword-glow.md`. This is our VO-anchored standard applied to on-screen emphasis — free once the
  transcript exists. Pair with **marker patterns** (`rules/css-marker-patterns.md`) to circle/underline
  a term like a live argument.

### Media & compositing
- **Video-text-pivot** (`blueprints/video-text-pivot.md`), **grid-card-assemble** (enumerate breadth —
  the leverage toolbox, the coalition wall), **clip-path reveals / iris**, **ken-burns** (never stack
  two transform tweens on one img — parent = entrance, child = ken-burns), **PiP**, **text-behind-subject
  matte** (`hyperframes remove-background` → the avatar can occlude a headline).
- **Shader scene transitions** (registry, use ≤2/video): `domain-warp-dissolve`, `cinematic-zoom`,
  `glitch`, `sdf-iris`, `whip-pan`, `flash-through-white`… for act-break register shifts.

### Generative / canvas / 3D — 1–3 hero beats per video, for contrast
- **Canvas 2D procedural / WebGL FBM shader background** — atmospheric dark-register backdrops that beat
  a flat `#000`. `techniques.md` #2/#13; components `grain-overlay` + `vignette` for cinematic base.
- **Canvas pixel-art** — draw retro pixel graphics per-frame with a seeded palette (Terry's "pixel-like
  images" ask). Good for a pixel server-farm / grid motif. Seek-safe via a GSAP proxy `onUpdate`.
- **HTML-in-Canvas VFX** (the most powerful capability) — capture a finished card as a GPU texture, then
  3D-rotate-with-bloom / shatter / noise-dissolve / CRT-scanline / pixel-sort it. `adapters/
  html-in-canvas-patterns.md`, registry `vfx-shatter` / `vfx-portal` / `vfx-liquid-background`. ONE hero
  beat per act — the contrast with flat beats IS the storytelling.
- **Three.js / Lottie / TypeGPU** adapters for a 3D globe, a polished vector logo, or GPU glass.

## `hyperframes add` — installable blocks (142 items; the ones we want)
- **Maps/data:** `us-map`, `us-map-bubble`, `us-map-flow`, `us-map-hex`, `world-map`, `data-chart`,
  `flowchart`, `flowchart-vertical`.
- **Lower-thirds/chyrons:** `lt-*` family (12), `news-ticker`, `yt-lower-third` (subscribe l/3 w/ avatar).
- **Branding:** `logo-outro`. **Code:** `code-typing`, `code-diff`, `code-highlight`, terminal/VS-Code
  themes. **Transitions:** shader set (≤2/video). **VFX:** `vfx-shatter`, `vfx-portal`,
  `vfx-liquid-background`. **Components (stamped in):** `grain-overlay`, `vignette`, `shimmer-sweep`,
  `morph-text`, `caption-*` identities.
- Discover with the registry: `~/.claude/skills/hyperframes-registry/references/discovery.md`; install
  per `hyperframes-registry` SKILL; wire per its `references/wiring-blocks.md`.

## Fonts (break the Inter/Roboto monoculture)
Pair a heavy display face — **Oswald / League Gothic / Archivo Black** — with **JetBrains Mono** for
data/attribution (keep `tabular-nums` on stacked numbers). Serve via local `@font-face` for determinism.

## The rule of thumb
Every scene should answer: *what is this beat's JOB?* — a proportion (dot-grid/ring), a place (map), a
chronology (spatial-pan timeline), a relationship (constellation/network), a comparison (split), a quote
(cream card + typewriter), a verdict (ticker-takeover), or a breather (one calm library clip). Only reach
for a plain full-frame text card when the job is genuinely a title or a landing line — never as the
default because it was quick.

**Source of truth (re-read for implementation):** `~/.claude/skills/hyperframes-animation/{techniques.md,
rules/*, blueprints/*, adapters/*}` · `~/.claude/skills/hyperframes-creative/references/{data-in-motion,
video-composition, motion-principles, visual-styles, typography, composition-patterns}.md` ·
`~/.claude/skills/hyperframes-registry/references/discovery.md`.

## Reference library — real production compositions (what "possible" looks like)
Cloned 2026-07-08 (public `heygen-com` repos), stored on the **ORICO drive** to avoid Dropbox eviction:
`/Volumes/ORICO/hyperframes-upstream/` (breadcrumb: `${JARVIS_PRIVATE}/references/HYPERFRAMES-UPSTREAM-MOVED-TO-ORICO.txt`).
- **`hyperframes-launches/`** — 15+ finished showcase videos by the HyperFrames makers, each with the
  actual `compositions/*.html`, `renders/`, `fonts/`, `assets/`. When you want a technique done RIGHT,
  open the composition and read how they timed it on `tl`. Effects-heavy ones to study first:
  `vfx-heygen-combined`, `spacex-launch`, `texture-launch-video`, `timeline-launch`, `claude-paper-launch`.
- **`hyperframes/`** — the product monorepo: `registry/` (the SOURCE for all 142 `add` blocks +
  `registry/examples/`), `examples/`, `docs/`, and `skills/` (same skill docs as the plugin, at HEAD).
- **`hyperframes-launch-video/`** — the flagship launch film (heavy: renders + assets).
- **CLI is pinned:** run `hyperframes` (global, 0.7.42) — NEVER bare `npx hyperframes` (version roulette).
- Re-pull with `git -C <repo> pull`. These are read-only reference; do not build inside them.
