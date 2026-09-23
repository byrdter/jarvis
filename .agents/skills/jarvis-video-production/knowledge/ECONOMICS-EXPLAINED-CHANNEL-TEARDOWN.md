# Economics Explained — channel teardown

**Measured 2026-09-23.** `@EconomicsExplained` · 2,880,000 subs · 372 long-form + 75 Shorts ·
367M long-form views · first public upload 2019 · faceless, one Australian narrator.

Method: full catalog pull (`yt-dlp --flat-playlist`); **exact** upload dates, like and comment counts
for 362 of 372 long-form videos (the 10 missing are all 2019–20 and were interpolated from their
neighbors); **every title hand-classified** by frame and topic (`raw/econexp/videos.csv`); era
control = residual against the half-year median of log(views); 4,000–20,000-shuffle permutation tests.
Six transcripts (`teardown.py` for two; NotebookLM for four after YouTube IP-blocked yt-dlp);
thumbnail contact sheets (`raw/econexp/thumbs_*.jpg`); monetization mix read from all 362 descriptions.

> ⚠️ **NOT MEASURED: the in-video shot census.** YouTube put a CAPTCHA on this IP halfway through
> (it hit Terry's own Chrome too), and storyboards need signed URLs. §5.2 marks everything about the
> in-video visuals as inference. Run `shot-census.py F_VUBpALcVE` once the block lifts.

---

## 0. The one-line finding

> **Economics Explained wins with a CONTAINER plus a STANCE.** The container is a country (unlimited
> supply, half the catalog, the best topic class at 1.20×). The stance is a title that passes a
> judgment instead of asking or labeling (1.37×, p<0.0001, **positive in all 8 years**). Put both in
> one title and it gets **1.40×**; use neither and it gets **0.79×**. That is a 1.8× spread from two
> decisions that cost nothing to make.

And it is drifting away from its own lever: open **questions** have climbed to 30% of current output
and are the worst class it makes right now (0.79×, p=0.0045).

---

## 1. The numbers

| year | n | med views | med runtime | p90/med | uploads/mo | med views/day | like % | comment % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 37 | 511K | 11:05 | 2.66 | 3.1 | 203 | 3.10 | 0.241 |
| 2020 | 104 | 674K | 16:36 | 2.34 | 8.7 | 285 | 3.04 | 0.294 |
| 2021 | 26 | 1.10M | 16:40 | 3.20 | 2.2 | 576 | 2.59 | 0.235 |
| 2022 | 25 | 1.07M | 16:40 | 3.52 | 2.1 | 738 | 2.66 | 0.207 |
| 2023 | 66 | 877K | 15:34 | 2.08 | 5.5 | 721 | 2.48 | 0.221 |
| 2024 | 44 | 621K | 15:16 | 2.56 | 3.7 | 733 | 2.53 | 0.207 |
| 2025 | 34 | 543K | 15:05 | 2.20 | 2.8 | 1,113 | 2.55 | 0.251 |
| 2026 | 34 | 416K | 18:08 | 2.30 | 3.9 | 3,240 | 2.72 | 0.283 |

- **2021–22 was the peak and it was scarce**: about 2 public uploads a month and the highest medians
  and ceilings on the channel. Treat that with care: this is the *public* Videos tab, so any
  unlisted or deleted videos would inflate the peak (survivorship).
- **The raw decline since 2023 (877K → 416K) is mostly age.** A single snapshot can't separate a
  weaker channel from younger videos. Median views/day rises every year, which fits younger cohorts
  but doesn't prove health. Call it *flat to slowly declining, unproven.*
- **Moderately hit-driven.** p90/median is 2.1–2.6 in the current era, flatter than the 2021–22 peak
  and about WSM's level (1.9–2.6). The top 10% of videos hold **35%** of all views; the all-time #1 has
  14.5M.
- **Shorts don't matter to this channel.** 75 Shorts, median 47K, 9.2M views in total, which is 2.5%
  of long-form. That matches our own finding that the 2-shorts rule is dead.

---

## 2. Niche and positioning

**Niche:** macroeconomics for a general audience, told through **nations**. The brand is the name of
the category, *Economics Explained*, which does three jobs at once: it's what people search for, it
claims authority, and it tells you what the channel is for.

**Positioning:** it sits between academic economics (accurate, dull) and finance-doom YouTube
(exciting, hysterical). The voice carries the position: wry, first-person, openly Australian (*"here in
Australia," "across the pond," "Thanks for watching, mate"*), willing to hedge (*"Okay, it's not quite
that bad"*), and making fun of its own field (*Economics Is A Junk Science*, 2026). **The titles lean
more doom than the scripts do**, and that gap between the package and the content is the whole
positioning trick.

**Origin → pivot:** 2019 was video-game and fiction economies (EVE Online ×3, RuneScape, Westeros,
Star Wars, Star Citizen). That's the worst topic class it has ever made (**0.56×, p=0.015**), and it
was dropped by 2021. The channel grew once it moved to real countries.

---

## 3. Topic selection

Hand-classified topics, era-controlled:

| topic | n | share | lift | p |
|---|---:|---:|---:|---:|
| **Country / place profile** | 179 | 48% | **1.20×** | 0.0004 |
| Viewer's wallet / generation | 23 | 6% | 1.25× | 0.12 |
| Concept / system | 98 | 27% | 0.94× | 0.20 |
| News event / markets | 37 | 10% | 0.87× | 0.13 |
| History | 10 | 3% | 0.86× | 0.41 |
| Meta / Nobel | 11 | 3% | 0.84× | 0.34 |
| **Fiction / game economies** | 12 | 3% | **0.56×** | 0.015 |

In the current era, country profiles are **59%** of output and lift **1.27×** (p=0.003).

**The country is a container, not a topic.** There are about 195 countries plus US states, cities
and regions, and each one can be revisited. The channel runs three repeatable franchises on that
supply:

1. **The profile:** *The [Adj] Economy of X* (2019–20 bread and butter; neutral versions now 0.93×).
2. **The revisit:** *How Has X Been Going?* (Brexit 3.5M, Argentina 1.3M, Turkey, Canada, France,
   Nepal, Sri Lanka). A built-in sequel format for any country covered before.
3. **The alarm:** *Something Terrible/Weird Is Happening in X* (Italy 3.2M, France 1.2M, California 1.4M).

**China is a sub-franchise** with 25 titles. **Annual tentpole:** the Nobel Prize explainer every
October; 2024's was the channel's #3 video of the era at **5.05×**.

**Wallet topics** (*Young Generations Are Now Poorer Than Their Parents*, 7.5M) lifted 1.64× before
2023 (p=0.05) and are **flat since** (0.98×). Our consumer-felt anchor rule doesn't replicate here
either. That's the same result as WSM, and the rule stays format-specific.

**Current-events drift in 2025–26:** four Iran-war videos plus Venezuela, Cuba and OPEC. News events
are the weakest real-world class in the current era (0.75×).

---

## 4. Title patterns: the measured lever is STANCE

Every title was hand-labeled into one of five frames:

| frame | example | n | share | lift | p |
|---|---|---:|---:|---:|---:|
| **VERDICT** | *Spain Was a Warning* · *The Rather Pathetic Economy of Russia* | 106 | 29% | **1.40×** | <0.0001 |
| WITHHELD | *Something Terrible Is Happening in Italy* · *This Tiny Country Built the Laziest Economy…* | 17 | 5% | 1.17× | 0.26 |
| PARADOX | *Denmark Should Not be Rich* · *Uruguay Has No Resources, But They're Rich* | 46 | 12% | 1.10× | 0.20 |
| QUESTION | *Is the European Union Worth It?* · *How Strong Is India's Economy?* | 95 | 26% | 0.87× | 0.019 |
| LABEL | *The Economy of Italy* · *How to Rebuild an Economy* | 106 | 29% | 0.87× | 0.012 |

**STANCE (verdict + paradox + withheld) vs no stance (question + label): 1.37×, p<0.0001.** Same result
in 2019–22 (1.50×) and in 2023+ (1.37×). It's positive in every single year: 2019 2.73×, 2020 1.23×,
2021 3.13×, 2022 3.33×, 2023 1.44×, 2024 1.05×, 2025 1.29×, 2026 1.72×.

**It's reach, not engagement.** Stance titles get *lower* like and comment rates (2.53% / 0.235% vs
2.82% / 0.255%). It's the same pattern as WSM's accusation frame: the frame gets the video clicked and
served. It doesn't get it argued about.

**Country × stance add together:**

| | no stance | stance |
|---|---:|---:|
| **not a country** | 0.79× (n=119) | 1.07× (n=72) |
| **country** | 1.00× (n=82) | **1.40×** (n=97) |

**Other surface features (2023+ era):** a number in the title **1.49×** (p=0.04); `$`/`%` 1.49×
(p=0.08); contrarian words (*not / no one / actually / wrong*) **1.39×** (p=0.02); dropping the
`| Economics Explained` suffix in 2023 made no difference at all (1.00×). Starting with "Why" or
"How", or using an ellipsis, did nothing measurable.

**Borrowed authority makes the ceiling.** *MIT Has Predicted that Society Will Collapse in 2040*
(14.5M, the all-time #1) and *MIT Study Reveals Why Africa Is Still Poor* (2.4M, 3.19×). Only 11
authority titles, so the lift isn't significant (0.92× overall, 1.30× in 2023+). The ceiling is real;
the average isn't.

**The current-era drag:** questions are 30% of 2023+ output and sit at **0.79× (p=0.0045)**. The
bottom 8 of the era are nearly all questions or neutral concepts: *Is The Survival of Humanity
Economically Viable?* 0.39×, *How Does Finland Redefine Economic Success?* 0.39×, *Did Washing Machines
Change The Global Economy More Than The Internet?* 0.36×.

**Top 8 of the current era (era residual):** *Why Everyone is Leaving New Zealand* 6.18× (3.6M) ·
*Spain Was a Warning* 5.09× · *2024 Nobel Explained* 5.05× · *Something Terrible Is Happening in Italy*
4.53× · *Can Tariffs Actually Work?* 3.75× · *MIT Study Reveals Why Africa Is Still Poor* 3.19× ·
*1 Year Later: How Has Argentina Been Going?* 2.99× · *Japan's Rise and Fall… And Rise Again?* 2.90×.
Six of the eight are countries. The two questions that win are news-pegged (tariffs, Feb 2025) or a
revisit.

---

## 5. Visual language

### 5.1 Thumbnails (measured: contact sheets of the 16 newest, the top 8 and 8 from 2019–20)

One locked system since about 2021:

- **Torn-paper text strips:** black condensed all-caps on yellow, or yellow on black, set at a slight
  angle. Two or three short lines at most.
- **The `EE` yellow roundel** in the top-right corner of every thumbnail. That's the whole brand mark.
- **The red area chart:** a red-filled line on a white grid (*Does Capitalism Still Work?*, *Global
  Assets / Global Debt*, *Utopia or Dystopia?*, *Life Expectancy vs GDP*). It's the channel's visual
  shorthand for "economics."
- **A photo of a real subject** with a head of state or a crowd, and often a **fake quote**: Xi with a
  phone, *"I JUST REMEMBERED WE'RE COMMUNISTS"* for the billionaire-tax video.
- **The thumbnail text adds to the title rather than repeating it:** *WHY NOW?* on the New Zealand safe
  haven video, *284 DAYS LATER* on Nepal, *INVESTED: $55 BILLION → EMPLOYEES: 10* on the AI data
  center video. The title makes the claim and the thumbnail shows the evidence or the question.
- **2019–20:** full-bleed yellow outlined serif-condensed type over a dark, tinted photo. The torn
  strip replaced it.

### 5.2 In-video (INFERENCE ONLY, NOT MEASURED; see the warning at the top)

Signs in the transcripts: deictic "this" and "here" point at footage (*"when a shack like this sells
for $7 million," "across the pond here in Australia"*). The end screen says *"which you should be able
to click to on your screen now."* Storyblocks is one of their sponsors (a stock footage library). So
it's most likely stock and news footage with maps and charts under a continuous VO, but **no
shot-rate, material mix or graphics share is claimed** until `shot-census.py` runs.

---

## 6. Storytelling: one template, run every time

Measured on 6 transcripts (2021 #1, 2024 and 2025 hits, a 2025 flop, two 2026 uploads).

1. **Situational cold open (45–90s).** Place, status and a paradoxical fact, stated flat.
   *New Zealand:* "a country that probably looks like a dreamland to most of the rest of the world and
   they're leaving it." *Spain:* opens in 2006 with Spain "riding high," then the crash, then the
   twist: Spain was *less* leveraged than many economies are today. *MIT 2040:* the claim, then "we are
   ahead of schedule," inside the first 10 seconds.
2. **The triple-question roadmap.** *"So, what makes New Zealand's economy so unique? What are the
   issues causing so many Kiwis to leave? And finally, why has this trend been so hard to reverse?"*
   The same "So… what? … And finally, why?" shape opens New Zealand, Spain, Survival of Humanity and
   the billionaire tax video: **4 of 6 confirmed.** It names the loops out loud.
3. **The sponsor read comes right after the roadmap (~1:30–2:30).** The loops are open at exactly the
   point the ad starts, so the roadmap does double duty as the ad bridge. There's a second, smaller
   plug mid-video (the newsletter at 7:51 in *Junk Science*).
4. **The body answers the questions in order.** It's a chain of causes (NZ: small and remote → only
   industries that have to be there → housing is half of GDP → but the young leave for *opportunity*,
   not cheaper homes → Australia is legally a domestic move). There's usually one "the obvious answer
   is wrong" turn (*"this makes it seem like a pretty open and shut case, right? … The problem with
   that assumption is…"*).
5. **A persona in the gaps:** personal anecdote (*"when my partner went to medical school, about half
   of the students in their year were from New Zealand"*), dry jokes (*scenery "actively trying to kill
   them"*), crediting other creators by name.
6. **A soft landing.** The ending is hedged and balanced, and it points to an older video.
   **The title's verdict is harsher than where the script ends up.**

**Pace: about 205–220 wpm** in the current era (*Junk Science* measured at 206; the others estimated
from character counts); the 2021 #1 was about 187. **That's the fastest narration we have measured:**
WSM and Modern MBA both sit at 180. The pace is a constant across hits and flops, so it's a house
style, not a lever.

**The hook in terms of our rules:** the open gives facts and the question and holds back the
mechanism, which is exactly our curiosity-gap rule, run the same way every time. The billionaire-tax
video is a clean **withheld-name** package: the title says "a country," the thumbnail shows Xi, and
the script says China in its first word.

---

## 7. Production system

| layer | what they do |
|---|---|
| **Talent** | One faceless Australian narrator. The voice *is* the brand. |
| **Writing** | A team (*"between scripting episodes, editing drafts and going back and forth with collaborators"*). Statista credited for research on every video since 2022. |
| **Cadence** | 3–5 long-form videos a month, 15–18 min. Shorts ignored. |
| **Sponsors** | A read in **56–88%** of videos per year. 2025–26: Surfshark, Trading212, Saily, Incogni, Odoo, AnyDesk, Grammarly, Storyblocks. ⚠️ Sept 2026: a **paid penny-stock promotion** (Salescloer, "compensated by Synergy Capital," with an SEC-style disclaimer read aloud), which is a credibility risk for a brand built on explaining things. |
| **Patreon** | In every description since 2020. The tiers are named **Royalty / Upper / Upper Middle / Middle Class**, which is on brand. |
| **Reuse** | **Localized channels:** WirtschaftsWissen (German), L'Économie Expliquée (French) since 2023–24. **Audio podcast** on Spotify/Apple since 2021. **Sister channel** *Context Matters* since 2023. **Newsletter** (beehiiv, ~10K) since 2026, with early ad-free access to the next video as the carrot. |

**This is a media company built on one script.** Each script ships as the English video, a German
dub, a French dub, a podcast episode and newsletter material. The per-view cost keeps falling as
more channels reuse it.

---

## 8. What transfers to us (Ordinary Economics lane)

This is the **closest channel to Ordinary Economics** we have torn down so far. It's the only
economics explainer at scale in the corpus.

### ✅ Take

1. **Stance titles, always.** Verdict, paradox or withheld; never a neutral question or a topic label.
   1.37×, replicated in every year. Together with WSM (accusation 1.69×), that makes **two
   independent channels where the frame that commits wins.** This also confirms the Ordinary
   Economics note that *mechanism framings are dead*: EE's neutral mechanism and label titles are its
   bottom class.
2. **A container with unlimited supply.** Countries gave EE 179 videos, a sequel format (*How Has X
   Been Going?*) and a regional alarm format. Ordinary Economics needs the same thing: a noun type we
   can fill forever (an investment, a company, a product) and a revisit format for it.
3. **The triple-question roadmap** as an out-loud loop at 0:45–1:30. It costs nothing and it's a
   standing template on the channel that has run it 300+ times.
4. **The thumbnail adds the missing piece:** the title makes the claim and the thumbnail carries a
   number, a quote or the question. One strip style, one roundel, one chart motif, locked.
5. **Annual tentpole** (EE's Nobel): pick one recurring date-anchored explainer per year.
6. **Reuse per script** (dubs, podcast, newsletter) once there's a back catalog. It's cheap with
   our TTS stack.

### ❌ Do not take

1. **Open questions.** EE's own worst current habit (30% of output, 0.79×).
2. **Fiction and game economies.** The origin era, and the worst class at 0.56×.
3. **The news-war cluster.** Dated, and 0.75× in the current era.
4. **Paid stock promotion.** It trades away exactly the credibility the brand sells.
5. **The 205–220 wpm pace** as a default. It's a house style, not a proven lever, and it's harder on
   TTS clarity.

---

Data: `tools/raw/econexp/videos.csv` (every video, exact date, era residual, hand labels:
frame L/Q/V/X/N, topic C/K/W/E/H/F/M). Thumbnails: `tools/raw/econexp/thumbs_{recent,top,2019}.jpg`.
Transcripts: NotebookLM notebook *Economics Explained teardown 2026-09-23*, plus
`tools/teardowns/TsfsoaNFyTQ.md`.
