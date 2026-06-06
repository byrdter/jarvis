# Monospace on Stage

**STATUS:** proven
**Channel fit:** universal
**Tone fit:** educational, technical-demo

## Use case
Code fragments, command output, API call signatures rendered as monospace text directly on the cream stage — NO terminal chrome, NO IDE window, NO contained card. Used when you need to show "real" code in a teaching context without committing to a full terminal/IDE simulation.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/010-mcp-what-it-is/hyperframes/index.html` (`.code-request`, `.code-response`).

## Build notes
- Font: JetBrains Mono 500, ~28px, line-height 1.3 (tighter than body — code reads better tightly packed).
- Subtle highlight stripe BEHIND the text: `background: rgba(15, 20, 32, 0.05); border-radius: 6px; padding: 10px 28px;` — provides just enough containment to read against the cream stage without being a card.
- Position each line as a SEPARATE absolute-positioned div with its own `top` value. **Do NOT stack lines as children of a single container** — the layout becomes hard to control and can produce mystery offsets (see Module 10 R1 anti-pattern: response rendered 150px lower than expected when stacked as spans inside a parent div).
- Color the special tokens: `→` in cyan + bold, comments in muted brown, strings in default dark navy.
- Typewriter reveal optional (per-character `opacity: 0 → 1` stagger). For Module 10 we used a simpler fade-in for the whole line — typewriter is more dramatic but slower.

## Anti-patterns
- **Stacking child spans with `display: block` inside one container** — layout offsets are unpredictable. Use separate absolute-positioned divs.
- Adding a full dark "terminal" background — that becomes a card. If you need a terminal window, use `terminal-session.md` instead.
- Too much code at once — keep to 1–3 lines per beat. Long code blocks belong in `vscode-ide-simulation.md`.
- Mixing this with monospace-in-a-card in the same module — pick one treatment per module.

## Example beats
- Module 10 Beat 6 — `tools/call: github.read_file("README.md")` and `→ "# Project..."` as two separate lines on cream with subtle highlight stripes.

## When to escalate to full chrome
- Multi-line code (>5 lines)? Use `vscode-ide-simulation.md`.
- Interactive command-output sequences? Use `terminal-session.md`.
- Single illustrative line or two? Stay with `monospace-on-stage`.
