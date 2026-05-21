# Video 12 Visual Treatment Board - First 10 Segments

Purpose: define the production-level visual direction for Segments `002-010` using the newer structure: most segments get **2 visual subsegments**, with **3 only when the teaching idea naturally requires it**.

This replaces the earlier 4-subsegment image-prompt structure. The older A/B/C/D stills remain useful as concept references, but they are no longer the production unit.

## Production Rule

- Default: `2` visual beats per narrative segment.
- Exception: `3` visual beats when the concept has a natural sequence, such as Step 1 / Step 2 / Step 3.
- Each beat should generally run `10-18 seconds`, depending on final VO.
- Visuals should be selected before final VO.
- HyperFrames/Remotion are assembly and precision tools, not the only visual language.
- Consider Veo, still+motion, source capture, simulated UI/IDE, talking head overlays, and HyperFrames/Remotion for every beat.

## High-Level Direction

Segments `002-003` should carry the most important visual correction. They should not be abstract boxes. Segment `002` should feel like a real AI workbench or workstation where tools are connected before the task starts. Segment `003` should become more precise and instructional, because it teaches the Tool Search mechanism.

Segments `004-006` should move into interpretation: what Tool Search does not solve, why retrieval becomes reliability, and why MCP/Skills/CLI/Code Execution are layers rather than replacements.

Segments `007-010` should use more source-proof and workflow-specific visuals: Cloudflare Code Mode, discover/inspect/execute/return, and the Google Drive to Salesforce transcript example.

---

## Segment 002 - Old Failure Mode: Tool Definitions Before Work

Recommended subsegments: `2`

### 002A - Connected Tools Before The Task

VO coverage: "Here is the old failure mode. You connect GitHub, Slack, Sentry, Grafana, Splunk, maybe Jira. Before the user types a task..."

**Option 1 - Cinematic Workstation UI**

A realistic desk and monitor fill the frame. On the monitor, a dark AI workbench is open. The left rail shows connected services: GitHub, Slack, Sentry, Grafana, Splunk, and Jira. Each service lights up one by one as available/search-ready while the central task input is still empty or only has a blinking cursor. The right side shows a context/search panel waiting to activate. The viewer understands that the system is prepared before the user has actually started the job. This treatment should feel like a real operator workstation, not an abstract context diagram.

**Option 2 - Simulated IDE / Tool Sidebar**

A VS Code-like interface shows a sidebar called "Connected MCP Tools." GitHub, Slack, Sentry, Grafana, Splunk, and Jira each switch to green status. The editor area remains blank except for an empty task prompt. A small context inspector shows tool definitions beginning to register. The action is precise and controllable, but less cinematic than the workstation shot.

**Option 3 - Talking Head With Tool Cards**

The presenter remains on screen while service cards enter from different screen edges. Each card opens a small drawer showing "available" or "indexed," then docks into an organized side rail. A blank prompt box appears beside the presenter. The speaker anchors the explanation while the graphics show that tool readiness is happening before the task.

**Recommendation**

Use **Option 1: Cinematic Workstation UI**. This is the strongest correction away from the old box-heavy style. Use HyperFrames/Remotion only for overlays, service highlights, cursor text, and labels.

### 002B - Idle Context Becomes Overhead

VO coverage: "...the model is already carrying tool definitions. That is not work. That is overhead. And overhead is not just money. It is latency, confusion, and less room for the actual problem."

**Option 1 - Same Workstation, Context Usage Rises**

Continue from `002A`. The right-side context usage panel begins filling before the task is meaningful. Service badges send compact definition packets into the context panel. The number climbs toward `55,000 tokens`. The central task area visibly loses space as the context panel grows. Around the monitor, four small effects appear: a latency stopwatch, a cost counter, tangled confusion arrows, and a shrinking "actual problem" workspace. This keeps the whole segment as one coherent mini-story.

**Option 2 - Task Space Gets Crowded Out**

The user's task input is shown cleanly at first. Then a wall of schema cards slides forward and starts covering or squeezing the task area. The viewer sees the practical effect: less room for the actual problem before the model has reasoned about anything.

**Option 3 - Physical Load Metaphor**

