# AI lane scan — where to plant the flag

**Measured 2026-09-04.** 64 demand probes, 4 rounds, 1,479 result rows.
Raw data: `ai-lane-probe-2026-09-04.csv`. Tool: `jarvis-video-production/tools/demand-probe.py`.
Scoring: outlier = views ÷ the **posting channel's** subs, reachable band 1,000–300,000 subs,
shorts excluded, videos since 2025-01-01. Every verdict below was checked against its rows.

---

## 0. The one-line finding

**AI content travels when it names a physical or social OBJECT and a STAKE. It dies when it
promises a MECHANISM.** Measured on the same subject, same round:

| framing | verdict |
|---|---|
| "why ai makes things up" (mechanism) | **DEAD** — 0.00× median, top row 0.02× |
| "where does ai get its training data" (mechanism) | MIXED — the only hit is a how-to tutorial |
| "what an ai data center does to a town" (object + stake) | **PROVEN** — 8 hits, 2% drift |
| "ai layoffs are not really about ai" (social event + accusation) | 10 hits, 51.6× max |

This is the same diagnosis that came out of the Ordinary Economics slate on 2026-09-04, arrived at
independently on a completely different subject. It is now measured twice. Treat it as a law.

**Corollary: the object must be physical or social, never conceptual.** "The end of the open web"
→ DEAD. "Everything is an AI product now" → THIN. "AI is making decisions about your life" →
DEAD. Concepts do not have stakes; things do.

---

## 1. The three lanes that survived

Ranked by durability first, raw score second — because a lane whose hits all land in one month is
a crest, not a position.

### Lane A — "The stated reason is not the real reason" ⭐ RECOMMENDED

The corporate-AI accusation. A company says AI did something; the record says otherwise.

- **Hits: 10, spread across 8 different months over 14 months.** The most durable profile measured.
- Reachable and then some: **51.59× on 7,140 subs** · **45.34× on 29,500 subs (1.34M views)** ·
  3.87× on 12,000 · 2.28× on 253,000 · 1.57× on 187,000.
- Median winning channel **64,900 subs**, median runtime **12.1 min**.
- Representative winners: *"Tech Layoffs Are NOT About AI: An Insider View"* · *"Companies Are
  Lying About AI Layoffs — Here's the Proof"* · *"The AI Con: How Tech Giants Are Using Layoffs to
  Reset the Labor Market."*

**Why this one is yours.** It is the only lane on the list where 30 years in the field converts
into something a viewer can't get elsewhere: the ability to say *whether the company's technical
claim is actually true.* Everyone in this lane can be angry. Almost nobody in it can adjudicate.
That is judgment, not credential — see §3 on why the credential itself is worthless as a hook.

It also matches the WSM teardown finding already in the bible: an accusation frame (named actor +
adverse present-tense verb) is worth **+1.69× reach**, and it lifts the floor rather than the
ceiling — exactly what a 147-sub channel needs.

**Caveat, stated plainly:** the probe gate downgraded this query to INCONCLUSIVE on 69% drift.
I am overriding that downgrade because every surviving row is squarely on-thesis, and the tool's
own documentation says the relevance gate counts word overlap and cannot see topic, and that
suppressing real signal is the worse error. The rows are the evidence. They are listed in the CSV.

### Lane B — "AI is degrading something we all share"

Slop: the internet, YouTube, Amazon listings, search results, music.

- **"ai slop is everywhere"** — PROVEN, **0% drift** (the cleanest measurement in the entire scan).
  33.06× on **14,100 subs** (466k views) · 14.85× on 30,800 · 7.69× on 60,100 · 4.45× on 165,000.
- **"ai is ruining the internet"** — PROVEN, 5% drift, **8 hits spread across 8 separate months**.
  Median winning channel 61,050 subs, median runtime **16.0 min**.
- Reachable proof: 6.83× on 24,600 subs (168k views); 2.49× on 44,800 (112k views).

**Strength:** culture, not technology. Zero news peg, so it doesn't date. Evenest durability
profile in the scan.

**Watch the sub-format, not the lane.** *"AI generated books on Amazon"* returned 10 hits — and
**zero of them since May 2026.** All ten land between March 2025 and January 2026. That specific
instrument has decayed. The lane is alive; that particular object is used up. Pick a fresh object
each time (this is the Fireship half-life rule biting on a real example).

### Lane C — "AI made physical" — a standing lane

> **⚠️ CORRECTED 2026-09-04** — see `AI-GEOGRAPHY-CELL-2026-09-04.md`. This section originally read
> "6 of 8 hits land in July 2026 alone — a crest, not a plateau" and called Lane C a timed raid.
> **That was wrong**: it generalized one query's date distribution to a whole lane. Pooling every
> data-center hit across all 75 probes, deduped: **44 hits across 14 distinct months** (2025-03 →
> 2026-08), July at **31%**, not 75%. Lane C is a standing lane, not a closing window. Cui's
> follow-ups did decay, so a differentiated instrument still matters — the deadline does not.

Data centers, power, water, the town next door.

- Highest raw numbers anywhere in the scan: **10 hits, 1% drift** on "inside an ai data center."
- Reachable winners are real and large: Leo Cui **13.05× on 31,600 subs with a 40-minute atlas** ·
  MEP Academy 10.98× on 108,000 (1.19M views) · Wall Street Skinny 10.50× on 33,600 · High Yield
  13.46× on 122,000 (1.64M views) · Kiraa 8.60× on 47,200.
