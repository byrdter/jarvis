# Text Container Palette — what object holds the words

**Companion to `HYPERFRAMES-TECHNIQUE-PALETTE.md`.** That doc answers *what is this beat's JOB?*
(a proportion → dot-grid, a chronology → spatial pan). This one answers the question that comes
immediately after: **what artifact do the words live inside?**

Written 2026-07-31 against the live `hyperframes catalog` (**138 installed items** — older docs say
142; the binary is authoritative). Verified by running the CLI, not by reading a manifest.

> House rule this enforces (`.claude/rules/video-production-standard.md` §9 rule 4):
> **No naked text on screen.** Information lives inside an artifact — a real document, a citation card,
> a webpage, a terminal/IDE, a data-viz graphic, an org chart. Naked centered or lower-third text is a
> LAST resort, permitted only for a true title or a landing line.

---

## 0. The premise — HyperFrames is a headless browser

The registry is a **shortcut list, not a boundary.** Anything that can be rendered in HTML/CSS is an
available container. So the real inventory is not "what blocks exist" — it is *"what object in the
world would plausibly contain this sentence?"* Most of §7 (the gaps) is 30–60 lines of CSS.

## 1. Why the container is the entertainment

A container carries a second meaning the words themselves do not:

| container | the implicit claim |
|---|---|
| terminal | *someone is doing this right now* |
| state filing | *this is on the record and can't be walked back* |
| redaction | *someone tried to hide this* |
| Reddit thread | *ordinary people noticed* |
| court docket | *this got serious* |
| spreadsheet | *someone was tracking it* |
| job posting | *this already changed what gets hired* |
| receipt | *money actually moved* |

Same sentence, eight different emotional arguments. **Choosing the container is a rhetorical act, not
a decorative one.** A beat that could be a text card and is instead a personnel record whose
Fired/Promoted rows read UNCHANGED while the work-performed list keeps growing is the same information
and a completely different video.

**Selection test:** if the container could be swapped for a plain text card without losing an
implication, you picked the wrong container.

---

## 2. Paper / record register — cream, "on the record"

The **evidence** half of the two-register system (`CONDUIT-VISUAL-SYSTEM.md` §2). Bone `#F4F1EA`,
serif display head, letterspaced mono kicker, hairline rules, label/value rows, circular seal.

| container | implies | notes |
|---|---|---|
| **Citation card** | a verified quote, on the record | the channel signature. **Word-sync-highlight it** (`video-production-standard.md` §10.2, times from `tools/cue.py`) |
| **Real source capture** | we did not retype this | number highlighted ON the real page. Playwright `channel="chrome"` clears Cloudflare. **Budget: ≤35% of runtime** |
| **Academic paper page** | peer-reviewed / methodological | arXiv abstract, a figure caption, a footnote pull-out |
| **Court filing / docket** | this escalated | docket entries revealing beside a schematic map |
| **Registration / licence / certificate** | the state agrees this exists | seal + `REGISTERED` stamp landing (the Messi cold open) |
| **Stacked papers, sequential** | a *pattern* of dismissals | each item stamps as it lands |
| **Personnel record / form** | the contradiction inside ONE artifact | see §1 — this is the canonical example |
| **Redacted document** | concealment | bars retracting is inherently a reveal beat |
| **Memo / letterhead / margin note** | internal, not written for you | not pre-built; trivial CSS |

Motion signature: slides/scales in, stamp lands, slow drift, label/value rows fill in sequence.
Dating anything load-bearing? Stamp it `REPORTED · FEB 2026` — the evergreen constraint.

---

## 3. Screen / interface register — text as something happening

The densest pre-built family in the registry.

### Terminal — 12 Apple Terminal profiles
Per-character typing of a shell session, deterministic:
`code-snippet-apple-terminal-{basic, pro, homebrew, grass, novel, man-page, ocean, red-sands,
silver-aerogel, solid-colors, clear-dark, clear-light}`

**Novel** (warm parchment) and **Man Page** (pale yellow/black) are the sleepers — they read as
*documents rendered in a terminal*, which bridges the cream and dark registers without mixing them.

### IDE — 12 VS Code workbench themes
Full chrome: activity bar, sidebar, tabs, integrated terminal, status bar.
`code-snippet-{dark-plus, dark-modern, dark-2026, light-plus, light-modern, light-2026, monokai,
solarized-light, high-contrast, high-contrast-light, visual-studio-dark, visual-studio-light}`

