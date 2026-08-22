# Timeliness revision — I measured stock, not flow, and it cost the main recommendation

**Written 2026-08-22** after Terry's critique: *are these topics still timely? Context engineering has
had a lot of play, and harness engineering seems to be the new thing.*

**He is right on both counts, and the error is mine.** This document revises
`AGENTS-IN-PRODUCTION-LAUNCH.md` §3.

---

## 0. The methodological error

Every keyword judgement in the launch plan used **`estimatedMonthlySearch` and `competition`** — both
**stock** measures. Neither says whether a term is *rising, flat, or saturating*. I never asked what
was gaining momentum; I asked how big the terms I had already chosen were. **That is answering the
question I set rather than the question that matters.**

Two things fell out of it once measured properly.

### 0.1 Search volume badly overstates real consumption

vidIQ's `vphDailyViews` (views/hour accruing to content on a term) is the flow measure:

| term | est. monthly search | **actual views/hour** | ratio to context-eng |
|---|---:|---:|---:|
| prompt engineering | 469,633 | **~220,000** | ~88× |
| ai agents | 779,920 | **~100,000** | ~40× |
| **context engineering** | 98,056 | **~2,500** | 1× |

**"Context engineering" carries 98K monthly searches and delivers ~2,500 views/hour.** On the
search-volume figure it looks like a fifth of prompt engineering; on actual consumption it is under
**1.5%**. I built three titles on it and ranked it as a lead term. That was wrong.

*(Its trend is genuinely upward — 663/hr on Jul 25 to ~3,000/hr by Aug 21 — so the term is not dying.
It is simply far smaller than its search figure implies.)*

### 0.2 The lane has moved, and the field says so out loud

The videos on the current term state the succession explicitly:

> *"If Context Engineering was the skill of 2025, then Harness Engineering is becoming the skill of
> 2026."* — Edward Donner
>
> *"Everyone says 'harness engineering' is the most important skill in AI coding for 2026, but almost
> nobody can tell you what it actually is."* — Cole Medin
>
> *"Prompt engineering may no longer be the real advantage in AI."* — AI Revolution

**Prompt engineering (2023–24) → context engineering (2025) → harness engineering (2026).** My titles
positioned on the previous two stages of that arc.

---

## 1. Harness engineering — verified, and it is the strongest lane measured all session

**First, the drift check** (the "titles, never bare counts" rule). "Harness engineering" is 108,188/mo
with top markets India 27%, Chile 8%, Brazil 5% — a profile consistent with *automotive wire-harness*
engineering, a large industrial field. **Checked against actual results: zero drift.** All 12 top
results are AI agent harness content.

| term | monthly | competition |
|---|---:|---:|
| **harness engineering** | **108,188** | **43.8** |
| agent harness | 32,971 | 44.5 |
| what is agent harness | 17,769 | 50.4 |
| ai agent harness | 13,503 | 61.6 |
| what is an agent harness | 5,367 | **37.4** |
| agent harness explained | 4,451 | 43.2 |
| claude agent harness | 4,339 | 52.0 |

**~186K monthly across the cluster at competition 37–62 — and "harness engineering" alone beats
"context engineering" on every axis:** more volume (108K vs 98K), lower competition (43.8 vs 54.1),
higher opportunity score (67.6 vs 63.1).

### 1.1 The outlier pattern is the real signal

| video | channel subs | views | **outlier** | published |
|---|---:|---:|---:|---|
| Harness Engineering Masterclass | **4,310** | 40,784 | **96.9×** | 2026-05-16 |
| What Is Harness Engineering? | 40,600 | 25,297 | **79.4×** | 2026-07-29 |
| Harness Engineering (Lopopolo, OpenAI) | 623,000 | 212,924 | 19.0× | 2026-04-17 |
| Harness Engineering Explained in 22 Min | 101,000 | 20,520 | 9.7× | 2026-07-19 |
| Agent Harness explained in 8min | 104,000 | **371,287** | 7.3× | 2026-05-22 |
| Harness Engineering: What Separates Top Agentic Engineers | 222,000 | 77,725 | 2.8× | 2026-05-28 |

**A 4,310-sub channel got 40,784 views — 9.5× its subscriber count.** Small channels are landing
enormous outliers, which is the signature of **demand exceeding supply.** Every one of these was
published between March and August 2026. This is live, right now.

### 1.2 And Terry already owns the asset

> **His single best-performing video is *"Inside Anthropic's Agent Harness: 200+ Features Built
> Autonomously"* — 1,100 views, tied for #1 on the channel.**

I put it in **Tier 2 ("proof layer")** and re-titled his *other* harness video —
*"Why AI Agents Fail After 2 Hours (And How Harnesses Fix It)"* — to *"AI Agents in Production: Why
They Fail After 2 Hours"*, **deleting the word "harness"** and pointing it at a competition-69 head
term instead. That is a straightforward mistake and it inverted the two best assets on the channel.

---

## 2. Revised evaluation of all 16 re-titles

Verdicts: **LEAD** (current front, ship first) · **KEEP** (durable, not trendy) · **REFRAME** (right
material, wrong term) · **DEMOTE** (positioning on a past stage).

