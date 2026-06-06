# Action Blips

**STATUS:** proven
**Channel fit:** Byrddynasty, universal
**Tone fit:** educational, technical-demo

## Use case
Small monospace pill-shaped labels that pop out of a hero element, drift outward briefly, then fade. Perfect for enumerating concrete actions while the VO lists them ("api.call(), read_file(), send_message(), ...").

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/008-tools/hyperframes/index.html` (`.blip`, `.blip-api`, `.blip-file`, `.blip-msg`, `.blip-db`, `.blip-work`).

## Build notes
- Pill: ~36–44px tall, monospace text, dark navy bg, cyan border, cyan text, slight glow.
- Start position: at the hero element's center.
- Motion (per blip):
  ```js
  // Pop in at center
  tl.fromTo(selector,
    { opacity: 0, scale: 0.5, x: 0, y: 0 },
    { opacity: 1, scale: 1.0, duration: 0.35, ease: "back.out(2.2)", transformOrigin: "center center" },
    vTime);
  // Drift outward
  tl.to(selector,
    { x: dx, y: dy, duration: 1.1, ease: "power2.out" },
    vTime + 0.05);
  // Fade out
  tl.to(selector,
    { opacity: 0, duration: 0.4, ease: "power2.in" },
    vTime + 0.95);
  ```
- Drift directions: typically up-left, up-right, down-left, down-right for 4 blips; or single up-center for a "real work" closer beat.
- Timing: anchor each blip to its VO word using whisper-cli timestamps.

## Anti-patterns
- Don't let two blips collide mid-flight — stagger drift directions.
- Don't extend blip lifetime past 1.5s — they're meant as quick flashes, not sustained labels.
- Don't use blips when the satellites are already visible at the corners — the blip drift collides visually with the satellites. Either use blips OR satellites in a given beat, not both. (Modules 08 used blips BEFORE satellites arrived.)

## Example beats
- Module 08 (Beat 4) — "To call an API. To read a file. To send a message. To query a database. To do real work." Five blips fire at the exact VO word boundaries (15.55s, 16.85s, 18.35s, 19.95s, 22.00s).
