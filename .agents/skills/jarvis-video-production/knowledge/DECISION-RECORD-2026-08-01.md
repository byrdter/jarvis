# DECISION RECORD — channel direction, 2026-08-01

**Status: DECIDED. Do not relitigate before video 10.**
Terry's call, made after the 2026-07-31/08-01 measurement work. This record exists so the decision
stops being reopened every session.

---

## THE DECISION

**Byrddynasty runs the BUILD-INVESTIGATION register. One video per week. 15–25 minutes.
Ten videos, then evaluate.**

- **Register:** a named real AI system + a number + a verdict, on something Terry has actually built
  or actually examined. Practitioner audience.
- **Cadence:** 1/week. ~10 weeks to a full evaluation set.
- **Runtime:** 15–25 min.
- **Repurpose:** the week's material feeds other platforms (see §5).
- **Nothing is deleted.** The existing catalogue stays up.

## 1. Why this register — the evidence

Measured, all first-party, all in this folder:

| Era | Videos | Impressions/video | Result |
|---|---|---|---|
| Dec 2025–Jan 2026 — technical tutorials | 27 | ~350 | died |
| **Feb–Apr 2026 — build investigations** | — | **2,862 (Feb)** | **worked** |
| Jul 2026 — conduit essays | 22 | 368 | died |

- **3 videos produced 65 of 109 long-form subscribers.** All three are Claude Code / JARVIS builds.
- **2 videos produced 97 of 278 watch-hours.**
- **11 of the top 12 CTR videos** (≥500 impressions) are agent-engineering builds.
- Feb 27 → Mar 6 was **seven videos, one subject, eight days** — the only coherent run the channel
  has ever had, and the only time it spiked (42,890 impressions, 68 subs).

Sources: `BYRDDYNASTY-CHANNEL-AUDIT.md`, `TEN-TITLES-PROBE-2026-08-01.md`,
`teardowns/Tlqe0A8ED8o.md`.

## 2. What this is NOT

**Not "go technical."** The most technical era was the worst era. Both of these are technical:

| Died | Worked |
|---|---|
| *Testing AI-Written React Components with Vitest* | *Inside **Anthropic's** Agent Harness: **200+** Features* |
| *The API Layer Pattern: Clean Data Fetching* | *Why AI Agents Fail After **2 Hours** (And How Harnesses **Fix It**)* |

The difference is a **named subject people are already trying to understand**, plus a **verdict**.

**The real axis is audience, not topic.** Practitioners want utility (*How to Optimize Token Usage in
Claude Code* — 14.11× on 5,450 subs). General audiences want story. **The recommender can only learn
one.** That is why the swinging cost more than either register did.

## 3. Per-video craft floor — NON-NEGOTIABLE

Set against our own 8.00× *Agent Harness*, which had none of these. The 69–82× teardowns all did.

| # | Device | Agent Harness | **Floor** | Evidence |
|---|---|---|---|---|
| 1 | Negation density | 1.3/min | **≥3.0/min** | strong |
| 2 | wpm | 125 | 135–150 | **weak — advisory** |
| 3 | Concrete data points, first 45s | — | **≥8** | strong |
| 4 | Forbidden phrases | 2 violations | **0** (1 documented exception) | strong |
| 5 | Runtime | 19:26 | **15–25 min** | strong, this lane only |
| 6 | One loop named early and **carried** | ✖ 0 carried | **≥1 carried** | strong |
| 7 | Authored reversal at 40–55% | ✖ none | ✅ required | strongest |
| 8 | Persistent on-screen spine | ✖ | ✅ required | strong, not text-detectable |

**Enforced by `tools/prepublish-check.py`** — run on the VO script *before* render, the cheapest
point to fail. It imports its term lists from `teardown.py` so the pre-publish ruler is byte-identical
to the one that scored the reference videos. A different ruler would make the floor meaningless.

### 3.1 Definitions — the authoritative spec

