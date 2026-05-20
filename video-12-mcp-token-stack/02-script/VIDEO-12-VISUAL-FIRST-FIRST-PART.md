# Video 12 Visual-First First-Part Plan

Purpose: rebuild the first part of Video 12 using a visual-first method. The visual sequence leads the narrative, and the VO explains what the viewer is already seeing. This replaces the earlier four-subsegment-per-segment breakdown for Segments 002-006.

Reference standard: use `09-stills/TestFolder/contact-sheet.png`, especially `002A`, `002B`, `003C`, `004B`, `005B`, `005C`, `006A`, and `006C`. The goal is not to copy the stills pixel by pixel. The goal is to build comparable HyperFrames scenes with live objects, motion, sequencing, and readable holds.

## Production Rules

- A segment is one narrative idea, usually 25-35 seconds.
- A subsegment is one animated visual shot, usually 10-18 seconds.
- Most segments get 2 subsegments. Use 3 only when the concept naturally has three steps.
- Visuals may lead the VO by 0.5-1.5 seconds. The viewer should see the action begin before the narration names it.
- The visual should tell the basic story with audio muted.
- The VO should describe, interpret, and sharpen the visual action.
- Avoid text-only box scenes. Every subsegment needs a system action: cards flow, meters climb, payloads expand, search beams scan, layers organize, data duplicates, or context compresses.
- Keep important text stable long enough to read. Text and panels must not enter over existing readable text unless the older text is leaving or intentionally dimmed.
- No viewer-facing production labels such as "Segment 004," "Video 12," "test," or internal filenames.

## Segment 002 - Old Failure Mode: Tool Definitions Before Work

Target duration: 30-34 seconds  
Subsegments: 2  
Visual story: before any user task exists, connected tools are already filling the context window. Then the accumulated load becomes a token accounting dashboard that shows why this is overhead.

### 002A - Integrations Fill Context Before the Task

Target duration: 14-16 seconds  
Reference: `002A.png`

Scene idea: The old MCP setup looks alive before the user has asked for anything.

Main visual: A central "AI context window" opens in the middle. GitHub, Slack, Sentry, Grafana, Splunk, and Jira panels sit around it. Streams of small schema cards begin moving from the tool panels into the central window. At the bottom, an empty user prompt waits untouched.

Objects:
- Six tool source panels with distinct accent colors.
- Central context window with browser-style top bar.
- Empty user prompt bar below the context window.
- Small schema cards with unreadable code-like lines.
- Electric blue and cyan flow paths.
- Bottom status text: "User task has not started yet."

Motion:
- Visual leads VO: context window flickers on first, then tool panels slide in from the sides.
- Schema cards start moving before the VO says "Before the user types a task."
- Cards do not simply fade. They travel along curved paths, accelerate near the context boundary, and stack inside the window.
- The empty prompt bar rises slightly and glows, making the contrast obvious: no task has started, but context is already filling.

Entrance:
- Dark circuit background powers up.
- Tool panels arrive from offscreen left and right.
- Central context window scales up from 0.85 with cyan glow.

Exit:
- The streams continue for a moment, then freeze into a dense context pile.
- Camera pushes into the central pile and transitions into the token dashboard of 002B.

Information hierarchy:
- Primary: "Integrations connected before work begins."
- Secondary: tool names.
- Tertiary: tiny schema cards and decorative route labels.

What must remain readable:
- Tool names.
- "Central AI context window."
- "Empty user prompt."
- "User task has not started yet."

What should not appear:
- Long labels on every small card.
- Dense explanatory paragraphs.
- Any "Segment 002" label.

VO draft:
"Here is the old failure mode. The user has not typed a task yet, but the system is already connected to GitHub, Slack, Sentry, Grafana, Splunk, and Jira. Watch what happens before real work even begins: tool definitions start moving into the model context."

### 002B - Idle Context Becomes Measurable Overhead

Target duration: 15-18 seconds  
Reference: `002B.png`, with less clutter than the still.

Scene idea: The incoming tool definitions resolve into an observability-style token meter.

Main visual: The central pile becomes a dashboard titled "Context memory before the task." Colored horizontal bands stack up to 55,000 tokens. A small "actual problem" space remains empty and squeezed to the side.

