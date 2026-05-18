# Video 12 HyperFrames Components

This folder is the first pass at turning the `14-design-system` static mocks into reusable HyperFrames building blocks.

## Files

- `index.html` renders the current proof composition: Segment 7, Cloudflare Code Mode.
- `components/byrd-components.css` contains shared design tokens, scene shell styling, browser mock, metric panel, event cards, and thesis bar styles.
- `components/byrd-components.js` contains reusable HTML builders and the Segment 7 GSAP timeline.
- `DESIGN.md` defines the visual identity used by this component library.
- `renders/segment-07-cloudflare-proof.mp4` is the rendered motion proof.
- `qa-frames/seg07/contact.jpg` is the QA contact sheet for the rendered proof.

## Current Components

- `sourceBadge()`
- `browserMock()`
- `metricCounter()`
- `eventCard()`
- `thesisBar()`
- `segmentShell()`
- `terminalMock()`
- `vscodeMock()`
- `comparisonSplit()`
- `sideAvatarFrame()`
- `phoneMock()`
- `dashboardPanel()`
- `lowerThird()`
- `ctaControls()`
- `decisionTable()`
- `architectureLayers()`
- `evidenceMosaic()`

## Preview

- `component-gallery.html` is a static browser preview of the reusable components. It is intentionally not a HyperFrames root composition so it does not interfere with Segment 7 rendering.

## Rendering Segment 7

```bash
cd video-12-mcp-token-stack/14-design-system
npm run check
npm run render:seg07
```

## Asset Guidance

Use HTML/CSS components for generic objects: terminals, phones, dashboards, cards, browser chrome, tables, charts, arrows, badges, and CTA controls.

Use real image/video assets when the viewer needs evidence or recognition: source screenshots, product pages, logos, a real app UI, a real terminal/screen recording, avatar footage, or photographic backgrounds.
