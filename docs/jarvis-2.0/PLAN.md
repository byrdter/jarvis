# JARVIS 2.0: One Brain, Many Bodies

*Drafted 2026-11-07 (travel week), revised 2026-11-08 after Terry's decisions. Status: PLAN, nothing built yet.*

**Direction (Terry, 2026-11-08):** agentic AI engineering is THE focus, broadly defined. That means:
- *Using* dark factories to ship apps
- Cloning apps
- Team and organization brains
- Local LLMs replacing paid services
- Testing open models and reporting the findings
- Outsourcing specialist work to open agents (Hermes, OpenClaw)

Other lanes get archived during the reorganization. JARVIS is both the tool and the test bench.
See §10.

**Decided 2026-11-08:**
- Home Mac mini = **32 GB**.
- Brain = **private GitHub repo**, with memory leaving Dropbox (migration script comes after the repo exists).
- Phone channel = **Telegram** for now.
- **Cloud server = yes**, and it doubles as the lab.
- Private domains get decided at local-brain setup.

The goal: talk to JARVIS from anywhere (phone, terminal, desktop, voice) and get the same brain,
the same memory and the same personality. It should keep working when the home machine is off, and
it should get good at any topic quickly.

---

## 0. Where we actually are (measured 2026-11-07)

| Piece | State |
|---|---|
| Brain call | `agent-sdk/src/claude-wrapper.ts` spawns the `claude` CLI on the subscription (good, and still allowed; see §1) |
| Server | Bun server + heartbeat + daily reflection (Phase 3A/3B) **not running on the new Mac**: no JARVIS launchd jobs in `~/Library/LaunchAgents` |
| Telegram | Phase 10 remote-terminal code exists (`src/remote-terminal.ts`); never deployed |
| Memory | Split three ways: `jarvis-private/context/` (markdown), Claude auto-memory (69 files), `bd` memories; vector index in a local DB |
| Sync | Dropbox only. Works between Macs, does **not** work for a cloud server |
| Phase state file | Stale since April (`project_jarvis_phase_state.md` still says "Phase 8 just shipped") |

The honest diagnosis: the pieces were built, but JARVIS only lives inside a terminal on whichever
Mac is open. The upgrade is mostly wiring and hosting, plus one cleanup of memory.

---

## 1. The subscription question (answer)

**Running the official `claude` CLI (`claude -p`) or the Claude Agent SDK while signed in with
your Claude plan still draws from your subscription limits.** It is not billed at API rates.
Source: Anthropic's help article "Use the Claude Agent SDK with your Claude plan," updates of
2026-06-15 and 2026-10-07.

What happened:
- **Announced spring 2026:** starting June 15, `claude -p`, the Agent SDK and third-party apps
  would leave subscription limits and move to a monthly credit metered at API rates. A lot of
  commentary from that window treats it as fact. (None of the 26 videos you sent actually says
  it. Cole ran his brain on Codex and Kimi "for the sake of testing," and argues the harness and
  model should be swappable. Zubair pays API rates by choice, so JARVIS gets a separate bill.)
- **June 15, 2026:** paused the day it was due. "Nothing has changed."
- **October 6–7, 2026:** briefly re-announced, then the page was revised. Final text: Max, Ultra
  and Team plans now *also* include monthly API credits, which apply when you run the SDK /
  `claude -p` **with a Console API key**. Signed in with the plan, they still use subscription limits.

What this means for JARVIS:
1. Keep `claude -p` / Agent SDK on the subscription as the main brain. It is the cheapest
   option and it is allowed for personal use.
2. **Do not hard-wire it.** Anthropic has tried to change this twice in six months. Put every LLM
   call behind one adapter (§5.1) so the brain can switch in a config line to: Console API key
   (the Max credits) → Codex CLI on the ChatGPT subscription (Cole's choice, for the same
   reason) → a local model on the home Mac.
3. Stay inside the rules: use the official CLI/SDK only, for yourself only. Never pull the OAuth
   token into a third-party harness, and never offer the login to anyone else. The January 2026
   crackdown hit exactly that pattern.

---

## 2. The architecture in one picture

