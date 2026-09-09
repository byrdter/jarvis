# V01 — CLAIM-SOURCE MAP (PIPELINE Step 0d)

> ## ⚠️ REWRITTEN 2026-09-08 — the script changed register
>
> The script no longer walks study by study. It states **five findings about the viewer**, with the
> evidence in passing. **Every statistic was removed from the VO** — no p-values, no effect sizes, no
> confidence intervals, no sample sizes, no journal names spoken. About **seven numbers** survive in
> the whole video.
>
> **That makes this file more important, not less.** It is now the only place the full evidence lives
> in prose, and it is where anyone checking the video's claims should be sent. The scene numbers below
> are the NEW ones (9 scenes).
>
> | old | new |
> |---|---|
> | 01 cold open · 02 not-about-school | **01** cold open (Ng's loss → Terry's) · **02** the line nobody draws |
> | 03 Barcaui · 04 Bastani · 05 CEPR | **03** Finding 1 · **04** Finding 2 *(+ the single caveat)* · **05** Finding 3 |
> | 06 reversal · 07 Shen & Tamkin | **06** Finding 4 (de-skilling) · **07** Finding 5 (the turn) |
> | 08 distinction · 09 verdict · 10 CTA | **08** verdict · **09** CTA (HyperFrames, no presenter) |
>
> **The six sources and every verified figure below are unchanged** — only where they appear moved.

Every spoken or on-screen factual claim, mapped to its source. **Confidence** is about the *claim as
stated in the script*, not the quality of the paper.

| | |
|---|---|
| ✅ **VERIFIED** | Read directly from the PDF or the publisher's own abstract |
| 🟡 **DERIVED** | True but restated/rounded by me — check the phrasing survives |
| 🔵 **TERRY** | Personal or process claim only Terry can confirm |
| ⏱ **TIMING** | Correct today; breaks if the recording date or edit length moves |

## The six sources

| # | Citation | Local file |
|---|---|---|
| S1 | **Barcaui, A. (2025).** "ChatGPT as a cognitive crutch: Evidence from a randomized controlled trial on knowledge retention." *Social Sciences & Humanities Open* 12:102287. UFRJ, Brazil. | `main.pdf` |
| S2 | **Fan, Y., Tang, L., Le, H., Shen, K., Tan, S., Zhao, Y., Shen, Y., Li, X. & Gašević, D. (2025).** "Beware of metacognitive laziness…" *British Journal of Educational Technology* 56:489–530. DOI 10.1111/bjet.13544. | `Metacognitive09_05_2026.pdf` |
| S3 | **Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö. & Mariman, R. (2025).** "Generative AI without guardrails can harm learning…" *PNAS* 122(26):e2422633122. | `GenertiveAINoGuardrails.pdf` |
| S4 | **Strömberg, D., Lei, V. & Wu, Y. (2026).** "The Generative AI Learning Penalty: Evidence from Chinese Secondary Education." CEPR DP21577, 2 Jun 2026. | `GenerativeAILearningPenalty.pdf` |
| S5 | **Shen, J. H. & Tamkin, A. (2026).** "How AI Impacts Skill Formation." arXiv 2601.20245v2, 3 Feb 2026. | `2601AIImpactsSkill.pdf` |
| S6 | **Zhu, Y., Liu, Q. & Zhao, L. (2025).** "Exploring the impact of generative AI on students' learning outcomes: a meta-analysis." *Education and Information Technologies* 30:16211–16239. | `MetaStudy2025.pdf` |
| NG | Andrew Ng interview, *Silicon Valley Girl*, 2026-08-28, 37.9 min. | `ng-quotes-VERBATIM-whisper.txt` |

---

## Scene 01 — cold open

| Claim | Source | Conf |
|---|---|---|
| "Frankly, AI models are terrible for learning" | NG @ 14:09 | ✅ Whisper-verified |
| "I don't know **if** I've said this publicly, but I think it's true" | NG @ 14:04 | ✅ Whisper-verified |
| "the data is very clear" / "all the data that's coming out" / "more and more studies are coming out" | NG @ 14:25–14:43 | ✅ Whisper-verified |
| Co-founded Coursera; built founding Google Brain team; ~8M taught | Ng public record + interview intro | ✅ |
| Ng names no paper, author or number | Full transcript, 13:35–16:05 | ✅ Verified by absence |
| Interviewer puts the **$100M from Coursera** to him; he confirms | NG @ 15:55–16:02 — **interviewer states it** | ✅ Corrected 09-06 |
| "Nine days ago" | Interview 2026-08-28; script written 09-06 | ⏱ **Recompute on recording day** |
| "It took a week" | Terry's own research window | 🔵 |
| Six studies · two RCTs · one pre-registered · 26,811 / 30 months · meta-analysis of 26 trials | S1–S6 | ✅ |
| "Four found harm. Two found the opposite." | Harm: S1,S2,S3(Base),S4,S5 = 5. Helps: S6, S3(Tutor). | 🟡 **S3 appears on both sides — deliberate, and Scene 06 explains it. Verify the line still reads honestly after the edit.** |

