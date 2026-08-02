# Byrddynasty channel audit — first-party Studio export, 2026-08-01

**THIS IS THE AUTHORITATIVE DOC.** It supersedes the channel-strategy conclusions in
`BEAT-A-CHANNEL.md`, `TITLE-TEST-PLAN.md`, `EVIDENCE-STATE-2026-07-31.md` and the cross-channel
comparison in `KEYADVANCES-CHANNEL-AUDIT.md`. Source: Studio Advanced-mode CSV export, lifetime
(2025-11-30 → 2026-07-31), 168 rows.

---

## 0. The correction that forced this rewrite

`video-production-standard.md` §0 records "traffic was effectively 0% Browse / Search / External —
no algorithmic distribution." **That is not true of the channel as a whole.** Measured:

| | **Byrddynasty** | KeyAdvances |
|---|---|---|
| Impressions | **93,735** | 22,750 |
| CTR | **3.69%** | 2.30% |
| Views | 10,111 | 1,296 |
| Watch time | **286.9 h** | 40.4 h |
| Subscribers | 147 | 14 |

Byrddynasty earns **4× the impressions at a 60% better click-through rate.** Every strategic
conclusion drawn on 2026-07-31 from the §0 figure — including "KeyAdvances is the channel YouTube
is willing to distribute" — was wrong. This is the §6 rule biting: the ~0% number was read out of a
document and never checked against the artifact.

## 1. Long-form vs Shorts

| | Views | Impressions | Subs | Watch time |
|---|---|---|---|---|
| Long-form (95) | 5,798 | 85,833 | **109** | **278 h** |
| Shorts (73) | 4,091 | 7,646 | **4** | **8 h** |

**Shorts are 41% of views and 1.4% of value.** 73 shorts produced 4 subscribers and 8 watch-hours.
Stop making them, or make them only as trailers for a long-form that exists.

## 2. The timeline — long-form only

| Month | Videos | Impressions | **Impr/video** | Median CTR | Subs | Watch h |
|---|---|---|---|---|---|---|
| 2025-12 | 14 | 3,966 | 283 | 4.21% | 8 | 18.1 |
| 2026-01 | 13 | 5,484 | 422 | 2.88% | 3 | 13.1 |
| **2026-02** | 7 | **20,036** | **2,862** | 2.87% | **37** | **86.5** |
| **2026-03** | 22 | **22,854** | 1,039 | 2.63% | **31** | **86.6** |
| 2026-04 | 7 | 13,527 | 1,932 | 3.94% | 9 | 34.8 |
| 2026-05 | 3 | 5,099 | 1,700 | 3.38% | 16 | 10.9 |
| 2026-06 | 7 | 6,777 | 968 | 2.20% | 2 | 9.2 |
| 2026-07 | 22 | 8,090 | **368** | **3.70%** | 3 | 19.2 |

**CTR IS NOT THE PROBLEM.** July's median CTR of 3.70% is the second-best month on record. The
packaging works.

**IMPRESSIONS PER VIDEO COLLAPSED 7.8×** — 2,862 in February to 368 in July. YouTube stopped
spending impressions on the channel.

**WATCH TIME PER VIDEO COLLAPSED 14×** — 12.4 h/video in February to 0.87 h in July. That is almost
certainly the cause of the impressions collapse, not a coincidence beside it.

## 3. Where the channel's entire value came from

| Subs | Impressions | CTR | Watch | Video |
|---|---|---|---|---|
| **33** | 16,561 | 4.4% | **65.8 h** | Inside Anthropic's Agent Harness: 200+ Features Built Autonomously |
| **19** | 9,970 | 5.4% | **31.7 h** | Building JARVIS: A True Second Brain with Claude Code |
| **13** | 3,918 | 3.1% | 6.9 h | My Second Brain Learns From YouTube Every Day |

**3 videos → 65 of 109 long-form subscribers. 2 videos → 97 of 278 watch-hours (35%).**

Highest CTR at ≥500 impressions — **11 of the top 12 are agent-engineering / build content**:
9.5% *Run Your Applications For Hours Autonomously* · 7.4% *6 Agent Frameworks Compared* ·
6.4% *Command Center for a Second Brain* · 5.4% *Building JARVIS* · 5.2% *Vector Search & Gmail* ·
4.9% *Full Terminal Access To My AI* · 4.7% *Why AI Agents Fail After 2 Hours* · 4.4% *Agent
Harness* · 4.3% *OpenClaw Security Alert* · 4.0% *The Secret to Autonomous AI*.
The single exception: **5.5% *AI Doesn't Hallucinate*** — the one conduit-era video in the set.

## 4. "Technical" is NOT the winning variable — this is the key distinction

The **most technical era was the worst era.** Dec 2025 – Jan 2026, 27 tutorials, **max 798
impressions**, ~350/video, 4 subscribers total across all of them:

> Building Your First Production Backend with AI (Step by Step) — 362 impr · The API Layer Pattern:
> Clean Data Fetching — 276 · Why Frontend Architecture Must Mirror the Backend — 317 · Testing
> AI-Written React Components with Vitest — 633 · Frontend-First AI Workflows — 253 · How
> Professionals Build Full-Stack Features — 188 · Your App Is Lying to Users — 217

**What died:** generic instructional how-to. No named subject, no number, no verdict, no stake.

**What won:** a **named real system + a number + a verdict or a reveal**, usually something Terry
actually built or actually examined.

