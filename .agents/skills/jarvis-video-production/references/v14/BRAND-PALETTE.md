# V14 Brand Palette

## Per-brain accent colors

Each "brain" intro scene (4/5/6) is monochrome accent in its brand color. The router/orb scenes (1/8/9/10/12) use gold.

| Brain | Hex | Used in |
|---|---|---|
| Claude (Anthropic) | `#d97757` (sunset orange) | Scenes 4 + Claude references throughout |
| Codex (OpenAI) | `#10a37f` (emerald green) | Scenes 5 + Codex references throughout |
| Gemini (Google) | `#4285f4` (sapphire blue) | Scenes 6 + Gemini references throughout |
| JARVIS / Router | `#FFD700` (gold) | Scenes 1, 8, 9, 10, 12, all router moments |

## Semantic colors

| Token | Hex | Purpose |
|---|---|---|
| Error / negation | `#FF5050` | Red strike-throughs ("don't", "wrong"), problem callouts |
| Success / strength | `#4ADE80` | Green strength rows, positive ✓ checks |
| Text primary | `#ffffff` | Body text on dark stage |
| Text secondary | `rgba(255,255,255,0.55)` | Subheadings, kickers, captions |
| Text muted | `rgba(255,255,255,0.35)` | Disabled / dimmed text |

## Stage tokens

| Token | Value | Purpose |
|---|---|---|
| Stage black | `#050505` | Body background, scene root |
| Card gradient | `linear-gradient(180deg, #131418 0%, #0a0b0e 100%)` | Hero cards, tradeoff cards |
| Tile gradient | `linear-gradient(180deg, #1a1c20 0%, #0e0f12 100%)` | Spec-grid tiles |
| VSCode bg | `#1e1e1e` | Code panes |
| VSCode line numbers | `#6e6e6e` | Gutter color |
| VSCode chrome | `#2d2d30` | Title bar |
| VSCode statusbar | `#007acc` | Bottom status strip |
| Vignette | `radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%)` | Edge darken, layer 60 |

## Glow / drop-shadow per brain

The signature "brand glow" around a brain icon:
```css
.brain-card.claude img  { filter: drop-shadow(0 0 50px rgba(217, 119, 87, 0.55)); }
.brain-card.codex img   { filter: drop-shadow(0 0 50px rgba(16,  163, 127, 0.55)); }
.brain-card.gemini img  { filter: drop-shadow(0 0 50px rgba(66,  133, 244, 0.55)); }
.brain-card.jarvis img  { filter: drop-shadow(0 0 50px rgba(255, 215,   0, 0.55)); }
```

For final-hero shots, double the intensity:
```css
.final-stage .brain-glow { filter: drop-shadow(0 0 80px rgba(<brand>, 0.55)); }
```

## When to mix vs. when to lock

**Lock to one color per scene.** Within a single scene, pick ONE accent color and use only that color for pulses, badges, and accents. The exception:

- Scenes that show ALL THREE BRAINS (Scene 1, 8, 9) — use each brain's color for that brain's element. Gold accents the orb/router.
- Scene 11 montage — each routing card uses its destination brain's color.

**Don't:**
- Mix two brain colors in the same shot (looks chaotic).
- Use red `#FF5050` as a brand accent — it reads as error.
- Use gold for anything other than the router/orb/final-time accents.

## CSS variable convention

V14 compositions use inline hex literals rather than CSS variables. Reason: composition files are self-contained, agents read them in isolation, and inline hex is greppable.

If you find yourself wanting variables, you've probably written enough shared CSS that it should move into `lib/byrd-transitions.css` instead.

## Typography

V14 uses system fonts. No web font loads. Fallback chain:

```css
font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
font-family: 'Menlo', 'Consolas', monospace;  /* for code / tabular */
```

For final-pass production, add `@font-face` for Menlo/Consolas to avoid the lint warning. Inter is widely available on macOS so it's usually fine.

## Sizing scale

V14 typography stays inside a defined scale:

| Class | Size | Weight | Usage |
|---|---|---|---|
| `.kicker` | 26px | 800 | "BRAIN ONE" badges |
| `.label`, `.row-label` | 16–18px | 700 | Tile labels, row tags |
| `.sub`, `.desc` | 30–32px | 600 | Subheadings |
| `.row-text`, `.what` | 38–84px | 600–900 | Card body, verb statements |
| `.title`, `.caption` | 76–110px | 900 | Hero copy |
| `.title-line` | 160–200px | 900 | Title slams |
| `.punch-slam` | 200–220px | 900 | Punch-in slams |

Letter-spacing: `0.02em` to `0.04em` for headlines; `0.18em` to `0.4em` for kickers/badges/labels.
