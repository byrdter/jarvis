# Flow Node with Floating Label

**STATUS:** proven
**Channel fit:** universal
**Tone fit:** educational, technical-demo

## Use case
A small dot (the "node") with a label floating above it — NO containing chip, no card, no rectangle. The canonical "no box" diagram primitive. Used to label points in a flow, network, or system diagram. Replaces what you'd otherwise put in a labeled rectangle.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/010-mcp-what-it-is/hyperframes/index.html` (`.flow-node`, `.flow-agent`, `.flow-service`, `.flow-mcp-center`).

## Build notes
- Label: Inter 800, ~38px, letter-spacing 0.12em, uppercase, dark navy, centered.
- Dot below the label via `::after`:
  ```css
  .flow-node::after {
    content: ""; display: block; width: 10px; height: 10px; border-radius: 999px;
    background: transparent; border: 2px solid #34F5FF;
    margin: 12px auto 0;
  }
  ```
- For "filled" nodes (the centerpiece), use `background: #34F5FF; box-shadow: 0 0 18px rgba(52, 245, 255, 0.7);`
- For fan-out variants (smaller secondary nodes), use 22px font + 8px dot.

## Anti-patterns
- Adding any background fill or border to the LABEL — that's a chip/card. Forbidden by the "earn every container" rule unless explicitly justified.
- Placing labels TOO close to neighboring labels — give 80-120px vertical spacing minimum at 22-38pt sizes.
- Using only the dot without a label — viewers can't identify the node.
- Multiple nodes overlapping in screen space — see Module 10 R1 anti-pattern (Cursor / AGENT collision).

## Example beats
- Module 10 (Beat 3+) — AGENT / SERVICE labels with dot nodes on a cream stage flow diagram.
- Module 10 (Beat 5) — multi-agent / multi-service fan-out: 3 left nodes + 4 right nodes, all label+dot, no chips.