```
             MOUTHS (how you talk)                     BODIES (where it runs)
  ┌──────────────────────────────────────┐   ┌────────────────────────────────────┐
  │ Claude app (phone) → Remote Control   │──▶│ A. Laptop  (Claude Code, travel)   │
  │ Telegram / Discord → Channels         │──▶│ B. Home Mac (always on, local LLM) │
  │ Voice web page (PWA) on phone         │──▶│ C. Cloud VPS (always on, fallback) │
  │ Terminal / Desktop Code tab           │   │ D. Anthropic cloud (Routines, web) │
  └──────────────────────────────────────┘   └───────────────┬────────────────────┘
                                                             │ all read/write
                                     ┌───────────────────────▼──────────────────┐
                                     │  ONE BRAIN (the shared memory)            │
                                     │  • brain repo: private Git (markdown)     │
                                     │  • Postgres + pgvector (Supabase)         │
                                     │  • secrets: 1Password / Doppler           │
                                     └──────────────────────────────────────────┘
               Network glue: Tailscale (every body on one private network)
```

**The rule that makes it one JARVIS:** bodies are disposable, the brain is not. A body holds no
memory of its own. It pulls the brain at the start of a task and pushes what it learned at the
end. Any body can die and nothing is lost.

---

## 3. Phase 3C: Talk from anywhere (do now, while traveling)

Cheapest wins first. All four run on the existing subscription.

| # | Mouth | What it gives you | Needs |
|---|---|---|---|
| 1 | **Remote Control** (`/remote-control`, or the setting in the desktop app) | Drive a live Claude Code session on a Mac from the Claude phone app, with full JARVIS context | The Mac awake. Works today. |
| 2 | **Channels + Telegram plugin** (`/plugin install telegram@claude-plugins-official`, start with `--channels`) | Text or voice-note JARVIS in Telegram, and JARVIS can message you first (alerts, briefings) | A Claude Code session kept running (tmux/launchd) on an always-on body |
| 3 | **Routines** (scheduled cloud agents) | Morning briefing, ETF stage scan, stop-loss guard, monthly tracker run in Anthropic's cloud with the Mac off | Brain repo on GitHub (§6) |
| 4 | **Claude Code on the web / mobile** | Start a cloud session against the brain repo from the phone | Brain repo on GitHub |

Channels replaces most of the hand-built Phase 10 bot. Keep `remote-terminal.ts` only for things
Channels cannot do. Retire the rest; don't maintain two Telegram bots.

**Before trusting any of this:** check on Anthropic's docs which plan tiers have Channels (the
research preview had limits) and that it works under a non-interactive launch.

---

## 4. Body C: the cloud clone (always on)

### Recommendation: one small VPS, plus Anthropic-native cloud for scheduled work

| Option | Cost/mo | Verdict |
|---|---|---|
| **Hetzner Cloud CPX31/CAX31** (4–8 vCPU, 8–16 GB, Ashburn/Hillsboro) | ~$15–20 | **Pick this.** Sized up from the minimum because it also hosts the lab: the factory, Hermes and OpenClaw (§10). x86 (CPX) if any lab tool lacks ARM builds |
| Hostinger KVM2 | ~$10–15 | What Cole's factory videos use (sponsored), so his walkthrough applies step for step |
| DigitalOcean / Vultr droplet, 4 GB | ~$24 | Same idea, friendlier console, double the price |
| Fly.io / Railway (containers) | $5–20 | Good for the Bun server alone; awkward for a long-lived interactive Claude session |
| Anthropic Routines + web sessions | $0 extra | Use for **scheduled** jobs regardless. Not a chat endpoint by itself |
| Supabase (Postgres + pgvector) | $0 free → $25 Pro | The shared database for every body. Already the Phase 4 plan |
| Cloudflare Tunnel / Tailscale Funnel | $0 | Exposes the voice page to the phone without opening ports |
| Mac mini at home *as* the server | power only | The home machine (Body B) can be the always-on body. The VPS is the fallback for when it's off |

### VPS build list
1. Ubuntu 24.04, non-root user, SSH keys only, `ufw` deny-all, **Tailscale** (no public ports).
2. Install Node/Bun, `git`, `claude`. Run `claude setup-token` for a long-lived subscription token,
   kept in a root-only env file, never in the repo.
3. Clone the brain repo. Run the JARVIS Bun server + one Claude Code session with the Telegram
   channel, both under `systemd` with auto-restart.
4. **Least privilege:** the cloud body gets read-only market data, Gmail drafts (not send), no
   brokerage keys. Trades stay human-in-the-loop on the home Mac (CLAUDE.md principle 4).
5. Cost-guard: a daily usage check that pages you on Telegram if subscription usage spikes.

---

## 5. Body B: the home local brain (plan now, build when home)