Objects:
- Amber warning perimeter frame.
- Stacked token meter with six bands: GitHub, Slack, Sentry, Grafana, Splunk, Jira.
- Left status panels: integrations active, pre-task data populated.
- Right problem panel: uninitialized.
- Small line chart or meter at the bottom showing overhead rising.

Motion:
- Visual leads VO: stacked bands begin snapping into place before the VO says "That is overhead."
- Number count rises from 0 to 55,000.
- The actual problem area shrinks or gets pushed aside as the token meter fills.
- Four overhead icons appear briefly around the meter: latency, confusion, cost, less room. These should orbit or slide in as secondary callouts, not become separate text cards.

Entrance:
- The frozen schema pile from 002A collapses into the first token band.
- Remaining bands stack in from alternating sides.

Exit:
- Amber frame pulses once.
- The problem-space panel dims, leaving the viewer with the overhead feeling.

Information hierarchy:
- Primary: "55,000 tokens."
- Secondary: "Context memory before the task."
- Tertiary: six tool-definition bands.

What must remain readable:
- "55,000 tokens."
- Tool-definition band names.
- "Actual problem: not loaded yet."

What should not appear:
- More than four overhead callouts.
- Tiny unreadable percentages that compete with the main number.

VO draft:
"That is not work. That is overhead. The model is carrying definitions before it knows the problem. And overhead is not just money. It is latency, confusion, and less room for the actual task."

## Segment 003 - Tool Search Changes the Baseline

Target duration: 38-45 seconds  
Subsegments: 3  
Visual story: Tool Search turns upfront loading into a three-step visual process. This segment can support three subsegments because the concept itself has three steps plus a payoff.

### 003A - Minimal Initial Load

Target duration: 11-13 seconds  
Reference: `003A.png`, `003C.png`

Scene idea: The full tool library remains outside the reasoning window.

Main visual: A clean model context window contains one compact "Tool Search" card. A large grid of available tools sits outside the context boundary in dim gray.

Objects:
- Model context window.
- Small Tool Search card inside it.
- Large external tool library grid outside it.
- Boundary line between "inside context" and "outside context."

Motion:
- Visual leads VO: the big tool library appears first and threatens to move in, then stops at the boundary.
- Only the Tool Search card slips through the boundary and lands inside the model context.
- The library cards dim to signal they are available but not loaded.

Entrance:
- Library grid slides in from the right as a large mass.
- Context window opens from the center.
- Tool Search card snaps into the context window with a small glow.

Exit:
- A blue search light begins to form on the Tool Search card, setting up 003B.

Information hierarchy:
- Primary: small loaded search tool versus large unloaded library.
- Secondary: boundary between outside and inside.

What must remain readable:
- "Tool Search."
- "Tool library outside context."
- "Minimal initial load."

What should not appear:
- Selected Jira/Sentry/AWS cards loaded yet.
- Token reduction numbers yet.

VO draft:
"Tool Search changes the baseline. Step one: the model does not load every tool definition. The full library stays outside the reasoning window, and only a small search capability enters the context."

### 003B - Search Selects Relevant Tools

Target duration: 12-15 seconds  
Reference: `003B.png`, `003C.png`

Scene idea: The search card actively scans the library and identifies matches.

Main visual: The Tool Search card projects a moving blue search beam across the external tool library. Jira Task, Sentry Error, and AWS Metrics glow green-blue while unrelated tools remain gray.

Objects:
- Search beam or spotlight.
- Tool grid outside context.
- Three matched tool cards.
- Unmatched gray cards.
- Small task prompt signal entering from the bottom.

Motion:
- Visual leads VO: the task signal arrives as a small pulse, then the beam begins scanning before the narration says "when the task arrives."
- Beam sweeps across rows of tools.
- Cards brighten only when the beam crosses them.
- Selected cards lift slightly but do not enter context yet.

Entrance:
- Task signal pulses into the Tool Search card.
- Beam extends from the context window to the library.

Exit:
- Matched cards hover in a selected lane, ready to move.

Information hierarchy:
- Primary: three selected tool cards.
- Secondary: scanning beam.
- Tertiary: gray background library.

What must remain readable:
- "Jira Task."
- "Sentry Error."
- "AWS Metrics."
- "Selected, not loaded yet."

What should not appear:
- A completed context window full of selected tools before 003C.
- Too many highlighted tools.

