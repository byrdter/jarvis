# SCRIPTING — topic → researched VO script (PIPELINE Step 0)

How a topic becomes a 10–15 min VO script that is born **pipeline-ready** (so `split-heygen.py`
can ingest the recorded take with zero rework). The writing is collaborative and one-at-a-time;
this runbook makes the *scaffold* consistent: research method, channel voice, structure, fact-check,
and the handoff format.

> Output of this step = a `01-script/` folder + a `scenes.json`. Then Terry records the VO in
> HeyGen, and PIPELINE Step 1 (`split-heygen.py --spec scenes.json`) takes over.

## Step 0a — Research (one command)
Pull cited source material from the wikis (reuses the production FTS index; zero-dep):
```bash
python3 <skill>/tools/research-topic.py "your topic in plain words" --wiki ai-futures --top 15
```
Returns ranked passages with title, author, source, date, URL, **thesis_lens**, and a matched
snippet. Use the URLs as citations. The channel's non-academic corpus is `ai-futures`; cross-check
the academic folder for the same topic. Pick the strongest 6–12 sources; note which Show Bible
**lens** each serves. (Topic ideas already seeded in `…/strategic-pivot-launch/25-VIDEO-TOPICS.md`,
each tagged with its anchor source.)

## Step 0b — Voice + thesis (non-negotiable)
Read `…/strategic-pivot-launch/SHOW-BIBLE.md`. Hold to:
- **Thesis:** "Technology is neutral. Choices aren't." Every claim serves it.
- **Voice:** Dr. Terry Byrd — measured, explorer's tone. **Explore, don't predict.** Pose the
  trade-off; show the evidence; let the viewer weigh it. No hype, no doom.
- **Lenses (use 1 or combine):** power & choices · scenarios & trade-offs · strategic navigation ·
  meaning & identity · social consequences. Aim for the channel's lens balance over time (the
  meaning/identity lens is currently lightest — favor it when the topic allows).
- **Format templates** (case study, scenario exploration, etc.) live in SHOW-BIBLE "FORMAT TEMPLATES".

## Step 0c — Structure (pipeline-ready)
- **Length:** 10–15 min ≈ **1,500–2,200 spoken words** (~140 wpm). Don't pad; add evidence/examples.
- **Arc:** hook (a stop-you-in-your-tracks open) → body via the chosen lens framework → close that
  lands the choice back on the viewer.
- **Standard structure (Byrddynasty):** **avatar intro → body beats → CTA (penultimate) → avatar
  close.** The intro, CTA, and close are all spoken/recorded by the avatar. `scaffold-script.py`
  builds exactly this and **pre-fills the intro opener** ("I'm an avatar for Dr. Terry Byrd…") and the
  **full CTA** (subscribe · like · ring the bell) so you only write the body + close. Total ≈ 8–10
  scenes (6–7 body beats).
- For EACH scene, write a **distinctive first line** — the *anchor* `split-heygen.py` locates in the
  recorded take to split it. Unique and verbatim-stable; **don't reword after recording** (verify the
  anchors against the recorded VO, then split).
- The CTA + close are avatar; body beats are usually graphics (but can use any register — see
  VISUAL-SOURCING). Mark `avatar` in `scenes.json` accordingly (scaffold does this for you).

## Step 0d — Fact-check + claim-source map
Every meaningful on-screen/spoken claim needs a source (or be framed as interpretation). Fill
`claim-source-map.md` (scene · claim · source · url · confidence · lens). The research helper's URLs
feed this directly. Flag any claim too strong for its evidence and soften it.

## Scaffold the folder (one command)
```bash
python3 <skill>/tools/scaffold-script.py --project <project-dir> --topic "..." \
  --lenses "power-control,economic-futures" --scenes 8
```
Creates `01-script/` with `COMPLETE-SCRIPT.md` (script + [SCENE NN] markers + visual notes),
`VO-ONLY.md` (spoken words only — what gets recorded), `SCRIPT-STRUCTURE.md` (per-scene: lens,
~duration, first-line anchor, treatment idea), `claim-source-map.md`, and `scenes.json` (the
`split-heygen.py` spec skeleton). Then fill them in with the researched, voiced script.

## Handoff to production
1. `VO-ONLY.md` → Terry records in HeyGen → `heygen.mp4`.
2. Finalize `scenes.json` anchors to match the **recorded** first lines (verify, don't assume).
3. PIPELINE Step 1: `split-heygen.py --video heygen.mp4 --spec scenes.json --out …/hyperframes-v3/scenes`.
4. Continue PIPELINE Steps 2–9.

## Treatment foresight (helps Step 3 later)
While scripting, jot a treatment idea per scene (data-viz? diagram? B-roll? symbolic clip? breather?)
— see `knowledge/VISUAL-SOURCING.md`. Don't default everything to text/HyperFrames; plan ≥1 breather
and ≥1 symbolic beat. Query reusable visuals by meaning via the asset DB (`references/ASSET-CONTRACT.md`).
