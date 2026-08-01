# State of the evidence — channel-direction testing, 2026-07-31

> ## ⚠️ PARTIALLY SUPERSEDED 2026-08-01 by `BYRDDYNASTY-CHANNEL-AUDIT.md`
>
> **Still valid:** the shape-family probe results (§1, §2) and the verdict-led-beats-mechanism-led
> finding. Those were independently reproduced by Byrddynasty's own CTR data.
>
> **Superseded:** every conclusion about *which channel* and *what to build*. The premise that
> Byrddynasty lacked algorithmic distribution came from `video-production-standard.md` §0 — a
> document — and is false. Measured: **93,735 impressions at 3.69% CTR**, four times KeyAdvances'
> impressions at a better click-through rate.

Nothing here is a decision. This is the scoreboard after one day of measurement: 4 teardowns,
41 demand probes, 1 discovery sweep, 1 channel-history pull.

---

## 1. The headline: PROPHECY → RECEIPTS did not survive its own probe

It was proposed off the Mackard teardown (73.03×) as the format primitive to rebuild around.
Probed as a shape family, it is **the most crowded and lowest-yielding lane measured today.**

| Shape family | n (on-topic) | drift | **median** | max | verdict |
|---|---|---|---|---|---|
| `whatever happened to` | 25 | 2 | **0.32×** | 43.42× | PROVEN — *but off-topic* |
| `hype vs reality ai` | 22 | 3 | **0.47×** | 17.85× | PROVEN |
| `what happened to the metaverse` | 14 | 0 | **0.84×** | 25.37× | PROVEN |
| `ai pilots failing enterprise` | 7 | 0 | 0.03× | 20.63× | MIXED |
| `the technology that was supposed to change everything` | 6 | 3 | 0.02× | 2.30× | MIXED |
| `predictions that aged badly` | 6 | 8 | 0.28× | 0.54× | THIN |
| `companies that bet on ai and lost` | 3 | 14 | 0.03× | 0.28× | **DEAD** |
| `why the ai rollout is failing` | 3 | 5 | 0.04× | 0.07× | **DEAD** |
| `we were told ai would replace` · `the ai revolution that never happened` · `whatever happened to self driving cars` · `the promise that never arrived` | 1–2 | — | — | — | unmeasured |

**Read against the rest of the day, the pattern is unambiguous:**

| Family | n | median |
|---|---|---|
| `what ai gets wrong` | 4 | **16.17×** |
| `why ai can never be conscious` | 9 | **4.73×** |
| `what ai will never be able to do` | 4 | **4.42×** |
| `what happened to the metaverse` | 14 | 0.84× |
| `hype vs reality ai` | 22 | 0.47× |
| `whatever happened to` | 25 | 0.32× |

**The prophecy families have the MOST on-topic rows and the LOWEST medians.** That is the signature
of a saturated lane — many makers, low typical return. The verdict families have fewer makers and
several times the typical return.

