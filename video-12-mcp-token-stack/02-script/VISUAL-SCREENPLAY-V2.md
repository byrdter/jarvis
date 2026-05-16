# Video 12 Visual Screenplay V2

Purpose: rebuild the video from a director's plan before any render work. Each segment gets its own visual reason to exist. The renderer must not stretch one generic scene across unrelated narration.

Timing source: `10-videos/heygen-source.mp4`, 1920x1080, 25 fps, 803.756 seconds.

Transcript source: fresh Whisper alignment from the HeyGen source. Segment 3 was manually inserted at 61.20s because automatic matching folded it into segment 2.

Avatar rule: use HeyGen full-frame source for the visible avatar sections, but crop/reposition it in HyperFrames/Remotion for side-avatar segments 6, 13, and 22. Do not cover the avatar face with large captions.

Still-image rule: `09-stills/NNN.png` files are optional concept art, not production instructions. For each segment, inspect the still if one exists, then decide whether it helps. It may be used as inspiration, loosely emulated, ignored, or replaced with a completely new visual if the still does not serve the narration. Do not force the video to follow the stills.

Layered-object rule: the final visual should be built as animated layers, not as a flat still with effects. Use separate text, counters, panels, rays, meters, highlights, cards, source windows, data objects, cursor/callout layers, and avatar layers, each with its own timing. The point is not to rebuild every still image. The point is to design the best layered scene for the idea being spoken in that segment.

Global layout rules:

- Use the whole 1920x1080 frame. Avoid small top-left panels floating in empty space.
- Minimum primary text size: 56px. Minimum secondary text size: 34px. Avoid dense paragraphs.
- Every segment gets one primary visual verb: build, collapse, compare, zoom, reveal, audit, measure, or decide.
- Every segment gets a fresh visual decision. Do not over-apply one technique across the whole video just because it worked once.
- Cursor appears only when it performs a real action: click, select, drag, open, underline, or confirm. No idle cursor.
- Captions are not subtitles. Use one large visual thesis line only when it strengthens the scene.
- Visual timing must follow the spoken timing below. If the voice moves to a new concept, the screen must move too.

## Segment Timing Map

| Seg | Start | End | Avatar | Core visual |
|---:|---:|---:|---|---|
| 1 | 0.00 | 35.04 | Full | Cold open talking head |
| 2 | 35.04 | 61.20 | None | Old MCP context flood |
| 3 | 61.20 | 85.98 | None | Tool Search before/after |
| 4 | 85.98 | 107.54 | None | Trap reset cards |
| 5 | 107.54 | 139.22 | None | Accuracy evidence board |
| 6 | 139.22 | 172.50 | Side | Layer thesis |
| 7 | 172.50 | 199.10 | None | Cloudflare Code Mode source |
| 8 | 199.10 | 222.13 | None | 1.17M to 1K number drop |
| 9 | 222.13 | 242.37 | None | Anthropic workflow source |
| 10 | 242.37 | 265.53 | None | Transcript data movement |
| 11 | 265.53 | 286.63 | None | 150K to 2K compression |
| 12 | 286.63 | 315.39 | None | MCP connector caveat |
| 13 | 315.39 | 345.23 | Side | Security warning |
| 14 | 345.23 | 373.33 | None | Scoped MCP groups |
| 15 | 373.33 | 394.63 | None | Skills as procedure |
| 16 | 394.63 | 417.06 | None | JARVIS video skill artifact |
| 17 | 417.06 | 442.50 | None | CLI benchmark |
| 18 | 442.50 | 470.96 | None | CLI versus MCP boundary |
| 19 | 470.96 | 496.50 | None | Output filtering |
| 20 | 496.50 | 520.82 | None | TOON caution |
| 21 | 520.82 | 550.32 | None | Full stack table |
| 22 | 550.32 | 577.18 | Side | Practical rule |
| 23 | 577.18 | 600.78 | None | JARVIS architecture map |
| 24 | 600.78 | 626.48 | None | Four-run measurement plan |
| 25 | 626.48 | 646.34 | None | Migration phase 1 |
| 26 | 646.34 | 669.88 | None | Migration phase 2 |
| 27 | 669.88 | 693.66 | None | Migration phase 3 |
| 28 | 693.66 | 717.36 | None | Mistakes to avoid |
| 29 | 717.36 | 743.14 | None | Evidence wall |
| 30 | 743.14 | 763.36 | None | CTA |
| 31 | 763.36 | 787.90 | Full | Closing recap |
| 32 | 787.90 | 803.44 | Full | Clean close |

