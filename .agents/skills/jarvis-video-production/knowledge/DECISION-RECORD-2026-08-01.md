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

| Device | Agent Harness | **Floor** |
|---|---|---|
| Authored reversal at 40–55% | ✖ | ✅ required |
| Negation density | 1.3/min | **≥3.0/min** |
| One loop named early and carried | ✖ | ✅ required |
| wpm | 125 | 135–150 |
| Concrete data points in first 45s | — | **≥8** |
| Persistent on-screen spine | ✖ | ✅ required |

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
