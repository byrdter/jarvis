# Asset Contract

## Canonical library + how to query it

The canonical asset library is the **searchable DB**:

```
~/Library/CloudStorage/Dropbox/jarvis/asset-library/assets.db   (+ clip-library/ media, products/ screenshots)
```

280+ assets, each with AI metadata (description, mood, setting, people, color_palette) PLUS
`symbolizes` (abstract ideas it can represent) and `usable_as` (breather / background /
establishing / symbolic / literal). All `file_path`s are absolute and resolve.

Media lives under `clip-library/`: `videos/` (B-roll clips), `backgrounds/` (cinematic
dark-register photographic backgrounds — bg-still Ken-Burns layers, added from V3/V5 in 2026-07),
`images/`, plus the `pixel*` / `addition-images` variant sets. Query the DB, don't browse by folder.

**Query it** with the tool in the youtube-video-automation skill (referenced, not duplicated —
see PIPELINE / VISUAL-SOURCING):

```bash
# hybrid semantic + keyword search (needs OPENAI_API_KEY for the query embedding)
python3 .agents/skills/youtube-video-automation/tools/search-assets-db.py "5s calm clip, relief" \
  --db ~/Library/CloudStorage/Dropbox/jarvis/asset-library/assets.db --top 8 --json
# filter by type/duration:  --type video --min-duration 4
```

> Both `search-assets-db.py` and `batch-analyze-assets.py` use the flag **`--db`** (not
> `--db-path`). Web-roll PNGs taller than ~8000px will be rejected by the vision API — capture
> at viewport height or split before tagging.

For non-HyperFrames sourcing, query by what an asset can REPRESENT and how it can be USED (the
`symbolizes` / `usable_as` fields) — see `knowledge/VISUAL-SOURCING.md`.

### Tooling (all in youtube-video-automation/tools/, run against the canonical DB)
- `search-assets-db.py` — find assets (semantic + keyword)
- `batch-analyze-assets.py` — AI-tag NEW assets (Claude vision → description/mood/.../symbolizes/usable_as) + embeddings
- `enrich-symbolic-tags.py` — backfill `symbolizes`/`usable_as` on existing rows from their metadata
- `init-asset-db.py`, `generate-embeddings.py`, `resolve-assets.py`

### Adding new assets (the loop)
1. Drop files into `asset-library/clip-library/<category>/` (or `products/`).
2. Tag: `python3 .../batch-analyze-assets.py --asset-dir <dir> --db <canonical db> --skip-existing`
   (writes metadata + embeddings + symbolizes/usable_as; `--skip-existing` avoids re-billing API
   calls on assets already tagged).
3. They're now queryable. Update this contract / VISUAL-SOURCING if a new category or tag emerges.

## Secondary library (migrating in)
`${JARVIS_PRIVATE}/video-production/asset-library/` (MANIFEST.json semantic keys for V14 brand
icons + `capture-runner.js` web-roll capture). Treat the DB above as canonical; migrate this
library's assets into the DB as they're used, and point `capture-runner.js` output at the DB.

## Contract (per scene)
- Find assets by **querying the DB**, not by remembering paths.
- Copy chosen assets into the scene-local `assets/` folder. Do NOT symlink final scene assets.
- Do not reference temporary screenshots, desktop files, or session folders from production HTML.
- After using/adding a reusable asset, make sure it's tagged in the DB.

## Naming for new assets
- B-roll variants: `<subject>-<action>--silent.mp4` / `--audio.mp4` (strip audio under VO)
- Product/tool screenshots: `<product>-<surface>-<state>.png`
- Web proof screenshots: `<source>-<page>-<state>.png`
- Runway/Higgsfield clips: `<scene>-<purpose>.mp4`
- Brain icons: `<brain>-brain.png`
Older names are grandfathered; migrate only when touched for another reason.

## Required metadata (the DB captures this)
path · type · duration/dimensions · description · mood · setting · people · color_palette ·
**symbolizes** · **usable_as** · keywords · source/provenance (for web/claim evidence) ·
audio/silent variant when applicable.