## Segment Screenplay

### Segment 1 - 0.00-35.04 - Full Avatar Cold Open

Narration purpose: introduce the problem and the thesis: MCP is not bad, the layer choice matters.

Visual: full-screen HeyGen avatar. Add a lower-third only after the avatar introduction line finishes.

Screen layout: avatar full frame. Lower-left title panel, 760px wide, 210px high, 72px from left, 78px from bottom.

On-screen text: "The 2026 Agent Token Stack" and smaller "MCP, Tool Search, Skills, CLI, Code Mode".

Motion beats:
- 0.00-7.70: no overlay. Let "I am the avatar..." land cleanly.
- 8.20: title panel slides in as "MCP used to have a brutal problem" begins.
- 18.00: three small chips appear: "Tool Search", "Scoped Loading", "Code Mode".
- 29.50: final thesis text types in: "Which layer should do which job?"
- 33.80: lower-third fades out before transition.

Cursor: none.

Transition: quick dark wipe into segment 2.

### Segment 2 - 35.04-61.20 - Old MCP Context Flood

Narration purpose: show the old failure mode where tool definitions fill context before useful work begins.

Visual type: full-screen context-window animation, not VS Code.

Screen layout: center 70 percent is a large translucent "MODEL CONTEXT" container. Left edge has tool cards stacked vertically: GitHub, Slack, Sentry, Grafana, Splunk, Jira. Right side has a huge token counter.

On-screen text: "Work has not started yet." Counter: "0K -> 77K tokens loaded".

Motion beats:
- 35.04: empty context window appears.
- 38.00: first three tool cards fly in and expand into schema strips.
- 43.00: remaining cards enter faster, making the context window visibly crowded.
- 50.36: phrase "That is not work" triggers a big stamped label: "OVERHEAD".
- 53.34: counter turns amber on "not just money".
- 55.04-60.18: three words appear in sequence: "Latency", "Confusion", "Less room".

Cursor: none. This is a conceptual motion scene.

Transition: context window compresses horizontally into a thin bar that becomes segment 3's before/after divider.

### Segment 3 - 61.20-85.98 - Tool Search Changed Baseline

Narration purpose: show the improvement from upfront schemas to search-driven expansion.

Visual type: split-screen before/after.

Screen layout: left half labeled "Before: every schema loaded"; right half labeled "After: search, then load only what matters". The divider is large and animated.

On-screen text: "77K context consumption" on left, "8.7K with Tool Search" on right, "85 percent reduction" as final badge.

Motion beats:
- 61.20: split-screen opens from the compressed bar.
- 64.62: left side fills with tool-definition cards.
- 68.08: right side starts with one search box: "find the tool".
- 73.56: right side reveals only three selected tool cards.
- 76.78: left counter lands at "77K".
- 80.96: right counter lands at "8.7K".
- 84.00: green compression wipe crosses the screen.

Cursor: optional. If used, cursor clicks the right-side search box once at 68.08, then disappears.

Transition: green wipe snaps into red warning cards for segment 4.

### Segment 4 - 85.98-107.54 - The Trap

Narration purpose: prevent the viewer from oversimplifying the issue.

Visual type: three full-screen warning cards.

Screen layout: one large statement at a time, each taking most of the screen.

On-screen text:
- "Tool Search reduces schema load."
- "It does not shrink every result."
- "It does not make retrieval perfect."

Motion beats:
- 85.98: card 1 appears with green check.
- 92.00: card 1 slides left; card 2 slams in with amber warning.
- 97.00: card 3 slams in with red outline.
- 102.00: all three cards arrange into a triangle with a center label: "MCP is improved, not magically solved."

Cursor: none.

Transition: triangle rotates flat into a benchmark board.

### Segment 5 - 107.54-139.22 - Accuracy Evidence

Narration purpose: make the reliability tradeoff concrete.

Visual type: large benchmark board with animated bars.

Screen layout: two rows for Anthropic, one stress-test row for Arcade. Use big percentages, not tiny tables.

