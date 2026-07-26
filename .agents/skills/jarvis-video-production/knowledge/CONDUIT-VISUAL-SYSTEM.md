# The Conduit Visual System — what a Byrddynasty video looks like

**Status:** current standard, faceless mode. Derived from the **Messi / "Secretly an AI Investor"**
master (2026-07-26) — the reference build. Read with `CITATION-CARD-FORMAT.md` (assembly + QC
mechanics) and `RETENTION-AND-HOOKS.md` (scripting). The `.claude` mirror is
`.claude/rules/video-production-standard.md`.

This doc answers: *what do I put on screen, when, and why that and not a text card.*

---

## 1. Positioning — why variety is the strategy, not decoration

The nearest faceless competitor is **AI Explained** (400K+ subs): fact-based, fact-*showing*, roughly
80% of screen time is document pull-outs with highlighted passages. It works, and it has a long head
start.

**We use that device but must not be that channel.** Our position is *more entertaining, equally
rigorous*. The differentiator is the **component library in §4** — a document capture is one
instrument in the kit, not the format. If a finished video is mostly full-frame source captures, we
have built a weaker version of a channel that already owns that lane.

Rough target: **source captures ≤ 35% of runtime.** The rest is the conduit treatment — tables,
schematics, maps, HUDs, timelines, grids, splits — carrying the same evidentiary weight in a form
that moves.

### The evergreen constraint
A good share of the catalogue should still be worth watching **a year out**. That shapes visuals as
much as scripting:
- Anchor on **mechanism**, not this week's number. Where a dating figure is load-bearing, stamp it
  (`REPORTED · FEB 2026`) so it reads as a record rather than as current.
- Prefer **structures** that stay true (how a cap table works, what a paper mark is) over **states**
  that won't (what something is worth today).
- Avoid on-screen furniture that ages: "this week," "just announced," live counters.

---

## 2. The two registers

Every surface belongs to one of two, and mixing them inside a beat is a defect.

### Cream document register — EVIDENCE
Bone paper `#F4F1EA` · serif display head · letterspaced mono kicker · hairline rules · label/value
rows · circular seal or stamp. Slight push-in permitted.

Carries: filings, licences, certificates, agreements, notes-to-valuation, real source captures.
**Job:** *this is on the record.*

### Dark navy panel register — ANALYSIS
Deep slate on `#0A0E14` · gold `#E0B84A` primary · teal `#5AD1D1` secondary · serif head, white ·
mono numerals · letterspaced mono kickers ≥26px.

Carries: cap tables, dossiers, dockets, portfolios, comparisons, charts, HUDs.
**Job:** *this is what it means.*

**Accent discipline:** one brand accent per scene; a second colour only at a deliberate comparison
split. Assign accents per-video in the ASSET-PLAN (Messi: gold = wealth, teal = AI, green = the one
money beat, steel-blue = the European contrast).

---

## 3. The bed contract

Both registers sit over a **photographic or video bed** that is darkened and defocused so the card
reads.

- The bed **always** carries ambient motion — a slow Ken-Burns drift, a live clip, or particle
  movement. A frozen bed is a render failure, not a style.
- The bed must not compete: scrim it, but **not past the luminance floor**. Where content has not yet
  landed, use the `.soft` scrim variant rather than the default or `.deep`.
- **Beds are atmospheric by definition** — they count against the 10% budget in §6 *only* when the bed
  is the entire visual. A bed under a denotative card is denotative.

---

## 4. The component library

Named so they can be *instantiated*, not re-derived per scene. Each has a job and a motion signature.

| component | job — the beat it serves | motion signature |
|---|---|---|
| **Document card** | a claim is on the record | slides/scales in, stamp lands, slow drift |
| **Profile / dossier row** | introduce an entity | label/value rows fill in sequence |
| **Data table, one row lit** | this actor among others | rows populate; the subject row lights last |
| **Numbered grid, ghosted slots** | a set, partially known | filled slots resolve; unknown stay ghosted |
| **Stat hero** | one number is the point | count-up + kicker above + italic aside below |
| **Browser / search chrome** | what the public can see | query types with caret; page resolves under it |
| **Annotation / eval HUD** | how a system actually works | boxes acquire, queue scrolls, meters fill |
| **Timeline / funding chart** | chronology, growth | axis draws; callout card rides the line |
| **Schematic map + docket** | place, territory, holdings | region lights; docket entries reveal beside it |
| **Comparison split** | two paths, two verdicts | book-open from opposing wings |
| **Stacked papers, sequential** | a list of dismissals | items reveal in order, stamped as they land |
| **Constellation / hub** | one centre, many positions | nodes spring to a ring, connectors draw |
| **Landing card** | the line to remember | full-frame text — **titles and landings only** |

