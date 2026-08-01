# Three candidate beats — measured, 2026-07-31

> ## ⚠️ RECOMMENDATION SUPERSEDED 2026-08-01 by `BYRDDYNASTY-CHANNEL-AUDIT.md`
>
> **Still valid:** the probe measurements. The verdict-led-vs-mechanism-led split found here was
> independently reproduced by Byrddynasty's own CTR data, which makes it the most-confirmed finding
> we have.
>
> **Superseded:** the recommendation to commit to Beat A. These beats were derived from *external*
> channels. Byrddynasty's own export shows a proven register already exists on the channel —
> named real system + a number + a verdict — which outperformed everything measured here.

**Why a beat at all.** The scan of 2026-07-31 found that every channel we admire in the
near-future lane is a **single-beat** channel: Anastasi = semiconductors (115 videos), Species =
AGI risk scenarios (29), Logically Answered = tech-company post-mortems (194). None of them runs
topic discovery per video. "In-demand explainer topics are hard to find" is the characteristic
problem of a channel *without* a beat — and it is the same drift `video-production-standard.md` §8
records on the data-center build.

So: pick a beat, and let runtime and cadence follow. **Do not decide runtime first.**

Probed with `tools/demand-probe.py` (shape families, not publishable titles — see its docstring).
**Rows read, not just verdicts**, per the tool's own standing warning.

---

## BEAT A — "What AI Can Never Do" · the limits beat ✅ RECOMMENDED

Proofs, neuroscience, benchmarks, and structural failure modes. The claim is always of the form
*this is not a current limitation, it is a permanent one — and here is the proof.*

| Probe | Verdict | n | drift | median | max |
|---|---|---|---|---|---|
| why ai can never be conscious | **PROVEN** | 9 | 3 | 4.73× | **95.62×** |
| what ai will never be able to do | **PROVEN** | 4 | 12 | 4.42× | **69.00×** |
| the limits of what ai can do | INCONCLUSIVE | 2 | 14 | — | 69.60× |
| why ai cannot actually reason | INCONCLUSIVE | 1 | 22 | — | 0.04× |
| does ai actually understand anything | INCONCLUSIVE | 1 | 22 | — | 0.95× |

**Repeatability is demonstrated, not a single fluke — three separate channels have TWO hits each:**
- Universal Resilience (17.8k) — `Why AI Can Never Escape Turing's 1936 Proof` **69.0×** (22.8m) ·
  `Why AI Keeps Hitting Walls (and AGI is a Myth)` **12.6×** (10.7m)
- This Is The World (61.9k) — `Gödel's theorem debunks the most important AI myth` **6.3×** (31.9m) ·
  `AI Will Never Become Conscious | Sir Roger Penrose` **6.2×** (8.3m)
- Noema Magazine (25.8k) — `Why AI Will Never Become Conscious, According To Neuroscience`
  **81.8×**, 2.11M views, **70.2 minutes**
- Fractal Philosophy (132k) — `Things AI Will Never Understand` **6.0×** (45.2m)

**Discount the top row.** The 95.62× (`No, AI Isn't Conscious`, Decoded Genius Clips) is a **podcast
clip**, not a produced explainer — the same channel `outlier-ratchet.py`'s docstring already flags as
a flooder. The replicable evidence is Noema / Universal Resilience / This Is The World.

**This beat reproduced our own noun-split finding exactly.** "conscious" → 95.6×; "reason" → 0.04×;
"understand" → 0.95×. Same split measured 2026-07-29, independently reproduced today. **The word is
load-bearing. Title on *conscious / never / proof*, never on *reason / understand*.**

**⭐ This is the only beat where the hour format is evidenced.** Runtimes on the hits: 70.2m, 62.5m,
45.2m, 31.9m, 22.8m, 18.7m. Terry's instinct about depth and length is correct — *inside this beat.*

**Supply (my judgment, not measured — 25+ videos):** Gödel · Turing/halting · Chinese room · symbol
grounding · IIT and global-workspace neuroscience · Moravec's paradox · the reversal curse ·
out-of-distribution generalization · causal vs correlational inference · ARC-AGI · continual learning
· long-horizon agency · hallucination as structural not fixable · compositionality · sample
efficiency vs a child · tacit knowledge · embodiment · taste and judgment · novel science.

**Fit with our production system:** the best fit of the three. Every episode is a proof, a paper, or
a named researcher — i.e. cream citation cards, word-synced per §10.2, which is already built.
Evergreen by construction: a 1936 proof does not date. Persistent spine per §1 comes free — *the
claim → the proof → the strongest counterargument → the verdict.*

**Risk:** the lane attracts cranks (one probe row is Vedic quantum consciousness at 1.30×). Our
grounding rigor is the differentiator, but the neighbourhood is noisy — the visual register has to
signal "citation" within the first two seconds.

---

## BEAT B — "Run the Numbers" · the arithmetic debunk ⚠️ USE AS SUB-FORMAT, NOT AS THE BEAT

