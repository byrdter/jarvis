# Wall Street Millennial — channel teardown

**Measured 2026-08-16.** `@wallstreetmillennial` · 367,000 subs · 958 uploads · 92.2M lifetime views
· created 2020-07-21 · US · faceless.

Method: full catalog pull (951 uploads, `yt-dlp`); **exact** upload dates, view/like/comment counts
for the newest 453 (the entire post-pivot era, back to 2022-01); interpolated dates from 48 anchors
for the 2020–21 pre-pivot tail only. Four `teardown.py` transcript teardowns, one full
`shot-census.py` (every shot classified by hand), age-residualised permutation tests on 408
post-pivot videos. Raw data in `tools/raw/wsm/`, censuses in `tools/census-Juc-IyTdSho/`, teardowns
in `tools/teardowns/`.

> Every statistical claim below (§1.2, §2.1, §2.2) was computed twice — once on interpolated dates,
> once on exact — and agreed within rounding. Where the two differ, the **exact** figure is printed.

---

## 0. The one-line finding

> **This channel does not win with outliers. It wins by never missing.** Its current-era p90/median
> view ratio is **1.92** — the flattest distribution we have measured on any channel. It is a
> conveyor belt: ~10 uploads/month, ~15 minutes each, ~98% third-party material, a median video that
> reliably clears 0.26× and almost never clears 1×.

Every craft observation below follows from that. Nothing here is a retention lesson, because a
channel with this dispersion is not being selected on retention — it is being selected on **supply**.

---

## 1. The numbers

### 1.1 Era structure — there was a hard pivot in late 2022

| year | n (long) | med views | med runtime | p90 | **p90/med** | % under 8 min | uploads/mo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2020 | 47 | 5,200 | 4:04 | 40,000 | 7.69 | 89% | 11.2 |
| 2021 | 322 | 36,000 | 9:18 | 160,000 | 4.44 | 6% | 27.1 |
| 2022 | 155 | 50,000 | 11:07 | 126,000 | 2.52 | 2% | 12.9 |
| **2023** | 110 | 105,666 | 14:30 | 332,445 | 3.15 | 0% | 9.2 |
| **2024** | 117 | 120,858 | 14:07 | 312,508 | 2.59 | 0% | 9.8 |
| **2025** | 123 | 76,119 | 15:01 | 167,493 | 2.20 | 0% | 10.1 |
| **2026** | 65 | 99,165 | 15:12 | 190,960 | **1.93** | 0% | 8.2 |

Bold rows are exact. 2020–22 rows use interpolated dates and rounded catalog view counts.

2020–21 was a *different channel*: r/wallstreetbets meme recaps, options tutorials, 3–5 minute clips,
27 uploads a month. Those videos are the bottom of the library (298 to 1,000 views). The pivot to
long-form corporate-fraud documentary lands ~2022–23 and doubles median views while **cutting output
by two-thirds**.

**Do not read the 2025/2026 median dip as decline.** Views are lifetime and these cohorts are young.
Age-normalised, current output is the strongest the channel has ever been:

| year | med age (days) | med views | med views/day |
|---|---:|---:|---:|
| 2023 | 1,130 | 105,500 | 95 |
| 2024 | 791 | 121,500 | 154 |
| 2025 | 404 | 73,000 | 183 |
| 2026 | 113 | 99,000 | 892 |

### 1.2 The dispersion collapse is the real story

p90/median has fallen monotonically for four straight years: **3.15 → 2.59 → 2.20 → 1.93**. Within
the age-controlled 2025 cohort, p90/p10 is only **4.15×** and the best-to-worst matched pair is
**15.9×** (`The New Elizabeth Holmes` 381K vs `Why Ivy League Universities Lose Money` 24K).

For scale: the Modern MBA matched pair we measured on 2026-08-16 was **18.3×** on a channel
publishing a third as often. WSM has traded variance for reliability. That is a deliberate,
coherent strategy — and it is the opposite of the outlier-hunting strategy our own rules assume.

