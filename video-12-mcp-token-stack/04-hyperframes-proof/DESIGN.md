# Video 12 HyperFrames Proof Design

## Style Prompt

Build a high-contrast developer operations video that feels like a premium VS Code demo, not a slide deck. The screen should look active: editor tabs, file tree, terminal output, command palette, cursor motion, token meters, and code panels should react to the voiceover. Use dark technical surfaces with cyan, amber, green, and red status colors.

## Colors

- Canvas: `#06090f`
- Panel: `#0d1320`
- Panel elevated: `#111b2d`
- Border: `#24324d`
- Text primary: `#f7fbff`
- Text muted: `#8ea3bd`
- Cyan action: `#3ee7ff`
- Green success: `#46f39a`
- Amber warning: `#ffb84d`
- Red danger: `#ff4d6d`

## Typography

- Interface: `Inter, Arial, sans-serif`
- Code/terminal: `JetBrains Mono, Menlo, Consolas, monospace`

## Motion Rules

- Cursor movements must land on meaningful UI targets.
- Terminal lines should stream in response to narration beats.
- Token values should change visibly, not sit as static labels.
- Prefer panel swaps, file tree expansion, command palette search, and data-flow movement over decorative circles.

## What NOT To Do

- Do not use generic slide cards.
- Do not rely on static images with light sweeps as the main action.
- Do not use tiny unreadable text as the primary message.
- Do not animate circles unless they point to a specific UI target.
