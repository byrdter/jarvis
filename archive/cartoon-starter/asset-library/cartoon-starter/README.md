# Cartoon Starter Library

Reusable flat cartoon assets for CuriosaMente-style explainer videos and HyperFrames scenes.

This starter kit is intentionally source-first: assets are SVG, grouped with stable IDs where useful, and designed for simple motion such as pop-ins, camera pushes, prop slides, pose swaps, labels, arrows, and diagram builds.

## What Is Included

- 4 recurring/support host characters
- 40 layered host poses across the four hosts
- 40 standalone expression/head assets, 10 per host
- 40 science, tech, media, legal, office, and everyday props
- 40 diagram and callout elements
- 20 16:9 cartoon backgrounds
- 8 transparent texture overlays
- 16 HyperFrames-oriented animation presets

## Tier 2 Coverage

Tier 2 expands the kit from a minimum viable identity into a reusable production library for explainers:

- Hosts A/B remain the primary recurring presenters.
- Hosts C/D are supporting characters for expert, skeptic, student, witness, or audience roles.
- Props now cover science, tech, media production, legal/courtroom, education, and general workflow scenes.
- Diagrams now include evidence cards, risk ladders, myth/fact panels, network maps, heatmaps, probability balls, source tags, caption boxes, and process systems.
- Backgrounds now cover newsroom, podcast studio, hospital, library, factory, data center, museum, whiteboard room, internet map, and outdoor field scenes.
- Motion presets now cover pop, drift, shake, orbit, draw, blink, squash, wiggle, parallax, stamp, wipe, pulse, thought bubble, and diagram build patterns.

Run the generator whenever the source templates change:

```bash
node asset-library/cartoon-starter/scripts/build-assets.mjs
```

The generated catalog is written to `CATALOG.md`, and the machine-readable inventory is written to `manifest.json`.

## Production Rules

- Prefer SVG assets for reusable characters, icons, diagrams, and props.
- Use generated bitmap stills only for complex one-off scenes, painterly backgrounds, thumbnails, or assets that are not worth vectorizing.
- Use Higgsfield only for hard-to-fake motion: walk cycles, complex animal movement, cinematic action, or organic motion that would take longer to rig than to generate.
- Keep new assets in this library only when they are reusable across future videos. Episode-specific images should live with the episode project.

## HyperFrames Usage

Most SVGs expose predictable groups such as `character`, `head`, `torso`, `arm-left`, `arm-right`, `held-prop`, `diagram`, `background`, `texture`, or `prop`. Import the SVG as an image for simple moves, or inline the SVG when you need to target internal groups.

Recommended scene workflow:

1. Choose a background.
2. Add one host pose or topic character.
3. Add props and diagram elements as independent layers.
4. Animate with small, readable moves: pop, drift, push, shake, reveal, orbit, label draw.
5. Save any genuinely reusable new element back into this library.
