# Asset Standards

Channel-agnostic standards for typography, color tokens, file structure, and asset paths. Channel-specific tokens (palette, brand mark) live in `channel-identities/<channel>/IDENTITY.md`.

---

## Composition

- **Resolution:** 1920×1080 (16:9). Verticals are a separate cut, generated from a parallel composition file.
- **Frame rate:** 25 fps.
- **HyperFrames version:** 0.6.7. Lock per project — newer versions may break composition format compatibility.

---

## Typography

Three font families, three roles:

| Family | Role | Where used |
|---|---|---|
| **Fraunces** (serif) | Editorial headlines, chapter card titles | Module headline ("Tools."), chapter card "MCP" |
| **Inter** (sans) | Body, eyebrows, captions, labels, button-like elements | Almost everything else |
| **JetBrains Mono** (mono) | Code, terminal output, token counters, numeric scales | Action blips, cost meter counter, scale ticks |

**Channel substitutions:** A different channel can swap any of these by defining its own typography tokens in `channel-identities/<channel>/typography.css`. The roles stay; the typefaces vary.

### Common sizes

- Eyebrow (Inter 700, letter-spacing 0.28em, uppercase): 20–24px
- Module headline (Fraunces 600, letter-spacing -0.02em): 132–168px
- Chapter headline (Fraunces 600): 100–132px
- Sub-headline (Inter 500, italic): 24–28px
- Caption ribbon text (Inter 800, letter-spacing 0.1em, uppercase): 28–34px
- Body / label (Inter 500–700): 16–22px
- Counter (JetBrains Mono 700): 18–22px

---

## Color tokens

Channel-agnostic background tokens (any channel can override):

| Token | Hex | Role |
|---|---|---|
| `--stage-cream` | `#F4EFE6` | Channel stage background |
| `--stage-navy` | `#1A2634` | Card backgrounds, ribbon backgrounds |
| `--stage-deep` | `#0F1420` | Inner card gradients |

Channel-specific accent (Byrddynasty):

| Token | Hex | Role |
|---|---|---|
| `--accent-cyan` | `#34F5FF` | Borders, glows, focus rings |
| `--orb-teal` | `#14D1BD` | Gradient orb |
| `--orb-purple` | `#8A2BBE` | Gradient orb |
| `--orb-blue` | `#5BB9FB` | Gradient orb |
| `--warn-amber` | `#FFB037` | Cost indicators, warnings |

For new channels, redefine these in `channel-identities/<channel>/color-tokens.css`.

---

## File structure (per module)

```
02-modules/NNN-module-name/
├── CONCEPT.md
├── VISUAL-SEQUENCE.md
├── VO.txt
├── generate_storyboard.py
├── storyboard/
│   └── module-NN-storyboard-grid.png
├── assets/
│   ├── module-NN-heygen.mp4        # HeyGen drop
│   ├── module-NN-audio.wav         # whisper-ready mono 16k
│   └── module-NN-words.json        # whisper output
├── hyperframes/
│   ├── package.json
│   ├── hyperframes.json
│   ├── index.html
│   ├── media/
│   │   └── vo.wav                  # 48k stereo audio for composition
│   └── renders/
│       └── module-NNN-module-name.mp4
├── keyframes/
│   └── m<NN>r<N>-t<seconds>.jpg    # critique keyframes per render
└── promotion/                       # Step 8.5 deferred
```

---

## Audio pipeline

### Extract from HeyGen MP4 to composition WAV:
```bash
ffmpeg -y -i assets/module-NN-heygen.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s16le hyperframes/media/vo.wav
```

### Extract to whisper-ready mono 16k:
```bash
ffmpeg -y -i assets/module-NN-heygen.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le assets/module-NN-audio.wav
```

### Run whisper for word-level timestamps:
```bash
whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-small.en.bin \
  -f assets/module-NN-audio.wav -ml 1 -oj -of assets/module-NN-words
```

### Probe audio duration before setting composition duration:
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 hyperframes/media/vo.wav
```

---

## API keys

| Key | Path | Used for |
|---|---|---|
| `GEMINI_API_KEY` | `${JARVIS_PRIVATE}/apps/content-creation/video-generator/.env` | Nano Banana Pro storyboard generation |
| `GROQ_API_KEY` | `~/.config/watch/.env` | Blocked by Cloudflare on Terry's network — do not use |
| `OPENAI_API_KEY` | `~/.config/watch/.env` | Currently empty — do not use |

Whisper is local-only via `whisper-cli`. No API calls.

---

## Channel identity inheritance

Every composition's HTML must inherit:
1. The cream stage with gradient orbs (or the channel's stage equivalent)
2. The film grain layer
3. The brand mark + gradient orb top-left
4. The typography stack
5. The accent color tokens

These come from `channel-identities/<channel>/IDENTITY.md` and the supporting CSS files in the same folder.

---

## Render commands

```bash
# Inside hyperframes/ directory:
npm run check     # lint + validate
npm run preview   # interactive studio at http://localhost:3029 (or per-module port)
npm run render    # produce mp4 at renders/<comp-id>.mp4
```

The `render` command uses draft quality + 2 workers + 25fps. For final delivery passes, override with `--quality high --workers 4`.
