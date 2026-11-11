# Zubair's JARVIS, June–November 2026: what we still need (reviewed 2026-11-11)

> Source: 14 videos from youtube.com/@AI-GPTWorkshop published 2026-06-15 → 2026-11-11 that weren't
> in the 2026-11-07 digest (the 13 already in PLAN.md §6.1, §10.3, §12). Transcribed locally with
> whisper.cpp (`ggml-small.en`, ~30 s per video on the M5) after YouTube rate-limited caption downloads.
> He shows features; he doesn't publish architecture. Builds ship as free prompt packs or a paid zip
> (his paid JARVIS is at **v8.2**).
>
> Videos: xHAZo1SmnhM (Second Brains, 6/15) · I-cvxBMue08 (JARVIS Fable 5, 7/4) · LmfIIpWgaFQ (content
> autopilot, 7/5) · pOFVioeRG2I (AI employee/TARS, 7/10) · o0eksPNCJcc (debate show, 7/18) ·
> w0fSAHOC6fo (record a skill, 8/12) · mitzci4FsOg (JARVIS GPT-6 Astra, 9/9) · fMV6JKkQVfE + D5v4UuvtUXc +
> _0RRAUw-mT0 (Jev reflex layer, 9/21–26) · zdnijkAbknA (JARVIS phones him, 9/24) · 84CkBM_jF4g (REA
> reverse-engineering, 10/14) · oj2MVUbb4iE (TV OS, 10/23) · 34J8xhaAn4U (Fable 5.2 workshop, 11/11).

## Already in our plan (confirmed, no change)
Markdown brain + CLAUDE.md as router · 3D typed galaxy + orb + model badge + fly-to-source · voice ·
Telegram · morning brief · draft-never-send email · tool armory · REA as a lab specialist ·
local/offline tier · interview-to-fill profile (our BOOTSTRAP) · status line.

## New: adopt (ranked by value to us)
1. **A reflex layer before the brain.** Five fast yes/no/probability gates on every request, shown in
   the UI so routing is visible and debuggable: **lane** (brain / mail-calendar / agent task / web),
   **complete** (has Terry finished talking?), **addressed** (talking to JARVIS or narrating a video?),
   **stakes** (would this send, call, delete or spend? → must confirm), **brain-has-it** (does a note
   already answer this? → skip web and tools). He uses *Jev* (TypeSafe, a non-LLM decision model,
   ~60–300 ms, input-only pricing) via its API or Zapier MCP. **Ours:** build the same five gates on
   Haiku or the local 27B model first (no new vendor); test Jev in the lab as a comparison
   ("I tested a decision model vs. an LLM" is a video). Measured payoff in his demo: 12 support
   requests in 19.7 s with 4 frontier calls vs. 33.9 s with 12.