**Which machine is at home? Its chip and memory decide everything below.** Memory sets the size
of the local model. Rule of thumb: 4-bit models need about 0.6 GB per billion parameters, plus 30%
headroom.

| Home Mac memory | Local brain (Ollama/MLX) | Role |
|---|---|---|
| 16 GB | Qwen 3.5 9B | Small talk, offline note lookup; Claude does real thinking |
| 32 GB | Qwen 3.8 27B or Gemma 4 26B-A4B | Real local assistant; good everyday default |
| 64 GB | Gemma 4 31B + vision model + embeddings, all resident | Comfortable; same class as this M5 Pro laptop |
| 96–128 GB+ | gpt-oss-120b / Llama 4 Scout | Near-cloud quality at home |

**Terry's home Mac mini has 32 GB, which is the 32 GB row.** What that means in practice:
- **Main local brain:** Qwen 3.8 27B (~17 GB) *or* Gemma 4 26B-A4B (~18 GB, faster, 256K context).
  Only one fits at a time alongside the voice and listening engines.
- **Small model kept loaded:** Qwen 3.5 9B for quick chat and routing.
- **Embeddings:** `nomic-embed-text` (tiny).
- **Not a fit here:** gpt-oss-120b-class models. That's what the 64 GB travel M5 Pro is for, so it
  becomes the test bench for bigger open models when we report on them.

Ollama loads one large model at a time, so the first reply after switching models is slow.

### Local stack
- **Brain:** Ollama (OpenAI-compatible endpoint on `:11434`), models pinned by tag.
- **Ears:** `mlx-whisper` (large-v3-turbo for commands, small for wake word).
- **Voice:** a local TTS (Kokoro / VoiceStudio-class engine); ElevenLabs stays optional for the
  cloud voice.
- **Embeddings:** local `nomic-embed-text` or `bge-m3` via Ollama, so indexing costs $0 and
  works offline.
- **Always on:** `pmset` no-sleep, launchd jobs for server + heartbeat + reflection, UPS if possible.

### 5.1 The brain adapter (build this first; it's what makes "editions" possible)
One module, `agent-sdk/src/llm/router.ts`, with one interface: `ask(task, {tier, tools, privacy})`.

| Tier | Default engine | Fallback chain |
|---|---|---|
| `deep` (agentic work, coding, research) | Claude Code / Agent SDK on subscription | Console key (Max credits) → Codex CLI |
| `chat` (conversation, quick Q&A) | Claude Sonnet via subscription | local 27B → Codex |
| `private` (finances, health, journal) | **local model only** | none, by design |
| `bulk` (embeddings, tagging, summaries of 1,000 notes) | local model | Haiku |

Every call is logged with engine, tokens and latency, so we can *measure* which engine earns its keep.

---

## 6. The brain: reorganize memory (the actual "reorganize")

Today knowledge lives in five places. Target: **one brain repo** that every body clones.

```
jarvis-brain/                 (PRIVATE GitHub repo; replaces Dropbox as sync for text)
├── SOUL.md                   who JARVIS is: voice, humor, how it talks to Terry
├── USER.md                   who Terry is, standing preferences (from MEMORY.md "user" + feedback)
├── memory/                   durable facts (today's Claude auto-memory, moved here)
├── journal/YYYY/MM-DD.md     daily log + nightly reflection output
├── topics/<slug>/            one folder per subject JARVIS is learning (§7)
│   ├── INDEX.md              what we know, open questions, confidence
│   ├── sources/              clipped articles, transcripts, PDFs-as-markdown
│   └── notes/                synthesized notes, linked [[like-this]]
├── domains/                  investments, video, macro, health… (from jarvis-private/context/projects)
└── skills/                   symlink or submodule of the jarvis repo skills
```

- **Git is the sync for text** (versioned, conflict-visible, works on a VPS). Dropbox keeps media
  and big binaries only.
- **Postgres + pgvector (Supabase)** holds the embedding index, the improvements queue, costs and
  conversation logs, so every body searches the same index.
- **Write discipline:** bodies append to `journal/` freely. Edits to `SOUL.md`/`USER.md`/`memory/`
  go through the nightly reflection job, which consolidates and commits. One writer per file type
  prevents merge fights.
- Keep the CLAUDE.md memory doctrine: `memory/` = durable facts, `bd remember` = build-time gotchas.
- Open it in **Obsidian** on Mac and phone (Obsidian Git plugin), and you can read and edit the brain by hand.

**Never commit:** account numbers, API keys, brokerage credentials. Secrets live in 1Password /
Doppler and get injected per body.