**1. NEGATION DENSITY ≥3.0/min.** How often the narration marks a limit, contradiction or
correction. Terms come from `teardown.py:NEGATION` (*can't · cannot · doesn't · isn't · never ·
nobody · fails · failure · wrong · myth · limit · ceiling · wall · impossible · breaks · debunk ·
actually · turns out · but · however · except · unless*).
Measured: Mackard 4.0 (73.03×) · Universal Resilience 3.1 (69.61×) · **ours 1.3 (8.00×)**.
*Why:* an argument built from contradiction creates tension; a description does not. Ours is a
description.
**Anti-gaming sub-check:** hedge terms (`but · however · actually · don't · doesn't`) must be
**≤50%** of all negation hits. Noema scored 3.4/min but ran `but(104) don't(53)` — conversational
hedging, not authored negation. Universal Resilience skewed to `limits(9) impossible(6) cannot(5)`.

**2. WPM 135–150 — ADVISORY, DO NOT BLOCK ON IT.** Narration words per minute.
Measured: Noema 168 (81.81×) · Mackard 151 · Universal Resilience 136 · **ours 125** · Fractal 183
(6.06×). n=5 and the top scorer sat at 168 — the real signal is "not 125, not 183." Warn only.

**3. ≥8 CONCRETE DATA POINTS IN THE FIRST 45s.** A number, date, proper noun (company / person /
named system), named document, or quoted figure — anything the viewer can verify or picture.
Measured: Mackard's 44s open = **8** (`2023 · up to 80% of software developers · by 2025 · 152,000
laid off · Q1 2025 · Intel · Amazon · 30,000 roles`). Universal Resilience = 8
(`1936 · Alan Turing · father of modern computing · progress bars · "2 minutes" · "17 minutes" ·
"4 minutes"`). **Noema = 0 before 0:26** and is the counter-example.
*Why:* this makes §2's information-first rule countable — the difference between a first frame that
carries information and one that carries mood.

**4. FORBIDDEN PHRASES = 0.** Grep for the §2 DELETE FOREVER register: *welcome back · today we're
going to · in this video · on this channel · before we dive in*, the bio opener, and cross-references
to other videos.
**The one documented exception:** *Agent Harness* opened with *"This is part two of our three-part
series"* **and** *"Before we dive into how it works"* — and pulled 16,561 impressions. For a
**reference/implementation** video the viewer wants the agenda; they are confirming they are in the
right place before committing 20 minutes. **For an investigation these stay forbidden.** The checker
flags them and allows an explicit override with a stated reason.

**5. RUNTIME 15–25 MIN.** Probe winners in this lane: 46.2 · 41.4 · 37.6 · 29.9 · 27.4 · 23.8 · 21.4
· 16.3 · 15.0 min. Our *Agent Harness* 19:26. **This is NOT the 8:12-wins finding** — that came from
the essay lane (Mackard / Universal Resilience / Fractal) and does not transfer. 15–25 is a
deliberately conservative band inside the proven range while the craft floor is new.

**6. ONE LOOP NAMED EARLY AND CARRIED.** A *loop* is a phrasing that names a question without
answering it (`teardown.py:LOOP` — *why · how · what if · what happens · who decides · nobody knows ·
the question · the catch · the twist · which raises · no one can*).
**Carried vs spent is the whole point.** A loop answered within 30s is **spent** — the tension is
cashed immediately. **Carried** = named, then left open until the payoff.
Measured: Universal Resilience **[0:19]** *"But any algorithm, no matter how powerful"* — carried into
the body. **Ours: 0.4 loops/min and every one answered on the spot. Zero carried.**
**The metric is NOT density.** One carried loop beats eight spent ones; a high density of answered
questions is *worse* than a single held one.

**7. AUTHORED REVERSAL AT 40–55%.** A moment where the argument turns against itself. Two working
shapes:
- *Concede then escalate* — Universal Resilience **[9:37] = 42%**: "this doesn't mean we can never
  verify an AI's correctness… just not in all scenarios" → into Rice's Theorem and intractability.
- *Escalate the stake* — Mackard **[4:12] = 51%**: "But the most damaging effect isn't the code.
  **It's the people.**" Technical complaint → the junior death spiral.
**Ours: none** — the 40–55% window is the middle of an eight-step procedure.
*Why:* it is what makes minute 12 feel different from minute 4. Its absence is the most likely
single cause of the 0.87 watch-hours/video collapse.
*Why that window:* §1 specified it, and both winners landed inside it independently (42%, 51%).

**8. PERSISTENT ON-SCREEN SPINE.** A visual element that persists and shows progress: Universal
Resilience's **escalating-limits ladder** (each rung "and it's worse than that"), Mackard's 8 chapters
at ~60s, video 1's planned funnel `11B tokens → 473 sessions → 47 sessions → 1 decision`. §1 names it
as *the* retention device above 8 minutes.
**Not text-detectable** — it lives in the render. The checker reports it as MANUAL. Per the
2026-07-26 note, gate and human each catch what the other misses; this is the human's.

### 3.2 The persistent spine — the one item only your eyes can check

`prepublish-check.py` reports this MANUAL and always will: it lives in the render, not the words.
So it needs a real spec, not one line.

#### What a spine is

**A visual element that persists across the whole video and does two jobs at once:**
1. **Position** — where are we, how much is left.
2. **Anticipation** — the unrevealed parts are *visible* but not yet readable.

Job 2 is the one people skip, and it is the one that holds. A progress bar reading "3 of 8" does
job 1 only; it is decoration. `CONDUIT-VISUAL-SYSTEM.md`'s **ghosted-placeholder** device does both,
and we already own the component.

#### The evidenced distinction: a spine that REVEALS beats one that ANNOUNCES

| Video | Spine | Score |
|---|---|---|
| **Universal Resilience** | 8 chapters, each a **new and worse limit**, revealed as it goes — *"Even That Hack Has a Hidden Limit"* | **69.61×** |
| **Fractal Philosophy** | announces at [0:25] *"a framework of **three different things**"* — the whole structure, up front | **6.06×** |
| Mackard | 8 chapters ≈60s each, **narrowing** general claim → juniors → salaries | 73.03× |
| **Ours (Agent Harness)** | **no chapters declared, no spine at all** | **8.00×** |

*Caveat: n=2 on the reveal-vs-announce comparison, confounded by topic, runtime and channel size.
Treat as a strong steer, not proof.*

**The rule this implies is just §3's curiosity gap applied to structure: the spine should show how
much is LEFT without revealing WHAT is left.** Ghosted slots, not a table of contents.

#### Four properties a spine must have

1. **MONOTONIC** — each step moves one dimension the viewer cares about, always the same direction:
   worse · bigger · narrower · closer · fewer suspects left. Universal Resilience's every rung is
   *"and it's worse than that."* An unordered list of topics is not a spine.
2. **GHOSTED, NOT LISTED** — unrevealed slots visible, contents not readable. Per
   `CONDUIT-VISUAL-SYSTEM.md`, content must resolve within **~1.2s** of a panel appearing or it reads
   as a dead frame.
3. **UPDATES AT EVERY BEAT** — if it changes four times in twenty minutes it is a static graphic.
   Each update is also a change-event feeding the 45–60/min density target.
4. **RESOLVES AT THE VERDICT** — the last state *is* the answer. If the spine is still ambiguous at
   the end, it was ornament.

#### Four checks you can actually run on the render

- **The screenshot test.** Grab frames at 25%, 50% and 75%. **Can you tell which is which from the
  spine alone?** If not, it isn't carrying position.
- **The 90-second test.** Is the spine on screen inside the first 90 seconds? Introduced at minute
  eight, it is a chapter card, not a spine.
- **The update count.** Count spine state-changes; it should be within ±2 of your beat count.
  Fewer means static.
- **The mute test.** With sound off, can a stranger tell the argument is *going somewhere*? That is
  the whole function.

#### Spine types, ranked by fit for the build register

1. **ELIMINATION LIST** *(best fit — use this)* — named suspects, ghosted, struck through one at a
   time. Monotonic (fewer remain), reveals rather than announces, updates every beat, resolves on the
   survivor.
2. **ESCALATING LADDER** — Universal Resilience's shape. Each rung worse than the last. Best when the
   payoff is cumulative dread rather than a single answer.
3. **NARROWING FUNNEL** — Mackard's shape. Good for scope, **but it usually has too few states** (see
   the video-1 correction below).
4. **COMPONENT CHECKLIST** — parts of a system ticked off as explained. Weakest: it tells position
   but creates little anticipation, because the viewer can guess what's coming.
5. **SECTION BADGE ALONE** — not a spine. Do not count it as one.

#### ⚠️ Correction to the video-1 plan

`VIDEO-PLAN-claude-code-usage.md` proposes the funnel `11B tokens → 473 sessions → 47 sessions →
1 decision`. Measured against property 3 that is **four states across ~20 minutes — one change every
five minutes.** That is a static graphic, not a spine.

**Replace it with an ELIMINATION LIST**, which the plan's own beat map already implies:

```
   WHAT IS BURNING THE LIMIT?
   ▸ the model            ███ ruled out  (opus 96% — but sonnet sessions cost the same shape)
   ▸ output tokens        ███ ruled out  (0.4% of tokens)
   ▸ inefficiency         ███ ruled out  (13.7–31.8× cache ratio, ABOVE average)
   ▸ ▓▓▓▓▓▓▓▓▓▓           ghosted
   ▸ ▓▓▓▓▓▓▓▓▓▓           ghosted
