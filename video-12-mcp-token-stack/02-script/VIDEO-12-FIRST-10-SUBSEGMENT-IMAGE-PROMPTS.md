# Video 12 First 10 Segments: Sub-Segment Image Prompts

Purpose: break segments 002-010 into visual sub-segments where each image gives evidence for the spoken idea. Segment 001 is skipped because it is a talking-head opener.

Global style for all images:

- Format: 16:9, 3840x2160 or 1920x1080.
- Tone: premium engineering documentary, crisp, evidence-first, high contrast, readable at video scale.
- Use a dark neutral workspace background with restrained accent colors: electric blue for discovery/search, green for savings, amber for warnings, red for waste.
- Text must be large and minimal. Use numbers, labels, and short phrases only.
- Prefer real artifact language: browser chrome, terminal panels, token meters, source badges, file cards, API panels, workflow arrows.
- If using brand logos, use clean app tiles with labels. If official logo use is not available, use simple labeled tiles: GitHub, Slack, Sentry, Grafana, Splunk, Jira, Google Drive, Salesforce.
- Avoid generic network-node wallpaper. Every image should have one clear visual claim.

## Segment 002 - Old Failure Mode: Tool Definitions Before Work

Voiceover:
"Here is the old failure mode. You connect GitHub, Slack, Sentry, Grafana, Splunk, maybe Jira. Before the user types a task, the model is already carrying tool definitions. That is not work. That is overhead. And overhead is not just money. It is latency, confusion, and less room for the actual problem."

### 002-A - Connected Tools Before the Task

Image prompt:
Create a polished engineering documentary graphic showing a central AI context window connected to six large app tiles labeled GitHub, Slack, Sentry, Grafana, Splunk, and Jira. The tiles should be arranged across a colorful but controlled page, each sending thick streams of small "schema" cards into the context window. At the bottom, show an empty user prompt box labeled "User task has not started yet." The core message should be obvious: integrations are connected before any actual work begins. Use crisp UI glass panels, large readable labels, dark background, electric blue connection lines, 16:9.

### 002-B - 55,000 Tokens of Idle Context

Image prompt:
Create a token accounting dashboard titled "Context Memory Before the Task." Show a stacked token meter filling to 55,000 tokens. Break the stack into labeled bands: GitHub tool definitions, Slack tool definitions, Sentry tool definitions, Grafana tool definitions, Splunk tool definitions, Jira tool definitions. The meter should dominate the image, with a small empty problem space squeezed to the side labeled "Actual problem: not loaded yet." Make it feel like a serious observability dashboard, readable numbers, dark theme, amber warning edge, 16:9.

### 002-C - Overhead Is Not Just Money

Image prompt:
Create a dramatic but clean visual metaphor for overhead spilling out of an AI context window. From an overfilled context panel, show four types of spillover: dollar bills labeled "cost," stopwatch icons labeled "latency," tangled arrows labeled "confusion," and a shrinking white workspace labeled "less room for the real problem." The image should feel analytical, not cartoonish: premium 3D UI panels, controlled lighting, red and amber warning accents, 16:9.

### 002-D - Context Window Crowded Before Reasoning

Image prompt:
Create a split-screen composition. Left side: a clean user question waiting in an input box. Right side: an overloaded model context window packed with tiny tool schema cards and API method blocks. Add a large label across the top: "Before the model thinks." The user question should be visually blocked by the pile of schemas, making clear that idle tool definitions are competing with reasoning space. Dark interface, sharp typography, 16:9.

## Segment 003 - Tool Search Changes the Baseline

Voiceover:
"Anthropic's Tool Search changed the baseline. The workflow is simple, but important. Step one: Claude does not load every tool definition into context. It starts with a tiny search tool, while the full tool library stays outside the reasoning window. Step two: when the task arrives, that search tool looks across the library and selects the few tools that match the job: maybe Jira tasks, Sentry errors, or AWS metrics. Step three: only those relevant tool definitions are injected into the model context. The unrelated tools stay gray and outside the reasoning space. That is the shift: context is loaded on demand, not prepaid upfront. In Anthropic's own example, consumption moves from roughly seventy-seven thousand tokens to about eight point seven thousand. That is a serious improvement."