---

### 6.1 What the 26 videos agree on (adopt these)
Ranked by how many creators endorse each (digest of Cole Medin, Ben AI, Nate Herk, Nick Saraev,
Ray Fu, Samin Yasar, Zubair Trabzada, Jul–Nov 2026):
1. **Plain markdown you own, usable by any model** (~12 videos). This is already the JARVIS base. Keep it.
2. **Karpathy LLM wiki** (7): `raw/` is read-only sources, `wiki/` is AI-owned pages with
   `index.md` + `log.md`, and good answers get saved back into the wiki. → shape for `topics/`.
3. **Scheduled ingest from connectors** (7): Gmail, calendar, YouTube, meetings → summarized into
   the journal daily.
4. **Always-loaded core via a SessionStart hook** (6): `SOUL.md` + `USER.md` + `MEMORY.md` + "last
   24 hours" summary, injected deterministically (Cole). A hook always fires; a memory tool only
   runs when the agent remembers to call it (Samin).
5. **Hygiene / audit against rot** (6): tag every incoming fact **state** (overwrite) or **event**
   (append + date). Cole measured "just date everything" working only 8% of the time. A weekly
   audit skill gives a health score and asks before changing anything.
6. **Skills for anything explained 3×** (5), plus **an eval suite of real tasks** to re-run whenever
   the model/engine changes (Cole). This is how we'll know if the local model is good enough.
7. **Heartbeat that reports back** (4): Cole runs every 30 min on a VPS, checking mail/tasks,
   drafting (never sending) and posting a summary to chat.
8. **Retrieval:** start with **BM25 keyword search + recency weighting**. Use Haiku/local to
   pre-summarize each note into "likely questions + atoms" (Saraev: ~90% cheaper than vector RAG,
   unverified). Add pgvector as the hybrid half, not the only half.
9. **Cloud Routines can't see local files**: the brain must be reachable as a git repo or an MCP
   server (Ben). This is exactly why §6 moves the brain to a private GitHub repo.
10. **Thin permission wrappers around tools** (Cole): e.g. Gmail = draft-only for the cloud body.
11. **Personality files:** `SOUL.md` ("chief of staff, challenge my assumptions") plus an
    `anti-ai-style.md` banned-phrase list (Ray Fu).

Cole's own host: a ~$20/mo DigitalOcean VPS with Slack as the phone mouth. Hetzner does the same
for less. Pick DigitalOcean if you'd rather follow his walkthrough step by step.

## 7. "Talk like a friend, learn any topic fast"

What JARVIS needs from you to do this well (an interview session, about 45 minutes, once):
1. **Voice and relationship:** how you want to be addressed, humor level, when to push back,
   when to be brief. → `SOUL.md`
2. **Your world:** family/work context you're comfortable storing, goals for the next 12 months,
   current projects, what "a good day" looks like. → `USER.md`
3. **Privacy lines:** which topics never leave the home machine (routes to the `private` tier).
4. **Proactivity budget:** how often JARVIS may message first, and about what.
5. **Learning style:** Socratic vs. lecture, examples vs. theory, how you like to be quizzed.

### The "learn any topic" loop (a skill: `learn-topic`)
Modeled on Nate Herk's "clone an expert" build, which crawls an expert's ~700k words with parallel
subagents and compiles them into a wiki, then quoted principles, then a teaching skill.
1. `learn <topic>`: research sweep (web + YouTube transcripts via yt-dlp + NotebookLM + your existing notes)
   → `topics/<slug>/sources/`. Optionally pick 1–3 named experts and ingest their public work.
2. Synthesize a **map**: core concepts, key people/sources, debates, a "what to read first" list
   → `INDEX.md`.
3. **Converse:** you talk about it like you'd talk to a friend; JARVIS answers from the topic
   folder first, the web second, and cites which.
4. **Spaced review:** the heartbeat sends 2–3 questions a day on Telegram for active topics.
   Your answers update a confidence score per concept.
5. **Graduate:** after N sessions the topic gets a one-page "what I now believe" note, linked to
   neighboring topics. That is the cross-wiki bridge from Phase 8, reused.

The macro curriculum (52 weeks, Mankiw remap) is the first real tenant of this loop.

---

## 8. Build order (realistic hours, not weeks)

