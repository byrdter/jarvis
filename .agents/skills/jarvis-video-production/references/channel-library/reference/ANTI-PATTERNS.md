# Anti-Patterns

Hard-won failures across Modules 04–09. Every one of these cost us a re-render. Read this before every build.

---

## Composition

### A1 — Boxes-on-boxes
Any visible element overlapping another visible element's bounds. The eye reads this as broken, not layered.

**Examples we hit:**
- Module 08: MCP satellite at 18% opacity covered the "Tools." headline. *Fix:* fade headline to opacity 0 fully before satellite arrives.
- Module 09 r1: Promoted cost meter overlapped Skills + Code Exec satellite cards. *Fix:* fade satellites to 0 during meter promotion; bring them back at row positions in Beat 6.

**Discipline:** Before rendering, mentally map every animated element's bounds at every beat boundary. If two elements share screen real estate at the same time, decide which one wins (fade the other) or move one out of the way.

---

### A2 — Text-on-text
Any caption, label, header, or counter overlapping another text element. Even at low opacity, the eye reads two strings as one garbled line.

**Examples we hit:**
- Module 09 r1: "200K TOKENS" subheader briefly overlapped the "TOKEN COST" orange label during meter promote. *Fix:* remove the obsolete label entirely (`display: none`).
- Module 09 r1: Cost-band labels for thin sub-type bands (CLI, Skills, Code Exec) crammed into ~26px of vertical space. *Fix:* explicit `top` offsets per label with thin leader lines connecting to bands.
- Module 09 r1: "BEFORE YOU'VE DONE ANY REAL WORK." caption ribbon stretched full-width and overlapped the bottom of the cost meter. *Fix:* narrow ribbon and left-align it into the empty half of the frame.

**Discipline:** Same as boxes-on-boxes. The fix is usually one of three things: (a) fade one text element out before the other appears, (b) move one to the empty half of the frame, (c) give explicit positions with leader lines instead of relying on auto-centering.

---

### A3 — Default to the previous module's shape
Reusing the previous module's composition because "it worked." Every module's shape must be chosen deliberately for the role it plays in the arc.

**Example we caught early:** Module 08 (Tools — climax) was tempted to reuse the editorial spread + chat panel shape from Modules 04–07. *Decision:* break the shape deliberately. Tools is the arrival, not another sibling beat. Dark product showcase with centerpiece + satellites was the right shape.

**Discipline:** Step 1 (`CONCEPT.md`) requires a "Visual shape (and why)" field. If you can't justify the shape choice in writing — why this shape, why not the previous one — you have not done Step 1.

---

### A4 — Repeating a shape across non-sibling beats
The parallel-set shape (Modules 04–07) works because those four modules ARE siblings. Reusing the same shape for a non-sibling module dilutes the narrative.

**Discipline:** Sibling beats can share a shape. Climax beats need their own shape. Closer beats need their own shape. Openers need their own shape. Decide what role each module plays; then pick the shape.

---

## Animation

### A5 — Infinite repeats (`repeat: -1`)
The HyperFrames deterministic capture engine seeks to exact frame times. Infinite repeats break this. The lint warns: `gsap_infinite_repeat`.

**Fix:** Use a finite count calculated from composition duration:
```js
repeat: Math.floor(duration / cycleDuration) - 1  // Math.floor, not Math.ceil
```

**Hit in:** Module 09 r1 (Tools centerpiece breathing animation). Fixed by limiting to a finite count that fit within Beat 1.

---

### A6 — Animations firing before VO catches up
Visuals leading by more than 1.5s feels disconnected. Visuals lagging the VO at all feels broken.

**Discipline:** Get word-level timestamps from whisper-cli. Anchor each animation to a VO word boundary, leading by 0.3–1.0s for build-ups, leading by 0 for punchlines.

---

### A7 — Element with `transform-origin` not set explicitly
Scale and rotate animations on elements without `transform-origin: center center` (or whatever you intend) will pivot from arbitrary origins, causing weird drift.

**Discipline:** Every `scale`, `rotate`, or `transformOrigin`-sensitive tween needs explicit `transformOrigin` in the tween config.

---

### A8 — `opacity` animated together with `display: none`
GSAP can animate opacity, but it can't animate `display`. If an element is `display: none` initially, GSAP won't tween its opacity until display is removed.

