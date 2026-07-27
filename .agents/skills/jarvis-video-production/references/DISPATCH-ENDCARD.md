# Today's Dispatch end-card (daily 3-video connector)

The connective device for a daily **3-video set**. Drops in as the **final scene**
(~12s) of EACH of the day's three videos. It names the day's set and marks the
other two as "watch next" — while leaving the right side clear for YouTube's
**clickable native end-screen elements** (the real routing tool).

**Placement rule (load-bearing):** the end-card appears ONLY at the end, NEVER
during the hook. The channel is retention-gated; a competing-topics rail in the
first 30-60s costs more than it earns. Connection happens on the way *out*.

## Why an end-card, not a ticker
Breaking Points runs a topic ticker DURING segments because it has a large loyal
audience. A growing faceless channel can't spend hook-window attention on
cross-promo. So we take the same instinct and move it to the doorway: end-card +
YouTube end screens (clickable) + a daily playlist + pinned comment.

## Generate it
```
tools/make-dispatch-endcard.py \
  --theme "The Little Tricks Beating Big AI" \
  --titles "Video A title|Video B title|Video C title" \
  --current 1 \                     # which of the 3 is THIS video (dimmed "YOU'RE WATCHING")
  --dispatch-line "Today's dispatch: ..." \
  --duration 12 \
  --out <project>/hyperframes-*/scenes/99-dispatch-endcard
```
Render each of the three videos with `--current` set to 1, 2, 3 respectively.

- Output: a faceless-conduit scene (dark navy bed, gold `#E0B84A`, Georgia serif
  heads, JetBrains-mono kickers), all motion on the registered `tl`, passes
  `tools/scene-validator.py`. Silent by default (no VO needed).
- The dashed **END-SCREEN ZONE** on the right marks where to drop the two video
  end-screen elements + subscribe in the YouTube editor (last ~20s).

## Feeding it
The daily-ideas email (`agent-sdk/scripts/daily-ai-ideas.ts`, emailed 9:30am)
ends with a **"Today's Dispatch"** block: theme + the 3 titles + the dispatch
line — copy those straight into the flags above. So the daily set → end-card is
a ~1-minute step.

## The full connection stack (in order of value)
1. **YouTube end screens** — the clickable thumbnails (last 20s). The real router.
2. **Daily playlist** ("Dispatch — <date>") + **pinned comment** linking the other two.
3. **This end-card** — names the set, gives the day a "show" identity.