| Step | Where | Est. |
|---|---|---|
| 1. Turn on Remote Control + try Channels/Telegram on this laptop | travel | 1 h |
| 2. Create private `jarvis-brain` repo; migrate memory + context (script, dry-run first) | travel | 3–4 h |
| 3. Brain adapter (`llm/router.ts`) + call logging; route existing callers through it | travel | 3 h |
| 4. Personality interview → `SOUL.md`, `USER.md` | travel | 1 h |
| 5. Hetzner VPS + Tailscale + systemd Claude/Channels session + Bun server | travel | 3 h |
| 6. Routines for morning brief, ETF stage scan, stop-loss guard, monthly tracker | travel | 2 h |
| 7. Supabase pgvector; re-index brain; all bodies search it | travel | 3 h |
| 8. `learn-topic` skill + spaced-review heartbeat | travel | 3 h |
| 9. Home Mac: Ollama + Whisper + TTS + local embeddings; join Tailscale; adapter `private` tier | **home** | 3–4 h |
| 10. Voice PWA (phone browser → home Mac via Tailscale, VPS fallback) | home | 4 h |
| 11. Failover drill: shut the home Mac off, confirm phone → VPS still answers from the same memory | home | 1 h |

---

## 9. Open decisions (Terry's call)

Resolved 2026-11-08: home = 32 GB mini · brain = private GitHub · chat = Telegram · cloud server = yes.
Still open:
1. Which domains are `private` (local-only)? Decide at local-brain setup.
2. Which lanes/repos get archived vs. deleted in the reorganization? (Proposed: archive branch +
   `archive/` folder, nothing deleted.)
3. Terry's "updated idea" for the original premise. Not yet discussed.

---

## 10. JARVIS as an agentic-AI lab

JARVIS stays the trusted core: your memory, personality and judgment. Everything experimental
runs **beside** it as a *specialist* that JARVIS can call, on the cloud server. Specialists never
write to the brain repo directly. They return results, and JARVIS decides what to keep.

```
                 ┌──────────── JARVIS (core: brain repo, SOUL, memory) ────────────┐
   Telegram ───▶ │  router: "is this mine, or do I outsource it?"                  │
                 └──┬──────────────┬──────────────┬──────────────┬────────────────┘
                    ▼              ▼              ▼              ▼
              Dark factory     Hermes Agent    OpenClaw       REA teardown
              (Archon, Cole's   (self-writing   (multi-channel (reverse-engineer
              ai-software-      skills, cron,   gateway,       an app → findings
              factory)          own memory)     plugins)       → PRD)
                    │              │              │              │
                    └──────── results + a lab log entry ─────────┘
                                         ▼
                       journal/lab/ → reports → channel material
```

### 10.1 The specialists (what's verified so far)
| Specialist | What it is | How JARVIS calls it | Use it for |
|---|---|---|---|
| **Dark factory**: Cole's `coleam00/ai-software-factory` on **Archon** (MIT) | GitHub issues in, reviewed and merged PRs out; frontier model plans and reviews, cheaper model builds; `MISSION.md` + hidden holdout tests | File GitHub issues on a factory repo; it runs on cron on the VPS | Building apps and tools (§10.2) |
| **Hermes Agent** (Nous Research, MIT) | Self-hosted agent: writes its own skills, has its own memory and cron, any model including Ollama | `hermes chat -q` one-shot, `hermes acp`, MCP server plugin, OpenAI-compatible API | Long-running specialist jobs; a test bench for open models |
| **OpenClaw** (OpenClaw Foundation, MIT) | Personal-assistant gateway, 20+ chat channels, swappable models | `openclaw agent exec`, `openclaw acp`, `openclaw mcp`, webhooks | Comparing against JARVIS; multi-channel experiments; team brain prototypes |
| **REA** (`morluto/rea`, MIT, `npx rea-agents setup`) | MCP server that lets an agent look inside apps without their source (JS/Electron, binaries via Ghidra, Android, web) | MCP in Claude Code | App teardowns → PRD for the factory. Clone *behavior*, not code or assets; respect licenses |

All call interfaces above come from the projects' docs and are **unverified until we run them**.
Each needs a smoke test before JARVIS depends on it.

### 10.2 The app pipeline (using factories, not explaining them)
1. **Pick** a target: a paid service to replace, an app to clone, or a team-brain tool. Nick's
   roundup shows the winners are small and personal: replace one subscription.
2. **Teardown** (optional): REA plus a browser walkthrough → `topics/<app>/teardown.md`.
3. **Spec:** JARVIS interviews you, then writes `MISSION.md` (including "never becomes") + PRD +
   10–20 issues.
