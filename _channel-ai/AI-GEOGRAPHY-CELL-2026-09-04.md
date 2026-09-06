# The AI × geography cell — and a correction

**2026-09-04, round 8.** The eight unrun probes are finished plus three AI × geography crossings.

**Route change, declared:** the YouTube Data API was still returning 429 at 10:30 Pacific (reset is
midnight, ~13 hours out). These eleven probes ran through **vidIQ search** instead, which returns
`viewCount`, `subscriberCount`, `publishedAt` and `duration` — every field the probe needs. Results
were scored by importing `demand-probe.py` and calling its own `verdict()` and `drift_filter()`
functions unchanged: same 1,000–300,000 band, same ≥1.5× hit threshold, same 90-second shorts floor,
same 65% drift downgrade. **Different transport, identical scoring.** Cost 55 of 142 vidIQ credits.

---

## 1. ⚠️ A correction to what I told you yesterday

I said Lane C (AI data centers) was **"a crest, not a plateau — 6 of 8 hits land in July 2026 alone"**
and told you to treat it as a timed raid with a closing window.

**That was wrong, and it was wrong for a reason worth recording.** It came from a single query whose
phrasing — *"what an ai data center does to a town"* — pulled recent news coverage. I generalized from
one query's date distribution to a lane.

Pooling **every** data-center hit across all 75 probes run this week, deduped by video ID:

| | |
|---|---|
| Hits (≥1.5×, ≤300k subs) | **44** |
| Distinct months with a hit | **14** |
| Span | 2025-03-06 → 2026-08-14 |
| Share in July 2026 | **31%**, not 75% |
| Median hit-channel size | **33,600 subs** |
| Median runtime | 12.8 min |

Monthly: `2025-03 ██ · 06 █ · 07 █ · 10 ██ · 11 █ · 12 ███ · 2026-01 █ · 02 ████ · 03 ██ · 04 █ ·
05 ██ · 06 ████████ · 07 ██████████████ · 08 ██`

**This is a lane with a hit in every month for eighteen months**, rising through 2026. Whether July is
a true peak or a surfacing artifact cannot be settled here — recent videos haven't accumulated views
yet, and the documented age confound works *against* them, so August's 2 is not evidence of decline.
Either way, "cresting, ship within weeks" was not supported. **Lane C is not a timed raid. Treat it as
a standing lane.**

---

## 2. The AI × geography crossing — measured

| Query | Verdict | Drift | Hits | Best reachable rows |
|---|---|---:|---:|---|
| **where ai data centers are being built** | **PROVEN** | 6% | **4** | 10.99× on 108,000 (1.19M views) · 2.19× on 291,000 · 1.80× on 240,000 |
| **why africa is building data centers** | **PROVEN** | **3%** | 2 | **33.69× on 14,200** (478k views) · **12.43× on 134,000** (1.67M views) |
| which country controls the world's chips | MIXED | 3% | 1 | 3.64× on 85,300, 22.0 min |
| who owns the undersea internet cables | MIXED | 1% | 1 | only hit is a 2.1-min engineering short |
| **which countries actually own the internet** | **DEAD** | 8% | 0 | 0.02× median — top row 0.21× |

**You named three cells. One is strong, one is mixed, one is dead.**

- **Data centers: live, and the strongest cell in the crossing.** Note *what wins* inside it —
  *"They Aren't Building AI Data Centers. (It's Way Worse)"* and *"The AI Data Center Crisis is Worse
  Than You Think."* Those are **Lane A accusation shapes** pointed at a physical object.
- **Africa specifically is excellent** — 3% drift, both hits reachable, both huge. *"Why Capital Is
  Flooding Into Africa's Data Centers"* did 478k views on **14,200 subs**.
- **Chips: the winning framing is the negation.** Not "which country controls chips" but
  *"Why NO Country Can Build AI Chips Alone"* — 3.64× on 85,300 subs at 22 minutes.
- **"Who owns the internet" is dead.** 0.02× median. The internet has no location, so the geography
  doorway has nothing to open onto. Same law, ninth confirmation this week.

---

## 3. The five remaining shape probes

| Query | Verdict | Best reachable row |
|---|---|---|
| why america cannot build anything anymore | PROVEN, 2 hits | **14.62× on 203,000 subs — 2.97M views**, "Why Only Three Countries Bother Building **Ships** Anymore" |
| why nobody can compete with china | PROVEN, 2 hits | 8.31× on **1,720 subs** (17.3 min) · 3.99× on 243,000 (**48.9 min**) |
| how one country beat america at its own game | MIXED, 1 hit | 1.93× on 1,600 subs |
| the country that quietly won | INCONCLUSIVE | 17 dropped; surviving rows are Chinese drama serials |
| why this country banned it | DEAD as a format | results are almost entirely sub-60s geography listicles |

**Note what rescued "America can't build anything."** Both hits are about **ships** — a concrete
object. The abstract framing drifts to cost-of-living content and dies. Once again: name the object.

---

## 4. The synthesis — the overlap cell is real and it is the data center

You asked for the cell where the Lane A material and the Asian Boss format overlap. It exists, it is
narrower than the whole crossing, and it is unusually well evidenced.

Read the 44 pooled data-center hits by title and the pattern is unmistakable:

> *You're being lied to about electricity and AI data centers* · *Why Tech Companies Are Quietly
> Cancelling AI Data Centers* (12.43×) · *Why Tech CEOs Are Quietly Cancelling Their AI Plans*
> (**81.77×**) · *They Aren't Building AI Data Centers. (It's Way Worse)* · *$700 Billion Spent.
> $100 Billion Back. The AI Math Doesn't Math* · *How AI Became More Expensive Than The Workers It
> Replaced* (**15.35×, 1.99M views on 130,000 subs**) · *The Math Behind "AI Will Take Your Job"*
> (25.77×) · *Debunking the Biggest Myth About AI Data Centers*

**The data center is already where most of Lane A's proven titles live.** It is the one AI object
that has a street address — which means it simultaneously satisfies the object-and-stake law, the
accusation frame, the arithmetic-debunk shape, *and* the geography doorway. Four independent findings
from this week land on the same object.

And the format fits: median hit runs 12.8 min, but the long tail is exactly the AB Explained band —
41.0 min *(Why Energy Experts are Concerned About AI Data Centers)*, 40.3 min *(The Entire AI Data
Center Explained)*, 39.3 and 38.7 min *(Ed Zitron)*, 36.6 and 31.0 min *(the two engineer
arithmetic videos)*.

### What that makes the first video

The strongest-evidenced opening move on the board: **an arithmetic-debunk of a data-center claim,
30–40 minutes, built from licensed news, permit filings, utility rate cases and source-credited
captures.** It needs no travel, no original location footage, and no on-camera presenter to establish
the object — because the object is a building with a public paper trail.

**Africa is the sharpest untaken angle in it.** 3% drift, both hits reachable and huge, and it is the
one geography where the data-center story is being told as capital flow rather than as local nuisance.

---

## 5. Standing caveats

- **Route:** eleven probes came via vidIQ, not the YouTube Data API. Scoring is identical, but the
  underlying search ranking may differ from the API's. Cross-check the two winners on the API path
  when quota resets, before committing production time.
- **Verify pegs against primary sources.** Everything above is demand measurement, not fact-checking.
- **The pooled recency analysis is post-hoc** across queries chosen for other purposes. It is strong
  enough to retract "cresting"; it is not a clean time series.