### 003-A - Step 1: Minimal Initial Load

Image prompt:
Create a clean technical dashboard showing Step 1 of on-demand context injection. The model context window contains only one compact card labeled "Tool Search." A large searchable tool library sits outside the context boundary in faded gray, with Slack, GitHub, Sentry, Jira, AWS, and other tool cards visible but not loaded. Add a small badge: "Minimal initial load." Do not show selected tools loaded yet. Premium dark technical style, readable labels, 16:9.

### 003-B - Step 2: Search Selects Relevant Tools

Image prompt:
Create Step 2 of the workflow. Show the Tool Search card inside the model context window projecting a focused blue search beam into the faded tool library. Only three matching cards are highlighted in blue/green: "Jira Task," "Sentry Error," and "AWS Metrics." Unrelated tools remain gray. The selected tools are highlighted but not yet loaded into the context window. Add a label: "Select relevant tools." Engineering product explainer style, dark UI, 16:9.

### 003-C - Step 3: Inject Only What Matched

Image prompt:
Create Step 3 of the workflow, using 003C as the style guide. Show the three selected cards from Step 2 moving into a glowing green "Model Context Window" labeled "Loaded relevant tools." The cards should be Jira Task, Sentry Error, and AWS Metrics. All unrelated tools remain outside the context boundary in faded gray. Add a label: "Context injected on demand." Do not include the 77K-to-8.7K meter yet. Premium technical explainer, 16:9.

### 003-D - 77K Down to 8.7K

Image prompt:
Create a payoff frame after the three-step workflow. Left side: old upfront schema loading, a tall red meter labeled "77,000 tokens." Right side: Tool Search with on-demand injection, a shorter green meter labeled "8,700 tokens." Between them, show a compression arrow labeled "load only what matches." Add a small footer: "Schema load reduced, not every problem solved." This should foreshadow Segment 004 without turning into Segment 004. Crisp dashboard style, source-proof feeling, 16:9.

## Segment 004 - Search Helps, But It Does Not Fix Everything

Voiceover:
"But this is where the easy take gets dangerous. If you say, 'MCP is fixed now,' you miss the next problem. Search reduces schema load. It does not make every tool result small. It does not make every multi-step workflow efficient. And it does not make tool retrieval perfectly reliable."

### 004-A - The Dangerous Easy Take

Image prompt:
Create a bold warning-card image with a large statement in the center: "MCP is fixed now?" Put a yellow caution outline around the claim, with a smaller label beneath: "Incomplete conclusion." Behind it, show a clean token reduction chart partially visible, implying the claim came from real improvement but overreaches. Use premium technical presentation style, dark background, amber caution, 16:9.

### 004-B - Tool Results Can Still Be Huge

Image prompt:
Create a visual of a small tool schema card on the left leading to a massive returned payload on the right. The payload should look like an overlong JSON/document result filling the screen with fields, metadata, links, and text blocks. Label the left "Small schema" and the right "Large result." The result panel should push into the model context boundary, showing that output size still matters. Dark UI, red payload accents, 16:9.

### 004-C - Multi-Step Workflows Still Copy Data

Image prompt:
Create a workflow diagram with three tools connected in a chain. A large data object moves from Tool A into the model context, then back out to Tool B, then into context again before Tool C. Show duplicate copies of the same data blob stacking up. Label the duplication "intermediate data copied through context." Make it visually clear that search did not solve workflow transport waste. Clean engineering diagram, 16:9.

### 004-D - Search Quality Becomes Reliability

Image prompt:
Create a tool retrieval board where a search query points toward a library of tool cards. Two correct tools are highlighted green, one important missing tool is outlined red, and one irrelevant tool is highlighted amber. Add the top label "Search quality is now part of reliability." Use a sober evaluation-board style with confidence scores beside cards. Dark background, crisp readable labels, 16:9.

