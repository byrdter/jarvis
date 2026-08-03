# Asset Inventory

This is the pre-production requirement list. No asset should be generated before visual-treatment approval.

## Library Audit

- Canonical source: `asset-library/assets.db`
- Checked 2026-08-03: **883 indexed assets—530 images and 353 videos**.
- Existing relevant categories include semiconductor fabrication, circuit/data flow, rural infrastructure, autonomous vehicles, hospitals, factories, warehouse robots, offices, phones, diverse workers, and network imagery.
- Selection is database-first by meaning, `symbolizes`, and `usable_as`. Folder browsing is not the sourcing method.
- Full per-scene three-clip floor, single-use assignments, unique backgrounds, and current gap list: `MOTION-ASSET-MAP.md`.

## Required Assets

| Asset | Semantic Key | Source Path / URL | Scene(s) | Local Scene Copy | Status | Notes |
|---|---|---|---|---|---|---|
| Nature paper chip figure/crop | proposed `proof-6g-photonic-chip-nature-2025` | https://www.nature.com/articles/s41586-025-09451-8 | S00, S02, S05 | pending | needed | Crop only the exact figure/text used; capture source/date |
| Nature apparatus/method crop | proposed `proof-6g-lab-apparatus-nature-2025` | same | S05 | pending | needed | Must substantiate external components and 1.3m path |
| OFC 2022 abstract crop | proposed `proof-370ghz-ofc-2022` | https://opg.optica.org/abstract.cfm?uri=OFC-2022-M3Z.9 | S00, S05 | pending | needed | Show 103.125-Gbps net result and date |
| ITU capabilities/requirements crop | proposed `proof-imt2030-requirements-2026` | ITU links in claim map | S03, S04, S06, S10 | pending | needed | Prefer multiple focused crops over one unreadable page |
| NICT 60/300-GHz demo crop | proposed `proof-nict-dual-band-2026` | https://www.nict.go.jp/press/2026/05/27-1.html | S03 | pending | needed | Translate labels if necessary; preserve provenance |
| CityUHK ISAC mechanism crop | proposed `proof-cityuhk-isac-2025` | claim map URL | S06 | pending | needed | Source proof for sensing mechanism |
| Human-in-spatial-map hero | proposed `generated-human-radio-spatial-map` | original generation | thumbnail, S06, S10 | pending | needed | Thumbnail and episode can share concept but not necessarily exact crop |
| Ordinary-room sensing bed | proposed `generated-room-rf-sensing` | original generation/clip | S06, S09 | pending | needed | Avoid futuristic lab; ordinary home or care setting |
| City/rural/disaster environments | search existing asset library first | asset-library | S03 | pending | needed | Three locations, consistent grade |
| Road/warehouse/port/hospital vignettes | search library, generate only gaps | asset-library / original | S07 | pending | needed | No borrowed competitor footage |
| 4G/5G lived-use montage | search existing library first | asset-library | S01 | pending | needed | Maps/video/ride commerce plus fixed wireless/private network |

## New Assets To Add To Manifest

| Asset | Proposed Key | File Name | Category | Metadata Needed |
|---|---|---|---|---|
| Human spatial sensing hero | `generated-human-radio-spatial-map` | `human-radio-spatial-map.png` | brain / generated image | prompt, generation date, channel, symbolizes, usable_as |
| Ordinary sensing room | `generated-room-rf-sensing` | `room-rf-sensing.mp4` | generated clip | prompt/model, duration, audio=no, evidence state=illustration |
| Nature chip proof | `proof-6g-photonic-chip-nature-2025` | `nature-chip-proof.png` | web-proof | URL, capture date, paper date, exact claim |
| Nature apparatus proof | `proof-6g-lab-apparatus-nature-2025` | `nature-apparatus-proof.png` | web-proof | URL, capture date, method/figure reference |
| OFC proof | `proof-370ghz-ofc-2022` | `ofc-2022-proof.png` | web-proof | URL, capture date, exact quoted figure |

## External Clips

| Clip | Tool | Prompt / Brief Location | Duration | Audio | Status |
|---|---|---|---:|---|---|
| Person inside radio-derived spatial map | Terry's selected I2V tool | `I2V-PROMPT-PACK.md` S06-BR02 | 6–8s generated; 3–5s used | silent | still needed |
| Ordinary room, subtle radio mesh movement | Terry's selected I2V tool | `I2V-PROMPT-PACK.md` S09-BR02 | 5–7s generated; 3–5s used | silent | still needed |
| Photonic light-path macro | Terry's selected I2V tool | `I2V-PROMPT-PACK.md` S02-BR03 | 6–8s generated; 3–5s used | silent | still needed |
| Chip-to-optical-bench reversal | Terry's selected I2V tool | `I2V-PROMPT-PACK.md` S05-BR01 | 8–10s generated; ≤5s segment used | silent | still needed |
| Horn-antenna short laboratory link | Terry's selected I2V tool | `I2V-PROMPT-PACK.md` S05-BR03 | 6–8s generated; 3–5s used | silent | still needed |

**Production division:** Codex creates and freezes the source stills and writes complete I2V prompt packets. Terry generates the clips. Codex reviews and integrates the returned clips. Statuses: needed, still-created, still-approved, prompt-ready, Terry-generating, delivered, reviewed, locked.

## Site Prototypes / Captures

| Site | Role | URL / Location | Scene(s) | Capture Plan | Access / Privacy | Status |
|---|---|---|---|---|---|---|
| Nature | on-screen visual source | claim map URL | S00, S02, S05 | focused screenshots / PDF crops | public article / archived research copy | planned |
| ITU IMT-2030 | on-screen visual source | claim map URLs | S03, S04, S06, S10 | focused screenshots | public | planned |
| NICT | on-screen visual source | claim map URL | S03 | focused screenshot + translated annotation | public | planned |
| CityUHK | on-screen visual source | claim map URL | S06 | focused screenshot | public | planned |

## Asset Risks

- Generated imagery may falsely imply a deployed product. All such frames need a PLAUSIBLE or ILLUSTRATION label.
- Paper figures may be too dense for mobile. Recompose only the relevant measurement while showing an authentic cream source crop alongside it.
- Search the asset database before commissioning generic locations; do not duplicate existing beds.
- Freeze final downloaded/generated media locally and record provenance before scene construction.
- Each scene must have a different real background and at least three scene-local, single-use clips; an asset does not count until it has been copied into that scene's `assets/` directory.
- A still requires an authored Ken Burns/parallax/annotation action. No visual state may remain unchanged for five seconds.
