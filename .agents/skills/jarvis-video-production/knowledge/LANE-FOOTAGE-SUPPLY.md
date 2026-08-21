# Which topics in our lane actually have native footage

**Measured 2026-08-21** with `tools/archival-search.py --limit 25` across 14 candidate topics.
Raw JSON in `tools/raw/lanefootage/`. Prompted by `SNAPSHIFT-CHANNEL-TEARDOWN.md` §8.6, which found
that Snap Shift's 0.77 uploads/day is downstream of picking a subject the world already films — and
raised the obvious question about our own lane.

---

## 0. The finding

> **SUPPLY (§1): the split is SITED vs. ABSTRACT** — 11 of 14 candidates have deep donor pools, and
> every one of them has a physical place a camera can stand.
>
> **DEMAND (§5): that is a supply test and NOTHING MORE.** Measured, footage-richness does not predict
> audience at all — the richest footage ecosystem in the set (port automation) is **DEAD**, and exactly
> **one** lane comes back PROVEN: the data-center **community-harm** angle, at 969×, which we already
> found in July 2026 and never built. Read §5 before acting on §1.
>
> Original §0, kept because §1 still stands as a supply finding:
> **The split is not "AI topics vs. non-AI topics." It is SITED vs. ABSTRACT.** Every topic that
> returned a deep donor pool has a **physical place you can point a camera at** and **somebody with a
> standing reason to point one there**. 11 of 14 candidates saturated the probe. The ones that did
> not are the document-and-argument-shaped topics — which is exactly where this channel has
> historically lived.

So the answer to "what has footage" is not a list to memorise, it is a **test to apply** (§2).

---

## 1. What saturated

All 11 hit the 25-row ceiling with on-topic results, so **their ordering is meaningless** — the probe
capped out. The meaningful fact is that they capped out at all.

| topic | distinct filming sources | news/outlet | indie/trade |
|---|---:|---:|---:|
| AI diagnostics in hospitals | 25 | 5 | 20 |
| AI drive-thru ordering | 25 | 16 | 9 |
| robotaxi on public streets | 24 | 5 | 20 |
| data-center buildout + local opposition | 23 | 14 | 11 |
| warehouse automation displacing workers | 23 | 9 | 16 |
| grid strain from AI load | 23 | 6 | 19 |
| chip fabs + export controls | 22 | 10 | 15 |
| self-driving trucking | 21 | 10 | 15 |
| port automation vs longshoremen | 21 | 4 | 21 |
| AI in classrooms | 21 | 11 | 14 |
| offshore call-center displacement | 16 | 21 | 4 |

### 1.1 Four filming pipelines, and what switches each one on

The `news` vs `indie` split above is not decoration — it tells you *which* pipeline is feeding a
topic, and therefore what the footage will look like and how reusable it is.

1. **Local news** — switches on when there is a **community conflict or a local business story**.
   Data centers pull CBC, ABC7NY, KSL Utah, WKRN, CHCH, CBS Boston, PBS NewsHour. Drive-thru AI pulls
   KTLA, FOX 35 Orlando, WGN, WTHR, WEAR. Classrooms pull FOX5 Vegas, KGUN9, WALB, LEX.
   *This is the pipeline that matches our consumer-felt anchor most directly.*
2. **Trade / occupational communities** — switches on where a **job** is involved. Port automation is
   the purest case: 21 of 25 sources are indie — `Eric The Longshoreman` (3 videos), `Cranedaddy`,
   `laborvideo`, `Propeller Club`. Trucking has `Smart Trucking`; radiology has practising
   radiologists (`Juan | Certified Rad`, `Kevin Jubbal, M.D.`, `Justin Shafa, M.D.`).
3. **Corporate promo** — switches on where a **vendor wants to sell it**: Waymo, Tesla, Aurora,
   Brightpick, Intel Newsroom, Samsung Semiconductor, Cleveland Clinic, NHS Alliance, NVIDIA Developer.
4. **Foreign / state broadcast** — offshore call-centre displacement is 21 of 25 news because the
   **Philippine broadcast ecosystem covers it as domestic economic news**: One News PH, ABS-CBN (×3),
   PTV Philippines (×3), NET25, ANC 24/7. Also CGTN, New China TV, Al Jazeera, VOA.

**The practical read:** a topic with a *trade* pipeline gives you process footage and real workers but
no narrative spine; a topic with a *local news* pipeline gives you conflict, faces and stakes but
short clips; a topic with only a *corporate* pipeline gives you clean, glossy, and untrustworthy
b-roll. The strongest topics above have at least two pipelines running.

---

## 2. The test to apply to any future topic

Before committing to a subject, ask in order:

1. **Is there a SITE?** A place a camera can stand — a warehouse floor, a dock, a reading room, a
   substation, a drive-thru lane, a road. If the answer is "a filing" or "a model's behaviour," stop.
2. **Who already has a standing reason to film it?** Name the pipeline (local news / trade / corporate
   / foreign broadcast). If you cannot name one, there is no supply, regardless of how important the
   topic is.