Take a claim everyone repeats, do the arithmetic on screen, show it's wrong.

| Probe | Verdict | n | drift | median | max |
|---|---|---|---|---|---|
| the math behind ai power claims | **PROVEN** | 9 | 6 | 0.47× | **24.70×** |
| engineer explains what ai really costs | INCONCLUSIVE (77% drift) | 3 | 20 | 5.04× | 22.29× |
| is the ai bubble real numbers | PROVEN | 9 | 7 | 0.54× | 2.46× |
| why ai companies lose money on every user | INCONCLUSIVE (77% drift) | 3 | 17 | 2.52× | 2.88× |
| how much power will ai need by 2030 | INCONCLUSIVE | 2 | 13 | — | 1.65× |

**The evidence concentrates on ONE template**, and it is close to unclaimed:
- Jovan EEN (12.3k) — `The Math Behind "AI Will Replace Engineers" Is Embarrassing` **24.7×**, 54.4m
- Mide (9.7k) — `Energy Engineer Explains: The Math Behind "AI Will Take Your Job" Is Laughably Wrong`
  **22.3×**, 31.0m
- Mide (9.7k) — `Process Engineer Explains: The Math Behind "Water-Efficient AI Data Centres"…`
  **5.0×**, 36.6m

Three hits, two independent channels, both under 13k subs, all 31–54 minutes. But note what
*doesn't* work: the **bubble/economics** framing sits at 0.54× median, max 2.46×. The winning
ingredient is **arithmetic against a specific popular claim**, not "AI finance."

**Why not the primary beat:** (1) only 3 hits from 2 channels — thinner evidence than Beat A;
(2) every episode is the same rhetorical move, which fatigues; (3) the credibility comes from a
*credentialed practitioner* doing their own field's math ("Energy Engineer", "Process Engineer") —
a faceless plural-voice channel has to earn that differently, via visible sourcing rather than a
named person.

**Verdict: run it as roughly 1-in-4 episodes inside Beat A.** "Can AI do X?" and "the number
everyone repeats about X is wrong" are the same beat wearing two hats.

---

## BEAT C — "What It's Doing To You" · self-relevant harm ❌ REJECTED IN THE FORM WE'D WANT IT

| Probe | Verdict | n | drift | median | max |
|---|---|---|---|---|---|
| ai took my job | **PROVEN** | 21 | 2 | 1.49× | 40.69× |
| they built a data center next to my house | **PROVEN** | 11 | 4 | 1.41× | 955.39× |
| what ai is doing to your electricity bill | **THIN** | 5 | 24 | 0.14× | 0.84× |
| an algorithm decided my application | INCONCLUSIVE (n=0) | 0 | 19 | — | — |
| what ai companies know about you | INCONCLUSIVE | 1 | 19 | — | — |

On paper this is the strongest lane measured — `ai took my job` returned **21 on-topic rows with
only 2 drift**, the cleanest signal in the whole probe set. **Read the rows and it collapses:**

- 40.69× `AI took my job as a translator. I'm starting over at 39` — 7.2k subs
- 17.94× `I Lost My Job to AI` · 12.80× `I lost my $200,000 job... now what?` · 11.02× `AI Took My Job…`

**Every hit is first-person memoir with a protagonist.** The demand is for *a person's story*, not
for analysis. A faceless channel in first-person plural structurally cannot make these — and §2's
stop-condition test hasn't fired, so we're not reversing faceless to chase it.

And the 955.39× headline is a mirage: **Piedmont Media, 1,120 subs, 1.7 minutes** — local TV news
footage of a community noise complaint. Not a format; a local-virality accident. The reachable rows
under it are 10.4× and 9.4×, both ordinary infrastructure explainers.

`electricity bill` is genuinely THIN (0.14× median, 24 drift, zero hits) despite feeling self-relevant.

**This refines §8's "self-relevant story" heuristic:** a *story* needs a protagonist. Where a lane's
demand is carried by testimony, a faceless analytical channel cannot enter it — it can only cover the
*mechanism* behind it, which is Beat A/B territory anyway.

---

## Recommendation

**Commit to Beat A. Run Beat B as ~1-in-4 inside it. Drop Beat C.**

Then let the format follow the beat, in this order:
1. Ship 4–6 episodes at **20–30 min** — the band where Universal Resilience, This Is The World and
   Species all live. Do *not* open at 70 minutes.
2. Read the retention graph at the 10-min mark, per §1.
3. Only if it holds past ~40% do we go to the Noema 45–70 min shape.

Cadence: Species runs a 23-day median gap and Anastasi 12 days — both far tighter than the
"monthly" impression. **Every 2–3 weeks is the evidenced cadence**, not monthly.

**Open question worth one probe before committing:** whether the *pluralised* voice survives this
beat. Every Beat-A hit is either a named authority (Penrose, a neuroscientist) or an essayistic
publication (Noema). Noema is the proof that no on-screen person is required — worth a teardown
(`tools/teardown.py`) of that 70-minute video before we build.
