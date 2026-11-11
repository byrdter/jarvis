# Brain Studio: what Zubair built, and how we build ours (studied 2026-11-11)

> The visual layer of JARVIS: the brain repo rendered as a living 2D/3D graph.
> **Sources:** (1) video "The Next Era of Second Brains Is Here" (youtube.com/watch?v=xHAZo1SmnhM,
> 2026-06-15), studied frame by frame; 18 full-res frames + 24 contact sheets in
> `~/Dropbox/AITerryByrd/brain-studio-frames/` (`tNNN.jpg` = second NNN of the video).
> (2) **The free version's source code**: `github.com/zubair-trabzada/brain-map`, **public, MIT
> license**, last commit 2026-06-12 (`build.py` 250 lines + `index.html` 246 lines). The paid "Brain
> Studio" (2D + 3D, white-label) is in his paid community and Terry's free-community level can't open
> the course, so everything about the paid version below comes from the video frames.
> MIT means we may reuse brain-map's code if we keep its copyright and license notice.

## 1. How his brain is organized (the part that makes the graph work)
The graph is only as good as the folder layout. `build.py` detects an "AI Workshop OS" vault (a
`CLAUDE.md` + a `wiki/` folder) and assigns each note a **type from its path**:

| Path | Type (legend name) | Color | Base radius | Count in his brain |
|---|---|---|---|---|
| `CLAUDE.md` | Router | `#34d399` green | 11 | 1 |
| `wiki/*` (other), `cadence/` | Wiki (core) | `#e7e5e4` white | 7 | 7 |
| `wiki/concepts/` | Concepts | `#fbbf24` gold | 7.5 | 17 |
| `wiki/skills/<suite>.md` (depth 2) | Suites | `#a78bfa` violet | 7 | 13 |
| `wiki/skills/<suite>/…` | Skills | `#60a5fa` blue | 3.2 | 197 |
| `wiki/tools/` | Tools | `#f472b6` pink | 5.5 | 18 |
| `wiki/worlds/` | Worlds (project sites) | `#fb923c` orange | 5.5 | 15 |
| `projects/`, `brainstorm/`, root files | Notes | `#34d399` | 5.5 | 4 |
| anything else linked | Files (external) | `#3e4c63` slate | 2.1 | 192 |

The paid version adds business types: **Clients 13, Videos 10, Community 5, SaaS 5, Sponsorships 5,
Affiliates 5, Decisions 5**. Totals on screen: **512 notes, 1,760 connections**. Top hubs: Skill
Suites 233, Local Businesses 129, Zubair OS 49, AI Workshop 48, YouTube Channel 45.
His underlying vault (seen in Obsidian at 0:32) is a Claude Code project: `wiki/`, `projects/`,
`skills-library/`, `scripts/`, one folder per demo site ("worlds"), plus root files such as
`CLAUDE`, `FRESH-SESSION-WALKTHROUGH`, `SKOOL-PROPOSAL-PAGE`.

### Note conventions (read off the inspector panels)
- **Router (CLAUDE.md):** *"You are Zubair Trabzada's AI operating system and second brain. Your job
  is to help him spend less time on operations and admin so he can focus on building Claude Code to…"*
  It links to every hub, so it sits at the center.
- **Concept note** = one-line "what it is" + pointers + a `Related:` line that creates the links.
  E.g. CiteVue: *"Live GEO audit SaaS at citevue.com… Free score → $19.99 Full Audit → $2,000 +
  $500/mo done-for-you. Stripe LIVE; code in geo-audit-app/ (read its HANDOFF.md first). Project 3 of
  the Build and Sell series… Related: GEO, Build and Sell series, Local Businesses. Docs: products."*
