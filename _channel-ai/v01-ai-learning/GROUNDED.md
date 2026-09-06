# V01 — AI and learning · GROUNDED (v2)

**Working title:** *Students Using AI Score Higher. Then They Forget Everything.*
**Status:** research grounded, rebuilt 2026-09-06 around Terry's category distinction. Not yet scripted.
Every figure below is verified at primary source or the publisher's own abstract — never from an
aggregator's rendering.

---

## 0. The distinction that organizes everything (Terry, 2026-09-06)

> **AI used FOR learning** (built to teach you) — *not this video.*
> **AI used to DO THE TASK**, and what that does to learning and retention — *this video.*

This is not a scoping preference. **It is the finding.** Without it the literature looks
self-contradictory: a 2025 meta-analysis says AI *helps* learning, and five studies say it *hurts*.
Sort them by the distinction and the contradiction disappears.

| | Category A — AI as pedagogy | Category B — AI does the task |
|---|---|---|
| **Effect on learning** | **Positive** (g = 0.392) | **Negative or flat, every time** |
| **In this video** | The counterweight — one scene | The spine |

---

## 1. Category A — the counterweight (2 sources)

**Zhu, Y., Liu, Q. & Zhao, L. (2025).** *"Exploring the impact of generative artificial intelligence
on students' learning outcomes: a meta-analysis."* **Education and Information Technologies**,
30:16211–16239. DOI `10.1007/s10639-025-13420-z`. Received 23 Sep 2024, published 26 Feb 2025.

- **26 empirical studies** screened from **5,887**; RCTs only; search window **2020 – Aug 2024**.
- Overall effect **g = 0.392** — significant but small. Physical g=0.701 · social-emotional g=0.347 ·
  intellectual g=0.372.
- Longer interventions beat short ones. *(Yin et al. 2021: no effect after a 40-minute session.
  Essel et al. 2022: marked improvement after 16 weeks.)*
- ⚠️ **Terry's read is correct — this is pre-2025 evidence.** Interventions are chatbots and
  intelligent tutoring systems. Use it to establish that **AI built to teach does work**, then leave it.

**Sarsenbayeva, N., Bizhigitova, E., Orazkeldiyeva, Z., Sadykova, A., Alimbekova, R., Absadikova, I.
& Avasi, V. (2026).** *"Human-AI collaborative assessment in central Asian EFL classrooms: An action
research study."* **Social Sciences & Humanities Open 14 (2026) 103280.** Nazarbayev Intellectual
School, Kazakhstan. *(Local: `AIStudyCyborg.pdf`)*

Longitudinal action research, EFL writing, ages 16–18, five instructors using Microsoft 365 Copilot
with a "Dictation Bridge" for handwritten essays. **Teacher-mediated AI feedback produced highly
significant IELTS band-score improvement (p < .001).** Coins the **"cyborg workflow"** — AI handles
analytical grading, the teacher interprets and contextualizes.

⚠️ **Weak evidence tier** — single site, action research, no control arm. Use for the *shape* of the
argument (AI + human mediation works), never as a causal number. **One finding worth stealing:**
unmediated AI feedback may put **high-achieving students at risk of "stylistic flattening"** — which
rhymes with the CEPR finding that high achievers lose most.

**Bastani et al. — the "GPT Tutor" arm** *(full citation in §2)*. Guardrailed: teacher-designed hints,
no answers. **+127%** during practice — the *largest* gain in the study — and afterward
**statistically indistinguishable from control.** Best short-run performance, zero lasting harm.

---

## 2. Category B — the spine. Five studies, five designs, one signature

### 2.1 Barcaui, A. (2025) — the cleanest retention number ⭐
*"ChatGPT as a cognitive crutch: Evidence from a randomized controlled trial on knowledge retention."*
**Social Sciences & Humanities Open 12 (2025) 102287.** Universidade Federal do Rio de Janeiro, Brazil.
Received 11 Jul 2025 · accepted 25 Nov 2025 · online 29 Nov 2025. *(Local: `main.pdf`)*

