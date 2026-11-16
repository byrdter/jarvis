# Asset Inventory

This is the pre-production requirement list. No asset should be generated before visual-treatment approval.

## Library Audit

- Canonical source: `asset-library/assets.db`
- Checked 2026-08-03: **883 indexed assets—530 images and 353 videos**.
- Existing relevant categories include semiconductor fabrication, circuit/data flow, rural infrastructure, autonomous vehicles, hospitals, factories, warehouse robots, offices, phones, diverse workers, and network imagery.
- Selection is database-first by meaning, `symbolizes`, and `usable_as`. Folder browsing is not the sourcing method.
- Full per-scene three-clip floor, single-use assignments, unique backgrounds, and current gap list: `MOTION-ASSET-MAP.md`.
- Staged 2026-08-04: 31 unique library clips plus five generated source stills across `03-scenes/s00`–`s11`. Every scene now contains three local media assets; the five stills become the remaining clip-floor items after Terry returns approved I2V renders.

## Required Assets

| Asset | Semantic Key | Source Path / URL | Scene(s) | Local Scene Copy | Status | Notes |
|---|---|---|---|---|---|---|
| Nature paper result cards | proposed `proof-6g-photonic-chip-nature-2025` | https://www.nature.com/articles/s41586-025-09451-8 | S02, S03, S05 | cards frozen; scene copies staged | ready | Five focused mobile-readable cards cover 0.5–115 GHz, 100 Gbps, atmospheric absorption, chip area, and the 1.3 m path |
| Nature apparatus/method proof | proposed `proof-6g-lab-apparatus-nature-2025` | same | S05 | `02-assets/source-proofs/cards/nature-1_3m.png` | ready | Substantiates the short path while the approved pullback clip reveals the external bench |
| OFC 2022 abstract proof | proposed `proof-370ghz-ofc-2022` | https://opg.optica.org/abstract.cfm?uri=OFC-2022-M3Z.9 | S05 | `02-assets/source-proofs/cards/ofc-2022-103_125gbps.png` | ready | Exact 103.125-Gbps abstract sentence, source, and date preserved |
| ITU capabilities/requirements crop | proposed `proof-imt2030-requirements-2026` | ITU links in claim map | S03, S04, S06, S10 | pending | needed | Prefer multiple focused crops over one unreadable page |
| NICT 60/300-GHz demo crop | proposed `proof-nict-dual-band-2026` | https://www.nict.go.jp/press/2026/05/27-1.html | S03 | pending | needed | Translate labels if necessary; preserve provenance |
| CityUHK ISAC mechanism crop | proposed `proof-cityuhk-isac-2025` | claim map URL | S06 | pending | needed | Source proof for sensing mechanism |
| Human-in-spatial-map hero | `generated-human-radio-spatial-map` | `02-assets/generated-stills/ka01-network-sensing-hero-v1.png` | thumbnail, S06 | staged in S06 | still-created | Awaiting Terry approval; thumbnail typography will be composited separately |
| Ordinary-room sensing bed | `generated-room-rf-sensing` | `02-assets/generated-stills/ka01-ordinary-room-rf-sensing-v1.png` | S09 | staged in S09 | still-created | Normal apartment, cane, no visible camera; awaiting approval |
| Photonic light-path macro | `generated-photonic-light-path` | `02-assets/generated-stills/ka01-photonic-light-path-v1.png` | S02 | staged in S02 | still-created | Illustration; pair with real Nature proof |
| Optical-bench reversal | `generated-optical-bench-reversal` | `02-assets/generated-stills/ka01-optical-bench-reversal-v1.png` | S05 | staged in S05 | still-created | Load-bearing pullback still; awaiting approval |
| Horn short-link close shot | `generated-horn-short-link` | `02-assets/generated-stills/ka01-horn-short-link-v1.png` | S05 | staged in S05 | still-created | Exactly two horns; ruler added in HyperFrames |
| City/rural/disaster environments | search existing asset library first | asset-library | S03 | staged scene-local | ready | Three unique location/mobility clips selected from the library |
| Road/warehouse/port/hospital vignettes | search library, generate only gaps | asset-library / original | S07 | staged scene-local | ready | Three unique machine-coordination clips; no competitor footage |
| 4G/5G lived-use montage | search existing library first | asset-library | S01 | staged scene-local | ready | Three unique phone/business clips selected from the library |