```

Monotonic, ghosted, updates at every beat, and the last surviving row *is* the verdict — session
length, which you cannot prompt your way out of. Keep the funnel as a **one-shot graphic** in the
cold open; it is a good hook and a bad spine.

**Cadence flexes; the floor does not.** Nine videos in ten weeks that all clear the floor beats ten
where three are filler. A video that isn't ready slips a week.

## 4. Evaluation — pre-registered so it can't be rationalised later

**Judge the trailing set, not individual videos.** At 147 subs the per-video variance is enormous
(16,561 impressions vs a ~500 typical). Single videos prove nothing either way.

Baselines: **Feb 2026 = 2,862 impressions/video · 12.4 watch-h/video · 5.3 subs/video.**
**Jul 2026 = 368 · 0.87 · 0.14.**

| Metric | Primary? | Target by video 10 |
|---|---|---|
| **Watch-hours per video** | ⭐ **PRIMARY** | **≥5.0 h** (from 0.87) |
| Impressions per video | secondary | ≥1,500 (from 368) |
| Subscribers per video | secondary | ≥2.0 (from 0.14) |
| CTR | guardrail only | ≥4% (already at 3.69%) |

**Watch-hours per video is the primary metric** because it is the measured constraint: impressions/
video fell 7.8× while CTR stayed healthy, and watch-time/video fell 14×. CTR is not the problem and
must not be optimised for.

**Checkpoint at video 5** — trend only, not a decision point. Purpose: catch a craft-floor failure
early, not to abandon the register.

### FALSIFIER — and what it does NOT mean

**Trigger:** at video 10, watch-hours/video still **under 2.0** AND impressions/video **under 800**.

**⚠️ THIS IS NOT A TRAPDOOR BACK TO CHANGING THE CHANNEL.** Its purpose is the opposite. Without a
threshold committed in advance, every disappointing video becomes an argument for a new direction —
which is exactly what happened on 2026-07-31, when four separate strategies were proposed in one day
because each measurement disappointed. **A pre-registered exit is what buys the ten weeks.** Until
video 10, nothing changes regardless of how any individual video performs.

**Note where the bar sits.** July's *failing* conduit essays did 0.87 h and 368 impressions.
February did 12.4 h and 2,862. Triggering this means ten craft-floored build videos performed barely
better than the essays that already failed. That would be genuinely surprising. **It is a smoke
alarm, not a schedule.**

**If it does trigger, investigate IN THIS ORDER. The register is the LAST suspect, not the first:**

1. **Was the craft floor actually met?** Measurable from the artifacts, not from memory — run
   `teardown.py` on our own ten videos and check reversal placement, negation/min, loop density,
   wpm against §3. **This is the most likely cause by a wide margin.** Fix: execution, not strategy.
2. **Was subject selection wrong within the register?** Ten niche subjects nobody was searching for
   would produce this result with perfect craft. Fix: selection, same register, same channel.
3. **Only then, the register itself** — and note this is contradicted by evidence already in hand:
   Feb–Apr 2026 proved this register works *on this channel* (42,890 impressions, 68 subscribers,
   three videos producing 65 of 109 subs). That is measured, not hypothesised. **The prior against
   "the register is wrong" is strong.**

**What is forbidden either way: iterating on wording.** Rewriting titles and re-probing phrasings
in response to disappointing numbers is the documented 2026-07-31 failure mode and produced four
wrong conclusions in a day.

## 5. Multi-platform repurposing

Supported. One caution, precisely scoped:

- **YouTube Shorts specifically failed here** — 73 shorts → 4 subscribers → 8 watch-hours → 90.7%
  from the Shorts feed, which does not transfer to long-form. **Do not make YouTube Shorts.**
- **Other platforms are a different question and are NOT condemned by that data.** LinkedIn, X,
  newsletter, written post — untested here, and the marginal cost of repurposing one week's research
  is low. Go ahead.
- Keep the repurposing downstream of the video, never upstream. The video's craft floor is not
  negotiable against the needs of another platform.

## 6. What does NOT change

**The entire production system survives.** Conduit visual system, cream citation cards, word-synced
highlights, HyperFrames pipeline, scene validator, dead-space gate, asset library — none of it is
subject-specific. Citation cards work on a token table, a config file, a terminal session, a `usage`
JSON block. The token-economics plan uses existing components with zero new build.

**What changes is what the camera points at, not how it shoots.**

## 7. What is parked, not killed

The conduit-essay subjects (Pope, Messi, data centers, job displacement) are **parked**. Nothing is
deleted, so the option survives.

The re-entry path, if it comes: earn an audience with the register that travels, then test whether
the essays land with people who already trust the channel — the sequence Species used (early topical
content, breakout later on a durable format). **This is a hypothesis, not a measurement.** It is not
a reason to hedge now.

## 8. Immediate queue

Probed and ranked in `TEN-TITLES-PROBE-2026-08-01.md`:

1. **Claude Code token economics** — plan complete in `VIDEO-PLAN-token-economics.md`. Data measured:
   11.0 B tokens, $28,173 API-equivalent, top 10% of sessions = 96.2% of cost.
2. The eight-month agent (max 16.70× family)
3. Memory systems compared (drift 0)
4. MCP context overload (7.88× precedent on 1,960 subs)
5. Skills that never fire — reframe as a **disambiguation verdict** (7.08× on 1,160 subs), not a survey

**Rejected, do not build:** vector-search debug story (`why rag doesn't work` THIN 0.19×), YouTube
self-audit (drift false positive — the lane is channel-cloning hustle content).

## 9. Housekeeping (cheap, reversible, do once)

Reorganise the channel page so build content is the front door — featured playlist and section
order, so a viewer arriving from *Agent Harness* sees more of the same. ~1 hour.

## 10. Known risk

Weekly production of a 15–25 min video with real research, real data, custom visuals and the QC
gates is demanding. **The risk is not the cadence — it is the craft floor slipping to meet it.**
That is exactly what §3 and §4's primary metric are designed to catch. Terry's call, made with the
tradeoff stated.