VO draft:
"Step two: when the task arrives, that search tool scans the library. It does not grab everything. It selects the few definitions that match the job: maybe Jira tasks, Sentry errors, and AWS metrics."

### 003C - Inject Matches And Show The Compression

Target duration: 15-17 seconds  
Reference: `003C.png`, `003D.png`

Scene idea: The selected definitions move into context, then the old upfront load compresses into the new on-demand load.

Main visual: The three selected cards fly into a green optimized context window. Unrelated cards stay outside and fade back. Then a token comparison appears: 77K upfront load compresses into 8.7K on-demand load.

Objects:
- Green optimized context window.
- Three selected definition cards.
- Faded unrelated library.
- Red 77K meter.
- Green 8.7K meter.
- Compression arrow.

Motion:
- Selected cards travel along visible paths into context, one after another.
- Context window glows green as each card lands.
- The unused library recedes and desaturates.
- Red 77K meter collapses horizontally into green 8.7K meter.

Entrance:
- Matched cards from 003B continue their motion into the context.

Exit:
- The green 8.7K meter holds for 2 seconds.
- A subtle amber edge appears, foreshadowing Segment 004: improved does not mean solved.

Information hierarchy:
- Primary: on-demand injection.
- Secondary: 77K to 8.7K compression.
- Tertiary: unused tools stay outside.

What must remain readable:
- "77,000 tokens."
- "8,700 tokens."
- "Loaded on demand."

What should not appear:
- A claim that MCP is fully fixed.
- Extra caveats that belong in Segment 004.

VO draft:
"Step three: only the relevant definitions are injected. The unrelated tools stay outside the reasoning space. That is the shift: context is loaded on demand, not prepaid upfront. In Anthropic's example, the load drops from roughly seventy-seven thousand tokens to about eight point seven thousand. That is a serious improvement."

## Segment 004 - Search Helps, But It Does Not Fix Everything

Target duration: 26-32 seconds  
Subsegments: 2  
Visual story: The green win from Segment 003 gets stress-tested. The same dashboard reveals three failure modes: large results, workflow copying, and imperfect retrieval.

### 004A - The Easy Take Breaks Under Stress

Target duration: 12-14 seconds  
Reference: `004A.png`, `004B.png`

Scene idea: The viewer sees "MCP is fixed now?" appear as an unstable conclusion, then the first failure mode breaks through it.

Main visual: A polished "MCP is fixed now?" claim card sits over the successful green token reduction chart from 003C. A caution frame slams around it. Then a small schema card triggers a massive red result payload that pushes the claim aside.

Objects:
- Overconfident claim plate.
- Green token reduction chart behind it.
- Small schema card.
- Large red JSON/result payload panel.
- Model context boundary line.

Motion:
- Visual leads VO: the claim card appears first, tempting the viewer.
- Caution frame snaps around it when VO says "dangerous."
- Small schema card travels into a tool.
- Large payload expands from the tool result and forces the claim card out of the center.

Entrance:
- Claim card drops in with a heavy amber frame.
- Payload expands with a fast horizontal wipe, not a fade.

Exit:
- Payload remains large and presses against the model context boundary.

Information hierarchy:
- Primary: small schema can still produce large result.
- Secondary: "MCP is fixed now?" is incomplete.

What must remain readable:
- "Small schema."
- "Large result."
- "Incomplete conclusion."

What should not appear:
- Four separate warning cards at once.
- Paragraph-length caveat text.

VO draft:
"But this is where the easy take gets dangerous. If we say MCP is fixed now, we miss the next problem. Search reduces schema load. It does not make every tool result small."

### 004B - Workflow And Retrieval Risk Remain

Target duration: 14-18 seconds  
Reference: `004C.png`, `004D.png`

Scene idea: The remaining two caveats appear as animated system failures, not static warning boxes.

Main visual: The large payload becomes a data object that moves through a three-tool workflow and duplicates through the model context. Then the scene pivots into a retrieval board where one correct tool is missed and one wrong tool is selected.

Objects:
- Three tool nodes.
- Model context boundary at center.
- Large data blob copied through context.
- Duplicate data shadows.
- Retrieval board with correct, missed, and irrelevant cards.
- Reliability meter.

Motion:
- Data blob crosses the context boundary twice, leaving ghost copies behind.
- Ghost copies stack and raise an amber "intermediate data" meter.
- The workflow diagram folds into a retrieval board.
- Search beam lands on one correct tool, misses one red-outlined required tool, and highlights one amber irrelevant tool.

