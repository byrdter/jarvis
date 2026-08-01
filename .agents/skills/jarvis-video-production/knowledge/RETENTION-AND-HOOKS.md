# Retention & Hooks — the Byrddynasty standard (READ FIRST when scripting)

This is the **canonical playbook** for how Byrddynasty ("Understanding AI") videos hold attention.
It was derived on 2026-07-14/15 from the channel's real YouTube Studio numbers and applied to the V6
and V5 8-minute recuts. **Every video and every short follows it.** If any older doc (including this
skill's own "preferred runtime 10–15 min" line, now superseded) conflicts, this wins.

**§1–§6 are about executing a video well. §7 is about choosing which video to make — it runs
*upstream* of everything here, so read it first when the topic isn't already decided.**

---

## 0. The diagnosis that drives everything (from real Studio data)

Diagnosed from our own YouTube Studio analytics, 2026-07-14. (The specific figures are kept
out of this public repo — see the private analytics notes. The shape of the finding is what
matters, and it generalises.)

- The channel was **growing on subscribers** — **not** a quality problem.
- **The large majority of viewers left in the first ~30 seconds.** Our best-performing video still
  showed a steep cliff inside the first 30s; a weak one averaged well under a minute of view
  duration on a 15-minute runtime.
- Traffic was **effectively effectively 0% Browse / Search / External** — i.e. the algorithm was **not
  distributing** the videos at all.

**The mechanism:** YouTube only pushes a video into Browse/Suggested once it trusts the video will
hold attention. Low first-30-seconds retention → no Browse → ~single-digit views. **The channel is
retention-gated, not quality-gated.** The product was never the problem; the first 30 seconds and the
runtime were. Full strategic write-up: `jarvis-private/apps/content-creation/video-generator/
PromotionPlanning/BYRDDYNASTY-GROWTH-PLAN-2026.md`.

What we also found by watching our own videos:
- Our best-performing opening put **Terry's face on camera in the first second**; the dying ones
  opened on **dark abstract graphics** with a disembodied AI voice for ~20s (reads as "AI slop").
- Every video then sagged at ~0:17–0:40 into the same boilerplate: **"I'm an avatar… he spent 38
  years… on this channel we keep asking one question…"** — a bio + channel-refrain + thesis block that
  deflated the hook. That block is the single biggest retention leak we had.

---

## 1. The runtime rule: retention-gated, start ~10 min

> **Revised 2026-07-29** (supersedes the flat "~8 minutes" that stood here). 8 min was a *training
> wheel* imposed while retention was unproven — not an optimum. The competitor teardowns (Big Data
> Factor 5:45, Explainer Chris 19, High Yield 30, Fractal Philosophy 45) proved long-form wins **iff
> the video carries a whole-runtime withheld payoff + a persistent progress spine.** The old 12–15 min
> videos failed for *lacking that spine*, not for their length. So the rule is now a mechanic.

**Runtime = the longest you can sustain a withheld payoff at high retention — no longer.** YouTube
rewards *total watch time* (runtime × % viewed); longer wins only when the curve holds.

1. **Start a rebuilding batch at ~10 minutes**, then let the retention graph vote: holds past ~40% at
   the 10-min mark → next video 12–13; sheds after the reversal → tighten. **Never blind-ship 12–15
   again — that shape is what failed; earn it with the curve first.**
2. **Precondition for any runtime over ~8 min — all three or trim to 8:** (a) a payoff withheld across
   the *whole* runtime (mystery/punchline, not just a 0:20 hook); (b) a persistent on-screen spine
   (scale ladder / component checklist / numbered framework / section badge); (c) a reversal at ~40–55%.
3. **% viewed is still what YouTube rewards** — a tight 10-min cut with a real loop beats a baggy 15.
   The highest-outlier *reachable* winner (Big Data Factor) is 5:45; length is a privilege retention
   earns, not a default. 8:00+ also clears the mid-roll-ad threshold (later monetization; not the point now).

Recut baggy videos by trimming redundancy, example-parades, and throat-clearing while keeping every
*verified fact* and installing the missing spine. (V6 went 15:29→8:32; V5 went 13:00→8:30.)

---

## 2. The cold-open template (INFORMATION FIRST) — every video, no exceptions

> **CHANGED 2026-07-26.** This section previously mandated FACE FIRST (avatar on camera from frame
> one). **The channel is now faceless** — a ~1-month test, decided 2026-07-26. Every competitor in our
> set is either faceless or genuinely on-screen; none uses an avatar. Faceless is also far cheaper to
> produce automatically, which buys time for the lessons themselves. The avatar requirement is removed;
> the *mechanism* it served is preserved below.

The opening exists to give the viewer **a reason to keep watching** by creating tension they can't
resolve alone.

§0 found the dying videos opened on **dark abstract graphics** with a disembodied voice for ~20s —
"AI slop." The face was never the point; it was one way to satisfy the real requirement:

> **The first frame must carry concrete, specific information the viewer can read, and the VO must be
> about that thing.**

- ✅ A named document, a filing, a headline, a real number, a chart with a labelled axis.
- ✅ A face — still valid, simply no longer required.
- ❌ A gradient, a particle field, an abstract cityscape, a kicker label alone. **Mood is not
  information.** Dark is fine; *vague* is what killed the old opens.

*Proven instance:* the Messi cold open lands a California Secretary of State filing — entity name
PLAY TIME — stamped REGISTERED, inside two seconds. Dark register, concrete from frame one.

### Structure
1. **0:00 — the concrete thing on screen**, VO already inside the story.
2. **~0:00–0:20 — THE HOOK.** The single most provocative concrete stake, as a **paradox** where
   possible (see §3). A number, a story, a contradiction.
3. **~0:20–0:35 — RE-OPEN THE LOOP.** End the intro on a **named question**, not the thesis.

### Known open risk in the faceless test
The old step 3 was **the avatar joke** — *"he writes every word, I just say them"* — which disarmed the
AI-voice objection with personality. Going faceless removes the avatar but **not** the synthetic voice,
so the objection survives with nothing disarming it.

**Stop condition:** if first-30s retention drops against the face-first videos over the test month,
the test has answered and face-first returns. Re-read §0 before deciding — that data is the referee.

> **DELETE FOREVER from openings:** the "38 years" bio paragraph, "on this channel we keep asking one
> question," "Welcome back to Understanding AI," "today we're going to explore / talk about…" — every
> line that tells the viewer the video hasn't started yet. It has. *Be* started.

Proven examples: V6 = "An AI took the exam that licenses American doctors — and beat them… Would you
let it treat someone you love?"; V5 = "A lawyer walked into federal court with a brief full of cases…
not one of them existed… he'd sworn they were real."

### 2.5 Three devices that sharpen the open (from the competitor teardowns)

These are *construction* techniques for the HOOK and RE-OPEN steps above — the specific moves the
highest-outlier cold opens in our competitor set use. Source: the Internet of Bugs teardown
`tools/teardowns/a3-vf78ZwTc.md` (§7.6), first applied to AI-Finance V1 on 2026-07-22. Reach for them
whenever a hook feels informative but flat.

1. **ADVERSARY IN SENTENCE ONE.** Open on a *conflict with sides*, not a fact or a topic. IoB opens
   *"They spent a long time trying to convince you that AI wasn't a bubble."* — the viewer is recruited
   into a fight in two seconds. A fact is something you *watch*; an adversary is something you *take a
   side against*. The adversary need not be a person — it can be a consensus, an accounting treatment,
   a received analogy. If your first sentence states a fact, ask what *claim* that fact argues against
   and lead with the argument.
   - AI-Finance V1: opened on *"everyone is arguing about which bubble this is"* (the live public
     argument) instead of the CFO's quote (a fact). Conflict, not topic.

2. **THE NEGATION LADDER.** *"Not because X. Not because Y. Because ——."* Pre-empt the two explanations
   the viewer would reach for, deny both, and withhold the third. This is a mechanically perfect
   curiosity gap: it proves the two cheap answers are wrong (so the viewer *can't* resolve it alone)
   without spending the real one. It is the §3 fact-vs-meaning rule in a fixed grammar — the denied
   guesses are facts you hand over; the withheld cause is the meaning you keep.
   - IoB: *"And not just because it's way bigger, and not just because it's a higher percentage of the
     economy… but because generative AI, unlike the internet, is not a step toward prosperity."*
   - AI-Finance V1: *"Not because it's hidden. Not because anyone broke a rule. Because of a decision
     somebody made about what counts as debt."*

3. **DECLINE THE FRAME FIGHT (when a competitor owns the obvious framing).** If a proven video already
   occupies the natural framing of your topic, don't argue *within* it — name the whole argument as the
   wrong question and step outside it. This converts the incumbent's video into your setup, and it is
   paradox-shaped (a viewer can't resolve "which side is right?" if you've told them the sides are the
   wrong axis). Requires §7.3 demand to already exist — you're re-framing a live conversation, not
   inventing one.
   - AI-Finance V1 vs. IoB's 72K-view "dot-com bubble" video: instead of arguing dot-com-vs-crypto, the
     open says *"everyone is arguing which bubble this is… we read the filings instead, and they say
     something stranger."* IoB's 11-minute analogy debate becomes the thing our first line rises above.

> **Corollary — cut what the new open already delivers.** Sharpening the first lines usually makes a
> later paragraph redundant. When you rebuild an open with these devices, re-scan the next two scenes
> and delete any sentence the stronger open now carries (V1: the "second number / isn't anywhere" block
> and the "repeated the line the day before" aside both became dead weight once the adversary line
> landed). A device that adds tension up front but leaves the old scaffolding in place just inflates
> runtime.

---

## 3. HOW MUCH TO REVEAL IN A HOOK — the curiosity-gap rule (use this forever)

This is the reasoning behind the hook. Most people get it backwards.

### Core principle: hooks work by OPENING GAPS, not by HIDING information
Attention is protected by **unresolved tension**, not by withholding. (Loewenstein's *curiosity gap*:
curiosity is the feeling of a gap between what you know and what you want to know — and **you have to
know something concrete to even feel the gap.**) Give too little and there's no gap; the viewer isn't
intrigued, just uninformed — and they leave. So the question is never "how much did I reveal?" It is:
**"After this, does the viewer have a question they genuinely can't answer on their own?"** If yes, you
can reveal a lot and still hold them.

### Reveal FACTS freely; withhold MEANING
Sort every sentence of a hook into two columns:
- **HAND them (reveal):** facts, events, numbers, the *situation*. These build credibility and tension.
- **WITHHOLD (the payoff):** the explanation, the mechanism, the verdict, the twist, the resolution.
  This is what they stay 8 minutes to receive.

Example (V6): reveal = "it's catastrophically wrong on ~1 in 10 hard questions / in the same confident
voice / you can't tell which." Withhold = *how* that's possible (the loss function), the twist (humans
hallucinate more), who decides the acceptable failure rate, what to do about it.

### Prefer a PARADOX — it's self-sealing
- A plain fact ("An AI beat doctors on the licensing exam") is a **closed loop** — the viewer can
  resolve it themselves ("AI is good at tests, got it") and leave.
- A paradox ("…beat doctors, but 1 in 10 answers a physician can't call safe, in the same confident
  voice, and you can't tell which") is an **open loop** — the viewer *cannot* resolve the contradiction
  without you.
Adding information didn't spoil the fact; it **un-closed** it. **More information that deepens a
contradiction increases retention; more information that resolves it kills retention.** Same words,
opposite effect.

### The precise boundary: REVEAL UP TO THE QUESTION, STOP BEFORE THE ANSWER
Name the questions the hook raises; do not answer them. The moment you explain the *why*, you've spent
the video. ❌ "…the reason is language models have no truth term, so they optimize for plausibility…"
hands over the intellectual payoff — loop closed, why stay?

### Loop-naming vs agenda-setting (they look alike; they're opposite)
- ❌ **Agenda-setting:** "Today we'll talk about AI in medicine and look at some studies." → announces a
  *topic*. A table of contents. No tension.
- ✅ **Loop-naming:** "how that's possible — and who gets to decide what we do about it." → crystallizes
  the *specific unresolved tension* into a question. A cliffhanger.
Naming a sharp question is one of the strongest ways to END a cold open. Announcing a topic is one of
the weakest. This is why "Today: how that's possible, and who decides" is GOOD while "today we're going
to explore…" is BANNED — one is a gap-pointer, the other is procedural.

### Two tests to run on any hook
1. **Prediction test:** Could a smart viewer accurately guess your conclusion from the hook?
   - Yes → you revealed the answer; pull it back.
   - They can't even guess the *question* → too vague; add concrete stakes.
   - They know exactly what's at stake but can't predict the answer → **perfect.**
2. **Fact-vs-meaning test:** Sort every hook sentence — fact/event/number (safe to give) vs
   interpretation/verdict/mechanism (withhold). If your hook contains *meaning*, you're spending the
   payoff early.

**One-line summary:** *Give them the locked door and let them see it's locked. Do not hand them the key.*

---

## 4. Retention THROUGH the video (not just the open)
- **End every scene on a pull** — a question, a reversal, a "here's the part nobody quotes." Never end a
  scene on a fully closed thought.
- **Plant a mid-video reversal** (~40–55% mark) to re-hook the natural fade point. (V6: "the humans
  hallucinate *more*." V5: "the tool didn't fail — the lawyers did.")
- **A new visual beat every 3–5s**; no static hold >5s (the QC gate enforces it). Vary the register.
- **Save the thesis/mechanism for the middle-to-late scene it belongs to** — the open only names it.

---

## 5. Shorts: 2 per video (the distribution wedge)
Shorts **bypass the cold-start wall** that long-form is stuck behind, so they're the fastest path to
subs for a small channel. **Every 8-min video gets 2 shorts (~60s, 9:16):**
- Terry records each short's VO in HeyGen on a blank screen; the operator builds the 9:16 short by
  **recutting the MAIN video's own visuals** (scenes + citation cards) to that VO, **burned-in
  captions** (most watch muted), ending on the title lockup + a "WATCH THE FULL VIDEO ▸" + SUBSCRIBE.
- Pick **2 distinct angles** so they don't cannibalize (e.g. story/mechanism vs thesis/verdict).
- Same hook rules as §3 apply to the first *second* of a short — even harder (swipe test).
See the V5 build: `SHORTS-V5.md` + `hyperframes-shorts/SHORTS-BUILD-SPEC.md`.

---

## 6. Packaging (reinforces retention by earning the click honestly)
- **Titles:** stakes + curiosity-gap; the punchier framings out-performed the cerebral ones 5–8× in our
  data. A/B two.
- **Thumbnails:** face + ≤6 words + one focal idea; dark navy/gold/cream system; no red-arrow chrome.
- **Chapters, pinned engagement-question comment, end-screen subscribe** every time.
- Prime **external warm traffic** (newsletter + one Reddit post + one X thread per video) — 0% external
  was our widest-open door.

---

## 7. IDEATION — choosing what to make (runs upstream of §1–§6)

§1–§6 make a video hold attention. **This section is about not spending that effort on a topic nobody
was going to click.** A perfectly executed hook on a dead concept still dies.

### 7.1 Rank candidates by OUTLIER SCORE, never by raw views

Raw view counts measure *the channel*, not *the idea*. A 500K-view video on a 2M-sub channel tells you
nothing — it got those views because the channel is large. The signal we want is **an idea that
outperformed its own distribution.**

> **Outlier score = views ÷ subscriber count of the channel that posted it.**
> 66K views on a 1K-sub channel = **50×** — that idea broke containment. 500K views on a 2M-sub
> channel = **0.25×** — that idea *underperformed*.

**Run it:** `python3 tools/outlier-scan.py` (canonical channel set baked in; `--refresh` to re-fetch,
`--all` to drop the recency floor). Writes `tools/outliers.csv`.

Method:
1. Assemble **≥15 competitor channels** in the AI-explainer / tech-explainer space, weighted toward
   channels our size or a little larger (their outliers are reachable; MKBHD's are not).
2. Pull each channel's videos with view count + the channel's sub count; compute the ratio.
3. Sort descending. **≥1.5× is a candidate concept** in this space — see the calibration note below.
4. Ignore the top-line topic; extract *why it broke out* — the tension, the stake, the framing.

> **CALIBRATION — the threshold is domain-specific, and 5× is wrong here.** The ">5×" figure came
> from the make-money-online / faceless niche where breakouts are far more extreme. On our actual
> competitor set (first run 2026-07-20, 366 videos since 2025-01-01) **exactly one video cleared 5×.**
> In technical AI-explainer content the realistic bands are: **median ~0.2–0.4× is normal, ≥1.5× is
> a genuine outlier, ≥3× is rare, ≥10× is a once-a-year event.** Recalibrate against a fresh run
> before trusting any threshold; don't import a number from another niche.

> **AGE CONFOUND — correct for this or the ranking lies.** Views accumulate over a video's whole
> life, but subscriber count is a **current snapshot**. So (a) an old video on a channel that has
> since grown scores spuriously high — a 2019 video divided by 2026 subs — and (b) a *recent*
> breakout scores spuriously LOW, because the subs it just earned are already in the denominator.
> The scan applies a 2025-01-01 floor by default, which kills (a). Effect (b) means recent high
> scores are **conservative**: a video that just did 12× probably did more than 12× at the time.
> On the first run, dropping the floor promoted a cluster of 2019–2020 math videos into the top 10 —
> pure artifact, and a good check that the filter is doing its job.

Why this matters for us specifically: we are a ~137-sub channel that is **retention-gated, not
quality-gated** (§0). Outlier scoring is the matching discipline on the input side — it finds ideas
that traveled *without* a subscriber base behind them, which is exactly our situation.

### 7.2 COMBINATION TITLING — fuse two proven concepts, don't clone one

Cloning a single outlier puts us in direct comparison with a video that already won, on a channel with
more authority. Instead, **take two independently-proven concepts and fuse them into one that doesn't
exist yet.** The result inherits demand from both parents while having no incumbent.

- The parents must be **independently proven** (each an outlier on its own) — fusing two dead ideas
  produces a dead idea.
- The fusion must be **specific**, not a broadening. `AI safety + jobs` is a category, not a concept.
  `the exam that licenses doctors` + `nobody can tell when it's wrong` → V6. That's a fusion.
- Prefer fusions that generate a **paradox**, because §3 says a paradox is a self-sealing loop. This is
  the real payoff of the technique: *the combination step is where the hook gets born.* A fused concept
  that contains a built-in contradiction hands §2/§3 a working cold open for free.

**Sequencing:** outlier scan (§7.1) → **teardown (§7.6)** → fuse (§7.2) → paradox test (§3) →
hook (§2) → script. If the fused concept can't be stated as a contradiction a viewer can't resolve
alone, fuse a different pair before writing a word of VO.

### 7.3 The "burning problem" filter

From the same source, and it survives scrutiny: prefer topics where the audience has a **problem they
are desperate to solve**, not one they're mildly interested in. Desperation drives clicking, finishing,
and sharing; curiosity alone drives only a click. For *Understanding AI*, the burning-problem
register is: **"is this coming for my job / my kid's education / my safety / my ability to tell what's
true"** — not "here's an interesting capability."

Corollary worth keeping: **low competition on a topic usually means no proven demand, not an open
lane.** Wanting to see competitors already succeeding on a theme is a feature. We want to enter a
proven conversation with a better frame — not invent an audience.

### 7.4 First-run result (2026-07-20): REGISTER beats topic

The first scan (17 channels, 486 videos; 366 after the recency floor) produced one finding that
matters more than any individual title it surfaced. Median outlier, recent window:

| register | channels | median |
|---|---|---|
| **Explainer / contrarian / mechanism** | Artem Kirsanov, Welch Labs, Internet of Bugs, bycloud, Dr Waku | **0.26 – 0.45×** |
| **AI news / hype / model-reaction** | AI Explained, Wes Roth, Matthew Berman, Two Minute Papers, The AI Advantage, TheAIGRID | **0.03 – 0.19×** |

**The news channels underperform their own subscriber base by roughly an order of magnitude versus
the explainer channels** — TheAIGRID's median is 0.03× against Artem Kirsanov's 0.45×, a ~15× gap.
Big sub counts are hiding the fact that the *ideas* aren't travelling. Their best-performing titles
are still hype-cased ("Google's SHOCKING…", "The 10 Most INSANE Things…", "Anthropic is coming for
EVERYTHING") and still top out around 0.25–0.48×.

**This validates the format we already run.** Byrddynasty's citation-card evidence-explainer sits in
the high-performing register. The strategic error would be drifting toward model-release reaction
content to chase volume — that's the register with the worst idea-travel in the entire set.

**What actually breaks out is NEGATION, not news.** Every top performer is a limit, a correction, or
a reversal — never an announcement:

| score | title | shape |
|---|---|---|
| **12.25×** | The AI Scaling Problem *(Edan Meyer, 80K subs, 985K views)* | the ceiling |
| 3.20× | How Your Brain Chooses What to Remember | mechanism |
| 1.96× | Your Favorite Science YouTubers Are Wrong About AI | consensus is wrong |
| 1.92× | The Brain's Learning Algorithm Isn't Backpropagation | negation of an assumed truth |
| 1.60× | ChatGPT "Physics Result" Reality Check | debunk |
| 1.02× | AI May DOOM humans After All. I may have been wrong. | public reversal |
| 1.01× | Yann LeCun's $1B Bet Against LLMs | insider defection |
| 2.75×¹ | AI can't cross this line and we don't know why | **limit + unexplained = paradox** |

¹ pre-cutoff (2024), shown because it's the cleanest paradox-shaped title in the corpus.

That bottom row is the template: **a hard limit that nobody can explain** is self-sealing exactly the
way §3 demands — the viewer cannot resolve it alone. Fusions (§7.2) should aim at that shape.

**Caveats, stated honestly:** Edan Meyer's 12.25× is **n=1** in the recent window (he posts rarely),
so treat it as a strong signal about the *shape* rather than a reliable channel-level benchmark. And
these outliers run 15–27 min against our retention-gated runtime rule (§1, revised 2026-07-29) — that
is **not** a licence to blind-ship long, because those are 30K–900K-sub channels spending trust we
don't have yet. §1 now permits >8 min *only* behind the whole-runtime-loop + spine precondition;
start ~10 and let the retention curve, not their sub count, earn the extra minutes.

### 7.5 Provenance and confidence — read this before trusting §7

§7.1–§7.3 were extracted on **2026-07-20** from a full-transcript review of the last 30 videos on
YouTube's `@makemoneymatt` (Matt Par). **That channel is a sales funnel** — he owns the tools he
recommends, most videos are sponsored, ~6 ideas are recycled across all 30, and much of his
algorithm commentary is unsourced folk claims (see the discard list below). It was mined, not trusted.

**Kept because it's mechanically sound and self-demonstrating** (he shows the technique producing his
own titles): outlier scoring, combination titling, the burning-problem filter, the
competition-as-demand-signal heuristic.

**Explicitly rejected from that source — do not import:** "trust points in the algorithm" from letting
an upload sit unlisted; "YouTube promotes videos with more ads"; "the top 100 YouTubers lost 50% of
views in a week"; "$50–100 per 1,000 views"; "every channel with 50%+ AVD uses this pattern"; "AI
avatars keep your channel safe"; "don't share your video with friends and family." All unsourced,
several arithmetically self-contradicting, all doing sales work.

**Independent corroboration worth noting:** his "re-hook every 60–90 seconds / open a loop and don't
resolve it" is the same mechanism as our §3 curiosity-gap rule, arrived at separately. Our §1 8-minute
runtime also matches his recommendation — but for a *different and better* reason: ours came from our
own retention data, his from mid-roll ad inventory. **No change to §1–§6 resulted from that review;
this section is the entirety of what was worth adopting.**

Raw transcripts, if the analysis ever needs re-auditing, were pulled with `yt-dlp` auto-captions
(all 30 available; no paid transcription needed).

### 7.6 TEARDOWN — reverse-engineer a proven video into a structural spec

§7.1 finds *which* ideas out-travelled their distribution. This finds ***why***, mechanically, so the
answer is a reusable shape instead of an impression.

> **The move: treat a proven video as a spec to be extracted, not a video to be admired.** Pull the
> winner apart — cold open verbatim, beat map, pacing curve, where the loop is named, where the
> reversal lands — then fuse that *structure* (§7.2) onto a different concept.

**Run it:** `python3 tools/teardown.py <url|id>` or `--from-outliers 5` to take the top N straight
from `outliers.csv`. Writes `tools/teardowns/<id>.md`. Captions only — free, no API key, no download.

Each teardown has two halves, and **the split is the whole design**:

| | |
|---|---|
| **EVIDENCE** (1–7) | Mechanical, from the script. Cold open verbatim, chapters or a 10% sample, the reversal window verbatim, timestamped loop-openers and negation markers *with their clauses*, a words-per-minute curve, and the packaging. The script never guesses at intent. |
| **ANALYSIS** (9 prompts) | Judgment, written by whoever reads the file. Hook shape (§7.4), fact-vs-meaning sort (§3), paradox test, where the loop is named and whether it's held or spent, the reversal, beat cadence, **transferable structure**, **fusion candidates**, and **do-not-import**. |

Rules that make the output worth having:

- **Answer #7 (transferable structure) in terms of MOVES, not topics.** "Opens on a number that
  contradicts its own title" is transferable. "Talks about scaling laws" is not. If a teardown's
  §7 bullets name the subject matter, it failed and should be redone.
- **Never fuse with an unproven parent (#8).** §7.2's requirement is unchanged: name the second
  parent *and its outlier score*. A teardown makes cloning easier, which is exactly the failure it
  has to be pointed away from — one outlier torn down and copied puts us head-to-head with a winner
  on a bigger channel.
- **#9 is not optional.** These videos run 15–27 min on 30K–900K-sub channels. Runtime, tangents,
  and assumed authority are things they can afford and we cannot; §1 does not move at our size.
- **The lexical markers are a place to LOOK, never a score.** `how`/`why`/`but` hits are printed with
  surrounding clauses precisely because density alone can't tell an opened loop from ordinary usage.
- **No captions = no teardown.** The cold open is the point. Either watch the first 45s with
  `/watch --end 45` or drop that candidate.

**Provenance:** the technique was lifted on **2026-07-21** from a Spanish AI-tools tutorial
(`youtube.com/watch?v=3h89eX-p5sE`) that used it in a different domain — pull the top-ranked ads off
Ad Forum, hand a winning ad to Gemini, ask for a spec, rebuild it with changes. **The mechanism was
kept and the implementation was not:** we already read the video ourselves, so routing it through a
second model to summarize it adds a lossy layer and no judgment. Everything else in that source
(auto-generate the story, speed-ramp clips to fit the VO — a direct contradiction of our
VO-anchored-timing rule, AI-generated everything) was rejected.

---

**Provenance:** V6 "When a Hallucination Could Kill You" and V5 "The Lawyer Who Trusted ChatGPT" are the
first two builds on this standard (`*-8MIN.*` files beside each original; `DECISIONS-8MIN.md` per video).
Related: `CITATION-CARD-FORMAT.md` (assembly), `HYPERFRAMES-LESSONS.md` (motion/QC), the growth plan.