On-screen text: "49% -> 74%", "79.5% -> 88.1%", "4,000+ tools: about 60%".

Motion beats:
- 107.54: headline: "Better, not magical."
- 112.00: Opus 4 bar grows from 49 to 74.
- 119.00: Opus 4.5 bar grows from 79.5 to 88.1.
- 126.00: Arcade stress-test row appears as a shaking load bar around 60%.
- 133.00: final label: "Search quality becomes reliability."

Cursor: none.

Transition: benchmark board slides left, leaving room for side avatar.

### Segment 6 - 139.22-172.50 - Side Avatar Thesis

Narration purpose: direct address. Explain the layer thesis.

Visual type: avatar side-screen plus animated layer stack.

Screen layout: avatar cropped from HeyGen source on right 35 percent, full height. Left 65 percent has four large vertical layers.

On-screen text: "MCP: external systems", "Skills: procedures", "CLI: deterministic local work", "Code execution: data movement".

Motion beats:
- 139.22: side avatar appears on right, background dimmed behind the crop.
- 146.00: layer 1 appears with an external-system icon.
- 151.00: layer 2 appears.
- 156.00: layer 3 appears.
- 161.00: layer 4 appears.
- 167.00: all layers lock into one stack with big text: "Do not make one layer do every job."

Cursor: none.

Transition: avatar fades right; layer stack becomes browser chrome.

### Segment 7 - 172.50-199.10 - Cloudflare Code Mode Source

Narration purpose: introduce the strongest Code Mode example.

Visual type: source-proof browser view inspired by still 007.

Screen layout: full-screen browser article mock. URL badge top-left. Headline takes center-left. Metric panel on right.

On-screen text: "search() + execute()", "Entire API", "about 1,000 input tokens".

Motion beats:
- 172.50: browser page loads with Cloudflare badge.
- 177.00: two tool pills appear: `search()` and `execute()`.
- 183.00: endpoint-schema cards dissolve into a typed API file.
- 190.00: metric panel flips to "1,000 input tokens".
- 196.00: source badge holds for credibility.

Cursor: cursor scrolls once at 176.00, then clicks/underlines "search and execute" at 179.50.

Transition: metric panel expands into segment 8's number field.

### Segment 8 - 199.10-222.13 - Cloudflare Number Drop

Narration purpose: change the viewer's mental model from schemas-in-context to discovery and execution.

Visual type: kinetic metric collapse.

Screen layout: full-screen number animation. Left number is huge: "1,170,000". Right number: "1,000". Center has a narrowing funnel labeled "discover -> inspect -> execute -> result".

On-screen text: "Context should carry reasoning, not every instruction manual."

Motion beats:
- 199.10: "1,170,000 tokens" fills the screen.
- 203.00: number starts draining through the funnel.
- 208.00: four verbs appear one at a time: discover, inspect, execute, return.
- 214.00: number lands at "1,000".
- 218.00: final thesis sentence writes in large type.

Cursor: none.

Transition: funnel becomes a data pipeline.

### Segment 9 - 222.13-242.37 - Anthropic Code Execution Example

Narration purpose: show the Google Drive to Salesforce workflow.

Visual type: source proof plus workflow icons.

Screen layout: top third is Anthropic source-card mock. Bottom two-thirds shows Google Drive, model context, Salesforce.

On-screen text: "Download transcript -> attach to lead".

Motion beats:
- 222.13: source card appears with Anthropic badge.
- 226.00: Google Drive document icon appears.
- 231.00: transcript moves into model context.
- 236.00: same transcript moves from context to Salesforce.
- 240.00: both trips glow red to show duplicate context transport.

Cursor: cursor underlines the exact example text at 224.50, then disappears.

Transition: duplicate red path splits into naive vs sandbox lanes.

### Segment 10 - 242.37-265.53 - Data Movement Waste

Narration purpose: show that the model is transporting, not reasoning.

Visual type: two-lane data-flow animation.

Screen layout: left lane "Naive tool calls"; right lane "Code execution". Large document object looks like a real transcript page, not a floating label.

On-screen text: "50K intermediate-result tokens" and "Only final status returns".

Motion beats:
- 242.37: left lane replays document moving through context twice.
- 248.00: counter adds "+50K" above the model context.
- 253.00: right lane appears with a code box: `const transcript = drive.download(...)`.
- 258.00: transcript stays inside the sandbox boundary.
- 262.00: only a small green status pill exits: "attached".

