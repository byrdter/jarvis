# Roadmap — running the Fireship playbook on Byrddynasty

**Written 2026-08-22**, at Terry's request, from the measured Fireship teardown
(`FIRESHIP-CHANNEL-TEARDOWN.md`), the Snap Shift and WSM teardowns, and a direct measurement of
`_cozRrck3lE` ("Your AI Subscription Costs 14X What You Pay For It", 10:28, **10 views**).

Channel state: **96 videos · 150 subs · top video 1,100 views.**

---

## 0. Conceding the point that started this

Terry's push-back was right and is adopted here: *"the number of viewers is going down versus
subscribers but so what — he's still getting a ton of views and adding subscribers."* Correct. Per-sub
decline at 4.25M subs is arithmetic, not failure; nobody sustains high views/subs at that scale. I
over-weighted it. **The efficiency framing is dropped. What follows treats Fireship as a working model
to copy, not a cautionary tale.**

---

## 1. The honest diagnosis — what is actually blocking this channel

**It is not craft.** The 11B video's cold open is genuinely good and follows our own §2:

> *"Over eight months, this subscription cost $1,000. Over those same eight months, it consumed
> $13,753 of compute. That isn't an estimate. It is Anthropic's own published price list applied to a
> count of every token that moved through one machine. 11,346,275,422 of them…"*

Concrete from frame one, real numbers, verifiable, self-relevant. That open would not embarrass any
channel in the corpus.

**It is discoverability.** 96 videos have produced ~6,000 lifetime views. The single measurable,
fixable cause: **the titles do not contain the words people type.** That is exactly the half of
Fireship we identified as the acquisition engine (§4d.4) — and it is the half Byrddynasty is not
running.

### 1.1 The evidence — this video sits on a live query cluster and names none of it

vidIQ keyword research, run 2026-08-22:

| query | est. monthly searches | competition | score |
|---|---:|---:|---:|
| **claude usage limits** | **44,751** | 34 | **68.1** |
| claude code cost | 8,886 | 43 | 58.0 |
| claude pro plan | 8,644 | 31 | 62.7 |
| claude ai plans | 6,529 | 38 | 58.8 |
| **claude code pricing** | 5,017 | **26.5** ← lowest | **62.5** |
| claude max plan | 4,294 | 34 | 58.9 |
| claude code plans | 4,129 | 34 | 58.9 |
| *(context)* claude code | 3,381,694 | 68 | 71.3 |
| *(context)* claude code tutorial | 687,903 | 54 | 70.7 |

**~80,000 monthly searches across the pricing/limits cluster, at competition 26–43 — low.** The 11B
video answers every one of those questions with better evidence than anything currently ranking.

**Its title contains none of those words.** No "Claude", no "Claude Code", no "cost", no "pricing", no
"limits". *"Your AI Subscription Costs 14X What You Pay For It"* is a browse headline for an audience
that isn't being served one, on a channel with no browse distribution to serve it with.

> **This is the single highest-leverage fix available and it costs nothing.**

---

## 2. The two-engine model — pick the right one for 150 subs

From `FIRESHIP-CHANNEL-TEARDOWN.md` §4d.3:

| engine | what it is | what it does | Fireship era |
|---|---|---|---|
| **ACQUISITION** | evergreen, search-addressable explainers on terms people already query | recruits strangers **continuously, forever** | 2019–2022 (teaching 61%→34%) — built 4.25M subs |
| **HARVEST** | topical news/commentary with browse hooks | retains an existing base; recruits poorly | 2023– (news 29%) — five flat years at ~950K/video |

