# Byrddynasty Video Standard — "Understanding AI"

**Scope:** every long-form video and every short. This is the single `.claude`-surface rule for video
production; it replaces `video-hooks-curiosity-gap.md` (deleted 2026-07-26).

Canonical detail lives in the skill — read it before scripting or building:
- `.agents/skills/jarvis-video-production/knowledge/RETENTION-AND-HOOKS.md` (§0 diagnosis, §3 curiosity
  gap, §7 ideation)
- `.agents/skills/jarvis-video-production/knowledge/CONDUIT-VISUAL-SYSTEM.md` (registers, components,
  density, VO binding)
- `.agents/skills/jarvis-video-production/PIPELINE.md` (the runbook + QC order)

---

## 0. Why any of this exists (our own Studio analytics, 2026-07-14)

_Exact figures live in the private analytics notes, not in this public repo. The finding:_

- **The large majority of viewers left in the first ~30 seconds.**
- A 15-minute video averaged well under a minute of view duration.
- ~~Traffic was **effectively 0% Browse / Search / External** — no algorithmic distribution.~~

> ### ⚠️ THE 0%-DISTRIBUTION LINE IS FALSE — corrected 2026-08-01 from the Studio export
>
> Byrddynasty lifetime: **93,735 impressions · 3.69% CTR · 286.9 watch-hours · 147 subs.** The
> channel has always had algorithmic distribution — 4× KeyAdvances' impressions at a better
> click-through rate. Whatever that 0% figure described (a date window? a single video?), it is not
> true of the channel, and treating it as true produced a full day of wrong strategy on 2026-07-31.
> **Authoritative numbers now live in `jarvis-video-production/knowledge/BYRDDYNASTY-CHANNEL-AUDIT.md`.
> Read that before reasoning about distribution.**
>
> **The retention finding below still stands and is now better supported:** impressions per video
> fell 7.8× (2,862 → 368) between Feb and Jul 2026 while **CTR stayed healthy (Jul median 3.70%)**
> and watch-time per video fell **14×** (12.4 h → 0.87 h). The channel is retention-gated. It was
> never distribution-gated.

**The channel is retention-gated, not quality-gated.** The product was never the problem; the first
thirty seconds and the runtime were. Everything below follows from that one finding.

---

## 1. Runtime and shape

> **This section changed 2026-07-29.** It previously hard-coded **~8 minutes**. That number was a
> *training wheel*, not a law: §0 found the channel retention-gated, and 8 min was the discipline
> imposed *while retention was unproven*. The old 12–15 min videos did not fail because 15 is too long
> — they failed because they had no whole-runtime loop and shed viewers past 0:30, so length
> multiplied the leak. Runtime was never the disease; retention was.

> ### ⛔ HARD FLOOR: 8:00 — MONETIZATION. Set by Terry 2026-08-02, channel-wide.
> Under eight minutes YouTube blocks mid-roll ads. This is a business constraint, not a craft
> preference, and nothing below overrides it. **There is no upper bound** — length is set by the
> material. Everything in this section is about shape *above* that floor.
>
> **Verify the floor against RENDERED AUDIO, never a word count.** Measured 2026-08-02: a word-count
> estimate ran **82 seconds long** on a 17-minute script, because the model counts
> `11,346,275,422.` as one word when it is **6.2 seconds** of speech. Measured rates on our own
> Cartesia voice ranged **119 wpm** (number-dense) to **175 wpm** (prose) *in the same script*. A
> script that estimates 9:00 can render under the floor and lose monetization silently.
>
> Note `tools/prepublish-check.py` still enforces a **15-minute** floor and will FAIL anything
> shorter. That threshold was calibrated for the conduit-essay format, which is 0-for-22 on this
> channel. When the target lane's winners run shorter — the Claude-pricing lane's measured winners
> run **6.7–9.9 min** — that FAIL is expected and must **not** be cleared by padding. Record the
> exception in the script header and ship. Every other check still has to pass.

**Runtime = the longest you can sustain a withheld payoff at high retention — no longer.** YouTube
rewards *total watch time* (runtime × retention), so longer wins **iff** the curve holds. The rule is
now a mechanic, not a number:

