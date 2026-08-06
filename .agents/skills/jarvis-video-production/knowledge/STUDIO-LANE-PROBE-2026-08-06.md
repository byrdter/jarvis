# Studio-lane demand probe — 2026-08-06

18 shape families, two rounds, via `tools/demand-probe.py`. Raw rows in `tools/demand-probe.csv`.
Band 1,000–300,000 subs, since 2025-01-01, shorts excluded, ≥1.5× = hit.

**Question:** if the Studio build became the subject matter, does that shape travel — and which
framing of it?

---

## Round 1 — the AI-video framings

| verdict | n | drift | median | p75 | max | hits | query |
|---|---|---|---|---|---|---|---|
| PROVEN | 32 | **2%** | 0.65x | 1.96x | 4.46x | **10** | ai video consistent characters |
| PROVEN | 18 | **0%** | 0.30x | 1.64x | 16.49x | 5 | my ai video workflow |
| PROVEN | 24 | 1% | 0.36x | 0.60x | 5.28x | 2 | ai filmmaking workflow |
| PROVEN | 16 | 7% | 0.44x | 1.04x | 8.37x | 2 | i tested ai video generators |
| PROVEN | 13 | 7% | 0.44x | 0.87x | 2.46x | 2 | ai video automation pipeline |
| PROVEN | 6 | 13% | 1.10x | 1.74x | 16.44x | 2 | i built an ai video tool |
| PROVEN | 6 | 9% | 0.63x | 1.64x | 7.88x | 2 | how ai video actually works |
| THIN | 4 | 13% | 0.54x | 1.17x | 1.17x | 0 | how ai video generation works |
| INCONCLUSIVE | 5 | 65% | — | — | 61.55x | 1 | ai film studio setup |

**Row reads that change the verdicts:**
- **"how ai video actually works" is a FALSE POSITIVE.** Top rows are *"SIMPLEST Explanation of How
  Artificial Intelligence Works?"* (7.88×) and *"How AI Actually Works in 10 Minutes"* (1.64×) —
  general-AI explainers with zero AI-video content. Word overlap only. Discard.
- **"i built an ai video tool" is partly false.** The 16.44× is *"I Make Animated Videos 100% FREE"* —
  a free-tools video. The genuine build-in-public row scores 1.37×, below the hit line.
- **"ai film studio setup"** was correctly auto-downgraded: its 61.55× is **ImagineArt promoting its
  own product**. Vendor reach, not audience demand.
- **"ai video automation pipeline"** passes on n8n no-code content — a different audience. Real
  "I built a pipeline" rows score 0.87× and 0.75×.

**Genuine in round 1:** consistent characters (most hits, lowest drift, repeatable), personal
workflow (0% drift, **16.49× on a 5,070-sub channel**), filmmaking workflow (5.28× on 13,300 subs;
a 45-minute concept-to-film at 1.49× on 10,800).

**Not validated:** the mechanism/survey framing — *"how it works / what each tool brings"* — which is
the framing the idea started as. Tutorial framing displaces it.

---

## Round 2 — the build-your-own-AI-system framings

| verdict | n | drift | median | p75 | max | hits | query |
|---|---|---|---|---|---|---|---|
| **PROVEN** | 16 | 8% | **3.69x** | **8.17x** | 37.56x | **11** | **i built my own ai assistant** |
| PROVEN | 14 | **2%** | 0.62x | 3.26x | 14.26x | 5 | claude code automation workflow |
| PROVEN | 25 | 1% | 0.35x | 0.96x | 4.74x | 4 | ai second brain system |
| PROVEN | 6 | 2% | 2.06x | 4.59x | 92.93x | 3 | why ai video looks fake |
| MIXED | 7 | 1% | 0.20x | 0.60x | 2.09x | 1 | why my ai project failed |
| THIN | 4 | 16% | 0.50x | 1.40x | 1.40x | 0 | how much does ai video cost |
| INCONCLUSIVE | 3 | 79% | — | — | 36.42x | 1 | ai video quality problems |
| INCONCLUSIVE | 1 | 9% | — | — | — | — | what i learned building with ai |
| INCONCLUSIVE | 1 | 19% | — | — | — | — | automating my work with ai agents |

**Rows are clean — no false positives in the strong shapes.**

