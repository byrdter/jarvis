# Fireship — channel teardown

**Measured 2026-08-22.** `@Fireship` · **4,250,000 subs** · 783 long uploads · **638.8M lifetime views**
· first upload 2017-08 · created by Jeff Delaney · dev-education + tech news.

Method: full catalog pull (`yt-dlp`, 783 items); **exact** upload dates + view/like/comment counts for
**495 of 783** — 100% of 2024–2026, 99% of 2023, 87% of 2022, 30% of 2021, 2–16% before (the pull was
rate-limited by YouTube; see §7); **approximate** dates for the full 783 via
`--extractor-args youtubetab:approximate_date`, **validated against the exact set and found unreliable
— see §0.1**. Three `teardown.py` transcript teardowns, scene-detection density on two downloaded
videos, permutation tests (20,000 resamples) age-residualised on the exact subset. Raw data in
`tools/raw/fireship/`, teardowns in `tools/teardowns/{x7X9w_GIm1s, Nl7aCUsWykg, pEfrdAtAmqk}.md`.

---

## 0. The one-line finding

> **Fireship's famous short runtime is not why it wins — and its signature format is now its worst.**
> Pooled, sub-5-minute videos look **1.79× better**; on exact dates, within era, that becomes
> **0.91× — slightly negative** — and the age-residualised test is **null (p = 0.20)**. Meanwhile
> *"X in 100 Seconds"* — the format the channel is known for — peaked at **1.34× in 2022**, halved to
> **0.52× in 2024**, and has been deliberately cut from **55% to 1–5%** of output.

The channel is a **conveyor belt** (p90/median **1.71–1.78** since 2023), not an outlier machine, and
it is currently executing a **format succession** in the open.

### 0.1 A method warning, paid for in this teardown

`yt-dlp`'s `approximate_date` gave dates for all 783 in one call. Cross-checked against 168 videos
where both approximate and exact dates existed:

- **exact match: 0%** · within 1 day: 6% · within 7 days: 24%
- median absolute error **23 days**, **max 225 days**
- **year-bin disagreement: 18%**

They are usable for a coarse trajectory and nothing else. **Every headline claim below is verified on
the exact-date subset.** Tables built on approximate dates are labelled as such. Had this not been
checked, the 2026 row alone would have been read as fact — it disagreed with the exact data until
confirmed independently (§3.1).

---

## 1. The numbers

### 1.1 Era structure — EXACT dates 2021+, approximate before

**Rebuilt 2026-08-22.** Exact-date coverage by year: 2026/2025/2024 **100%**, 2023 **99%**, 2022
**87%**, 2021 **30%**, 2017–2020 **2–16%** (§7). Rows below 2021 remain approximate and are the
weakest evidence here.

| year | n (exact) | med views | p90 | **p90/med** | med runtime | % <5 min |
|---|---:|---:|---:|---:|---:|---:|
| 2019 | 11 | 189,883 | 400,773 | 2.11 | 10.0m | 0% |
| 2020 | 12 | 634,155 | 1,529,497 | 2.41 | 8.3m | 42% |
| 2021 | 44 | 1,058,582 | 3,060,471 | 2.89 | 4.0m | 50% |
| **2022** | 99 | 798,769 | 2,627,365 | **3.29** | 3.1m | 68% |
| **2023** | 86 | 962,382 | 1,747,157 | **1.82** | 3.8m | 78% |
| **2024** | 92 | 969,935 | 1,691,844 | **1.74** | 4.3m | 75% |
| **2025** | 82 | 950,880 | 1,621,805 | **1.71** | 4.2m | 83% |
| **2026** | 55 | 767,447 | 1,365,157 | **1.78** | 5.3m | **22%** |

The dispersion collapse is confirmed exactly: **3.29 (2022) → 1.71–1.82** and flat since. 2021 carries
the highest median in the catalog (1.06M) but is also the oldest cohort with real volume — that is
accumulation, not superiority.

#### Superseded — the original approximate-date table *(kept for provenance)*

| year | n | med views | p90 | **p90/med** | med runtime | % <5 min | uploads/mo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2017 | 41 | 54,000 | 110,000 | 2.04 | 5.3m | 44% | 3.4 |
| 2018 | 68 | 64,500 | 262,000 | 4.06 | 9.6m | 3% | 5.7 |
| **2019** | 77 | 104,000 | 814,000 | **7.83** | 9.9m | 13% | 6.4 |
| 2020 | 61 | 388,000 | 1,000,000 | 2.58 | 6.7m | 46% | 5.1 |
| 2021 | 80 | 734,500 | 1,900,000 | 2.59 | 8.3m | 41% | 6.7 |
| 2022 | 111 | 951,000 | 2,600,000 | 2.73 | 2.8m | 65% | 9.2 |
| 2023 | 97 | 819,000 | 1,700,000 | 2.08 | 3.6m | 74% | 8.1 |
| 2024 | 78 | 1,050,000 | 2,200,000 | 2.10 | 4.3m | 77% | 6.5 |
| 2025 | 115 | 939,000 | 1,600,000 | **1.70** | 4.3m | 79% | 9.6 |
| 2026 | 55 | 767,000 | 1,300,000 | **1.69** | 5.3m | 22% | 6.9 |