- **Start a rebuilding-retention batch at ~10 minutes**, then let the audience-retention graph vote.
  Holds past ~40% at the 10-min mark → push the next video to 12–13. Sheds after the reversal → the
  back half is too long; tighten. Two videos of real retention data beat any a-priori number. **Never
  blind-ship 12–15 again — that shape is what failed; only ship it once the curve has earned it.**
- **Precondition for ANY runtime over ~8 min — all three, or trim to 8:**
  1. a payoff **withheld across the whole runtime** (a mystery or punchline, not just a 0:20 hook —
     this is what holds the 19/30/45-min proven builds; see the 2026-07-29 teardowns). **This is now
     a measured gate, not a wish:** `jarvis-video-production/knowledge/NARRATIVE-STRUCTURE.md` +
     `tools/narrative-measure.py` — first payoff ≥40% of runtime, spine silent-gap ≤90s, CTA after
     the verdict. Our *AI Doesn't Hallucinate* master failed the first two at **5.6%** and **539s
     (58% of runtime)** while beating a 73× outlier on negation and loop density — which is how we
     know the device checklist alone is not sufficient. **Run it on the VO draft, before recording.**
  2. a **persistent on-screen progress spine** (scale ladder / component checklist / numbered
     framework / section badge — the real retention device),
  3. a **reversal at ~40–55%**.
- **Data point behind the ceiling:** the highest-outlier *reachable* data-viz winner (Big Data Factor)
  is **5:45**; the 30- and 45-min winners are already-large channels. Short + tight throws the biggest
  outlier from a cold start. Length is a privilege retention earns, not a default.
- **2 shorts per video**, distinct angles, same hook discipline on the first second.
- Narrator is first-person **plural**. **No video references another** — this is a batch, not a series.

---

## 2. The cold open — INFORMATION FIRST

> **This section changed 2026-07-26; settled 2026-08-02.** It previously mandated FACE FIRST (avatar
> on camera from frame one). **The channel is faceless and the avatar is gone permanently** — not a
> test, no stop condition, no reversion path, no opt-in. The avatar requirement is removed; the
> *mechanism* behind the old rule is kept, restated below.

§0 found the dying videos opened on **dark abstract graphics** with a disembodied voice for ~20s —
"AI slop." The fix was never the face as such; the face was one way to satisfy the real requirement:

**The first frame must carry concrete, specific information the viewer can read, and the VO must be
about that thing.**

- ✅ A named document, a filing, a headline, a real number, a chart with a labelled axis.
- ✅ A face (a person is talking) — still valid, just no longer required.
- ❌ A gradient, a particle field, an abstract cityscape, a kicker label alone. Mood is not information.

*Proven instance:* the Messi cold open lands a California Secretary of State filing — entity name
PLAY TIME — stamped REGISTERED, inside two seconds. Dark register, but concrete from frame one.

### Structure
1. **0:00 — the concrete thing on screen**, VO already inside the story.
2. **0:00–0:20 — THE HOOK.** The single most provocative concrete stake, as a **paradox** where possible.
3. **0:20–0:35 — RE-OPEN THE LOOP.** End on a **named question**, not the thesis.

### DELETE FOREVER
The "38 years" bio, "on this channel we keep asking one question," "Welcome back to Understanding AI,"
"today we're going to explore…" — every line that says the video hasn't started. Be started.

### Known open risk — not solved by bringing the avatar back
The avatar joke ("he writes every word, I just say them") disarmed the AI-voice objection. Faceless
removes the avatar but **not** the synthetic voice, so the objection survives with nothing disarming
it. **That risk is accepted** — the avatar is not returning. If the objection ever needs answering, it
gets answered faceless, through what is on screen and what the writing earns.

### Three devices that sharpen the open
1. **Adversary in sentence one.** Open on a conflict with sides, not a topic. If sentence one is a
   fact, lead instead with the claim that fact argues against.
2. **The negation ladder.** *"Not because X. Not because Y. Because ——."* Deny the two guesses the
   viewer would reach for; withhold the third.
3. **Decline the frame fight.** When a proven competitor owns the obvious framing, name the whole
   argument as the wrong question and step outside it.

> Then **cut what the new open already delivers** — sharpening the first lines makes a later paragraph
> redundant. Re-scan the next two scenes and delete it, or you've only added runtime.

---

