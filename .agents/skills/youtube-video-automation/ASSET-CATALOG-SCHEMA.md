# Asset Catalog Schema

The asset catalog is a JSON manifest that provides searchable metadata for all reusable video production assets (B-roll, screenshots, web-rolls, generated clips).

## File Location

**Primary catalog:** `jarvis-private/video-production/asset-library/MANIFEST.json`

**Per-project overrides:** `video-XX-name/local-assets/MANIFEST.json` (optional)

## Schema Version

Current version: `1.0`

Future versions will maintain backward compatibility. Version bumps occur only when breaking changes are introduced.

## Top-Level Structure

```json
{
  "$schema": "https://example.com/asset-manifest.schema.json",
  "version": "1.0",
  "description": "Source of truth for all V14-eligible video assets. Look up by semantic key (e.g. 'brains.claude.icon') instead of remembering file paths.",
  "roots": {
    "asset_library": ".",
    "video_assets": "../video-assets",
    "project_local": "./local-assets"
  },
  "conventions": { /* ... */ },
  "brains": { /* ... */ },
  "orbs": { /* ... */ },
  "broll": [ /* ... */ ],
  "screenshots": { /* ... */ },
  "web_rolls": [ /* ... */ ],
  "generated": [ /* ... */ ],
  "audio": [ /* ... */ ]
}
```

## Roots

Roots define base paths for asset resolution. Paths in asset entries are relative to these roots.

```json
"roots": {
  "asset_library": ".",
  "video_assets": "../video-assets",
  "project_local": "./local-assets"
}
```

**Resolution example:**
- Asset path: `b-roll/office-typing.mp4`
- Root: `video_assets`
- Resolved: `../video-assets/b-roll/office-typing.mp4` (relative to MANIFEST.json)

## Conventions

Documents naming rules and migration policy.

```json
"conventions": {
  "filename_rules": {
    "brain_icons": "<brain>-brain.png (lowercase kebab) — going forward. Existing PascalCase files (ClaudeBrain.png) grandfathered until next migration.",
    "broll_variants": "<subject>-<action>--silent.mp4 vs <subject>-<action>--audio.mp4. Existing files use opaque '2' suffix for silent — grandfathered.",
    "product_screenshots": "<product>-<surface>-<state>.png. Existing files use mixed conventions per vendor — grandfathered.",
    "runway_clips": "<scene>-<purpose>.mp4 (e.g. 03-title-hero.mp4, 07-transition-burst.mp4)"
  },
  "migration_policy": "Don't bulk-rename. Migrate individual files only when touched for unrelated reasons. Update this manifest immediately when paths move.",
  "asset_resolution": "Scenes copy assets into their own assets/ folder rather than referencing the library directly. HyperFrames' file server does not follow symlinks — always use cp."
}
```

## Brains

AI model brain icons and colors for multi-brain videos.

```json
"brains": {
  "claude": {
    "icon": "shared/ClaudeBrain.png",
    "icon_raw": "shared/ClaudeBrainRaw.png",
    "color_hex": "#d97757",
    "color_rgb": [217, 119, 87],
    "color_name": "sunset orange",
    "name": "Claude",
    "vendor": "Anthropic",
    "model_family": "claude-opus / sonnet / haiku"
  },
  "codex": { /* ... */ },
  "gemini": { /* ... */ }
}
```

**Semantic keys:** `brains.claude.icon`, `brains.codex.color_hex`, etc.

## Orbs

Router/orchestrator orb icons and colors.

```json
"orbs": {
  "jarvis": {
    "icon": "shared/JarvisOrb.png",
    "icon_raw": "shared/JarvisOrbRaw.png",
    "color_hex": "#FFD700",
    "color_name": "gold"
  }
}
```

## B-Roll

Documentary-style B-roll clips (office scenes, hands, devices, etc.).

