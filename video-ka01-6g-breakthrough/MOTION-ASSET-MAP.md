# Motion and Asset Map

This is a hard production contract for the 6G episode, not a stylistic suggestion.

## Non-Negotiable Motion Rule

- **No visible state may remain unchanged for five seconds.** Design for a meaningful new event every **2–4 seconds** so render and master compression never push a borderline hold over the limit.
- A qualifying event can be a new clip or still, a source roll, a person entering the composition, a side panel, callout, highlight, counter, diagram path, node change, image replacement, crop/zoom, parallax move, or camera reframe.
- A still image is not static when it has an authored Ken Burns move, parallax separation, mask reveal, annotation, or image-to-image handoff. Grain alone does not count.
- HyperFrames ambient drift prevents literal freezing, but it does **not** replace narrative change. Every event must either advance the claim, expose evidence, orient the viewer, or reset attention.
- Every animation must live on the registered HyperFrames `tl`. No free `gsap.to()` calls and no infinite repeats.
- Beat timing is anchored to actual VO word timestamps after recording. This map defines the event sequence; `cue.py` supplies the final times.

## Per-Scene Asset Floor

Each scene requires:

1. One unique real visual background: a library/generated image or video bed, never the flat basefill alone.
2. At least three single-use video clips staged locally in the scene's `assets/` folder.
3. Additional stills, real people, web-rolls, papers, diagrams, and HyperFrames actions as the scene requires.
4. No recognizable literal clip loop. A clip plays once and exits before its loop point. Only abstract shader/particle beds may repeat.

The three clips are a floor, not a command to cut every five seconds. They can enter as full-screen breaths, picture-in-picture evidence, masked side panels, backgrounds under a diagram, or short human inserts. Most change density should come from motion inside the composition.

## Database-First Sourcing

- Canonical database: `asset-library/assets.db`
- Current inventory checked 2026-08-03: **883 assets—530 images and 353 videos**.
- Query by meaning, `symbolizes`, and `usable_as`; do not browse folders as the primary method.
- Copy selected assets into each scene; do not symlink.
- Outside assets are single-use across this episode. Only assets created specifically for this episode may recur where the visual spine requires continuity.
- Represent different races, genders, and ages across human shots.

## Scene Motion and Asset Plan

Names marked **LIBRARY** are current database candidates, not locked selections. **NEW** means the database does not yet contain a sufficiently specific asset and a gap remains after final query/review.