2. **Stakes-based confirmation + duplicate check.** Any action scored high-stakes asks first; emails go
   to Drafts; before sending, check recent history for an identical action ("you've sent this
   three times today"). Goes into SOUL boundaries and the action wrapper.
3. **Knower vs. doer.** "JARVIS knows everything; TARS does everything." A commander agent dispatches
   background sub-agents with a **jobs board** (status, a briefing per mission, a **debrief** that
   states which tools were missing, an "open result" link) and pings Terry when jobs finish.
   **Ours:** this is the shape for the lab specialists (PLAN §10): one jobs board for factory, Hermes,
   OpenClaw and REA runs, debriefs written to `lab/`.
4. **Voice that behaves like a person.** Wake word ("Jarvis"), barge-in ("stop," "thank you, Jarvis"),
   the *addressed* gate so a video narration doesn't trigger it, captions, and **two voice tiers**:
   realtime (~0.3 s, ~5¢/min) for conversation and cheap TTS for hands-free/background.
   **Ours:** add wake word, barge-in and tiers to the voice PWA (PLAN §8 step 10).
5. **JARVIS can call Terry.** Standing escalation rules ("I'm out, call only if it can't wait"); the
   phone agent (Retell AI) delegates work to the tool-using "desk" and confirms by **Telegram text +
   voice note**. **Ours:** Telegram voice notes first (cheap); outbound calls later, gated by explicit
   rules in HEARTBEAT.md.
6. **Cost visibility.** Show the cost before any paid generation; a per-session dollar cap in the UI.
   **Ours:** add both to the brain adapter (PLAN §5.1), which already tracks usage.
7. **Tool access order: connector → MCP/Zapier → recorded skill.** Zapier MCP reaches ~9,000 apps with
   per-app permissions. Claude desktop's **"Record a skill"** (Cowork) turns one narrated
   demonstration into a SKILL.md and lists the steps it *didn't* see; recorded skills also guide the
   browser agent. **Ours:** adopt the order; use record-a-skill for Terry's repeat chores.
8. **Debate / stress-test mode.** Two personas on *different* models argue a question while Terry judges
   and can interrupt; settings for rounds, humor/honesty, and a budget cap. Built against sycophancy
   ("a single model always agrees with you"). **Ours:** a `stress-test` skill for big decisions; it fits
   Terry's rule "push back once, plainly." Also strong video material.
9. **Answers become memory.** Research results appear as cards Terry can dismiss or **keep as a note**
   (lands in `wiki/`). Proven pipelines are saved as playbook notes and re-read on the next run.
10. **Teardown artifact with fixed sections** (stack / how it works / how to rebuild / unknowns /
    evidence), filed to the brain and reused as a build blueprint; builds **self-test in a hidden
    browser** before Terry sees them. Our Financial Wisdom study already followed this shape; make it
    the REA template.
11. **Galaxy upgrades** from his free "AI Second Brain OS": depth 1/2/3 neighbor highlight, pin a node,
    heatmap, type toggles, 2D mode with icons, themes, particle flow on links.

## New: optional / later
- **Eyes / Watch / Focus / Holo modes:** camera (posture, outfit), per-tab screen share as context,
  **focus lock** (30-minute timer, calls out tab drift, reports a drift count), hand gestures.
  Focus lock is the one with real daily value.
- **Computer use with narration** ("taking over the screen," narrates each click, voice kill switch,
  never publishes). In Claude/Fable already; wire it into JARVIS with the stakes gate.
- **Model switch by voice** ("switch your brain to Fable 5.2") with a skin per model; OpenRouter for
  non-Anthropic models.
- **3D workshop** (Fable 5.2): build an object from a photo/sketch/floor plan, explode it into labeled
  parts, edit by voice, render a photo. Demo appeal; low priority.
- **Ambient TV dashboard** paired to the phone by QR code (his "TV OS").
- **Humor / honesty dials** as settings rather than fixed SOUL text.

## Business angle (feeds Terry's plan)
He sells second-brain setups to local businesses: a brain + visual layer for **$2,000–3,000 setup plus
a monthly retainer** (his HVAC client: $2,000 + $500/mo). This matches Terry's "second brains for teams
and organizations" lane and the company-visit line in the business plan.

## What to get from his free community (AI Workshop Lite)
Path for all: **Classroom → YouTube Resources → "Claude Code and Codex GPT" folder** (newest at the bottom).
We already have: the main 6-prompt JARVIS pack, Fully Offline, Fully Local, Sixteen Languages.
Needed, in priority order:
1. **Fable 5.2 JARVIS workshop prompt pack** (posted with today's video).
2. **Jev / reflex-layer guide** (PDF with prompts to add Jev to JARVIS).
3. **CASE: build your first mission agent** (the knower/doer jobs board).
4. **Updated JARVIS prompt pack with REA integration.**
5. **GPT-6 Astra JARVIS pack** (eyes / watch / focus / holo prompts).
6. **AI Second Brain Operating System** (the free 2D/3D visualizer: GitHub link + install steps).
7. **Debate show prompt pack.**
8. The JARVIS phone-call prompts, if posted with "My AI Called Me During a Meeting."
Optional: Social Media Automation (brand-voice template, for the channel), tvOS files, Record-a-skill notes.