Cursor: none.

Transition: green status pill expands into token compression chart.

### Segment 11 - 265.53-286.63 - 150K to 2K

Narration purpose: explain the headline number and the deeper reason.

Visual type: compression chart plus code snippet.

Screen layout: left 60 percent has a giant counter "150K -> 2K". Right 40 percent has three code lines.

On-screen text: "98.7% reduction" and "Keep intermediate data out of context."

Motion beats:
- 265.53: 150K appears in red.
- 269.00: code wrapper appears line by line.
- 272.00: counter collapses to 2K.
- 276.00: 98.7% stamp lands.
- 281.00: final sentence appears in giant type across bottom.

Cursor: optional. Cursor selects the `return status` line at 278.00.

Transition: code panel scrolls to documentation restriction.

### Segment 12 - 286.63-315.39 - Programmatic Tool Calling Caveat

Narration purpose: explain why MCP connector tools are not automatically solved.

Visual type: documentation zoom punch.

Screen layout: large docs page crop. One sentence becomes huge: "MCP connector tools cannot be called programmatically."

On-screen text: "Caveat: connectors are excluded."

Motion beats:
- 286.63: docs page appears at full browser scale.
- 292.00: zoom into restriction line.
- 298.00: red underline animates under "MCP connector tools".
- 304.00: three workaround cards appear: "wrapper pattern", "server-side Code Mode", "controlled runtime".
- 311.00: cards stack into "Use another layer".

Cursor: cursor drags across the restriction line at 294.00.

Transition: red underline becomes sandbox boundary.

### Segment 13 - 315.39-345.23 - Side Avatar Security Warning

Narration purpose: make the warning credible and senior-engineer-friendly.

Visual type: side avatar plus sandbox checklist.

Screen layout: avatar cropped from HeyGen source on left 34 percent. Right 66 percent shows a secure runtime diagram.

On-screen text: "No file system", "No env vars", "Fetch disabled", "Credentials via bindings", "Monitoring required".

Motion beats:
- 315.39: side avatar appears left.
- 321.00: sandbox box draws itself on right.
- 326.00: checklist items appear one by one.
- 335.00: red label appears outside sandbox: "New attack surface".
- 341.00: final label changes to green only when checklist is complete: "Sandboxing is the product."

Cursor: none.

Transition: sandbox box collapses into scoped MCP group selector.

### Segment 14 - 345.23-373.33 - Scoped MCP

Narration purpose: present the lighter-weight production fix.

Visual type: MCP configuration dashboard, not VS Code unless showing the actual env line.

Screen layout: center has a large tool-group selector. Right has a compact config card.

On-screen text: "Rapid", "Pro", "browser", "finance", "ecommerce", "code", `GROUPS=browser,finance`, `TOOLS=...`.

Motion beats:
- 345.23: title: "Scoped MCP: load less on purpose."
- 350.00: 11 group chips appear in a grid.
- 356.00: selected chips glow.
- 362.00: config line types in on right.
- 368.00: huge label appears: "Production agents should be narrow."

Cursor: cursor clicks two group chips and then clicks "apply".

Transition: group chips become skill folders.

### Segment 15 - 373.33-394.63 - Skills Section

Narration purpose: distinguish skills from connectors.

Visual type: file-folder knowledge card.

Screen layout: full-screen folder tree opens into a readable `SKILL.md` page. Use large blocks, not tiny Markdown.

On-screen text: "A skill is procedure, not live access."

Motion beats:
- 373.33: folder labeled `skills/mcp-token-stack/` opens.
- 377.00: `SKILL.md` card expands.
- 381.00: three large notes pin to the file: "what files matter", "what commands to run", "what mistakes to avoid".
- 389.00: main context file shrinks in the background.

Cursor: cursor opens `SKILL.md` and highlights "procedure".

Transition: skill file becomes JARVIS video-production artifact.

### Segment 16 - 394.63-417.06 - JARVIS Skill Artifact

Narration purpose: show JARVIS using skills to keep domain-specific process out of unrelated work.

Visual type: real local artifact emulation.

Screen layout: three large path cards connected by animated arrows: `02-heygen-vo`, `09-stills`, `03-remotion` or `05-hyperframes`.