An abstract AI model or assistant carries heavy manuals labeled GitHub, Slack, Sentry, Grafana, Splunk, and Jira before receiving the actual task. The model leans under the weight. This is simple and memorable, but less specific than the workstation sequence.

**Recommendation**

Use **Option 1**. The best version of Segment 002 is a continuous workstation story: connected services wake up, context usage rises, overhead effects appear, and the task area gets squeezed.

---

## Segment 003 - Tool Search Changes The Baseline

Recommended subsegments: `3`

This is the main exception to the 2-beat rule because the concept is naturally a three-step process.

### 003A - Step 1: Minimal Initial Load

VO coverage: "Anthropic's Tool Search changed the baseline. The workflow is simple, but important. Step one: Claude does not load every tool definition into context. It starts with a tiny search tool, while the full tool library stays outside the reasoning window."

**Option 1 - Optimized Workbench**

The same AI workbench resets into optimized mode. The service rail remains available, but the active context panel contains only one compact Tool Search capability. The full tool library appears as a blurred/off-context shelf behind or beside the interface. The library tries to move toward context but stops at a boundary; only the small Tool Search capability passes through.

**Option 2 - Digital Library Shelf**

Thousands of tool manuals sit outside a glass reasoning room. Only a small search lens enters the room. The full library remains visible but outside. This is visually rich and good for Veo, but less literal than a real workbench.

**Option 3 - IDE Plugin Manager**

A simulated IDE shows many installed tools in a sidebar, but the active context inspector contains only `tool_search()`. Tool schemas remain collapsed and off-context. This is the most precise teaching treatment.

**Recommendation**

Use a **hybrid of Option 1 and Option 3**: a polished workbench/IDE where the Tool Search card is the only object entering active context.

### 003B - Step 2: Search Selects Relevant Tools

VO coverage: "Step two: when the task arrives, that search tool looks across the library and selects the few tools that match the job: maybe Jira tasks, Sentry errors, or AWS metrics."

**Option 1 - Ranked Search Results**

The task appears: investigate a Sentry error and create a Jira issue, possibly with AWS metrics. A search panel opens and ranks candidate tools. Sentry, Jira, and AWS rise to the top and glow. Unrelated tools stay gray. This creates a reusable visual language for later retrieval reliability discussion.

**Option 2 - Search Beam Across Library**

The Tool Search capability emits a blue beam across the off-context tool library. It passes over irrelevant tools without effect, then locks onto Sentry, Jira, and AWS. The selected cards lift but do not enter context yet.

**Option 3 - Detective Lens**

A magnifying lens moves across a field of tool cards. Correct matches stamp themselves as "match." This is visually intuitive but less tied to the actual software mechanism.

**Recommendation**

Use **Option 1: Ranked Search Results**. It sets up Segment `004D` and `005D`, where search quality becomes reliability.

### 003C - Step 3: Inject Matches And Show Reduction

VO coverage: "Step three: only those relevant tool definitions are injected into the model context... context is loaded on demand, not prepaid upfront. In Anthropic's own example, consumption moves from roughly seventy-seven thousand tokens to about eight point seven thousand. That is a serious improvement."

**Option 1 - Selected Cards Enter Context, Then Metric Compresses**

The selected Sentry, Jira, and AWS cards slide from the ranked results into the active context panel. Each becomes a compact schema chip. Unrelated tools recede and desaturate. Then a red ghost path labeled `77,000 tokens` compresses into a green `8,700 tokens` packet. The viewer sees both the mechanism and the payoff.

**Option 2 - Physical Compression Gate**

A massive red stack of upfront schemas labeled `77K` collapses through a compression gate into a small green packet labeled `8.7K`. The selected tool cards remain visible as the reason for the smaller packet.

**Option 3 - Source-Proof Metric Card**

Show a source-style metric card with the `77K -> 8.7K` claim, then animate the two numbers into the workbench. This is more credible but less dramatic.

**Recommendation**

Use **Option 1**. It combines the Step 3 action and the metric payoff without creating a fourth subsegment.

---

## Segment 004 - Search Helps, But It Does Not Fix Everything

Recommended subsegments: `2`

### 004A - The Dangerous Easy Take

VO coverage: "But this is where the easy take gets dangerous. If you say, 'MCP is fixed now,' you miss the next problem."

**Option 1 - Presenter Challenge**