4. **Build:** the factory on the VPS. Plan/review on Claude, build on a cheaper or open model (Cole's
   measured mix: about the same quality at ~¼ the cost). You approve the epic split and promotion to
   production. Cole's own verdict is that fully hands-off fails, so keep those two gates.
5. **Report:** every run logs cost, time, tickets passed and model mix to `journal/lab/`. That
   log becomes the channel's evidence.

**Budget note:** Cole burned through both a $200 Claude Max and a $200 Codex Pro weekly limit in
one week running factories. JARVIS's daily use must not starve the factory, or the other way
around. The adapter (§5.1) tracks both and pauses factory laps when your interactive headroom gets low.

### 10.3 The face of JARVIS (Zubair-style "entity" interface)
- **What:** a local web app (served by the home Mac or VPS, reached over Tailscale, installable on
  the phone as a PWA).
- **Center:** a 3D **knowledge galaxy** of the brain repo (3d-force-graph / three.js). Notes are
  stars, links come from `[[wikilinks]]`, and folders are colored by domain.
- **Corner:** the **JARVIS orb**, a living entity that changes color per engine (Claude gold /
  local green / Codex blue, matching your existing brain palette). It pulses while speaking and
  shows a status line ("thinking", "outsourcing to factory", "reading 4 notes").
- **Fly-to-source:** when JARVIS answers from notes, the camera flies to them and lights the cluster.
- **Specialists as moons:** factory, Hermes, OpenClaw and REA orbit the core and light up when a
  job is out. You can *see* the outsourcing.
- **Build source:** Zubair's free prompt packs (in `~/Dropbox/AITerryByrd/`) cover the galaxy,
  voice and fly-to-source. We adapt them to the brain repo and the router, not his API-key server.
  His finished app is members-only. We build our own.

### 10.4 Revised build order (replaces §8 where they differ)
| Step | Where | Est. |
|---|---|---|
| 1. Private `jarvis-brain` repo, built fresh on Cole's template (§11 layout) | travel | 1–2 h |
| 2. Remote Control + Telegram Channels on the laptop | travel | 1 h |
| 3. Personality interview → `SOUL.md`, `USER.md` | travel | 1 h |
| 4. Brain adapter + usage tracking (Claude / Codex / Ollama) | travel | 3 h |
| 5. VPS (Hetzner) + Tailscale + always-on JARVIS + Telegram | travel | 3 h |
| 6. Archive the dropped lanes (archive branch/folder, nothing deleted) | travel | 1–2 h |
| 7. Dark factory on the VPS; first real app through it, with a lab log | travel | 4–6 h |
| 8. Hermes + OpenClaw installed as specialists; smoke-test each call path | travel | 3 h |
| 9. JARVIS face v1 (galaxy + orb + fly-to-source) | travel | 4 h |
| 10. Memory migration script (Dropbox → brain repo) | after 1–5 | 3–4 h |
| 11. Home mini: Ollama 27B + Whisper + TTS + embeddings; `private` tier | **home** | 3–4 h |
| 12. Failover drill: home off → phone → VPS, same memory | home | 1 h |

## Sources
- Anthropic, "Use the Claude Agent SDK with your Claude plan": https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan
- HN discussion of the Oct 6→7 revision: https://news.ycombinator.com/item?id=49997654
- Pause coverage: https://devops.com/anthropic-hits-pause-on-claude-agent-sdk-billing-change-for-now
- Channels overview: https://dev.to/alanwest/claude-code-channels-control-your-ai-coding-agent-from-telegram-2b0n
- Zubair Trabzada prompt packs (in `~/Dropbox/AITerryByrd/`): hardware tiers and the local stack
- The 26 videos (digest 2026-11-07): Cole Medin qIWB1yMsqRo, xOFkpf9KgKg, mjQlZrteMIY, YHKuUjicB3M · Ben AI pXHpUyC54uQ, Puzgmzv7t3Q, 82hCt3xH9Gc, d7VPnW1KsgA · Nate Herk bvGptCLDhyo, yysILVsfLFM · Nick Saraev LP7bfT4vOlo · Samin Yasar kG_CoTjCC98 · Ray Fu -SsAwIkW9rI · Zubair Trabzada OTb1DR47LSo, BgpRjk4Yoqk, acsXZP3SA6w, wJ3CFmzMbtA, U-LXFzu6sGU, YK-qJwmwjVc, 1ILapFgLf2E, Acw0NtkyNtM, qfpD1FWdyTs, ud7wzdiM0gk, 2od7tPirPYE, whIp1SOahOM, dCKBxcYGkoE (all youtube.com/watch?v=<id>)