## Scene 02 — why this isn't about school

| Claim | Source | Conf |
|---|---|---|
| Terry's lost configuration knowledge, "maybe two years ago" | Personal | 🔵 **Terry's to adjust to what's true** |
| Ng's front-end/back-end component, forgotten at six months | NG @ 15:26–15:40 | ✅ Whisper-verified (paraphrased — the captions garble the lead-in; do not quote that clause verbatim) |
| One study is about professionals, not students | S5 | ✅ |

## Scene 03 — Barcaui, and Fan

| Claim | Source | Conf |
|---|---|---|
| UFRJ Brazil; *Soc. Sci. & Humanities Open*; Nov 2025 | S1 header | ✅ |
| 120 business-administration undergraduates, randomized 60/60 | S1 Fig. 3 + Table 1 | ✅ |
| **85 completed** the retention test — 43 AI, 42 traditional; 70.8% follow-up | S1 Fig. 3 + §Missing data | ✅ **Corrected 09-06** |
| Surprise test at **45 days**, no prior warning | S1 §8.5–8.6 | ✅ |
| Traditional **68.5%** vs ChatGPT **57.5%** | S1 Table 2 (means 6.85 / 5.75 on a 10-point scale) | ✅ |
| t(83) = −3.19 · p = .002 · d = 0.68 · CI [0.24, 1.12] | S1 Table 2 | ✅ |
| Cohen's d bands: .2 small / .5 moderate / .8 large | Standard convention (Cohen 1988) | ✅ |
| "Educational interventions… routinely land in the small range" | General knowledge — **softened 09-06** from an unsourced "point two / half don't replicate" claim | 🟡 **Deliberately vague. Do not re-sharpen without a citation.** |
| Pre-registered | S1 abstract + §2 | ✅ |
| Desirable difficulties, "since the nineteen-nineties" | Bjork & Bjork; S1 frames the study this way | ✅ **Corrected 09-06** from "forty years old" |
| **Fan et al.:** 117 students, randomized lab, 4 arms, essay task | S2 abstract | ✅ |
| ChatGPT group better essay scores; knowledge gain **and transfer not significantly different** | S2 abstract | ✅ |
| Coined "metacognitive laziness" | S2 title + abstract | ✅ |

## Scene 04 — Bastani (GPT Base)

| Claim | Source | Conf |
|---|---|---|
| PNAS, June 2025; ~1,000 students; ~50 classes; grades 9–11; four 90-min sessions; Turkey | S3 | ✅ |
| GPT Base **+48%** during practice | S3 | ✅ |
| After access removed: **−17% vs control**, statistically significant | S3 | ✅ |
| Authors' word "crutch" | S3 | ✅ |
| Third arm exists, withheld until Scene 06 | S3 | ✅ Disclosed on camera — deliberate structure, not concealment |

## Scene 05 — CEPR

| Claim | Source | Conf |
|---|---|---|
| 26,811 students, grades 7–12, one county ~1M, 30 months, 9 subjects | S4 abstract | ✅ |
| **Difference-in-differences**, staggered adoption — not an RCT | S4 abstract + §1 | ✅ **Corrected 09-06** |
| Discussion paper, **not peer-reviewed** | CEPR DP series | ✅ **Mandatory on camera** |
| Homework **+18%**; time **−30%**, 64 → 45 min | S4 §1 | ✅ |
| Monthly exams **−20%** = **1.4 SD** | S4 §1 | ✅ |
| Zhongkao **−24%** (1.5 SD); Gaokao **−18%** (1.3 SD) | S4 §1 | ✅ |
| Full penalty emerges after **~2 years** | S4 §1 | ✅ |
| **81%** show the outsourcing fingerprint (short time + high scores) | S4 §1 | ✅ |
| The time-matched counterfactual: AI users who kept non-user hours had comparable exam scores, and were **not** differentially selected on prior achievement | S4 §1 | ✅ |
| Penalty fell ~25% (early 2023) → ~16% (Jun 2025) | S4 §1 | ✅ |
| High achievers, junior students and boys hit hardest | S4 §1 | ✅ |

## Scene 06 — the reversal

| Claim | Source | Conf |
|---|---|---|
| GPT Tutor: teacher-designed hints, withholds answers | S3 | ✅ |
| GPT Tutor **+127%** during practice | S3 | ✅ |
| GPT Tutor after removal: **statistically indistinguishable from control** | S3 | ✅ |
| Meta-analysis: **5,887** screened → **26** RCTs; overall **g = 0.392** | S6 abstract | ✅ |
| "the last twelve minutes" | Position-dependent | ⏱ **Recheck against the assembled edit** |

