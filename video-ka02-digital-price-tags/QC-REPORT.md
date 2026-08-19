# QC Report

Run QC on rendered MP4s, not only previews.

## Master Summary

- Master file:
- Duration:
- Resolution:
- Audio stream:
- QC status: pending / pass / fail

## Runtime Gate

- Minimum 8 minutes met: no
- Preferred 10-15 minutes met: no
- Notes:

## Scene Findings

| Scene | Timestamp | Severity | Finding | Fix | Status |
|---|---:|---|---|---|---|
| 06 | full scene | — | HyperFrames check: 0 runtime errors, 0 layout issues, 46/46 text contrast checks pass | none | pass |
| 06 | full scene | — | Motion scan: 64 events / 58.0 per minute; longest static interval 3.7s; visual bed passes | none | pass |
| 06 | full scene | — | Dead-space scan: no black or blown frames | none | pass |
| 06 | full scene | — | Scene validator: 66.16s composition, timeline and narration end exactly together | none | pass |

## Text Checks

- [ ] No split words across lines
- [ ] No adjacent words joined together
- [ ] No tiny labels
- [ ] No typo in on-screen text
- [ ] Text readable on mobile

## Visual Checks

- [ ] Important screenshots are zoomed/cropped/highlighted enough to read
- [ ] Brain icons/logos/key visuals are large enough
- [ ] No incoherent overlap
- [ ] No repeated presentation mode for too long

## Motion / Audio Checks

- [ ] Animations land on VO words or audio hits
- [ ] No accidental B-roll audio under VO
- [ ] Pacing changes every 3-8 seconds in normal explanatory sections
- [ ] Intro, middle, and ending watched as motion

## Approval

- Approved by:
- Date:
- Remaining risk: Scene 06 is review-ready, not editorially locked. Confirm Steve voice, mobile readability,
  evidence-cue frequency, and the real-footage/document balance before propagating the grammar.

## Scene 06 Review Prototype — 2026-08-19

- File: `05-hyperframes/renders/scene06-study-reversal-review-v4.mp4`
- Duration / format: 66.1667s; H.264 video + AAC audio; 1920×1080 at 30fps
- Narration: Steve / Cartesia Sonic 3.5; selective Scene 06 synthesis; word-timed animation cues
- Evidence status: working paper is identified as a working paper; 114 stores, four states, and
  0.005%→0.0056% result are represented on a common axis; no peer-review claim
- Media treatment: licensed real Walmart interior beneath authored evidence graphics; no photoreal AI
- HyperFrames lint note: Track 4 contains seven timed beat sections. This is acceptable for the one-scene
  prototype; the full episode should mount coherent scene groups as sub-compositions.