Entrance:
- Data blob continues from 004A large result.
- Tool nodes snap into a chain.

Exit:
- Reliability meter lands in amber, not red, to say "risk," not total failure.

Information hierarchy:
- Primary: search does not solve workflow transport or retrieval quality.
- Secondary: duplicate copies and missed tool.

What must remain readable:
- "Copied through context."
- "Missed required tool."
- "Retrieval quality affects reliability."

What should not appear:
- A dense matrix of many tools.
- Too many labels on path lines.

VO draft:
"It also does not make every multi-step workflow efficient. Data can still be copied through the context again and again. And retrieval is now part of reliability: the system has to find the right tool, at the right moment, without pulling in the wrong one."

## Segment 005 - Accuracy Improves, But Retrieval Is Not Magic

Target duration: 28-34 seconds  
Subsegments: 2  
Visual story: Stronger benchmarks appear, then the larger tool-library stress test shows why search quality becomes a reliability concern.

### 005A - Better Numbers, Still Not A Guarantee

Target duration: 13-16 seconds  
Reference: `005A.png`

Scene idea: The benchmark board grows upward with real improvements, but the visual tone stays measured.

Main visual: A source-proof benchmark board shows Opus 4 improving from 49% to 74%, and Opus 4.5 improving from 79.5% to 88.1%. Bars grow from left to right. The board is framed like evidence, not marketing.

Objects:
- Two progress rows.
- Before and after markers.
- Evidence-frame border.
- "Improved, not perfect" badge.

Motion:
- Visual leads VO: old percentages appear first in muted red/orange.
- New percentages slide in from the right and push the bars longer.
- The board briefly glows green, then settles into sober blue.

Entrance:
- Board rises from bottom like a report page entering a scanner.

Exit:
- The board tilts backward and becomes one tile in a much larger tool grid for 005B.

Information hierarchy:
- Primary: 49 to 74, 79.5 to 88.1.
- Secondary: "better, not magical."

What must remain readable:
- "Opus 4: 49% to 74%."
- "Opus 4.5: 79.5% to 88.1%."

What should not appear:
- Confetti, victory animation, or over-hyped "solved" language.

VO draft:
"The accuracy numbers are better, but not magical. Anthropic reported MCP eval improvements from forty-nine percent to seventy-four percent on Opus 4, and from seventy-nine point five to eighty-eight point one percent on Opus 4.5."

### 005B - Retrieval Quality Becomes Part Of Reliability

Target duration: 15-18 seconds  
Reference: `005B.png`, `005C.png`, `005D.png`

Scene idea: The evidence board becomes a huge library of possible tools. The search system has to retrieve the right one from thousands.

Main visual: Thousands of tiny tool cards recede into depth. A search beam tries to locate a matching card. A large amber 60% retrieval ring appears. The visual then resolves into a reliability model where "retrieval quality" becomes a highlighted component.

Objects:
- Deep field of tool cards.
- Moving search beam.
- Amber 60% ring.
- Reliability checklist: permissions, latency, output size, retrieval quality.
- Retrieval quality highlighted.

Motion:
- Camera pushes through the tool library.
- Search beam picks out a few candidates but leaves visible uncertainty.
- The 60% ring draws itself clockwise.
- Tool library compresses into the reliability checklist.

Entrance:
- Benchmark board from 005A flips into a field of tool cards.

Exit:
- Retrieval quality highlight remains as the bridge to layered architecture in Segment 006.

Information hierarchy:
- Primary: 4,000+ tools and around 60% retrieval.
- Secondary: retrieval quality is now part of reliability.

What must remain readable:
- "4,000+ tools."
- "Around 60% retrieval."
- "Retrieval quality."

What should not appear:
- Too many benchmark citations or tiny labels.
- A red disaster tone. This is caution, not collapse.

VO draft:
"Then Arcade stress-tested more than four thousand tools and saw retrieval around sixty percent. That is the trade: better context economics, but now search quality is part of the reliability model."

## Segment 006 - Layered Architecture, Not One Universal Tool

Target duration: 30-36 seconds  
Subsegments: 2  
Visual story: The reliability checklist becomes a stack of architectural layers. Then an overloaded single-layer design breaks, and the organized multi-layer stack takes its place.

