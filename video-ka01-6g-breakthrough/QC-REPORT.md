# QC Report

## Current Gate

- Artifact under review: `05-hyperframes/renders/MASTER-KeyAdvances-6G-v2.mp4`
- Render QC status: **PASS — ready for Terry's editorial review**
- Master: 1920×1080, H.264, 30 fps, AAC stereo 48 kHz, 544.9 seconds (9:04.9), 139,821,552 bytes
- Voice: Steve / Cartesia Sonic 3.5, locked to the approved twelve-scene narration

## Script Gate — 2026-08-04

- Spoken words: 1,375 by `prepublish-check.py`; estimated 9:35 at 143 wpm.
- Negation/reversal density: PASS, 3.65/min; hedge share PASS, 49%.
- Opening evidence density: PASS, 11 detected concrete points.
- Forbidden phrases: PASS, none.
- Carried loop: manual PASS; opens at approximately 0:38 and is not resolved within 30 seconds.
- Reversal: manual PASS; Scene 06 occupies the 40–55% window and changes the controlling question.
- Persistent spine: manual PASS at plan level; Impact Map changes in every scene. Render verification remains required.
- Runtime: the shared tool reports FAIL because its current floor is hard-coded to 15–25 minutes. This is an intentional channel-profile exception: KeyAdvances approved 8–10 minutes and this episode is locked at 9:20–9:45. Padding to satisfy a Byrddynasty runtime constant would violate the KeyAdvances profile.
- `narrative-measure.py`: PASS on the global Cartesia transcript. First payoff 88.3%; longest spine gap 70s; reversal occupies the required 40–55% window; CTA follows the payoff.

## Narration Gate — 2026-08-04

- Provider/model: Cartesia Sonic 3.5.
- Voice: Steve; explicit voice ID frozen in `02-audio/voice/audio_meta.json` to prevent `.env` duplicate-key drift.
- Delivery speed: 0.86.
- Twelve scene-local mono PCM WAV files at 44.1 kHz; all durations measured with `ffprobe`.
- Spoken duration: 537.2 seconds. Timed structure with 0.7-second scene transitions: 544.9 seconds (9:04.9).
- Word timestamps: present and monotonic for all twelve scenes.
- Long internal silence scan: PASS; no silence interval at or above 1.5 seconds detected at -45 dB.
- Reversal: begins 39.84% and ends 50.81% of the timed structure.
- Verdict: begins 86.47%; CTA follows at 98.55%.
- Earlier Terry-voice and faster Steve tests are isolated under clearly labeled `02-audio/rejected-*` folders and are not build inputs.

## Pre-Production Narrative Gate

- [x] Whole-runtime question declared
- [x] Persistent spine visible and advanced in every scene
- [x] Withholding ledger non-empty until verdict
- [x] Withholding debt expands before the reversal
- [x] Reversal placed at 40–55%
- [x] Verdict withheld until final 10–15%
- [x] CTA after verdict
- [x] Every scene pays out a fact and opens a harder question
- [x] Human consequences include daily life, work/business, access, and privacy
- [x] Demonstrated facts separated from standards targets, plausible applications, and speculation

## Pre-Production Visual Gate

- [x] At least six relevant presentation registers
- [x] No more than three consecutive scenes with the same dominant register
- [x] Quick-cut montage planned
- [x] Held 4–6 second breath planned
- [x] Source proof reserved for load-bearing facts
- [x] Denotative visual budget at least 90%
- [x] Every scene specifies what appears and what changes
- [x] Every scene has a planned meaningful change every 2–4 seconds, never reaching a five-second static hold
- [x] Every scene has a unique real-background brief and at least three single-use clip roles
- [ ] Source crops captured and checked at mobile size
- [x] Library clip provenance frozen into scene-local folders
- [x] Visual treatment approved by Terry
- [x] Five original source stills created and frozen locally
- [x] Original stills approved through Terry's generation handoff
- [x] Returned I2V clips reviewed and frozen

## Returned I2V Review — 2026-08-04

| Clip | Result | Locked interval | Notes |
|---|---|---:|---|
| Photonic light path | PASS | 0:00–0:07 | Stable chip and connectors; moving optical energy reads clearly |
| Laboratory pullback | PASS | 0:00–0:12 | Strong chip-to-system reveal; stable equipment and continuous camera motion |
| Horn short link | CONDITIONAL PASS | 0:00–0:04 | Signal is subtle and source is nearly static; use only below five seconds with the animated `1.3 m` ruler |
| Network sensing hero | PASS | 0:00–0:10 | Clean room reconstruction and natural head turn; anatomy remains stable |
| Ordinary sensing room | PARTIAL PASS | 0:00–0:06.5 | Opening is clean; later frames contain a ghosted double lamp/cane and are excluded |

All approved intervals were re-encoded without audio and frozen under `02-assets/approved-clips/`, then copied into the corresponding scene-local asset folders.

## Master Render Gates — 2026-08-04

- [x] HyperFrames check: 0 lint errors, 0 runtime errors, 0 layout issues, 0 motion errors
- [x] Contrast: 71/71 sampled text checks pass WCAG AA
- [x] Master `freezedetect=n=-50dB:d=5`: no `freeze_duration` output
- [x] Master silence scan at -45 dB / 1.5 seconds: no long silence output
- [x] `deadspace-scan.py`: no black or blown-white frames
- [x] `motion-scan.py` density: 572 events, 63.0/min — PASS above the 56.8 strong threshold
- [x] `motion-scan.py` static: longest low-change interval 4.3 seconds — PASS below the 5.0-second ceiling
- [x] `motion-scan.py` bed: mean luma 45.9, texture standard deviation 69.3 — PASS
- [x] Output integrity: H.264 1920×1080 at 30 fps; AAC stereo 48 kHz; exact 544.9-second duration
- [x] No sparse-keyframe source warnings after four local clip transcodes
- [x] Text readable at full-frame review; no observed collisions, joined words, clipping, or unsafe margins
- [x] Intro, 4G/5G expectation reset, midpoint reversal, sensing reveal, governance split, verdict, and CTA inspected from rendered MP4 pixels

`scene-validator.py` expects a legacy `scenes/*` render tree and reports no scenes for this single-master HyperFrames architecture. Its render-failure responsibilities are covered here by the master-level freeze, silence, deadspace, motion-density, static-hold, bed, layout, runtime, contrast, and manual pixel-review gates.

## HyperFrames Scene Gate — Full Build

- Twelve modular scene compositions: S00–S11.
- Audio-derived duration: 544.9 seconds including eleven 0.7-second inter-scene transitions.
- `npm run check`: PASS with zero lint errors, runtime errors, layout issues, or motion errors; 71/71 contrast checks pass.
- Real scene-specific backgrounds plus three single-use clips are mounted for every scene; narration is mounted as twelve separate audio elements.
- Visual changes are anchored to Cartesia word timings and reinforced by evidence-aligned camera reframes.
- A first rendered master exposed seven ≥5-second freeze intervals. The build was revised; a second pass reduced these to one; the delivery v2 clears both freeze and tile-motion static gates.

## Approval

- Visual treatment approved by: Terry
- Date: 2026-08-04
- Remaining before publication: Terry's editorial review, final source/description/chapter package, and unlisted YouTube upload QA. Rendered motion QC is complete.
