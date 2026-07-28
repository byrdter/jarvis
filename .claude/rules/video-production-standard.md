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
- Traffic was effectively **effectively 0% Browse / Search / External** — no algorithmic distribution.

**The channel is retention-gated, not quality-gated.** The product was never the problem; the first
thirty seconds and the runtime were. Everything below follows from that one finding.

---

## 1. Runtime and shape

- **~8 minutes** (7:30–9:00). Strangers give an unknown channel eight minutes, not fifteen.
- **Mid-video reversal at ~40–55%.**
- **2 shorts per video**, distinct angles, same hook discipline on the first second.
- Narrator is first-person **plural**. **No video references another** — this is a batch, not a series.

---

## 2. The cold open — INFORMATION FIRST

> **This section changed 2026-07-26.** It previously mandated FACE FIRST (avatar on camera from frame
> one). The channel is running a **faceless test**, so the avatar requirement is removed. The
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

### Known open risk in the faceless test
The avatar joke ("he writes every word, I just say them") disarmed the AI-voice objection. Going
faceless removes the avatar but **not** the synthetic voice, so the objection survives with nothing
disarming it. **Stop condition:** if first-30s retention drops against the face-first videos, the test
has answered and face-first returns.

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