```json
"broll": [
  {
    "id": "office-typing",
    "path": "b-roll/office-typing--silent.mp4",
    "root": "video_assets",
    "type": "video",
    "duration": 12.5,
    "resolution": "1920x1080",
    "fps": 30,
    "keywords": ["office", "typing", "productivity", "work", "desk", "laptop", "hands"],
    "description": "Close-up of hands typing on laptop keyboard in modern office with natural lighting",
    "variants": {
      "silent": "b-roll/office-typing--silent.mp4",
      "audio": "b-roll/office-typing--audio.mp4"
    },
    "audio_description": "Mechanical keyboard sounds, ambient office noise",
    "usage": "unrestricted",
    "source": "Pexels",
    "source_url": "https://www.pexels.com/video/...",
    "license": "CC0",
    "added": "2026-06-01",
    "last_used": "2026-06-15",
    "use_count": 3,
    "quality_score": 0.92,
    "notes": "Good for productivity/work scenes. Natural lighting looks premium."
  }
]
```

### B-Roll Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (semantic key) |
| `path` | string | Path relative to root |
| `root` | string | Root key from `roots` |
| `type` | `"video"` or `"image"` | Asset type |
| `keywords` | string[] | Searchable keywords |
| `description` | string | What the asset shows |
| `usage` | string | Usage rights (`"unrestricted"`, `"attribution"`, `"internal-only"`) |

### B-Roll Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `duration` | number | Seconds (video only) |
| `resolution` | string | `"1920x1080"`, `"3840x2160"`, etc. |
| `fps` | number | Frame rate (video only) |
| `variants` | object | Silent/audio variants |
| `audio_description` | string | What the audio contains |
| `source` | string | Where asset came from |
| `source_url` | string | Original URL |
| `license` | string | License type |
| `added` | string | ISO date added |
| `last_used` | string | ISO date last used |
| `use_count` | number | Times used in videos |
| `quality_score` | number | 0-1 quality rating |
| `notes` | string | Production notes |

## Screenshots

Product screenshots (Claude Code, Codex, Gemini, etc.) with UI annotations.

```json
"screenshots": {
  "claude_code_desktop": {
    "path": "products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png",
    "root": "asset_library",
    "dimensions": [3584, 2240],
    "aspect_ratio": "1.6",
    "dpi": 144,
    "format": "png",
    "input_box_pct": { "left": 16.5, "top": 81.5 },
    "description": "Claude Code Desktop with Sessions sidebar, Recents list (jarvis project), Local/jarvis/main/worktree branch indicators, Opus 4.8 selector, Max plan",
    "keywords": ["claude", "desktop", "sessions", "jarvis", "opus"],
    "interactive_regions": [
      {
        "label": "Sessions Sidebar",
        "bbox_pct": { "left": 0, "top": 0, "width": 16, "height": 100 }
      },
      {
        "label": "Input Box",
        "bbox_pct": { "left": 16.5, "top": 81.5, "width": 67, "height": 15 }
      }
    ],
    "captured": "2026-05-20",
    "platform": "macOS 14.4",
    "notes": "Max plan badge visible. Good for showing full interface."
  }
}
```

### Screenshot Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Path relative to root |
| `root` | string | Root key |
| `dimensions` | [width, height] | Pixel dimensions |
| `description` | string | What the screenshot shows |
| `keywords` | string[] | Searchable keywords |

### Screenshot Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `aspect_ratio` | string | Width/height ratio |
| `dpi` | number | Retina/HiDPI scale |
| `format` | string | `"png"`, `"jpg"`, `"webp"` |
| `input_box_pct` | object | Input box location (for cursor placement) |
| `interactive_regions` | array | UI regions with bounding boxes |
| `captured` | string | ISO date |
| `platform` | string | OS/browser version |
| `notes` | string | Production notes |

## Web Rolls

Scrolling website captures (docs, changelogs, Reddit threads, etc.).

```json
"web_rolls": [
  {
    "id": "anthropic-claude-code-announcement",
    "path": "web-rolls/anthropic-claude-code-launch.mp4",
    "root": "video_assets",
    "type": "video",
    "duration": 18.2,
    "resolution": "1920x1080",
    "url": "https://www.anthropic.com/news/claude-code",
    "captured": "2026-05-15",
    "description": "Scroll through Anthropic's Claude Code launch announcement",
    "keywords": ["anthropic", "claude-code", "announcement", "launch", "official"],
    "scroll_type": "smooth",
    "highlights": [
      { "timestamp": 3.5, "label": "Hero image" },
      { "timestamp": 8.2, "label": "Feature list" },
      { "timestamp": 14.1, "label": "Pricing section" }
    ],
    "usage": "fair-use",
    "notes": "Clear branded page. Use for source proof."
  }
]
```

