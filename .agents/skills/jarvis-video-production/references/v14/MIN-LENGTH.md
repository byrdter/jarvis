# V14 Minimum Length & Variety

## Hard rules

- **Every V14 video MUST run at least 8 minutes total.**
- **Target range: 10–15 minutes** (the channel's sweet spot for YouTube ranking + educational pacing)
- **Cap: 18 minutes** (longer videos fall off the watch-time cliff unless the topic genuinely demands it)
- **A pilot under 8 minutes is incomplete.** Don't ship it.

## Why

Watch-time is what YouTube optimizes for. An 8-minute video that holds 70% retention beats a 4-minute video that holds 90% — total watch-seconds matters more than retention rate. The Byrddynasty audience is technical and patient; we have the headroom to go long.

## Building to length WITHOUT padding

Length should come from MORE INFORMATION, not from stretched pacing. Three legitimate ways to add minutes:

### 1. Add interlude segments between major scenes (30–60s each)

Examples for Video 14:
- **"How we got here"** — 4-shot history montage with real news/blog screenshots of model releases (Claude 3 → 4 → 4.5 → 4.7, GPT-4 → 5, Gemini 1.5 → 2.5 → 3)
- **"What we tried first"** — show 2 failed approaches before the router landed (always-Opus, hardcoded if/else)
- **"The router in your editor"** — meta moment: Claude Code editing `router.ts` itself
- **"A day with the router"** — time-lapse / day-in-the-life of routing decisions, real chat windows, counters

### 2. Expand existing scenes with more examples

If a scene shows 3 of something, ask: would 5 or 6 land better? Don't blindly multiply, but a 3-card rotation that becomes a 5-card rotation adds 12–20 seconds AND raises perceived completeness.

For V14 specifically: Scene 9 (Live Decisions) is the obvious one — has 3 examples, could have 5 or 6.

### 3. Add deep-dive moments

When the main script mentions a concept in one sentence, branch off for 60–90 seconds to go deeper. Example: Scene 10 mentions "code presence" as one of four signals. A 60-second sub-scene could show how `code_presence` is actually computed — regex patterns, attachment detection, threshold tuning.

These reward the technical audience and prove the depth of the work without padding the main thread.

## What padding looks like (don't do this)

- Stretching a 5-second visual hold to 8 seconds with no new information
- Slowing down VO with `atempo` filters until 5 minutes becomes 8
- Repeating the same shot type 6 times in a row
- Using `timeScale` to extend visual animations

These tactics get caught by the variety check below and by the audience's attention budget. They will tune out.

## The variety quota

If your video is 12 scenes, you need at least **6 distinct shot-type categories** represented across them. Categories:

1. Title slam / pivot text
2. Hero card / final hero
3. Tradeoff card / N-tile grid
4. Real-screenshot overlay
5. Punch-in phrase
6. 3-card rotation / rapid montage
7. Orb-and-paths SVG
8. VS Code mock / code reveal
9. Runway cinematic B-roll
10. Pixel-art B-roll
11. Architecture diagram / flow chart
12. Stylized data-viz beat (counter, bar, gauge, etc.)

V14 used: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10. That's 10/12 — strong. The variety quota is met by USING these types in different scenes, not by jamming all of them into one.

**Anti-pattern:** 3 or more consecutive scenes that all use the same primary shot type (e.g. three back-to-back "hero card with brain icon" intros). Break them up by sandwiching a different vocabulary entry between.

## Adding to V14 — concrete examples

To bring V14 from 5:12 to 9:30, here's the proven approach (4 new segments, total ~4:18):

| Insertion point | Working title | Style | Runtime |
|---|---|---|---|
| Before Scene 8 | "How we got here" | News/blog screenshots montage + timeline | ~45s |
| Between 9 and 10 | "What we tried first" | Two failed-approach demos + transition | ~60s |
| Between 9 and 10 | "The router in your editor" | Real terminal session — Claude Code editing router.ts | ~50s |
| Before Scene 11 | "A day with the router" | Day-in-the-life montage, counters, real chats | ~60s |
| Within Scene 9 | Add 3 more examples (total 6) | Same 3-card pattern, more cases | ~30s |

That puts V14 at ~9:30, well within the 8–15 minute target with no stretching.

## Future videos — design to length up-front

When drafting a new V14 video, work backward from the target:

| Target | Active VO time | Visual breathing | Scene count |
|---|---|---|---|
| 8 min | ~5 min VO | ~3 min visual | 10–12 scenes |
| 10 min | ~6:30 VO | ~3:30 visual | 12–14 scenes |
| 12 min | ~8 VO | ~4 visual | 14–16 scenes |
| 15 min | ~10 VO | ~5 visual | 16–20 scenes |

At ~140 wpm, the VO column translates to word counts:
- 8 min → ~700 words VO
- 10 min → ~910 words VO
- 12 min → ~1120 words VO
- 15 min → ~1400 words VO

Write the script to the word count BEFORE breaking into scenes. If your draft VO is under target, brainstorm what's missing — examples, deep dives, history, "what we tried first," interludes.