## 3. The curiosity-gap rule (use forever)

Hooks work by **opening gaps, not hiding information**. The test is never "how much did I reveal?" It
is: **does the viewer now have a question they genuinely cannot answer alone?**

- **Reveal FACTS freely** — events, numbers, the situation. They build credibility and tension.
- **Withhold MEANING** — explanation, mechanism, verdict, twist. That's the payoff they stay for.
- **Prefer a PARADOX** — self-sealing; more information *deepens* it rather than resolving it.
- **Boundary: reveal up to the QUESTION, stop before the ANSWER.**
- **Loop-naming ≠ agenda-setting.** ✅ "and who decides what we do about it" ❌ "today we'll look at
  some studies."

**One line:** *give them the locked door and let them see it's locked; do not hand them the key.*

---

## 4. The visual system — what a finished video looks like

Reference build: **Messi / "Secretly an AI Investor"** (2026-07-26 master). Full spec in
`CONDUIT-VISUAL-SYSTEM.md`.

### Two registers, used with discipline
- **Cream document card** — bone paper, serif display head, letterspaced mono kicker, hairline rules,
  label/value rows, circular seal. Carries **evidence**: filings, licences, certificates, source
  captures.
- **Dark navy panel** — deep slate card, gold primary / teal secondary accent, serif head, mono
  numerals. Carries **analysis**: cap tables, dossiers, dockets, portfolios, comparisons.

Both sit over a **darkened, defocused photographic bed with continuous ambient motion**. One brand
accent per scene; never mix except at a deliberate comparison split.

### The signature device — progressive disclosure with ghosted placeholders
Unrevealed rows are **visible but dimmed**, then resolve. It tells the viewer how much is still coming.
Use it — but content must resolve within **~1.2s** of the panel appearing. Held longer, it reads as a
dead frame (this was the single defect the QC gate caught on the Messi build, three times).

### Density
Target **45–60 visual change-events per minute** (scene-detect threshold 0.02). Measured baselines:
strong scene 56.8, good scene 44.0, weak scene 28.9. Prefer **within-beat motion** — fields populating,
counters running, stamps landing, beds drifting — over rapid cutting. That reads as continuous rather
than choppy, and it is the channel's chosen feel.

### Information variety — every video should use most of these
Documents · data tables with a highlighted row · charts with labelled axes · schematic maps ·
browser/search chrome · annotation HUDs · numbered grids · stat heroes · comparison splits · real
source captures · library video clips · generated stills · typeset lockups.
A plain full-frame text card is permitted **only** for a title or a landing line.

---

## 5. VO BINDING — the 90/10 rule

**≥90% of runtime must be DENOTATIVE:** the visual illustrates the specific claim the VO is making at
that second. Numbers, names, dates, documents, places, relationships — show the thing being said.

**≤10% may be ATMOSPHERIC** — a loosely related or purely tonal visual. Permitted at **transitions and
breathers** (e.g. a stock clip of someone working at a computer while bridging between topics).

**Never atmospheric on a beat carrying a number, a date, a name, a citation, or a verdict.** Those beats
are why the channel is trusted.

Classify every beat as one or the other in the beat map. If a scene cannot say which, it isn't planned.

---

## 6. Process integrity — how this stops being aspirational

Learned the hard way on 2026-07-26: **every one of the day's defects was already "documented."** The
QC gate was specified in prose and had never run. A card manifest asserted quotes were verbatim; the
pixels disagreed. Beat maps described a design two revisions old. The CLI pin disagreed with the
installed binary in three files.

1. **Verify against the artifact, never against the document.** Check the rendered PNG, not the YAML
   that describes it. A written "verified" line is a claim, not a check.
2. **A gate that isn't a runnable script doesn't exist.** Prose in a knowledge doc will not run.
3. **Measure before asserting.** Counting lines in a plan is not measuring the render. Two confident
   conclusions were wrong on 2026-07-26 for exactly this reason.
4. **Both kinds of check are load-bearing.** The gate caught dim beats a human eye had passed over
   repeatedly; the human caught a production countdown timer no gate would ever flag. Neither replaces
   the other.
5. **When the CLI pin moves, re-render the whole batch** — one master must never mix versions.

---

## 7. Considered and REJECTED (do not re-propose)