### Web Roll Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `path` | string | Path relative to root |
| `url` | string | Source URL |
| `description` | string | What the web roll shows |
| `keywords` | string[] | Searchable keywords |

### Web Roll Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `duration` | number | Seconds |
| `resolution` | string | Video dimensions |
| `captured` | string | ISO date |
| `scroll_type` | string | `"smooth"`, `"step"`, `"jump"` |
| `highlights` | array | Key moments with timestamps |
| `usage` | string | Usage rights |
| `notes` | string | Production notes |

## Generated

AI-generated clips (Runway, Higgsfield, etc.).

```json
"generated": [
  {
    "id": "fork-road-choice",
    "path": "generated/runway/fork-road-automation-vs-augment.mp4",
    "root": "video_assets",
    "type": "video",
    "duration": 8.5,
    "resolution": "1280x768",
    "generator": "runway",
    "model": "gen-3-alpha",
    "prompt": "Cinematic aerial shot of a fork in a forest road. Left path labeled AUTOMATION (dark, industrial). Right path labeled AUGMENTATION (bright, organic). Camera slowly pushes forward, emphasizing the choice.",
    "seed": 42,
    "generated": "2026-06-10",
    "keywords": ["fork", "road", "choice", "automation", "augmentation", "decision"],
    "description": "Fork road visual representing automation vs augmentation choice",
    "cost_usd": 0.45,
    "iterations": 3,
    "selected_iteration": 2,
    "notes": "Iteration 2 had best lighting. Iteration 1 was too dark, iteration 3 had weird artifacts."
  }
]
```

### Generated Clip Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `path` | string | Path relative to root |
| `generator` | string | `"runway"`, `"higgsfield"`, `"pika"`, etc. |
| `prompt` | string | Generation prompt |
| `keywords` | string[] | Searchable keywords |
| `description` | string | What the clip shows |

### Generated Clip Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `duration` | number | Seconds |
| `resolution` | string | Video dimensions |
| `model` | string | Generator model version |
| `seed` | number | Deterministic seed |
| `generated` | string | ISO date |
| `cost_usd` | number | Generation cost |
| `iterations` | number | How many attempts |
| `selected_iteration` | number | Which iteration was chosen |
| `notes` | string | Why this was chosen |

## Audio

Music beds, sound effects, ambient audio.

```json
"audio": [
  {
    "id": "ambient-office-noise",
    "path": "audio/sfx/ambient-office-typing-phones.mp3",
    "root": "video_assets",
    "type": "audio",
    "duration": 120.0,
    "format": "mp3",
    "bitrate": "192kbps",
    "sample_rate": 48000,
    "channels": "stereo",
    "keywords": ["ambient", "office", "typing", "phones", "background"],
    "description": "Subtle office ambiance with distant typing and phone calls",
    "usage": "unrestricted",
    "source": "Freesound",
    "license": "CC0",
    "volume_recommendation": 0.15,
    "notes": "Layer under VO for office scenes. Keep volume low (0.1-0.2)."
  }
]
```

## Search API (Conceptual)

The asset catalog should support keyword-based search with ranking.

