# Video 12 Full HyperFrames Design

## Style Prompt

Build a high-contrast developer operations video that feels like a premium VS Code demo, not a slide deck. The screen should look active: editor tabs, file tree, terminal output, command palette, cursor motion, token meters, code panels, and source-proof windows should react to the voiceover. Use dark technical surfaces with cyan, amber, green, and red status colors.

## Colors

- Canvas: `#06090f`
- Panel: `#0d1320`
- Panel elevated: `#111b2d`
- Border: `#24324d`
- Text primary: `#f7fbff`
- Text muted: `#b7c7dc`
- Cyan action: `#3ee7ff`
- Green success: `#46f39a`
- Amber warning: `#ffb84d`
- Red danger: `#ff4d6d`

## Typography

- Interface: `Inter, Arial, sans-serif`
- Code/terminal: `JetBrains Mono, Consolas, monospace`

## Motion Rules

- Cursor movements must land on meaningful UI targets.
- Terminal lines should stream in response to narration beats.
- Token values should change visibly, not sit as static labels.
- Prefer panel swaps, file tree expansion, command palette search, data-flow movement, and row highlights over decorative circles.

## Local Media

- Render-safe HeyGen source lives locally at `assets/heygen-source-keyframed.mp4`.
- It is generated from `../10-videos/heygen-source.mp4` with a 30 fps/keyframed H.264 pass so browser rendering can seek reliably.
- Draft output: `renders/video-12-hyperframes-full-draft.mp4`.
- QA contact sheet: `qa-frames/contact-sheet.png`.

## What NOT To Do

- Do not use generic slide cards as the default visual.
- Do not rely on static images with light sweeps as the main action.
- Do not use tiny unreadable text as the primary message.
- Do not animate circles unless they point to a specific UI target.
