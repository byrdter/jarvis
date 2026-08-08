# Federation-video demand probe — 2026-08-07

Follows [STUDIO-LANE-PROBE-2026-08-06.md](STUDIO-LANE-PROBE-2026-08-06.md). That file proved the
*lane* (build-your-own-AI-system, ~5× the AI-video lane). This file gates the *execution* of one
specific idea — the JARVIS×Studio **federation** video ("I built multiple AI systems and they
disagree") — per the 2026-07-30 rule: a proven lane does not guarantee the specific framing travels.

Tool: `tools/demand-probe.py`. Band 1k–300k subs, since 2025-01-01, shorts excluded, ≥1.5× = hit.
**Read the per-video rows, not the medians** — every headline number below is moved by a false
positive, exactly the trap the tool exists to catch.

---

## Round A — the federation "shape" (conflict / multi-agent / connect)

| verdict | n | median | p75 | max | hits | query |
|---|---|---|---|---|---|---|
| PROVEN | 12 | 0.46x | 1.40x | 10.82x | 2 | multi agent ai system |
| THIN | 4 | 0.36x | 0.66x | 0.66x | 0 | ai agents working together |
| MIXED | 9 | 0.27x | 0.66x | 10.82x | 1 | multiple ai agents |
| MIXED | 7 | 0.87x | 1.15x | 44.40x | 1 | when ai agents disagree |
| PROVEN | 10 | 0.26x | 1.56x | 12.74x | 3 | i built a team of ai agents |
| INCONCLUSIVE | 1 | — | — | — | — | connecting my ai tools |
| PROVEN | 6 | 6.70x | 37.65x | 55.50x | 3 | ai assistant lied to me |
| PROVEN | 7 | 0.12x | 2.01x | 55.50x | 2 | ai agents out of control |

**The "lying / disagree / out of control" hook is DEAD — and contaminated.** Every high score is a
false positive:
- The 44.40×–55.50× rows across three queries are ONE viral novelty meme —
  *"AI agents activate secret language / Three AI agents realize they're all AI"* (3–3.8M views).
  Not our content; word overlap only.
- `ai assistant lied to me`'s 37.65× / 12.44× are **build-your-own-assistant tutorials** bleeding in.
- The genuinely on-concept rows: *"My AI Assistant Lies to Me… AND YOURS DOES TOO"* → **0.12×**,
  *"Your AI Assistant Is Lying to You"* → **0.03×**, *"When Your 10 AI Agents Disagree 67 Times"* →
  **1.15× on 1,920 subs** (below the hit line). The drama-of-conflict framing has no demand.
- `connecting my ai tools` → **n=1, a measurement void.** The literal "federation / connect my tools"
  framing is not a recognized search shape.

**What IS real in Round A — the BUILD frame, at reachable size:**
```
 12.74x   146,485    11,500   I Built a Full AI Team Inside OpenClaw for $400/Month
 10.82x   758,632    70,100   My Multi-Agent Team with OpenClaw
```
Demand is for *building/orchestrating multiple AIs*, not for the melodrama of them fighting.

---

## Round B — revised: build-frame + second-brain fusion + film-studio-as-build

| verdict | n | median | p75 | max | hits | query |
|---|---|---|---|---|---|---|
| PROVEN | 5 | 2.74x | 2.85x | 61.46x | 3 | i built an ai film studio |
| PROVEN | 13 | 0.73x | 1.17x | 2.86x | 2 | i built a studio with ai |
| **PROVEN** | 6 | **1.79x** | **4.74x** | 11.75x | **3** | **delete your second brain** |
| MIXED | 6 | 0.24x | 0.82x | 4.74x | 1 | second brain is useless |
| MIXED | 4 | 0.45x | 2.04x | 2.04x | 1 | why second brains fail |
| MIXED | 8 | 0.47x | 1.20x | 7.82x | 1 | i built ai agents to run my business |
| INCONCLUSIVE | 1 | — | — | — | — | i automated everything with ai |
| PROVEN | 26 | 0.30x | 0.88x | 4.53x | 2 | ai second brain that works |

**The cleanest proven signal in the whole investigation is the second-brain BACKLASH lane — and it's
essay-framed, not tutorial-framed:**
```
  4.74x   154,924    32,700   Why I Deleted My Second Brain: A Journey Back to Real Thinking
  2.48x    20,963     8,460   The Dark Side of a Second Brain
 11.75x   162,144    13,800   I Built a Second Brain That Fits in My Pocket (and You Can too)
```
Reachable channels (8,460 / 13,800 / 32,700), and the winners are titled like essays ("a journey back
to real thinking," "the dark side of") — squarely our register. The `useless / suck / why they fail`
phrasings are weaker (0.82×, 0.25×, 2.04×/1,620); **"delete / dark side" beats "useless."**

**Film-studio-as-build is REAL but MODEST, and the word "studio" is contaminated:**
- `i built an ai film studio` 61.46× = **ImagineArt promoting its own product** (same vendor trap as
  "ai film studio setup" 61.55× on 2026-08-06). Discard.
- `i built a studio with ai` PROVEN is **entirely Google AI Studio** (an app-builder product) — a
  coding-tutorial lane, not film. Discard.
- The genuine on-concept rows are *"I made a FILM with AI"*, not *"I built a filmmaking SYSTEM"*:
  *How I Made a Cinematic Film Using AI* 2.85× / 174k; *Filmmakers Hybrid Workflow (LTX Studio)*
  2.74× / 28,500. Above the hit line, but a **lower ceiling** than the assistant/second-brain/agent
  lanes and no reachable-size outlier.

`i built ai agents to run my business` — one strong reachable hit
(*AI Agents Army… Run my $28k/mo business* 7.82× / 12,200), rest weak; a business-automation (money)
register, adjacent to but not our essay identity.

---

## Verdicts

1. **Federation video hook = BUILD + SECOND-BRAIN-BACKLASH fusion.** Both halves proven, clean,
   reachable, essay-framed. The conflict ("they disagreed") **demotes from hook to the ~45%
   reversal** — it carries retention, not the click. Titling on "lying to each other" bets on a dead,
   meme-contaminated framing.
2. **On "just talking about building the Film Studio" (Terry's question):** not rejected — but the
   data says it's a *modest, lower-ceiling* lane, the demand is really for the *film result* not the
   *system tour*, and "studio" collides with vendor (ImagineArt) and product (Google AI Studio)
   content. **Strongest use: fold the Studio into the federation story as one of the two AIs** — it
   appears in the title as a character ("a second brain AND a film studio") without staking the hook
   on the weak "here's my studio architecture" framing. A standalone studio-build video is better told
   as "the film I made with it."
3. **Only the tool-survey framing stays rejected** (from 2026-08-06): "what each tool brings" is the
   review treadmill. Building your own system — assistant, second brain, agent team, or studio — is
   the strong lane.

**Candidate title shapes to lock or probe next (all fold the studio in, ride proven lanes, keep the
conflict as twist):**
- *"I Gave My AI a Second Brain and a Film Studio. Then They Turned On Each Other."*
- *"Everyone's Deleting Their Second Brain. I Built a Second One."*
- *"The Dark Side of Having Two Second Brains."*

Guardrail unchanged from [[feedback-channel-direction-held]]: essay, not build-log. We reference the
"delete your second brain" cluster as the frame we push *off from* — not as our own failure confession.