`i built my own ai assistant` — every row genuinely a build-your-own-assistant video, on very
reachable channels:
```
 37.56x    980,360    26,100  How to Create Your Own AI Assistant (No Code)
 12.40x    306,410    24,700  I Created the AI Assistant We All Dreamed Of (Iron Man Jarvis…)
 10.46x    258,457    24,700  I Built an AI Desk Assistant That Can Rewrite its Own Code
  8.17x     98,034    12,000  I Built My Dream AI Assistant. Then I Shut It Down.
  6.89x     30,917     4,490  Building an AI Girlfriend in 2026? (Full Code Setup)
  5.05x    124,638    24,700  I Built a Local AI Assistant: 100% Free & No Subscriptions
```
One 24,700-sub channel hits 12.40× / 10.46× / 5.05× — **repeatable at our size, not a lottery.**

`claude code automation workflow` — and note the exact intersection of both halves of the work:
```
 14.26x    467,699    32,800  How I use Claude Code (Meta Staff Engineer Tips)
  7.27x     96,724    13,300  How I Fully Automated My Video Editing (Claude Code)
  4.32x    353,546    81,800  How Claude Code's Creator Starts EVERY Project
  3.26x    163,160    50,100  How I Fully Automated My Video Editing (Claude Code)
```
**"How I Fully Automated My Video Editing (Claude Code)" appears twice, from two independent
channels, both hits, one at 13,300 subs.** That title is the bridge between the Studio and JARVIS.

`ai second brain system` — 4.52× *Build The ULTIMATE AI Second Brain (Obsidian + Claude)* at 58.5
minutes; 3.12× on a **5,370-sub** channel.

---

## The headline

**The build-your-own-AI-system lane is ~5× stronger by median than the AI-video lane.**
Round 1 best median 0.65× / p75 1.96×. Round 2 best median **3.69×** / p75 **8.17×**.

This is corroborated independently by our own analytics in
[BYRDDYNASTY-CHANNEL-AUDIT.md](BYRDDYNASTY-CHANNEL-AUDIT.md):
- *Building JARVIS: A True Second Brain with Claude Code* — **31.7 watch-hours**, against a February
  average of 12.4 h/video and a July average of 0.87 h/video.
- The top three videos by CTR are all in this lane: *Command Center for a Second Brain* (6.4%),
  *Building JARVIS* (5.4%), *Vector Search & Gmail* (5.2%).
- The audit's own recommendation #1 is **"Return to the Feb–April register."**

Three independent sources agree: our analytics, our audit's stated recommendation, and external
demand measured twice today.

---

## Two precise findings, easy to get wrong

**1. Failure narratives work as a TWIST on a build, not as a genre.**
*"I Built My Dream AI Assistant. Then I Shut It Down."* → 8.17× on 12,000 subs.
*"Why I Deleted My Second Brain"* → 4.74× on 32,700 subs.
But standalone **`why my ai project failed` → MIXED**, one hit at 2.09×, and
**`what i learned building with ai` → INCONCLUSIVE, n=1.**
So "what didn't work" must ride on a specific named build. It does not stand alone.

**2. `why ai video looks fake` is a real lane but a different one.**
PROVEN, 2% drift — but the rows are *detection* content (*"8 Easy Ways To Spot Fake AI Videos"*
92.93×, *"How to Spot AI Videos in 2025"* 3.48×), i.e. consumer protection, not the mechanism of why
generation drifts. Adjacent to us, not ours.

---

## What this does and does not license

**Supports:** one named system + what it does + what it cost + what broke, demonstrated in the
working thing. The Studio and the JARVIS federation as *subject*, not just as *capability*.

**Does not support:** surveying the AI-video tool landscape ("what each tool brings"). That is the
tool-review treadmill — a 278k-sub channel already owns it and the content dates in weeks.

**⚠ Unresolved tension, flagged not decided.** [[feedback-channel-direction-held]] (2026-08-02)
records that a JARVIS-failure-receipts framing and a named-system+number+verdict framing were
**considered and declined**, along with any revert to "I create it and report it." The lane measured
here is adjacent to that. The distinctions that may make it not a reversal: it is Terry's own
proposal rather than a reactive fix to a bad-numbers day; it keeps the essay format and the "stories
about AI and its effects" identity; and the demonstration is *evidence inside an essay*, not a
tutorial. **The failure mode is real: if it becomes a build-log for builders, it has become the thing
that was declined.** Terry decides; this file only records that the question is live and what the
numbers say.
