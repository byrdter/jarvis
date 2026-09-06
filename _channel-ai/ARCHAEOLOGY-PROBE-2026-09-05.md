# The archaeology round — hypothesis mostly falsified, one cell survived

**2026-09-05.** 26 probes across two rounds (YouTube Data API).

**Hypothesis under test:** from the digital-transformation round, two survivors were *object + history*
(a 30-minute fax-machine history, 3.78× on 3,430 subs; "Why Everything In Britain Now Requires An
App," 8.54× on 1,910 subs) while every *complaint* framing died. Proposed law: **archaeology travels
where grievance dies.**

**Result: mostly wrong.** Reported as measured.

---

## 1. Where the archaeology framing failed

Five queries returned PROVEN or MIXED and **every one is a false positive** once the rows are read.
This is the documented failure mode — the relevance gate counts word overlap and cannot see topic.

| Query | Verdict | What the "hits" actually are |
|---|---|---|
| the history of the atm | PROVEN, 0% drift, 3 hits | **ATM heist stories.** 17.00× is a Turkish TV clip; 12.71× is *"Inside the Hyderabad ATM Gang Heists"*; 1.14× is a UK crime documentary. The genuine history row — *"ATM Explained: How It Works and The History Behind The Machine"* — scores **0.07×** |
| what happened to the phone book | PROVEN, 2 hits | 5.95× is *"Gen-Z Replaces Phone with Books"*; 2.04× is a Christian ministry documentary. The real ones: **0.07×** and **0.01×** |
| the history of the barcode | MIXED, 0% drift | 40.00× is a 2.5-min QR-vs-barcode short. The actual history video: **0.10×** |
| why old software still runs the world | PROVEN, 3 hits | the top hit is a **MapleStory** video |
| how the cash register was invented | MIXED | 4.12× is an employee-theft story |

And the direct contrast control **did not** support the hypothesis: *"the history of the atm"* and
*"why atms are disappearing"* both fail once read — archaeology didn't beat complaint on that object,
they both lost to crime content.

**Cleanly dead on their own terms:**

- *the history of the self checkout* — **DEAD, 0.08×.** Too young to have archaeology.
- *why we still use fax machines* — **THIN.** The 3.78× row that generated this hypothesis **did not
  replicate** under a different phrasing of the same object.
- *why do checks still exist* · *why receipts still exist* — **n = 0** on-topic in band.

---

## 2. The one cell that survived — and it is clean

**"why banks still run on cobol" — PROVEN, 2% drift, 4 hits, and every row is on-thesis.**

| × | views | subs | runtime | video |
|---:|---:|---:|---:|---|
| **30.00×** | 135,302 | **4,510** | 9.9m | The Code that Runs the World |
| **28.85×** | 48,176 | **1,670** | 10.4m | COBOL: The Language Your Bank Is Afraid to Touch |
| **13.44×** | 46,765 | **3,480** | 11.5m | Why Banks Still Run on Code from 1959 |
| **7.76×** | 22,972 | **2,960** | 1.8m | Why 95% of ATMs Still Run on 60-Year-Old Code |
| 0.45× | 7,641 | 16,900 | 9.8m | Why Banks Still Run on a Language Declared Dead in 1985 |
| 0.31× | 3,087 | 10,000 | 12.6m | Why Banks Still Run Code From 1959 |

Four hits on channels of **1,670 to 4,510 subs**, pulling 23k–135k views, spread across four separate
months (Aug 2025 → Jun 2026). This is the **most reachable clean result in the entire scan** —
smaller winning channels than any lane measured this week.

**Note the two failures at the bottom.** Near-identical titles on *larger* channels (16,900 and
10,000 subs) scored 0.45× and 0.31×. The shape is proven; it is not automatic.

---

## 3. ⚠️ But every abstraction of it is dead

This is the important half. Round 2 tried to generalize the COBOL result. All of it failed:

| Query | Verdict | Evidence |
|---|---|---|
| why nobody can replace this software | **DEAD** | 0.07× median |
| legacy systems are a time bomb | **DEAD** | 8 on-topic rows, **2% drift**, 0.08× median — cleanly measured, cleanly dead |
| what happens when the old programmers retire | **DEAD** | 0.03× median |
| **air traffic control still uses floppy disks** | **DEAD** | **11 on-topic rows**, 0.02× median — a famous story, and it is dead |
| the software holding up the economy | INCONCLUSIVE | **n = 0** |
| ai is being used to rewrite old code | INCONCLUSIVE | n = 2 |
| the system nobody knows how to fix | INCONCLUSIVE | n = 1 |
| the last people who understand this machine | INCONCLUSIVE | n = 1 |

**"COBOL" works. "Legacy systems" does not.** The proper noun with a date attached is load-bearing;
the category is not.

---

## 4. The law, confirmed again

This is now the **tenth** independent confirmation this week, and the sharpest yet because the two
sides are the same subject:

| Named object with a date | Category |
|---|---|
| **COBOL, 1959** — 30.00× | *legacy systems* — DEAD |
| **the data center** — 44 pooled hits | *who owns the internet* — DEAD |
| **ships** — 14.62× | *America can't build anything* — drifts and dies |
| **the Netherlands and food** — 6.71× | *Germany is falling behind* — INCONCLUSIVE |

**Archaeology alone is nostalgia, and nostalgia is weak.** What made COBOL work is not that it is
old — it is that it is **still load-bearing right now**. *"The Language Your Bank Is Afraid to
Touch"* is present tense, has a defendant, and names a stake the viewer is exposed to today. The
phone book has no stake. Self-checkout has no history. COBOL has both.

So the refined rule is not *archaeology beats grievance*. It is:

> **A named thing, with a date, that something you depend on is still standing on.**

---

## 5. What this means for you

**The good news is specific and it is yours.** Legacy modernization is core digital-transformation
literature — the thing you actually researched. And the one archaeology cell that measured alive is
exactly that cell. It also connects forward: AI-assisted COBOL modernization is a live enterprise
push, so the object sits at the intersection of your background, the DT literature, and AI.

**The honest caution: this is one video's worth of proven demand, not a channel.** Four hits, n=9,
one narrow object, and its own generalizations are dead. Do not build a "legacy tech" lane on it —
that abstraction measured DEAD at 0.08%.

**Also note the runtimes: 1.8 to 12.6 minutes.** This cell is *short*, unlike the 30–50 minute
arithmetic band. If you build it, build it short — and do not stretch it to hit a runtime target.

**Unchanged recommendation:** the primary build is still the AI-and-learning arithmetic in the
brain/cognition lane. The COBOL cell is a strong, cheap, reachable **second** video — and the one
place your research background converts directly into an object that measures.
