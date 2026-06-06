# Chat Panel

**STATUS:** proven
**Channel fit:** Byrddynasty, faceless-educational
**Tone fit:** educational, technical-demo

## Use case
IDE-style chat showing a user prompt and a streaming AI response. Perfect for "the agent thinks" or "the agent decides" beats where you need to show actual textual reasoning.

## Reference implementation
`${JARVIS_HOME}/agent-stack-deep-dive/02-modules/004-foundation-model/hyperframes/index.html` (`.chat-card`, `.chat-prompt`, `.chat-response`).

## Build notes
- Card uses the dark-card treatment (navy gradient + cyan border + glow halo).
- Width ~720px is the sweet spot — wider clips at the chat-card edge; narrower compresses the text awkwardly.
- Prompt row: right-aligned bubble with a soft cyan-tinted background.
- Response row: left-aligned bubble that fills in word-by-word via GSAP `staggerFrom` on `.word` spans.
- Position: right side of frame (`left: 880`), leaving the left pane for the editorial spread.

## Anti-patterns
- Don't place the chat card centered if there's a headline to its left — that's text-on-text territory.
- Don't let the response panel scroll. If it would scroll, the response is too long; trim it.
- Don't animate the prompt with a typewriter — that wastes time. Prompts appear; responses stream.

## Example beats
- Module 04 — Foundation Model: chat card showing "What's the weather in NYC?" → streamed weather response.
