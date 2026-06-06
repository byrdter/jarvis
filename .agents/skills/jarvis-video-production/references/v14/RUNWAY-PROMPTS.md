# V14 Runway Prompt Templates

Reusable prompts for the two Runway use cases in V14: title hero beats (Scene 3 pattern) and transition burst beats (Scene 7 pattern).

Each entry has three prompts:
1. **Image prompt** — for the seed still image
2. **Video prompt** — for image-to-video animation
3. **Sound prompt** — for synchronized SFX (or Splice keywords for manual sourcing)

---

## Title Hero — Three Brands Converging

**When to use:** Major title reveals where three brand-colored elements need to converge or align. The Scene 3 "THREE BRAINS. ONE ROUTER." pattern.

### Image prompt

> *Cinematic ultra-wide shot of three glowing orbs floating in a deep black void, slowly orbiting around a single brighter central point of light. The left orb glows warm Anthropic orange (#d97757), the center-back orb glows OpenAI emerald green (#10a37f), the right orb glows Google sapphire blue (#4285f4). Each orb leaves a soft trailing arc of light as it orbits. The central point is brilliant white-gold, larger and more intense than the orbs, pulsing faintly. Volumetric haze fills the surrounding void; faint particles drift through the space. The camera is positioned slightly below center, looking up at a dramatic 3/4 angle. Inky black background, deep negative space, no text, no logos, no UI elements. Hyperrealistic, photographic, cinematic lighting, depth of field with bokeh on background particles. Mood: anticipatory, ominous, reverent — like the moment before a reveal. Aspect ratio 16:9, resolution 1920×1080.*

### Video prompt

> *Slow controlled push-in toward the central point of light. The three colored orbs continue their orbit around it, gradually accelerating over the duration of the shot. As they accelerate, their light trails brighten and lengthen, blurring into ribbons of orange, green, and blue. Particles in the surrounding void drift toward the center. At the 4-second mark, the three orbs collapse inward toward the central point in unison; their trails converge into a single brilliant flash of light that briefly whites out the center of the frame. After the flash, the central point is left intensified — larger, brighter, white-gold — pulsing once. Hold the final pulsing frame for one full beat. Cinematic, no camera shake, smooth motion, depth of field preserved. 7 seconds, 1920×1080.*

### Sound prompt

> *Rising cinematic synth bed building tension from 0 to 4 seconds, layered with subtle low-frequency drone and barely-audible particle whoosh sounds. At the 4-second mark, a single massive cinematic impact thud — deep sub-bass with a metallic reverb tail and a high-frequency shimmer/sparkle on the transient. After the impact, the synth bed drops away into a sustained low atmospheric drone tail that fades out over the remaining 3 seconds. No music melody, no dialogue, no foley. Just tension build → impact → atmospheric tail.*

**Splice/Epidemic search:** "rising synth riser 4s" + "cinematic impact / boom hit" + "low atmospheric drone 3s"

---

## Transition Burst — Choice Paralysis Reveal

**When to use:** Mid-video transition beats where you need to ask a question and slam an answer. The Scene 7 "BUT WHICH ONE?" pattern.

### Image prompt

> *Cinematic ultra-wide shot of three glowing orbs floating in deep black void, arranged in a triangular pattern equidistant from each other. Left orb glows warm orange (#d97757). Right orb glows emerald green (#10a37f). Bottom-center orb glows sapphire blue (#4285f4). All three orbs are roughly equal brightness. Between them, in the negative space at the center of the triangle, a single translucent glowing question mark "?" made of soft white light hovers, slightly out of focus. The orbs cast subtle colored glows onto each other across the void. Faint dust particles drift through the dark space. Pure black background. No text, no logos, no UI. Cinematic depth of field with the orbs in sharp focus and the question mark slightly hazy. Mood: choice paralysis, tense anticipation, "the right answer isn't obvious." 16:9, 1920×1080.*

### Video prompt

> *The three colored orbs hover and pulse slowly and independently in the void — each at slightly different rhythms, like indecision. The central question mark flickers and stutters — sometimes appearing solid, sometimes fragmenting into smaller floating particles before reforming. At the 3-second mark, the question mark begins to vibrate and split into three identical translucent copies, each drifting outward toward one of the three orbs. As the question marks drift, the orbs begin to vibrate subtly and their light intensifies. At the 5-second mark, a single hard convergent impact — all three question marks collapse simultaneously into their respective orbs, each orb flares to maximum brightness, and the camera does a small sharp shake. After the impact, hold on the three pulsing intensified orbs as they slowly settle for the remaining 1.5 seconds. Cinematic, smooth motion, depth of field preserved, no rotation. 7 seconds, 1920×1080.*

### Sound prompt

> *0 to 5 seconds: rising anxious synth bed — dissonant tonal cluster of three slightly-detuned notes that build in volume and density, communicating mounting tension. Layered with subtle stuttering electronic glitch sounds throughout that match the visual flickering of the question mark. At the 5-second mark: sharp incoming whoosh — a fast high-frequency air sweep that lasts about 0.3 seconds — immediately followed by a HARD cinematic boom impact (deep sub-bass with a metallic transient and high-frequency sparkle on the hit). After the impact: a low atmospheric drone tail with faint ringing sub-bass that fades out gradually over the remaining 2 seconds. No music melody, no dialogue. 7 seconds.*

**Splice/Epidemic search:** "tense synth riser 5s dissonant" + "whoosh impact boom" + "low atmospheric drone tail"

---

## Color reference for Runway prompts

When asking Runway to render brand colors, the hex codes don't always render accurately. Helpful synonyms:

| Brand | Hex | Synonyms that Runway tends to nail |
|---|---|---|
| Claude | `#d97757` | "warm Anthropic orange", "sunset clay", "burnt sienna" |
| Codex | `#10a37f` | "OpenAI emerald green", "deep teal", "jade" |
| Gemini | `#4285f4` | "Google sapphire blue", "cobalt", "deep azure" |
| JARVIS | `#FFD700` | "brilliant gold", "white-gold", "warm golden" |

Always include the hex code AND a descriptive synonym. If first generation is off-color, second-generation usually corrects.

---

## After Runway delivers the clip

1. **Drop the clip** at `video-XX-NAME/scenes/NN-pilot/assets/runwaybg.mp4`
2. **Open in Quicktime**. Watch through. Note the exact timestamp of the impact (it usually drifts ±1s from the brief).
3. **Update the HyperFrames overlay timing** to match the actual impact:
   - Title cascade fires ~2s before the impact
   - Title slam + pulseBloom + screenShake fire EXACTLY ON the impact
4. **Lint + render**

See [`ANTI-PATTERNS.md#a12--misjudging-runway-clip-impact-timing`](ANTI-PATTERNS.md#a12--misjudging-runway-clip-impact-timing) for the sync workflow.

---

## Things we won't use Runway for

Documented so we don't burn credits twice:

- **Cold-open hooks** — we tried this for Scene 1 ("chaos of multiple AI tools" workspace shot). The Runway aesthetic competes with the pure-HyperFrames vocabulary of later scenes. Pure-HyperFrames with real product screenshots is cleaner.
- **Anything with VO** — Runway audio conflicts with the VO bed.
- **Real-product-UI scenes** — use the actual screenshot. It's always more credible.
- **Long expository scenes** — too expensive per second; HyperFrames is the right tool.

---

## Future categories to template

When we ship these, add prompts here:

- **Outro hero card** — Runway-generated logo reveal for end card
- **Module transition** — between major sections of a long video
- **Stat-of-the-day** — single number reveal with sound
- **Higgsfield short clips** — when we add that integration