---

## 11. Reorganize vs. start fresh: the answer (2026-11-08)

**Neither a pure reorganization nor a fresh start. Split JARVIS by role: build the *brain* fresh, refit
the *engine* in place, and turn `jarvis-private` into cold storage.**

Measured state: `jarvis` is ~15 GB mixing engine code (`agent-sdk`, skills, tools) with video media
(`asset-library` 4.4 GB, two video folders 5.6 GB). `jarvis-private` is ~60 GB, almost all video
projects. The actual *knowledge* is small and scattered: 17 files in `context/`, 69 auto-memory
files, `bd` memories, two wikis (`ai-futures-wiki`, `claude-code-wiki`), and `research/`. Much of it
is stale: the phase state was frozen in April and `NewDirection.md` in June.

| Piece | Action | Why |
|---|---|---|
| **`jarvis-brain`** (NEW private repo) | **Build fresh** on Cole's 4 C's template (his repo is at `~/Dropbox/Dynamous/claude-code-second-brain`: SOUL/USER/MEMORY, daily logs, hybrid search, heartbeat, chat), then **import selectively** | Moving 6 stores of half-stale notes in bulk just moves the rot. Cole: "start with soul.md and user.md… keep it incredibly simple." Each import is a decision: still true, and serves the focus? |
| **`jarvis`** (existing repo) | **Refit in place** as the ENGINE: server, router, Telegram, interface, skills, CLI tools | The code works and has history. It needs pruning, not a rewrite |
| Video media inside `jarvis` | Move to ORICO / Dropbox media (out of git) | 10 GB of binaries don't belong in an engine repo |
| Dropped lanes (investments, Ordinary Economics, Camino, macro, athlete…) | `archive/` branch or folder; nothing deleted | Terry's call 2026-11-08: archive, refocus |
| **`jarvis-private`** | Becomes **cold storage** (media, finished video projects); not synced to the cloud | The brain stops living here |
| **`jarvis-lab`** (NEW repo) | Factory config, Hermes/OpenClaw setups, `lab-log/` run records | Experiments stay outside the brain (§10) |
| Apps built by the factory | One repo each | Each is a product, and a video |

### The brain repo layout (Cole's two layers + Karpathy wiki + Zubair's typed graph)
```
jarvis-brain/
├── SOUL.md  USER.md  MEMORY.md     ← layer 1: loaded every session by a SessionStart hook
├── wiki/                            ← layer 2: AI-owned Karpathy wiki, one entity page per thing
│   ├── index.md  log.md
│   ├── people/  projects/  apps/  tools/  models/  concepts/   ← "types" = colors in the galaxy
├── raw/                             ← read-only sources (transcripts, articles, teardowns)
├── daily/YYYY-MM-DD.md              ← every conversation summarized here; nightly reflection promotes
├── lab/                             ← verdicts pulled back from jarvis-lab (results only)
└── evals/tasks.md                   ← Cole's eval suite: real tasks re-run on every model/engine change
```
Every fact is tagged **state** (overwrite) or **event** (append + date). That's Cole's fix for rot.

### Selective import list (first pass, decided with Terry)
Keep: user facts + feedback memories that still hold · the agent-engineering salvage + positioning
docs · JARVIS architecture notes · `claude-code-wiki` (directly on-topic) · channel production
standards that still apply to the AI channel. Archive: investments, Ordinary Economics, Camino,
macro, athlete, hallucinations series, old phase files.

### Run Cole's four audits after the build (they're the acceptance test)
1. **Context:** fresh session, "what are we working on and why?" → answers like a teammate, no digging.
2. **Connections:** "Monday catch-up" → pulls Gmail, calendar, GitHub, Telegram.
3. **Capabilities:** a weekly job in one short request → real output, no re-explaining.
4. **Cadence:** one heartbeat job reports back on Telegram unasked.

## 12. The JARVIS face: what Zubair actually shows (frames reviewed 2026-11-08)
From frame grabs of three of his videos (YK-qJwmwjVc, OTb1DR47LSo, acsXZP3SA6w); `localhost:4719`, titled "AI WORKSHOP OS":
- **Center:** a 3D force graph, "531 notes · 1940 connections". Nodes are **typed and color-filtered**
  (Router, Wiki, Concepts, Suites, Skills, Tools, Worlds, Notes, Files), and hubs are labeled by size
  (Skill Suites 236, Local Businesses 123…). Toggle "back to 2D."
