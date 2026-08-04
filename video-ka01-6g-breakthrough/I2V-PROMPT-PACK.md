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
| S02-BR03 | S02 | Photonic light travels through the integrated chip | still-created | draft complete; awaiting still approval | Codex → Terry | Literal technical motion; equipment geometry must remain credible |
| S05-BR01 | S05 | Camera pulls back from tiny chip to the external optical bench | still-created | draft complete; awaiting still approval | Codex → Terry | Load-bearing reversal shot |
| S05-BR03 | S05 | Directional horn antennas establish the short laboratory link | still-created | draft complete; awaiting still approval | Codex → Terry | Preserve exactly two antennas and short visual scale |
| S06-BR02 | S06 | Person inside a radio-derived spatial mesh | still-created | draft complete; awaiting still approval | Codex → Terry | Thumbnail-adjacent hero; radio “inference,” not literal camera vision |
| S07-BR04 | S07 | Port or hospital machines coordinate from shared sensing | needed | blocked on library search/still | Codex → Terry | Generate only if the final database search fails |
| S09-BR02 | S09 | Ordinary room is sensed without a visible camera | still-created | draft complete; awaiting still approval | Codex → Terry | Quiet, plausible, non-dystopian visual |
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

## Draft Handoff Packets — Awaiting Still Approval

### `S02-BR03` — Photonic light path

- **Scene / cue:** S02, “It generated signals from zero point five to one hundred fifteen gigahertz.”
- **Source still:** `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/video-ka01-6g-breakthrough/02-assets/generated-stills/ka01-photonic-light-path-v1.png`
- **Output filename:** `s02-photonic-light-path.mp4`
- **Generate:** 1920×1080, 16:9, silent, 7 seconds
- **Screen-use target:** 3–5 seconds
- **Motion:** One amber optical pulse enters from the left connector, divides smoothly through the existing etched waveguides, then three restrained cyan output pulses travel through the existing right-side connectors. Animate only light intensity along paths already present.
- **Camera:** Very slow 4% macro push toward the chip center; no orbit.
- **End state:** Amber input subsides; cyan outputs remain softly illuminated for a clean cut.
- **Must remain still:** Chip, mount, connectors, cable count, optical table, and all etched geometry.
- **Scene-specific negatives:** No new waveguides, cables, connectors, sparks, heat, smoke, traveling text, or fantasy energy. Do not make the chip expand or flex.
- **Integration:** Full-frame under a `DEMONSTRATED / ILLUSTRATION` pairing; cut to the real Nature evidence crop before the numerical claim.
- **Accept only if:** The light follows the existing physical paths without any component morphing.

### `S05-BR01` — Laboratory pullback reversal

- **Scene / cue:** S05, “Pull back, and the experiment includes external lasers…”
- **Source still:** `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/video-ka01-6g-breakthrough/02-assets/generated-stills/ka01-optical-bench-reversal-v1.png`
- **Output filename:** `s05-chip-to-optical-bench-pullback.mp4`
- **Generate:** 1920×1080, 16:9, silent, 9 seconds
- **Screen-use target:** two 3–5-second segments, divided by apparatus callouts
- **Motion:** Begin close enough that the foreground chip dominates. Pull steadily backward and slightly upward until the full optical table, surrounding instruments, and both horn antennas are visible. Existing indicator lights may flicker subtly; nothing else moves.
- **Camera:** One smooth dolly-out with a mild crane-up, constant speed, no cut and no focus pumping.
- **End state:** Wide composition matching the approved still, with chip at lower center and horn gap visible above it.
- **Must remain still:** Every instrument, cable, chip, horn, mount, screen, rack, and bench edge.
- **Scene-specific negatives:** No equipment appears or vanishes; no cable crawl; no changing screen text; no laser beams in air; no camera rotation; no invented people.
- **Integration:** Start beneath the tiny-chip crop, then use HyperFrames callouts for lasers, amplifiers, detectors, horns, and `1.3 m` as the pullback exposes them.
- **Accept only if:** The shot reveals scale through camera movement alone and the apparatus remains geometrically identical.