### 006A - Four Layers, Four Jobs

Target duration: 14-17 seconds  
Reference: `006A.png`, `006B.png`

Scene idea: The video states the core position with an organized architecture, not a debate card.

Main visual: Four colored architecture layers assemble from bottom to top: MCP, Skills, CLI Scripts, Code Execution. Each layer has a small icon and one job phrase. On the side, three overclaims are crossed out as small secondary cards, not the main scene.

Objects:
- MCP layer: external systems.
- Skills layer: procedures.
- CLI Scripts layer: local deterministic work.
- Code Execution layer: multi-step compression.
- Three overclaim chips: "MCP is dead," "Skills replace MCP," "CLI solves everything."

Motion:
- Visual leads VO: the empty reliability model from 005B transforms into a blank architecture surface.
- Layers slide in from different directions and lock together.
- Overclaim chips appear, then are crossed out and slide to the side.
- The architecture stack remains stable and readable.

Entrance:
- Reliability checklist from 005B collapses into four empty layer slots.
- Each slot fills with a distinct color.

Exit:
- The stable stack shifts left to make room for the overloaded-layer comparison in 006B.

Information hierarchy:
- Primary: four layers and their jobs.
- Secondary: no single layer is the universal answer.

What must remain readable:
- "MCP - external systems."
- "Skills - procedures."
- "CLI - local deterministic work."
- "Code execution - multi-step compression."

What should not appear:
- Paragraph text inside layers.
- Dense decision matrix yet.

VO draft:
"So here is our position. MCP is not dead. Skills are not a replacement for MCP. And CLI scripts are not the universal answer. These are layers, and each layer has a different job."

### 006B - Do Not Force One Layer To Carry Everything

Target duration: 16-19 seconds  
Reference: `006C.png`, `006D.png`

Scene idea: A single overloaded layer tries to carry all jobs and bends into the red. Then the jobs redistribute across the correct layers.

Main visual: On the left, one monolithic layer is overloaded with four task weights: external access, procedures, local commands, and data transformation. A stress gauge moves into red. On the right, the same task weights move one by one into the correct layer of the organized stack. The gauge drops back into green.

Objects:
- Overloaded monolith.
- Four task weights.
- Stress gauge.
- Organized four-layer stack.
- Optional compact decision surface at the end.

Motion:
- Task weights drop onto the monolith one by one.
- Monolith bends and emits red stress lines.
- The weights lift off and fly to their matching layers.
- Stress gauge sweeps from red to green.
- Final frame holds the clean stack.

Entrance:
- Stable stack from 006A duplicates into two panels: bad single-layer design versus organized layered design.

Exit:
- Clean layered stack holds for 2 seconds and becomes the bridge to Cloudflare Code Mode in Segment 007.

Information hierarchy:
- Primary: use the right layer for the job.
- Secondary: forcing one layer creates strain.

What must remain readable:
- Four layer names.
- "Use the right layer for the job."

What should not appear:
- A full decision matrix with many rows unless this becomes its own later scene.
- Any text overlap during task-weight transfers.

VO draft:
"MCP connects agents to external systems. Skills teach the agent procedures. CLI scripts do deterministic local work. Code execution compresses multi-step workflows. The mistake is forcing one layer to do all four jobs."

## Timing And Build Notes For The Next Test

Recommended test range: Segments 002-006 only.  
Estimated duration: 150-180 seconds depending on final VO pace.  
Recommended subsegment count: 11 total: two for Segments 002, 004, 005, 006, and three for Segment 003.

Before coding:

1. Record or synthesize VO from the drafts above.
2. Force-align the exact audio to the subsegment text.
3. Create a timing JSON with start, end, lead-in, hold, and exit times for each subsegment.
4. Build each subsegment as a HyperFrames shot, not as a static full segment.
5. QA every subsegment at entrance, mid-build, final hold, and exit.

Minimum QA frames per subsegment:

- 0.5 seconds after entrance starts.
- Moment when the main object/action is halfway built.
- Final readable hold.
- 0.3 seconds before exit completes.

Rejection criteria:

- Scene reads as boxes with text but no system action.
- VO describes one concept while visual shows another.
- Text overlaps with active readable text.
- Text is smaller than needed for a 1080p YouTube viewer.
- Visual relies mainly on fades.
- Completed frame would not make sense with audio muted.