> *Inside **Anthropic's Agent Harness**: **200+** Features Built Autonomously*
> *Building **JARVIS**: A True Second Brain with **Claude Code***
> *Why AI Agents Fail After **2 Hours** (And How Harnesses **Fix It**)*
> *Which AI Agent Framework Should You Use? **6** Frameworks **Compared***
> *Run Your Applications For Hours Autonomously: **5** Universal Patterns*
> *Why Your AI Agent Wastes **95%** of Its Context*

**This is the same formula every other data source produced today**, which is why it should be
trusted:
- KeyAdvances' best (3.5% CTR, 3 subs): *We Tested **Anthropic's Opus 4.6** Claims — Here's What's
  **Actually True***
- KeyAdvances' highest CTR (7.7%, 4 subs): ***Apple** Just Spent **$110 Billion** — **Genius Move or
  Corporate Blunder?***
- Demand probes: verdict-led PROVEN (4.4–16.2× medians), mechanism-led DEAD (0.00–0.19×)
- Mackard teardown (73.03×): named prophecy + receipts, 8 data points in 44 seconds

Four independent sources, one formula.

## 5. The conduit-essay verdict — honest version

The July conduit essays are **not** failing on packaging. Median CTR 3.70%; *AI Doesn't Hallucinate*
hit 5.5% on 1,357 impressions. They fail on **watch time**: 22 videos → 19.2 hours → 3 subscribers.

That is a large enough sample to act on. But state the failure precisely: **the format holds
attention badly, not that the subjects are wrong.** A conduit essay with a real spine and a reversal
is untested — every one built so far lacks both.

> ### ⚠️ CORRECTED 2026-08-02 — the last sentence is wrong for *AI Doesn't Hallucinate*
>
> Measured from that master's own word-level transcript (`tools/narrative-measure.py`), it **has an
> authored reversal at 7:19 = 47.0% of runtime** — inside the §1 window — and scores **4.2
> negations/min and 1.03 loop-openers/min**, beating the 73.03× Mackard outlier on both. The devices
> were present. It still didn't hold.
>
> What it actually did: **stated its own verdict at 0:51 (5.6% of runtime)** and **named its spine
> ("we're putting one word on trial") once at 1:21, then went silent on it for 539 seconds — 58% of
> the runtime.** Full teardown and the model derived from it:
> **`NARRATIVE-STRUCTURE.md`**. Do not repeat "conduit essays lack a reversal" — that claim was
> asserted from the beat maps, not measured from the master, and this is §6.1 biting again.

## 6. Revised plan

1. **Return to the Feb–April register** — named real system + number + verdict, built on work
   actually done. Not tutorials.
2. **Kill the title test** (`TITLE-TEST-PLAN.md`). CTR is 3.69% channel-wide and 4.4–9.5% on winners.
   It is aimed at a problem this channel does not have.
3. **Fix the body.** The constraint is watch time per video. Apply the two surviving teardowns:
   authored reversal at 40–55% (`WfjGZCuxl-U` at 51%, `u_5erLilDXY` at 42%), an escalating spine,
   a stake that compounds.
4. **Stop the shorts** — 73 of them bought 4 subscribers.
5. **Slow the cadence.** 170 uploads in 8 months is one every 1.4 days; Anastasi runs 12-day gaps and
   Species 23. February produced 7 videos and 37 subscribers; July produced 22 and 3.
6. **Judge on watch-hours per video, not views.** February ran 12.4 h/video. That is the number to
   restore.

## 7. Why February spiked — ANSWERED by the teardown (`teardowns/Tlqe0A8ED8o.md`)

*Agent Harness* won on **demand capture, not retention craft.** Measured against the other four
teardowns it scores **last on every retention device**:

| Video | Outlier | wpm | Loops/min | Negation/min | Reversal |
|---|---|---|---|---|---|
| Mackard | 73.03× | 151 | 0.6 | **4.0** | ✅ 51% |
| Universal Resilience | 69.61× | 136 | 1.1 | 3.1 | ✅ 42% |
| **Agent Harness (ours)** | **8.00×** | **125** | **0.4** | **1.3** | **✖ none** |

No open loop, no reversal, a third the negation density, the slowest pacing measured. By §3 it
should have failed. It didn't, because:

1. **The title is the engine** — `Inside Anthropic's Agent Harness: 200+ Features Built
   Autonomously`. Named company + named system + number + astonishing claim → 4.44% CTR on 16,561
   impressions.
2. **The subject was searched-for and unanswered.** Anthropic had just open-sourced the harness;
   everyone was studying it; nobody had explained it end-to-end.
3. **The payoff was implementable** — two-agent architecture, four artifacts, eight-step loop, named
   pitfalls. 3.36 min/view against 1.81 for *Building JARVIS* and 1.87 for the July conduit videos.

**So 8.00× is a FLOOR, not a ceiling.** Our best video has none of the devices that carry the 69–82×
videos. **Keep the title engine and the implementable payoff; add the body devices it lacks** —
an authored reversal at 40–55%, negation density ≥3/min, one loop named early and carried.

It also **broke §2 twice and survived** (opens with "part two of our three-part series" and "before
we dive into how it works"). For a *reference/implementation* video the viewer wants the agenda
stated. §2's rules are calibrated for narrative essays; do not apply them unmodified to this
register — and do not generalise the exemption back the other way.

## 8. What is still NOT settled

- Whether the conduit-essay format can be rescued by a spine + reversal, or should be dropped. It
  has 22 attempts and no breakout, but it has never been built with either device.
- Whether demand capture is repeatable on purpose. *Agent Harness* caught a live, unanswered
  question. That is a **selection** skill, not a craft skill, and we have no process for spotting
  the next one. The ratchet/probe apparatus is aimed at topic lanes, not at "what did a major lab
  just ship that nobody has explained yet."