- **Left panel:** "Search the brain…", an **Inspector** (click a node to light only its connections;
  *shift-click a second node to trace the path between them*), Top Hubs, force sliders (repel, link
  length).
- **Right:** the **J.A.R.V.I.S. arc-reactor ring** (purple/teal HUD), with status ("ONLINE", "LISTENING",
  "THINKING"), a **model badge** ("FABLE 5.1", "QWEN 3.5 9B"), and **skins: RING / CUBE / FACE**. Below:
  toggles EYES, WATCH, HOLO, FOCUS.
- **Overlays:** a "Tool armory" grid of integrations; live call cards ("ON THE CALL · the tire shop");
  his Telegram chat with Jarvis shown side by side; spoken replies as a caption line at the bottom.
- **Takeaway for us:** the galaxy works because the brain is *typed*. That's why the `wiki/` folders
  above are typed. Our version adds the lab specialists as moons (§10.3) and colors the orb by engine.
- Spotted on ollama.com in his video: `ollama launch claude | opencode | hermes | openclaw --model qwen3.5`.
  Ollama now launches Hermes and OpenClaw against a local model directly. Useful for the lab
  (unverified until we run it).

## 13. What we take from Cole's `second-brain-starter` (reviewed 2026-11-08)

The repo (github.com/coleam00/second-brain-starter, last commit 2026-06-09) is small: a **PRD-generator
skill** plus **memory templates**. The *implementation* (hooks, search, heartbeat, chat) is his
workshop code, which we already have locally at `~/Dropbox/Dynamous/claude-code-second-brain/.claude/`
(March 2026). Together they cover most of steps 1–4.

**Adopt directly**
- **`BOOTSTRAP.md`**: a first-run interview, one question at a time, that fills USER/SOUL/HEARTBEAT and then
  deletes itself. It resumes if a session ends partway. **This replaces our "personality interview" step.** We
  add our own questions: the agentic-AI focus, the lab, privacy tiers, the learning style.
- **Templates** `SOUL.md` (values, proactivity rules, Always Ask / Never Do / Safe Freely), `USER.md`,
  `MEMORY.md`, `HEARTBEAT.md`.
- **Requirements form** (8 sections), filled out once → becomes our spec. Pick **"Advisor"** as the
  proactivity level to start: drafts for review, never sends.

**Adopt the patterns (these solve problems our plan would hit)**
1. **`concat-both` git merge driver** for `daily/*.md`. Laptop, VPS and home Mac all append to daily
   logs, and plain git merges conflict on day one. Cole's fix: git-sync every 2 min plus a merge driver that
   concatenates both sides. **Required, because we chose git as the sync layer.**
2. **SessionStart / PreCompact / SessionEnd hooks.** `memory_flush.py` (a no-tools Claude call) writes
   *intelligent* summaries to the daily log, not transcript dumps.
3. **Hook recursion guard:** every SDK session sets `CLAUDE_INVOKED_BY`, so heartbeat/flush runs don't
   re-trigger the flush hooks.
4. **Heartbeat state-diffing:** only *new* items reach the model, which stops 30-minute nag loops.
5. **Pre-flight guardrail agent:** a no-tools call rates external data pass/fail/suspicious before
   the main agent reads it. This is the prompt-injection check.
6. **`block-secrets.py`** PreToolUse hook plus `DANGEROUS_BASH_PATTERNS`. **Essential on the VPS**, where
   the agent runs unattended.
7. **SOUL.md write-protection:** reflection can *suggest* personality changes but can't make them (stops "soul drift").
8. **Integration CLI wrapper** (`query.py gmail …`): the LLM never sees keys, and permissions are set per tool.
9. **Hybrid search:** FastEmbed (local ONNX) + SQLite FTS5/sqlite-vec locally, Postgres + pgvector on the VPS,
   weighted 70% vector / 30% keyword.
10. **Draft lifecycle** (`drafts/active → sent | expired`), voice-matched from your sent mail.

**Skip / change**
- Slack chat bot → we use **Telegram via Channels**.
- Asana / Circle integrations → not in our stack. Swap in **GitHub** (factory issues/PRs) and YouTube.
- Habits tracker → optional, later.
- Obsidian Sync → **git** (we chose GitHub).
- The repo has no license file, so we adapt the patterns and write our own code rather than copy
  files wholesale. The workshop code is Dynamous member material, for your own use.
