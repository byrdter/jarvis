# Video 25 Real Capture Prompts

Use this as the capture kit for optional real local assets. The first Video 25 mock already works without these, so only capture the screens that add credibility and feel safe to show.

## Global Capture Rules

- Target resolution: 1920x1080 if possible.
- Keep browser/app zoom between 90% and 110%.
- Use dark mode where possible.
- Hide sidebars that reveal private folders, client names, account names, API keys, billing, email, or local paths.
- Record 8-15 seconds for web-roll or app-roll clips.
- Scroll slowly. One smooth scroll is better than many jumps.
- If a screen contains private names but is visually useful, capture it anyway only after masking or cropping.
- Put final captures in `video-25-2027-ai-builder-roadmap/real-captures/`.

Recommended review filenames:

- `obsidian/obsidian-graph-safe.png`
- `obsidian/obsidian-note-scroll-safe.webm`
- `agent-workspace/codex-safe-workspace.png`
- `agent-workspace/claude-code-safe-workspace.png`
- `terminal/jarvis-safe-command.webm`
- `terminal/jarvis-safe-command.png`
- `jarvis-dashboard/jarvis-dashboard-masked.png`
- `jarvis-dashboard/jarvis-dashboard-masked.webm`
- `knowledge-search/knowledge-search-safe.webm`
- `knowledge-search/knowledge-search-results-safe.png`

## 1. Obsidian Graph Or Note Scroll

### Purpose

Show that JARVIS is connected to a real thinking system, not just a generic dashboard. This should feel like a personal knowledge map without exposing private details.

### Best Visual

A graph view or note scroll where the labels are hidden, blurred, too small to read, or safely generic. The visual value is the density and connectedness, not the text.

### Setup

1. Open Obsidian.
2. Switch to dark mode.
3. Open graph view or a non-sensitive note.
4. Hide left/right sidebars if they show private folders.
5. If graph labels show private names, turn labels off or zoom out until labels are not readable.

### Prompt To Use With An Assistant

```text
Help me prepare an Obsidian screen for a YouTube B-roll capture about a personal AI knowledge system. I need the screen to look like a connected knowledge graph or research note, but it must not reveal private names, client names, account details, file paths, or sensitive note contents. Tell me what panes to hide, what labels to turn off, and how to frame the window for a clean 1920x1080 screenshot or 10-second slow scroll.
```

### Capture Shot

- Screenshot: graph view with labels hidden, centered cluster, no private sidebars.
- Optional web-roll: slow pan/zoom across the graph or slow scroll through a sanitized note.

### Use In Video

Layer 3: Memory and Knowledge. It can replace or sit behind the synthetic JARVIS memory screen.

### Privacy Check

- No readable private names.
- No raw note titles that reveal projects, people, clients, or finances.
- No local folder path.
- No account/email visible.

## 2. Safe Codex Or Claude Code Workspace

### Purpose

Show a real agent workspace so viewers understand that the episode is based on actual builder workflows.

### Best Visual

Codex or Claude Code open on a harmless project, ideally with a visible task thread, file tree, and terminal/log panel. The screen should imply "AI agent doing structured work" without showing secrets.

### Setup

1. Open Codex or Claude Code.
2. Use a safe repo or folder.
3. Close `.env`, credentials, private notes, and unrelated tabs.
4. Show a non-sensitive file such as a README, mock plan, design doc, public script, or sanitized HTML.
5. Hide the full file tree if folder names are sensitive.

### Prompt To Use With Codex Or Claude Code

```text
Prepare this workspace for a public YouTube screenshot about how AI builders work with coding agents. Use only non-sensitive files. Show a clear task, a harmless project file, and a terminal or status panel if available. Do not reveal API keys, .env files, private project names, client names, personal folders, or account details. If anything risky is visible, tell me exactly what to hide before I take the screenshot.
```

### Suggested On-Screen Task Text

```text
Build a sanitized visual roadmap for the 2027 AI builder stack using public captures, mock JARVIS surfaces, and a validator-first video workflow.
```

### Capture Shot

- Screenshot: workspace with task thread and safe file open.
- Optional clip: 8-12 seconds showing a response or file diff, no typing required.

### Use In Video

Cold open, workflows section, or "workflows beat one-off prompts."

### Privacy Check

- No `.env`.
- No API keys.
- No private repo names unless intended.
- No customer/client names.
- No account email, tokens, billing, or local private folder tree.

## 3. Terminal Run Of A Harmless JARVIS Command

### Purpose

Give the video a real builder texture: a command runs, returns useful status, and reinforces that JARVIS is an operating system around the work.

### Best Visual

A clean terminal with a harmless command showing database counts, project status, capture inventory, or validator status.

### Safe Commands To Try

Run from the repo root:

