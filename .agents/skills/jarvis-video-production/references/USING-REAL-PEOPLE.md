# Using Real People — safe-use guardrail (quotes, photos, clips)

**Not legal advice.** This encodes the practical discipline for putting real people in Byrddynasty
videos so the channel stays in the defensible "commentary/analysis" lane. When genuinely unsure about
a specific asset, take the conservative option.

## The one distinction that governs everything
- ✅ **Using REAL, already-existing** footage/photos/quotes of a real (usually public) figure **to
  analyze or comment on them** = the legitimate commentary lane (fair use + First-Amendment-protected
  commentary). This is what we do.
- ❌ **AI-GENERATING / faking** a real person (a synthetic "Sam Altman" image or voice) = banned.
  Likeness + fabrication + credibility risk. Never generate a real person's face or voice.

## The 6 rules (apply to any real-person asset)
1. **Real, never fabricated.** Only use footage/photos/quotes that actually exist. (Same standard as
   our GROUNDED verification — the quote/clip must trace to a real, cited source.)
2. **Short & transformative.** Seconds, not minutes. Use only enough to make the point, wrapped in
   OUR analysis. We comment *on* it; we don't rebroadcast it.
3. **About the subject.** The person's OWN public statement/interview about the very topic is the
   strongest position.
4. **Attribute.** Name + title + source + date on screen. Supports the commentary framing and our
   credibility. (The quote card does this by design.)
5. **Never imply endorsement.** Don't make it look like the person backs the channel or a product.
   That's the right-of-publicity line.
6. **No false factual claims** about the person. That's defamation — separate from images, and exactly
   why the fact-check step matters.

## What's cleared for use (Terry's standing call, 2026-07-28)
- **Quotes with attribution** — safest. Reporting what a real person publicly said, sourced. Default
  to the quote card.
- **Press photos, public-domain, and Creative Commons images** — OK. Prefer official press/handout
  photos, government/public-domain, or CC-licensed over random Getty/agency grabs.
- **Short real interview clips of the actual person talking** — OK **when relevant**; NOT required in
  every video. Keep them short, on-topic, attributed. (Terry handles clip selection.)

## Sourcing preference ladder (cleanest → touchiest)
1. Attributed quote text (no image) — the quote card, `--photo`/`--icon` omitted.
2. Public-domain / government / CC-licensed photo, or an official press/handout photo.
3. The person's own public post/interview still or a SHORT clip of them speaking, attributed.
4. ⚠ Licensed news-network footage (CNBC/ABC/etc., network bug visible) — the competitor's least-clean
   move. Fair use likely, but it invites a YouTube copyright *claim* (demonetization on that video),
   not usually a lawsuit. Use sparingly, keep short, and only when nothing cleaner exists.

## The quote card — `tools/make-quote-card.py`
The primary way to add human presence to a faceless build. Photo is optional:
```bash
# safest / on-brand default — elegant attributed quote, NO photo
make-quote-card.py --quote "…" --name "Gabe Newell" --title "Co-founder, Valve" \
  --date "IGN interview, 2011" --out <project>/hyperframes-v3/scenes/NN-quote-newell
# add a generic silhouette (no real likeness):     --icon
# add a REAL press/public-domain/CC photo:          --photo path/to/photo.jpg
```
Emits a faceless-conduit scene (dark navy, gold accents, Georgia serif quote typing in word-by-word),
all motion on the registered `tl`, passes `scene-validator.py`. When `--photo` is used, confirm the
image is real and rightsable per the ladder above.

## Interview / archival clips (when used)
Treat like any b-roll asset in Step 3, but: keep it SHORT (a few seconds), it must be the REAL person
(never AI-generated), attribute on screen, and prefer the cleanest source available. Not every video
needs one.
