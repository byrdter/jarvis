# Asset Contract

`asset-library/MANIFEST.json` is the source of truth for reusable production assets.

## Contract

- Look up assets by semantic key, not remembered path.
- Copy assets into scene-local `assets/` folders.
- Do not symlink final scene assets.
- Do not reference temporary screenshots, desktop files, or session folders from production HTML.
- Update the manifest whenever a reusable asset is added, moved, renamed, or replaced.

## Naming For New Assets

- Brain icons: `<brain>-brain.png`
- Product screenshots: `<product>-<surface>-<state>.png`
- B-roll variants: `<subject>-<action>--silent.mp4` and `<subject>-<action>--audio.mp4`
- Runway/Higgsfield clips: `<scene>-<purpose>.mp4`
- Web proof screenshots: `<source>-<page>-<state>.png`
- Thumbnails/concept frames: `<video>-thumbnail-<variant>.png`

Existing files with older names are grandfathered. Migrate only when touched for another reason.

## Required Metadata

For manifest entries, capture what automation needs:

- path
- root if outside asset-library
- dimensions or duration when known
- tags
- description
- audio/silent variant when applicable
- source/provenance for web or claim evidence

## Automation Direction

Future helpers should:

- resolve semantic keys
- copy assets to a scene folder
- validate manifest paths exist
- warn when a production scene references files outside its scene assets
- scaffold a scene with required assets and shared libraries