- Cui's own follow-ups decayed 13.05× → 0.78× → 0.12× across the next six weeks — the lane is standing, but a repeated instrument is not.
  follow-ups decayed 13.05× → 0.78× → 0.12× across the next six weeks.

Enter with a differentiated instrument — Cui's 40-minute whole-object atlas at 31,600 subs is the existence proof that it can be won.

**Ignore the two headline outliers here** (992× and 922×). The 992× is a 1,230-sub local news
channel covering a noise complaint; the 922× is **Applied Digital's own corporate channel**
marketing itself. Neither is a lane you can occupy. The middle of the distribution is the finding.

---

## 2. Killed with data — do not re-propose

| Lane | Verdict | The number |
|---|---|---|
| **AI decides things about you** — insurance denials, benefits, hiring, rent, government | **DEAD across the board** | insurance DEAD 0.07× · benefits DEAD 0.00× · "decisions about your life" DEAD 0.00× · hiring THIN · rent n=1 |
| AI in healthcare / diagnosis | DEAD | 0.01× median, top row 0.12× |
| Why AI hallucinates (mechanism) | DEAD | 0.00× median |
| AI companions / kids / teenagers | DEAD | 0.03× and 0.02× medians |
| AI companies stealing your work | DEAD | 0.03× median |
| The end of the open web | DEAD | 0.19× median |
| AI and your electricity bill (as a consumer framing) | THIN | 1.17× max, on a 10,400-sub channel |
| AI replacing *entry-level* jobs | THIN | narrowing "jobs" to "entry-level" collapses it |

**The insurance/benefits/hiring family deserves a note.** It is the most emotionally compelling
list on this page — algorithms denying ordinary people things they need — and it is
comprehensively dead. This is exactly the 2026-07-27 trap the probe tool was built to catch: low
competition read as an open lane when it is absence of demand. It would have been an entirely
reasonable thing to spend two months on.

### Two PROVEN verdicts that are traps

- **"why nobody can tell what is real anymore"** — PROVEN, 4 hits, 12.54× max. **Every winning row
  is about social behavior with zero AI content**: *"Why Nobody Knows How to Act in Public
  Anymore," "nobody knows how to talk anymore," "Nothing Feels Real Anymore."* Textbook confident
  false positive.
- **"we are not ready for superintelligence"** — PROVEN, but every winner is a **clip of a famous
  person** (Godfather of AI, Tom Bilyeu, Axios). That is a clip-farming lane, not an
  original-essay lane. The one original long-form entry scored 0.10×.

---

## 3. Your 30 years is not a hook — measured

You raised it, so it was probed.

- *"i have worked in tech for thirty years"* → MIXED, **0.01× median**
- *"someone who has watched ai for decades"* → **n = 0**, nothing on-topic in the reachable band

Nobody searches for it and nobody clicks it. It is not a lane, and it is not a title.

What it **is**: the thing that makes Lane A defensible once someone is already watching. The
credential belongs in the judgment — in being right about whether a company's AI claim holds up —
never in the hook. This is also already channel doctrine: the "38 years" bio line is on the
permanent-delete list in `video-production-standard.md` §2.

---

## 4. What the numbers say about size and shape

Across every surviving lane, consistently:

- **Winning channels are 10,000–120,000 subs.** Median winner in Lanes A and B sits near 45,000–65,000.
  These are not big-channel lanes. Reachable channels are pulling 400k–1.3M views.
- **Runtime 12–20 minutes**, median 16.0 in Lane B and 12.1 in Lane A. Clears the 8:00 monetization
  floor with room. The one 40-minute winner (Cui) is an atlas, and it beat everything around it.
- Every winner is a **general-audience** video. Not one developer-facing video appears in the
  reachable band of any surviving lane.

That last point is the direct answer to what you asked for: the measured lanes are the
non-technical ones. The technical-audience framing is not being suppressed by taste — it isn't in
the data.

---

## 5. What this does not fix

Lane choice is a distribution problem. The channel's measured problem is **retention** — 93,735
lifetime impressions at a healthy 3.69% CTR, and watch-time per video down 14× while CTR held
(`BYRDDYNASTY-CHANNEL-AUDIT.md`). A correct lane gets more people to click. It does not keep them.
The retention machinery — information-first cold open, withheld payoff across the whole runtime,
progress spine, reversal at 40–55% — still has to do its job. Nothing here replaces it.

---

## 6. Recommendation

**Plant the flag in Lane A, use Lane B as the second instrument, and run Lane C as a third.**

Lane A is the most durable measured, the most reachable, the shortest to produce, and the only one
where three decades in the field is a genuine and unfakeable advantage. Lane B keeps the channel
publishing when no corporate claim is ripe, and it has the cleanest measurement in the scan. Lane C
is real money right now and probably will not be in six months.

**Not settled here, and yours to call:** whether this runs on Byrddynasty as it stands or wants a
clean channel. The existing channel has 147 subs, a retention-gated history, and a back catalog in
a different register. Say which and the next step is titles — probed as shape families, never as
drafted titles, per the tool's own warning.