**2019 was the breakout year** — p90/median 7.83, the only genuinely outlier-shaped season in the
catalog. Everything after is progressively flatter.

### 1.2 The dispersion collapse — a third channel doing the same thing

p90/median on **exact** dates: **2.89 (2021) → 3.29 (2022) → 1.82 → 1.74 → 1.71 → 1.78.** The break is
sharp and lands in 2023.

| channel | p90/median (current era) | shape |
|---|---:|---|
| Snap Shift | **6.76** | outlier machine |
| **Fireship** | **1.71–1.78** | conveyor belt |
| Wall Street Millennial | 1.93 | conveyor belt |

Fireship is now **flatter than WSM** — the flattest distribution measured on any channel to date. Its
median outlier score is 0.162× (views ÷ subs), but at 4.25M subs that number is mostly a size
artifact and should not be compared to small-channel scores.

---

## 2. Runtime does NOT predict views — a textbook Simpson's reversal

This is the finding most likely to be misread from the outside, and the reason
`WSM-CHANNEL-TEARDOWN.md`'s "era-split before any analysis" rule exists.

| slice | dates | <5 min | ≥5 min | ratio |
|---|---|---:|---:|---:|
| **POOLED (all 783)** | mixed | 805,500 | 450,000 | **1.79×** |
| 2017–2019 (tutorial era) | approx | 50,500 | 86,500 | **0.58×** |
| **2022** | **exact** | 735,434 | 968,576 | **0.76×** |
| **2023–2026 (current)** | **exact** | 911,973 | 961,463 | **0.95×** |
| **2022–2026 combined** | **exact** | 870,811 | 961,463 | **0.91×** |

Pooled says short wins by 79%. Within era, measured on **exact** dates, the effect is not merely gone
— it is **slightly negative**: short videos run 0.91× the long ones across 2022–2026, and 0.76× in
2022 alone. The pooled number is an artifact of *when* long videos were made — the long ones are old
tutorials from when the channel was small.

**Verified independently on exact dates** (n=202, 2024-07 → 2026-08, log-views residualised on
log-age): <5 min mean residual **−0.034** vs ≥5 min **+0.056**; difference −0.090 log-units,
**permutation p = 0.1997. Null.**

> **Do not take "Fireship is short, therefore short works" from this channel.** Its own catalog says
> runtime is neutral. Short is a *production* choice — it lets them ship ~8/month — not a
> distribution lever.

---

## 3. The format succession — a signature format with a measured lifecycle

### 3.1 *"X in 100 Seconds"* has gone from the engine to a liability

**Rebuilt on EXACT dates 2026-08-22** after the metadata pull reached 495/783 (2021+ coverage
30–100%; see §7).

| year | share of output | med views (100 Sec) | med views (everything else) | **ratio** |
|---|---:|---:|---:|---:|
| 2021 | 55% | 1,165,742 | 1,002,684 | 1.16× |
| **2022** | 39% | 955,362 | 713,090 | **1.34×** ← peak |
| 2023 | 17% | 1,045,975 | 954,956 | 1.10× |
| **2024** | 15% | 605,599 | 1,154,928 | **0.52×** ← collapse |
| 2025 | 1% | 517,803 | 962,081 | 0.54× |
| 2026 | 5% | 470,891 | 782,330 | 0.60× |

> **CORRECTION to the first version of this document.** It reported a **2.26× peak in 2020** from
> approximate dates. That row rested on **13% exact coverage of 2020** and was **overstated**. On
> exact dates the measured peak is **1.34× in 2022**. The *shape* — rise, parity, collapse — and the
> collapse year (2024) are unchanged, but the magnitude was wrong and the peak was a year late.

On the exact-date subset, era-controlled and age-residualised, *"in 100 Seconds"* measures
**0.58×, p = 0.0001** — the single strongest signal in the whole title analysis, and it is
**negative**.

**The format held ~1.1–1.3× through 2023, then halved in 2024 and stayed there. They read it and
switched.** Output share fell 55% → 1–5%.

### 3.2 What replaced it