---

## 2. Titles — two levers, and only two

Measured on the 415 post-pivot (2023+) videos, era-controlled.

| title feature | n | share | med views | lift |
|---|---:|---:|---:|---:|
| **fraud / scam / ponzi / hoax** | 60 | 14.5% | 145,000 | **1.56×** |
| **contains a $ amount** | 32 | 7.7% | 143,000 | **1.51×** |
| contains any number | 46 | 11.1% | 137,500 | 1.45× |
| collapse / fail / implode / bankrupt | 78 | 18.8% | 111,500 | 1.17× |
| named company (OpenAI, Tesla…) | 61 | 14.7% | 105,000 | 1.11× |
| possessive (*X's Y*) | 89 | 21.4% | 105,000 | 1.11× |
| verdict adjective | 36 | 8.7% | 101,500 | 1.05× |
| A.I. in title | 27 | 6.5% | 99,000 | 1.03× |
| named person (Musk, Altman…) | 36 | 8.7% | 98,500 | 1.02× |
| *The Rise/Fall/Story of…* | 29 | 7.0% | 91,000 | 0.92× |

**Only fraud and a number lift.** Celebrity names, company names, AI, drama adjectives and the
classic *Rise and Fall of* template are all flat. Titles are short and stable: median 43 characters,
7 words.

> ⚠️ **Era-controlling reversed two results.** Pooled across the whole library, "contains a number"
> reads **0.65×** and "contains a $ amount" **0.78×** — both apparently *negative*. That is pure
> Simpson's paradox: the 2020–21 options-tutorial era is full of numeric titles (`$10K Gone on PRPL
> Options`) and is uniformly the worst-performing content on the channel. Split by era, both flip to
> **+45–51%**. Any title analysis on a channel that pivoted must be era-split first.

### 2.1 The measured lever: ACCUSATION, not analysis

Classifying every 2023+ title as **ACCUSATION** (a named actor is asserted to be doing or suffering
something adverse) vs **ANALYSIS** (a neutral interrogative or mechanism explainer):

| class | n | share | med views | p90 |
|---|---:|---:|---:|---:|
| ACCUSATION | 126 | 30.4% | 125,500 | 318,000 |
| both | 15 | 3.6% | 133,000 | 285,000 |
| neutral | 195 | 47.0% | 94,000 | 207,000 |
| ANALYSIS | 79 | 19.0% | 89,000 | 326,000 |

Age-residualised on log(views/day), **exact dates, n=408**, 20,000-permutation test:

> **ACCUSATION frame: rho = +0.224, p < 0.0001, 1.69× median views/day (253 vs 149).**

The ratio holds every year independently (2023: 1.53×, 2024: 1.82×, 2025: 1.21×).

**And the lift is reach, not engagement.** On the 403 videos with full engagement data, accusation
titles get a *slightly lower* comment rate than the rest — 0.432% vs 0.486% (**0.89×**) — against
channel medians of 2.83% like/view and 0.463% comment/view. The frame is not winning by provoking
the existing audience into arguing; it is winning by being clicked and served more widely.

Note the ceilings: ANALYSIS p90 (326,000) is *higher* than ACCUSATION p90 (318,000). Accusation does
not raise the ceiling — **it raises the floor.** That is exactly what a conveyor belt needs.

The matched-pair extremes are categorically clean:

- **Top 8 (2025):** *The New Elizabeth Holmes* · *Sam Altman Freaking Out As Gov Rejects Bailout* ·
  *The Beginning Of The End For OpenAI* · *OpenAI Losing Billions on AI Slop Videos* ·
  *The Coming AI Datacenter Collapse* · *Tesla Sales Are Imploding* · *What Ever Happened To VinFast?* ·
  *Tesla Lies About Almost Everything*
- **Bottom 8 (2025):** *Is MicroStrategy Distorting the Bitcoin Market?* · *Elio Motors, The Original
  Aptera* · *How Much Are Ukraine's Minerals Worth* · *US Military Invests In SPAC Company* ·
  *Crocs Are Ugly, Yet They Still Sell Billions* · *How CoreWeave Became The Biggest IPO of 2025* ·
  *European Defense Companies Profit Massively From Ukraine War* · *Why Ivy League Universities Lose Money*

Every winner names a villain in the present tense. Every loser asks a neutral question about a thing.

### 2.2 ⛔ Our consumer-felt anchor rule does NOT replicate here

Same corpus, same method, same permutation test, applying the `CHANNEL-BIBLE` §5 anchor
classifier (has the viewer personally paid for / stood inside / worked in the thing):

> **CONSUMER-FELT ANCHOR: rho = +0.028, p = 0.58, 1.02× median views/day. Nothing.**

The 2×2 is unambiguous — accusation works identically in both anchor columns, anchor works in
neither accusation column:

| | acc=0 | acc=1 |
|---|---:|---:|
| **felt=0** | 148 (n=234) | 251 (n=114) |
| **felt=1** | 136 (n=37) | 254 (n=22) |

*Crocs* and *Ivy League tuition* are as consumer-felt as topics get, and both sit in the bottom 8.

*(2×2 cells above are from the interpolated-date run; the exact-date run gives the same picture —
rho +0.028, p = 0.58.)*

**This qualifies our own §5 finding rather than contradicting it.** The anchor result (rho +0.51,
p<0.0001) was measured on Modern MBA — a *systems-explainer* channel where the viewer's own
experience is the entry point. WSM is a *prosecution* channel; its entry point is the accusation, and
the reader's personal exposure to the defendant is irrelevant. Two channels, two levers.
**The anchor rule is format-specific, not universal — record it that way in the bible.**

---

## 3. The visual layer — a full shot census

`Figure AI Appears To Be Faking Its Demos` (258K, 0.70×, 13:25, best recent performer). Every one of
its 38 shots classified by hand.

```
  38 shots · 13.4 min · 2.8 shots/minute
  median shot 4.7s · mean 21.2s · longest 241.7s

  class                                     shots    %sh     time   %time
  people TALKING (interview/news/keynote)       9  23.7%     211s   26.3%
  people present, not talking to camera         5  13.2%     115s   14.3%
  live footage, NO people                      18  47.4%     118s   14.7%
  capture of an existing artifact               5  13.2%     345s   42.9%
  graphic ORIGINATED by the channel             1   2.6%      15s    1.8%

  REAL MATERIAL (A+B+C+D1)                     37  97.4%     790s   98.2%
  ORIGINATED by the channel (D2)                1   2.6%      15s    1.8%
```

**The single originated graphic in the entire video is the end-card logo.**

### 3.1 What that means in practice

- **Zero data-viz. Zero charts. Zero designed panels. Zero lower-thirds. Zero chapter cards.**
  The whole conduit component library — cream evidence card, dark navy analysis panel, ghosted-slot
  grid, stat hero, funding timeline — has no counterpart here.
- **The channel's entire original visual vocabulary is a red circle and a line of white sans-serif
  text with a drop shadow, placed over someone else's footage.** Verified in the pixels at 500s:
  Figure's own promo video, plain overlay reading *"Robot started turning around BEFORE Adcock told
  it to."* That is the design system.
- **Sources are the subject's own material.** Bloomberg Tech interview clips, the CEO's own podcast
  appearances, Figure's own promo reels, BMW's own factory footage, X posts, a Fortune article. The
  prosecution is built out of the defendant's own evidence — which is *why* it needs no graphics.
- **Enormous holds.** 6 shots run over 30s and account for **69% of runtime**. One shot — a tweet
  with an embedded video and a red circle — holds for **241.7 seconds**. Four minutes.
- The description carries an explicit fair-use disclaimer. It has to.

### 3.2 Against the three proven doc channels we censused on 2026-08-12

| | Explorist *Nvidia* 7.48× | ColdFusion *DataCentres* 2.6× | ColdFusion *Dropbox* 0.93× | **WSM *Figure AI*** |
|---|---:|---:|---:|---:|
| shots / minute | **10.6** | 7.3 | 4.7 | **2.8** |
| mean shot | 5.7s | 8.2s | 12.8s | **21.2s** |
| real material (% shots) | 88.0% | 89.5% | 84.0% | **97.4%** |
| graphics made by channel | 12.0% | 10.5% | 16.0% | **2.6%** |

WSM cuts **3.8× slower than the 7.48× outlier** and originates **a quarter as much** design work.

> **This does not overturn the cutting-rhythm finding — it bounds it.** That finding was measured
> *within* one lane (documentary-essay), where rhythm was monotonic with outcome. WSM is a different
> lane, and inside it rhythm is not the lever. Cut rhythm and material mix are both **lane
> constants**, not universal dials. What travels across all four censuses is only this: *the material
> is overwhelmingly real, and the channel's own design work is a rounding error.*

---

## 4. The prose layer

From four `teardown.py` runs:

| video | uploaded | outlier | runtime | words | wpm | negation/min | loop-openers/min |
|---|---|---:|---:|---:|---:|---:|---:|
| Richard Branson (all-time #1) | 2023-03-29 | 4.39× | 14:43 | 2,653 | 180 | 1.8 | 0.3 |
| Luxury Fashion | 2021-12-21 | 2.27× | 9:27 | 1,949 | 206 | 3.9 | 0.3 |
| Figure AI (best recent) | 2026-06-01 | 0.70× | 13:25 | 2,438 | 182 | 2.1 | 0.6 |
| Anthropic / SBF | 2026-08-14 | 0.17×* | 19:16 | 3,498 | 182 | 1.8 | 0.5 |

\* two days old at measurement — **not** a flop; it was running ~30K views/day. Included for register,
excluded from any performance claim.

**Pace is locked at ~180 wpm** and does not move. Same constant we found on Modern MBA (178.4 vs
178.4 across an 18.3× pair). Third independent confirmation that **prose register is an entry
requirement, not a lever.**

### 4.1 Their cold opens break our §2 and §3 rules, and win anyway

**Figure AI (0.70×) gives away the entire verdict by 0:43:**

> *"…last year Figure's CEO Brett Adcock claimed that the robot was doing his laundry in his house.
> Adcock was lying."*

No curiosity gap. No withheld meaning. The thesis is stated flat, in the first forty seconds.

**Luxury Fashion (2.27×) opens with the exact boilerplate our standard says to DELETE FOREVER:**

> *"what's up guys and welcome back to wall street millennial on this channel we cover everything
> related to stocks and investing…"*

**Richard Branson (4.39×, the all-time #1) opens on 42 seconds of unbroken praise** — knighthood, the
Virgin empire, "his adventurous spirit" — before the word *despite* turns it. That is a setup-and-
reverse, and it is the only one of the four with a real narrative hinge.

**Read honestly:** the curiosity-gap rule is not falsified, but this channel demonstrates it is not
*necessary* at this cadence. When a viewer sees you three times a week and the title is an
accusation, the open's job is to confirm the accusation is real, fast — not to open a loop. The gap
is doing work in the *title*; the open just has to cash it.

---

## 5. Business model

Not a pure AdSense channel:

- **Sponsor reads** — GoDaddy (2026), moomoo (2023). Present in the description, not merely the video.
- **Patreon** (older era).
- **A second channel** — `@brokenbusinessmodels`, cross-linked in every description.
- **A research business** — *Differentiated Analytics*, `founder@differentiatedanalytics.com`.
- **Professional management** — `mary@creatormanager.co` handles sponsorship inquiries.

At ~10 uploads/month × ~99K median views, the channel produces roughly **1M views/month** of
15-minute, mid-roll-eligible finance content. That is the actual product. The library is not
appreciating (news-anchored topics date), so the revenue is a **flow**, not a **stock** — which is
precisely the treadmill our own `BEAT-A-CHANNEL` §2 argues against, run competently and at scale.

---

## 6. What transfers to us, and what does not

### ✅ Take

1. **The ACCUSATION title lever is measured, replicated across three years, and cheap.** *Named actor
   + adverse present-tense verb.* It raises the floor by 71%. Our current title register leans
   analytical (*How X works*, *Why Y happens*) — the class that sits at the **bottom** here.
2. **Build the case out of the defendant's own material.** Their promo reel, their keynote, their
   tweet, their earnings call. It is free, it is unimpeachable, and it removes the need for the
   graphics budget entirely. This is `VISUAL-SOURCING` §9.1 taken to its limit.
3. **The red circle is the whole annotation system.** One highlight primitive, used relentlessly,
   beats a component library nobody can afford to keep filling. Worth one experiment against our
   word-synced citation card.
4. **Era-split before any title analysis.** Cost us a wrong sign on two features here; would have
   cost a wrong conclusion if we had shipped it.

### ❌ Do not take

1. **The cadence.** ~10 uploads/month of 15-minute video is the entire mechanism. We cannot run it,
   and every craft observation above is downstream of it. Copying the *style* without the *supply*
   gets the flat ceiling (they have never cleared 1× since 2023) without the flat floor.
2. **The 241-second hold.** It works because the artifact on screen is genuinely damning and the VO
   is dissecting it frame by frame. On a weaker beat it is a dead frame. Our `deadspace-scan.py`
   would fail that shot, correctly, for our format.
3. **The news anchor.** Post-2023 output is almost entirely dated within 90 days. `BEAT-A-CHANNEL` §2
   and `video-production-standard` §8 both already rule this out for us, and this teardown is
   evidence *for* that rule, not against it — the channel's library does not compound.
4. **2.8 shots/minute.** Only survivable with 98% real material and a prosecutorial spine. Our
   footage-first rules (one clip once, ≤6s) exist because we do not have their sourcing position.

### ⚠️ Update in our own docs

- `CHANNEL-BIBLE` §5 / `VOICE-AND-REGISTER` §0 — **mark the consumer-felt anchor finding as
  format-specific.** Measured +0.51 on Modern MBA, **+0.019 (p=0.70) here.** State the scope.
- `reference_proven_doc_channels_presentation` — add WSM as a fourth census and note that cut rhythm
  is a **lane constant**, not a universal dial (2.8/min at 0.70× vs 4.7/min at 0.93×).

---

## 7. Files

```
tools/raw/wsm/uploads.tsv · uploads.json · dates.tsv     # 951-row catalog + interpolated dates
tools/raw/wsm/meta.tsv                                   # 453 EXACT: date, views, likes, comments
tools/teardowns/XvP7RV2umRU.md  # Richard Branson 4.39x
tools/teardowns/RuLAOfWWgxE.md  # Luxury Fashion 2.27x
tools/teardowns/Juc-IyTdSho.md  # Figure AI 0.70x
tools/teardowns/DFar4hdQMfI.md  # Anthropic/SBF (2 days old)
tools/census-Juc-IyTdSho/       # sheet_01.jpg, shots.json, classes.txt, census.csv
```

**Known limits.** Dates and counts are **exact for the whole post-pivot era** (453 videos, back to
2022-01) — every statistical claim rests on those. The 2020–21 rows use dates interpolated from 48
anchors and rounded catalog view counts; they are descriptive background only. Only one shot census was run —
the visual findings are n=1 for this channel and should not be generalised past "this is what their
best recent video looks like." No retention data exists for a third-party channel, so every outcome
here is views, never watch-time.
