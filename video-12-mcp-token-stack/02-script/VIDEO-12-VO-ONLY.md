# Video 12 VO Only

## 001 — Avatar V Full-Screen

I am the avatar for Dr. Terry Byrd, and we are looking at a problem every serious agent builder has to understand. MCP used to have a brutal problem. You could burn tens of thousands of tokens before you asked the agent to do anything. But in 2026, that story changed. Tool Search, scoped loading, and Code Mode are real improvements. So the question is no longer, "Is MCP bad?" The better question is, "Which layer should do which job?"

## 002 — Hidden Voice

Here is the old failure mode. You connect GitHub, Slack, Sentry, Grafana, Splunk, maybe Jira. Before the user types a task, the model is already carrying tool definitions. That is not work. That is overhead. And overhead is not just money. It is latency, confusion, and less room for the actual problem.

## 003 — Hidden Voice

Anthropic's Tool Search changed the baseline. The workflow is simple, but important. Step one: Claude does not load every tool definition into context. It starts with a tiny search tool, while the full tool library stays outside the reasoning window. Step two: when the task arrives, that search tool looks across the library and selects the few tools that match the job: maybe Jira tasks, Sentry errors, or AWS metrics. Step three: only those relevant tool definitions are injected into the model context. The unrelated tools stay gray and outside the reasoning space. That is the shift: context is loaded on demand, not prepaid upfront. In Anthropic's own example, consumption moves from roughly seventy-seven thousand tokens to about eight point seven thousand. That is a serious improvement.

## 004 — Hidden Voice

But this is where the easy take gets dangerous. If you say, "MCP is fixed now," you miss the next problem. Search reduces schema load. It does not make every tool result small. It does not make every multi-step workflow efficient. And it does not make tool retrieval perfectly reliable.

## 005 — Hidden Voice

The accuracy numbers are better, but not magical. Anthropic reported MCP eval improvements from forty-nine percent to seventy-four percent on Opus 4, and from seventy-nine point five to eighty-eight point one percent on Opus 4.5. Then Arcade stress-tested more than four thousand tools and saw retrieval around sixty percent. That is the trade: better context economics, but now search quality is part of your reliability model.

## 006 — Avatar V Side-Screen

So here is our position. MCP is not dead. Skills are not a replacement for MCP. And CLI scripts are not the universal answer. These are layers. MCP connects agents to external systems. Skills teach the agent procedures. CLI scripts do deterministic local work. Code execution compresses multi-step workflows. The mistake is forcing one layer to do all four jobs.

## 007 — Hidden Voice

Cloudflare showed the sharpest version of this idea. They took the entire Cloudflare API and exposed it through two tools: search and execute. Instead of loading thousands of endpoint schemas, the agent writes code against a typed API and runs that code in a sandbox. Their claim is extreme: about one thousand input tokens instead of one point one seven million.

## 008 — Hidden Voice

That number matters because it changes the mental model. The agent does not need every API endpoint poured into its context window. It needs a way to discover what exists, inspect what matters, execute the operation, and return the result. The context window should carry reasoning, not every possible instruction manual.

## 009 — Hidden Voice

Anthropic published the same pattern from another angle. Their example is simple: download a meeting transcript from Google Drive and attach it to a Salesforce lead. In the naive tool-call path, the transcript enters the model context when it is read, then enters again when the model passes it to Salesforce.

## 010 — Hidden Voice

That is the waste. The model is not thinking about the transcript twice. It is transporting the transcript twice. Anthropic estimates a two-hour sales meeting could add fifty thousand intermediate-result tokens. With code execution, the transcript stays inside the execution environment as a variable, and only the final status comes back to the model.

## 011 — Hidden Voice

The result is the headline number: one hundred fifty thousand tokens down to two thousand. That is a ninety-eight point seven percent reduction. But the important part is not the percentage. The important part is where the data lives. If intermediate data never needs the model's judgment, it should not enter the model's context.

## 012 — Hidden Voice

There is a catch. Anthropic's programmatic tool calling docs say MCP connector tools cannot be called programmatically. That means you cannot simply take every MCP connector and expect programmatic calling to solve it. For MCP-heavy workflows, you need the code-execution wrapper pattern, server-side Code Mode, or another layer that turns tools into callable code inside a controlled runtime.

## 013 — Avatar V Side-Screen

This is also where serious engineers should slow down. Code execution is powerful because the model can write code that touches real tools. That is also why it is dangerous. Cloudflare runs generated code in a V8 isolate with no file system, no environment variables, and external fetch disabled by default. If you cannot provide a real sandbox, you do not get a free token win. You get a new attack surface.

## 014 — Hidden Voice

The lighter-weight fix is scoped MCP. Bright Data is a good example. Their MCP docs expose Rapid mode, Pro mode, and eleven tool groups. You can turn on a group like browser, finance, ecommerce, or code. You can also allowlist specific tools. That is not as dramatic as Code Mode, but for production agents it is often the first sane move.

## 015 — Hidden Voice

Skills solve a different problem. A skill is not a live connector. It is procedural knowledge. It tells the agent how to do a job: what files matter, what commands to run, what patterns to follow, what mistakes to avoid. That kind of knowledge does not belong in a massive always-loaded context file.

