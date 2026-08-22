# Channel salvage — what to pull out of Byrddynasty, and what it's about

**Measured 2026-08-22** at Terry's request: *which of the last 30 videos can be repackaged into a new
channel, and what would its core be?*

I widened the window. **The last 30 is too noisy to decide on** — its videos run 3–96 views, so a
cluster difference of 0.22 vs 0.60 views/day is a difference between ~8 and ~27 lifetime views. That
is not a signal. The full 96-video catalog is unambiguous, so this analysis uses that.

---

## 0. The answer

> **There is one channel in here, it is much bigger than one or two videos, and it is not the one the
> last 30 videos suggest.**
>
> **42 of 96 videos form a single coherent cluster: AI agent engineering — specifically why agents
> FAIL in production and what fixes it.** That cluster has **median 48 views against a channel median
> of 21**, holds **10 of the top 12 videos**, and contains both 1,100-view videos — the channel's
> ceiling.

---

## 1. The measurement

Full catalog, first-match clustering:

| cluster | n | median views | mean | top |
|---|---:|---:|---:|---:|
| **AGENT BUILDING / Claude Code practice** | **42** | **48** | **116** | **1,100** |
| AI RELIABILITY / when AI is wrong | 12 | 13 | 29 | 138 |
| AI LABOR / economics | 8 | 13 | 17 | 33 |
| AI INFRA / community harm | 3 | 27 | 24 | 33 |
| AI MONEY / bubble / pricing | 5 | 12 | 12 | 15 |
| (unclustered) | 28 | 14 | – | 185 |
| **CHANNEL MEDIAN** | 96 | **21** | | 1,100 |

**Top 12 videos: 10 are agent-building.** No other cluster clears the channel median by a meaningful
margin, and none has both volume and a ceiling.

### 1.1 Why I first got this wrong

Working only the last 30, age-normalised, the best cluster looked like *infrastructure/community harm*
(0.60 views/day) and *AI reliability* looked promising on the strength of one 96-view video. Both
readings dissolve on the full catalog. **The last 30 are all 30–70 days old and 3–96 views — there is
no statistical room for a cluster ranking there.** Recorded because it is the same trap as the Fireship
approximate-date table: a small, noisy slice produced a confident wrong answer.

---

## 2. The core — and it is sharper than "AI agents"

Read the 42 titles together and the through-line is not *how to build an agent*. It is **why the one
you built breaks**:

- Why AI Agents Fail After 2 Hours (And How Harnesses Fix It) — 145
- Why Your AI Agent Wastes 95% of Its Context — 132
- Why One Giant Prompt Breaks AI Systems (The PIV Loop) — 92
- Why Agentic AI Demos Fail in Production — 46
- Why "Just Prompting" Fails in Production — 28
- Why Your AI Forgets Everything (Agent Memory) — 31
- Why Prompt Engineering Fails at Scale — 8
- Context Overload? Master Subagents — 24
- Stop Wrapping Bash. Let The Agent Just Run It — 79
- Stop Re-Prompting Your Agent. Write A Skill Instead — 77
- MCP: The Honest Verdict — When To Use It, When To Skip It — 53
- From Black Box to Glass Box: Observable Agent Reasoning — 27
- Agentic Security: How Autonomous AI Fails — 14

> ### The core, in one line
> **"Why your AI agent breaks — and what actually fixes it."**
> Operator-grade failure modes, proven on a real system that has been running 24/7 for months.

### 2.1 Why this is defensible

The obvious lane is crowded; **this specific slice is not.**

| query | monthly searches | competition |
|---|---:|---:|
| ai agents | 779,920 | **69** |
| ai automation | 1,078,060 | 60 |
| how to build ai agents | 92,940 | **59** |
| ai agents tutorial | 72,070 | 50 |
| ai agents explained | 115,704 | 56 |
| **claude usage limits** | **44,751** | **34** |
| **claude code cost** | 8,886 | 43 |
| **claude code pricing** | 5,017 | **26.5** |

The head terms are beginner-saturated at competition 50–69. **The long tail — the operator questions —
runs at competition 26–43.** Those are the questions Terry's catalog already answers, and they are
asked by people who have *already* built something and hit a wall.

Topic liveness, from vidIQ's daily trend: **~90,000–120,000 views/hour** across the agent lane through
late August 2026. It is not decaying.

### 2.2 The moat, and it is real

Terry runs **JARVIS** — an actual agent system, live for months, generating real telemetry:
**11,346,275,422 tokens across 509 sessions and 33,313 messages**, all locally verifiable.