Return to the presenter for a direct interpretive reset. The green `8.7K` improvement number floats beside him, then an amber "not solved" marker slices through it. Three unresolved icons appear behind or beside the improvement: large result payloads, multi-step workflow waste, and retrieval mistakes.

**Option 2 - False Victory Freeze**

The `8.7K` success frame freezes like a victory screen. A caution frame slams around it, and the claim "MCP is fixed now?" appears as an overreach. The camera pulls back to reveal the success card is only one tile in a larger problem board.

**Option 3 - Evidence Board**

The claim "MCP is fixed now" appears on an evidence board. A red marker circles "fixed," and three evidence folders slide in underneath for the problems that remain.

**Recommendation**

Use **Option 1**. A talking-head reset helps the viewer understand that the video is not just celebrating Tool Search.

### 004B - What Still Breaks: Results, Workflows, Retrieval

VO coverage: "Search reduces schema load. It does not make every tool result small. It does not make every multi-step workflow efficient. And it does not make tool retrieval perfectly reliable."

**Option 1 - Three-Part Problem Board**

Build one fast editorial board with three animated areas. First, a small schema request triggers a huge JSON/document payload. Second, a large data object crosses the model context boundary repeatedly and leaves ghost copies. Third, a ranked retrieval panel shows two correct tools, one missed needed tool, and one irrelevant amber result. Each problem appears as the VO names it, then the three problems lock together as the unresolved risk set.

**Option 2 - Conveyor Belt Through Context**

Focus mainly on workflow waste. A data object travels from Tool A into context, out to Tool B, back into context, then out to Tool C, leaving duplicate copies. Retrieval risk appears as a secondary warning overlay.

**Option 3 - Wrong Tool Doors**

A hallway of tool doors shows the search system opening two correct doors, missing one needed door, and opening a wrong door. A large payload then jams at the context doorway. This is more cinematic but less source-like.

**Recommendation**

Use **Option 1**. Segment 004 needs to consolidate the three caveats into one clear beat, not split them into three separate subsegments.

---

## Segment 005 - Accuracy Improves, But Retrieval Is Not Magic

Recommended subsegments: `2`

### 005A - Benchmark Improvements

VO coverage: "The accuracy numbers are better, but not magical. Anthropic reported MCP eval improvements from forty-nine percent to seventy-four percent on Opus 4, and from seventy-nine point five to eighty-eight point one percent on Opus 4.5."

**Option 1 - Source-Proof Benchmark Board**

A clipped source-style board shows two benchmark rows. `Opus 4: 49% -> 74%` grows from amber to green. `Opus 4.5: 79.5% -> 88.1%` grows next. The board looks like evidence, not generic hype. After both rows settle, a small amber label appears: "better, not magical."

**Option 2 - Presenter With Metric Cards**

The presenter remains visible while two metric cards slide in beside him, one per model. The cards animate in time with the spoken numbers, then shrink into a larger reliability board.

**Option 3 - Number Transformation**

The numbers themselves animate as physical objects: `49` transforms into `74`, and `79.5` transforms into `88.1`, but both stop short of `100`. This is more visual but less credible.

**Recommendation**

Use **Option 1**. Exact numbers need source-proof treatment.

### 005B - Arcade Stress Test And Reliability Tradeoff

VO coverage: "Then Arcade stress-tested more than four thousand tools and saw retrieval around sixty percent. That is the trade: better context economics, but now search quality is part of your reliability model."

**Option 1 - Deep Tool Library With Reliability Overlay**

The camera flies over a deep field of thousands of tool cards. A search beam tries to retrieve the correct card, and an amber `60%` retrieval ring appears. The field then compresses into a reliability test harness where retrieval quality becomes a scored system metric alongside permissions, latency, and output size.

**Option 2 - Source Badge Plus Stress Field**

Show a source/evidence card for Arcade first, then expand it into a dense tool-library stress field. The `4,000+ tools` and `60%` metrics remain attached as source-style callouts.

**Option 3 - Presenter Tradeoff Interpretation**

Return to the presenter. A green "context economics" object and an amber "retrieval risk" object balance on screen. The presenter explains that the optimization shifts risk into search quality.

**Recommendation**

Use **Option 2** if a source card is available. Otherwise use **Option 1**. This beat should connect the `60%` number directly to reliability.