- **Cut-on-twos / 12fps quantisation.** Deliberately choppier motion; points away from the chosen
  continuous feel. Rejected 2026-07-26.
- **Chromatic aberration or heavy grain over text.** Degrades exactly the citation legibility that is
  the channel's credibility.
- **Halftone / paper-texture grade.** Belongs to a paper-collage register this channel doesn't use.
- **"The gap is surface texture."** Retracted. The gap was doc↔build drift and unenforced gates.
- **"The videos are under-dense."** Retracted — that conclusion came from counting plan lines, not
  measuring renders. Measured, the cold open is the densest scene in the video.

*Still open for one-scene experiments:* footage homogenization (a shared treatment so library clips,
generated stills and HyperFrames output stop looking mismatched at cuts).

---

## 8. Ideation runs upstream of all of it

A perfect hook on a dead concept still dies.
- **Outlier score = views ÷ the posting channel's sub count.** Never rank by raw views. >5× is a
  candidate; weight toward channels near our size.
- **Combination titling:** fuse two independently-proven concepts into one that doesn't exist yet.
  Prefer fusions that produce a **paradox** — that's where the §3 hook is born.
- **Burning problem, not mild interest** (job / kid's education / safety / can't tell what's true).
  Low competition usually means no proven demand, not an open lane.
- **Gate the EXECUTION, not just the lane** (learned 2026-07-30, the data-center build). "How big is an
  AI data center" probed PROVEN — but production then committed to a *narrower, un-probed* bet (one company
  + a lawsuit + a breaking-news legal fight) and ~450k tokens went in before anyone measured whether *that
  version* travels. It didn't: the specific angles split hard — generic scale-explainer PROVEN, community
  harm ("what it does to the town next door") a MONSTER (955× / 13.4×), but the Musk/legal/DOJ framing
  THIN–DEAD (0.03–0.89×). Re-probe when the anchor, framing, or emotional core narrows the proven lane —
  grounding rigor never rescues a mis-aimed target, and a build chat in flow is the least likely to notice
  the drift. **Self-relevant + evergreen beats fresh + exciting:** the breaking-news register (DOJ/Grok/
  lawsuit) is exactly the lane this channel loses in — it's not about *you*, and it dates. Witness the
  harm to a community ("could be your town"), don't cover the courtroom.

---

## 9. VISUAL SOURCING — hard rules (Terry, 2026-07-30, after the job-dissolving v2 review)

The v2 rebuild fixed "footage-first" but broke on *how* footage is used. These are **hard rules**, not
preferences:

1. **One clip, once per video.** A given video clip may appear exactly ONCE in a finished video. No
   reuse anywhere. (v2 tiled the same br clip across a whole scene — it visibly loops. Never again.)
2. **Clips ≤ ~6 seconds.** A clip runs 6s max unless the action genuinely needs longer (e.g. a
   meaningful gesture — a finger tracing a row, two people in exchange). A clip may run scene-length
   ONLY when it *is* the scene's single shot and does not loop/repeat.
3. **Never a blank/black frame.** Beds must tile continuously; a `<video>` blanks to black once its
   data-duration exceeds the clip length — so tile distinct clips, don't over-run one.
4. **No naked text on screen.** Information lives INSIDE an artifact — a real document, a citation-card
   screenshot, a webpage, a terminal/VS-Code simulation, a data-viz graphic, or an org chart (text only
   as labels on the side of the graphic). Naked centered/lower-third text is a LAST resort, only when
   there is genuinely no artifact form for that beat.

**Consequences that follow:**
- **Citation cards throughout.** A research/evidence video with zero real source captures is wrong.
  Capture the actual sources (Playwright `channel="chrome"` clears Cloudflare) and cut to them at every
  evidence beat — the number highlighted ON the real page, not retyped as naked text.
- **Match the clip to the VO literally.** "writing / scheduling" → show writing and scheduling, not an
  abstract conveyor. "radiologist" → a radiology reading room / X-ray / MRI, not a random person.
  "the researchers" → a research office / people discussing research. A boundary "moving" → an org
  chart that shifts (built in HyperFrames), not a FIRED/PROMOTED text stamp.
- **Rotate footage; don't camp on one shot.** Change the shot every ~5–6s; never show the same setup
  (paper pile, data-wall board, person-at-screen) repeatedly across a video.
