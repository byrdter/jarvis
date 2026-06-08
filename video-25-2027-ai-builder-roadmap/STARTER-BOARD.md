# Video 25 Starter Board: The 2027 AI Builder Roadmap

## Working Thesis

By 2027, the useful builders will not be the people who only know how to prompt a chatbot. They will understand the operating stack around models: tools, memory, workflows, evals, observability, deployment, and judgment about which model or agent should do which job.

This should be framed as **preparation**, not prediction. The video is not "what will happen in 2027." It is "what we should learn now so we are ready for 2027."

## Target Shape

- Channel: Byrddynasty
- Format: faceless, HeyGen clean VO only
- Runtime: 10-12 minutes
- Visual system: HyperFrames final composition, with real web-rolls, product screenshots, Codex Site surfaces, pixel B-roll, and kinetic roadmap graphics
- Tone: practical, builder-focused, not hype-heavy
- Voice: first-person plural where personal channel voice is needed: we, our, us

## Existing Product Assets Found

These are already present under `asset-library/products` and can be used immediately as first-pass visual material.

### OpenAI

- `asset-library/products/openai/surfaces/web/hero.png`
- `asset-library/products/openai/surfaces/web/hero-full.png`
- `asset-library/products/openai/surfaces/web/platform.png`
- `asset-library/products/openai/surfaces/web/pricing.png`
- `asset-library/products/openai/surfaces/web/scroll-homepage.webm`
- `asset-library/products/openai/surfaces/web/page@8d0497ce1713d7a147221f460b487bed.webm`

Best use: model/platform layer, developer platform proof, roadmap section on APIs and model selection.

### ChatGPT

- `asset-library/products/chatgpt/surfaces/web/hero.png`
- `asset-library/products/chatgpt/surfaces/web/hero-full.png`
- `asset-library/products/chatgpt/surfaces/web/login-landing.png`
- `asset-library/products/chatgpt/surfaces/web/scroll-homepage.webm`
- `asset-library/products/chatgpt/surfaces/web/page@86a712abefe2275af8e32b39ee9c11d9.webm`

Best use: "chatbot baseline" before the roadmap moves into agent systems.

### Claude Code

- `asset-library/products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png`
- `asset-library/products/claude-code/surfaces/web/hero.png`
- `asset-library/products/claude-code/surfaces/web/hero-full.png`
- `asset-library/products/claude-code/surfaces/web/docs-landing.png`
- `asset-library/products/claude-code/surfaces/web/scroll-homepage.webm`
- `asset-library/products/claude-code/surfaces/web/page@718c8440e8b6f69eef42c23096065c1e.webm`
- `asset-library/products/claude-code/surfaces/web/page@bc12f5abaac1d076acd1d242de0c621d.webm`

Best use: agentic coding, long-running work, desktop agent workflow, skills/hooks/workflows bridge.

### Codex

- `asset-library/products/codex/desktop/CodexDesktop.png`

Best use: coding agent comparison, multi-agent production, local thread/workspace visual.

### Gemini

- `asset-library/products/gemini/surfaces/web/hero.png`
- `asset-library/products/gemini/surfaces/web/hero-full.png`
- `asset-library/products/gemini/surfaces/web/app-landing.png`
- `asset-library/products/gemini/surfaces/web/scroll-homepage.webm`
- `asset-library/products/gemini/surfaces/web/page@f7ed66a3b2212a1172985fce78330c3e.webm`

Best use: multimodal/research/large-context lane and model choice segment.

### Antigravity

- `asset-library/products/antigravity/surfaces/web/hero.png`
- `asset-library/products/antigravity/surfaces/web/hero-full.png`
- `asset-library/products/antigravity/surfaces/web/labs-fallback.png`
- `asset-library/products/antigravity/surfaces/web/scroll-homepage.webm`
- `asset-library/products/antigravity/surfaces/web/page@1625e4af79645428b77797122ae6c418.webm`

Best use: agentic development environment visual, "IDE becoming agent cockpit" section.

## Visual Arc Draft

### 1. Cold Open: 2027 Is Not About Better Chat

Visual register: quick-cut montage.

Use ChatGPT hero as the baseline, then cut rapidly into Claude Code desktop, Codex desktop, GitHub-like code review, terminal logs, and a roadmap timeline. The point: chat is the entry point, not the destination.

Needs:

- Existing ChatGPT/OpenAI/Claude/Codex assets.
- Additional GitHub PR/action web-roll.
- Terminal clip or HyperFrames terminal simulation.

### 2. Layer 1: Model Judgment

Visual register: model picker / dashboard.