---

## Segment 006 - Layered Architecture, Not One Universal Tool

Recommended subsegments: `2`

### 006A - Thesis Reset: Not One Universal Answer

VO coverage: "So here is our position. MCP is not dead. Skills are not a replacement for MCP. And CLI scripts are not the universal answer. These are layers."

**Option 1 - Talking Head Thesis Reset**

Return to the presenter full or side-screen. Three overclaims appear and are crossed out: "MCP is dead," "Skills replace MCP," and "CLI solves everything." The crossed-out claims slide away and reveal the principle: "Different layers, different jobs."

**Option 2 - Tool Debate Table**

MCP, Skills, CLI, and Code Execution appear as distinct artifacts around a control table. The camera moves from one to another, making clear that none is the whole answer.

**Option 3 - Layer Stack Begins**

A four-layer stack starts assembling immediately, but each layer is a concrete artifact, not just a rectangle: connector hub, procedure notebook, terminal strip, sandbox runtime.

**Recommendation**

Use **Option 1**, then transition into the layer artifacts. This is a natural place for a human/direct-address reset.

### 006B - Four Layers, Four Jobs

VO coverage: "MCP connects agents to external systems. Skills teach the agent procedures. CLI scripts do deterministic local work. Code execution compresses multi-step workflows. The mistake is forcing one layer to do all four jobs."

**Option 1 - Jobs Route To Matching Layers**

Four layers remain on screen. As each job is spoken, a specific animated object travels to the matching layer: external app cable to MCP, procedure document to Skills, terminal command to CLI, and large intermediate-data workflow to Code Execution. Then all four are briefly pulled into one overloaded layer, which shakes and fails, before returning to the proper layered structure.

**Option 2 - Overloaded Layer Splits Apart**

A single overloaded layer tries to carry all four tasks and visibly strains. It then splits into four specialized layers, and each task moves to the correct place. This is more dramatic and compact.

**Option 3 - Decision Matrix Hold Frame**

A practical matrix appears after the animation: external access -> MCP; procedure -> Skill; deterministic local operation -> CLI; large intermediate data -> Code Execution. This is less cinematic but valuable as a final rule.

**Recommendation**

Use **Option 1**, ending with a brief **Option 3** hold frame. The mistake needs motion; the rule needs readability.

---

## Segment 007 - Cloudflare Code Mode: Search And Execute

Recommended subsegments: `2`

### 007A - Entire API Through Two Tools

VO coverage: "Cloudflare showed the sharpest version of this idea. They took the entire Cloudflare API and exposed it through two tools: search and execute."

**Option 1 - Source Capture With Callouts**

Use the Cloudflare source page or a credible source-style browser frame. Overlay two large callouts: `search` and `execute`. Behind those two tools, the full API catalog appears as a compressed or blurred layer. The viewer sees credibility first, then the abstraction.

**Option 2 - API Catalog Compression**

A massive grid of endpoint cards fills the screen and compresses into two exposed tool cards labeled `search` and `execute`. The endpoint grid remains outside context, still available but not loaded.

**Option 3 - Developer Workbench**

A developer interface shows thousands of endpoints in an API tree, while the active agent tool list contains only `search()` and `execute()`. The cursor hovers over the two exposed tools.

**Recommendation**

Use **Option 1** if we have the source recording. Otherwise use **Option 3** with a source badge.

### 007B - Typed API, Sandbox, Extreme Token Reduction

VO coverage: "Instead of loading thousands of endpoint schemas, the agent writes code against a typed API and runs that code in a sandbox. Their claim is extreme: about one thousand input tokens instead of one point one seven million."

**Option 1 - Code Editor To Sandbox To Metric**

A TypeScript-like editor writes code against a typed Cloudflare API. Autocomplete opens with method signatures. The code block moves into a glowing sandbox/runtime boundary and runs. Then the source metric appears: `1,170,000 input tokens` collapses into `1,000 input tokens`.

**Option 2 - Source Metric First, Then Code Mode**

Highlight the Cloudflare metric on the source page first, then pull the numbers into a dramatic comparison. Behind the numbers, a code editor and sandbox show why the reduction happens.

**Option 3 - Data Flood Diverted**