- **Diversity.** Include people of colour across the clip/still selection.
- A large video needs a LARGE pool of distinct clips (≈ runtime ÷ 6s). Source them from
  `asset-library` (`search-assets-db.py --db asset-library/assets.db`) and GENERATE the gaps; never
  paper over a shortage by reusing or over-running a clip.

### 9a. VO-MATCHING IS THE FIRST STEP (Terry, 2026-07-30 — the root cause)

> *"The main problem is you are not matching the visuals with the VO. Examine that first."*

Before building ANY scene, run this audit and write it into the beat map:

1. Segment the scene transcript into VO **phrases** (split on word gaps > ~0.45s).
2. For each phrase, write the exact words, then the artifact/clip that answers *those words*.
3. Only then build — and every element's start time comes from its phrase's start time.

**Failure signature (all three found in one 52s scene):** a clip that illustrates the *topic* but not
the *sentence* ("weren't looking for layoffs" over generic typing); an element arriving early and
holding empty until its line lands (a chart ring waiting 3.4s); a device appearing before the VO names
it (the org chart 6s before "org chart"). If a visual can't be traced to the phrase under it, it's wrong
— no matter how good it looks.

**Corollary — the artifact must answer the negation too.** "Nobody was fired, nobody was promoted, the
boundary moved" is not a text stamp: it's a personnel record whose Fired/Promoted/Title/Pay rows read
UNCHANGED while the "work actually performed" list keeps growing. Show the contradiction inside one
artifact.

**And keep the bed.** Graphics/artifacts still sit over the darkened, moving photographic bed — an
artifact on flat black is a dead frame.

---

## 10. HUMAN PRESENCE, WORD-SYNCED CARDS, REAL CLIPS (Terry, 2026-07-30)

Refined watching **Logically Answered (LA)**. Rules 1–4 above (one-clip-once, ≤6s, no blank frame, no
naked text) stand. These extend them — the goal is LA's *density of human presence* and its
word-locked citation cards.

### 10.1 Maximize human presence — every scene should have a person if it can
Rank of sources, use them all across a video:
1. **Library human clips** — 193 of 353 clips in `asset-library/assets.db` have people (query
   `people`); the pixelart character series (developer at desk, hand writing, frustrated debugging,
   person pointing at screen) is Terry's own and adds **lightness/surprise** — use it liberally.
2. **Created two-person debates** — anonymous, generated, animated (the job-dissolving
   `OptimisticSceptic` method: still → I2V, or Runway Act-Two). Lower-third `ILLUSTRATION`. Use for any
   beat where two readings collide (a fork, a "some say X / others Y").
3. **Real press/news PHOTOS of named people** — CEOs, researchers — **≤5s, in passing**, attributed.
   Terry has used these before without issue. Per `references/USING-REAL-PEOPLE.md`.
4. **Terry's pixelart characters** (`asset-library/clip-library/pixelvideos`) — the surprise/levity beat.

### 10.2 Word-synced citation cards — the LA karaoke technique
When a cream citation card is on screen, **highlight it word-by-word in lockstep with the VO reading
it.** `tools/cue.py` already returns word-start times from the transcript; a highlight tween pinned to
those times on the registered `tl` is deterministic and seek-safe. Build the highlight component ONCE
and reuse. This is a **standing technique for every evidence card**, not a one-off.

### 10.3 Brief third-party YouTube clips of a person being discussed (rule 7)
Allowed, on the same terms as press photos: **brief (a few seconds), attributed, about the person or
their own work**, sourced from their / their company's channel. (LA uses talking clips of e.g. Chamath
this way.) It is the strongest human-presence beat available for a video about a specific person's work
— e.g. the study's own author explaining it. Governed by `references/USING-REAL-PEOPLE.md`: real
footage only, transformative, name+source on screen, never implying endorsement. When no clean clip
exists, fall back to 10.1.

**Consequence for asset planning:** every scene's visual is now tagged one of — `[LIBRARY]` (single-use
≤6s), `[GENERATE]` (created debate / gap clip), `[SOURCE-REAL]` (press photo / third-party clip), or
`[CARD]` (word-synced citation). A scene with none of these and only naked text is a defect (rule 4).
