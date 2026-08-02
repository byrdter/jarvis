# Shared YouTube Development Workflow

This is the channel-independent development core. Load the active channel profile before using it.
The profile changes the topic universe, audience promise, brand assets, and channel baselines; it does
not replace this workflow. KeyAdvances work uses [channel-profiles/KEYADVANCES.md](channel-profiles/KEYADVANCES.md).

## Gate 0 — Channel Profile and Issue

1. Load the channel profile and state the channel name in `EPISODE.md`.
2. Create or claim the beads issue.
3. Initialize the command center:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

Do not inherit another channel's topic rules, thumbnail assets, CTA, cadence, Shorts policy, or
performance baseline merely because both channels use this production system.

## Gate 1 — Demand Evidence

Do not spend full-research or production effort on an unmeasured idea. A candidate passes when at
least one of these is documented in `YOUTUBE-PACKAGE.md`:

1. the same conceptual demand appears as an outlier on at least **two independent channels**;
2. the concept fuses **two independently proven parents**, each with its own evidence; or
3. the active channel's first-party data already proves the title/subject register.

For every evidence row record channel, subscribers, video, publication date, views, outlier score,
current velocity when available, transferable framing, and a manual relevance check. Raw views alone
do not pass. Read the underlying result rows; a median or automated verdict without relevance review
is not evidence.

Use:

- `tools/outlier-scan.py` to find ideas that exceeded their channel's normal distribution;
- `tools/demand-probe.py` to test **shape families and lane demand**, never to choose between two exact
  finished titles;
- `tools/teardown.py` to identify transferable structural moves.

**One outlier is a lead; independent recurrence is evidence.** An exception requires a written reason
and must be labeled an experiment.

## Gate 2 — Pre-Script Packaging

Packaging is an input to development, not decoration added after the render. Before full research,
final VO, asset generation, or scene production, complete and approve in `YOUTUBE-PACKAGE.md`:

- three accurate title candidates and one recommended working title;
- two or three thumbnail concepts and one recommended direction;
- the title/thumbnail division of labor (they complement rather than repeat each other);
- the concrete viewer payoff;
- the question or contradiction whose meaning will be withheld;
- the demand evidence from Gate 1.

If the idea cannot produce a compelling and truthful package, stop or reframe it before production.
The package may be refined after the final cut, but it must not be invented for the first time then.

## Gate 3 — Research and Claim Map

Gather source material from the active Jarvis knowledge stack:

- official documents, product pages, filings, changelogs, papers, and source screenshots;
- YouTube transcripts and monitored channels;
- news/RSS/Substack/Reddit/HN aggregation;
- existing Jarvis research, scripts, and prior episode folders.

Output a research brief with thesis options, claim/source map, must-show evidence, uncertainty,
counter-evidence, and unanswered questions. Every meaningful factual claim needs a source or must be
clearly framed as interpretation.

## Gate 4 — Originality Firewall

Competitor work is a structural reference, never source material to paraphrase. We may transfer:

- sequence, tension, pacing, loop mechanics, reversal position, and general presentation moves.

We may not transfer:

- distinctive wording, examples, research selection, conclusions, visual identity, thumbnail
  composition, or a competitor's unique combination of elements.

Every teardown must record both `TRANSFERABLE MOVES` and `DO NOT IMPORT`. The episode must add original
research, synthesis, judgment, or practical utility that makes the work recognizably ours and protects
its eligibility under YouTube's original/authentic-content standard.

## Gate 5 — Visual-First Script and Retention Architecture

Plan the visual arc before locking VO. For each beat record what appears, what changes, which claim it
supports, the production tool, approximate duration, and approval status. Then write VO to explain the
visual—not the reverse.

The script must include:

- an information-first opening frame and a named carried question;
- facts revealed early while meaning/mechanism/verdict remains unresolved;
- compounding stakes;
- an authored reversal at roughly 40–55%;
- an escalating, persistent visual spine;
- a runtime no longer than the held payoff can sustain.

## Gate 6 — Visual Treatment and Asset Resolution

Every scene needs a treatment row containing purpose, VO claim, screen action, visual register,
container, source assets, motion, tool, risk, and approval. Select the register for the beat's job; do
not default to the previous scene.

Use `asset-library/MANIFEST.json` by semantic key. Copy resolved files into each scene's `assets/`
directory; do not symlink final assets or reference one-off session paths. Real source proof beats
simulated proof. Simulated UI/code beats generic cards when the subject is technical work. Sites may
support dashboards, simulations, evidence explorers, review boards, and companion resources; capture
their output into the final VO-synced composition. See [SITES.md](SITES.md).

## Gate 7 — Scene Production and Rendered QC

Use HyperFrames unless another tool is clearly better. Run lint before layout because lint errors can
short-circuit layout sampling. Then run both required rendered-scene gates:

```bash
python3 .agents/skills/jarvis-video-production/tools/scene-validator.py <project>/hyperframes-v3 --frames
hyperframes check <scene-dir> --at-transitions --json
```

Each scene must have zero unresolved errors. Inspect extracted frames across every beat. Verify exact
VO/visual correspondence, no dead-air tails, no synthetic-voice pauses left merely because they were in
the source audio, no blank/near-empty frames, no static hold over five seconds, and no text collision or
occlusion. A tool pass without human frame inspection is incomplete.

## Gate 8 — Master and Final Package Verification

Assemble using the mode-appropriate current assembler documented in `PIPELINE.md`. Run the final
master gates and review transitions, audio continuity, visual/VO alignment, and the persistent spine.

Recheck the approved title and thumbnail against the actual finished promise. Prepare description,
chapters, sources/provenance, end screen, cards, playlist placement, pinned comment, final QA summary,
and handoff notes. Refinement is allowed; changing the video's fundamental promise requires returning
to Gate 2.

## Gate 9 — Unlisted Upload QA

Upload the approved master as **unlisted** for processing and operational QA—not as an algorithmic
trust tactic. Before scheduling or making it public:

- wait for all intended resolutions and YouTube checks to finish;
- verify title, thumbnail, description, chapters, sources, end screen, cards, and playlist;
- check copyright, restrictions, AI disclosure, audience designation, and monetization status;
- set and confirm the original language;
- test desktop and mobile playback and verify the processed audio/video;
- record the final public or scheduled URL in the command center.

## Gate 10 — Optional Reviewed Localization

Automatic dubbing is optional and must never be treated as automatic reach. For eligible evergreen
videos, set the original language accurately, require manual publication of dubs, and review each dub's
transcript before release—especially names, numbers, quotations, scientific terminology, and company
names. Publish only acceptable language tracks. Localization must not delay the primary-language
release unless the channel profile explicitly requires it.

## Gate 11 — Measurement and Learning

Record the channel profile's metrics at its specified checkpoints. Judge the package, opening, body,
and conversion separately; raw views alone cannot diagnose the failure. After the measurement window,
write what should be retained, changed, or tested next. Fold only genuinely general lessons back into
the shared skill; channel-specific findings stay in that channel's profile or episode record.