Nobody making beginner agent tutorials can produce that. Every failure-mode claim can be backed with
"here is what happened on a system that has been running since January." **That is the unfakeable
asset, and it is the reason this core is defensible rather than just another agent channel.**

---

## 3. What migrates

### Tier 1 — the spine (the channel IS these)
Every "why it fails / what to do instead" video. Roughly 15 titles, listed in §2. These are evergreen,
search-addressable, and operator-grade. **Lead with these.**

### Tier 2 — the proof layer
The JARVIS build videos: *Building JARVIS: A True Second Brain* (1,100), *Inside Anthropic's Agent
Harness* (1,100), *Claude Code Agent SDK* (188), *Vector Search & Gmail Automation* (114), *Command
Center* (57), *Full Terminal Access From Telegram* (51), *$100K Portfolio* (130).

These are not the pitch — they are the **evidence that the system is real**, which is what licenses
the Tier 1 claims. Both 1,100-view videos live here, so they are also the best available trailers.

### Tier 3 — bring, but re-title
The comparison/reference videos: *Which AI Agent Framework Should You Use?* (240), *Claude Subagents
vs. Agent Teams* (113), *What is Agentic AI?* (34), *AI Agent Interoperability* (26). Real search
intent, currently essay-titled. Re-title query-first per `BYRDDYNASTY-FIRESHIP-ROADMAP.md` §3.1.

### Also bring: the 11B tokens video
*Your AI Subscription Costs 14X What You Pay For It* (10 views) belongs on this channel, not the old
one. It is a Claude Code operator question sitting on an ~80K/month query cluster at competition
26–43. Re-titled query-first it is a **Tier 1** asset, and it is the single best demonstration of the
telemetry moat.

---

## 4. What does NOT go

| stays behind / separate | n | why |
|---|---:|---|
| **Athlete / celebrity money** (Ronaldo, footballer, $750K ad) | 3 | Entirely different audience. Not adjacent to anything here. |
| **AI labor & economics** (layoffs, paychecks, entry-level jobs) | 8 | General commentary. No edge, no moat, and demand-probed MIXED/DEAD earlier this session. |
| **Philosophy / frameworks** (Pope, 7 Boxes, Nine Skills) | ~5 | The Nine Skills material is Terry's own framework — low external pull (9–98 views). |
| **AI reliability / hallucination** | 12 | Coherent, and "ai hallucination" is a genuinely good keyword (25,863/mo at competition **25.2**, the best ratio measured all session). But it is a **different channel**, not part of this one. **Park it as candidate #2.** |
| **Data centers / community harm** | 3 | **Do not discard.** This is the one lane measured **PROVEN** (969×, replicating the 955× recorded 2026-07-30). But it is browse-driven with *zero* search volume and a homeowner/local-politics audience — incompatible with an engineering channel. Its own thing, or leave on Byrddynasty. |

---

## 5. Practical notes

1. **YouTube cannot move videos between channels.** Migration means re-upload. At a median of 48
   views, the loss is negligible — and it buys a clean slate with correct titles, descriptions and
   thumbnails. **The low view counts are, unusually, an argument in favour.**
2. **Do not re-upload all 42 at once.** Launch with 8–12 Tier 1 videos, correctly packaged, then add
   at a normal cadence. A wall of back-catalogue on day one gives the algorithm no signal to read.
3. **Re-title everything query-first before re-uploading.** That is the whole point of the move; a
   re-upload with the old essay titles reproduces the original outcome.
4. **Keep Byrddynasty.** It becomes the general-interest AI channel (labor, infrastructure, money,
   reliability). The split is the fix for the "six channels in one" problem — not abandonment.

---

## 6. Honest limits

- **This predicts the click, not the hold.** Same standing warning as every teardown in this corpus.
  Byrddynasty was independently diagnosed as retention-gated; a cleaner channel identity fixes
  discovery, not the first thirty seconds.
- **The agent lane is crowded at the head** (competition 50–69). The recommendation rests on the
  *operator long tail* being uncrowded (26–43) and on the JARVIS telemetry moat. If either fails, this
  is a commodity lane.
- **Cluster medians are lifetime views on a channel with almost no distribution.** 48 vs 21 is a real
  ratio on n=42, but the absolute numbers are tiny and neither is evidence that the format works at
  scale — only that it is the strongest thing here.
- **Keyword figures are vidIQ estimates**, not YouTube ground truth. The cluster shape is clear;
  individual numbers are directional.