- **Client note** = one line with money and result, plus **child notes**: *Apex HVAC — "Dallas HVAC
  company — reputation engagement, $2,000 setup + $500/mo. 3.4 → 4.6 stars in 90 days"* → children
  `Apex — intake` ("20 trucks, 4 dispatchers. Pain: emergency-call reviews. Decision maker: Marcus
  (owner)"), `Apex — review audit`, `Apex — monthly report`.
- **Suite note** = what's in the bundle + the member list: *"16 Claude Code skills in the ads suite —
  sold via AI Workshop as part of Skill Suites… Skills: ads-orchestrator · ads-audit · …"*
- **Skill note** = which suite it belongs to + related skills.
- The pattern everywhere: **short summary first, explicit links last.** Links come from `[[wikilinks]]`
  and relative `.md` links; that's what the free builder parses.

## 2. The free version, exactly (from the code)
- **Build (`build.py`, stdlib only):** walk the vault (skip `.git`, `.obsidian`, `node_modules`, dot
  dirs) → type each `.md` by path (above) or, for a generic folder, one color group per top-level
  folder → links from `[[wikilink]]` (matched by filename stem, case-insensitive) and relative
  `](x.md)` links → in AIOS mode drop nodes with no links; in generic mode add a vault → folder →
  file tree so link-free folders still form a galaxy → write `graph-data.js`
  (`const GRAPH = {brand, groups, nodes:[{id,label,g,p}], links:[{s,t}]}`) + `index.html` + a
  `serve.py` on `127.0.0.1:4710`. `SKILL.md`/`README.md`/`index.md` take their folder's name as label.
- **Render (`index.html`, one file, d3 v7 from a CDN, HTML canvas):**
  - **Growth animation:** nodes are born one by one, sorted router-first then by group; each group has
    a `pace` (ms between nodes: router 0, wiki 480, concepts 230, suites 270, skills 16, tools 150,
    files 5) and a `pause` before the group starts. Each newborn appears next to an already-born
    neighbor. The camera auto-fits until the user touches it. **R** replays.
  - **Size** = group radius × (0.8 + √degree × 0.15), capped at 2.2×.
  - **Physics:** forceLink distance 30 / strength 0.5; charge −(15 + 6r), distanceMax 450; center
    0.05; collide r+3.5; weak x/y gravity 0.03; alphaDecay 0.012.
  - **Interaction:** hover lights a node and its neighbors (others fade to 12%); click pins that
    highlight (Esc clears); drag a node; drag empty space to pan; wheel zooms around the cursor; search
    + Enter flies to the first label match; labels show only for big nodes or the lit set.
  - Bottom bar: "N notes · M links", search, ⟲ Replay. Top-right legend. An upsell card bottom-left.

## 3. The paid Brain Studio (from the frames)
**Two pages:** `localhost:4710/index.html` (2D) and `/3d.html` (3D), "← back to 2D" link between them;
explainer pages on `:4712`.

**Left panel:** brand block ("AI WORKSHOP OS · 512 notes · 1760 connections") → **Search the brain** →
**Inspector** (empty state: "Click a node to focus it — only that node and its connections light up,
and you can read its note here. Shift-click a second node to trace the path.") → when a node is
selected: name, "Type · N connections", the note excerpt, **Read full note / Show less**, a **Depth
1 · 2 · 3** dial, then the neighbor list with each neighbor's degree → **Top hubs** (by degree) →
**Forces** sliders (Repel, Link length, Gravity) → **Display** toggles → **Theme**.

**Right panel:** **Filter** = every type with a colored dot and count; click to hide a type (he hides
the 192 Files to declutter).

**Display toggles (2D):** Labels (slider), Glow, Curved links, Particle flow, Cluster auras, Aurora
sky, Icons, Shapes, Star dust. **(3D):** Hub labels, Particle flow, Auto-rotate, Starfield.
**Theme:** 4 color schemes (green, violet, emerald, blue) + **By type / Heatmap** coloring.

**Bottom bar (2D):** "512 notes · 1760 links" · search · **▶ Tour** (guided camera tour) · a mode
button · **3D** · a circle button · **1× / 4×** (growth-animation speed) · two more · a camera
button. **Minimap** bottom-left. **(3D):** ◎ Fit, isolate, camera.

**Keyboard/mouse (footer):** *3D:* drag = orbit · scroll = zoom · click = focus · shift-click = path ·
I = isolate · Esc = clear. *2D:* scroll zoom · drag pan · grab nodes · click = focus · right-click =
menu (radial) · shift-click = path · I = isolate · Esc = clear.

**Other details:**
- Deep links: `index.html#n=CLAUDE`, `#n=Ads%20Suite`, `#n=Apex%20HVAC` (the URL focuses a node).
- 2D **icons per type**: brain (router), open book (wiki), lightbulb (concepts), graduation cap
  (AI Workshop), diamond (CiteVue), crossed tools (Skill Suites), folder (suites), pencil (scripts).
- Hover tooltip: name, "Type · N links — click to focus", first line of the note.
- "Isolated" badge in the inspector when isolate is on; pinned nodes stay lit.
- Growth animation shown in stages (17 → 237 → 496 → 512 notes).

**The demo that sells it (7:54–10:10):** a *fresh* Claude Code session (Opus 4.8, 1M context) answers
"Which industry should I target first for reputation management…?" correctly from the brain, and
offers to run the `reputation-audit` skill. Then he searches "reputation" in the 3D view and shows the
notes and the skill it used. The graph is the **proof** of where the answer came from.

**Explainer page ("What a Second Brain actually is"):** YOU (talk in plain English) ⇄ THE BRAIN (just
folders and markdown files: Knowledge, Clients, Products, Content, Decisions, Live data, tied together
by CLAUDE.md, "the router") ⇄ CLAUDE (your thinking partner; already knows who you are, every client and
product, your pricing and playbooks, what you decided last month). Three benefits: no more amnesia ·
it compounds · it outlasts the hype (swap the engine, keep the brain).

**Business page ("Turn this into a business"):** find a business (movers, HVAC, law firms, clinics,
contractors) → build their brain (logo, white-label) → get paid. **The Build $2,000+** (audit tools,
build brain + router, wire live data, install and train the team, white-label 3D graph, starter skills
and templates) + **The Retainer $500/mo** (keep the brain updated, new automations, new skills, monthly
report, priority support, upsell agents). Math: 1 client $2K + $500/mo; 5 → $10K + $2.5K/mo; 10 → $20K +
$5K/mo.

## 4. How we build ours
**Decision:** start from `brain-map` (MIT) instead of from scratch, and add the paid-tier features we
want ourselves. Keep his copyright line + license file in our copy.

| Step | What | Est. |
|---|---|---|
| 1 | Fork into the engine (`jarvis/apps/brain-studio/`); map **our** brain layout to types: `CLAUDE.md`/`SOUL`/`USER`/`MEMORY` = Router; `wiki/concepts` Concepts; `wiki/people` People; `wiki/projects` Projects; `wiki/apps` Apps; `wiki/tools` Tools; `wiki/models` Models; `lab/` Lab results; `daily/` Journal (dim, small); `raw/` Sources (Files style) | 1 h |
| 2 | **Note previews** (`preview_of` is a stub in the free version): first ~700 chars, plus Read full note | 0.5 h |
| 3 | Inspector panel: type, degree, excerpt, **depth 1/2/3**, neighbor list, Top hubs, type filter with counts, deep links `#n=` | 2 h |
| 4 | **Fly-to-source**: JARVIS answers return the note ids it used; the graph lights them (our existing plan) | 1 h |
| 5 | Path (shift-click, BFS shortest path), isolate (I), heatmap (color by **recency of edit**: what changed this week) | 1.5 h |
| 6 | 3D page with `3d-force-graph` (same `graph-data.js`), auto-rotate, starfield, fly-to | 2 h |
| 7 | JARVIS orb + engine badge; lab specialists as moons (PLAN §10.3) | 2 h |
| 8 | Install as a Claude Code skill (`/brain-map` → build + serve), and a nightly rebuild | 0.5 h |

**Writing rule for our brain (adopt now, it costs nothing):** every wiki page opens with a one-line
summary (what it is, numbers, status) and ends with a `Related:` line of `[[links]]`. Clients and
projects get child notes (`<name> — intake`, `— decisions`, `— monthly report`). The graph, search
and JARVIS's answers all get better from the same habit.

**For Terry's business plan:** the same build is a sellable "team brain" for local businesses at
$2,000 setup + $500/month (his numbers), and a demo for company visits.