On-screen text: "Load video-production rules only during video work."

Motion beats:
- 394.63: JARVIS workspace map appears.
- 399.00: HeyGen block rule card opens.
- 404.00: stills path rule card opens.
- 409.00: avatar segment rule card opens.
- 413.00: market-scan and wiki-cleanup cards fade in gray with label: "Do not carry video rules here."

Cursor: cursor only opens the first path card, then disappears.

Transition: local artifact map wipes into a terminal benchmark.

### Segment 17 - 417.06-442.50 - CLI and Scripts

Narration purpose: show why deterministic local CLI often wins.

Visual type: benchmark race.

Screen layout: split-screen race track. Left: CLI. Right: MCP. Large token meters.

On-screen text: "CLI: 1,365 tokens", "MCP: 44,026 tokens".

Motion beats:
- 417.06: CLI command runs on left.
- 423.00: left result returns quickly.
- 428.00: MCP side begins loading tool schemas.
- 433.00: right counter jumps to 44,026.
- 438.00: multiplier stamp appears: "32x token cost".

Cursor: none.

Transition: split-screen shifts from cost comparison to identity/permission comparison.

### Segment 18 - 442.50-470.96 - Honest MCP Defense

Narration purpose: prevent an anti-MCP oversimplification.

Visual type: "who is the agent acting for?" decision scene.

Screen layout: left half is "acting as you on your machine"; right half is "acting for customers across organizations".

On-screen text: "Local credentials" versus "Permission and audit boundary".

Motion beats:
- 442.50: CLI side gets green check for "your machine".
- 449.00: customer/org grid appears on MCP side.
- 455.00: audit log and permission boundary draw around the org grid.
- 462.00: center question appears in huge type: "Who is the agent acting for?"

Cursor: none.

Transition: permission boundary becomes output boundary.

### Segment 19 - 470.96-496.50 - Output Filtering

Narration purpose: show that output size matters after the tool call.

Visual type: messy payload cleanup.

Screen layout: a huge messy web-scrape payload fills the screen, then collapses to three fields.

On-screen text: "title", "URL", "price".

Motion beats:
- 470.96: messy page payload pours in: nav, ads, related links, metadata.
- 477.00: red labels mark unused fields.
- 484.00: unused fields fade out.
- 490.00: three clean fields expand to fill the screen.
- 494.00: final label: "Return what the agent needs."

Cursor: cursor selects "title, URL, price" at the end only.

Transition: three fields become tabular rows.

### Segment 20 - 496.50-520.82 - TOON and Compact Formats

Narration purpose: show TOON as useful but narrow.

Visual type: JSON vs TOON transformation with caution.

Screen layout: left shows repetitive JSON rows. Right shows compact tabular rows. Bottom has a nested object warning.

On-screen text: "Flat rows: useful", "Nested data: be careful", "Prompt tax is real".

Motion beats:
- 496.50: JSON keys repeat visibly.
- 502.00: repeated keys lift out into one header row.
- 507.00: compact table forms.
- 512.00: nested object enters and refuses to flatten cleanly.
- 517.00: caution badge appears: "Use where it fits."

Cursor: none.

Transition: caution badge becomes one row in the full stack table.

### Segment 21 - 520.82-550.32 - Comparison Table

Narration purpose: put the architecture in one coherent map.

Visual type: full-screen decision table with row reveal.

Screen layout: seven wide horizontal rows. Each row has icon, token behavior, complexity, best use.

On-screen text rows: Direct MCP, Tool Search, Scoped MCP, Skills, CLI, Code Execution, Output Filtering.

Motion beats:
- 520.82: blank table frame appears.
- 524.00-543.00: one row reveals every 2.5 seconds.
- 545.00: rows sort into "connection", "procedure", "execution", "payload" bands.
- 548.00: big title: "Right layer. Right scope. Measured output."

Cursor: none.

Transition: table bands slide left to make room for side avatar.

### Segment 22 - 550.32-577.18 - Side Avatar Practical Rule

Narration purpose: direct-address rule for builders.

Visual type: side avatar plus four decision cards.

Screen layout: avatar cropped on right 34 percent. Left has four huge cards in a 2x2 grid.

