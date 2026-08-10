# Image-Generation Prompt Packet

Mode used: built-in image generation with local reference images. All selected project assets are stored in `../frames/`.

The first anchor used the previous fall-detection still only as an identity and environment reference. Every later home frame used the selected continuity anchor or fall frame. Emergency-response frames used the first ambulance-bay frame as their continuity reference.

## Global continuity lock

- 16:9 premium documentary cinematography, photorealistic and restrained.
- Elena: late seventies, short softly waved silver-white hair, cream cardigan, off-white top, beige trousers and shoes.
- Home: blue armchair, neutral sofa, wood table and floor, patterned rug, photographs, plants, amber lamps.
- Human world is warm amber; network visualization is restrained cyan with amber trajectory accents.
- Never show a surveillance camera, wearable, medical pendant, obvious router, glowing sensor gadget, floating interface, generic hologram panel, watermark, or cyberpunk city.

## F01 — Ordinary moment

Reference: `../../02-assets/generated-stills-v2/s06-parent-fall-detection-v2.png`

> Create a new wide establishing shot of the same older woman and the same warm, lived-in living room from the reference, several seconds before the fall. She is standing naturally near the blue armchair carrying a ceramic mug toward the coffee table, unaware anything is wrong. Use restrained premium documentary cinematography, natural skin texture, coherent floor space, warm window light, and no visible technology or overlays.

## F02 — Trip

Reference: `../frames/f01-ordinary-moment.png`

> Capture the split second Elena's slipper catches the edge of the rug while she carries the ceramic mug. Her balance breaks, one hand reaches toward the armchair, and a small arc of liquid leaves the tilting mug. Preserve identity, wardrobe, room layout, lighting, and believable anatomy.

## F03 — Fall impact

Reference: `../frames/f01-ordinary-moment.png`

> Show Elena immediately after the fall. The ceramic mug is shattered on the wood beside spilled tea while she lies partly on the rug near the blue armchair, stunned and trying to orient herself. Use an overhead-oblique wide shot; serious but not graphic, with no injury or blood.

## F04 — Phone out of reach

Reference: `../frames/f01-ordinary-moment.png`

> Elena's fingers stretch toward a smartphone lying beyond reach under the coffee table, with a clear gap between hand and phone. Her face is softly out of focus in the background. Use a floor-level close shot, shallow depth of field, and a dark phone screen.

## F05 — Room notices

Reference: `../frames/f03-fall-impact.png`

> Preserve the fallen-woman scene but reveal camera-free radio sensing as invisible structure becoming barely visible: thin restrained cyan wavefronts reflect from walls, chair, floor, and Elena's body. The contours originate from the surrounding room rather than an obvious gadget. Keep the real woman as the focal point.

## F06 — Fall reconstructed

Reference: `../frames/f03-fall-impact.png`

> Transform the scene into a camera-free spatial reconstruction while keeping the room photoreal and recognizable. A restrained cyan point-cloud reconstructs Elena's body position; an amber motion trail drops from standing height to the floor and ends in the cyan contour. Avoid dashboards and written labels.

## F07 — Routine broken

Reference: `../frames/f03-fall-impact.png`

> Show the room from near-ceiling top down as an inferred motion map rather than a camera feed. Elena is a soft cyan contour on the floor. A luminous amber path shows her last steps and a sharp break downward. Subtle fading routine paths suggest the system has a history of movement.

## F08 — Response begins

Reference: `../frames/f01-ordinary-moment.png` for color and realism only.

> Inside a regional ambulance bay in the same plausible 2034 world, two paramedics react as a wall-integrated amber incident signal comes alive. One grabs a compact medical bag while the other turns toward the ambulance; bay doors are beginning to open. Use real uniforms and equipment, no floating screens or fantasy design.

## F09 — Ambulance departs

Reference: `../frames/f08-response-begins.png`

> Continue the same response: the ambulance accelerates out of the regional bay as the doors finish opening, wet pavement catching amber bay light. One paramedic is visible through the windshield. Use a low exterior three-quarter angle, restrained motion blur, and strict vehicle/weather continuity.

## F10 — Help en route

Reference: `../frames/f08-response-begins.png`

> The same ambulance moves quickly along a wet two-lane road outside a regional city toward Elena's home at dusk. A restrained cyan route trace is anchored to the road surface and faint amber pulses suggest traffic signals clearing ahead. Use an elevated trailing view, documentary realism, and no map panel or floating interface.

## Rejected output

An attempted close return to Elena drifted in identity and was not copied into the project. Frame 11 therefore makes a motivated return to the approved top-down routine map (`f07`) and will create new information through HyperFrames motion rather than accepting an inconsistent face.