**At 150 subs there is no base to harvest.** Byrddynasty's current output is mostly harvest-shaped
(inside-baseball topical essays about *our* system — "Orchestrating AI Swarms", "Claude Subagents vs.
Claude Agent Teams") aimed at an audience that doesn't exist yet.

**Run acquisition almost exclusively until roughly 5–10K subs.** Then add harvest.

### 2.1 What "search-addressable" means concretely here

Fireship's *"Python in 100 Seconds"* ranks because millions type "python". The equivalent moves for
this channel are the queries above, plus the tutorial/beginner cluster (687K + 123K/mo).

Reframe existing catalog ideas as answers to queries:

| current framing (essay) | search framing (answer) |
|---|---|
| Your AI Subscription Costs 14X What You Pay For It | **Claude Code Pricing: What $200/Month Actually Buys You** |
| Why Your AI Agent Wastes 95% of Its Context | **Claude Code Context Limits — Why You Hit Them So Fast** |
| Claude Subagents vs. Claude Agent Teams | **Claude Subagents vs Agent Teams (2026)** ← already close |
| Orchestrating AI Swarms That Actually Work | *(no query — hold for the harvest phase)* |

---

## 3. Titles — the measured mechanics

Three independent teardowns produced three title findings. They compose.

1. **TWO CLAUSES: fact — withheld consequence.** Snap Shift, **3.86× median views**, p<0.0001, 64% vs
   16% clearing 100K. The gradient: clause 2 that *withholds* (177K) > *completes* (98K) > none (43K).
2. **NAMED ACTOR + adverse present-tense verb** (the accusation frame). WSM, **1.69×**, p<0.0001 —
   raises the floor, not the ceiling.
3. **Trailing ellipsis topical headline.** Fireship house style, 1% → **91%** of output, 1.11×,
   p=0.037.

**The current title fails 1 and 2 and spends the payoff.** *"Your AI Subscription Costs 14X What You
Pay For It"* — single clause, no named actor, and **"14X" is the answer**, given away. Our own §3 rule
is *reveal facts, withhold meaning*; 14× is the meaning.

Fireship's own Anthropic titles, for calibration — *"Tragic mistake... Anthropic leaks Claude's source
code"* (3.2M), *"Did Anthropic just kill the indie hacker...?"*, *"Anthropic is starting to panic…"*,
*"Anthropic begged the world to stop AI… then shipped this"*. Every one: **named actor + adverse verb
+ ellipsis + withheld verdict.**

### 3.1 A dual-title system — because the two engines want opposite titles

This is the key structural insight and it resolves an apparent conflict.

- **Search titles** want the query **at the front**, plainly, with the answer implied. Fireship's
  *Python in 100 Seconds* has **no hook at all** and 3.0M views (§4.3) — a gap would be friction when
  the viewer already typed the question.
- **Browse titles** want the two-clause withheld-consequence structure.

**Do not mix them.** Decide per video which engine it serves, then title for that engine.

For `_cozRrck3lE`, which should be an **acquisition** video:

> **`Claude Code Pricing: I Counted 11 Billion Tokens to See What $200 Really Buys`**

Query at the front (`claude code pricing`, competition 26.5), concrete proof in the back, answer
withheld. If a browse variant is wanted later for a *different* video on the same material:

> **`We counted every token in one Claude subscription... the math doesn't work`**

---

## 4. VO and pace — the measured gap

Direct comparison, same method as `FIRESHIP-CHANNEL-TEARDOWN.md` §4d.1:

| | wpm | **numbers/min** | *you/your*/min | **turns/min** |
|---|---:|---:|---:|---:|
| **Byrd — 11B Tokens** | **159** | **7.4** | 3.0 | **2.2** |
| Fireship — DeepSeek (3.8M) | **237** | 3.1 | 2.8 | **3.9** |
| Fireship — Roadmap (8.3M) | 211 | 0.8 | 4.2 | 3.5 |
| Snap Shift — BYD (512K) | 144 | 3.5 | 1.5 | 1.1 |

**Three findings, one of them counter-intuitive:**

1. **Direct address is already right.** 3.0 vs Fireship's 2.8 — no change needed. This is the one
   dimension already at target; don't break it.
2. **There are 2.4× TOO MANY numbers.** 7.4/min vs Fireship's 3.1. This is the surprise, and it is
   compounded by speed: numbers are *expensive in time*. Our own `CLAUDE.md` records that
   `11,346,275,422` is **6.2 seconds of speech** and that a word-count estimate ran 82 seconds long
   for exactly this reason. At 159 wpm with a number every 8 seconds, a large share of runtime is
   *reciting digits*. **Target ~3–4 numbers/min.** Keep the three that carry the argument
   ($1,000 / $13,753 / 11.3 billion); put the rest **on screen only**, never in the VO.
3. **Too few rhetorical turns.** 2.2 vs 3.9/min. Fireship reverses roughly every 15 seconds —
   *but / actually / turns out / which means*. The argument keeps pivoting instead of accumulating.
   **Target ~3.5/min.** This is a rewrite of connective tissue, not of content.

**Speed follows from 2 and 3.** Cutting spoken numbers and adding turns will lift wpm toward ~200
without talking faster. Do not simply speed up the read — that reads as rushed rather than dense.

---

## 5. Runtime — and the conflict Terry has to resolve

Measured facts, not preferences:

- **Runtime does not predict views within era** on Fireship's catalog: pooled 1.79×, within-era
  **0.91×**, age-residualised **p=0.20 (null)**. Length is not the deterrent — their biggest video is
  16:42 at 8.3M.
- Fireship's median is **~5 min**, and **94% of its current output cannot carry a mid-roll** (§4b).
- Byrddynasty's median is **~14 min**, driven by our own **8:00 monetisation floor**.

**The conflict:** at 150 subs, AdSense revenue is effectively zero regardless of runtime. The 8:00
floor is currently costing production time to protect income that does not yet exist — while the
acquisition engine wants short, tight, query-answering videos.

**This is Terry's call and the data does not make it for him.** Two coherent options:

- **(a) Suspend the floor during the acquisition phase.** Ship 5–7 minute query-answering videos,
  reinstate 8:00 once there is a base worth monetising. Maximises acquisition speed.
- **(b) Keep the floor.** Then the 11B video at 10:28 is already compliant, and the fix is purely
  §3 (title) + §4 (pace) — a smaller change with a slower ramp.

**I recommend (a), and note (b) still works.** Recorded per §7 of the standard: the floor is a
*business* constraint, and the business it protects has not started yet.

---

## 6. The specific play for `_cozRrck3lE`

**Do not just re-title and hope.** A published video's browse impression test already ran and won't
re-run. But **search ranking is not gated the same way** — a video that starts matching a query can
accrue traffic months later. So:

1. **Re-title for the query.** `Claude Code Pricing: I Counted 11 Billion Tokens to See What $200
   Really Buys`.
2. **Rewrite the description's first two lines** to carry the query terms verbatim — *claude code
   pricing, claude code cost, claude max plan, claude usage limits*. The current description is
   excellent prose but leads with narrative, not query terms.
3. **Thumbnail**: the number, huge, and the two dollar figures. Our own
   `feedback_finding_type_is_large` applies — finding rows ≥60px.
4. **Then make 2–3 more for the same cluster** — these are the acquisition engine, not one-offs:
   - `Claude Usage Limits: Why You Hit Them So Fast` (44.7K/mo, competition 34)
   - `Claude Code Pricing: Max vs Pro vs API in 2026` (5.0K/mo, competition 26.5)
   - `Is Claude Code Worth $200 a Month?` (direct purchase-intent query)

   A cluster ranks better than a single video; they cross-recommend.

**Expectation setting, honestly:** this will not produce Fireship numbers. It should produce *hundreds
to low thousands* of views per video accumulating over months rather than 10 in a burst, and it
compounds — search traffic does not decay the way browse traffic does. **The mechanism is replicable;
the scale took Fireship three years of it.**

---

## 7. Cadence and portfolio

Fireship ships **~8/month**. Byrddynasty has 96 videos over roughly 18 months ≈ **5/month** — the
cadence is not the problem, the *targeting* is.

Suggested split during the acquisition phase:

| share | type | purpose |
|---|---|---|
| **70%** | search-addressable evergreen (query in title) | recruit strangers |
| 20% | topical AI-industry commentary (ellipsis/browse titles) | stay current, catch occasional breakouts |
| 10% | experiments | find the next format |

Then invert toward harvest once a base exists.

---

## 8. What to measure — and the gap in our own tooling

The Fireship teardown surfaced a capability we lack: **nothing tracks the decay of a format we own.**
`outlier-ratchet.py` watches other channels. Fireship's whole advantage was noticing their signature
format slid 1.34× → 0.52× and killing it (§3.1); Snap Shift's failure was drifting off its best lever
without noticing (§2.5).

**Build a self-format tracker.** For each of our recurring formats, per month: n, median views,
median views/day, ratio vs channel median. Alert when a format's ratio drops below 1.0 for two
consecutive months. That is a small script and it is the difference between the two channels.

Track per video: **query term in title (y/n) · search impressions share · numbers/min · turns/min ·
wpm.** The first is the acquisition-engine gate; the last three are the §4 craft targets.

---

## 9. Honest limits of this roadmap

1. **150 subs means very little algorithmic testing**, regardless of packaging. Search is the way
   around that, which is why §2 leads — but nothing here makes a video go viral from a standing start.
2. **Keyword volumes are vidIQ estimates**, not YouTube ground truth. The *cluster* is clearly real
   and low-competition; treat individual figures as directional.
3. **Fireship's scale is partly first-mover.** It occupied "fast dev explainer" before that slot was
   contested. The mechanics replicate; the timing does not.
4. **This roadmap addresses the CLICK.** Every teardown in this corpus measures what got clicked, not
   what held. Retention remains unmeasurable from outside and is where Byrddynasty was independently
   diagnosed as gated (`video-production-standard.md` §0). Packaging fixes get people in the door;
   they do not fix the first thirty seconds.