Show models as choices in a decision surface, not as mascots. The viewer should understand that 2027-ready builders choose by task: cheap/fast, deep reasoning, long context, multimodal, local/private, or coding-specialized.

Needs:

- OpenAI, Claude Code, Gemini, Codex, Antigravity assets.
- Codex Site or HyperFrames "model decision dashboard."

### 3. Layer 2: Tools And APIs

Visual register: docs/web-roll plus self-drawing diagram.

Show official docs and API surfaces, then transform them into tool calls in an agent flow.

Needs:

- OpenAI docs/platform web-roll.
- Anthropic docs web-roll.
- Google AI docs web-roll.
- MCP/tool registry visual.

### 4. Layer 3: Memory And Knowledge

Visual register: JARVIS knowledge database / second brain.

This is where the video can become uniquely Byrddynasty. Show that a serious builder needs reusable memory, searchable sources, and evidence-backed notes.

Needs:

- Codex Site for JARVIS knowledge search.
- Optional Obsidian graph.
- Existing `agent-sdk/data/ai-knowledge.db` can drive a local surface.

### 5. Layer 4: Workflows, Hooks, And Skills

Visual register: workflow control panel.

Show the difference between asking an AI once and giving it a repeatable operating procedure.

Needs:

- Local skill folder safe screenshots.
- Hook timeline simulation.
- Workflow template gallery Site.

### 6. Layer 5: Evals And Observability

Visual register: flight recorder / trace dashboard.

Show why 2027 agents need traces, screenshots, logs, eval cases, and failure review.

Needs:

- Arize / LangSmith / W&B pages.
- GitHub Actions logs.
- Synthetic JARVIS trace dashboard.

### 7. Layer 6: Deployment And Real Systems

Visual register: infrastructure web-rolls.

Show that a builder needs to know how agent work leaves the demo: endpoints, queues, jobs, webhooks, schedulers, and monitoring.

Needs:

- RunPod or Modal web-roll.
- Vercel / Cloudflare / Supabase docs.
- GitHub Actions/deployment visual.

### 8. Roadmap: What To Learn In Order

Visual register: interactive skill tree.

Turn the video into a practical learning sequence:

1. Prompting and judgment
2. Git and terminal basics
3. APIs and CLI tools
4. MCP/tool calling
5. Memory and retrieval
6. Workflows and skills
7. Evals and observability
8. Deployment
9. Product taste and visual communication

Needs:

- Codex Site "2027 Builder Roadmap."
- HyperFrames final roadmap animation.

### 9. Close: Build The Stack, Not Just The Prompt

Visual register: recap montage plus CTA.

Bring back the layers as a completed system and end with a kinetic subscribe/like/bell CTA, not a static card.

Needs:

- Recap callbacks from earlier scenes.
- CTA pattern adapted from the newer no-avatar Video 14 direction.

## Capture Gaps To Fill Next

### Public Captures I Can Do

- GitHub repo README slow scroll.
- GitHub PR diff / review web-roll.
- GitHub Actions run web-roll.
- Hugging Face model card web-roll.
- Hugging Face Space demo web-roll.
- OpenAI docs/model page web-roll.
- Anthropic docs/Claude Code page web-roll.
- Google AI docs/Gemini page web-roll.
- LangChain/LangGraph docs web-roll.
- Arize or LangSmith observability page web-roll.
- RunPod or Modal deployment page web-roll.
- Vercel / Cloudflare / Supabase docs web-rolls.

### Local Or Private Captures Terry Should Decide

- Whether to show real JARVIS knowledge database screens.
- Whether to show real Obsidian graph/screens.
- Whether to show real JARVIS code or use sanitized mock code.
- Whether to show actual Codex/Claude Code project screens beyond the current saved desktop screenshots.

### Sites I Can Build

- 2027 Builder Roadmap skill tree.
- Model decision dashboard.
- Agent stack layer map.
- Knowledge database search/explorer.
- Workflow/skills control panel.
- Agent observability flight recorder.

## Tomorrow Decisions For Terry

1. Should Video 25 be a **pillar video** for the channel, or a regular episode?
2. Audience level: non-coders, builders, business owners, or technical founders?
3. JARVIS screens: real, sanitized, or mock-only?
4. 2027 framing: roadmap, preparation, or prediction?
5. Which style target from the PDF feels right for this one:
   - cinematic WebGL / layered depth
   - editorial evidence gallery
   - dark technical product reveal
   - kinetic type/specimen
   - infinite canvas roadmap

## Recommended Next Step

Build the public capture pack first, then design the roadmap Site. That gives us enough real artifacts to make the video feel grounded before writing final VO.
