# The ten build-register titles — probed 2026-08-01

14 shape families, `demand-probe.py`. Rows read, not just verdicts.
**7 of 10 supported · 2 rejected · 1 unmeasured.** Much healthier than the 2026-07-31 title set
(5 of 10 DEAD there), which is itself evidence that the register change is the right one.

---

## Verdicts

| # | Title | Family | Verdict |
|---|---|---|---|
| **4** | Claude Code Cost Me $X | `claude code cost too much` | **PROVEN — best of batch.** n=21, drift 3, **median 1.24×**, max 14.11×, **10 hits** |
| **2** | My Agent Ran Eight Months | `running ai agents 24 7` | **PROVEN — strong.** n=15, median 0.68×, p75 7.85×, **max 16.70×** |
| **9** | Beads vs Markdown | `ai agent memory explained` | **PROVEN — clean.** n=15, **drift 0**, median 0.61×, max 6.28× |
| **1** | 200 Skills, 12 Fire | `claude code skills` | **PROVEN — clean but modest.** n=25, **drift 0**, median 0.56×, **max only 2.70×** |
| **5** | 200 MCP Tools, Context Collapsed | `too many mcp tools context` | **PROVEN — one near-exact precedent.** max 12.24×; **7.88× on a 1,960-sub channel** |
| **10** | Memory Remembered Wrong Things | `llm long term memory problem` | PROVEN but weak. median 0.14×, drift 8, p75 5.64× |
| **8** | 450k Tokens, Wrong Question | `multi agent orchestration wasting tokens` | PROVEN but marginal. median 0.25×, drift 14, max 4.47× |
| **6** | AI Believed Its Own Docs | — | **UNMEASURED** — no clean family exists |
| **3** | Vector Search Returned Zero | `why rag doesn't work` · `vector search embeddings not working` | ❌ **REJECT** |
| **7** | I Audited My Own Channel | `i built an ai tool to analyze my youtube channel` | ❌ **REJECT — drift false positive** |

## The two rejections — read the rows

**#7 looked like the best result in the batch (median 3.73×, 8 of 11 hits). It is a false positive.**
- 47.03× — *How To **Clone Any YouTube Channel** With Claude AI (Full Auto)*
- 8.90× — *I **BLEW UP** a YouTube Channel in 7 Days with AI*
- 5.03× — ***Clone ANY** YouTube Channel With AI (NotebookLM Hack)*
- 4.48× / 4.01× — ***Clone Any** Youtube Channel With Claude AI*

Four of six rows are the **channel-cloning hustle lane**. The demand is "make money copying other
people's channels," not "audit your own honestly." Textbook drift — exactly what the tool's docstring
warns about, and it would have been believed on the verdict line alone.

**#3 is not supported as a debug story.** `why rag doesn't work` → **THIN, 0.19×, zero hits.**
`vector search embeddings not working` reads PROVEN, but its 12.82× is *How AI Turns Words Into
Vectors: Embeddings* — a **what-is explainer**. The one genuinely on-thesis row,
*RAG Doesn't Work for Code — Here's Why*, scored **0.01×**. **Demand is for what vectors ARE, not
for why yours broke.** A silent-failure debug story has no measured audience.

## Three cross-cutting findings that change standing guidance

### 1. Utility/how-to WORKS in this niche — the opposite of the general-audience rule
`feedback_ideation_self_relevant_story.md` and §8 say utility/how-to probes worse than
self-relevant story. **In the Claude Code practitioner lane the reverse is measured:**
- 14.11× — *How to Optimize Token Usage in Claude Code* (5,450 subs)
- 10.90× — *How to Optimize Token Usage in Claude Code* (5,500 subs)
- 10.50× — *Stop Hitting Claude Code Rate Limits! (3 pro tips)* (1,180 subs)
- 8.33× — *I Stopped Hitting Claude Code Usage Limits (Here's How)* (15,800 subs)
- 6.28× — *How AI Agents Remember Things* (12,500 subs)

**Practitioners want utility. General audiences want story.** Both rules are true; they apply to
different audiences. This is the cleanest explanation yet for why the conduit essays underperform
and the build videos don't — they are aimed at different people.

### 2. This lane is REACHABLE at our size — the previous ones were not
Channels scoring 5–14× here: **1,160 · 1,180 · 1,960 · 5,450 · 5,500 · 5,760 · 9,930 · 10,800 ·
12,100 · 12,500 subs.** Byrddynasty is 147. The limits/conduit lane's big numbers all belonged to
borrowed authority or 25k–400k-sub channels.

### 3. Runtime: LONG wins here — reverses the short-form conclusion FOR THIS LANE
Winners: **46.2m · 41.4m · 37.6m · 29.9m · 27.4m · 23.8m · 21.4m · 16.3m · 15.0m.**
- 14.20× — *How I use Claude Code (Meta Staff Engineer Tips)* — **46.2 min**, 32,800 subs
- 8.57× — *Every Claude Code Concept Explained for Normal People* — **27.4 min**, 94,400 subs
- 1.56× — *Every Claude Code Memory System Compared* — **41.4 min**, 94,400 subs

The 8:12-beats-22:49-beats-45:12 finding came from the *essay* lane (Mackard / Universal Resilience /
Fractal). **It does not transfer.** In the practitioner lane, comprehensive and long is the winning
shape — which also matches our own *Agent Harness* at 19:26.

## Revised shooting order

1. **#4 — Claude Code cost.** Best median, 10 hits, every winner a small channel, and we have real
   billing data. Two channels under 5,600 subs did 14.11× and 10.90× on the *same title*.
2. **#2 — the eight-month agent.** Max 16.70×, first-person build reports dominate the rows
   (*I have 25 AI Agents working 24/7*, *I Built an AI Agents Army*), and our Dropbox-eviction
   failure is a real, undocumented story.
3. **#9 — memory systems compared.** Zero drift, and *Every Claude Code Memory System Compared*
   (94.4k subs, 41.4 min) is literally this video's shape already working.
4. **#5 — MCP context overload.** *MCP Context Overload: Why Too Many Tools Break Your AI Agent*
   did **7.88× on 1,960 subs** — near-exact precedent at a reachable size.
5. **#1 — skills that never fire.** Clean lane, zero drift, but **max 2.70%** — a safe floor, not a
   breakout. *Stop Confusing Skills and Subagents in Claude Code* did 7.08× on 1,160 subs, so the
   **disambiguation-verdict** framing beats the survey framing here.

**Do not shoot #3 or #7 as written.** #6 needs a family found before it can be judged.

## Caveat that still applies
Medians in this lane are low (0.15–1.24×) with high hit counts — these are **competitive** lanes with
many makers, not open ones. The advantage is that the winners are our size, which was never true of
anything probed on 2026-07-31.