```bash
pwd
sqlite3 agent-sdk/data/ai-knowledge.db "select 'sources', count(*) from content_sources union all select 'segments', count(*) from segments union all select 'topics', count(*) from topics union all select 'channels', count(*) from channels;"
python3 tools/scene-validator.py --help
find video-25-2027-ai-builder-roadmap/real-captures -maxdepth 2 -type f | sort
```

If you want the terminal to read more like JARVIS without exposing internals, use this safer staged sequence:

```bash
echo "JARVIS knowledge status"
sqlite3 agent-sdk/data/ai-knowledge.db "select 'sources', count(*) from content_sources union all select 'segments', count(*) from segments union all select 'topics', count(*) from topics union all select 'channels', count(*) from channels;"
echo "Video 25 capture kit ready"
```

### Prompt To Use With An Assistant

```text
Give me a harmless terminal sequence for a public YouTube screen recording about my JARVIS knowledge system. It should show useful status, such as source/segment/topic counts or validator help, but it must not print secrets, environment variables, private folder trees, account names, API keys, or client data.
```

### Capture Shot

- Screenshot after the command finishes.
- Optional clip: 8-10 seconds from command entry to results.

### Use In Video

Memory section, workflows section, or cold open montage.

### Privacy Check

- Terminal prompt does not show a sensitive local path.
- Command output does not include file paths beyond safe project-relative paths.
- No environment variables.
- No tokens or API responses.

## 4. Local JARVIS Dashboard With Private Data Masked

### Purpose

Show the most credible local proof: JARVIS as a real dashboard or command center. This is optional because it has the highest privacy risk.

### Best Visual

A dashboard with high-level stats, generic cards, source counts, topics, recent workflow status, and no readable private source titles.

### Setup

1. Open the local JARVIS dashboard if it is running.
2. Navigate to a safe overview page.
3. Mask or crop private source titles, private channels, account names, and local file paths.
4. Prefer aggregate numbers and generic labels over raw entries.

### Prompt To Use With Codex Or Claude Code

```text
Review this local JARVIS dashboard for public YouTube capture safety. I want to show high-level stats and the idea of a personal AI command center, but I do not want to reveal private source titles, client names, account names, local paths, API keys, or personal notes. Identify exactly what should be hidden, cropped, masked, or replaced with generic labels before I take a screenshot or short screen recording.
```

### Safe On-Screen Labels

- Knowledge Sources
- Segments Indexed
- Active Topics
- Research Channels
- Capture Queue
- Video Pipeline
- Validator Status
- Workflow Runs

### Capture Shot

- Screenshot: masked dashboard overview.
- Optional clip: 8-15 second slow movement across the dashboard.

### Use In Video

Layer 3: Memory and Knowledge, or Layer 4: Workflows.

### Privacy Check

- No private source titles.
- No raw transcript content.
- No URLs that should stay private.
- No names, folders, `.env`, tokens, email, billing, or account menus.

## 5. Clean Knowledge Database Search UI

### Purpose

This is the strongest real replacement for the synthetic JARVIS memory mock. It directly shows search, retrieval, topics, and evidence-backed segments.

### Best Visual

A search query such as "2027 builder roadmap" returning sanitized/generic results. The UI should show real structure and counts, but result titles should be safe.

### Setup

1. Open the JARVIS knowledge search UI.
2. Use a query that maps to the episode without exposing private work.
3. Use safe terms:
   - `AI builder roadmap`
   - `agent workflows`
   - `memory and retrieval`
   - `evals observability deployment`
4. Crop or mask result titles if needed.
5. Keep the search box, stats, and result cards visible.

### Prompt To Use With Codex Or Claude Code

```text
Help me create a public-safe knowledge database search screen for a YouTube video about the 2027 AI builder roadmap. Use a harmless query like "AI builder roadmap", "agent workflows", or "memory and retrieval". The screen should show search, topics, source/segment counts, and result cards, but it must not reveal private source titles, personal notes, client names, account names, hidden URLs, API keys, or raw transcript text that should stay private. Tell me what to mask and what query/result view will look best on camera.
```

### Capture Shot

- Screenshot: search box plus results.
- Clip: 10-15 seconds showing query entry, results appearing, and a slow scroll through result cards.

### Use In Video

Main replacement candidate for the current synthetic JARVIS scene.

### Privacy Check

- Result titles are safe.
- Snippets do not expose private transcripts or sensitive claims.
- URLs and channel names are safe or hidden.
- No account controls or local paths visible.

## Priority Order

If time is limited, capture these first:

1. Knowledge database search UI
2. Safe Codex or Claude Code workspace
3. Terminal JARVIS command
4. Obsidian graph
5. Local JARVIS dashboard

The local JARVIS dashboard is most credible but also highest risk. The knowledge search UI gives the best balance of credibility, relevance, and controllability.

## Quick Delivery Checklist

When you drop captures into `real-captures`, include:

- one screenshot or short clip per selected category
- a note if anything is intentionally masked
- whether the asset is approved for YouTube use
- whether it can be used full-screen or only as a blurred/depth background