The house style is now a **trailing-ellipsis topical headline**: *"Big Tech in panic mode... Did
DeepSeek R1 just pop the AI bubble?"*, *"This free Chinese AI just crushed OpenAI's $200 o1 model..."*

Ellipsis titles went **1% → 91%** of output and measure **1.11×, p = 0.037** era-controlled. A small
lift on a very large base — this is a *floor* mechanic, not a ceiling one, exactly like WSM's
accusation frame.

| formula (exact subset, n=202, age-residualised) | n | lift | p |
|---|---:|---:|---:|
| **"X in 100 Seconds"** | 13 | **0.58×** | **0.0001*** |
| ellipsis "…" / "..." | 156 | 1.11× | 0.037* |
| superlative (insane/crazy/panic/god-tier) | 11 | 1.11× | 0.044* |
| named company/product | 71 | 1.14× | 0.053 |
| question title | 15 | 1.09× | 0.186 |
| "new"/"just"/recency | 63 | 1.04× | 0.229 |
| numbered listicle | 10 | 0.92× | 0.947 |

### 3.3 The 2026 shift is real, verified, and free

Confirmed on **exact** dates, not approximate:

| | 2025 (n=82) | 2026 (n=55) |
|---|---:|---:|
| median runtime | 4.2m | **5.3m** |
| % under 5 min | **83%** | **22%** |
| median views | 950,880 | 767,447 |
| **age-residualised mean** | **−0.005** | **+0.019** |

Fireship roughly **doubled its share of longer videos in a single year, and performance did not
move.** The raw median dip (950K → 767K) is entirely an age artifact — the 2026 cohort's median age is
110 days vs 438. Age-normalised the two years are indistinguishable.

---

## 4. The craft layer — measured

### 4.1 It is the fastest-talking channel we have measured

| channel | wpm |
|---|---:|
| **Fireship — "DeepSeek" (news format)** | **236** |
| **Fireship — "God-Tier Developer Roadmap"** | 210 |
| **Fireship — "Python in 100 Seconds"** | 191 |
| Modern MBA | 178 |
| Snap Shift | 150 |

236 wpm is roughly **1.6× Snap Shift's rate**. Combined with near-zero filler, the information
density per minute is the channel's actual signature — far more than the runtime.

### 4.2 Density is above our own target; hard cuts are not

Scene detection on two downloaded videos:

| video | change-events/min @0.02 | hard cuts/min @0.25 | avg shot |
|---|---:|---:|---:|
| Python in 100 Seconds (2:23) | **72.0** | 4.2 | 14.3s |
| DeepSeek / Code Report (3:36) | **89.7** | 19.2 | 3.1s |

Our `CONDUIT-VISUAL-SYSTEM.md` target is **45–60 change-events/min**; Fireship runs **72–90**. But note
the split: the evergreen format has only **4.2 hard cuts/min** and a 14-second average shot — its
density is almost entirely **within-frame** (code scrolling, terms appearing, highlights landing), not
cutting. That is precisely the "prefer within-beat motion over rapid cutting" principle we already
hold, executed harder than we execute it.

### 4.3 Two different businesses under one brand

**Evergreen / reference — no hook at all.** *Python in 100 Seconds* opens:

> *"python — a high-level interpreted programming language famous for its zen-like code…"*

A dictionary definition. No adversary, no curiosity gap, no withheld payoff — it violates every rule
in `RETENTION-AND-HOOKS.md` §2–§3, and it has 3.0M views. **Because it serves SEARCH intent.** The
title is a query people type; the promise is the title; a gap would be friction. This is a genuine
boundary condition on our hook doctrine: **hook rules govern browse/suggested traffic, not search
traffic.**

**Topical / news — hook-saturated.** *DeepSeek* opens with an adversary in sentence one, a named
victim, and a stake:

> *"last week Chinese company DeepSeek shocked the world when they walked right over OpenAI's moat by
> releasing the open-source R1 model… not only does it beat their $200 o1 reasoning model…"*

Register is aggressively opinionated and slangy — *"in order for the grift to keep on grifting"*,
*"my vibe test"*, *"normies"*. Nothing like our conduit register, and not portable to it.

### 4.4 Visual vocabulary — real captures, annotated, cut against memes

From frame inspection of the DeepSeek build: the actual DeepSeek benchmark chart from the paper, the
real NVDA price chart mid-crash, Sam Altman's actual tweet, a Bloomberg article, a Tom's Guide
article, real Reddit comments, the ChatGPT pricing page, the DeepSeek chat UI.

Two devices worth stealing:

1. **Annotation on top of a real capture** — a hand-drawn arrow and the caption *"CHINESE MATH
   SUPREMACY"* scrawled over the genuine benchmark chart. The evidence stays real; the editorial
   lives in the annotation layer on top. This is our annotation-HUD component with a joke in it.
2. **Big overlay numerals on the capture** — *"< $10 million"*, *"−$6,000,000"*, *"671B"* — the number
   at display size over the artifact rather than retyped into a text card.

Generated imagery **is** present (an AI-composited Altman-as-Napoleon, celebrity-head reaction
composites) but strictly as **memes/punctuation**, never as a substitute for evidence. That is the
opposite of the Snap Shift posture, where the imagery *is* the substance.

---

## 5. What transfers to us

### TAKE

1. **Watch your own format for decay, and be willing to kill it.** This is the sharpest contrast in
   the corpus. Snap Shift found its best lever (two-clause titles), drifted off it under volume
   pressure, and its median fell. Fireship watched its signature format decay from 1.34× (2022) to
   parity (2023) to 0.52× (2024) **and deliberately replaced it**, cutting output share 55% → 1–5%. **A format is not an
   identity; it is a position with a half-life.** Nothing in our tooling currently tracks the decay of
   a format we own — `outlier-ratchet.py` watches other channels, not our own formats.
2. **Annotation-on-capture** (§4.4) — draw the editorial on the real artifact instead of building a
   separate card. Cheap, keeps the evidence real, and carries voice.
3. **Density via within-frame motion, harder than we do it.** 72/min with only 4.2 hard cuts/min is
   the exact shape we say we want; we target 45–60. Worth raising our floor on evergreen material.

### DO NOT TAKE

4. **Not the short runtime.** Measured on their own catalog, runtime is **null** (p=0.20). The pooled
   1.79× is a Simpson's artifact. Short serves their *cadence* (~8 uploads/month), not their reach —
   and we have an 8-minute monetisation floor they do not.
5. **Not the hookless open — unless the traffic is search.** *Python in 100 Seconds* works because the
   title is a search query. Our lane is browse/suggested, where §2–§3 still governs. **Do not
   generalise "Fireship doesn't hook" into "hooks don't matter."**
6. **Not the register.** "The grift keeps grifting" is a native-voice channel with a personality
   attached to a real named person. We are faceless and evidence-register; borrowing the slang would
   read as costume.

### THE STANDING WARNING, again

Same as Snap Shift §3.1: **this measures the click, not the hold.** Every number here is
views-derived. A 236-wpm delivery is plainly a retention device, but nothing in this method can prove
that — only the shape of what got clicked.

---

## 6. Tested and rejected — do not re-run

- **Runtime as a driver** — pooled 1.79×, within-era 0.95×, exact-date test p=0.1997. Null.
- **`approximate_date` as a substitute for exact dates** — 0% exact match, 18% year-bin error. Coarse
  trajectory only.
- Question titles (1.09×, p=0.19), recency markers (1.04×, p=0.23), numbered listicles (0.92×, p=0.95).
- Named company/product (1.14×, p=0.053) — suggestive, does not clear the bar, and is 35% of output.
- Reading the 2025→2026 median dip as decline — it is entirely age; residualised, the years are
  identical.

## 7. Data completeness — and the one number this exercise corrected

**Resolved 2026-08-22.** The exact-date pull finished at **495 / 783**. It exited 0, but **288 videos
failed** — 287 to `This content isn't available, try again later. The current session has been
rate-limited by YouTube`, 1 to an age gate. **A zero-exit yt-dlp run is not a complete run**; the
error count has to be read from the log.

The failures are **strongly era-biased**, because the id list is chronological and the throttle hit
partway through:

| year | exact coverage |
|---|---:|
| 2024 / 2025 / 2026 | **100%** |
| 2023 | 99% |
| 2022 | 87% |
| 2021 | 30% |
| 2017–2020 | 2–16% |

So §1.1 and §3.1 are now exact from 2021 on, and §2's within-era test is exact from 2022 on. **Only
the 2017–2020 rows still rest on approximate dates**, and they are flagged in place. A retry of the
missing 288 with `--sleep-requests 3` is queued.

**What re-running on exact dates actually changed:** the *"100 Seconds"* peak moved from a claimed
**2.26× (2020)** to a measured **1.34× (2022)** — the original rested on 13% coverage of 2020 and
overstated the magnitude by ~70%. The collapse year (2024), the direction, and every headline
conclusion held. The within-era runtime result got *stronger* against short (0.95× → 0.91×, and 0.76×
in 2022). **This is why §0.1 exists:** approximate dates were adequate for the shape and wrong on the
number, exactly as their 23-day median error predicts.