A flood of endpoint schemas rushes toward context but is diverted by `search` and `execute`. Only a tiny code-mode packet reaches the model. The numbers appear as labels on the flood versus packet.

**Recommendation**

Use **Option 1**, with a source-style metric badge. This keeps the mechanism and payoff in one production beat.

---

## Segment 008 - The New Mental Model

Recommended subsegments: `2`

### 008A - Do Not Pour The Whole API Into Context

VO coverage: "That number matters because it changes the mental model. The agent does not need every API endpoint poured into its context window."

**Option 1 - API Manual Pour Redirected**

A massive API manual made of endpoint pages pours toward the model context. A clean redirect barrier sends most of it into an external searchable library. The context remains mostly empty except for reasoning notes. This directly visualizes the rejected mental model.

**Option 2 - Before/After Workbench**

Left side: old model, endpoint schemas dumped into context. Right side: new model, API docs stay external and context holds only reasoning plus small tool handles. A camera move shifts from cluttered to clean.

**Option 3 - Presenter Between Two Models**

The presenter stands between two floating models: "pour everything in" and "keep capability outside." The better model becomes highlighted as the VO explains the shift.

**Recommendation**

Use **Option 1**. It is memorable and transitions naturally to the four-step workflow.

### 008B - Discover, Inspect, Execute, Return

VO coverage: "It needs a way to discover what exists, inspect what matters, execute the operation, and return the result. The context window should carry reasoning, not every possible instruction manual."

**Option 1 - Four-Step Action Chain**

Create a horizontal chain where each verb is an actual action: Discover uses a search lens over the external library; Inspect opens a relevant documentation snippet; Execute sends code into a sandbox; Return sends a compact result card back to context. The context window remains small and clean throughout.

**Option 2 - Clean Reasoning Context With Rich External Capability**

A small bright model context contains only goal, constraints, selected tools, and decision notes. Around it sit larger external zones: docs, tool registry, execution sandbox, result store. The camera pulls back to show that the system is powerful because everything does not live inside context.

**Option 3 - IDE Walkthrough**

A simulated IDE runs through search registry, open docs, execute sandbox, receive result. This is concrete and controllable.

**Recommendation**

Use **Option 1**, ending on the small-context/rich-capability frame from Option 2.

---

## Segment 009 - Naive Tool Calls Duplicate The Transcript

Recommended subsegments: `2`

### 009A - Google Drive To Salesforce Example

VO coverage: "Anthropic published the same pattern from another angle. Their example is simple: download a meeting transcript from Google Drive and attach it to a Salesforce lead."

**Option 1 - Source Capture First**

Use the Anthropic source page or source-style article frame showing the Google Drive to Salesforce example. The cursor or highlight marks the sentence. The source page then shrinks into an evidence card while the Drive -> model -> Salesforce workflow expands around it.

**Option 2 - Enterprise Workflow Workbench**

A realistic business workflow interface shows a Google Drive document tile labeled "Meeting transcript" on the left, a Salesforce lead record on the right, and an AI assistant context window in the middle. The task label appears at the top: attach transcript to Salesforce lead.

**Option 3 - Talking Head With Workflow Tiles**

The presenter explains while Google Drive and Salesforce tiles appear beside him. A transcript card moves from Drive toward Salesforce and pauses at the model context.

**Recommendation**

Use **Option 1** if the source recording is available. Otherwise use **Option 2**. This named example benefits from credibility.

### 009B - Transcript Crosses Context Twice

VO coverage: "In the naive tool-call path, the transcript enters the model context when it is read, then enters again when the model passes it to Salesforce. The same transcript crosses the model context boundary twice..."

**Option 1 - Two Context Crossings Map**

Show Google Drive on the left, model context in the center, Salesforce on the right. The transcript flows from Drive into context and gets stamped `context hit #1`. Then the same transcript duplicates and flows from context to Salesforce with `context hit #2`. A token meter jumps both times. This is the clearest explanation.

**Option 2 - Transcript Flood In Chat Window**

The transcript enters a chat/context window as a huge block of text, then is copied again when sent to Salesforce. The scroll bar shrinks and the context meter rises twice.

**Option 3 - Toll Booth Metaphor**

The transcript travels through a glowing context toll booth twice, paying token cost each time. This is simple and memorable but less technical.

**Recommendation**