| Scene | Unique background | Three required clip roles | Meaningful screen-change sequence; maximum gap 4s |
|---|---|---|---|
| S00 · 35s | Macro photonic-chip or wafer bed, darkened | **LIBRARY:** `clip-semiconductor-wafer-fab.mp4`; `bg-data-flow-cyan.mp4`; `bg-neural-network-3d.mp4` | 0–3 RF trace draws; 3–6 wafer clip; 6–9 `206.25` source roll; 9–12 chip measurement; 12–16 data-flow clip; 16–20 `1.3 m` method crop; 20–24 dates split; 24–28 network clip; 28–32 human silhouette forms; 32–35 five nodes lock |
| S01 · 45s | Crowded station or mixed-generation city bed | **LIBRARY:** `clip-headphones-phone-night.mp4`; `office-vibrant.mp4`; `manager-tablet-inventory.mp4` | 4G still montage changes every 2–3s; phone clip; speedometer grows; office clip enters from side; fixed-wireless card resolves; tablet worker clip; marketing layer fades; SPEED node unlocks; final 4s human breath retains camera push |
| S02 · 50s | Different semiconductor/fibre laboratory still | **LIBRARY:** `GlowingDataPacket_CircuitBoard.mp4`; `clip-two-researchers-whiteboard.mp4`; **NEW:** photonic-light-path macro | Light enters at frame 0; chip layers separate; circuit-board clip; frequency ruler sweeps; band slot changes every 2–3s; researchers appear beside proof; 100-Gb/s counter; new optical macro; 120-Gb/s result lands separately; equipment/distance question appears |
| S03 · 50s | Rural communications landscape | **LIBRARY:** `datacenter-revolt__br_02b_pylons-farmland.mp4`; `clip-autonomous-car-highway-lidar.mp4`; `fork-road-drone.mp4` | City map pans; high-band beam blocks; pylons clip; rain attenuation overlay; rural route draws; car clip; satellite arc arrives; fork-road clip; NICT web-roll scrolls; 60/300-GHz routes swap; REACH node unlocks |
| S04 · 70s | Transit concourse or field-service environment | **LIBRARY:** `person-pointing-at-screen2.mp4`; `clip-team-around-monitor-engaged.mp4`; `celebrity-cac-subsidy__pov-phone-in-hand-notification.mp4` | Person/glasses still pushes; device→edge→cloud paths animate; latency chip changes; pointing-person clip; battery lock pops; team clip; compute route reverses; phone notification clip; field-tech overlay; small-business cost meter; three dependencies close; INTELLIGENCE unlocks |
| S05 · 45s | Real optical bench or dark lab background distinct from S02 | **NEW:** optical bench pullback; **LIBRARY:** `clip-semiconductor-wafer-fab.mp4` is **not available here if locked in S00**, so select another fab clip; **NEW:** horn-antenna link | Chip holds with slow push for <3s; camera starts continuous pullback; lasers appear; amplifiers appear; detectors appear; fab/lab clip; horn antennas enter; 1.3-m ruler draws; apparatus clip; 2022 paper slides left; 2025 paper slides right; correction stamp; map rotates and SPEED moves outward |
| S06 · 60s | Ordinary care room, not a futuristic laboratory | **LIBRARY:** `hallucinations-v6__br-02a_corridor.mp4`; `hallucinations-v6__br-10a_hands-of-care.mp4`; **NEW:** diverse person inside radio-derived spatial mesh | Room pushes inward; corridor clip; person appears; radio paths draw one by one; spatial-mesh clip; object contour resolves; movement trail; hands-of-care clip; fall inference popup; `SEE` strikes to `INFER`; 1–10cm ruler closes; privacy question slides in; SENSING moves inward |
| S07 · 60s | Port or machine-coordination overview | **LIBRARY:** `clip-autonomous-car-highway-lidar.mp4` is unavailable if locked in S03, so source alternate vehicle clip; `clip-warehouse-robots-fulfillment.mp4`; `clip-smart-factory-robotic-arm.mp4`; **NEW:** port/hospital coordination if needed | Four-grid slots appear ghosted and resolve within 1.2s; vehicle clip; hazard path crosses panels; warehouse clip; reroute animates; factory clip; robot nodes synchronize; port/hospital still or clip; local maps merge; world-model pulse travels across grid; COORDINATION unlocks |
| S08 · 50s | Human systems-integration workplace | **LIBRARY:** `clip-young-old-worker-desk.mp4`; `clip-team-around-monitor-engaged.mp4` is unavailable if locked in S04, so select alternate team clip; `manager-tablet-inventory.mp4` is unavailable if locked in S01, so select alternate field-worker clip | Worker clip; infrastructure rung grows; systems rung; team clip; service rung; three work labels branch; field-worker clip; operator moves upward; privacy/compliance rung; new/changed/automated columns pulse individually; opportunity verdict lands |
| S09 · 50s | Ordinary room with subtle radio mesh | **LIBRARY:** `hallucinations-v6__br-07a_iv-drip.mp4`; `superhuman-ban__br-08a_voting-booths.mp4`; **NEW:** unoccupied sensing-room motion | Same RF path draws; IV clip; fall-alert panel; room clip; occupancy log duplicates the signal; voting-booth privacy clip; SAFETY/SURVEILLANCE split; ACCESS/EXCLUSION split; PUBLIC/PRIVATE split; 5s apparent breath retains slow camera push and moving mesh; ownership question lands |
| S10 · 50s | Dawn infrastructure-to-home landscape | **LIBRARY:** `hallucinations-v6__br-10b_dawn-hospital.mp4`; `fear-economy__br-09a_dawn-break.mp4`; `out-window-city-night-view.mp4` | Impact Map expands; city-night clip; FIRST tier draws; dawn-hospital clip; NEXT tier draws; industrial icons resolve one per 2s; dawn-city clip; LATER tier draws; dependencies appear; speed slides under timeline; consent controls populate; evidence-state test lands; clean verdict hold retains 1.04 camera push |
| S11 · 10s | Abstract KeyAdvances navy/cyan/amber particle bed | Three **single-use abstract micro-clips** selected from unused network/data candidates | 0–3.3 evidence badges collapse; 3.3–6.6 first micro-bed handoff + channel mark; 6.6–10 second handoff + end-screen zones. Third micro-clip can enter as masked side light so the graphics-only CTA remains clean |

## Current Gap List

Generate or capture only after the final database query and visual-board approval:

1. Photonic light-path macro for S02.
2. Optical-bench pullback showing external 6G test apparatus for S05.
3. Directional horn-antenna short-link shot for S05.
4. Diverse person inside a radio-derived spatial mesh for S06 and thumbnail development.
5. Ordinary sensing-room motion without a visible camera for S09.
6. Port or hospital machine-coordination shot if the library search does not return a credible literal clip.
7. Enough alternate vehicle/team/field-worker footage to preserve the single-use rule.

Every I2V entry must later include its own bounded **Motion:** instruction, the global camera style, and I2V negatives. A still prompt without subject motion is incomplete.

## Render and Master Gates

Run on every rendered scene, fix, then repeat on the assembled master:

```bash
ffmpeg -hide_banner -nostats -i RENDER.mp4 \
  -vf freezedetect=n=-50dB:d=5 -an -f null - 2>&1 | grep freeze_duration
```

Expected output: **nothing**.

Also required:

- `scene-validator.py <project>/hyperframes-v3 --frames`: zero errors.
- `hyperframes layout <scene-dir> --at-transitions --json`: `errorCount` zero.
- `deadspace-scan.py`: target 45–60 visual change events per minute; under ~30/min requires more within-beat motion.
- Re-run `freezedetect` after master assembly because re-encoding can expose scene holds that passed individually.
- Verify that every visual event aligns with the corresponding VO phrase and exits before the next topic begins.

## Recent-Master Check

The 8:48 `MASTER-ai-layoffs.mp4` was sampled across 40 frames and scanned with `freezedetect`. It demonstrates the useful mixture to retain—human footage, full-bleed B-roll, cream source cards, animated data, diagrams, comparison splits, and restrained landings—and produced no reported ≥5-second freeze interval at the standard threshold. Its avatar scenes are legacy and are not carried into KeyAdvances; the current skill permanently requires faceless production.
