# Video 12 First 10 Segments: VO Sub-Segments

Purpose: divide the original VO from segments 002-010 so each spoken chunk lines up with the matching image prompt in `VIDEO-12-FIRST-10-SUBSEGMENT-IMAGE-PROMPTS.md`.

Segment 001 is skipped because it is a talking-head opener.

## Segment 002 - Old Failure Mode: Tool Definitions Before Work

### 002-A - Connected Tools Before the Task

Here is the old failure mode. You connect GitHub, Slack, Sentry, Grafana, Splunk, maybe Jira.

### 002-B - 55,000 Tokens of Idle Context

Before the user types a task, the model is already carrying tool definitions.

### 002-C - Overhead Is Not Just Money

That is not work. That is overhead. And overhead is not just money.

### 002-D - Context Window Crowded Before Reasoning

It is latency, confusion, and less room for the actual problem.

## Segment 003 - Tool Search Changes the Baseline

### 003-A - Step 1: Minimal Initial Load

Anthropic's Tool Search changed the baseline. The workflow is simple, but important. Step one: Claude does not load every tool definition into context. It starts with a tiny search tool, while the full tool library stays outside the reasoning window.

### 003-B - Step 2: Search Selects Relevant Tools

Step two: when the task arrives, that search tool looks across the library and selects the few tools that match the job: maybe Jira tasks, Sentry errors, or AWS metrics.

### 003-C - Step 3: Inject Only What Matched

Step three: only those relevant tool definitions are injected into the model context. The unrelated tools stay gray and outside the reasoning space. That is the shift: context is loaded on demand, not prepaid upfront.

### 003-D - 77K Down to 8.7K

In Anthropic's own example, consumption moves from roughly seventy-seven thousand tokens to about eight point seven thousand. That is a serious improvement.

## Segment 004 - Search Helps, But It Does Not Fix Everything

### 004-A - The Dangerous Easy Take

But this is where the easy take gets dangerous. If you say, "MCP is fixed now," you miss the next problem.

### 004-B - Tool Results Can Still Be Huge

Search reduces schema load. It does not make every tool result small.

### 004-C - Multi-Step Workflows Still Copy Data

It does not make every multi-step workflow efficient.

### 004-D - Search Quality Becomes Reliability

And it does not make tool retrieval perfectly reliable.

## Segment 005 - Accuracy Improves, But Retrieval Is Not Magic

### 005-A - Anthropic Eval Improvement Board

The accuracy numbers are better, but not magical. Anthropic reported MCP eval improvements from forty-nine percent to seventy-four percent on Opus 4, and from seventy-nine point five to eighty-eight point one percent on Opus 4.5.

### 005-B - Arcade 4,000+ Tool Stress Test

Then Arcade stress-tested more than four thousand tools and saw retrieval around sixty percent.

### 005-C - Better Economics, New Reliability Risk

That is the trade: better context economics,

### 005-D - Reliability Model Includes Retrieval

but now search quality is part of your reliability model.

## Segment 006 - Layered Architecture, Not One Universal Tool

### 006-A - Four Layers, Four Jobs

So here is our position. MCP is not dead. Skills are not a replacement for MCP. And CLI scripts are not the universal answer.

### 006-B - MCP Is Not Dead

These are layers.

### 006-C - Forcing One Layer to Do Everything

MCP connects agents to external systems. Skills teach the agent procedures. CLI scripts do deterministic local work. Code execution compresses multi-step workflows.

### 006-D - Layer Selection Decision Surface

The mistake is forcing one layer to do all four jobs.

## Segment 007 - Cloudflare Code Mode: Search and Execute

### 007-A - Entire API Through Two Tools

Cloudflare showed the sharpest version of this idea. They took the entire Cloudflare API and exposed it through two tools: search and execute.

### 007-B - Agent Writes Code Against Typed API

Instead of loading thousands of endpoint schemas, the agent writes code against a typed API.

### 007-C - Sandbox Execution Boundary

And runs that code in a sandbox.

### 007-D - 1.17 Million to 1,000 Tokens

Their claim is extreme: about one thousand input tokens instead of one point one seven million.

## Segment 008 - The New Mental Model: Discover, Inspect, Execute, Return

### 008-A - Do Not Pour the Whole API Into Context

That number matters because it changes the mental model. The agent does not need every API endpoint poured into its context window.

### 008-B - Discover, Inspect, Execute, Return

It needs a way to discover what exists, inspect what matters, execute the operation, and return the result.

### 008-C - Reasoning Belongs in Context

The context window should carry reasoning,

### 008-D - Minimal Context, Rich External Capability

not every possible instruction manual.

## Segment 009 - Naive Tool Calls Duplicate the Transcript

### 009-A - Google Drive to Salesforce Task

Anthropic published the same pattern from another angle. Their example is simple: download a meeting transcript from Google Drive and attach it to a Salesforce lead.

### 009-B - Transcript Enters Context When Read

In the naive tool-call path, the transcript enters the model context when it is read,

### 009-C - Transcript Enters Context Again When Passed

then enters again when the model passes it to Salesforce.

### 009-D - Naive Path Has Two Context Crossings

The same transcript crosses the model context boundary twice: once from Google Drive into the model, and once from the model into Salesforce.

## Segment 010 - Code Execution Keeps Intermediate Data Out

### 010-A - Thinking vs Transporting

That is the waste. The model is not thinking about the transcript twice.

### 010-B - 50,000 Intermediate-Result Tokens

It is transporting the transcript twice. Anthropic estimates a two-hour sales meeting could add fifty thousand intermediate-result tokens.

### 010-C - Transcript Stays as a Variable

With code execution, the transcript stays inside the execution environment as a variable,

### 010-D - Only Final Status Comes Back

and only the final status comes back to the model.

### 010-E - Naive vs Code Execution Side by Side

Naive tool calls transport the transcript through context twice. Code execution keeps the transcript inside the runtime and sends only the final status back.