## Scene 07 — Shen & Tamkin

| Claim | Source | Conf |
|---|---|---|
| Anthropic; arXiv 2601.20245; 3 Feb 2026 | S5 header | ✅ |
| **52** developers, 26/26, crowd-recruited, $150, ages ~25–35, weekly Python coders | S5 §5.2.1 + Table 1 | ✅ **Corrected 09-06** |
| Library is **Trio**, none had used it | S5 §4 | ✅ |
| Quiz: **14 questions, 27 points**, no AI | S5 §4.2 | ✅ |
| **4.15-point difference → "17% or 2 grade points"**, d = 0.738, p = 0.01 | S5 §5.2.2 | ✅ **Use this framing, not "~50% vs ~65%"** |
| Pre-registered (osf.io/w49e7) | S5 footnote 2 | ✅ |
| Task time 23.0 vs 24.8 min, **p = 0.391, not significant** | S5 Fig. 1 | ✅ |
| Up to 15 questions asked; >30% of task time composing queries | S5 §1.1 | ✅ |
| Six patterns w/ times and scores (86/68/65/39/35/24) | S5 Fig. 1 right panel | 🟡 **Read off the figure. ~4 per cell — descriptive only. The caveat is scripted; do not cut it.** |
| Barcaui d=0.68 vs Shen & Tamkin d=0.738 as independent replication | S1 + S5 | ✅ |
| "the last twenty minutes" | Position-dependent | ⏱ **Recheck against the edit** |

## Scene 08 — the distinction

| Claim | Source | Conf |
|---|---|---|
| Full quote: *"We should stop thinking of AI as helpful for learning. At least the vast majority of ways that the vast majority of people are using AI models today is absolutely terrible for learning."* | NG @ 15:42–15:52 | ✅ **Whisper-verified. The captioned version is wrong.** |
| *"It's just so clear that LLMs, as they are most commonly used, are terrible for learning."* | NG @ 15:11 | ✅ Whisper-verified |
| *"I'm not saying there's no way to use it in a way that is good for learning…"* | NG @ 15:16 | ✅ Whisper-verified |
| "Six words in the middle" (*as they are most commonly used*) | Count | ✅ **Corrected 09-06** from "four words" |
| Terry's own near-miss with the truncated quote | Process, this session | ✅ True and documented in the corrections log |
| Ng is describing two different products, not contradicting himself | **Interpretation** | 🟡 **Framed as Terry's reading, not as fact. Keep it framed that way.** |

## Scene 09 — verdict

| Claim | Source | Conf |
|---|---|---|
| "Six studies. Two found it helps… four found harm." | S6 + S3(Tutor); S1,S2,S3(Base),S4,S5 | 🟡 **S3 counted on both sides — the split arms are explained in Scene 06** |
| **81%** outsourcing fingerprint | S4 | ✅ **Corrected 09-06** — was inconsistent with Scene 05 |
| 4.5 min / 39% → 86% on a **24-minute** task | S5 Fig. 1 | ✅ **Corrected 09-06** — was "twenty-minute task" |
| "The bill arrives two years later" | S4 (~2-year lag) | ✅ |

## Scene 10 — CTA

| Claim | Source | Conf |
|---|---|---|
| "Every number came from a paper I opened and read" | This map | ✅ — **and it is now literally true; keep it that way** |
| Six citations on screen with journals, dates, DOIs | The table at the top of this file | ✅ Build the endcard from it |

---

## What changed in the VO — read before recording

- **Spoken numbers, entire video:** *eight million · nearly half · twenty-six thousand · two years ·
  eighty-one percent · eighty-six against thirty-nine · four and a half minutes.* Nothing else.
- **Never spoken:** t-statistics, p-values, Cohen's d, confidence intervals, sample sizes, "randomized
  controlled trial", "pre-registered", "meta-analysis", and every journal name.
- **The caveat is now ONE paragraph**, in Scene 04, ending *"that's the last time I'll qualify it."*
  It still names the peer-review status of the Chinese paper out loud. **That line is not optional.**
- **Everything struck from the VO stays true and stays on screen** — the papers appear as document
  captures, and the six citations hold as the final frame of Scene 09.

## Pre-record checklist

1. ⏱ **Recompute "nine days ago"** to the actual recording date.
2. ⏱ **Recheck "the last twelve minutes" and "the last twenty minutes"** against the assembled edit.
3. 🔵 **Terry's anecdote in Scene 02** — make it true to what actually happened.
4. ✅ **Read all Ng quotes from `ng-quotes-VERBATIM-whisper.txt`**, never the caption transcript.
5. ⚠️ **Never cut:** the CEPR "not peer-reviewed" line (Scene 05) and the six-pattern small-sample caveat (Scene 07). Both are load-bearing for the channel's promise.