**Fix:** Use `opacity: 0; visibility: hidden;` for hidden-initial elements, then animate opacity and visibility together. Or default to `opacity: 0; pointer-events: none;` for elements that need to be invisible but layout-present.

---

## Audio

### A9 — Trusting HeyGen duration estimates
HeyGen's stated duration on a generation request is not the same as the actual MP4 duration. Modules 08 and 09 both had VOs ~15-20s shorter than the script estimate.

**Discipline:** Always probe the actual audio duration first:
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.wav
```
Then remap beat timings against that exact duration. The composition `duration` field in `hyperframes.json` should be audio length + 2–4s tail.

---

### A10 — Multi-occurrence anchor words
When using `find_splits.py` to locate VO timestamps, common words ("image", "goal", etc.) may appear multiple times. Without an `nth` parameter, the script returns the first occurrence — which may not be the one you wanted.

**Discipline:** When using anchor words, prefer unique phrases. If a word appears multiple times, pass the occurrence index explicitly.

---

### A11 — Groq Whisper blocked, OpenAI key empty
Groq's Whisper API is blocked by Cloudflare 1010 on Terry's network. OpenAI fallback was empty in `.env`. Always use local `whisper-cli` with `ggml-small.en.bin` from `~/.cache/hyperframes/whisper/models/`.

---

## Pipeline

### A12 — Editing without reading first
The Edit tool requires Read first. Don't try to edit a file you haven't read in this session — it'll error.

---

### A13 — Skipping the storyboard checkpoint
The Nano Banana Pro storyboard is $0.10. The HTML build is hours. Always pass the storyboard checkpoint before HTML. If the storyboard composition is wrong, fix it before building.

---

### A14 — Composition file > 500 lines
HyperFrames lint warns: `composition_file_too_large`. Past ~500 lines a single composition becomes hard to iterate on and diff.

**Fix when this triggers:** Split into sub-compositions under `compositions/` and mount with `data-composition-src` from the parent.

---

### A15 — Skipping critique pass
No module ships on first render. The keyframe-extraction-and-read pass IS the critique. Skip it and you ship broken frames.

**Discipline:** Always extract keyframes at every beat boundary AND read them. The Read tool on a JPG works — use it.

---

## Voice

### A16 — First-person singular in collective-voice videos
Per the Jarvis memory `for-jarvis-dr-terry-byrd-youtube-video-dialogue`: collective voice (we/our/ours) by default. The only first-person-singular exception is the opening avatar self-intro ("I am the avatar for Dr. Terry Byrd...").

**Discipline:** Read VO drafts with this lens. Replace "I" → "we" except in the explicit avatar intro slot.

---

### A16.5 — Fragment-as-slogan VO writing

Short staccato fragment sentences ("One standard. Every agent. Every service.") read as marketing slogans, not teaching. The viewer has to fill in what the phrases mean. That defeats the educational role of the channel.

**The directive (from Terry):** *"I don't like those one-word phrases. We are teaching and I want to make sure we are clear in what we are saying. I like things explained out and not left to the imagination of what someone is talking about."*

**Bad (fragment-as-slogan):**
> *One standard. Every agent. Every service.*

**Good (full explanatory sentence):**
> *MCP is the single standard that every adopting agent uses to communicate with every adopting service, without either side needing to know the proprietary protocols of the other.*

**Rules:**
- Default to complete sentences with subject + verb + object. Spell out what each phrase means.
- Compact short sentences (e.g., "Developed by Anthropic.") are acceptable when they read as a complete thought — but combine them when possible into fuller phrasing ("Developed by Anthropic and adopted across the agent service provider ecosystem.")
- **Avoid three-fragment slogans entirely.** If you find yourself writing "X. Y. Z." as three nominal phrases in a row, rewrite as a sentence.
- Punchlines are allowed when they're complete sentences ("That is the core idea of MCP.") — but not when they're noun phrases ("One protocol.").
- Teaching tone over marketing tone. We are explaining, not selling.

**Discipline:** read every VO draft aloud at the intended delivery pace. If a line feels like it would land in a Super Bowl ad rather than a college lecture, rewrite it.

---

### A19 — Static composition holding for the entire module

**The trap I keep falling into:** building one composition with persistent elements (header at top, row at bottom, central element) and having beats animate IN AND OUT WITHIN that frame. Even with "fewer boxes," the **composition rhythm never changes** — the viewer sees the same architectural shape for the entire module. Different content, same picture.

**The directive (from Terry):** *"You don't have to stay on one page for the whole time. You can push pages and large graphics in and out. For example, in talking about the agents, Claude Code, Codex, etc., you could pop up large facsimiles of their apps across the page with their logos displayed prominently across the page and then show the various services cascading up the pages for a few seconds while you talk about them — not this boring boxes or text with a single line between them, boring, boring, boring."*

**The architectural fix — use scene-based clips, not one timeline.** HyperFrames natively supports it via `class="clip"` + `data-start` + `data-duration` on each scene's outer wrapper. Each beat is its own FULL-FRAME scene that materializes, holds, and exits — not a layer in a master composition. See `hyperframes-helper/SKILL.md` and `recipes.md` for the multi-clip pattern (recipe 6) and pulse-ring logos (recipe 7).

**Concrete techniques to reach for instead:**
- **Push-page transitions** — a whole-frame scene slides in (or fades up), holds, then yields to the next scene that pushes in from a different direction.
- **LARGE PRODUCT FACSIMILES with prominent logos** — when naming brands/products (Claude Code, Cursor, GitHub, Slack), use ~300-400px brand marks with pulsing-ring halos. Not small inline labels.
- **Cascading elements** — items scroll/cascade up the frame as the VO enumerates them. Not appearing in fixed positions, ENTERING from offscreen with motion.
- **Scale changes between beats** — one beat is full-frame product, next beat is intimate code detail, next beat is wide-angle ecosystem. The eye gets variety.
- **Real-feeling chrome when warranted** — when showing an agent product (Claude Code), use a liquid-glass card with the actual brand logo. Not a generic dark navy "AGENT" placeholder.
- **Different dominant axes per beat** — beat 3 might be vertical (cascading services), beat 4 might be horizontal (bridge), beat 5 might be radial (constellation), beat 6 might be focused-center (code detail).

**Test:** Look at the keyframes across all beats. Do they look like the SAME picture with different elements visible? If yes, you've fallen in the trap. Each beat should have a visibly different architectural composition.

---

### A18 — Default to a card for every element

Cards / boxes / contained panels are a tool — not a default. Modules 04–09 leaned on cards heavily (chat card, satellite cards, indicator cards, centerpiece, chapter card, caption ribbon). For Part 2, that pattern needs to break.

**The directive (from Terry):** *"Think outside the box, literally and figuratively. Not so many boxes in these."*

**Use a container when:**
- Content needs isolation from the stage (a chat panel, a code terminal, an IDE window — known recognizable surfaces).
- Content represents an entity with internal complexity (a stat block, a chapter card with multiple lines + dots).
- Content needs strong visual weight (the climax centerpiece).

**Do NOT use a container when:**
- The content is a single word or phrase — let large Fraunces type carry it on the cream stage.
- The content is a label on a diagram — use floating type with a thin leader line, not a chip.
- The content is a stat or number — let the number itself be the visual, with the cream stage as breathing room.
- A flow diagram has nodes — make nodes small dots with floating labels, not labeled rectangles.
- A callout points at an existing element — use a sketchy arrow + floating type, not a chip.

**Non-card techniques to reach for first:**
- **Type-as-design** — large Fraunces serif at 200pt+, the word IS the visual.
- **Free-floating callouts** — Inter or Fraunces text with a thin leader line to its target, no chip.
- **Sketchy annotation** — hand-drawn-feel arrows, marker-style highlights, scribble underlines (HyperFrames has a sketchout treatment).
- **Particle flows / data streams** — abstract motion between conceptual points, no containers.
- **Background-as-subject** — gradient washes, photo-textures, animated grain patterns ARE the content for a beat.
- **Negative-space split** — different zones of the cream stage doing different things, separated only by spatial gaps (no dividers).
- **Real-software chrome** — when you need a "window," use a known UI (VS Code, terminal, MCP Inspector), not a generic dark card.
- **Tilted / rotated elements** — break the rigid grid that boxes enforce.

**Test:** Before adding a card, ask: *"Could this be type-on-stage, a floating label, a particle, or a sketchy callout instead?"* If yes, do that.

---

### A17 — Forgetting the storytelling commitment
Every Tools-is-where-we're-heading line in Modules 04–07 cashes in Module 08. If Module 04 doesn't plant the seed, Module 08's climax fails. The arc is the load-bearing decision.

**Discipline:** Read the master arc every time you start a new module's concept. Confirm what this module is supposed to plant (for later modules) and what it's supposed to cash (from earlier modules).
