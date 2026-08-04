# QC Report

## Current Gate

- Artifact under review: final Cartesia narration, scene anchors, source cards, and returned I2V clips
- Render QC status: not started
- Reason: narration is approved and timed; rendered scenes and master do not exist yet

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

## Future Render Gates

- [ ] `scene-validator.py`: 0 errors
- [ ] Scene-level `freezedetect=n=-50dB:d=5`: no `freeze_duration` output
- [ ] Assembled-master `freezedetect=n=-50dB:d=5`: no `freeze_duration` output
- [ ] `deadspace-scan.py`: 45–60 change events/min target; no scene under ~30/min
- [ ] `deadspace-scan.py`: pass per scene and master
- [ ] `beatmap.py ghosts`: every ghost resolves within ~1.2s from opacity ≥0.40
- [ ] `beatmap.py check`: map matches build
- [ ] Citation-card presence and integrity verified from rendered pixels
- [ ] No beat gap over ~5s
- [ ] Narrative measurement run on timed VO/transcript
- [ ] Text readable on mobile; no collisions, splits, joined words, or tiny labels
- [ ] Intro, reversal, sensing reveal, verdict, and ending watched as motion

## HyperFrames Scene Gate — S00

- Composition: `05-hyperframes/compositions/s00-three-numbers.html`.
- Audio-derived duration: 33.92 seconds.
- `npm run check`: PASS with 0 lint errors/warnings, 0 runtime errors, 0 layout errors/warnings, 0 motion errors/warnings, and 78/78 contrast checks.
- Eleven snapshots captured across the opening and visually inspected as a contact sheet.
- Three single-use media clips are mounted directly at the host root; narration is mounted separately on audio track 10.
- Visual changes are anchored to Cartesia word timings; final map breath remains below the five-second static ceiling.
- One informational occlusion remains intentional: the host wafer shot temporarily covers the small `DEMONSTRATED` badge while the large lab proof is the focal object.

## Approval

- Visual treatment approved by: Terry
- Date: 2026-08-04
- Remaining risk: ITU/NICT/CityUHK/NIST proof cards and rendered motion QC remain outstanding. Narration and returned I2V motion are locked.
