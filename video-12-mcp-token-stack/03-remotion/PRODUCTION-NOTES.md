# Video 12 Remotion Production Notes

## Source

HeyGen source used:

`../10-videos/heygen-source.mp4`

Original upload path retained:

`../10-ouput/heygen-source.mp4`

The source is 1920x1080, 25fps, 730.007 seconds.

## Timing

`transcribe_and_align.py` created `segment-timings.json` from word timestamps.

The actual HeyGen MP4 does not contain every segment from the written script. In the transcript, segment 3 is absorbed into the long segment 2 block, and the planned scoped-MCP / skills narration block for segments 14-16 is absent. The Remotion timeline follows the actual audio in the MP4 instead of forcing silent visual slots for missing narration.

## Visual Approach

The automated Chrome screenshot pass was unreliable in this environment. The render therefore uses source-proof artifact panels with browser chrome, source URLs, highlighted figures, metrics, tables, and workflow cards. This is still evidence-oriented, but it is not a literal screenshot capture of each article page.

## V2 Stills-First Revision

After review, the first Remotion-only version was too repetitive and too plain. V2 uses the Claude-generated stills in `../09-stills/` as the primary visual foundation. The stills were copied into `public/stills/` for Remotion and animated with:

- slow push-in camera movement,
- subtle x/y drift,
- cyan/orange light sweeps,
- scanline texture,
- pulsing callout rings,
- vignette and contrast treatment,
- lower-left segment straps for non-avatar scenes.

The beginning and ending stills are intentionally ignored in the final assembly because those sections are carried by the full-screen HeyGen avatar. Side-avatar scenes are assembled after the Remotion base render by overlaying the HeyGen source video with ffmpeg.

Remotion's bundled media pipeline repeatedly stalled while decoding and encoding the large HeyGen MP4 from the Dropbox-backed project. The successful production path was:

1. Copy the Remotion project to `/private/tmp/video12-v2-remotion`.
2. Render the animated-stills base from Remotion without audio or embedded HeyGen video.
3. Encode the generated frame sequence with system ffmpeg.
4. Use system ffmpeg to overlay HeyGen avatar sections and mux the original HeyGen audio.

Final v2 output:

`../10-videos/video-12-v2.mp4`

## QA

Checks completed:

- TypeScript compile: passed.
- Still frame checks:
  - intro avatar,
  - source-proof panel,
  - side-avatar layout,
  - CTA card,
  - closing avatar.
- Final render: `../10-videos/video-12.mp4`
- Final MP4: 1920x1080, 25fps, H.264 video, AAC audio, 730.069 seconds.

V2 checks completed:

- Final render: `../10-videos/video-12-v2.mp4`
- Final MP4: 1920x1080, 25fps, H.264 video, AAC audio, 730.007 seconds.
- Sample frames inspected:
  - `out/v2-final-qa/010-intro.jpg`
  - `out/v2-final-qa/095-animated-still.jpg`
  - `out/v2-final-qa/155-side-avatar.jpg`
  - `out/v2-final-qa/475-stack.jpg`
  - `out/v2-final-qa/672-cta.jpg`
  - `out/v2-final-qa/696-closing.jpg`
