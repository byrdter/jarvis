# Positioning: the agentic-AI channel (measured 2026-11-08)

Terry asked: *where do I sit between Nick Saraev and Cole Medin, and can measurement guide it?*
Data: the latest 138 long-form videos from each of Nick Saraev, Cole Medin and Nate Herk (414 total),
each scored as views ÷ the median of its ±15 neighbors on the same channel. Titles coded by topic and
form; Mann-Whitney in-bucket vs out. Data + script: `tools/teardowns/lanes-2026-11/`. This
continues `CHANNEL-SALVAGE-AGENT-ENGINEERING.md` (2026-08-22), the "original premise."

## The answer

> **"I test agentic AI on a real, always-on system and report what actually ships."**
> Nate's test-report *format*, pointed at Cole's *subjects* (factories, open models, local,
> open agents), at a depth between Nick and Cole. The proof comes from JARVIS's lab logs.

Why this slot:
- **Nate owns the "I tested X, here's the verdict" format** but stays on hosted frontier models.
  Only 6 of his 138 videos touch open or cheap models, and 2 touch Hermes.
- **Cole owns the subjects** but frames them as process. His factory/harness videos sit at
  par (1.10×, n=28), and his last-30 median is *below* his long-run median.
- **Nick is outcome and status** with little depth. His model-news videos underperform (0.72×,
  p=.015), and his big hits are courses and other people's results.
- **Nobody** shows a factory shipping a named, real product. That supply is zero across 414 titles.

## What the numbers say (pooled across channels unless noted)

| Signal | Ratio | n | p | Read |
|---|---:|---:|---:|---|
| Full course ≥60 min | **2.0×** | 37 | <.0001 | Strongest effect measured. One flagship course per lane. (Not on Cole.) |
| "I Built / Turned / Made…" title | **1.46×** | — | .049 | Use |
| "I Tested / Tried…" title | **1.29×** | — | .03 | Use. Nate 1.42× (n=19) |
| Second brain / AI OS | **1.59×** | 19 | ≈.05 | Positive on all 3, **but wears out as a series** (Cole: 4.4× early → 0.65× late) |
| Outcome-framed autonomous experiment | 1.59× | 6 | weak | Promising: "I let it run 7 days" beats "here's the architecture" |
| Same-app build-offs | 2.33× | 3 | weak | Promising |
| **Question titles** | **0.66×** | 18 | .003 | **Never.** Matches Economics Explained (0.79×) |
| **$ / cost in title** | **0.81×** | — | .049 | Keep money in the video, out of the title |
| "Built a real app" as a topic | 0.98× | 17 | — | **Flat.** Framing decides it, not the topic |
| Local / open / cheaper models as a topic | 0.91× | 20 | — | **Flat** unless framed as a test with a verdict |
| "Free / replaces your paid X" | ~0.85× | 6 | weak | Mixed: "Claude Code for FREE" 2.35× vs "Cloned Calendly…Free Forever" 0.53× |
| Team / org brains | 0.78× | 8 | weak | **Demand unproven on YouTube.** Supply-side is strong (Nate: one member sold 17 company brains at $15K each) |

**The lesson in the "flat" rows:** Terry's favorite *topics* (ship an app, replace a paid
service) do not earn clicks on their own. The **test-and-verdict frame** is what earns them. Every video
is an experiment with a result.

## The lanes, ranked by evidence

1. **Factory output reports.** *I Let an AI Software Factory Run for 7 Days. Here's What Actually
   Shipped.* · *I Had My AI Factory Build the Same App at Every Autonomy Level.*
2. **Open-model test reports.** *I Tested 10 Open Models in Claude Code. These 3 Are Actually
   Usable.* · *I Had Every Open Model Build the Same App. One Clearly Won.*
3. **Second brain, as build-and-test.** Personal first (proven), then team (fresh angle, unproven):
   *I Built One AI Brain for a 20-Person Team. Here's What They Actually Asked It.*
4. **Handing work to open agents.** *I Tested Hermes vs OpenClaw on 10 Real Tasks. What You Need to
   Know.* · *Hermes Agent: Zero to Outsourced Assistant (Full Course).*
5. **Local replaces paid** (weakest; frame as the experiment). *I Replaced 6 Paid Apps With One
   Local Model. Here's What Survived.*

## Title rules (from this data)
- Lead with **I Tested / I Built / I Had X Build**, then **a number of real cases**, then **a verdict**
  ("What You Need to Know," "These 3 Actually Work," "Here's What Shipped").
- No questions. No $ in the title. Avoid stance-only titles on technical subjects (Cole 0.61×).
- **Rotate lanes.** A recurring series decays (Cole's second-brain arc).

## How JARVIS makes this defensible
Every lab run (factory lap, open-model bake-off, Hermes job) writes cost, time, tasks passed and
the model mix to `journal/lab/` (PLAN.md §10). That log is the video's evidence and the thing
Nick- and Nate-style channels can't produce: **measured results on a system that runs 24/7**. This is
the same moat the August analysis found (11B tokens of real telemetry), now pointed forward.

## Limits
- Predicts the **click, not the hold**: titles only, no thumbnails, runtime not controlled.
- Most of Terry's buckets are n<15, so they're directional. The robust findings are: courses, I Tested / I Built
  forms, no questions, no $, second brain positive but wears out.
- Nick's "31 Life-Changing Ways to Use Claude" (1.0M views in 6 days, ~9× his recent median) is full of
  Terry's lane (subscription replacements, local voice) but was too new to count. **Re-check at day 30.**