## Segment 005 - Accuracy Improves, But Retrieval Is Not Magic

Voiceover:
"The accuracy numbers are better, but not magical. Anthropic reported MCP eval improvements from forty-nine percent to seventy-four percent on Opus 4, and from seventy-nine point five to eighty-eight point one percent on Opus 4.5. Then Arcade stress-tested more than four thousand tools and saw retrieval around sixty percent. That is the trade: better context economics, but now search quality is part of your reliability model."

### 005-A - Anthropic Eval Improvement Board

Image prompt:
Create a benchmark board with two clean progress rows. Row one: "Opus 4 MCP eval: 49% -> 74%" with a bar growing from red/orange to green. Row two: "Opus 4.5 MCP eval: 79.5% -> 88.1%" with a smaller but clear green improvement. Use source-proof styling: document crop frame, citation badge style, metric callouts. The message should be improvement without hype. Dark dashboard, 16:9.

### 005-B - Arcade 4,000+ Tool Stress Test

Image prompt:
Create a dense tool-library stress-test visual: thousands of tiny tool cards receding into depth, with a search beam trying to retrieve the right card. In the foreground, show a large metric: "4,000+ tools" and "retrieval around 60%." Make the 60% feel cautionary, not catastrophic: amber progress ring, evaluation grid, dark technical style, 16:9.

### 005-C - Better Economics, New Reliability Risk

Image prompt:
Create a tradeoff scale. Left side: green token savings labeled "better context economics." Right side: amber reliability meter labeled "search quality risk." The scale should be balanced rather than one side winning. Behind it, show a context window that is cleaner but a retrieval board with uncertain matches. Professional engineering strategy visual, 16:9.

### 005-D - Reliability Model Includes Retrieval

Image prompt:
Create an architecture reliability diagram with four checklist items: permissions, latency, tool output size, retrieval quality. The first three are familiar gray checks; "retrieval quality" is newly highlighted in blue and amber. Show a small search icon feeding into a reliability score panel. The image should communicate that search moved from optimization feature to system reliability concern. Dark UI, 16:9.

## Segment 006 - Layered Architecture, Not One Universal Tool

Voiceover:
"So here is our position. MCP is not dead. Skills are not a replacement for MCP. And CLI scripts are not the universal answer. These are layers. MCP connects agents to external systems. Skills teach the agent procedures. CLI scripts do deterministic local work. Code execution compresses multi-step workflows. The mistake is forcing one layer to do all four jobs."

### 006-A - Four Layers, Four Jobs

Image prompt:
Create a clean vertical stack diagram with four large layers: MCP, Skills, CLI Scripts, Code Execution. Add one short job label per layer: "external systems," "procedures," "local deterministic work," "multi-step compression." Keep the layers distinct with different accent colors, not a single-hue palette. Leave space on the right for an avatar side-screen if used in edit. Premium technical architecture style, 16:9.

### 006-B - MCP Is Not Dead

Image prompt:
Create a calm myth-versus-reality board. Left side shows three crossed-out overclaims: "MCP is dead," "Skills replace MCP," "CLI solves everything." Right side shows the corrected principle: "Use the right layer for the job." Under the principle, show four small icons representing connector, procedure, terminal, and sandbox. Elegant, readable, not comedic, 16:9.

### 006-C - Forcing One Layer to Do Everything

Image prompt:
Create a visual metaphor of a single overloaded tool layer trying to carry four mismatched tasks: external app access, procedural instructions, terminal commands, and data transformation. The layer is bending under the weight, with warning stress lines. Beside it, show the same tasks distributed cleanly across four layers, stable and organized. Technical 3D UI style, 16:9.

### 006-D - Layer Selection Decision Surface

