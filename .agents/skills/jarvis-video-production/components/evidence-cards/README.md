# Evidence cards — the cream document register, plus its two companions

Built + pixel-verified 2026-08-04. `hyperframes check` clean: 0 errors, **45/45 WCAG AA**.

| function | job (CONDUIT §4) |
|---|---|
| `mountDocCard` | a claim is on the record — mono kicker, serif head, hairline rules, label/value rows, rotated stamp |
| `mountStatHero` | one number is the point — count-up, kicker above, italic aside below |
| `mountLanding` | full-frame text — **titles and landings ONLY** |

Two doc cards side by side make the comparison split (paid vs consumed); the stat hero underneath
resolves the subtraction. That trio is the cold open.

## Files
`evidence-cards.html` · `build-demo.py` (run after every edit) · `demo/` (46s, real frozen figures)
· `demo/snapshots/contact-sheet.jpg`

## A card is not a text slide

`mountLanding` **is** CONDUIT's "plain full-frame text card is permitted only as a title or a
landing" exception, and must not be used for anything else. Every other beat gets a card with
structure — kicker, head, rules, label/value rows — because the structure is what makes it read as
a document rather than a caption. Rows resolve within ~1.2s of the card appearing (CONDUIT §5);
held ghosted longer it reads as a dead frame.

## Give every card an `id`

Fixed `slot: 'a' | 'b'` was tried first and is a trap: mounting a second card into a slot wipes the
first one's `innerHTML` while its tweens keep targeting the same ids, so the **earlier card silently
renders the later card's text**. Cards now create their own container inside `#ec-host`. The layout
checker caught this as a `text_occluded` between two cards that should never have coexisted — the
real defect was one card overwriting another, which no gate would have named.

## Three fixes worth not undoing

1. **`line-height: 1` on a 132px number lets glyphs ride into the kicker's box** → `content_overlap`.
   The stat hero's number needs `line-height: 1.16` and real top margin.
2. **Name the font you actually mean.** `Georgia` is aliased to EB Garamond at render time, so
   preview and render disagree. The stack is `'Playfair Display','EB Garamond',serif`.
3. **Kicker on cream was 3.6:1.** Cream backgrounds eat contrast — anything muted on `#F2EDE0`
   needs checking, not eyeballing. `#6B5E40` clears AA.

Plus the two inherited build-script traps, re-armed: extraction anchors on **BLOCK marker comments**,
and BLOCK B is taken **marker-to-marker**.

## Counters are seek-safe
Proxy object + `textContent` in `onUpdate` — fires on seek, which is what the deterministic renderer
does every frame. Never `setInterval`/`rAF`; both render FROZEN.

## Where they're used first
`jarvis-private/video-projects/claude-code-11-billion-tokens` — S01 (paid / consumed / the gap),
S07 (what we cannot tell you), S10 (the landing). Cue schedule in that project's `VISUAL-MAP.md` §4.
