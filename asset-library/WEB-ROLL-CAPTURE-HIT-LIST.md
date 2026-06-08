# Web-Roll Capture Hit List

This is the reusable capture backlog for Byrddynasty, KeyAdvances, and related faceless videos. It is designed to feed `asset-library/capture-runner.js`, Codex Sites, and HyperFrames scenes.

## Capture Standards

Use these defaults unless a scene needs something different:

- Viewport: `1440x900` for desktop web-rolls, `1080x1350` for vertical crops, `390x844` for phone frames.
- Web-roll length: 6-12 seconds for reusable B-roll, 12-20 seconds for evidence walkthroughs.
- Scroll speed: slow enough that a title, code block, or model card section can be read for 1-2 seconds.
- Framing: crop or zoom in HyperFrames; do not show tiny full-page UI when the point is a single section.
- Secrets: never capture logged-in billing, keys, private dashboards, personal email, or account settings.
- Storage: `asset-library/products/<product>/surfaces/web/<name>.webm` for reusable product rolls; `keyadvances-assets/screenshots/<product>/` for KeyAdvances-specific proof; scene-local copies for final production.

## Priority Bands

P0 means capture first because the asset will be reused across many AI-agent videos. P1 is useful for recurring topics. P2 is topic-specific or nice-to-have.

## P0 Foundation Captures

| ID | Product / Source | Capture | Type | Duration | Best Use |
|---|---|---|---|---:|---|
| WR-GH-001 | GitHub | Public repo README slow scroll | web-roll | 10s | Any open-source tool, framework, or agent repo proof |
| WR-GH-002 | GitHub | Pull request diff with file tree and changed lines | screenshot + web-roll | 8s | Coding agents, refactors, review loops |
| WR-GH-003 | GitHub | Issues list filtered by labels | screenshot | n/a | Agent task tracking, bug triage |
| WR-GH-004 | GitHub | Actions workflow run page | web-roll | 8s | CI, evals, automation, shipping proof |
| WR-HF-001 | Hugging Face | Model card top and usage section | web-roll | 12s | Local models, small models, benchmarks |
| WR-HF-002 | Hugging Face | Spaces demo page | web-roll | 10s | Interactive AI demos, prototype proof |
| WR-HF-003 | Hugging Face | Datasets page with viewer | screenshot + web-roll | 10s | Data, evals, training, RAG |
| WR-HF-004 | Hugging Face | Blog article scroll with code/images | web-roll | 12s | AI news and research context |
| WR-OAI-001 | OpenAI Docs | API docs landing / model docs | screenshot + web-roll | 10s | OpenAI model/tool claims |
| WR-OAI-002 | OpenAI Platform | Playground or dashboard-style public surface | screenshot | n/a | Model testing, developer workflow |
| WR-OAI-003 | OpenAI News | Announcement article slow scroll | web-roll | 12s | Source proof for current OpenAI updates |
| WR-ANT-001 | Anthropic Docs | Claude Code or API docs page | web-roll | 10s | Claude Code, MCP, agentic coding |
| WR-ANT-002 | Anthropic News | Research/news article slow scroll | web-roll | 12s | Safety, policy, research proof |
| WR-GAI-001 | Google AI | Gemini docs / AI Studio docs | web-roll | 10s | Gemini model and tooling claims |
| WR-VSC-001 | VS Code Mock / Real | Code editor with agent-related TypeScript/Python | generated Site or local capture | 8s | MCP, agent harness, router code, skills |
| WR-TERM-001 | Terminal | Command run with streaming output | local capture | 8s | CLI tools, automation, install flows |
| WR-OBS-001 | Obsidian | Graph view or knowledge note scroll | manual/local capture | 10s | Second brain and memory videos |
| WR-JAR-001 | JARVIS | Command center dashboard walkthrough | Codex Site capture | 12s | Channel identity, proof of real system |

## Agentic Coding And Developer Workflow

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-DEV-001 | GitHub | README install instructions with terminal command | web-roll | 8s | Setup proof |
| WR-DEV-002 | GitHub | `package.json`, `pyproject.toml`, or repo file browser | screenshot | n/a | Codebase structure |
| WR-DEV-003 | GitHub | PR review comments and checks area | web-roll | 10s | Agent reviewer / QA loop |
| WR-DEV-004 | GitHub | Releases page with changelog | web-roll | 8s | Product/version update proof |
| WR-DEV-005 | Docker Docs | MCP / container / compose docs scroll | web-roll | 10s | Tool installation and infra |
| WR-DEV-006 | Vercel Docs | Deployment or AI SDK docs scroll | web-roll | 10s | Shipping apps with agents |
| WR-DEV-007 | Supabase Docs | Auth/database/vector docs scroll | web-roll | 10s | Agent memory and app backend |
| WR-DEV-008 | Cloudflare Docs | Workers / AI / browser rendering docs | web-roll | 10s | Edge AI and deployment |
| WR-DEV-009 | npm | Package page scroll for key AI package | web-roll | 8s | Library credibility |
| WR-DEV-010 | PyPI | Package page scroll for Python AI package | web-roll | 8s | Python ecosystem proof |