Image prompt:
Create a decision matrix with columns "Need" and "Best layer." Rows: permissioned external access -> MCP; know how we do it -> Skill; repeatable local operation -> CLI; large intermediate data -> Code Execution. Use large type, subtle icons, and a blue highlight moving down the rows. This should feel like a practical engineering rule card, 16:9.

## Segment 007 - Cloudflare Code Mode: Search and Execute

Voiceover:
"Cloudflare showed the sharpest version of this idea. They took the entire Cloudflare API and exposed it through two tools: search and execute. Instead of loading thousands of endpoint schemas, the agent writes code against a typed API and runs that code in a sandbox. Their claim is extreme: about one thousand input tokens instead of one point one seven million."

### 007-A - Entire API Through Two Tools

Image prompt:
Create a source-style technical graphic showing a huge Cloudflare API catalog compressed behind two large tool cards: "search" and "execute." Thousands of endpoint tiles sit behind the two cards, not inside the context window. Add a small Cloudflare source badge style. The image should make the abstraction obvious: many endpoints, two exposed tools. Dark browser/document composition, orange and blue accents, 16:9.

### 007-B - Agent Writes Code Against Typed API

Image prompt:
Create a code editor scene with typed API autocomplete visible. The code should be generic and readable, like `await cloudflare.zones.search(...)` and `await execute(plan)`, without needing full correctness. Show the agent's plan as a small side panel and a sandbox run button below. The mood should be serious developer workflow, with crisp TypeScript-style syntax highlighting, 16:9.

### 007-C - Sandbox Execution Boundary

Image prompt:
Create a sandbox boundary diagram. Inside a glowing isolated runtime box, show generated code running against typed API calls. Outside the box, show the model context with only a small request and final result, not all endpoint schemas. Label the boundary "sandbox." Use strong spatial separation and secure-runtime visual language, 16:9.

### 007-D - 1.17 Million to 1,000 Tokens

Image prompt:
Create an extreme metric comparison image. Left side: an enormous red column labeled "1,170,000 input tokens" stretching almost off-screen. Right side: a tiny green column labeled "1,000 input tokens." Between them, show a label "Code Mode pattern." Make the scale difference visually shocking but clean, with no clutter. Dark premium metric ticker style, 16:9.

## Segment 008 - The New Mental Model: Discover, Inspect, Execute, Return

Voiceover:
"That number matters because it changes the mental model. The agent does not need every API endpoint poured into its context window. It needs a way to discover what exists, inspect what matters, execute the operation, and return the result. The context window should carry reasoning, not every possible instruction manual."

### 008-A - Do Not Pour the Whole API Into Context

Image prompt:
Create a vivid engineering metaphor: a massive API manual made of endpoint cards being poured toward a model context window, but a clean barrier redirects most of it into an external searchable library. The context window remains clean, with only reasoning notes inside. Label the overloaded path "old mental model" and the clean path "new mental model." Dark premium style, 16:9.

### 008-B - Discover, Inspect, Execute, Return

Image prompt:
Create a four-step horizontal workflow: Discover -> Inspect -> Execute -> Return. Each step has a distinct visual: magnifying glass over API library, highlighted documentation snippet, sandbox code run, final result card. Keep all intermediate detail outside the model context until the final result. Use blue-to-green progression, large labels, 16:9.

### 008-C - Reasoning Belongs in Context

Image prompt:
Create a split composition. Left side: a clean model context panel containing reasoning bullets, constraints, and final decision notes. Right side: a huge instruction manual / API catalog stored outside the context in a searchable shelf. Add a headline: "Context carries reasoning, not every manual." Make the context panel feel spacious and calm. Technical editorial style, 16:9.

### 008-D - Minimal Context, Rich External Capability

Image prompt:
Create an architecture image with a small bright model context in the center, connected to large external capability layers: API docs, tool registry, execution sandbox, result store. The context stays small while the surrounding system is rich. Use a restrained, modern systems-design look with clear labels and no tiny text. 16:9.

## Segment 009 - Naive Tool Calls Duplicate the Transcript

