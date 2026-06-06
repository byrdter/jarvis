# V14 Tooling Integration

The third-party tools the V14 pipeline depends on. Auth, conventions, and gotchas.

## ElevenLabs (VO generation)

**Where it lives in env (`/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/.env`):**
```bash
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=gPiEpcKoaZywgOzc0Zn9       # current canonical voice
ELEVENLABS_MODEL=eleven_multilingual_v2
ELEVENLABS_SPEED=0.95
ELEVENLABS_STABILITY=0.6
ELEVENLABS_SIMILARITY_BOOST=0.75
ELEVENLABS_STYLE=0.3
ELEVENLABS_SPEAKER_BOOST=true
```

**Generation call (shell):**
```bash
curl -sS -X POST "https://api.elevenlabs.io/v1/text-to-speech/$ELEVENLABS_VOICE_ID?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your script here.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.6,
      "similarity_boost": 0.75,
      "style": 0.3,
      "use_speaker_boost": true,
      "speed": 0.95
    }
  }' \
  -o audio.mp3
```

**Gotchas:**
- `output_format=pcm_44100` requires Pro tier (we don't have it). Stick with `mp3_44100_128`.
- The "AI voice" complaint is almost always voice choice, NOT settings. Try a different voice ID before tuning sliders.
- Regenerating the same text+voice+settings produces a slightly different take each time. If you want deterministic timing, cache the output.
- Don't use Cartesia for V14. We tested it; sonic-2's `experimental_controls.speed` parameter was silently ignored in our tests and the voice quality lagged ElevenLabs for narration.

## HyperFrames (visual system + transcribe + render)

**Used commands:**

```bash
# Transcribe VO → word-level timestamps in assets/transcript.json
npx -y hyperframes transcribe assets/audio.mp3

# Lint composition for render-blocking errors
npx -y hyperframes lint

# Render to MP4 (writes to renders/NAME_TIMESTAMP.mp4)
npx -y hyperframes render
```

**hyperframes.json schema:**
```json
{
  "name": "video-XX-scene-NN-pilot",
  "version": "0.1.0",
  "compositions": [
    {
      "id": "NN-pilot",
      "file": "index.html",
      "width": 1920,
      "height": 1080,
      "duration": N
    }
  ]
}
```

**The transcribe output:**
```json
[
  { "text": "Most", "start": 0.04, "end": 0.59 },
  { "text": "personal", "start": 0.59, "end": 1.46 },
  ...
]
```

Use those `start` values as your timeline `at` anchors.

**Gotchas:**
- HyperFrames' file server does NOT follow symlinks. Use `cp`, never `ln -s`.
- The render's printed duration is often wrong. `ffprobe -v error -show_entries format=duration` gives the real number.
- The Studio preview can mis-time media (audio plays differently than render). Always trust the rendered MP4 over the preview for timing decisions.
- Adding `@font-face` declarations for Menlo/Consolas removes a warning but isn't required.

**ByrdTransitions library:**

Lives at `lib/byrd-transitions.{css,js}` inside each scene. Copy from any existing scene (Scene 02 is the reference):
```bash
cp video-XX-NAME/scenes/02-pilot/lib/byrd-transitions.* video-XX-NAME/scenes/NEW-pilot/lib/
```

Exports: `letterCascade`, `smokeReveal`, `maskWipeCircle`, `zoomPunch`, `glitchSplit`, `rgbSplit`, `pulseBloom`, `screenShake`, `lightLeakFlash`, `particleShatter`, `letterBurn`, `whipPan`.

See [`SHOT-VOCABULARY.md`](SHOT-VOCABULARY.md#11-helper-usage-idioms) for usage patterns.

## Runway (cinematic B-roll for title/transition beats)

Use ONLY for:
- Title hero beats (Scene 3 pattern)
- Transition burst beats (Scene 7 pattern)

Do NOT use for:
- Scenes with VO (audio conflict)
- Long expository scenes (too expensive)
- Scenes where real product UI works (use screenshots)

**Drop location:**
```
video-XX-NAME/scenes/NN-pilot/assets/runwaybg.mp4
```

**Composition pattern:**
```html
<video id="bgVideo" class="bg-runway" src="assets/runwaybg.mp4"
       data-start="0" data-duration="N" data-has-audio="true" playsinline></video>
```

The `data-has-audio="true"` attribute tells HyperFrames to include Runway's bundled audio in the render — the SFX is part of the clip.

**Sync the HyperFrames overlay to Runway's audio impact:**
1. Watch the Runway clip in Quicktime/preview
2. Note the impact timestamp (e.g., 4.0s or 5.0s)
3. Set your title cascade `at` value 2 seconds before the impact
4. Set the title's "slam" / accent pulseBloom `at` value EXACTLY on the impact
5. Add screen shake on the impact too

See [`RUNWAY-PROMPTS.md`](RUNWAY-PROMPTS.md) for prompt templates.

## ffmpeg (audio stripping, concat)

**Strip audio from B-roll:**
```bash
ffmpeg -i original.mp4 -an -c:v copy original-no-audio.mp4
```

Or use the `*2.mp4` variants from `video-assets/clip-library/pixelvideos/` which are pre-stripped.

**Slow VO via atempo (fallback when voice change isn't enough):**
```bash
ffmpeg -y -i audio_raw.wav -filter:a "atempo=0.82" audio.wav
```

Range: 0.5 to 2.0. Below 0.7 sounds warbly. We use 0.82 to 0.92 typically.

**Concat scenes into master:**
```bash
ls -1 scenes/*-pilot/renders/*.mp4 | sort > concat.txt
sed -i '' "s|^|file '$PWD/|;s|$|'|" concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy master.mp4
```

If codecs don't match, re-encode:
```bash
ffmpeg -f concat -safe 0 -i concat.txt \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  master.mp4
```

## Higgsfield (planned, not yet integrated)

For automated short B-roll clip generation in future videos. Will replace some Runway use cases when faster turnaround matters more than cinematic quality. Document the integration here when we ship the first scene that uses it.

## Asset library locations

- **Brain PNGs:** `asset-library/shared/{Claude,Codex,Gemini}Brain.png`
- **JARVIS orb:** `asset-library/shared/JarvisOrb.png`
- **Product screenshots:**
  - `asset-library/products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png`
  - `asset-library/products/codex/desktop/CodexDesktop.png`
  - `asset-library/products/gemini/surfaces/web/hero.png`
  - `asset-library/products/chatgpt/surfaces/web/hero.png`
  - `asset-library/products/antigravity/surfaces/web/hero.png`
  - `asset-library/products/openai/surfaces/web/hero.png`
- **Pixel-art B-roll (silent variants):** `video-assets/clip-library/pixelvideos/person-*2.mp4`

When copying assets into a scene's `assets/` directory, prefer `cp` over reference paths — keeps the scene self-contained for `hyperframes render` (which won't follow upward path references).
