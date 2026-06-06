# Terminal Session

**STATUS:** to-build
**Channel fit:** universal
**Tone fit:** educational, technical-demo

## Use case
A standalone terminal (no IDE chrome) with prompt → command typed → output streams → next prompt. Used for CLI tool demos, MCP server interactions, command-line workflows.

## Pattern (to implement)
- Dark terminal background (`#0a0a0a` or `#1e1e1e`), monospace.
- Visible cursor block at the prompt position.
- Command appears typewriter-style at the prompt.
- After command, output streams below.
- Next prompt appears at the bottom; cursor moves there.

## Build approach
- HTML: `<pre>` blocks with `<span>` elements for prompt vs command vs output (different colors).
- Typewriter for command: GSAP stagger on character spans, `opacity: 0 → 1`, 0.04–0.06s per character.
- Output streams: same approach, faster (0.02s per character) or per-line (0.1s per line).
- Cursor: separate `<span>` with a CSS `@keyframes blink` (but use a finite-iteration version for HyperFrames determinism).
- Prompt colors: green for `$`, cyan for paths, white for commands, gray for output.

## Reference (public examples)
- Most developer-focused HyperFrames templates include a terminal pattern.
- Existing Module 08 references a code/log panel inline ("github.read_file()...") that's a simpler version of this — could be the seed pattern.

## Anti-patterns (anticipated)
- Typewriter too fast — feels fake (humans don't type at 30 chars/sec without errors).
- Typewriter too slow — pacing wrecker.
- Prompt or output text in poor contrast — terminals need crisp readability.
- Terminal frame floating with no shadow — looks pasted in. Add a soft drop shadow + rounded corners (8px) to feel like a window.

## Build location when first needed
Likely in a Part 2 CLI module showing a real CLI tool being invoked, or MCP demonstrating a server interaction.