Use **Option 1**. It becomes the "before" lane for Segment `010`.

---

## Segment 010 - Code Execution Keeps Intermediate Data Out

Recommended subsegments: `2`, with an optional third only if the timing needs a separate final comparison.

### 010A - Thinking Versus Transporting

VO coverage: "That is the waste. The model is not thinking about the transcript twice. It is transporting the transcript twice. Anthropic estimates a two-hour sales meeting could add fifty thousand intermediate-result tokens."

**Option 1 - Thinking Panel Versus Transport Path**

Split the screen. Left side shows a compact reasoning panel with a few notes: goal, source, destination, rule. Right side shows the transcript traveling through context twice, producing duplicate token stacks. A counter climbs to `+50,000 intermediate-result tokens`. The message is that the reasoning is small; the transport is large.

**Option 2 - Transcript Timeline Cost Counter**

A two-hour meeting transcript appears as a long timeline. The transcript crosses context twice, and an amber counter climbs to `+50,000`. This is more focused on the numeric claim.

**Option 3 - Presenter Interpretation**

The presenter returns with a small "thinking" note and a massive transcript cargo path beside him. The thinking note stays small while the transport path flashes red.

**Recommendation**

Use **Option 1**. It combines the conceptual distinction and the `+50K` metric in one beat.

### 010B - Runtime Keeps Transcript, Only Status Returns

VO coverage: "With code execution, the transcript stays inside the execution environment as a variable, and only the final status comes back to the model."

**Option 1 - Sandbox Runtime Variable**

A sandbox runtime contains code such as `transcript = drive.download(fileId)` and `salesforce.attach(leadId, transcript)`. The transcript appears as a contained variable object inside the sandbox. The model context sits outside with only the plan and a small handle. When the sandbox finishes, it sends one green result card back: "Done: transcript attached."

**Option 2 - Containment Chamber**

The transcript enters a secure execution chamber and stays there while the operation runs. The model watches from outside and receives only a tiny receipt. This explains the concept without code.

**Option 3 - Terminal Success Output**

A terminal runs the workflow and returns only `success: transcript attached`. The context receives that line and nothing else.

**Recommendation**

Use **Option 1**. It is the clearest bridge between code execution and keeping intermediate data out of context.

### 010C - Optional Final Comparison: Naive Versus Code Execution

Use only if timing supports a third beat.

VO coverage: "Naive tool calls transport the transcript through context twice. Code execution keeps the transcript inside the runtime and sends only the final status back."

**Option 1 - Two-Lane Final Comparison**

Show identical Drive and Salesforce endpoints on both sides. Left lane: naive path, transcript crosses context twice and the meter turns red. Right lane: code execution path, transcript stays inside the sandbox and only a green final status returns. The two lanes make the difference impossible to miss.

**Option 2 - Before/After Swipe**

Start with the naive path full screen. A vertical wipe replaces it with the optimized code-execution path. The transcript route shortens and the context meter drops.

**Recommendation**

Use **Option 1** only if Segment 010 needs a strong section-ending summary. Otherwise fold this comparison into the ending of `010B`.

---

## Revised Production Summary

| Segment | Beats | Recommended Production Shape |
| --- | ---: | --- |
| 002 | 2 | Cinematic workstation: tools wake up, then idle context becomes overhead |
| 003 | 3 | Tool Search steps: minimal load, ranked search, inject + token reduction |
| 004 | 2 | Presenter warning, then three remaining failure modes in one board |
| 005 | 2 | Source-proof benchmark board, then Arcade/reliability tradeoff |
| 006 | 2 | Talking-head thesis reset, then four layers/four jobs |
| 007 | 2 | Cloudflare source/search-execute, then typed API/sandbox/token collapse |
| 008 | 2 | API manual not poured into context, then discover/inspect/execute/return |
| 009 | 2 | Anthropic Drive/Salesforce source, then transcript crosses context twice |
| 010 | 2-3 | Thinking vs transport/+50K, sandbox variable/final status, optional side-by-side |

## Recommended First Decision

Start with the **hybrid chain**:

- Segment `002`: cinematic workstation UI.
- Segment `003`: simulated UI/workbench for precise Tool Search mechanics.

This gives the video a strong visual opening without sacrificing teaching clarity.
