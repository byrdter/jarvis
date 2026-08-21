# Which topics in our lane actually have native footage

**Measured 2026-08-21** with `tools/archival-search.py --limit 25` across 14 candidate topics.
Raw JSON in `tools/raw/lanefootage/`. Prompted by `SNAPSHIFT-CHANNEL-TEARDOWN.md` §8.6, which found
that Snap Shift's 0.77 uploads/day is downstream of picking a subject the world already films — and
raised the obvious question about our own lane.

---

## 0. The finding

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
4. **Only then:** probe demand.

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
as a P1 bug (see §5). C-SPAN alone certainly has substantial AI-hearing footage; treating that zero as
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

---

## 5. Method defects found while doing this

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
