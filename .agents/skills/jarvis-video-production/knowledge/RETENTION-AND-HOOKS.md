# Retention & Hooks — the Byrddynasty standard (READ FIRST when scripting)

This is the **canonical playbook** for how Byrddynasty ("Understanding AI") videos hold attention.
It was derived on 2026-07-14/15 from the channel's real YouTube Studio numbers and applied to the V6
and V5 8-minute recuts. **Every video and every short follows it.** If any older doc (including this
skill's own "preferred runtime 10–15 min" line, now superseded) conflicts, this wins.

**§1–§6 are about executing a video well. §7 is about choosing which video to make — it runs
*upstream* of everything here, so read it first when the topic isn't already decided.**

---

## 0. The diagnosis that drives everything (from real Studio data)

Pulled from YouTube Studio, 2026-07-14 (channel = Byrddynasty · Understanding AI, our size):

- The channel is **alive and growing** (steady subscriber growth) — **not** a quality
  problem.
- **the large majority of viewers leave in the first ~30 seconds.** The best video still showed a low completion rate
  with a cliff in the first 30s; a weak one sat at well under a minute of average view duration on a 15-min video.
- Traffic was **effectively 0% Browse / Search / External** — i.e. the algorithm was **not distributing**
  the videos at all.

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

## 1. The runtime rule: ~8 minutes

**Target every video at ~8 minutes** (acceptable 7:30–9:00). Reasons:
1. **Strangers give an unknown channel ≤8 minutes, not 15.** Long-form is a *trust-gated privilege* —
   people reserve 15–20 min for creators they already know. At low subs, a 14-min video fights the
   retention math on hard mode.
2. **% viewed is what YouTube rewards**, and % viewed is structurally higher on a tight 8-min cut than
   a 15-min one carrying the same argument.
3. **8:00 also clears the mid-roll-ad threshold** (nice for later monetization; not the point now).

Recut existing 13–15 min videos to ~8 by trimming — keep every *verified fact*, cut redundancy,
example-parades, and throat-clearing. (V6 went 15:29→8:32; V5 went 13:00→8:30.)

---

## 2. The cold-open template (face-first) — every video, no exceptions

The opening exists to give the viewer **a reason to keep watching** by creating tension they can't
resolve alone. Structure:

1. **0:00 — FACE FIRST.** Terry's avatar ON CAMERA from frame one, delivering the hook. Never open on a
   dark abstract graphic. (You may punch in a 2–3s supporting graphic *beside/over* the face, but the
   face is present.) A human face stops the scroll and reframes "AI voice" as "a person is talking."
2. **~0:00–0:20 — THE HOOK.** The single most provocative concrete stake, as a **paradox** where
   possible (see §3). A number, a story, a contradiction.
3. **~0:20 — THE AVATAR JOKE (one line).** The witty self-ID — *"I am an avatar for Dr. Terry Byrd —
   he writes every word, I just say them…"* It disarms the AI-voice objection with personality. **Keep
   this. Cut everything else about the bio.**
4. **~0:20–0:35 — RE-OPEN THE LOOP.** End the intro on a **named question**, not the thesis.

> **DELETE FOREVER from openings:** the "38 years" bio paragraph, "on this channel we keep asking one
> question," "Welcome back to Understanding AI," "today we're going to explore / talk about…" — every
> line that tells the viewer the video hasn't started yet. It has. *Be* started.

Proven examples: V6 = "An AI took the exam that licenses American doctors — and beat them… Would you
let it treat someone you love?"; V5 = "A lawyer walked into federal court with a brief full of cases…
not one of them existed… he'd sworn they were real."

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

Method:
1. Assemble **≥15 competitor channels** in the AI-explainer / tech-explainer space, weighted toward
   channels our size or a little larger (their outliers are reachable; MKBHD's are not).
2. Pull each channel's videos with view count + the channel's sub count; compute the ratio.
3. Sort descending. **Everything above ~5× is a candidate concept.** Read the top ~30.
4. Ignore the top-line topic; extract *why it broke out* — the tension, the stake, the framing.

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

**Sequencing:** outlier scan (§7.1) → fuse (§7.2) → paradox test (§3) → hook (§2) → script. If the
fused concept can't be stated as a contradiction a viewer can't resolve alone, fuse a different pair
before writing a word of VO.

### 7.3 The "burning problem" filter

From the same source, and it survives scrutiny: prefer topics where the audience has a **problem they
are desperate to solve**, not one they're mildly interested in. Desperation drives clicking, finishing,
and sharing; curiosity alone drives only a click. For *Understanding AI*, the burning-problem
register is: **"is this coming for my job / my kid's education / my safety / my ability to tell what's
true"** — not "here's an interesting capability."

Corollary worth keeping: **low competition on a topic usually means no proven demand, not an open
lane.** Wanting to see competitors already succeeding on a theme is a feature. We want to enter a
proven conversation with a better frame — not invent an audience.

### 7.4 Provenance and confidence — read this before trusting §7

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

---

**Provenance:** V6 "When a Hallucination Could Kill You" and V5 "The Lawyer Who Trusted ChatGPT" are the
first two builds on this standard (`*-8MIN.*` files beside each original; `DECISIONS-8MIN.md` per video).
Related: `CITATION-CARD-FORMAT.md` (assembly), `HYPERFRAMES-LESSONS.md` (motion/QC), the growth plan.
