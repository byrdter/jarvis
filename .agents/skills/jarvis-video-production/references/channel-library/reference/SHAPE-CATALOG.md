# Shape Catalog — Dissected Reference Library

This is the **multi-channel** working library of visual *shapes* Terry's channels have access to. Each shape is dissected from a real HyperFrames example, tagged for tone fit, and noted for when to reach for it. Lessons are never thrown away — they're tagged for the channel that suits them.

## How to use this catalog

When writing a module's `CONCEPT.md`, every module is required to declare a "Visual shape (and why)" field. The choice should come from this catalog. The justification should answer:

1. **Why does this story call for this shape?**
2. **Does the shape's tone fit match the target channel's primary tone?** (See `TONE-MATRIX.md`.)
3. **If the shape is from a different tone, what's the adaptation plan?** (e.g., slowing a promo-cinematic move to educational pacing.)

The same shape can be reused across many modules. What is forbidden is **defaulting to a shape because it worked before**. Each module forces the choosing question.

## Tone tags used in this catalog

- `educational` — patient, publication-style, calm authority (Byrddynasty's primary tone)
- `promo-cinematic` — kinetic, fast cuts, motion trails, hype energy (Faceless channel's primary tone)
- `premium-product` — product launch / showcase, real artifacts as subject (sits between educational and promo-cinematic)
- `universal` — adapts to any tone with minimal modification
- `vertical-only` — 9:16 aspect, for promotional re-cuts only

See `TONE-MATRIX.md` for full definitions and channel mappings.

## Catalog overview

| # | Shape name | Tone fit | Reference example | Best for |
|---|---|---|---|---|
| 01 | **Editorial Spread** | educational, premium-product | Module 03 v4 (our pilot), Spiritt agentbook | "What is X" definitional teaching |
| 02 | **Evidence Collage** | educational, premium-product | YC "builders into formidable founders" | Real-world proof, real companies/founders cited |
| 03 | **Editorial + Code Panel** | educational, premium-product | Stripe | Product/protocol introduction with a code artifact |
| 04 | **Cosmic Stats Reveal** | premium-product, promo-cinematic | Stripe (mid section) | Big-number payoff against a sparse cosmic field |
| 05 | **Dark Product Showcase** | premium-product, promo-cinematic | Notion AI promo | Product-launch tone with surrounding integration logos |
| 06 | **Floating Polaroid Grid** | universal | Dribble | Multiple visual artifacts as parallel proof |
| 07 | **3D Tilted Card Stack** | premium-product, promo-cinematic | HyperFrames promo ("Hermes"), Jake albums | Templates, registry, catalogue presentations |
| 08 | **Workshop in Perspective** | promo-cinematic, premium-product | 3D (Figma showcase) | "A real workspace exists" cinematic shot |
| 09 | **Command Palette Pop** | universal | Shortcut (Raycast-style) | Single-action demo, "this is what the command does" |
| 10 | **Single Chat Card** | educational, universal | bluesweater (Claude chat) | "Watch one prompt complete end-to-end" |
| 11 | **Fanned Phone Trifold** | premium-product | phones | Mobile UI showcase (when relevant) |
| 12 | **Vertical News Stack** | vertical-only | Stories (9:16) | Vertical-only — Shorts cuts and TikTok |
| 13 | **Animation Paths Reveal** | promo-cinematic | HyperFrames promo (dot constellations) | Abstract concept reveal where motion *is* the meaning |
| 14 | **Numeric Reveal** | universal | Notion ("62% of Fortune 100") | Single number with one supporting line, no chrome |

---

## 01. Editorial Spread

**Tone fit:** `educational`, `premium-product`. Native Byrddynasty look.
**Reference:** `02-modules/003-five-component-model/hyperframes-v4/` (Module 03 v4), `Examples/Spiritt agentbook` (the cream-stage v3 source inspiration).

**Layout:**
- Cream warm-off-white background with soft gradient orbs + film grain.
- Left third: small-caps eyebrow → large Fraunces serif headline (with italic accent on key word) → short body sentence in Inter.
- Right two-thirds: dark IDE-style demo panel showing real-feeling software.
- Brand mark top-left. Indicator strip bottom-of-frame ticking through subject sections.

**Signature moves:**
- Eyebrow / headline / body all swap as a unit when the subject changes.
- Demo panel content is dark, so it reads as "real software dropped into a bright editorial layout."
- Indicator at the bottom lights one component at a time, with all-five-lit for synthesis beats.

**When to reach for it:**
- Definitional teaching beats ("what *is* X").
- Multi-part series where the same frame can hold many subjects sequentially (eyebrow + headline swap).
- When the story requires showing both "the concept" (left) and "the artifact" (right).

**When to skip it:**
- When the story is about *one concrete real-world thing* — use Evidence Collage instead.
- When the payoff is a single dramatic number — use Numeric Reveal instead.
- When you've used it three modules in a row — pick something else, you're defaulting.

---

## 02. Evidence Collage

**Tone fit:** `educational`, `premium-product`. Works in Byrddynasty when there are real artifacts (founder photos, product screenshots) to display.
**Reference:** YC "builders into formidable founders" promo (we received this earlier in the conversation; lives at `/Users/terrybyrd/Downloads/ycombinator (1)/renders/ycombinator_final.mp4`).

**Layout:**
- Same cream warm-off-white palette family (compatible with channel identity).
- Polaroid-style photographs scattered across the frame at slight rotations.
- Real artifacts: founder photos, company logos, real screenshots stamped onto cards.
- Hand-drawn arrows annotating relationships.
- Bold sans-serif headline anchored top-left, supporting text in small caps stamp-style.
- One giant numeric callout (e.g., "$0.9T") on a separate frame.

**Signature moves:**
- Polaroids arrive with slight rotation, mild drop shadow, organic stagger.
- "Stamp" headers ("Y COMBINATOR / 2005-NOW") top-left feel like a publication mark.
- Real photos do the heavy lifting — the layout is just frame and label.
- Concluding beat is often a quiet headline ("Be in the room.") + 2-3 lifestyle photos.

**When to reach for it:**
- Beats that cite real companies, real founders, real screenshots.
- "Proof" modules where artifacts substantiate a claim.
- Memorable opens for sections that hinge on real evidence.

**When to skip it:**
- When you don't have real artifacts to show — collage with stock visuals looks weak.
- When the teaching point is abstract/conceptual — Editorial Spread serves better.

---

## 03. Editorial + Code Panel

**Tone fit:** `educational`, `premium-product`. The cooler whiter palette pulls slightly toward premium-product, but adapts easily to Byrddynasty.
**Reference:** `Examples/Stripe.mp4`, first ~10s.

**Layout:**
- Bright off-white background, fading slightly cooler than channel cream.
- Left half: large sans-serif headline ("Financial infrastructure"), pill-shaped capability chips beneath ("Payments", "Billing", "Subscriptions", "Fraud detection"), one-line subtitle.
- Right half: dark code editor panel (Stripe-API.js) with syntax-highlighted code visible.
- Faint background currency glyphs scattered (visual texture).

**Signature moves:**
- Pills arrive in sequence with mild bounce.
- Code in the right panel appears line-by-line as if being typed.
- Subtle "200 OK" success comment color-pop at the end.

**When to reach for it:**
- "Here is the protocol/SDK/API" introductions.
- Beats where the code is the *artifact* the viewer needs to see.
- Product/protocol introduction tonality.

**Difference from Editorial Spread:**
- Cooler/whiter background vs cream.
- Sans-serif headline (not serif) — feels more like a corporate doc.
- Pills below headline (Editorial Spread uses body sentences).

**When to skip it:**
- When the right-side artifact isn't code (use Editorial Spread with a different panel instead).

---

## 04. Cosmic Stats Reveal

**Tone fit:** `premium-product`, `promo-cinematic`. The cosmic background drift carries promo energy. For Byrddynasty, dial down the parallax and hold longer.
**Reference:** `Examples/Stripe.mp4`, mid-section (~t=10-15s).

**Layout:**
- Deep navy background with a constellation of small white points.
- A subtle world-globe / arc network sits behind, partly visible.
- Three large stat columns across the middle: "135+", "99.999%", "200M+" with smaller two-line labels beneath each.
- Vertical thin separator lines between stats.
- Nothing else on frame. Massive negative space.

**Signature moves:**
- Camera holds for several seconds — the silence is the point.
- Numbers may count up or arrive simultaneously with a soft pulse.
- The cosmic background drifts very slowly (parallax).

**When to reach for it:**
- "Scale of the thing" beats — when the numbers themselves are the message.
- Mid-video punctuation between teaching sections.

**When to skip it:**
- Single-number beats (use Numeric Reveal — bigger, more dramatic, less cluttered).

---

## 05. Dark Product Showcase

**Tone fit:** `premium-product`, `promo-cinematic`. Strong fit for the Faceless channel. Useable in Byrddynasty for JARVIS-introduction moments (Module 43) with the spotlight intensity reduced.
**Reference:** `Examples/Notion.mp4`, opening frame.

**Layout:**
- Deep navy/black background with a soft top-down spotlight.
- Center: a small stat ("100M+"), a large display headline ("Your 24/7 AI team"), italic tagline ("Meet the night shift."), product wordmark below.
- Around the perimeter at four corners: floating circular logo discs of integrations (Gmail, Slack, etc.) in colored backgrounds, half-clipped at the edges.
- "Spotlight" gradient implies a stage.

**Signature moves:**
- Headline lands first; integration logos drift inward from corners with a slight scale-up.
- The wordmark appears at the bottom last, like a signature.

**When to reach for it:**
- "Here is our product / system / agent that touches all these things" reveals.
- Could fit a JARVIS introduction (Module 43) — integrations around the wordmark.

**When to skip it:**
- When the story isn't a product reveal — this shape is *all about* introducing one named thing.

---

## 06. Floating Polaroid Grid

**Tone fit:** `universal`. Works across every channel — the grid is decorative restraint, the cards do the heavy lifting.
**Reference:** `Examples/Dribble.mp4`, ~t=8s.

**Layout:**
- White or very pale background.
- Four (or more) image cards arranged in a horizontal row across the upper third of the frame, each with rounded corners, soft drop shadow, slight perspective tilt.
- The cards show real or stylized design artifacts (illustrations, app UIs, photos).
- Bottom two-thirds: empty whitespace.

**Signature moves:**
- Cards drift in from below with subtle staggered timing.
- Each card holds its position; the *grid itself* is the statement, not individual cards.
- May camera-pan or scroll laterally across many cards.

**When to reach for it:**
- "Look at this *range* of examples" beats.
- When the story is about variety / breadth / a portfolio of things.
- Could fit "agents are everywhere" Part 4 moments.

**When to skip it:**
- When one specific artifact is the focus — use Editorial Spread or Single Chat Card.

---

## 07. 3D Tilted Card Stack

**Tone fit:** `premium-product`, `promo-cinematic`. The perspective tilt and depth shadows carry kinetic energy — natural Faceless channel fit. In Byrddynasty, soften the angle (5-10° instead of 15-20°) and slow the drop.
**Reference:** `Examples/Hermes.mp4` (~t=27s, "Templates and registry"), `Examples/Jake.mp4` (album grid in perspective).

**Layout:**
- Dark or graphite background.
- 3-4 rectangular cards arranged with a perspective transform — tilted ~15-20° as if viewed from above, stacked diagonally with z-depth offset.
- Each card has a small visual block (color, logo, or small icon) on the left and a monospace label on the right.
- Bottom: a single line of text identifying the category.

**Signature moves:**
- Cards drop in one at a time, each landing slightly behind the previous with depth shadow.
- Slight subtle rotation animation; cards "settle" rather than snap.
- Optional ambient camera drift.

**When to reach for it:**
- "Catalogue of N things" beats — templates, options, layer types.
- When the story is about a *set* and the depth implies "more available than shown."

**When to skip it:**
- When each item needs equal weight — flat grid is clearer than perspective stack.

---

## 08. Workshop in Perspective

**Tone fit:** `promo-cinematic`, `premium-product`. The 25° tilt is decisively cinematic. For Byrddynasty, use only at cold opens or major section transitions — labels in the perspective window get hard to read at long holds.
**Reference:** `Examples/3D.mp4`, ~t=4-9s.

**Layout:**
- Pure black background.
- A dark macOS-style app window floats in 3D perspective, tilted ~25° toward camera.
- Inside the window, real-looking UI: sidebar, design canvas, properties pane.
- Subtle ambient glow underneath the window.

**Signature moves:**
- The window arrives by rotating into position from a steeper angle (closer to side-view) and easing to its resting tilt.
- Internal UI populates with content while the window is still settling.
- Camera may dolly closer or pan around the window mid-shot.

**When to reach for it:**
- Cinematic "here's a real software environment" reveals — opening hooks especially.
- Worked-example modules where the application is the star.

**When to skip it:**
- Teaching modules where text needs to be readable straight-on — perspective makes labels hard to read.

---

## 09. Command Palette Pop

**Tone fit:** `universal`. The modal-as-subject pattern crosses every channel cleanly — adjust panel size/brightness to match tone.
**Reference:** `Examples/Shortcut.mp4`.

**Layout:**
- Black or near-black background.
- Center of frame: a single modal-style panel that looks like Raycast / Spotlight / a launcher — rounded corners, title bar, command options inside.
- Floating colored dots in the corners as ambient accent (red / green / blue / orange / purple).
- Tiny "LAUNCH" label above the panel in tracked-out small caps.

**Signature moves:**
- Panel scales in with a soft pop.
- Command options inside may animate as the user "selects" them with a moving highlight.
- Single decisive action shown, then settle.

**When to reach for it:**
- Single-action demos: "the agent runs this one command."
- Module beats showing a specific tool invocation.

**When to skip it:**
- Multi-step workflows — needs Editorial Spread + IDE panel, not a single modal.

---

## 10. Single Chat Card

**Tone fit:** `educational`, `universal`. The cream palette and patient cadence fit Byrddynasty natively. AI-content channels of any tone can use this.
**Reference:** `Examples/bluesweater.mp4`.

**Layout:**
- Cream warm background.
- One single chat input card centered on frame, rounded, slightly off-center, with light drop shadow.
- Inside the card: a prompt being typed character-by-character on a single line.
- Bottom-right of the card: an orange/accent send button.
- Tiny model identifier ("Opus 5.0 Extended") inline.
- A cursor (arrow) is visible pointing at the send button at the end.

**Signature moves:**
- Text types in at a natural human cadence (~80ms per character with occasional thinking pauses).
- A small loading indicator may appear above the card briefly.
- The cursor moves to the send button — implying the moment of action.

**When to reach for it:**
- "Watch one prompt complete" beats.
- Worked examples where the entire story is one user turn.
- High focus, low chrome, lets the words be the subject.

**When to skip it:**
- Anything that needs multiple turns or surrounding context — use Editorial Spread + chat panel instead.

---

## 11. Fanned Phone Trifold

**Tone fit:** `premium-product`. Mobile-app showcase native. Rarely belongs in Byrddynasty unless an actual mobile app is the teaching subject.
**Reference:** `Examples/phones.mp4`.

**Layout:**
- Soft pale gradient background (sage green in the example).
- Three phones in the center of frame, slight outward fan with mild perspective, the center phone tallest/closest.
- Each phone shows a different app state (e.g., onboarding / dashboard / detail screen).

**Signature moves:**
- Phones drift in from below in formation.
- Slight ambient rotation suggests floating.
- Camera may push in slightly toward the middle phone.

**When to reach for it:**
- Mobile UI showcase modules (less common in our agent-stack video).
- "A flow across screens" presentations.

**When to skip it:**
- When mobile isn't the subject — phones-as-decoration is the kind of thing we explicitly banned in DESIGN.md.

---

## 12. Vertical News Stack

**Tone fit:** `vertical-only`. Promotional re-cuts only (TikTok / Reels / Shorts). Not a primary shape for long-form modules; secondary for the promotional repurposing step.
**Reference:** `Examples/Stories.mp4` (9:16 vertical aspect).

**Layout:**
- Vertical 1080×1920 canvas.
- Stacked "news cards" — each with a headline, a hero image, optional sub-images on the right.
- Black sans-serif headlines, photo-driven, magazine-feed feel.

**Signature moves:**
- Cards scroll vertically as if a feed is being browsed.
- Each card holds long enough to read the headline.

**When to reach for it:**
- **Vertical promotional cuts only** — Shorts, TikTok, Reels.
- Not a primary shape for the long-form module; secondary for promotional repurposing.

**When to skip it:**
- The long-form 16:9 modules. Use this shape *only* when producing the vertical re-crop in step 8 of the per-module workflow.

---

## 13. Animation Paths Reveal

**Tone fit:** `promo-cinematic`. Pure kinetic abstraction — Faceless channel native. In Byrddynasty, only as a brief transition between major Parts, not as a teaching beat surface.
**Reference:** `Examples/Hermes.mp4` (~t=16s, "Motion paths").

**Layout:**
- Pure black background.
- Hundreds of small dots traveling along curved paths — forming organic infinity / butterfly / orbit patterns.
- A small monospace label appears at the bottom mid-frame.

**Signature moves:**
- The motion *is* the content — the dots draw their paths and persist briefly as trails.
- Often used to imply "behind the scenes, things are flowing."

**When to reach for it:**
- Abstract beats where motion *is* the meaning — "data flowing," "search beam scanning," "connections forming."
- Transitions between major teaching sections.

**When to skip it:**
- Concrete teaching — too abstract on its own; would need a paired explanation.

---

## 14. Numeric Reveal

**Tone fit:** `universal`. Every channel uses big-number reveals. Tune the count-up speed and number type-style to the channel's tone (fast + bold for promo, slow + serif for educational).
**Reference:** `Examples/Notion.mp4` (~t=15s, "62% of Fortune 100").

**Layout:**
- Pale or off-white background.
- One enormous numeric value centered on frame (200-300px tall).
- One short supporting line beneath ("of Fortune 100").
- A thin horizontal underline or accent mark.
- Optional: a row of small monochrome icons across the bottom as supporting detail.

**Signature moves:**
- Number counts up or arrives with a single decisive moment.
- Negative space around the number does most of the work.
- Hold long enough for the number to register.

**When to reach for it:**
- Cost-crash payoffs: 77K → 8.7K, 1.17M → 1K, 150K → 2K. (Frequent in our master arc.)
- Any beat where one specific number is the entire point.

**When to skip it:**
- When two or more numbers compete — use Cosmic Stats Reveal (multi-stat) instead.

---

## Shapes we may want to add later (not yet in catalog)

- **Side-by-side matrix** (Part 3 of master arc — comparison table). I have an idea but no reference example yet.
- **Decision tree / flowchart** (Part 3 — the "if X, use Y" rule). Will need to design from scratch.
- **Timeline scroll** (history beats, before/after sequences).
- **Talking head + overlays** (avatar full-screen with active graphics around it).
- **Veo cinematic** (photographic establishing shot — reserved for openings and transitions).

When a future module needs one of the above and we design it, **document it here first** before building.

## Discipline rule

A shape doesn't enter this catalog by being mentioned in a meeting. It enters by being either:
1. **Dissected from a real working reference** (current case for shapes 01-14).
2. **Built and proven in a rendered Byrddynasty module**, then back-documented.

That keeps the catalog grounded.

## Forbidden patterns (apply to ALL channels)

- Same shape used in three consecutive modules.
- A shape chosen because it's "the last thing we used" rather than the story's needs.
- A shape invented ad hoc per module without being documented here.
- Any visual register that defaults to "boxes on dark background with text" — the failure mode we've already named.
- **A shape used in a tone it doesn't fit without an adaptation plan.** (See `TONE-MATRIX.md` — porting a promo-cinematic move into an educational module requires documenting the conversion in the module's CONCEPT.md.)