## 016 — Hidden Voice

This is why JARVIS uses skills heavily. A video-production skill can say, "Here is how we structure HeyGen blocks. Here is where stills live. Here is how Remotion should treat avatar segments." The model only needs that instruction when it is doing video work. It should not carry it during a market scan or a wiki cleanup.

## 017 — Hidden Voice

Then there is the boring layer that keeps winning: CLI scripts. If a task is deterministic and local, a command-line tool is often cheaper and more reliable than an MCP server. Scalekit measured a simple GitHub repo question at one thousand three hundred sixty-five tokens with CLI, compared with forty-four thousand twenty-six tokens through MCP.

## 018 — Hidden Voice

But the same benchmark makes the important counterpoint. CLI is great when the agent is acting as you, on your machine, with your credentials. If you are building a product where an agent acts for many customers inside many organizations, MCP gives you a permission and audit boundary that CLI does not automatically provide. So the right question is not CLI or MCP. It is: who is the agent acting for?

## 019 — Hidden Voice

The next layer is output filtering. Many tools return too much. A web scrape returns navigation, ads, related links, formatting, and metadata. A search result returns fields the agent never asked for. If the agent only needs title, URL, and price, return title, URL, and price. Every extra field competes with the user's actual task.

## 020 — Hidden Voice

Compact formats like TOON can help, but only in the right shape. TOON is strongest for flat, repetitive, tabular data where JSON repeats the same keys over and over. Independent benchmarks are more cautious than the hype. For small payloads, nested objects, or very wide rows, the instruction overhead and ambiguity can eat the savings.

## 021 — Hidden Voice

Put the stack on one screen. Direct MCP is simple but expensive when schemas and outputs are large. Tool Search reduces idle load. Scoped MCP narrows production surfaces. Skills carry procedure. CLI handles local deterministic work. Code execution keeps intermediate data out of context. Output filtering and compact notation reduce payloads after the call.

## 022 — Avatar V Side-Screen

Here is the rule we use now. If the agent needs permissioned access to an external system, consider MCP. If it needs to know how we do something, use a skill. If it needs to run a local deterministic operation, use a CLI script. If it needs to move or transform a lot of data across steps, use code execution. Do not make one tool carry every job.

## 023 — Hidden Voice

That is the pattern we want in JARVIS. The wiki is memory. Skills are operating procedures. Local scripts are reliable actions. MCP is for permissioned external services. Scheduled jobs create the heartbeat. The agent orchestrates the layers, but it does not need every layer fully loaded in context all the time.

## 024 — Hidden Voice

The next step is measuring it. Pick one real task: look up the current MACD value for QQQ, compare it to last week, and write a one-paragraph report. Run it four ways: naive MCP, Tool Search, the current JARVIS stack with skills plus CLI, and a code-execution version. Capture tokens, latency, reliability, and context used.

## 025 — Hidden Voice

If you are fixing your own setup, start with the free wins. Check your MCP token load. Disconnect servers you do not use. Turn on Tool Search where your client supports it. Scope big MCP servers by group or explicit tool list. You can do that in an hour, and it immediately reduces noise.

## 026 — Hidden Voice

Then move procedural knowledge into skills. Stop stuffing every rule into the main context file. Move deterministic local work into scripts. Filter tool outputs at the source. If the agent only needs three fields, return three fields. Do not make the model carry a full object because the tool was easy to write.

## 027 — Hidden Voice

Only then reach for the heavy patterns. For multi-step workflows with large intermediate data, use programmatic tool calling where it fits. For MCP connector workflows that cannot be called programmatically, use Code Mode or code execution with MCP wrappers. If you do this, sandboxing is not optional. It is the product.

## 028 — Hidden Voice

There are three mistakes we would avoid. First, saying MCP is dead because CLI is cheaper on local tasks. Second, saying MCP is fixed because Tool Search exists. Third, treating compact formats like TOON as a universal compression spell. The winning stack is boring: right layer, right scope, measured output.

## 029 — Hidden Voice

The reason this video matters is that the debate is moving from opinions to evidence. Cloudflare has the one-thousand-token API. Anthropic has Tool Search and code execution numbers. Arcade has a four-thousand-tool stress test. Scalekit has CLI versus MCP cost and failure data. JARVIS gives us a place to test the stack on real work.

## 030 — Hidden Voice

Before the closing summary, take a second to subscribe, hit the like button, and ring the notification bell for the next video. This channel is building a practical library around agentic AI, automation, and real systems like JARVIS. The more feedback we get, the better these walkthroughs become.

## 031 — Avatar V Full-Screen

So the answer is not "skills beat MCP." The answer is that MCP is one layer in a larger agent architecture. Use Tool Search to avoid loading everything. Use scoped MCP to narrow production access. Use skills for procedures. Use CLI for local deterministic work. Use code execution when intermediate data should stay out of the model.

## 032 — Avatar V Full-Screen

If you build agents, do not ask which integration is fashionable. Ask where the tokens go, where the data lives, and who the agent is acting for. That is the 2026 token stack. New videos every week.
