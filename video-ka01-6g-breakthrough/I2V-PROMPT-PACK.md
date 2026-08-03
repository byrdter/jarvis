# Image-to-Video Prompt Pack

## Ownership

- **Codex:** Create every original still image needed by the episode, save the approved master still locally, and prepare the complete image-to-video prompt packet.
- **Terry:** Generate the requested video clips from the supplied stills and prompts, then return the rendered files for review and scene integration.
- **Codex after delivery:** Inspect motion, continuity, image integrity, duration, artifacts, and story fit; request a rerun when necessary; stage approved clips into scene-local `assets/` folders and record provenance.

Library footage and real source rolls remain the first choice when they already carry the beat. The still-to-video workflow fills only documented gaps.

## Status Flow

`needed → still-created → still-approved → prompt-ready → Terry-generating → delivered → reviewed → locked`

A clip cannot move to `prompt-ready` until its exact source still has been approved. Motion prompts are written against the pixels that actually exist, not an imagined future image.

## Required Handoff Packet

Every requested clip will arrive with all of these fields:

| Field | Requirement |
|---|---|
| Clip ID | Stable scene-based identifier, such as `S06-BR03` |
| Scene and cue | Scene number plus the VO phrase or narrative action it supports |
| Approved source still | Absolute local path and displayed preview |
| Output filename | `<scene>-<purpose>.mp4` |
| Output specification | 1920×1080, 16:9, silent, requested source duration and delivery format |
| Screen-use duration | Usually 3–5 seconds even if a longer generation is requested for edit handles |
| **Motion** | A bounded description of what the subject does during this exact shot |
| Camera | Push, drift, orbit, rack focus, locked camera, or another single restrained move |
| End state | What must be true in the final frame so the clip can cut cleanly |
| Must remain still | Important objects, people, doors, screens, or structures that may not change |
| Global negatives | No morphing, extra limbs/fingers, face distortion, invented text/logos, cuts, camera shake, or unrequested scene changes |
| Scene-specific negatives | Failure modes unique to the still and the intended meaning |
| Integration note | Crop, scrim, overlay, side-panel placement, and the HyperFrames event that follows |
| Acceptance test | The visible action that proves the generation succeeded |

## Global I2V Style

Restrained cinematic editorial motion. Preserve the approved composition, person identity, geometry, lighting, wardrobe, object count, and negative space. Use one clear subject action and one subtle camera move. Maintain the KeyAdvances palette: deep midnight navy/charcoal, restrained cyan technology light, and warm amber human consequence. No fast cuts, handheld shake, gratuitous spectacle, neon cyberpunk treatment, interface clutter, captions, logos, or watermarks.

## Global I2V Negatives

No warping or morphing of faces, hands, fingers, bodies, architecture, equipment, antennas, screens, or room geometry. No extra people, limbs, fingers, devices, cables, vehicles, or objects. No person turns to camera unless explicitly requested. No text, numbers, captions, logos, or watermarks appear or change. No cut, scene transition, camera shake, sudden zoom, focus pumping, lighting jump, or change of art style. Preserve the exact framing, palette, and subject identity of the source still.

## Current 6G Generation Queue

These are identified needs, not permission to generate before the corresponding still and prompt are approved.

| Clip ID | Scene | Purpose | Still Status | Prompt Status | Owner | Notes |
|---|---|---|---|---|---|---|
| S02-BR03 | S02 | Photonic light travels through the integrated chip | needed | blocked on still | Codex → Terry | Literal technical motion; equipment geometry must remain credible |
| S05-BR01 | S05 | Camera pulls back from tiny chip to the external optical bench | needed | blocked on still | Codex → Terry | Load-bearing reversal shot |
| S05-BR03 | S05 | Directional horn antennas establish the short laboratory link | needed | blocked on still | Codex → Terry | Preserve antenna count and 1.3-metre visual scale |
| S06-BR02 | S06 | Diverse person inside a radio-derived spatial mesh | needed | blocked on still | Codex → Terry | Thumbnail-adjacent hero; radio “inference,” not literal camera vision |
| S07-BR04 | S07 | Port or hospital machines coordinate from shared sensing | needed | blocked on library search/still | Codex → Terry | Generate only if the final database search fails |
| S09-BR02 | S09 | Ordinary room is sensed without a visible camera | needed | blocked on still | Codex → Terry | Quiet, plausible, non-dystopian visual |
| ALT-BR | various | Alternate vehicle, team, or field-worker clips needed to preserve single use | conditional | blocked on library search | Codex → Terry | Search the 883-asset database before creating stills |

## Prompt Entry Template

### `[CLIP-ID] — [short purpose]`

- **Scene / cue:**
- **Approved source still:**
- **Output filename:**
- **Generate:** 1920×1080, 16:9, silent, `[duration]` seconds
- **Screen-use target:**
- **Motion:**
- **Camera:**
- **End state:**
- **Must remain still:**
- **Scene-specific negatives:**
- **Append global negatives:** yes
- **Integration:**
- **Accept only if:**

The final prompt Terry receives will combine, in this order:

> **Motion** + **Camera** + **End state / must-remain-still instructions** + **Global I2V style** + **Scene-specific negatives** + **Global I2V negatives**
