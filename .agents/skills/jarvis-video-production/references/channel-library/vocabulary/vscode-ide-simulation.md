# VS Code / IDE Simulation

**STATUS:** to-build
**Channel fit:** universal (high priority for Byrddynasty + faceless dev channels)
**Tone fit:** educational, technical-demo, developer-product

## Use case
A simulated VS Code (or generic IDE) window showing file tree + tabs + syntax-highlighted code + an integrated terminal panel running realistic command sequences with believable stdout. The natural shape for "the agent writes code and runs it" beats — load-bearing for Part 2's Code Execution segments.

## Pattern (to implement)

### Layout
- **Activity bar** (left, ~52px): icon column.
- **File tree** (~280px): collapsible folders with files.
- **Editor pane** (flex): tab strip on top, code body below with line numbers + syntax highlighting.
- **Integrated terminal** (~30% of editor height, bottom): monospace, optional split.

### Behavior
- Code appears with a typewriter effect (per-character or per-token) on a target file.
- Tabs can switch via cursor click (see `cursor-click-inline-reveal.md`).
- Terminal command appears typed character-by-character, then output streams.
- File tree items can highlight when their file is being edited.

## Build approach
- HTML/CSS for IDE chrome: dark `#1e1e1e` activity bar, `#252526` sidebar, `#1e1e1e` editor, `#1e1e1e` terminal — match VS Code's actual dark theme.
- Syntax highlighting: pre-tokenize the code as colored `<span>` elements; or use Prism.js inline at runtime. For a deterministic capture, prefer pre-tokenized HTML.
- Typewriter: GSAP `stagger` over the character/token spans, revealing them with `opacity: 0 → 1` (faster) or fully appearing in sequence (slower).
- Terminal: a `<pre>` block with monospace text. Use the same stagger approach for stdout output.
- Use real-feeling content: actual MCP CLI calls, real file paths, plausible stdout. Fake-looking code breaks suspension of disbelief.

## Reference (public examples)
- Many HyperFrames developer-channel templates include VS Code panels.
- Cursor IDE demo templates show file-tree + tabs + code + terminal as a unit.

## Anti-patterns (anticipated)
- IDE chrome that doesn't match a known editor — viewers don't recognize it as code.
- Tokens revealing too slowly (typewriter that takes 8s for one line) — pacing wrecker.
- Generic stdout ("Output: success!") instead of realistic output ("✓ 23 files indexed in 1.2s") — breaks credibility.
- Light theme IDE on a dark stage — high contrast clash. Use dark IDE on cream stage only with a contained frame/border.

## Build location when first needed
Almost certainly in a Part 2 Code Execution module showing the agent writing + running code. Could also appear in Skills (procedural code) or MCP (CLI-style invocations).