**So Mackard's 73.03× is the tail of a crowded distribution, not the type of it.** The inference
that the retrospective frame carried that video does not survive. What more likely carried it: the
**self-relevant stake** (developers' jobs), the **citation density**, and the **specificity** — and
note it was found under `what ai gets wrong`, the 16.17×-median family, not under a prophecy query.

Two supporting details that kill the generic version outright:
- `whatever happened to` at 43.42× is **The Monkees**; 14.22× is **Tina Turner's children**. Zero AI.
  The primitive belongs to a nostalgia/celebrity lane. Logically Answered's `Whatever Happened To
  Wish.com?` works because he is already inside a business-postmortem beat — not because the phrasing
  travels.
- `ai pilots failing enterprise` at 20.63× is a **VC podcast** with 1,350 subs. Every other row in
  that family: 0.00×–0.08×.

**Where it retains value:** `what happened to the metaverse` returned **14 on-topic rows with ZERO
drift** and all-produced small-channel entrants (TheCollapseCo 19.6k → 25.37×, ItsLuve 2.09k →
6.78×). A *specific* dead prophecy is a real lane. The *generic* prophecy frame is not.

## 2. What has survived every test today

**Shape families — measured twice or with low drift:**
- `why ai can never be conscious` — PROVEN, 4.73× med / 95.62× max, 5 hits, drift 3. Probed in two
  separate runs. **Strongest survivor.**
- `what ai will never be able to do` — PROVEN, 4.42× med / 69.00× max
- `what ai gets wrong` — PROVEN, 16.17× med / 73.03× max — **stake-dependent**: 73.03× on *your job*,
  0.13× on *AI art*, identical phrasing
- `the math behind ai power claims` — PROVEN, 24.70× max, two independent micro-channels (<13k subs)

**Teardowns — two replicable produced-faceless models, no borrowed authority:**

| | Mackard | Universal Resilience |
|---|---|---|
| runtime · subs · outlier | 8:12 · 39.5k · **73.03×** | 22:49 · 17.8k · **69.61×** |
| title | verdict-led (*Going Horribly Wrong*) | verdict-led (*Can Never Escape*) |
| open | 8 data points in 44s | date + authority + claim in 8s |
| stake | your job | your everyday experience (progress bars) |
| citations | every ~15–20s | dense |
| reversal | [4:12] = 51% — escalates the **stake** | [9:37] = 42% — concedes, then escalates |
| spine | 8 chapters ≈ 60s each | ladder of escalating limits |

**Their five shared properties are the actual finding of the day:** verdict-led title · a
self-relevant or identity stake · dense citation · an authored reversal at 40–55% · **no borrowed
authority**.

## 3. The borrowed-authority confound — appeared four separate times

Noema 81.81× (live panel, Anil Seth) · Decoded Genius Clips 95.62× (podcast clip) · Perimeter
Institute 20.17× (Veritasium lecture) · TRIGGERnometry 12.18× (Jimmy Carr clip) · plus 3 of 6 rows
in `hype vs reality ai` (Mark Cuban, Steven Kotler, a Meta VP).

**A large share of this lane's biggest numbers come from putting a famous person on screen.** We
cannot copy that. Every headline figure must be checked for it before it is used as evidence — it
has already produced one wrong recommendation today (see §4).

## 4. Corrections logged today

1. **"Noema proves a faceless produced essay can hold 70 minutes."** Wrong — it is a live panel with
   borrowed authority whose cold open is verbatim the §2 DELETE FOREVER list.
2. **"This lane runs long; start at 20–30 min."** Withdrawn — the long runtimes cited were the
   borrowed-authority videos. Produced-faceless: 8:12 → 73.03×, 22:49 → 69.61×, 45:12 → 6.06×. The
   **original ~8–10 min discipline in `video-production-standard.md` §1 is what the evidence backs.**
3. **Six of ten proposed titles led with a mechanism.** All probed DEAD or THIN. Mechanism-led dies;
   verdict-led proves.
4. **"Rebuild around prophecy → receipts."** Did not survive its own probe (§1 above).

**The meta-pattern worth noting: each of these came from theorising a format off a single artifact,
then measuring afterwards.** The probe caught all four. That is the apparatus working — but the
order should be reversed. Probe the family first, theorise second.

## 5. Honest position

- **The beat is still standing.** The limits/verdict lane is the only thing that has survived
  every test, and it survived two independent probes.
- **The channel concept built on it is not.** The boundary-ledger framing, its MOVED rung, its
  runtime recommendation and its ten titles have all been measured and mostly failed.
- **Nothing should be committed yet.** What exists is a proven *lane* and two teardowns of
  replicable *executions*. What does not exist is a probed set of specific episodes.

**Cheapest next test:** probe 8–10 shape families *inside* the surviving verdict lane — before any
more concept-building. If a majority prove, the beat is real at episode level and worth a pilot. If
they scatter like the title set did, the lane is real but too narrow to carry a channel, and that is
worth knowing before anything gets built.