**Pre-registered RCT**, **120 enrolled / 85 completed the retention test** (43 AI-assisted, 42 traditional; 70.8% follow-up, balanced). Brazilian business-administration undergraduates learning AI/ML concepts. 62% were already frequent ChatGPT users; 0% were novices. Random assignment:
ChatGPT as study aid vs traditional non-AI study. Retention measured by a **surprise test at 45 days**.

| Retention test (45 days later) | Score |
|---|---:|
| Studied traditionally | **68.5% correct** |
| Used ChatGPT | **57.5% correct** |

**t(83) = −3.19 · p = .002 · Cohen's d = 0.68**

**Why this is the strongest single study in the set:** pre-registered hypotheses, random assignment,
and a **delayed surprise assessment 45 days out** — not an exit quiz. The authors deliberately built
for ecological validity: real course topics, naturalistic tool access. Framed through cognitive
offloading and **desirable difficulties** — the effort *is* the mechanism, and AI removes it.

✅ **Resolved 2026-09-06:** `t(83)` because df = 85 − 2. The 68.5 / 57.5 figures are group means (6.85 / 5.75) on a 10-point scale. Subgroup: technical topics **d = 0.92**, ethics/society **d = 0.45** (difference n.s., Q = 2.84, p = .42). Prior AI experience did **not** moderate (r = 0.18, p = .10).

### 2.2 Fan, Y., Tang, L., Le, H., Shen, K., Tan, S., Zhao, Y., Shen, Y., Li, X. & Gašević, D. (2025)
*"Beware of metacognitive laziness: Effects of generative artificial intelligence on learning
motivation, processes, and performance."* **British Journal of Educational Technology**, 56:489–530.
DOI `10.1111/bjet.13544`

Randomized lab experiment, **117 university students**, writing task, four arms: **ChatGPT · human
expert · writing-analytics tools · no tool.**

- **ChatGPT group outperformed on essay score improvement.**
- **Knowledge gain and transfer: not significantly different.**
- Post-task intrinsic motivation: no difference between groups.
- Self-regulated learning processes: significantly different in frequency *and sequence*.

**Coins "metacognitive laziness"** — offloading the *monitoring and evaluation of your own thinking*,
not just the task. Better artifact, unchanged person. **This is the video's thesis in one study.**

### 2.3 Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö. & Mariman, R. (2025)
*"Generative AI without guardrails can harm learning: Evidence from high school mathematics."*
**PNAS** 122(26):e2422633122, 25 Jun 2025. DOI `10.1073/pnas.2422633122` · open at PMC12232635

RCT, **~1,000 students**, ~50 classes, grades 9–11, Turkey, four 90-minute sessions.

| | During practice | After AI removed |
|---|---:|---:|
| **GPT Base** *(unguarded — Category B)* | **+48%** | **−17% vs control** *(significant)* |
| GPT Tutor *(guardrailed — Category A)* | **+127%** | indistinguishable from control |

**The keystone.** One experiment containing both categories, with opposite outcomes. If the video
proves only one thing, prove this.

### 2.4 Strömberg, D., Lei, V. & Wu, Y. (2026) — scale and duration
*"The Generative AI Learning Penalty: Evidence from Chinese Secondary Education."*
**CEPR Discussion Paper DP21577**, 2 Jun 2026 · SSRN 6977138 · RePEc cpr/ceprdp/21577

**26,811 students**, grades 7–12, one county (~1M), **30 months**, 9 subjects.

| Measure | Change |
|---|---:|
| Homework scores | **+18%** |
| Homework completion time | **−30%** (64 → 45 min) |
| Monthly exams, at 6 months | **−20%** |
| High school entrance exam | **−24%** |
| College entrance exam | **−18%** |

Social sciences ≈ −27% · STEM −22% · English −17% · Chinese −9%.
**Full penalty emerges only after ~2 years** — which is why nobody caught it.
**Hardest hit: junior students, high achievers, and boys.** Dose: <1 hr/wk ≈ 5% loss; >5 hr/wk ≈ 30%.
**~80% of users** show the outsourcing fingerprint — *"exceptionally short homework completion time
coupled with high homework scores."*

**Effect sizes in SD:** monthly exams **1.4 SD** · Zhongkao **1.5 SD** · Gaokao **1.3 SD**.