On-screen text: "Permissioned external access -> MCP", "Procedure -> Skill", "Local deterministic work -> CLI", "Large intermediate data -> Code execution".

Motion beats:
- 550.32: avatar appears right.
- 555.00: MCP card lights up.
- 560.00: Skill card lights up.
- 565.00: CLI card lights up.
- 570.00: Code execution card lights up.
- 574.00: all cards connect to center phrase: "Do not make one tool carry every job."

Cursor: none.

Transition: cards become JARVIS architecture layers.

### Segment 23 - 577.18-600.78 - JARVIS Architecture Map

Narration purpose: show the layered architecture we actually want.

Visual type: full-screen JARVIS operating map.

Screen layout: bottom layer "Wiki memory"; middle layer "Skills + scripts"; top layer "Agent orchestration"; side port "MCP external services"; pulse line "scheduled jobs heartbeat".

On-screen text: "Memory", "Procedure", "Reliable action", "External services", "Heartbeat".

Motion beats:
- 577.18: wiki layer appears as a foundation.
- 582.00: skills and scripts slide in above it.
- 587.00: MCP port attaches to the side.
- 592.00: heartbeat line pulses across the layers.
- 597.00: context window above remains intentionally small.

Cursor: none.

Transition: architecture map folds into an experiment board.

### Segment 24 - 600.78-626.48 - Measurement Plan

Narration purpose: convert argument into a test plan.

Visual type: four-column experiment board.

Screen layout: columns: Naive MCP, Tool Search, JARVIS stack, Code execution. Rows: tokens, latency, reliability, context used.

On-screen text: "QQQ MACD report" as the task.

Motion beats:
- 600.78: task card appears at top.
- 607.00: four columns slide in.
- 612.00: rows appear as empty measurement slots.
- 618.00: checkboxes animate for tokens, latency, reliability, context used.
- 623.00: final label: "Measure before claiming victory."

Cursor: cursor clicks "Run 1" then "Run 2" if the UI is presented as a test board.

Transition: experiment board becomes migration checklist.

### Segment 25 - 626.48-646.34 - Migration Phase 1

Narration purpose: give immediate actions.

Visual type: action checklist with small terminal inset.

Screen layout: full-screen checklist with four rows. Terminal inset only for `/mcp`.

On-screen text: "1. Check token load", "2. Disconnect unused servers", "3. Turn on Tool Search", "4. Scope by group or tool list".

Motion beats:
- 626.48: "Free wins - one hour" appears.
- 630.00: `/mcp` command runs in inset.
- 633.00: unused server cards fade out.
- 637.00: Tool Search toggle turns on.
- 641.00: group allowlist appears.

Cursor: cursor clicks the Tool Search toggle and group selector.

Transition: checklist row 4 becomes a file move animation.

### Segment 26 - 646.34-669.88 - Migration Phase 2

Narration purpose: move procedure into skills, deterministic work into scripts, and filter outputs.

Visual type: three-lane refactor.

Screen layout: left "CLAUDE.md bloat"; center "skills/"; right "scripts/". Bottom "filtered output".

On-screen text: "Procedures -> Skills", "Deterministic work -> Scripts", "Full object -> 3 fields".

Motion beats:
- 646.34: bloated context file appears overstuffed.
- 651.00: procedure blocks move into `skills/`.
- 656.00: command blocks move into `scripts/`.
- 661.00: full JSON object shrinks to three fields.
- 666.00: context file becomes small and readable.

Cursor: cursor drags one rule from CLAUDE.md to SKILL.md, then disappears.

Transition: three lanes merge into sandbox scene.

### Segment 27 - 669.88-693.66 - Migration Phase 3

Narration purpose: describe heavy patterns and warn about sandboxing.

Visual type: controlled runtime build.

Screen layout: large sandbox boundary center. Left side has MCP connector wrappers. Inside is code execution. Right side has final result only.

On-screen text: "Programmatic where it fits", "Code Mode for MCP-heavy workflows", "Sandboxing is not optional".

Motion beats:
- 669.88: sandbox boundary draws.
- 674.00: programmatic tool calling card enters, but MCP connector card gets blocked.
- 680.00: wrapper/API card bridges into sandbox.
- 685.00: large data object stays inside.
- 690.00: only final result exits; red security lock remains visible.

Cursor: none.