**Python example:**
```python
def search_assets(query_keywords, asset_type=None, min_duration=None, max_duration=None):
    """
    Search catalog by keywords.
    
    Args:
        query_keywords: List of keywords (e.g. ["office", "typing", "productivity"])
        asset_type: Filter by type ("video", "image", "screenshot", "web_roll", "generated")
        min_duration: Minimum duration in seconds (video only)
        max_duration: Maximum duration in seconds (video only)
    
    Returns:
        List of (asset, score) tuples, sorted by score descending
    """
    results = []
    
    for asset in catalog:
        # Type filter
        if asset_type and asset.get("type") != asset_type:
            continue
        
        # Duration filter (video only)
        if min_duration and asset.get("duration", 0) < min_duration:
            continue
        if max_duration and asset.get("duration", float('inf')) > max_duration:
            continue
        
        # Keyword matching
        asset_keywords = asset.get("keywords", [])
        asset_description = asset.get("description", "").lower().split()
        asset_text = set(asset_keywords + asset_description)
        
        # Calculate match score
        matches = len(set(query_keywords) & asset_text)
        total_query = len(query_keywords)
        score = matches / total_query if total_query > 0 else 0.0
        
        # Boost exact ID matches
        if asset.get("id") in query_keywords:
            score += 0.5
        
        # Only include if score above threshold
        if score >= 0.3:
            results.append((asset, score))
    
    # Sort by score descending
    return sorted(results, key=lambda x: x[1], reverse=True)
```

**Example usage:**
```python
# Find office B-roll ≥10 seconds
results = search_assets(
    query_keywords=["office", "typing", "desk"],
    asset_type="video",
    min_duration=10.0
)

for asset, score in results:
    print(f"{asset['id']} (score: {score:.2f}) — {asset['description']}")
```

**Expected output:**
```
office-typing (score: 0.92) — Close-up of hands typing on laptop in modern office
desk-work-overhead (score: 0.75) — Overhead view of organized desk with laptop and notes
office-meeting (score: 0.42) — Team meeting in modern office conference room
```

## Validation Rules

The catalog should enforce these validation rules:

### 1. Unique IDs
All `id` fields must be unique across the entire catalog.

### 2. Path Existence
All `path` values must point to existing files.

```python
def validate_path(asset):
    root_path = roots[asset["root"]]
    full_path = os.path.join(root_path, asset["path"])
    if not os.path.exists(full_path):
        raise ValidationError(f"Asset {asset['id']}: path does not exist: {full_path}")
```

### 3. Required Fields
Each asset type must have its required fields.

### 4. Duration Consistency (Video)
For video assets, `duration` from metadata should match actual ffprobe duration ±0.5s.

```python
def validate_duration(asset):
    if asset["type"] != "video":
        return
    
    declared = asset.get("duration")
    if not declared:
        return  # duration is optional
    
    actual = get_ffprobe_duration(asset["path"])
    diff = abs(actual - declared)
    
    if diff > 0.5:
        raise ValidationError(f"Asset {asset['id']}: duration mismatch. Declared {declared}s, actual {actual}s")
```

### 5. Keyword Non-Empty
All assets must have at least one keyword.

### 6. Resolution Format
Resolution strings must match pattern `WIDTHxHEIGHT` (e.g. `"1920x1080"`).

## Maintenance

### Adding New Assets

1. Copy asset file to appropriate location in `asset-library/` or `video-assets/`
2. Add entry to `MANIFEST.json` in appropriate section (`broll`, `screenshots`, etc.)
3. Validate with schema checker (future tool)
4. Commit to git

### Updating Existing Assets

1. Update metadata fields in `MANIFEST.json`
2. If path changes, update `path` field AND move physical file
3. Increment `use_count` when asset is used in new video
4. Update `last_used` to current date

### Removing Assets

1. Check `use_count` and `last_used` before removing
2. If `use_count > 0`, consider archiving instead of deleting
3. Remove entry from `MANIFEST.json`
4. Move physical file to `archive/` directory (don't delete immediately)
5. Commit to git with reason

## Future Enhancements

### Version 1.1 (Planned)

- **Auto-tagging:** Use AI to suggest keywords from visual analysis
- **Thumbnail generation:** Auto-generate preview thumbnails for quick browsing
- **Similarity search:** Find visually similar B-roll based on embeddings
- **Usage analytics:** Track which assets get highest engagement in published videos
- **Quality scoring:** Auto-score assets based on resolution, lighting, composition
- **Smart variants:** Auto-detect silent/audio variants by file naming convention

### Version 1.2 (Future)

- **Web interface:** Browse and search catalog via local web UI
- **Batch import:** Import multiple assets with CSV metadata
- **AI generation integration:** Generate missing assets directly from catalog search
- **Asset pipelines:** Auto-process new assets (transcode, thumbnail, tag)
