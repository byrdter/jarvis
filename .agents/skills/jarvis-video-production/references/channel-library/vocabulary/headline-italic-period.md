# Headline With Italic Period

**STATUS:** proven
**Channel fit:** Byrddynasty (signature device — do not export to other channels casually)
**Tone fit:** educational, editorial

## Use case
Every Byrddynasty module's title beat uses this device. The headline is a single noun with a period; the period is italicized in warm brown. It is the channel's typographic signature.

## Reference implementation
See [`editorial-spread.md`](editorial-spread.md). Pattern:
```html
<h1 class="headline"><em>Tools.</em></h1>
```
```css
.headline em { font-style: italic; color: #5B4738; font-weight: 500; }
```

## Anti-patterns
- Don't use this for non-Byrddynasty channels without explicit permission — it's load-bearing channel identity.
- Don't use it for multi-word headlines (e.g., "Foundation Model.") — only single nouns. Multi-word headlines lose the rhythm.
- Don't change the brown — `#5B4738` is the warm tone that complements the cream stage. Other browns clash.

## Example beats
- See `editorial-spread.md` example list.
