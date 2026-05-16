# Token Flood Animation Design

## Style Prompt

Recreate the supplied neon cyberpunk token-overload image as an animated 20-second HyperFrames scene. It should feel like a high-end technical explainer: a dark isometric context window on the left, glowing tool tiles on the right, cyan data rays feeding into a red warning meter, and large readable pixel-style token text.

## Colors

- Deep canvas: `#07111f`
- Panel glass: `rgba(18, 36, 58, 0.72)`
- Cyan data flow: `#3ff7ff`
- Red overload: `#ff3d55`
- Orange token text: `#ffae63`
- Purple accent: `#9c5cff`
- Green active state: `#b8ff45`

## Typography

- Display: `Orbitron, Arial Black, sans-serif`
- Mono: `JetBrains Mono, Consolas, monospace`

## Motion Rules

- The `55,000 TOKENS` headline must flash and glow several times.
- The red context meter must scan up and down continuously.
- Tool tiles must cycle color/intensity; active tiles should feel like they are feeding the context window.
- Connection rays must pulse on/off with moving particles.
- Cursor is not used; this is a system animation, not UI operation.

## What NOT To Do

- Do not simply pan over the original bitmap.
- Do not use static stills with minor light sweeps.
- Do not leave large unused dead space.
- Do not make text too small to read at 1080p.