**A plain full-frame text card is permitted only as a title or a landing.** Every other beat picks a
component whose job matches it.

---

## 5. The signature device — progressive disclosure with ghosted placeholders

Unrevealed rows are **visible but dimmed**, then resolve. It tells the viewer how much is still
coming and makes a list feel like a reveal rather than a dump. It appears throughout the reference
build (the dismissal stack, the portfolio grid's empty slots, the holdings docket) and is the closest
thing the channel has to a proprietary move.

**Hard limit: content must resolve within ~1.2s of the panel appearing.** Held longer, the ghosted
state reads as a dead frame. This was the *only* real defect the QC gate caught on the reference build
— three times, at 50.5s, 448.5s and 479.5s. Ghost opacity ≥ `.40` over a dark panel; below that it
disappears rather than teases.

---

## 6. VO binding — the 90/10 rule

**≥90% of runtime DENOTATIVE:** the visual illustrates the specific claim being made *at that second*.
Numbers, names, dates, documents, places, relationships — show the thing being said.

**≤10% ATMOSPHERIC:** loosely related or purely tonal. Permitted at **transitions and breathers** —
e.g. a clip of someone working at a screen while bridging topics. Deliberate and budgeted, not filler.

**Never atmospheric on a beat carrying a number, a date, a name, a citation, or a verdict.**

Classify every beat `DEN` or `ATM` in the beat map. A scene that can't say which isn't planned.

---

## 7. Density — measured, not adjectival

Target **45–60 visual change-events per minute** at scene-detect threshold 0.02.

Measured baselines from the reference build:

| | events/min |
|---|---|
| cold open (strongest) | 56.8 |
| mid-video evidence scene | 44.0 |
| weakest scene | 28.9 |

Prefer **within-beat motion** — fields populating, counters running, stamps landing, beds drifting —
over rapid cutting. That is what makes the register read as continuous rather than choppy, and it is
the channel's deliberate choice.

```bash
ffmpeg -v error -i SCENE.mp4 -vf "scale=320:-2,select='gt(scene,0.02)',metadata=print:file=-" \
  -an -f null - 2>/dev/null | grep -c scene_score
```

---

## 8. The scene skeleton

Every scene decomposes into five layers. Specify each, or it gets improvised:

1. **Bed** — clip or still; scrim variant; drift range.
2. **Primary surface** — the component from §4 carrying the beat.
3. **Secondary elements** — kickers, chips, annotations, callouts.
4. **Evidence** — the cream card, if this beat has one, and the exact VO phrase it lands on.
5. **Camera** — push-in, hold, or cut, with its range.

Plus a **beat table**: cue phrase → visual event → layer → duration → `DEN`/`ATM`. The beat table is
generated from the build, not maintained beside it (`PIPELINE.md`).

---

## 9. QC — what must pass before Terry sees anything

1. `scene-validator.py` — determinism gate. `0 errors`, no exceptions.
2. `deadspace-scan.py` — render failure (near-black / blown-white) only, per-scene **and** on the
   assembled master. Its old `mean<22` dead-space threshold sat at this register's *median* luma
   and flagged half a good video; corrected 2026-07-26, do not restore it.
3. `beatmap.py ghosts` — the ghosted-hold gate. Every ghost resolves within ~1.2s; nothing resolves
   from below 0.40 opacity.
4. `beatmap.py check` — beat-map drift gate; the map must match the build.
5. **Card presence:** frame at each citation cue reads mean-luma > 200.
6. **Card integrity:** read the rendered PNG. A quote must not be truncated mid-clause. Verify against
   pixels, never against the manifest that describes them.
7. **Beat-gap check:** no interval > ~5s without a cued visual event.

---

## 10. Considered and rejected

- **Cut-on-twos / 12fps quantisation** — deliberately choppier; fights the chosen continuous feel.
- **Chromatic aberration, heavy grain over text** — degrades the citation legibility that is the moat.
- **Halftone / paper-texture grade** — belongs to a paper-collage register we don't use.
- **Mostly-document format** — that is AI Explained's lane; see §1.

*Open for a one-scene experiment:* **footage homogenization** — a shared treatment pass so library
clips, generated stills and HyperFrames output stop looking mismatched at cuts. This is the one idea
from the Vox-craft teardown that genuinely applies here.