### Code as MOTION — 9 distinct behaviors (badly underused)
- `code-typing` — token-streamed reveal, caret tracks the frontier
- `code-diff` — removals collapse red, additions expand green → **the "what changed" beat**
- `code-highlight` — band sweeps one line, context dims (`line` is 0-based)
- `code-scroll` — camera scrolls a long real file to a target line (`line` is 1-based — they differ)
- `code-morph` — one snippet *becomes* another, tokens gliding (Shiki Magic Move on `tl`)
  → **the strongest before/after device in the whole kit**
- `code-snippet-flight` — discrete snippets fly in and assemble into a stacked program (block FLIP)
- `code-3d-extrude` — lit beveled slab rotating through real WebGL depth
- `code-shader-dissolve` — code resolves out of seeded noise, chromatic front, then holds crisp
- `code-particle-assemble` — GPU points fly to the exact glyph pixels

### Web / social chrome
- **Browser + search chrome** — query types with a caret, page resolves under it. Job: *what the
  public can see.*
- `x-post` — post card with engagement metrics
- `reddit-post` — upvotes + comments → *ordinary people noticed*
- `macos-notification` — banner drop
- `spotify-card` — now-playing with progress
- `news-ticker` — broadcast crawl, LIVE label, headline ribbon

### Device-as-container (3D hero beats, ≤1 per act)
`vfx-iphone-device` (real GLTF iPhone 15 Pro Max + MacBook Pro with **live HTML in the screen**),
`ios26-liquid-glass`, `macos-tahoe-liquid-glass`, `app-showcase`.
A citation card can live *on a phone someone is holding.*

### Interactive surfaces (`PRESENTATION-VARIETY.md` register H)
Build a real mini-app — evidence explorer, decision dashboard, router simulator — screen-record it,
composite in HyperFrames. The implication: **text arrives because a user did something.**

---

## 4. Broadcast / editorial furniture

- **11 lower-third identities:** `lt-{clean-bar, dark-card, soft-pill, bold-block, color-block,
  stack-bars, accent-underline, kicker-name, mask-reveal, side-rule}` + `lower-third-bild`
  (German-tabloid white bar / red drop-shadow — very loud, use once)
- `yt-lower-third`, `instagram-follow`, `tiktok-follow`
- `camcorder-hud` — REC, battery, date, running timecode → *this was recorded, not authored*
- **Annotation / eval HUD** — acquisition boxes, scrolling queue, filling meters → *a machine is
  reading it* (component library, `CONDUIT-VISUAL-SYSTEM.md` §4)
- **Editorial map annotation** — `north-korea-locked-down` is the template: real map zoom,
  hand-drawn scribble circle, pop-up label, editorial colour wash

---

## 5. Data surfaces — where the text IS the number

Full detail in `HYPERFRAMES-TECHNIQUE-PALETTE.md`. Every statistic belongs here, not on a card:

Stat hero count-up with dynamic scale · ring/arc % readout · **dot-grid/waffle** (64% = 100 dots,
64 lit) · growth-bar stagger · trend line drawing itself against a labelled axis · `data-chart`
(NYT-style bar+line with value labels) · **data table with one row lit last** · numbered grid with
ghosted slots · timeline/funding chart with a callout card riding the line · comparison split
(book-open from opposing wings) · constellation hub with labelled nodes · `flowchart` /
`flowchart-vertical` sticky-note decision trees · schematic map + docket.

> ⚠️ **`us-map` and family fetch topology from a CDN at render time → capture dies with
> `sub_timeline_readiness_timeout`.** Bake the geometry to inline static SVG paths first. Verified
> 2026-07-18. Treat `us-map-bubble`, `us-map-flow`, `us-map-hex`, `world-map`, `spain-map` as suspect
> until checked for a fetch.

---

## 6. Kinetic typography — no container at all

Legitimate when the words genuinely ARE the shot. **This is the family that becomes "text + boxes" if
you lean on it** — it is the thing the technique palette was written to stop.

Typewriter/caret · scramble-decode flip · kinetic beat-slam · **ticker takeover** (slot-machine word
roll, then a hero crashes in and *shoves* the text aside — collision, not fade) · overwhelm-surround ·
**ASR keyword glow** (load-bearing words glow+scale exactly as the VO hits them — free once the
transcript exists) · marker patterns (circle/underline a term like a live argument) · `morph-text`
(gooey SVG-threshold morph) · `texture-mask-text` (66 ambientCG texture masks cut through letterforms) ·
`caption-blend-difference` (auto-inverts per-pixel against whatever is behind it) · **16 `caption-*`
identities** including `caption-parallax-layers` (text layered *behind the subject* in 3D),
`caption-kinetic-slam`, `caption-matrix-decode`, `caption-clip-wipe`, `caption-editorial-emphasis`,
`caption-pill-karaoke`.

