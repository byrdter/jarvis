---
name: hyperframes-video-director
description: Use when creating, revising, planning, or QAing Jarvis YouTube video scenes in HyperFrames, especially Video 12 and future videos that need Austin-style visual pacing, animated technical infographics, storyboard/still-to-HyperFrames conversion, simulated IDE/code scenes, dynamic scene transitions, or decisions about HyperFrames versus still images versus real screen recordings.
---

# HyperFrames Video Director

This is the Jarvis visual direction standard for YouTube videos. Use it with the `hyperframes`, `hyperframes-cli`, and `gsap` skills when building or revising scenes.

## Default Decision

Use **HyperFrames as the default visual system** for everything except talking-head/avatar footage.

Only use another source when it is clearly better:

- **Real screen recording**: use when believability depends on actual software behavior, a real website, a real product workflow, or source evidence.
- **Still image**: use for complex one-off art, real screenshots, source evidence, or highly detailed imagery that would be wasteful to rebuild.
- **Simulated UI/IDE/code**: prefer HyperFrames for VS Code, terminals, dashboards, code review, tool calls, schema/result cards, and technical workflows so code can be highlighted, transformed, rearranged, or timed to narration.

When stills or screenshots are used, animate them. Never treat a still as a dead full-screen slide unless the script needs a deliberate pause.

## Scene Standard

Each narrative segment should normally contain **2-3 visual beats**. Use more only when the voiceover naturally demands it.

Every segment needs at least one of these:

- Build: pieces assemble into a complete idea.
- Reveal: hidden information appears in timed layers.
- Transformation: bad state becomes good state, large payload compresses, messy stack organizes.
- Comparison: before/after, small/large, old/new, tool/result.
- Evidence: source screenshot or recording is framed, highlighted, and tied to the claim.
- Escalation: meter, needle, stack, count, or warning rises as the narration intensifies.

Avoid the old failure mode: one static dark panel with centered text and a few boxes for the entire segment.

## Concept-Art Workflow

When no finished still exists, write a **concept-art prompt** for the subsegment first, then build the HyperFrames scene from that prompt. The prompt is a storyboard, not necessarily an image-generation request.

Use this compact format:

```text
Scene idea:
Main visual:
Objects:
Motion:
Information hierarchy:
Transition in:
Transition out:
What must remain readable:
```

Use existing stills such as `002A.png` and `002B.png` as style references: dense but legible technical editorial graphics, glowing diagnostic frames, dashboards, flows, pages, meters, tool stacks, status panels, and energetic transitions.

## Motion Rules

Motion should serve the narration, not decorate randomly.

- Start a new beat when the voiceover introduces a new clause, contrast, tool, problem, or result.
- Keep important text still long enough to read.
- Use different entrance/exit patterns across neighboring beats.
- Animate chart/data/system objects more often than plain text.
- Let scenes hold for 1-3 seconds after the final build so the viewer can absorb the point.
- Prefer precise motion: slide, stack, snap, sweep, meter climb, card fan, path travel, tile dissolve, mask wipe, parallax, camera push.
- Use fades sparingly; a fade alone is not enough for most Video 12 scenes.

For detailed motion patterns, read [references/motion-vocabulary.md](references/motion-vocabulary.md).

## 002A/002B Lessons

The successful proof scenes established the target:

- Rebuild concept art as editable HyperFrames objects, not static backgrounds.
- Use many simple objects together: panels, cards, paths, bars, charts, token meters, windows, stream particles.
- Animate the information architecture: pages move into context, tool definitions stack, side panels arrive, totals glow.
- Keep the completed scene on screen briefly after assembly.
- Use stills as reference direction, not as a crutch.

## QA Before Final

For every HyperFrames proof or final scene:

1. Run `npx hyperframes lint`.
2. Capture snapshots at early/mid/late times.
3. Inspect at least the mid and final frames.
4. Render a short MP4.
5. Run `ffprobe` to confirm duration, resolution, and frame rate.
6. Create a contact sheet for quick review when useful.

Reject or revise scenes where text overflows, key content is covered, motion is only a fade, or the final frame reads like generic dark-box filler.