3. **Is more than one pipeline running?** One pipeline is a thin, homogeneous donor pool.
4. **Only then:** probe demand — and see §5.4, because this test predicts supply ONLY. It says nothing
   about whether anyone will watch, and two of the topics that pass it hardest are measured DEAD.

---

## 3. The rights trade this implies — read before acting

**The usable supply is AMBER, not GREEN.** The GREEN (free-to-use) tier is nearly worthless for these
topics: `commons` and `archive.org` returned PDFs, congressional reports, 1924 issues of *Nation's
Business*, and — for "AI copyright litigation" — *Lady Epping's lawsuit, a satirical comedy in three
acts*. This is exactly the drift `archival-search.py`'s own docstring warns about ("titles, never bare
counts"), and it means **the GREEN row counts must not be read as supply**.

Real supply is copyrighted third-party video: local news, trade channels, corporate uploads. That is
the **same rights posture as Snap Shift** (`SNAPSHIFT-CHANNEL-TEARDOWN.md` §8.4) — fair-use dependent,
with the same claim exposure. Moving into these topics means accepting that trade knowingly, or
budgeting for licensed stock. It is not a free upgrade.

---

## 4. What is NOT measured — do not read these as zero

**Three topics returned 0 YouTube rows and remain UNMEASURED:** congressional AI hearings, deepfake
fraud + scam calls, AI copyright litigation.

The zeros are **HTTP 429 throttling**, not absence. Running 14 topics back-to-back exhausted the
shared YouTube API quota; a retry after a 4-minute cooldown returned 429 again, so this is a **daily**
quota, not a short window. `archival-search.py` serialises a throttled provider as `[]` with only a
stderr warning, so in `--json` output **a rate-limit is indistinguishable from a true zero** — filed
as a P1 bug (see §6). C-SPAN alone certainly has substantial AI-hearing footage; treating that zero as
a finding would have been wrong.

**Re-run all three after the quota resets before drawing any conclusion about them.**

Prediction on the record, to be checked rather than assumed: hearings should score **high** (C-SPAN
is a deep, effectively-public-domain pipeline — the one GREEN-tier exception in this whole document),
while copyright litigation should score **low** (US federal courtrooms bar cameras, so there is no
site to film). If the retry contradicts that, the §2 test needs revising.

**The demand axis was not run at all.** `demand-probe.py` raises on the same 429. So this document
measures **supply only** and settles nothing about whether these topics are worth making.

### 4.1 The hypothesis the demand run should test

Supply and demand may substantially **coincide** in our lane, because our measured anchor —
consumer-felt, `feedback_footage_is_a_floor_not_a_lever`, rho +0.51 — means *it happens somewhere a
person goes*: a drive-thru, a classroom, a hospital, a road, a warehouse. Those are sites, and sites
are what local news films. If true, the consumer-felt rule and the footage-supply rule select nearly
the same topics, and topic selection collapses to one decision instead of two.

**This is a hypothesis, not a result.** It is exactly the kind of tidy convergence that turns out to
be wrong, and it must be tested with `demand-probe.py`, not adopted.

> **TESTED 2026-08-21 → REFUTED. See §5.** Supply and demand are close to orthogonal. It was indeed
> exactly the kind of tidy convergence that turns out to be wrong.

---

## 5. THE DEMAND AXIS — run 2026-08-21. The §4.1 hypothesis is REFUTED.

> **§4.1 predicted that footage-rich and consumer-felt would select nearly the same topics. They do
> not. Supply and demand are close to orthogonal.** The single richest footage ecosystem in the whole
> set — port automation, 21 of 25 sources being longshoremen filming their own work — is **DEAD** on
> demand: median 0.00×, max 0.19×, n=11. Meanwhile *AI copyright litigation*, which has no filmable
> site at all, comes back **MIXED** and outscores it.
>
> Having a filming community is not having an audience. A trade films itself for itself.

### 5.1 Raw verdicts

`demand-probe.py`, channels 1K–300K subs, ≥1.5× = hit, since 2025-01-01, shorts excluded.

| verdict | n | drift | median | p75 | max | hits | query |
|---|---:|---:|---:|---:|---:|---:|---|
| PROVEN | 9 | 1 | 0.75× | 10.60× | **969.89×** | 3 | data center built next to my house |
| PROVEN | 8 | 2 | 0.48× | 6.50× | 200.95× | 2 | AI taking fast food jobs drive thru |
| PROVEN | 8 | 0 | 0.24× | 10.60× | 14.44× | 2 | data centers raising electricity bills |
| MIXED | 10 | 2 | 0.28× | 0.49× | 17.60× | 1 | self driving trucks replacing truck drivers |
| MIXED | 6 | 1 | 0.16× | 0.37× | 17.66× | 1 | AI replacing call center workers |
| MIXED | 13 | 1 | 0.08× | 0.13× | 1.83× | 1 | AI copyright lawsuit authors books |
| THIN | 4 | 19 | 0.47× | 0.82× | 0.82× | 0 | AI replacing radiologists doctors |
| THIN | 6 | 3 | 0.43× | 0.73× | 1.04× | 0 | chip factory jobs america semiconductor |
| THIN | 6 | 7 | 0.03× | 0.08× | 1.23× | 0 | robotaxi replacing uber drivers |
| **DEAD** | 3 | 3 | 0.03× | 0.17× | 0.17× | 0 | warehouse robots replacing workers |
| **DEAD** | 11 | 5 | 0.00× | 0.02× | 0.19× | 0 | port automation dockworkers jobs |
| INCONCLUSIVE | 2 | 25 | – | – | – | – | AI in schools students teachers |
| INCONCLUSIVE | 2 | 27 | – | – | – | – | congress hearing AI testimony senators |
| INCONCLUSIVE | 1 | 6 | – | – | – | – | deepfake scam victims lost money |