| # | my re-title | term stage | verdict | revised |
|---|---|---|---|---|
| — | *(not in Tier 1 — my error)* **Inside Anthropic's Agent Harness** | **2026 front** | **LEAD** | **What's Actually Inside an Agent Harness: Anthropic's, Taken Apart** |
| 5 | AI Agents in Production: Why They Fail After 2 Hours | reframed off-term | **REFRAME** | **Agent Harness Explained: Why Agents Fail After 2 Hours Without One** |
| 16 | Claude Code Pricing: I Counted 11 Billion Tokens… | evergreen operator | **LEAD** | unchanged — competition 26.5, and the moat demo |
| 3 | MCP Explained: When To Use It — And When To Skip It | 2025, still large | **KEEP** | unchanged — 77K/mo, and "when to skip" is differentiated |
| 12 | Claude Code Subagents: How to Fix Context Overload | harness-adjacent | **REFRAME** | **Subagents in Your Harness: Fixing Claude Code Context Overload** |
| 8 | Claude Code Skills Explained: Stop Re-Prompting | harness component | **REFRAME** | **Skills in an Agent Harness: Stop Re-Prompting Your Agent** |
| 7 | Claude Code Tools: Stop Wrapping Bash | harness component | **REFRAME** | **Harness Tools Done Right: Stop Wrapping Bash** |
| 10 | AI Agent Memory Explained: Why Your Agent Forgets | harness component | **REFRAME** | **Memory in an Agent Harness: Why Your Agent Forgets Everything** |
| 13 | AI Agent Observability: How to See What Your Agent Is Doing | harness component | **REFRAME** | **Harness Observability: How to See What Your Agent Is Doing** |
| 14 | AI Agent Security: How Autonomous Agents Get Exploited | durable | **KEEP** | unchanged |
| 1 | Context Engineering for AI Agents: Why You Waste 95% of It | **2025 stage** | **REFRAME** | **Context Engineering Was 2025. Here's What Replaced It.** — uses the term as the *setup*, lands on harness |
| 15 | Why Prompt Engineering Fails at Scale — Use Context Engineering | **2023 stage** | **REFRAME** | **From Prompt to Context to Harness: Why the First Two Stopped Working** |
| 6 | Prompt Engineering at Scale: Why One Giant Prompt Breaks | **2023 stage** | **DEMOTE** | huge consumption (~220K/hr) but heavily saturated and framed as obsolete. Ship late, if at all. |
| 11 | Why Prompting Alone Fails in Production | 2023 stage | **DEMOTE** | merge into #15 — near-duplicate |
| 9 | Agentic AI in Production: Why the Demos Fail | generic, comp 68 | **KEEP** | durable but crowded — mid-order |
| 2 | Best AI Agent Framework in 2026? 6 Compared | evergreen comparison | **KEEP** | genuine search intent, ages via the year in the title |
| 4 | Claude Subagents vs Agent Teams | evergreen comparison | **KEEP** | unchanged |

### 2.1 Revised launch order

The old order led with Claude Code Pricing then MCP then Context Engineering. **Revised:**

1. **Inside Anthropic's Agent Harness** *(re-cut)* — the current front, and his proven best asset
2. **Agent Harness Explained: Why Agents Fail After 2 Hours Without One**
3. **Claude Code Pricing / 11 Billion Tokens** — competition 26.5, moat demo
4. **Context Engineering Was 2025. Here's What Replaced It.** — rides the old term into the new one
5. **MCP Explained: When To Use It — And When To Skip It**
6–10. The harness-component set (subagents, skills, tools, memory, observability)
11+. The generic/agentic and prompt-stage material

---

## 3. What this does to the channel core

The core does **not** change, but it gets sharper and gains a current name:

> **Agents in Production** — *"Why your AI agent breaks, and what actually fixes it."*
> **The spine is the HARNESS**: the layer around the model — tools, memory, skills, subagents,
> permissions, verification — that turns an LLM into something that survives real work.

That is precisely what his 42-video catalog already covers; it now has the term the field is
currently using for it. And the moat sharpens: **JARVIS is a working harness with 11.3B tokens of
telemetry through it.** Cole Medin's framing — *"almost nobody can tell you what it actually is"* — is
an open invitation to the one person who can show a real one running.

---

## 4. The risk, stated plainly

**Harness engineering is a fast-moving term and may be past peak before a 8–12 video run ships.** The
outlier scores (79×, 97×) say demand currently exceeds supply, but that gap is exactly what attracts
supply — Cole Medin, OpenAI, AI Jason and Shaw Talebi are already in it.

**Mitigation: own the substance, use the current term.** The underlying subject — making agents
reliable in production — is durable and is what the 42 videos are actually about. The *word* may fade;
the material does not. Title with the current term, structure the channel around the permanent
question, and expect to re-title again in 12 months.

**This is also the argument for the self-format-decay tracker already filed as P1.** The whole reason
this correction was needed is that nothing in our tooling watches term trajectory — and the same blind
spot will recur on whatever replaces "harness."

---

## 5. What to change in method, so this does not repeat

1. **Never rank a keyword on `estimatedMonthlySearch` alone.** Pull `vphDailyViews` — the discrepancy
   was ~40× on context engineering.
2. **Ask what is rising before choosing terms**, not after. Run `mode: 'rising'` and check the
   competitor set for the topic; do not just size the terms already in hand.
3. **Drift-check every keyword against actual results** before building on it. "Harness engineering"
   *looked* like automotive from its geography and was not — the check took one query and could have
   gone the other way.
4. **Check the small-channel outlier pattern.** A 4,310-sub channel at 9.5× its subscriber count is a
   far stronger signal of an open lane than any volume/competition pair.
