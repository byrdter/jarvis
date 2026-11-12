# The always-on server: plan (2026-11-11)

> PLAN §10.4 step 5. Goal: JARVIS answers on Telegram 24/7, sends the 10:00 brief, runs the 30-minute
> heartbeat, and later hosts the lab specialists, whether or not Terry's laptop is on.
> Builds on: SERVER notes in PLAN §4, the laws in ZUBAIR-PACKS-AND-JEV.md, Telegram setup of 2026-11-11.

## Decisions (defaults; Terry can change any)
| # | Decision | Default | Why |
|---|---|---|---|
| 1 | Provider + size | **Hetzner CX33**: 4 vCPU, 8 GB RAM, 80 GB disk, **~€8.49/mo + ~€0.50 IPv4** | Hetzner raised prices twice in 2026; the CX line rose ~30%, the CPX line 113–175%, so CX is the value pick. Resize up to CX43 (16 GB, ~€16/mo) in minutes when the lab needs it. Check the live price at signup. |
| 2 | Location | **Germany (Nuremberg or Falkenstein)** | Closest to Valencia; EU data. Latency doesn't matter for chat. CX is EU-only anyway. |
| 3 | OS | **Ubuntu 24.04 LTS** | Long support; Claude Code, Bun, Node, Tailscale all first-class. |
| 4 | Telegram bot | **The server takes over the main bot**; the laptop stops running it | Telegram allows **one** active poller per bot token (a second gets HTTP 409 Conflict). If you want the laptop on Telegram too, make a second bot ("JARVIS Laptop"). |
| 5 | How we reach the server | **Tailscale only**; no public SSH | The server is invisible to the internet; your laptop and phone reach it over a private network. |
| 6 | Permissions on the server | **Auto mode + explicit allow rules + a block-secrets hook**; approvals relay to your phone | Never `bypassPermissions`. Jev gate added in the reflex-layer step. |
| 7 | Claude account | **Your Max subscription**, signed in on the server | One subscription, two machines: usage is **shared**, so the heartbeat only wakes the model when something changed. |
| 8 | Backups | **Hetzner snapshots weekly** (~€0.01/GB/mo) + the brain is already in GitHub | The brain is safe on GitHub; snapshots cover the setup. |

## What runs on the box
```
user: jarvis (no root login; sudo only for setup)
~/code/jarvis          engine (git clone, public repo)
~/code/jarvis-brain    brain  (git clone, private repo, deploy key)
/etc/jarvis/*.env      secrets (600, owned by jarvis): Telegram token, later Jev key
```
| Service (systemd, --user) | What it does | Schedule |
|---|---|---|
| `jarvis-chat` | `claude --channels plugin:telegram@claude-plugins-official` inside tmux, in `~/code/jarvis` (so the brain loads every session). Restarts on crash. **Kills stray old pollers before starting** (the plugin can leave orphaned `bun` processes after a restart, which then trigger 409s). | always |
| `brain-sync` | `scripts/brain-sync.sh`: commit, merge (union merge for daily logs), push | every 2 min |
| `jarvis-heartbeat` | Gathers changes with plain scripts (GitHub, later Gmail), and **only if something changed** runs `claude -p` with HEARTBEAT.md; sends results via the Telegram Bot API `sendMessage` (sending doesn't conflict with the chat poller) | every 30 min, 10:00–19:00 Europe/Madrid |
| `jarvis-brief` | The morning brief: overnight changes, today's top 3, AI news later | 10:00 Europe/Madrid daily |
| `jarvis-preflight` | Live checks (law: "done means preflight passed"); posts failures to Telegram | daily + after every deploy |

Time zone: the server runs in UTC; jobs use `Europe/Madrid` explicitly (and follow Terry's travel when needed).

## Security checklist
- SSH keys only, password login off, root login off; **ufw: deny all incoming**, allow only the Tailscale interface.
- `unattended-upgrades` for security patches; fail2ban not needed behind Tailscale.
- Secrets only in `/etc/jarvis/*.env` (600); never in either repo; `block-secrets` PreToolUse hook +
  dangerous-command patterns in the server's Claude settings.
- Git identity set **per repo** on the server (the laptop lacked one; brain-sync would fail without it).
- Deploy key for the brain repo: read/write, that repo only.
- Telegram stays allowlist-only (1 sender). Anyone who can reply can approve actions, so keep it that way.

## Build steps
| # | Step | Who | Est. |
|---|---|---|---|
| 1 | Create a Hetzner account, add a payment method | **Terry** | 15 min |
| 2 | Generate an SSH key on the laptop; Terry pastes the **public** key into Hetzner (public keys aren't secret) | JARVIS + Terry | 5 min |
| 3 | Create the CX33 (Ubuntu 24.04, Germany, that SSH key) | **Terry** (it's a purchase) | 5 min |
| 4 | Harden the box: user, SSH, ufw, updates, time zone | JARVIS over SSH | 30 min |
| 5 | Tailscale on server + laptop + phone; then close public SSH | JARVIS + **Terry signs in** | 20 min |
| 6 | Install Claude Code (native), Bun, git; clone both repos; deploy key | JARVIS | 20 min |
| 7 | Sign Claude in on the server: it prints a URL, Terry opens it and approves | **Terry** | 5 min |
| 8 | Move the bot: stop it on the laptop, configure the token on the server, start `jarvis-chat`, re-pair if asked | JARVIS + **Terry pastes the token** | 15 min |
| 9 | brain-sync, heartbeat, brief and preflight timers | JARVIS | 60 min |
| 10 | Test from the phone with the laptop **closed**; update the status map | together | 15 min |
**Total ≈ 3 hours**, about 45 minutes of it Terry's.

## Cost
~€9/month for the server (+ snapshots, cents). The Claude Max subscription is shared with the laptop.
Jev (later) is fractions of a cent per day.

## Later on the same box (not now)
Dark factory (Archon), Hermes, OpenClaw, REA. Expect to resize to CX43 (16 GB) when the factory runs.
If a specialist misbehaves, it gets its own small server instead.

Sources: Hetzner 2026 price changes (northflank.com/blog/hetzner-cloud-server-price-increases;
trackvps.com/hetzner-cloud-pricing, checked 2026-11-08); Telegram one-poller rule and the Claude
plugin orphaned-poller issue (claudeissues.com/issue/38204).
