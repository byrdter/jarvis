# Tone Matrix — Channels and Visual Registers

This catalog lives in the agent-stack-deep-dive repo but the **shape catalog and motion library are channel-neutral by design.** They serve every channel Terry runs. This doc maps tones to channels so each lesson learned can be tagged, never thrown away.

## How to use the tone tags

Every shape in `SHAPE-CATALOG.md`, every recipe in future `MOTION_RECIPES.md`, every principle borrowed from external references gets a **Tone fit** line listing one or more of the tags below. When a module's `CONCEPT.md` declares its visual shape, the shape's Tone fit must include the target channel's primary tone.

Tags are inclusive, not exclusive. A shape tagged `educational, promo-cinematic` works in both. A shape tagged only `promo-cinematic` would feel off in Byrddynasty without modification.

## Channels

### Byrddynasty (active)

**Primary tone:** `educational`
**Compatible secondary tones:** `premium-product` (sparingly), `universal`
**Avoid as default:** `promo-cinematic` (allowed in cold opens / transitions only)

The educational publication channel — long-form deep-dive teaching, 60-90 minute modules, calm authority, "Numberphile meets Veritasium meets Stripe Press." Audience: serious AI/automation builders. The visual register is editorial first; cinematic moments are reserved for transitions and openings.

### Faceless Channel (paused / to be restarted)

**Primary tone:** `promo-cinematic`
**Compatible secondary tones:** `premium-product`, `universal`, `educational` (when teaching beats appear)
**Tone characteristics:** *TBD — Terry to fill in.* Likely shorter-form, higher kinetic energy, more "hype" appropriate. May lean into the gold-standard 30-second promo aesthetic Nate's MOTION_PHILOSOPHY.md deconstructs.

(Placeholder — replace this section when the channel relaunches and the tone is locked.)

### Future Channels (open slots)

Whatever Terry creates next gets a new entry here. Adding a new channel means: pick a primary tone, list compatible secondary tones, name what to avoid as default. Existing shape/recipe/principle tags don't change.

## Tone Definitions

### `educational`

The publication / documentary register. Patient, deliberate pacing. Headlines do the storytelling, motion does the emphasis. Negative space is the design. Kinetic moments are earned, not constant. Average beat duration 5-15s in a 60-90s module. The Spiritt agentbook reference and our Module 03 v4 are pure examples.

**Signature constraints:**
- One subject per frame.
- Beats long enough for the viewer to read the headline twice.
- No fast cuts inside a teaching beat.
- Color carries meaning, not decoration.

### `promo-cinematic`

The hype / kinetic register. Fast cuts (1-2s scenes typical). Type SCALES and morphs. Light streaks hide every cut. Object metaphors carry the narrative. Holds are reserved for hero reveals. Nate's Infinite Global Payments reference is the gold standard.

**Signature constraints:**
- One IDEA per beat — cuts move on quickly.
- Every transition has a motion trail.
- Reserved palette where each color owns one concept.
- The piece is *lit*, not *colored*.

### `premium-product`

The launch / showcase register. Lives between educational and promo-cinematic. Shows real artifacts — product UIs, dashboards, code panels — with editorial composition. Motion serves the artifact, not the abstract idea. Stripe and Notion promos are the gold standard. Spiritt agentbook also falls here.

**Signature constraints:**
- Real software / artifact is the subject of every frame.
- Headlines support the artifact rather than competing with it.
- Camera holds long enough for the artifact to register.
- Limited but deliberate color accents.

### `universal`

Works in any of the above with minimal modification. Numeric reveals, basic editorial spreads, single-chat-card patterns, polaroid grids — these don't carry a tone the way kinetic cinema or hype-promo do; they adapt to whichever tone the surrounding module wants.

### `vertical-only`

9:16 aspect ratio. Reserved for promotional re-cuts (TikTok / Reels / YouTube Shorts). Never used in primary long-form modules. Doesn't combine with the other tones — it's a delivery-format tag, not a register tag.

## What "borrowing across tones" looks like

A pattern tagged `promo-cinematic` can still inform an `educational` module if it's adapted to slower pacing and less kinetic intensity. Three examples:

- **Light-streak whip** (from Nate's library) — at full promo speed (0.3s), wrong for educational. *Adapted:* slowed to 0.6-0.8s, used only at major section transitions in a Byrddynasty module. The principle survives; the velocity scales down.
- **Color-recolor without cut** — exactly the same in both tones. The discipline of "color carries meaning" is universal.
- **Crystallize-to-wordmark** — the *mechanism* is universal (one object morphs into the brand mark). The *cadence* differs: in promo it lands in 1.5s; in educational it earns 2.5-3s of slower settle.

When porting a `promo-cinematic` move into an `educational` module, document the adaptation in the module's CONCEPT.md so the next module doesn't reinvent the conversion.

## Hard rule

A pattern's tone fit is documented once, here and in the catalog. **No pattern is rejected because of tone** — every pattern lives in the library and gets used somewhere. The rule is *match the tone to the channel*, not *prune the library to the channel*.
