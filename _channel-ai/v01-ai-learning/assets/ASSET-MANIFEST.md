# V01 — ASSET MANIFEST (scenes 03–07)

**The line that governs everything here:** anything offered as **evidence** is a real capture of a
real document. Anything **illustrative** is generated. A viewer must never have to guess which.

| | |
|---|---|
| 📄 **EVIDENCE — REAL** | Captured from the actual PDF at 200dpi. Never generated, never retouched. |
| 🎨 **ILLUSTRATION — GENERATED** | **Codex `image_gen__imagegen` (gpt-image-2), 1672×941, $0.** Carries no evidentiary weight. |

> ### Generation is free — never pay for it
> All 24 stills are generated through `codex exec` on Terry's ChatGPT subscription at **zero cost**.
> Prompts live in `prompts/*.txt`; `_gen.sh` regenerates any missing slug and skips what exists, so a
> run is resumable and the whole set is reproducible at any time for nothing.
>
> **These were first generated through the paid Higgsfield MCP (~3 credits) before checking for the
> free path — my error, 2026-09-07.** The paid set is archived in `alt-higgsfield/` (gitignored) and
> superseded. Rule now lives in `SKILL.md` and memory: **check for the free path before spending.**

---

## 📄 Evidence — 12 real captures from the papers

| File | Source | Use |
|---|---|---|
| `S1-barcaui-header` | *Soc. Sci. & Humanities Open* 12:102287 p1 | Scene 03 — masthead, DOI, dates |
| `S1-barcaui-design-fig3` | p5, Fig 3 | Scene 03 — **the 120 → 85 attrition flow** |
| `S1-barcaui-table2` | p6, Table 2 | Scene 03 — 6.85 / 5.75, t(83), d=0.68 |
| `S1-barcaui-fig4-dist` | p7, Fig 4 | Scene 03 — score distributions |
| `S2-fan-header` | *BJET* 56:489–530 p1 | Scene 03 — metacognitive laziness |
| `S3-bastani-header` | *PNAS* 122(26) p1 | Scenes 04 & 06 |
| `S4-cepr-cover` | CEPR DP21577 p1 | Scene 05 — **shows "Discussion Paper" on its face** |
| `S4-cepr-findings` | p3 | Scene 05 — the five findings |
| `S5-shen-header` | arXiv 2601.20245v2 p1 | Scene 07 |
| `S5-shen-fig1-patterns` | p2, Fig 1 | Scene 07 — **the six-pattern chart** |
| `S5-shen-results` | p9, §5.2.2 | Scene 07 — 4.15 pts, d=0.738, p=0.01 |
| `S6-zhu-header` | *Educ. Inf. Technol.* 30:16211 p1 | Scene 06 — the meta-analysis |

## 🎨 Illustration — 5 backgrounds + 17 b-roll stills

**Backgrounds** (one per scene, all distinct — satisfies the per-scene asset floor):
`s03-bg-library-dusk` · `s04-bg-turkish-classroom` · `s05-bg-exam-hall-overhead` ·
`s06-bg-tutoring-table-morning` · `s07-bg-dev-desk-night`

| Scene | B-roll | Note |
|---|---|---|
| 03 | `s03-a-desk-notebook-closed-laptop`, `s03-b-student-screenglow-typing`, `s03-c-empty-exam-hall-facedown`, `s03-d-calendar-45-days`, `s03-d2-calendar-crosses`, `s03-e-student-walking-away` | **use `d2`** — the original `d` has garbled AI text top-right; crop it out if used |
| 04 | `s04-a-teens-math-on-paper`, `s04-b1-laptop-closing`, `s04-b2-desk-absence`, `s04-c-whiteboard-half-erased` | **`b2` is the stronger read** — the empty desk and open palm |
| 05 | `s05-a-homework-late-night`, `s05-b-parents-at-gates`, `s05-c-graded-homework-stack`, `s05-d-corridor-time-passing` | |
| 06 | `s06-a-teacher-points-not-writes`, `s06-b-student-working-it-out`, `s06-c-stack-of-papers-26-trials` | **`s06-a` is the reversal's key image** — a hand pointing, the student's pencil still in the student's hand |
| 07 | `s07-a-dev-reading-carefully`, `s07-b-dev-moving-on-fast`, `s07-c-six-workstations-v2`, `s07-d-stopwatch-keyboard` | **use `v2`** — v1 rejected, kept as `_rejected-*` for the record |

**All 24 regenerated free via Codex on 2026-09-07 and swapped in** (`swap-in-codex.sh`).
Native 1672×941 (1.78:1) — marginally under the paid set's 2048×1152, immaterial for stills that are
punched into and animated rather than shown at native resolution.

### Quality pass — I looked at them, I did not trust the job status

**Paid set (Higgsfield), 8 inspected:** 5 excellent, 2 usable with a crop, 1 rejected.
- ❌ `s07-c` v1 — generic open office, readable terminal text, no distinct postures, poor diversity.
- ⚠️ `s03-d` — garbled AI text top-right. `d2` was generated clean.
- ⚠️ `s04-b1` — read as "closing a laptop," not "the tool being removed." `b2` is the better idea.

**Free set (Codex), 4 inspected — better on every one compared directly:**
- `s06-a-teacher-points-not-writes` — the pointing finger is unambiguous and the student's own pencil
  is visible at frame right. The reversal's whole argument in one image.
- `s04-b2-desk-absence` — the clean rectangle in the dust reads instantly; no VO needed to explain it.
- `s07-c-six-workstations-v2` — **six** distinct postures, varied people, and the monitors are pure
  abstract color fields with **no text at all**. Best version of this shot by a distance.
- `s03-bg-library-dusk` — real depth: brass lamps against blue dusk through tall windows.

**Conclusion: the free path is not a compromise.** It won every head-to-head.

---

## Motion: stills + HyperFrames, not generated video

These are **stills animated in HyperFrames** — slow push-in, parallax, Ken Burns, drift — all on the
registered `tl`. That satisfies the always-moving-bed rule, gives frame-exact control, keeps renders
deterministic, and costs nothing further. See `hyperframes-keyframes`.

Upgrade a specific beat to generated video only if a still cannot carry it. None in scenes 03–07
currently need it.

## ⚠️ On-screen labeling — required

`s05-b-parents-at-gates`, `s04-a-teens-math-on-paper` and `s07-c-six-workstations-v2` are
photorealistic enough to read as documentary photographs of the actual studies. **They are not.**

**Every generated image carries a small persistent `ILLUSTRATION` mark.** Not negotiable on this
channel: the video's entire claim is that the viewer can check what they are shown. An unlabeled
synthetic image that looks like evidence is the one thing that would cost more than it gains.

Real document captures carry the opposite mark — source, page, DOI.
