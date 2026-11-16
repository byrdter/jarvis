# JARVIS

**A personal AI second brain and agentic-AI workbench, built on Claude Code.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-purple.svg)](https://claude.ai/code)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

JARVIS is my working partner. It knows my work, keeps the record straight, and runs on its own when I'm
not at the keyboard. It's also my test bench: I use it to build AI apps and capabilities, test what
works, and show people who don't code how to do the same in their own work.

After 30 years teaching business people technology, this is the project where I build with AI myself.
Everything here is real, in daily use, and sometimes broken. That's part of the point.

---

## What it does today

- **Talks to me from anywhere.** I message JARVIS on Telegram from my phone. It answers from an
  always-on server, so it works with my laptop closed.
- **Remembers.** A private "brain" repository holds who JARVIS is, who I am, what we decided, and a daily
  log. Every session loads it at startup, and the laptop and server keep it in sync every two minutes.
- **Checks in without being asked.** A heartbeat looks for changes every 30 minutes during my working
  hours and stays quiet unless something matters. A morning brief arrives at 10:00 with what changed
  overnight and a suggested top three for the day.
- **Checks itself.** A daily preflight runs live health checks and messages me only when one fails.
  A watchdog restarts the chat if its connection drops.
- **Makes videos.** A full production pipeline (scripts, HyperFrames scenes, QC gates, assembly) for the
  YouTube work that documents all of this.

## How it fits together

```
        Phone (Telegram)                    Laptop (Claude Code)
               │                                     │
               ▼                                     │
   ┌───────────────────────────┐                     │
   │  Always-on server         │◄──── Tailscale ─────┤   private network only;
   │  Claude Code + Telegram   │                     │   no public SSH
   │  heartbeat · brief ·      │                     │
   │  preflight · watchdog     │                     │
   └─────────────┬─────────────┘                     │
                 │        brain sync (every 2 min)   │
                 ▼                                   ▼
          ┌────────────────────────────────────────────────┐
          │  Brain repo (private): SOUL · USER · MEMORY ·  │
          │  daily logs · wiki                             │
          └────────────────────────────────────────────────┘
                 ▲
                 │ loaded at session start by a hook
          ┌──────┴─────────────────────────────────────────┐
          │  This repo (the engine): rules, hooks, skills, │
          │  server setup, video pipeline                  │
          └────────────────────────────────────────────────┘
```

Two repos, split on purpose. **This one is the engine**: code and rules, safe to share. **The brain is
private**: memory and personal context. Claude Code is the reasoning core in both places, signed in
with a regular Claude subscription.

## What's in this repo

| Path | What it is |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Project rules every session follows (language, memory, video standards, session close) |
| [`.claude/hooks/`](.claude/hooks/) | Session hooks: load the brain at startup, recall relevant memories, save state before compaction |
| [`infra/server/`](infra/server/) | The always-on server: hardening script, the Telegram chat service, and the scheduled jobs (brain sync, heartbeat, brief, preflight, watchdog) with an installer |
| [`docs/jarvis-2.0/`](docs/jarvis-2.0/) | The current plan ([`PLAN.md`](docs/jarvis-2.0/PLAN.md)) and the server plan ([`SERVER-PLAN.md`](docs/jarvis-2.0/SERVER-PLAN.md)) |
| [`.agents/skills/`](.agents/skills/) | Video production: the `jarvis-video-production` pipeline, website-to-video, Excalidraw diagrams |
| [`skills/`](skills/) | Smaller skills: wiki (setup, ingest, query, lint, status), YouTube monitor, news aggregator, web browsing, invoices, image generation |
| [`cli-tools/`](cli-tools/) | Helper tools: skill scaffolding and title/citation card makers for video |
| [`ecosystem/`](ecosystem/) | The earlier orchestration framework (registry, memory backends, security gates), kept for reference |
| [`archive/`](archive/README.md) | Lanes I've stepped away from, including the original investment skills. Nothing deleted |

## Where it's headed

The build order lives in [`docs/jarvis-2.0/PLAN.md`](docs/jarvis-2.0/PLAN.md) §10.4. Done so far: the
brain repo, Telegram, the personality interview, and the always-on server. Next:

- **A dark factory on the server:** an agent pipeline that takes an app idea to a working, tested repo,
  with every run logged.
- **Open-source specialist agents** (Hermes, OpenClaw) the brain can hand work to.
- **A visual "face"** for the brain.
- **A home machine with a local model**, so private work never leaves the house and the cloud server
  becomes the backup.

## Running your own

This isn't packaged as a product yet, but the pieces are reusable:

1. Install [Claude Code](https://claude.ai/code) and clone this repo.
2. Read [`CLAUDE.md`](CLAUDE.md) and adapt the rules to your own work.
3. For the always-on part, follow [`docs/jarvis-2.0/SERVER-PLAN.md`](docs/jarvis-2.0/SERVER-PLAN.md): a
   small cloud server, Tailscale, Claude Code's Telegram channel, then
   [`infra/server/jobs/install.sh`](infra/server/jobs/install.sh) for the scheduled jobs.
4. Make your own private brain repo with `SOUL.md`, `USER.md` and `MEMORY.md`; the
   [`load-brain.sh`](.claude/hooks/load-brain.sh) hook shows what it expects.

Secrets (bot tokens, keys) never go in either repo. On the server they live in files only the service
user can read.

## Disclaimer

Educational and demonstration purposes only. Nothing here is financial, investment, legal or
professional advice. The archived investment skills showed technical implementation, not
recommendations. Use at your own risk.

## License

MIT. See [LICENSE](LICENSE). Claude Code is subject to [Anthropic's terms](https://www.anthropic.com/terms).

## Acknowledgments

Ideas borrowed with thanks from Cole Medin (the second-brain template and its four audits), Zubair
Trabzada (prompt packs and the local-model stack), Andrej Karpathy (the AI-owned wiki pattern), and
OpenClaw (plugin and memory design).

*Last updated: November 15, 2026*