### `S05-BR03` — Short horn-antenna link

- **Scene / cue:** S05, “The wireless path was about one point three metres.”
- **Source still:** `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/video-ka01-6g-breakthrough/02-assets/generated-stills/ka01-horn-short-link-v1.png`
- **Output filename:** `s05-horn-antenna-short-link.mp4`
- **Generate:** 1920×1080, 16:9, silent, 7 seconds
- **Screen-use target:** 3–4 seconds
- **Motion:** A single restrained cyan dotted pulse traverses the existing centerline from the left horn to the right horn, fades, then one weaker return pulse travels back. The analyzer trace may brighten once in response.
- **Camera:** Slow lateral slider move of no more than 3%, preserving antenna alignment.
- **End state:** Both horns remain aligned with the center gap empty and the signal dots faded.
- **Must remain still:** Exactly two horns, mounts, cables, analyzer, table, and background geometry.
- **Scene-specific negatives:** No antenna rotation, no giant beam, no sparks, no smoke, no additional dishes or horns, no ruler or text generated in the clip.
- **Integration:** HyperFrames draws the `1.3 m` ruler over the empty center gap after the pulse arrives.
- **Accept only if:** Exactly two unchanged horns remain and the signal stays on their shared axis.

### `S06-BR02` — Network-derived spatial map

- **Scene / cue:** S06, “A radio network doesn't see like a camera. It can infer.”
- **Source still:** `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/video-ka01-6g-breakthrough/02-assets/generated-stills/ka01-network-sensing-hero-v1.png`
- **Output filename:** `s06-person-radio-spatial-map.mp4`
- **Generate:** 1920×1080, 16:9, silent, 8 seconds
- **Screen-use target:** 4–5 seconds
- **Motion:** Cyan point-cloud contours reconstruct the room progressively from left to right. One radio arc sweeps past the person; the floor positioning rings tighten once around the person's existing feet. The person makes only a small natural head turn toward the reconstructed room.
- **Camera:** Slow 3% push toward the person; locked horizon.
- **End state:** Room mesh fully resolved, person still in the identical position, positioning rings softly lit.
- **Must remain still:** Person identity, face, body, hands, wardrobe, lamp, furniture, walls, and all architectural lines.
- **Scene-specific negatives:** No lip movement, walking, extra people, body tracking skeleton, camera icon, eye symbol, headset, phone, new furniture, or dense HUD text.
- **Integration:** Begin as thumbnail payoff with `IT CAN SEE`, then strike `SEE` and replace it with `INFER` in HyperFrames.
- **Accept only if:** The person remains anatomically stable and the motion reads as the room being inferred rather than photographed.

### `S09-BR02` — Ordinary room sensing

- **Scene / cue:** S09, “The same radio reflection can support a fall alert or an invisible occupancy log.”
- **Source still:** `/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis/video-ka01-6g-breakthrough/02-assets/generated-stills/ka01-ordinary-room-rf-sensing-v1.png`
- **Output filename:** `s09-ordinary-room-radio-sensing.mp4`
- **Generate:** 1920×1080, 16:9, silent, 7 seconds
- **Screen-use target:** 4–5 seconds
- **Motion:** A few cyan radio paths travel outward from the existing wall access point, reflect once from the sofa, floor, and doorway, then fade. The point-cloud surface resolves subtly in their wake. The warm lamp has a barely perceptible practical flicker.
- **Camera:** Slow, quiet push through the doorway direction, no pan.
- **End state:** Normal warm room remains; mesh is faint but readable; cane, sofa, and doorway unchanged.
- **Must remain still:** Furniture, cane, lamp, access point, doors, plants, floor, wall art, and room layout.
- **Scene-specific negatives:** No person appears, no fall is depicted, no CCTV camera, no warning siren, no horror lighting, no furniture morphing, and no new interface or text.
- **Integration:** Reuse the same signal once for a `FALL ALERT` benefit panel and once for an `OCCUPANCY LOG` risk panel; labels are added in HyperFrames, not generated video.
- **Accept only if:** The room stays ordinary and stable while the radio paths alone reveal the sensing layer.
