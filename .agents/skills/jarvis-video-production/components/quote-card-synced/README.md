# Word-synced citation card — the LA "karaoke" technique

Implements `.claude/rules/video-production-standard.md` §10.2. A cream evidence card whose quote
**highlights word-by-word in lockstep with the VO reading it** (pending words dim, each snaps to full
ink at its VO word-start). Built + pixel-verified 2026-07-31.

## Files
- `quote-card-synced.html` — the component. Three paste blocks (style / markup / script) + one call,
  `mountQuoteCard(tl, opts)`. Full usage in the file header.
- `demo/` — a 13s render proving the sweep. `hyperframes check` passes clean; verified in the pixels
  (1.6s all-pending → 5.0s first clause lit → 8.5s sweep advanced). Re-render after any edit; it's the
  regression test.

## The one rule that makes it honest
**The word timings MUST come from the VO transcript, never eyeballed.** At build time:

```
python3 tools/cue.py <scene-transcript.json> "<exact quote words>"
```

or read the `{text,start}` token array directly and slice the quote's span. Pass as
`opts.words = [{w:"before",t:12.30}, {w:"those",t:12.54}, ...]`. The demo *fabricates* its timings
(~0.30s/word) purely to exercise the mechanism — a real scene that fabricates them will drift off the
voice, which defeats the entire technique.

## Why it can't hit the spine's overwrite bug
Each word is ONE independent opacity tween (dim→full) on its OWN element at its OWN start time. No two
tweens share a property+element, so the breath-vs-resolve overwrite that bit the spine cannot recur.
All motion on the registered `tl` — a bare `gsap.to` renders frozen.

## Where it's used first
`ai-makes-you-dumber` (6 cards) and `mcp-your-tools` (3 cards), per their SPINE-AND-ASSETS plans.
Standing technique for **every** evidence card from now on.