Voiceover:
"Anthropic published the same pattern from another angle. Their example is simple: download a meeting transcript from Google Drive and attach it to a Salesforce lead. In the naive tool-call path, the transcript enters the model context when it is read, then enters again when the model passes it to Salesforce."

### 009-A - Google Drive to Salesforce Task

Image prompt:
Create a clear workflow image showing a Google Drive document tile labeled "Meeting transcript" on the left and a Salesforce lead record card on the right. Between them, show an AI assistant context window. The task label at the top: "Attach transcript to Salesforce lead." Use app-style tiles with labels, clean enterprise workflow aesthetics, 16:9.

### 009-B - Transcript Enters Context When Read

Image prompt:
Create a close-up of the first naive step. A large transcript document flows from Google Drive into the model context window. Inside the context, show the transcript as many stacked text pages taking up most of the available space. Label it "Read from Drive -> transcript enters context." Use a red/amber token meter rising as the transcript enters, 16:9.

### 009-C - Transcript Enters Context Again When Passed

Image prompt:
Create the second naive step. The same transcript document is shown duplicated inside the model context, then pushed outward to a Salesforce lead record. Show two identical transcript stacks in context with a label "same data, second pass." Add a token meter jumping again. This should visually prove the duplication. Dark enterprise UI, 16:9.

### 009-D - Naive Path Has Two Context Crossings

Image prompt:
Create a two-lane data-flow diagram titled "Naive tool-call path." Lane one: Google Drive -> Model Context, with transcript blob crossing boundary. Lane two: Model Context -> Salesforce, with the same transcript blob crossing boundary again. Mark each boundary crossing with a red token-cost stamp: "context hit #1" and "context hit #2." Clean motion-ready design, 16:9.

## Segment 010 - Code Execution Keeps Intermediate Data Out

Voiceover:
"That is the waste. The model is not thinking about the transcript twice. It is transporting the transcript twice. Anthropic estimates a two-hour sales meeting could add fifty thousand intermediate-result tokens. With code execution, the transcript stays inside the execution environment as a variable, and only the final status comes back to the model."

### 010-A - Thinking vs Transporting

Image prompt:
Create a split-screen comparison. Left side labeled "Thinking" shows a compact reasoning panel with a few decision bullets. Right side labeled "Transporting" shows the transcript blob being carried back and forth through context, creating duplicate token stacks. Put a large X over the duplicate transport path. The central message: the model does not need to think about the transcript twice. Premium technical style, 16:9.

### 010-B - 50,000 Intermediate-Result Tokens

Image prompt:
Create a metric image for a two-hour sales meeting transcript. Show a transcript timeline bar labeled "2-hour sales meeting" feeding into a large amber token counter: "+50,000 intermediate-result tokens." Surround the counter with duplicate document fragments and small context-boundary stamps. Make it feel like a cost report from an engineering benchmark, 16:9.

### 010-C - Transcript Stays as a Variable

Image prompt:
Create a code execution scene. Inside a sandboxed runtime, show a code editor with a highlighted line like `const transcript = await drive.download(fileId);` and a second line attaching it to Salesforce. The transcript appears as a contained variable object inside the runtime, not entering the model context. Outside the sandbox, the model context remains small. Crisp developer UI, 16:9.

### 010-D - Only Final Status Comes Back

Image prompt:
Create a final optimized workflow image. Google Drive and Salesforce are connected through a sandbox box that holds the transcript internally. From the sandbox back to the model context, show only one small green result card: "Done: transcript attached." The context token meter remains tiny. Add a calm success accent, green highlight, premium engineering documentary style, 16:9.

### 010-E - Naive vs Code Execution Side by Side

Image prompt:
Create a side-by-side comparison. Left lane: naive path, transcript crosses the model context boundary twice, token meter high and red. Right lane: code execution path, transcript remains inside sandbox as `transcript`, only final status returns, token meter low and green. Use identical source and destination tiles so the difference is the data path. Large readable labels, 16:9.