## AI Agent Infrastructure

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-INF-001 | LangChain | LangSmith or agents docs page | web-roll | 12s | Agent tracing, deployment, frameworks |
| WR-INF-002 | LangGraph | Graph / workflow docs page | web-roll | 12s | Agent orchestration |
| WR-INF-003 | Arize | Observability/evals product page | web-roll | 10s | Tracing and evals |
| WR-INF-004 | Weights & Biases | Weave/evals docs page | web-roll | 10s | Experiment tracking |
| WR-INF-005 | RunPod | Serverless endpoint or GPU product page | web-roll | 10s | Model deployment |
| WR-INF-006 | Modal | Serverless AI compute docs | web-roll | 10s | AI infra |
| WR-INF-007 | Firecrawl / Crawl4AI | Docs page slow scroll | web-roll | 10s | Data extraction and web ingestion |
| WR-INF-008 | Browserbase / Stagehand | Browser agent docs | web-roll | 10s | Browser automation |
| WR-INF-009 | Smithery / MCP registry | MCP server listing | web-roll | 10s | MCP ecosystem |
| WR-INF-010 | Stripe Docs | Agent payments / API docs surface | web-roll | 10s | Autonomous economy, payment infra |

## Model And Research Proof

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-RES-001 | arXiv | Abstract page with title/authors | screenshot + web-roll | 8s | Research credibility |
| WR-RES-002 | Papers with Code | Benchmark table or task leaderboard | web-roll | 10s | Performance comparisons |
| WR-RES-003 | Hugging Face Leaderboards | Leaderboard scroll | web-roll | 12s | Model ranking proof |
| WR-RES-004 | AI Engineering / conference page | talk listing or transcript page | web-roll | 10s | Expert evidence |
| WR-RES-005 | Latent Space | Article/podcast page scroll | web-roll | 12s | Industry interpretation |
| WR-RES-006 | OpenAI Research | Research article scroll | web-roll | 12s | Frontier research proof |
| WR-RES-007 | Anthropic Research | Research article scroll | web-roll | 12s | Safety and interpretability proof |
| WR-RES-008 | Google Research Blog | AI research article scroll | web-roll | 12s | Gemini/Google proof |
| WR-RES-009 | Hugging Face Blog | Technical article scroll | web-roll | 12s | Open ecosystem proof |
| WR-RES-010 | Reddit LocalLLaMA / ML | Thread title and top comments, sanitized | screenshot | n/a | Community sentiment, never primary proof |

## Knowledge, Memory, And Second Brain

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-MEM-001 | JARVIS Knowledge DB Site | Search query returning sources and segments | Codex Site web-roll | 12s | Proof of the new knowledge database |
| WR-MEM-002 | JARVIS Knowledge DB Site | Topic cluster map: memory, MCP, CLI, skills | Codex Site web-roll | 12s | Show database structure |
| WR-MEM-003 | Obsidian | Graph view zoom / pan | manual web-roll | 10s | Second brain metaphor with real artifact |
| WR-MEM-004 | Obsidian | Note with source links and highlights | manual web-roll | 8s | Knowledge capture |
| WR-MEM-005 | SQLite Browser / Site | Sources table filtered by topic | Codex Site web-roll | 10s | Grounded research workflow |
| WR-MEM-006 | Vector Search Site | Query -> ranked results -> selected source | Codex Site web-roll | 12s | Retrieval explained visually |
| WR-MEM-007 | Transcript Intelligence Board | YouTube transcript segments and timestamps | Codex Site web-roll | 12s | Video research pipeline |
| WR-MEM-008 | Claim Source Map | Claim cards linked to source cards | Codex Site web-roll | 10s | Evidence-backed scripting |
| WR-MEM-009 | Memory Timeline | Session memories over time | Codex Site web-roll | 10s | Persistent AI memory |
| WR-MEM-010 | Workflow Handoff Board | Scene status + blockers + assets | Codex Site web-roll | 10s | Production operations |

## Byrddynasty Visual Identity Captures

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-BYR-001 | JARVIS Router Site | Three-brain router choosing model by task | Codex Site web-roll | 12s | Video 14 and agent router series |
| WR-BYR-002 | Model Picker Site | Wrong model repeatedly selected for simple tasks | Codex Site web-roll | 8s | Tradeoff/cost story |
| WR-BYR-003 | Token Burn Site | Token meter rising by task type | Codex Site web-roll | 8s | Cost/context visual |
| WR-BYR-004 | Agent Stack Map Site | Foundation model -> tools -> memory -> workflow | Codex Site web-roll | 12s | Agent stack explainer |
| WR-BYR-005 | MCP Handshake Site | initialize -> capabilities -> tools/list -> registry | Codex Site web-roll | 12s | MCP explainer |
| WR-BYR-006 | CLI vs MCP Site | Same task through CLI vs MCP lanes | Codex Site web-roll | 10s | Tool choice explainer |
| WR-BYR-007 | Subagent Board Site | Research, code, QA agents passing handoffs | Codex Site web-roll | 12s | Multi-agent workflows |
| WR-BYR-008 | Evals Dashboard Site | Failing cases, traces, regressions | Codex Site web-roll | 10s | Evals and reliability |
| WR-BYR-009 | Agent Harness Site | checkpoints, memory, validation, handoff | Codex Site web-roll | 12s | Harness concept |
| WR-BYR-010 | Production Command Center Site | Episode brief, assets, scene status | Codex Site web-roll | 10s | Channel meta and proof |