Transition: security lock breaks into three mistake cards.

### Segment 28 - 693.66-717.36 - Mistakes to Avoid

Narration purpose: correct common wrong takes.

Visual type: three bad-take cards flipping into corrected takes.

Screen layout: three cards across full screen. Red side first, green side after flip.

On-screen text:
- Red: "MCP is dead" -> Green: "CLI wins local deterministic work."
- Red: "MCP is fixed" -> Green: "Tool Search helps but has caveats."
- Red: "TOON everywhere" -> Green: "Compact formats fit certain data."

Motion beats:
- 693.66: first red card appears and flips.
- 700.00: second card appears and flips.
- 706.00: third card appears and flips.
- 712.00: final phrase writes large: "Right layer. Right scope. Measured output."

Cursor: none.

Transition: final phrase becomes evidence wall title.

### Segment 29 - 717.36-743.14 - Evidence Beats Opinion

Narration purpose: anchor the argument in sources and JARVIS testing.

Visual type: cinematic evidence wall.

Screen layout: large mosaic of source tiles: Cloudflare, Anthropic, Arcade, Scalekit, JARVIS. Each tile should be readable enough to identify source, not a tiny screenshot.

On-screen text: "The debate is moving from opinion to evidence."

Motion beats:
- 717.36: "Opinion" labels fade out.
- 722.00: Cloudflare tile slides in.
- 726.00: Anthropic tile slides in.
- 730.00: Arcade and Scalekit tiles slide in.
- 735.00: JARVIS test-bench tile appears larger in the center.
- 740.00: all tiles connect to "Test it on real work."

Cursor: none.

Transition: evidence wall dims and CTA elements rise over it.

### Segment 30 - 743.14-763.36 - Graphics CTA

Narration purpose: ask for subscribe, like, and notification before closing summary.

Visual type: full-screen CTA with motion, not avatar.

Screen layout: three giant controls across the center: Subscribe, Like, Bell. Below them: "Next: JARVIS measurement run".

On-screen text: "Subscribe", "Like", "Ring the bell", "Next video: measure the stack on JARVIS".

Motion beats:
- 743.14: subscribe button appears.
- 747.00: button clicks and changes to "Subscribed".
- 750.00: like icon pulses once.
- 753.00: bell rings with small soundless visual vibration.
- 756.00: next-video teaser card slides in.
- 761.00: CTA fades before avatar closing starts.

Cursor: cursor clicks Subscribe, Like, and Bell exactly on those beats.

Transition: fade to avatar full screen.

### Segment 31 - 763.36-787.90 - Full Avatar Recap

Narration purpose: final answer and recap.

Visual: full-screen HeyGen avatar. Minimal overlay only.

Screen layout: avatar full frame. Small bottom-center phrase, not covering face or microphone.

On-screen text: "MCP is one layer."

Motion beats:
- 763.36: avatar appears clean.
- 768.00: small phrase appears: "MCP is one layer."
- 773.00: phrase changes to "Skills for procedures."
- 778.00: phrase changes to "CLI for local deterministic work."
- 783.00: phrase changes to "Code execution when data should stay out of context."

Cursor: none.

Transition: no hard transition; continue avatar into segment 32.

### Segment 32 - 787.90-803.44 - Full Avatar Close

Narration purpose: final memorable question and send-off.

Visual: full-screen HeyGen avatar, clean close.

Screen layout: avatar full frame. Final title card fades in only during the last 4 seconds.

On-screen text: "Where do the tokens go? Where does the data live? Who is the agent acting for?"

Motion beats:
- 787.90: no overlay for first sentence.
- 793.00: three questions appear one at a time in small lower-third style.
- 799.50: final card: "The 2026 Token Stack".
- 802.50: fade to black.

Cursor: none.

Transition: final fade out.

## Renderer Checklist Before Next Attempt

- Confirm segment 3 start is set to 61.20s, not merged into segment 2.
- Confirm avatar crops at segments 6, 13, and 22 use the HeyGen source as a side-avatar layer.
- Do not group segments unless this screenplay explicitly says to transition continuously.
- Each segment must own its own visual layer and scene timing.
- Before full render, export a QA frame at the midpoint of every segment and inspect it against this document.
- Any cursor path must be listed in the segment block. If it is not listed, hide the cursor.