⭐ **THE COUNTERFACTUAL I MISSED (added 2026-09-06):** AI users who spent **as much time on homework
as non-users** achieved **similar exam scores** — despite higher homework scores confirming they used
AI — and were **not differentially selected on prior achievement.** The escape hatch is inside the
bleakest study in the set.

**And it is improving:** the estimated penalty fell from ~25% (early 2023) to ~16% (June 2025).
Reported AI use rose from ~0 in 2022 to ~80% by June 2025.

⚠️ **Not an RCT — but a difference-in-differences design exploiting staggered adoption**, which is a
genuine causal design. Do **not** describe it as merely observational. It remains a **discussion
paper, not yet peer-reviewed.** Say that on camera.

### 2.5 Shen, J. H. & Tamkin, A. (2026) — the one that leaves school ⭐
*"How AI Impacts Skill Formation."* **arXiv 2601.20245v2**, dated **3 February 2026**.
Judy Hanwen Shen (Anthropic Fellows Program) · Alex Tamkin (Anthropic). *(Local: `2601AIImpactsSkill.pdf`)*

Randomized experiment — developers gaining mastery of a **new asynchronous Python library**, with and
without AI assistance.

**n = 52** crowd-recruited working developers (26 per arm), paid $150, ages ~25–35, ≥1 yr Python,
weekly coders, none had used the **Trio** async library before. Quiz: **14 questions, 27 points**, no
AI allowed. **Pre-registered** (osf.io/w49e7).

**Result as the paper states it: a 4.15-point difference on the 27-point quiz — "a 17% score
difference or 2 grade points." Cohen's d = 0.738, p = 0.01.** Controlling for warm-up time,
d = 0.725, p = 0.016.
**Task time: 23.0 vs 24.8 min, p = 0.391 — not significant.**

⚠️ **The ~50% / ~65% figures I first recorded were read off Figure 1 and are approximate — do not
put them on screen. Use the paper's own 4.15 / 27 framing.**

**Read that second line again.** There was no speed gain to trade for the lost skill. Participants
spent the saved time talking to the assistant — some asked up to 15 questions, or spent **over 30% of
total task time composing queries.**

#### The six usage patterns — the best single chart in the whole evidence base

| Pattern | Time | Quiz | Preserves learning? |
|---|---:|---:|---|
| **Generation-Then-Comprehension** | 24 min | **86%** | ✅ |
| **Hybrid Code-Explanation** | 24 min | **68%** | ✅ |
| **Conceptual Inquiry** | 22 min | **65%** | ✅ |
| AI Delegation | **19.5 min** | **39%** | ❌ |
| Progressive AI Reliance | 22 min | **35%** | ❌ |
| Iterative AI Debugging | 31 min | **24%** | ❌ |

⚠️ **Caveat that must be said on camera: 26 people in the AI arm, six patterns — roughly four per
cell.** This is a descriptive breakdown, not the study's statistical claim. The 17% is the finding.

**The fastest pattern is the second-worst.** AI Delegation finishes in 19.5 minutes and scores 39%.
Generation-Then-Comprehension takes 24 minutes and scores **86%** — 4.5 minutes more for **more than
double** the understanding.

**Why this matters most for your channel:** it isn't about children. It's adults, at work, learning a
tool — every person watching. **This is the study that makes it a video about the viewer**, and the
six patterns turn an abstract warning into something a viewer can locate themselves in.

---

## 3. What the five have in common

| Study | Design | Population | n |
|---|---|---|---:|
| Barcaui 2025 | RCT | undergraduates | 120 |
| Fan et al. 2025 | randomized lab | university students | 117 |
| Bastani et al. 2025 | field RCT | high schoolers (TR) | ~1,000 |
| Strömberg et al. 2026 | 30-month panel | secondary (CN) | 26,811 |
| Shen & Tamkin 2026 | randomized | **professional developers** | TBD |

Different countries, different ages, different subjects, three different designs — **the same
signature every time: the output improves, the person does not.**

### The convergence worth putting on screen

Two independent studies, different continents, different populations, different tasks, different
measures — and nearly the same effect size:

| | Population | Task | Effect |
|---|---|---|---:|
| **Barcaui 2025** | Brazilian undergraduates | AI/ML concepts, 45-day retention | **d = 0.68** |
| **Shen & Tamkin 2026** | Developers | new Python library, skill quiz | **d = 0.738** |

**d ≈ 0.7 is a medium-to-large effect.** Independent replication at that magnitude is the strongest
claim this video can honestly make.

**And the escape hatch replicates too.** Bastani: guardrails eliminate the harm. Shen & Tamkin: three
of six interaction patterns preserve learning. Fan et al.: engage metacognitively instead of following
the output. **The tool is not the variable. Whether you did the thinking is the variable** — and by
the CEPR fingerprint, ~80% of people don't.

---

## 4. The verdict

**Not "AI is bad for learning."** The meta-analysis disproves that, and asserting it would be exactly
the kind of claim this channel exists to check.

> **AI built to teach you works. AI used to finish the task leaves you with a better artifact and an
> unchanged mind — and almost everyone is using it the second way.**

That is a verdict that lands in the middle, is defensible against every source in this file, and
corrects a credentialed public claim without dunking on it. The ideal first video.

## 5. Andrew Ng — corrected 2026-09-06 (Terry's read, and he is right)

**I had this wrong.** I wrote that Ng's claim was "overstated." Re-reading the transcript, **Ng makes
the exact task-versus-teaching distinction himself** — and, more than that, he *lives both sides of
it simultaneously.* That is a far better use of him than catching him out.

**He states the distinction (14:55):**
> *"when you ask AI to do work for you you're cognitive offloading to AI... but human retention is
> much worse... I'm not saying there's no way to use it in a way that is good for learning. I think
> there are ways to use that good for learning."*

And again at 15:25, with the qualifier that does all the work:
> *"we should stop thinking of AI as helpful for learning — **at least the vast majority of ways that
> the vast majority of people are using AI models today.**"*

**He is Category B's own casualty (15:25):**
> building a project, *"how does this front end backend component work, whatever — give me the answer,
> get the job done. It was fantastic. But six months later I don't remember the answer. When I need to
> redo that front end backend component, I ask AI again."*

**And he is Category A's builder (15:56):** LearnVector, **$100M from Coursera**, explicitly
*"much more one-to-one than one-to-many"* — AI built to teach.

### Why this is the better frame

The same man, in the same interview: **using AI for tasks and losing the skill, while founding a
company to use AI for teaching.** He is not confused and he is not overstating — he is compressed.
The distinction is in his answer; it just doesn't survive being quoted.

**That is itself on-theme.** The nuance that dies in transmission is exactly what this channel exists
to restore. So the video does not correct Ng — **it finishes his sentence, with the five citations he
didn't have to hand.**

**Terry's addition (2026-09-06):** make the task-versus-teaching distinction explicit in the video,
using Ng living both sides as the demonstration. Agreed — it is the cleanest possible way to teach the
distinction, because it is a person rather than a taxonomy.

## 6. Open work

- [ ] **Shen & Tamkin sample size** — not on the abstract page. Pull the PDF.
- [ ] **Barcaui** — confirm population and country from the paper, not the abstract listing.
- [ ] **CEPR DP21577 full PDF** — read the identification strategy before defending causality.
- [ ] Optional third-category color, clearly labeled as **survey, not causal**: Gerlich 2025 (n=666,
      AI use ↔ critical thinking, mediated by offloading).
- [ ] Candidates not yet verified: *"Learning by Chatting?"* (arXiv 2606.11669); *"Working with Large
      Language Models"* (Behav. & Inf. Tech. 2026); *"AI-overdependence and human cognitive decline"*
      (2026).

## 7. Rules carried in

- **Runtime 30–50 min** — in-lane precedent 54.4 min at 23.73×; 75 min at 4.99M views.
- **Every on-screen number traces to a PDF that has been opened.**
- **The verdict is discovered past 40% of runtime, not announced.**
- **Candidate reversal:** the CEPR finding that **high achievers are hit hardest.** The intuition is
  that AI rescues weak students and the strong are fine. The data says the opposite.