## KeyAdvances Captures

| ID | Source | Capture | Type | Duration | Visual Role |
|---|---|---|---|---:|---|
| WR-KEY-001 | OpenAI News | Announcement article slow scroll | web-roll | 12s | AI news proof |
| WR-KEY-002 | Anthropic News | Announcement article slow scroll | web-roll | 12s | AI news proof |
| WR-KEY-003 | Google AI Blog | Announcement article slow scroll | web-roll | 12s | AI news proof |
| WR-KEY-004 | Hugging Face Blog | Release/article slow scroll | web-roll | 12s | Open-source AI proof |
| WR-KEY-005 | GitHub Trending / Repo | repo stars, README, releases | web-roll | 10s | Tool launch proof |
| WR-KEY-006 | Product Homepages | landing hero + feature block | web-roll | 8s | New product visual |
| WR-KEY-007 | Research Paper | arXiv abstract + figure crop | screenshot + web-roll | 8s | Research news |
| WR-KEY-008 | Social Proof | HN/Reddit thread sanitized | screenshot | n/a | Community reaction |
| WR-KEY-009 | Vendor Docs | feature docs section | web-roll | 10s | Feature validation |
| WR-KEY-010 | Comparison Site | side-by-side release board | Codex Site web-roll | 12s | Weekly digest structure |

## Award-Site-Inspired Visual Patterns

Use the `Top_50_Visual_Presentation_Websites.pdf` as inspiration for these reusable treatments. Do not copy site layouts or assets directly.

| Pattern | Inspired By | How To Use In Videos |
|---|---|---|
| Scroll chapter reveal | Lusion, Immersive Garden, Cartier, Prometheus Fuels | Turn each script section into a scroll-driven chapter with foreground proof and background depth |
| Infinite canvas | Oatly, KPRverse | Map an AI ecosystem as a wide pan across tools, models, sources, and workflows |
| Product disassembly | Longines, Daylight Computer | Break an agent workflow into layers: model, context, tools, memory, evals |
| Editorial evidence gallery | Getty, Dropbox Brand, Follow.Art | Show screenshots, source excerpts, and claim cards in a gallery wall |
| Kinetic type specimen | Bezier, Motion.ed | Use typography as the visual for definitions, mistakes, and decision rules |
| Dark technical product reveal | Moxion, Composites.archi, Cowboy | Use for infrastructure-heavy topics: GPUs, edge deploys, pipelines |
| Documentary archive timeline | Gehry/Getty, Voices of Alice | Use for historical segments or "how we got here" sections |
| Audio-reactive data form | Noomo Beat | Use lightly for music beds, token bursts, model activity, or live traces |
| 3D playground / world map | Bruno Simon, Nomadic Tribe | Use as a metaphor for navigating the AI tool ecosystem |
| Brand-guideline gallery | Dropbox Brand | Use for channel asset browsing, reusable component libraries, and visual identity explainers |

## First Capture Sprint

Start with these because they unlock the most future videos:

1. GitHub README, PR diff, Actions run, Issues list.
2. Hugging Face model card, Space demo, dataset viewer, blog article.
3. OpenAI docs/news, Anthropic docs/news, Google AI docs/blog.
4. JARVIS Knowledge DB Site: search, topic map, source segments.
5. JARVIS Router Site: model picker, token burn, three-brain router.
6. MCP Handshake Site: four-step protocol animation.
7. VS Code and terminal local captures for agentic coding.
8. Obsidian graph and source note captures.

## Playbook Candidates

Create or extend these playbooks first:

- `asset-library/playbooks/github.js`
- `asset-library/playbooks/huggingface.js`
- `asset-library/playbooks/openai.js`
- `asset-library/playbooks/anthropic.js`
- `asset-library/playbooks/google-ai.js`
- `asset-library/playbooks/langchain.js`
- `asset-library/playbooks/runpod.js`
- `asset-library/playbooks/arize.js`
- `asset-library/playbooks/mcp-registry.js`

## Naming Examples

```text
products/github/surfaces/web/repo-readme-scroll.webm
products/github/surfaces/web/pr-diff-review.png
products/huggingface/surfaces/web/model-card-scroll.webm
products/openai/surfaces/web/docs-models-scroll.webm
products/anthropic/surfaces/web/claude-code-docs-scroll.webm
products/jarvis-sites/surfaces/web/router-simulator-scroll.webm
products/jarvis-sites/surfaces/web/knowledge-search-query.webm
```

## How Captures Become Video

1. Capture the page or Site as screenshot/web-roll.
2. Add or update manifest metadata with source URL, capture date, tags, and best use.
3. Copy the asset into the scene-local `assets/` folder.
4. In HyperFrames, crop/zoom/frame the capture, add cursor or callout motion, and sync it to VO.
5. Avoid using raw full-page captures without motion, zoom, or annotation.
