# Video 25 HyperFrames V2 Proof

This is a short proof cut for the Video 25 rebuild. It covers the first two VO scenes, about 75 seconds, and is intended to test the corrected visual grammar before rebuilding the full 12.5 minute episode.

## What Changed From The Failed First Master

- No production metadata on screen.
- Real HyperFrames composition with GSAP timeline.
- VO-anchored visual beats instead of static boards.
- Public web-rolls appear as evidence within the story.
- The prompt-to-system shift is staged as a visual transformation.
- Mock agent/workflow surfaces animate in sequence.

## Local Output

- Proof MP4: `renders/video-25-v2-proof.mp4`
- QC contact sheet: `qc-contact-sheet.jpg`

Generated media is ignored by Git.

## Rebuild

```bash
./prepare-assets.sh
npx hyperframes lint
npx hyperframes render --output renders/video-25-v2-proof.mp4 --quality draft
```

## Known Follow-Up For Full Rebuild

Before full Video 25 production, re-encode web-roll assets to 30 fps with frequent keyframes so HyperFrames does not warn about sparse keyframes or risk frame freezing.

