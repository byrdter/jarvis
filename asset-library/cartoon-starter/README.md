# Cartoon Starter Library

Reusable flat cartoon assets for CuriosaMente-style explainer videos and HyperFrames scenes.

This starter kit is intentionally source-first: assets are SVG, grouped with stable IDs where useful, and designed for simple motion such as pop-ins, camera pushes, prop slides, pose swaps, labels, arrows, and diagram builds.

## What Is Included

- 2 recurring host characters
- 16 layered host poses across the two hosts
- 20 standalone expression/head assets, 10 per host
- 20 science, office, and everyday props
- 20 diagram and callout elements
- 10 16:9 cartoon backgrounds
- 5 transparent texture overlays
- HyperFrames-oriented animation presets

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
