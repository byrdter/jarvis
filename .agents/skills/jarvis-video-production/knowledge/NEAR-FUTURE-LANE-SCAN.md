# The near-future analysis lane — channel scan (2026-07-31)

**Question asked:** are there channels doing *Logically Answered*-grade effort but aimed at the
**near horizon** — things already underway whose consequences land in 1–5 years?

**Method (artifact-grounded, not listicle-grounded):**
1. Blind YouTube `search.list` sweep, 16 register-specific queries, 359 videos → 155 channels.
   **Contaminated as predicted** by `outlier-ratchet.py`'s documented caveat: "this is already
   happening and nobody noticed" pulled an entire music lane (The Marías – *No One Noticed*) at
   137–193×. Keyword search cannot classify topic. Sweep used for *lead generation only*.
2. Named-candidate verification: 49 channels resolved via `channels.list`, last 25 uploads pulled,
   shorts (<180s) dropped, outlier = views ÷ subs computed per video.
   Quota: 1,615 + 158 units.

Raw data: `tools/raw-probe/` companions — `nearfuture-videos.csv`, `nearfuture-channels.csv`,
`verified-channels.json` (scratchpad; re-runnable from `verify-channels.py`).

---

## Tier 1 — the actual answer (near-future + rigor, beating their own size)

| Channel | Subs | Med × | Max × | Med runtime | Register |
|---|---|---|---|---|---|
| **AI In Context** | 412k | **7.89×** | 26.6× | **40 min** | Near-future AI, one argument per video, no news pegs |
| **Species \| Documenting AGI** | 395k | **2.04×** | 28.0× | 18 min | "A realistic scenario" — near-future by construction |
| **Anastasi In Tech** | 497k | 1.00× | 2.4× | 20 min | Semiconductor near-horizon; what ships in 18 months |
| **Rational Animations** | 468k | 0.75× | 1.3× | 15 min | Animated near/mid-future AI reasoning, nonprofit-funded |

**AI In Context is the single closest match to the brief** and the strongest performer found.
15 videos total, 4 long-form in the sample:
- `We're Not Ready for Superintelligence` — 34 min, **10.96M views** on 412k subs (26.6×)
- `If you remember one AI disaster, make it this one` — 39 min, 4.05M
- `This best-selling book is freaking out national security advisors` — 43 min, 2.46M
- `You really should, unfortunately, be worried about Sam Altman.` — 40 min, 1.50M

**Caveat, stated plainly:** that 7.89× median is computed over **4 long-form videos**. It is a real
outlier, not a large sample. Species is the more *replicable* evidence — 29 videos, consistent
18–41 min, median 2.04×, holding across a real catalogue.

## Tier 2 — adjacent method, different subject (steal the method)

| Channel | Subs | Med × | Med runtime | Why it's here |
|---|---|---|---|---|
| **Perun** | 638k | 0.54× | **58 min** | Defence procurement. Slide decks, no face, hour-long. Proves the ceiling on "boring rigor" is very high |
| **Modern MBA** | 814k | 0.27× | 38 min | Financial teardowns; near-future industry verdicts |
| **Internet of Bugs** | 132k | 0.47× | 10 min | Credentialed contrarian; explicitly debunks near-future AI claims |
| **New Mind** | 750k | 0.27× | 22 min | Engineering-history method, aimed backward — the register without the horizon |

## Tier 3 — micro-channel worth watching (format is stealable)

**Mide** — 9.6k subs, 67 videos, median 0.03× — but:
- `Energy Engineer Explains: The Math Behind "AI Will Take Your Job" Is Laughably Wrong` — 31 min,
  **216k views on 9.6k subs = 22.5×**
- follow-up, same template: `Process Engineer Explains: The Math Behind "Water-Efficient AI Data
  Centres" Is Laughably Wrong` — 36 min, 46.8k (4.9×)

Everything else on that channel sits at 200–1,000 views. **The format is the outlier, not the
channel.** Template: *credentialed practitioner runs the arithmetic on a widely-repeated
near-future claim and shows it's wrong.* Two for two.

## Named and rejected — the anti-pattern

**AI Upload** (108k, med 0.53×) — `Ex-OpenAI Employee WARNS: "You Have No Idea What's Coming In
2027"`, then the same title with *Whistleblower*, *Scott Galloway*, *Ex-Google Exec*, *Eric
Schmidt*. Near-future *topic*, zero near-future *analysis*. This is the lane
`video-production-standard.md` §0 already says we cannot win, wearing horizon clothing.

---

## What the data says that we did not already have

1. **This lane runs LONG.** Every Tier-1/2 winner: 18–58 min. The 10.96M-view video is 34 minutes.
   Nothing in the near-future-analysis register performs at 8 min. This is direct evidence for
   `video-production-standard.md` §1's own precondition — the payoff withheld across the whole
   runtime — and against treating 8 min as the target here.
2. **Logically Answered itself runs 0.29× median.** The reference channel is *not* the outlier
   performer. Tier 1 beats it by 3–27×. Retrospective business teardowns are a saturated register;
   the horizon register is not.
3. **"A realistic scenario" is a title primitive.** Species uses it repeatedly and it works
   (`72-Hour AI Takeover: A Realistic Scenario`, `The First 48 Hours of an AI Civil War`). It
   satisfies §3's curiosity-gap rule structurally: facts are given, the *outcome* is withheld, and
   the frame is self-sealing.
4. **Credentialed-arithmetic debunk is an unclaimed micro-format** (Mide, 22.5× and 4.9×), and it
   sits directly on this channel's existing strength — grounding every claim.

## Not verified (handle resolution failed — absence of evidence, not evidence of absence)

Undecided with Matt Ferrell · Wendover Productions · Sabine Hossenfelder (uploads playlist 404) ·
Gary Marcus · ChinaTalk · 80,000 Hours · Low Level Learning · Matt Wolfe · AI Search.
Re-run with corrected handles or channel IDs before concluding anything about these.