## New Assets To Add To Manifest

| Asset | Proposed Key | File Name | Category | Metadata Needed |
|---|---|---|---|---|
| Human spatial sensing hero | `generated-human-radio-spatial-map` | `human-radio-spatial-map.png` | brain / generated image | prompt, generation date, channel, symbolizes, usable_as |
| Ordinary sensing room | `generated-room-rf-sensing` | `room-rf-sensing.mp4` | generated clip | prompt/model, duration, audio=no, evidence state=illustration |
| Nature result proofs | `proof-6g-photonic-chip-nature-2025` | `nature-*.png` | web-proof | Complete in each JSON sidecar: URL, capture date, paper date, exact highlighted claim |
| Nature apparatus proof | `proof-6g-lab-apparatus-nature-2025` | `nature-1_3m.png` | web-proof | Complete in JSON sidecar: URL, capture date, method reference |
| OFC proof | `proof-370ghz-ofc-2022` | `ofc-2022-103_125gbps.png` | web-proof | Complete in JSON sidecar: URL, capture date, exact quoted result |

## External Clips

| Clip | Tool | Prompt / Brief Location | Duration | Audio | Status |
|---|---|---|---:|---|---|
| Person inside radio-derived spatial map | Terry's selected I2V tool | `02-assets/approved-clips/s06-person-radio-spatial-map.mp4` | 10s approved; 4–5s used | silent | reviewed and locked |
| Ordinary room, subtle radio mesh movement | Terry's selected I2V tool | `02-assets/approved-clips/s09-ordinary-room-radio-sensing.mp4` | 6.5s approved; 4–5s used | silent | reviewed and locked; generated tail rejected |
| Photonic light-path macro | Terry's selected I2V tool | `02-assets/approved-clips/s02-photonic-light-path.mp4` | 7s approved; 3–5s used | silent | reviewed and locked |
| Chip-to-optical-bench reversal | Terry's selected I2V tool | `02-assets/approved-clips/s05-chip-to-optical-bench-pullback.mp4` | 12s approved; annotations change every 2–4s | silent | reviewed and locked |
| Horn-antenna short laboratory link | Terry's selected I2V tool | `02-assets/approved-clips/s05-horn-antenna-short-link.mp4` | 4s approved | silent | reviewed and locked; animated ruler mandatory |

**Production division:** Codex creates and freezes the source stills and writes complete I2V prompt packets. Terry generates the clips. Codex reviews and integrates the returned clips. Statuses: needed, still-created, still-approved, prompt-ready, Terry-generating, delivered, reviewed, locked.

## Site Prototypes / Captures

| Site | Role | URL / Location | Scene(s) | Capture Plan | Access / Privacy | Status |
|---|---|---|---|---|---|---|
| Nature | on-screen visual source | claim map URL | S02, S03, S05 | six focused evidence cards from the paper text | public article / archived research copy | captured and staged |
| ITU IMT-2030 | on-screen visual source | claim map URLs | S03, S04, S06, S10 | focused screenshots | public | planned |
| NICT | on-screen visual source | claim map URL | S03 | focused screenshot + translated annotation | public | planned |
| CityUHK | on-screen visual source | claim map URL | S06 | focused screenshot | public | planned |

The Nature and OFC proof cards are frozen under `02-assets/source-proofs/cards/` with JSON provenance sidecars. ITU, NICT, CityUHK, and NIST proof cards remain to be created before their scenes can render.

## Asset Risks

- Generated imagery may falsely imply a deployed product. All such frames need a PLAUSIBLE or ILLUSTRATION label.
- Paper figures may be too dense for mobile. Recompose only the relevant measurement while showing an authentic cream source crop alongside it.
- Search the asset database before commissioning generic locations; do not duplicate existing beds.
- Freeze final downloaded/generated media locally and record provenance before scene construction.
- Each scene must have a different real background and at least three scene-local, single-use clips; an asset does not count until it has been copied into that scene's `assets/` directory.
- A still requires an authored Ken Burns/parallax/annotation action. No visual state may remain unchanged for five seconds.
