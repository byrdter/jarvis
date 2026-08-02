# KeyAdvances YouTube Demand Probe

**Date:** 2026-08-02
**Purpose:** Test the eight proposed KeyAdvances revival concepts against current YouTube outlier evidence before selecting a production slate.

## Decision

The probe validates the broader KeyAdvances opportunity, but it changes the recommended launch order.

### Recommended first three

1. **Who Pays for the AI Data Center Next Door?**
2. **The First Age-Reversal Trial Is Testing Blindness, Not Aging**
3. **Are Solid-State Batteries Finally Worth Waiting For?**

These three have the cleanest combination of repeatable external demand, immediate human consequence, current primary-source evidence, and a distinctive KeyAdvances correction or verdict.

### Hold or reframe

- **AI-agent security:** the lane is real, but the exact passwords/permissions framing is unmeasured. Keep it in the first six, not first.
- **Medical AI:** the lane has demand, but several winning rows are institutional or commercial use cases rather than independent explainers.
- **Humanoid teleoperation:** humanoid listicles travel; the proposed “most still need humans” claim did not produce matching evidence.
- **AI scientists:** current apparent demand is mostly a Demis Hassabis lecture, a Yann LeCun interview, or discovery listicles. Do not produce yet.

## Method

The canonical Jarvis `demand-probe.py` searched YouTube's API for 27 **shape-family queries**, not finished publish titles.

Parameters:

- videos published since 2025-01-01;
- Shorts under 90 seconds excluded;
- channels below 1,000 subscribers excluded as unstable noise;
- reachable comparison band capped at 300,000 subscribers;
- outlier = views divided by current channel subscribers;
- a hit = at least 1.5x;
- `PROVEN` requires at least two hits;
- row-level manual review is mandatory because word-overlap relevance cannot detect semantic drift, paid distribution, listicles, corporate promotion, or borrowed authority.

The probe evaluates whether a **lane or phrasing family** is watched. It cannot select between two finished titles. KeyAdvances' own Studio impressions and CTR remain stronger evidence for packaging decisions.

## Probe scoreboard

| Concept | Families tested | Machine result | Human-audited result |
|---|---:|---|---|
| AI data centers and household bills | 3 | All PROVEN | **Strongest clean lane** |
| Human age-reversal trial | 3 | All PROVEN | **Strong, current, exact evidence frame** |
| Solid-state battery usefulness | 3 | All PROVEN | **Strong, low-drift decision lane** |
| Practical quantum advantage | 3 | All PROVEN | **Strong lane; package as a verdict, not a lesson** |
| AI-agent security | 4 | 2 PROVEN · 1 INCONCLUSIVE · 1 DEAD | **Real security lane; password title unsupported** |
| Medical AI agents/doctors | 3 | All PROVEN | **Promising but commercially/institutionally contaminated** |
| Humanoid robots and human assistance | 5 | 1 PROVEN · 2 MIXED · 2 INCONCLUSIVE | **Generic robot demand, proposed teleoperation angle unmeasured** |
| AI scientists and discovery limits | 3 | 1 PROVEN · 1 MIXED · 1 INCONCLUSIVE | **Weak after borrowed-authority/listicle audit** |

## 1. AI data centers and electric bills — promote to first

### Probe results

| Shape family | Verdict | n | drift | median | max | hits |
|---|---|---:|---:|---:|---:|---:|
| `ai data centers electric bill` | PROVEN | 8 | 17% | 1.42x | 11.63x | 4 |
| `who pays for ai data centers` | PROVEN | 8 | 11% | 1.03x | 108.49x | 4 |
| `ai power grid electricity demand` | PROVEN | 8 | 10% | 0.11x | 2.31x | 2 |

Clean supporting rows:

- [The Entire AI Data Center Explained — From Electricity to ChatGPT](https://www.youtube.com/watch?v=ckoi0RTEgcY) — 154,707 views on 13,300 subscribers, **11.63x**
- [Why Energy Experts Are Concerned About AI Data Centers](https://www.youtube.com/watch?v=lN-JNsJFVm8) — 104,137 on 10,200, **10.21x**
- [Do Data Centers Really Raise Your Electric Bill?](https://www.youtube.com/watch?v=Hixhu3ENLkc) — 10,191 on 5,360, **1.90x**
- [How Much Electricity Does AI Actually Use?](https://www.youtube.com/watch?v=cz3AYYZBiGs) — 44,922 on 27,100, **1.66x**
- [Energy Demand in AI](https://www.youtube.com/watch?v=AN7c5S9k5L0) — 230,495 on 100,000, **2.31x**

The 108.49x maximum came from Applied Digital promoting its own closed-loop cooling system. Exclude it as corporate self-promotion. The lane remains proven without it.

### Implication

This is the strongest first video because it fuses a proven AI-infrastructure lane with a burning household question. KeyAdvances should not merely explain energy consumption. It should adjudicate **who pays**, why the answer varies by utility and region, and why historical rate evidence can contradict current infrastructure warnings.

Recommended packaging:

- **Primary:** `Who Pays for the AI Data Center Next Door?`
- **A/B:** `Is AI Raising Your Electric Bill? The Evidence Is Stranger Than the Headlines.`
- **Thumbnail:** `YOUR BILL / THEIR AI`

## 2. Human rejuvenation trial — promote to second

### Probe results

| Shape family | Verdict | n | drift | median | max | hits |
|---|---|---:|---:|---:|---:|---:|
| `age reversal human trials` | PROVEN | 10 | 29% | 0.99x | 2.87x | 4 |
| `can humans reverse aging` | PROVEN | 7 | 48% | 2.36x | 8.66x | 4 |
| `age reversal what human trial proves` | PROVEN | 9 | 33% | 1.13x | 48.80x | 4 |

Most important row:

- [They Injected a Human With “Youth Genes” — Here's What Actually Happened](https://www.youtube.com/watch?v=0G7pJ2SL5B8) — 143,949 views on 2,950 subscribers, **48.80x**

Supporting rows:

- [The Race to Reverse Aging Is On — Who's Winning?](https://www.youtube.com/watch?v=4bN3MP2zHws) — 25,561 on 2,950, **8.67x**
- [Humans Were Injected: Breakthrough Age Reversal for Every Tissue](https://www.youtube.com/watch?v=WQOIrwOjw94) — 103,508 on 45,500, **2.28x**

Several other rows borrow David Sinclair's name or use aggressive unsupported percentages. They prove interest in the subject, not that those claims should be repeated.

### Implication

The exact “what the trial really proves” frame has already broken out. Do not clone it. Differentiate through the trial's most concrete paradox: the first so-called age-reversal treatment is a one-eye phase-one safety study aimed at optic disease, not a test of whole-body immortality.

Recommended packaging:

- **Primary:** `The First Age-Reversal Trial Is Testing Blindness, Not Aging`
- **A/B:** `One Eye, One Patient, and the Truth About “Age Reversal”`
- **Thumbnail:** `NOT IMMORTALITY`

## 3. Solid-state batteries — promote to third

### Probe results

| Shape family | Verdict | n | drift | median | max | hits |
|---|---|---:|---:|---:|---:|---:|
| `why solid state batteries fail` | PROVEN | 14 | 4% | 0.22x | 9.36x | 2 |
| `solid state battery breakthrough` | PROVEN | 16 | 9% | 0.55x | 6.66x | 4 |
| `solid state batteries worth waiting for` | PROVEN | 12 | 4% | 0.91x | 9.36x | 5 |

Clean supporting rows:

- [Are Solid-State EV Batteries Worth Waiting For?](https://www.youtube.com/watch?v=zsnuGkABfvc) — 62,864 views on 6,720 subscribers, **9.36x**
- [CATL Reveals New Details About Its Solid-State Battery](https://www.youtube.com/watch?v=gWFQ8gTMCoA) — 89,295 on 36,300, **2.46x**
- [The 1,100-Mile Solid-State Battery — Why You Still Can't Buy One](https://www.youtube.com/watch?v=KNhnCUMz1oU) — 8,839 on 5,410, **1.63x**

The lane also contains low-quality hype channels. The most transferable winner is the consumer decision, `worth waiting for`, not the word `breakthrough`.

### Implication

Lead with a decision and use the July MIT grain-boundary research as the mechanism that changes the answer.

Recommended packaging:

- **Primary:** `Are Solid-State Batteries Finally Worth Waiting For?`
- **A/B:** `The 1,100-Mile Battery Has One Problem: You Still Can't Buy It`
- **Thumbnail:** `WAIT OR BUY?`

## 4. Practical quantum advantage — keep high

### Probe results

| Shape family | Verdict | n | drift | median | max | hits |
|---|---|---:|---:|---:|---:|---:|
| `quantum computing useful problems` | PROVEN | 9 | 19% | 1.29x | 15.82x | 4 |
| `quantum computing no advantage` | PROVEN | 7 | 9% | 1.35x | 15.82x | 3 |
| `quantum computers practical advantage` | PROVEN | 12 | 34% | 1.44x | 15.82x | 6 |

Supporting rows:

- [Quantum Computers: Explained Visually](https://www.youtube.com/watch?v=Kv8N9alyYNc) — 583,865 views on 36,900 subscribers, **15.82x**
- [Quantum Computing Is a Lie](https://www.youtube.com/watch?v=Xvavyf_i9lc) — 172,407 on 112,000, **1.54x**
- [Quantum Echoes: Towards Real World Applications](https://www.youtube.com/watch?v=mEBCQidaNTQ) — 414,711 on 97,100, **4.27x**, but posted by Google Quantum AI

### Implication

The topic is proven, but the channel's old generic quantum explainer underperformed. The new episode must be a concrete verdict: a $2 million healthcare prize without demonstrated advantage over classical computing.

Recommended packaging:

- `A Quantum Computer Won $2 Million. It Still Hasn't Beaten Classical Computing.`

## 5. AI-agent security — retain, reframe

### Probe results

| Shape family | Verdict | n | drift | median | max | hits |
|---|---|---:|---:|---:|---:|---:|
| `ai agent security risks` | PROVEN | 12 | 15% | 0.10x | 9.89x | 2 |
| `ai agent cybersecurity` | PROVEN | 13 | 0% | 0.27x | 9.89x | 2 |
| `ai agents passwords permissions` | INCONCLUSIVE | 2 | — | — | — | 0 |
| `dont trust ai agents` | DEAD | 5 | 65% | 0.02x | 0.11x | 0 |

The strongest genuine row:

- [How AI Agents Ignore 40 Years of Security Progress](https://www.youtube.com/watch?v=_3okhTwa7w4) — 154,210 views on 15,600 subscribers, **9.89x**

The second hit under `ai agent cybersecurity` is a build tutorial, not a warning, so the machine verdict overstates repeatability. The broader `security risks` query adds a 2.06x Box explainer, but it is only 1.7 minutes and may have corporate distribution.

### Implication

The topic remains good, especially because KeyAdvances' autonomous-Chrome video already performed. However, the probe does not validate `passwords` as the click-driving noun. Use a broader security verdict and make passwords/permissions the practical payoff inside the episode.

Recommended packaging:

- **Primary:** `AI Agents Ignore 40 Years of Security. Here Is the Part That Breaks.`
- **A/B:** `Before You Trust an AI Agent, Watch What a Web Page Can Make It Do`

## 6. Medical AI — promising but contaminated

### Probe results

- `ai doctors better than doctors` — PROVEN, two hits, but the 112.75x maximum is a WHO Foundation video and may reflect institutional distribution.
- `ai medical agents` — PROVEN, four hits, but the winners are mostly vendor case studies, appointment automation, and tutorials.
- `ai doctors passed medical exam` — machine-PROVEN but semantically false: four of five top rows concern human doctors passing exams or visa medical exams. The only truly relevant AI row scored 0.02x.

One useful independent row:

- [Yes, Doctors: AI Will Replace You](https://www.youtube.com/watch?v=kALDN4zIBT0) — 91,472 views on 23,500 subscribers, **3.89x**

### Implication

Keep the topic, but do not describe it as a medical-exam demand winner. Anchor it to the June 2026 autonomous-workflow research and separate simulation from deployment.

## 7. Humanoid robots — demote the proposed angle

### Probe results

- `humanoid robots need humans` returned PROVEN, but its two hits were generic `Top 10 robots` listicles. The words matched; the thesis did not.
- `humanoid robots actually working` and `humanoid robots factories` were MIXED with one hit each.
- `humanoid robots remote controlled` returned no reachable rows.
- `robots are remote controlled` returned one unrelated Chernobyl-history video.

### Implication

There is visible demand for humanoid robots, especially ranked product lists, but no external proof yet for the teleoperation correction. KeyAdvances' own factory-robot video received 2,828 impressions but only 1.3% CTR. Do not lead the revival with this idea. Re-probe when a named deployment, failure, price, or measurable task creates a more concrete hook.

## 8. AI scientists — do not produce yet

### Probe results

- `ai scientist scientific discovery` — MIXED; the sole 22.66x hit is a 64-minute Demis Hassabis lecture, a borrowed-authority artifact.
- `ai can discover new science` — PROVEN on four rows, but the hits are a 1.9-minute institutional video and a `Top 15 discoveries` listicle.
- `ai scientists cannot make discoveries` — INCONCLUSIVE after 78% drift; its one hit is a 59-minute Yann LeCun interview.

### Implication

The research is interesting, but current YouTube evidence does not show a replicable produced-explainer lane. Hold until a concrete AI-generated discovery creates a named event and human consequence.

## Revised six-video slate

1. `Who Pays for the AI Data Center Next Door?`
2. `The First Age-Reversal Trial Is Testing Blindness, Not Aging`
3. `Are Solid-State Batteries Finally Worth Waiting For?`
4. `A Quantum Computer Won $2 Million. It Still Hasn't Beaten Classical Computing.`
5. `AI Agents Ignore 40 Years of Security. Here Is the Part That Breaks.`
6. `AI Doctors Beat Doctors in a Test. The Real Test Hasn't Started.`

Reserve humanoid teleoperation and AI-scientist discovery for later re-probes.

## What the probe can and cannot decide

The probe has now answered the lane question: several proposed ideas have credible current demand. It has **not** selected the final titles.

KeyAdvances' own Studio evidence says:

- named, specific, checkable claims plus a verdict perform best;
- vague category questions perform worst;
- the channel already receives meaningful recommendation impressions;
- CTR and post-30-second retention are the primary constraints.

Therefore the next gate is not another broad demand search. It is title/thumbnail packaging, followed by a three-video controlled release batch and first-party CTR/retention measurement.