### 5.2 Two of the three PROVENs do not survive reading the rows

The tool's own rule — *"on-topic rows are the evidence, not the median"* — matters here. Reading them:

- **`AI taking fast food jobs drive thru` — PROVEN is an ARTIFACT. Discard it.** Both hits are drift
  the relevance gate let through on the token "McDonald's": *"If Michael Jackson Applied To Work At
  McDonald's…"* (200.95×, a comedy skit) and *"The Evil Design of McDonald's Drive-Thru"* (6.50×,
  about queue psychology, not AI). The genuinely on-topic rows run 1.25× / 0.83× / 0.14× / 0.08×.
  **Real verdict: THIN.**
- **`data centers raising electricity bills` — PROVEN is NOT INDEPENDENT.** Both hits (14.44×, 10.60×)
  are general data-center explainers that also matched the previous query — the same two videos
  counted twice. The genuinely bill-specific rows are 0.28× / 0.24× / 0.23× / 0.21×.
  **Real verdict: THIN.**
- **`data center built next to my house` — this one is REAL.** *"Data center noise at Great Oak
  community outside Manassas"* — **Piedmont Media, 1,200 subs, 1,163,866 views, 969.89×.** A tiny
  local outlet with a million-view video about noise in a neighbourhood. Squarely on topic.

### 5.3 The surviving finding replicates something we already knew

That Manassas result is not new. `video-production-standard.md` §8 already records, from 2026-07-30:
community harm — *"what it does to the town next door"* — measured as a **MONSTER at 955× / 13.4×**.
This run measured **969.89× / 14.44×** on the same angle from a different tool and a different search
index. **Independent replication of a recorded finding, ~18 months of catalogue apart.**

So the honest net of the whole two-axis exercise:

> **One lane is PROVEN — the data-center *community harm* angle — and we found it a year ago and did
> not build it.** Everything else in the sited/footage-rich set is THIN, DEAD, or artifact. The
> footage-supply screen did not surface a single new proven topic.

### 5.4 What actually predicts demand — the anchor, restated correctly

The pattern across the table is not sited-vs-abstract. It is **whose life is affected**:

| | topic | verdict |
|---|---|---|
| **the viewer is affected** | a data center appears in *your* neighbourhood | **PROVEN 969×** |
| someone else's job | warehouse workers | DEAD |
| someone else's job | dockworkers | DEAD |
| someone else's job | radiologists | THIN |
| someone else's job | truck drivers | MIXED |
| someone else's job | chip-fab workers | THIN |

This is `feedback_footage_is_a_floor_not_a_lever` (consumer-felt anchor, rho +0.51) confirmed again —
and it corrects **my** §2 framing. "Is there a site?" is a *supply* test and nothing more. It has no
predictive power over demand, and §2 must not be read as a topic-selection rule on its own.

### 5.5 Method deviation — read before citing these numbers

**This run did not use `demand-probe.py`'s own fetch path.** The YouTube Data API `search` endpoint
was quota-exhausted (§4), so results were pulled from **vidIQ** and written into demand-probe's cache
format; the tool then computed every verdict with its own drift filter, reachable band, and
thresholds. **Verdict logic is canonical; the row set is not.** vidIQ's index and ranking differ from
the Data API's, so a canonical re-run may return a different sample.

Other limits, stated plainly: band n is small (1–13), three topics are INCONCLUSIVE on drift, and the
two discarded PROVENs show the relevance gate passing off-topic rows on a single shared token. **Treat
§5.3 as the one durable result and re-run canonically to confirm.**

---

## 6. Method defects found while doing this

1. **`timeout` does not exist on macOS.** The first sweep wrapped every call in `timeout 180`, which
   failed with `command not found` and wrote 14 empty JSON files. They looked like 14 clean zeros.
   Use `gtimeout`, or no timeout.
2. **Silent 429 in `archival-search.py`** — filed P1. `demand-probe.py` gets this right (it raises);
   `localnews` and `archives` return `[]`. The module docstring already mandates the correct behaviour
   for Wayback ("a throttle can never be misread as no snapshots"); the rule needs extending to every
   provider.
3. **The 25-row cap flattens the ranking.** `--limit` bounds rows *per provider*, so any topic with
   real supply saturates and all saturated topics look identical. To rank the top 11 against each
   other, raise the limit substantially or count distinct donors at a fixed larger depth. **Do not
   report the §1 ordering as a ranking** — it is a pass/fail.
