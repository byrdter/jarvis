# VIDEO PLAN — "11 Billion Tokens" (build register, video #4)

Probe basis: `claude code cost too much` — **PROVEN**, n=21, drift 3, median **1.24×**, max 14.11×,
**10 hits**, every winner a channel under 30k subs. See `TEN-TITLES-PROBE-2026-08-01.md`.
Craft basis: `teardowns/Tlqe0A8ED8o.md` (our 8.00×) + `WfjGZCuxl-U.md` (73.03×) + `u_5erLilDXY.md` (69.61×).

---

## 0. The subscription problem, and why it makes the video BETTER

Terry is on a flat subscription — there is no dollar bill. That is not a weakness, because
**three of the four proven rows are about LIMITS, not dollars**:

- 14.11× · *How to Optimize Token Usage in Claude Code* (5,450 subs)
- 10.90× · *How to Optimize Token Usage in Claude Code* (5,500 subs)
- 10.50× · *Stop Hitting Claude Code Rate Limits! (3 pro tips)* (1,180 subs)
- 8.33× · *I Stopped Hitting Claude Code Usage Limits (Here's How)* (15,800 subs)

**The audience is subscription users hitting caps.** We are exactly them. The $ figure is the
attention-getter; the limit is the utility.

## 1. The data — FROZEN 2026-08-02 on Terry's C1+C4 capture, all first-party

Source: `~/.claude/projects/**/*.jsonl`, 509 files scanned / 490 with usage records, 33,313 assistant
messages. **Authoritative copy: `01-script/claim-source-map.md`.** Do not edit figures here without
editing there.

> ⚠️ **A prior version of this table was wrong by ~2.1×.** `usage-cost.py` carried Opus at $15/$75 —
> Opus 4.1/4 pricing, a generation Terry never ran — plus a flat 1.25× cache-write multiplier where
> 100% of his cache creation is 1-hour TTL and writes at 2.00×. Rates verified 2026-08-02 against a
> capture of the published pricing page (`assets/C5-Anthropic_Pricing.mp4`).

| Metric | Value |
|---|---|
| Total tokens | **11,346,275,422** |
| API-equivalent list cost | **$13,753** |
| **cache_creation** | 754.7 M — 6.7% of tokens, **51.3% of cost** ⬅ the largest component |
| cache_read | 10.54 B — 92.9% of tokens, **39.9% of cost** |
| output | 48.0 M — 0.4% of tokens, 8.6% of cost |
| input | 3.9 M — 0.03% of tokens, 0.2% of cost |
| Median session | **$0.94** |
| Mean session | **$28.07** (30× the median) |
| Most expensive session | **$1,208 · 1.38 B tokens · 3.2 M output** |
| Second most expensive | **$926 · 298 M tokens** — 3/4 the money on 1/4 the tokens, ratio 8.5× |
| **Top 10% of sessions (49 of 490)** | **89.8% of all cost** |
| **Top 1% of sessions (4 of 490)** | **25.7% of all cost** |
| July 2026 alone | 9.71 B tokens |
| Cost split by tier | opus 75.3% · fable 12.4% · sonnet 12.1% · sonnet-5 0.1% |
| Cache efficiency (read÷write), all | 14.0× |
| Cache efficiency, 10 costliest sessions | **8.5×–31.8× — 8 of 10 above average, 2 below** |

## 2. Title

**Primary — recommended (changed 2026-08-02):**
> **I Measured 11 Billion Tokens in Claude Code. Four Sessions Burned a Quarter.**

Named system + three numbers + a reveal, same formula that won on our own channel
(`Inside Anthropic's Agent Harness: 200+ Features…`, 4.44% CTR).

**Why not the literal swap.** The old title's 96% became **89.8%**, and
*"10% of Sessions Burned 90%"* reads as the 90/10 rule — a thing every viewer already believes. 96%
was startling *because* it wasn't the obvious complement; 90% surrenders that. **Four sessions out of
490 accounting for 25.7%** can't be pattern-matched to Pareto, and it points straight at the thesis
(concentration → session length).

**Alternates:**
- *I Measured 11 Billion Tokens in Claude Code. 7% of Them Cost More Than the Other 93%.* — the
  strongest **paradox** available now (§3: self-sealing, more information deepens it). Downside is
  thesis drift: it titles on the cache-write mechanism (Act 1), not the length finding (Act 6), so
  the payoff doesn't land where the title pointed.
- *Why You Hit Claude Code Limits: I Measured 11 Billion Tokens* — closest to the proven phrasing,
  weaker reveal.
- ~~*My Claude Code Usage Would Cost $28,877…*~~ **DEAD.** The figure is now $13,753 — materially less
  arresting, on top of the "that's not real money" pushback problem.

**Thumbnail:** the real terminal/table with `11,346,275,422` legible and `4` (or `90%`) as the second
element. Numbers must be readable at mobile size. No face.

## 3. Runtime — 18–22 minutes

**Long is correct for this lane** (probe winners: 46.2m, 41.4m, 37.6m, 29.9m, 27.4m, 23.8m, 21.4m;
our own *Agent Harness* 19:26). The 8:12-wins finding came from the **essay** lane and does not
transfer — see `TEN-TITLES-PROBE-2026-08-01.md` §3.

## 4. Cold open — 0:00–0:45, information-first

Target: **≥8 concrete data points in 45 seconds** (Mackard's density, 73.03×). Frame one is the real
aggregation output on screen, not a title card.

Beat content (write to VO, do not read as a list):
1. `11,277,811,806` tokens through Claude Code — on screen, counting up from the raw file scan.
2. 473 sessions · 32,373 messages · one machine · eight months.
3. At list API prices that is **$28,877**.
4. **"I paid a flat subscription fee. So this number is not a bill — it's a measurement."**
5. The median session cost **76 cents**.
6. The mean was **$59.21**.
7. One session was **$3,104**.
8. **Named question, carried:** *"Those three numbers cannot all be true of the same workload —
   unless something very specific is going on. So which sessions are actually eating the limit?"*

**Do NOT** reveal the 96% concentration here. That is the payoff.
**Do NOT** open with "in this video" or reference another video — that exemption in the Agent Harness
teardown applies to reference/implementation videos, and this is an investigation.

## 5. Beat map — the spine is an ELIMINATION LIST

> **CORRECTED 2026-08-01.** This section originally specified a funnel
> `11B tokens → 473 sessions → 47 sessions → 1 decision`. Measured against
> `DECISION-RECORD-2026-08-01.md` §3.2 property 3, that is **four states across ~20 minutes — one
> change every five minutes.** A static graphic, not a spine. Keep the funnel as a **one-shot cold-open
> graphic** (good hook), and run this as the spine instead:

```
   WHAT IS BURNING THE LIMIT?
   ▸ the model            ███ ruled out   (opus 96% — cost shape identical on sonnet)
   ▸ output tokens        ███ ruled out   (0.4% of all tokens)
   ▸ inefficiency         ███ ruled out   (13.7–31.8× cache ratio — ABOVE average)
   ▸ ▓▓▓▓▓▓▓▓▓▓▓          ghosted
   ▸ ▓▓▓▓▓▓▓▓▓▓▓          ghosted
```

Monotonic (fewer suspects survive) · ghosted rather than listed, so it shows how much is left without
revealing what · updates at **every** beat · and the last surviving row **is** the verdict —
session length, which no amount of prompting fixes. Uses the existing ghosted-slot-grid component;
content must resolve within ~1.2s per `CONDUIT-VISUAL-SYSTEM.md`.

| Time | % | Beat | Artifact on screen |
|---|---|---|---|
| 0:00–0:45 | 0–4% | Cold open, numbers, named question | live aggregation output |
| 0:45–3:30 | 4–17% | Where the data comes from — the JSONL usage record, field by field | real `usage` JSON, highlighted |
| 3:30–6:30 | 17–31% | **Suspect 1: the model.** opus 96% / sonnet 4% | model table |
| 6:30–9:00 | 31–43% | **Suspect 2: output tokens.** The intuitive answer — and it's 0.4% of tokens, 10.7% of cost | component bar |
| **9:00–11:30** | **43–55%** | **⭐ THE REVERSAL** (below) | distribution chart |
| 11:30–15:00 | 55–72% | Anatomy of the $3,104 session — 1.38 B tokens, 3.2 M output | session drill-down |
| 15:00–18:00 | 72–86% | **The second reversal** (below) | cache-ratio comparison |
| 18:00–20:00 | 86–100% | What to actually do; the honest unknown; land | checklist card |

### ⭐ The reversal at ~43–55%
Everything so far frames this as an efficiency question — better model, shorter prompts, less output.
Then the distribution lands:

> **Median session: $0.76. Mean: $59.21. Top 10% of sessions: 96.2% of everything.**

There is no general cost problem. There are ~47 sessions. Every habit-level optimisation — model
choice, prompt length, trimming output — is aimed at the 4% that doesn't matter.

### The second reversal at ~72–86% — the one that makes it worth watching
The obvious conclusion is "those sessions were wasteful." **Measured, they are not:**

> Overall cache-read÷write = **13.9×**. The ten costliest sessions run **13.7× to 31.8×** —
> at or **above** average cache efficiency.

The expensive sessions are the *best-cached* sessions. They are expensive because they are **long**.
**You cannot prompt your way out of this.** The only lever is **where you cut the session** — and
that reframes the whole problem from optimisation to scoping.

## 6. Craft floor — the numbers this video must hit

Our 8.00× *Agent Harness* had none of these. The 69–82× videos all did.

| Device | Agent Harness (ours) | **Target here** |
|---|---|---|
| Authored reversal at 40–55% | ✖ none | ✅ **two** (43–55%, 72–86%) |
| Negation density | 1.3/min | **≥3.0/min** |
| Loop named early and carried | 0.4/min, all answered on the spot | 1 carried loop + ≤1.5/min |
| wpm | 125 | 135–150 |

**Negation is the build instruction, not a metric to check afterwards.** Write each act as *what it
isn't*: not the model · not the output tokens · not inefficiency · not prompt length · not a bill.

## 7. GROUNDING — must be verified before a word is recorded

1. **Pricing is an assumption.** $28,877 uses published list rates (opus-tier in $15 / out $75 /
   cache-write 1.25× / cache-read 0.10×) mapped by model-name tier. **State the rates on screen** and
   call it an estimate. Re-check current pricing at record time.
2. **⚠️ THE HONEST UNKNOWN — say it out loud in the video.** We do **not** know how Anthropic's
   subscription limits weight cache reads against fresh input. The mapping from "these tokens" to
   "this is why you hit your cap" is an **inference, not a measurement**. Saying so is on-brand and
   is the thing that separates this from the guess-work videos in the same lane.
3. **491 files scanned, 473 had usage records.** Say the sample is what it is; do not imply totality.
4. Re-run `usage.py` / `cost.py` on the record date so every figure is current.
5. Model IDs shown are internal identifiers as recorded — do not map them to marketing names on
   screen without checking.

## 8. Do NOT

- **No shorts.** 73 of them bought 4 subscribers and 8 watch-hours (`BYRDDYNASTY-CHANNEL-AUDIT.md`).
- **No conduit-essay register.** This is practitioner utility — the probe shows utility WINS in this
  lane and loses in the general lane.
- **No series reference, no "in this video."**
- **Do not lead the title with $28,877.** It reads as clickbait to a subscription audience and
  invites the "that's not real money" derail. Earn it in the open instead.
