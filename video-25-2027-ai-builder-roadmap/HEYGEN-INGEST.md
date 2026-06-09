# Video 25 HeyGen Ingest

## Source Verification

- Raw source: `Video25raw.mp4`
- Pipeline copy: `heygen/raw-video-25.mp4`
- Extracted audio: `heygen/raw-video-25.wav`
- Video: 1920x1080, 25 fps, H.264
- Audio: AAC in source, extracted to 16 kHz mono WAV
- Duration: 754.2 seconds, about 12:34
- HyperFrames transcription: 1,787 words over 754.0 seconds

## Scene Split Method

Silence detection found useful pauses, but not a clean full set of scene boundaries because HeyGen softened several breaks. Scene timing is therefore mapped from the word-level transcript against the HeyGen paste script. Scene 7 required a manual normalization because Whisper transcribed "Layer five" as "Layer 5".

## Scene Timing

| Scene | Title | Segment Start | Segment End | Duration | Words |
| --- | --- | ---: | ---: | ---: | ---: |
| 01 | Cold Open: Chat Is Not The Destination | 0.000 | 33.090 | 33.090 | 78 |
| 02 | The Builder Stack Shift | 33.090 | 74.850 | 41.760 | 126 |
| 03 | Layer 1: Model Judgment | 74.850 | 150.800 | 75.950 | 179 |
| 04 | Layer 2: Tools And APIs | 150.800 | 232.170 | 81.370 | 205 |
| 05 | Layer 3: Memory And Knowledge | 232.170 | 328.690 | 96.520 | 209 |
| 06 | Layer 4: Workflows, Hooks, And Skills | 328.690 | 418.240 | 89.550 | 212 |
| 07 | Layer 5: Evals And Observability | 418.240 | 498.090 | 79.850 | 189 |
| 08 | Layer 6: Deployment And Real Systems | 498.090 | 577.130 | 79.040 | 179 |
| 09 | What To Learn In Order | 577.130 | 667.000 | 89.870 | 182 |
| 10 | Close: Build The Stack And CTA | 667.000 | 754.200 | 87.200 | 228 |

## Local Generated Assets

- `heygen/transcript.json` is tracked because it is small and needed for timing/caption work.
- `heygen/scene-timing.json` is tracked as the authoritative split map.
- `heygen/scenes/scene-XX.wav` files are local generated assets and ignored by Git.
- The raw `.mp4` and extracted `.wav` files are local production assets and ignored by Git.