---

## 7. Physical / composited text

- **Text-behind-subject matte** — `hyperframes remove-background`, so a person occludes the headline
- **Video-text-pivot** — type pivots to reveal footage through itself (`blueprints/video-text-pivot.md`)
- **HTML-in-Canvas VFX** — capture a *finished card* as a GPU texture, then shatter / portal /
  noise-dissolve / CRT-scanline / pixel-sort it. `vfx-shatter`, `vfx-portal`, `vfx-liquid-background`,
  `vfx-text-cursor`. **One hero beat per act** — the contrast with flat beats IS the storytelling.
- **Text living in b-roll** — whiteboard, notebook, signage, a monitor already in frame

---

## 8. The gaps — containers we don't have and should build

None exist as registry blocks. All are ordinary HTML/CSS. Each buys a distinct implication, which is
the whole point of §1 — this list is ranked by how often our lanes need it.

| container | the implication it buys | why it fits this channel |
|---|---|---|
| **Job posting / req** | this already changed what gets hired | the job-dissolving lane's most natural artifact; a req whose requirements list mutates between two postings is a whole scene |
| **Spreadsheet / cell grid** | someone was *tracking* this | a formula bar showing the arithmetic makes a derived number honest instead of asserted |
| **Email client / inbox** | sent, timestamped, forwardable | the "internal, then leaked" beat; a thread with a growing reply count is chronology for free |
| **SMS / iMessage thread** | private, unguarded | the register where people say the quiet part; pairs with a redaction beat |
| **Slide deck** | this was *pitched* to someone | investor-deck framing turns a claim into a promise made to a specific audience |
| **Wiki with edit history** | contested — the record itself is fought over | a diff view of a page being edited is an argument with no narration needed |
| **Receipt / invoice / transaction** | money actually moved | converts an abstract sum into an event |
| **Subtitle over foreign-language footage** | translated testimony | strongest human-presence text container we don't use; pairs with §10.1 diversity requirement |
| **Book page / e-reader** | settled knowledge, not news | the evergreen register — the opposite of a ticker |
| **Dictionary / glossary entry** | definitional authority | good for the "what does this word actually mean" reversal at ~40–55% |
| **Boarding pass / badge / ID** | a person was *somewhere* | place + identity in one artifact |
| **Handwriting / annotated printout** | a human read this and reacted | the most human container available without a face |

**Build order suggestion:** job posting → spreadsheet → email thread → wiki diff. Those four cover the
majority of beats currently defaulting to a cream card in the AI-and-work lane.

Each should ship as a reusable component under `components/` with a job, a motion signature, and a
`data-*` timing contract — same shape as the §4 component library — so it's instantiated, not
re-derived per scene.

---

## 9. Constraints that bound every container above

1. **All motion on the registered `tl`** (`window.__timelines["root"]`). A bare `gsap.to()`, a CSS
   `animation`, or a free `requestAnimationFrame` renders **FROZEN**.
2. **No render-time network fetch** — renders are offline and deterministic (the `us-map` failure).
3. **No `Date.now()` / `performance.now()` / `Math.random()`** — use `tl.time()` and a seeded PRNG.
4. **Source captures ≤35% of runtime** — past that we are a weaker AI Explained (§1 of the visual system).
5. **Ghosted placeholders resolve within ~1.2s**, ghost opacity ≥ `.40`, or it reads as a dead frame.
6. **Naked full-frame text = titles and landings only.**
7. **≥6 registers per 8-min episode**, no 3 consecutive scenes sharing a dominant register
   (`references/PRESENTATION-VARIETY.md` variety gate).
8. **Every scene passes `tools/scene-validator.py`** before Terry sees it. A written "verified" line is
   a claim, not a check — read the rendered PNG.

---

## 10. How to use this in the beat map

At `PIPELINE.md` Step 3 (treatment) every beat gets **two** tags, not one:

```
JOB:       proportion | place | chronology | relationship | comparison | quote | verdict | breather
CONTAINER: §2 paper | §3 screen | §4 broadcast | §5 data | §6 kinetic | §7 composited
```

Plus the existing `[LIBRARY]` / `[GENERATE]` / `[SOURCE-REAL]` / `[CARD]` asset tag and the
`DEN`/`ATM` VO-binding classification. A beat that cannot name its container is not planned — and if
the answer is §6 (no container) more than a handful of times in a video, the treatment pass isn't done.
