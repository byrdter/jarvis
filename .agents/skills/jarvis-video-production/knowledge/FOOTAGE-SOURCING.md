# Footage Sourcing — the merged map

**What this is.** Two independent pieces of research combined: a Kimi K3 deep-research report on
the commercial footage market (`jarvis/YoutubeRealSources/Real Footage Sources for Business & Tech
YouTube.pdf`, 18pp) and our own measured work from 2026-08-12 (three full shot censuses, a
free-sources feasibility test, and two build tests). They cover different halves and disagree in
two places that matter.

- **Kimi is stronger on:** the paid market, licence terms, fair-use doctrine, and several free
  sources we had missed entirely.
- **We are stronger on:** the free tier, measured cut rates, what winners actually put on screen,
  and whether stills can carry a video.

**Tooling:** `tools/archival-search.py` queries most of the free layer and tags every row GREEN /
AMBER / RED. `tools/shot-census.py` measures any reference video's shot structure.

---

## 0. The number that sizes everything

**Kimi's estimate is too fast.** It assumes 3–5s shots → **120–200 distinct shots per 10-minute
video**. Measured on the actual winners:

| video | performance | shots/min | mean shot |
|---|---|---:|---:|
| ColdFusion *How BIG is Samsung?* (2014) | 14.6× channel median | **24.8** | — |
| Explorist *Nvidia* (2024) | **7.48× outlier** | **10.6** | 5.7s |
| ColdFusion *AI Data Centres* (2026) | 2.6× channel median | 7.3 | 8.2s |
| ColdFusion *Dropbox* (2026) | 0.93× | 4.7 | 12.8s |

**A 10-minute video at winner pace needs ~75–106 distinct sources, not 120–200.** Only the 2014
Samsung montage sits in Kimi's assumed range. This roughly halves the sourcing requirement and
every budget that follows from it.

**And the second-order finding Kimi's framework has no room for:** material mix is a **constant**
across a 7.48× outlier and a below-median flop — all three sit at **84–90% real material, 10–16%
channel-originated graphics**. What varies monotonically is **rhythm**. Kimi's "provenance matters
more than production value" is probably right against AI slop; it does not explain the variance
*among* real-footage channels. Sourcing enough material is what buys you the rhythm.

---

## 1. GREEN — free to find AND free to use

| source | scale | terms | notes |
|---|---|---|---|
| **Wikimedia Commons** | **1,550,625 stills across our 24 test beats**; 54,014 files for "Intel" | CC0 / CC-BY / CC-BY-SA per file | **Absent from Kimi's report entirely.** The single largest free tier for chips, logos, buildings, portraits, hardware. Share-alike needs a decision — see §5 |
| **NASA Image & Video Library** | 140,000+ | US gov work, no copyright | 4K, claim-proof. No endorsement implication; identifiable astronauts need care |
| **SEC EDGAR** (full-text) | every US public filing | public record | **Absent from Kimi's report as a *visual* source.** The highest-credibility image a business channel can show — see §6 |
| **House / Senate floor feed** | all proceedings | **public domain outright** | The CEO-testimony goldmine. Zuckerberg, Cook, Pichai, Bezos hearings |
| **White House / federal agencies / Fed** | incl. every FOMC presser | public domain | Fed archive is essential for money beats |
| **Prelinger @ Internet Archive** | ~10,300 films | CC0 per item — **check each** | Industrial/advertising/educational — literally the history of American business on film |
| **Pond5 Public Domain Project** | curated | public domain | free account |
| **US National Archives** | 150,000+ reels | mixed — check catalogue | |
| **Free stock:** Pexels (150k), Pixabay (230k), Mixkit, Coverr, Videvo, Videezy, Mazwai, Dareful, Vidsplay | large | commercial OK, no attribution (Pexels/Pixabay/Mixkit); **per-clip for Videvo/Videezy** | Heavily duplicated across thousands of channels — sort by newest, follow specific contributors |
| **YouTube CC filter** | ~4M CC-BY videos | CC-BY, remixable with attribution | Features → Creative Commons |

> **The free tier is a STILLS library, not a footage library.** Across our 24 beats Commons held
> **1,550,625 stills against 2,208 videos — 702:1.** Kimi's "$0 tier can fill 90% of a 3–5s
> timeline" is true for *generic* footage and false for *specific* subjects. For "Gordon Moore in
> 1970" the free tier has a photograph, not a clip. **See §7 — that turns out not to be fatal.**

---

## 2. AMBER — free to find, copyrighted, fair-use dependent

| source | scale | why it matters |
|---|---|---|
| **Corporate press rooms** | per company | **Missing from our work, and Kimi is right that it's the best-kept secret.** NVIDIA Newsroom publishes downloadable corporate b-roll, fab and data-centre imagery, "Jensen Huang at GTC" assets. *No stock library has the inside of Tesla's factory; Tesla's press site does.* 15 verified URLs in `archival-search.py` |
| **C-SPAN** (own coverage) | all federal events | Free **non-commercial** with attribution (keep the logo). Commercial: **$100 per program per year per URL**. Floor feed itself is PD — a cheap conversion of a fair-use gamble into a line item |
| **Computer History Museum** | 2,051 videos | ~1,087 Steve Jobs hits, ~1,070 Intel, *Morris Chang in conversation with Jensen Huang*. **Reuse terms unconfirmed — the highest-value open question we have** |
| **Local TV affiliates** | vast | **The winning video's actual source.** WMBD, WKRN, FOX 2 St. Louis, NBC10, CBS Atlanta — residents on porches, not executives. Kimi covers national (CNBC/Bloomberg/Fox) and misses this tier |
| **Town-hall / council recordings** (archive.org `openpublica`) | thousands | North Las Vegas, Toledo, Seattle. Where affected-public footage lives |
| **Internet Archive TV News Archive** | continuous US TV | Searchable by **closed-caption text** — how you find the exact broadcast second before licensing it |
| **Company keynotes & IR webcasts** | per company | ~73% of companies archive webcasts post-call. Video for the *visual*, earnings-call *audio* under your own charts — audio excerpts draw far fewer automated claims |
| **University channels** | large | **Stanford GSB "View From The Top"** — sitting CEOs, hour-long, university-owned, light Content-ID enforcement. One interview yields dozens of 3–5s cuts |
| **Video podcasts** (Fridman, All-In, Acquired, 20VC) | huge | Richest raw leader footage; rights least formalised, enforcement is human not automated |
| **Wayback Machine** | the web, historically | Period-correct pages — the browser-chrome register Explorist leans on |
| **Google Patents** | all patents | Free, primary-source, visually distinctive |

---

## 3. RED — licensed and priced

| source | scale | price |
|---|---|---|
| **Reuters Connect** | 55M assets, ~1.2M licensable clips 1896→today | single-asset by card, or subscription |
| **AP Archive** | 2M+ stories to 1895 (incl. British Movietone) | billed in **15-second increments** |
| **British Pathé / Screenocean** | 220,000 newsreel items 1896–1984 | editorial licence |
| **Veritone Commerce** | CBS/60 Minutes, Bloomberg, CNN, NYT, SCMP | per clip, quote-based |
| **Pond5 editorial** | **4.3M clips from $79** | the affordable end of editorial — Reuters, Cover Video, Newsflare |
| **Jukin Media** (UGC) | 65,000+ cleared | **$99 = monetised, one channel** |

> ⚠️ **Two price claims conflict and neither is settled.** Kimi cites documentary news licensing
> "historically up to ~$1,000/minute" (≈$16/s); we found a published AP figure of **~$40/second**.
> Both cannot be current for the same thing. **Get a quote before budgeting.**

> ⚠️ **The AP pre-1964 claim is the most valuable and least verified thing in either document.**
> Kimi reports that AP content published 1963 or earlier was never copyright-renewed and is free to
> use in the US. Non-renewal of pre-1964 US works is real doctrine, but this is a sweeping claim
> about a specific 2M-item corpus. **If true it demolishes our "$19,200 per video, not a model"
> conclusion for the historical half.** Verify per item before building on it.

---

## 4. Traps

- **TED is CC BY-NC-ND** — no editing, no monetisation. Structurally incompatible with a monetised
  cut despite looking like the obvious source. **TEDx allows a 30-second excerpt.**
- **Shutterstock's Standard licence caps web/social distribution at 500,000 viewers** — a viral
  video can outgrow its own licence. Enhanced removes the ceiling.
- **Envato is project-based** — each distinct video should be registered; real record-keeping
  overhead on a daily-upload channel.
- **Artlist/Artgrid Social tier covers your own channels only** — sponsorships need Pro.
- **Committee-branded reposts of PD government footage** sometimes carry bogus "standard YouTube
  licence" labels that have no legal force over public-domain material.
- **Free-stock clips carry no trademark, logo or publicity-rights clearance**, and no free platform
  indemnifies you. Avoid free clips where a brand or a face is the *subject* rather than background.

---

## 5. Rights hygiene

**Licensing footage and being allowed to monetise it are two separate questions.** YouTube's
Partner Program requires commercial rights to the elements *and separately* evaluates originality
and reused content. Properly licensed stock inside original analysis is fine; a channel that is
*nothing but* reassembled clips carries monetisation risk regardless of licences.

- Keep an **asset log**: source, licence type, download date, project, and a **screenshot of the
  licence terms at time of download**. It is the defence in any dispute.
- Run **YouTube Studio's pre-publish copyright check** on every upload — it catches Content ID
  matches while still in draft.
- **Fair use is decided by courts, not by YouTube.** A claim is not a strike; three strikes in 90
  days ends a channel. Attribute on screen, keep excerpts minimal, embed in narration that adds
  analysis. Never rely on "I don't own this" disclaimers, pitch-shifting or mirroring — all
  worthless.
- **Share-alike (CC-BY-SA) on a monetised video is UNRESOLVED** and is a question for counsel.
  `archival-search.py` flags it per row rather than guessing.

*Neither this document nor the underlying report is legal advice.*

---

## 6. The register Kimi's report doesn't contain: documents as visuals

A business channel's most credible image is often not footage at all. Our document-scroll device
takes a **real SEC filing page capture** inside browser chrome, scrolls it in staged pulls with a
page ticker, punches in, and lands a highlight on the company's own sentence:

> *"The transactions are dilutive to existing stockholders."* — Intel Form 10-K, accession
> 0000050863-26-000011

Free, public record, unlimited, and unfakeable. Same applies to patents, court filings and
period web pages via Wayback. Explorist does this constantly with WSJ and Business Insider pages —
**dark-inverted real page captures with one figure highlighted**, never a redesigned card.

---

## 7. Stills work — the constraint is not fatal

The free tier is 702:1 stills to video. That would be fatal if stills could not carry a video.
**Measured, they can.** A 60-second scene built from **8 Wikimedia Commons stills — zero video,
zero AI** — scored **71.0 change-events/min**, beating our shipped masters (67.6–69.6).

What produced it (it failed twice first):
1. **Slow parallax is not motion.** A continuous drift across a 9.6s beat produced *zero* change
   events. Necessary, not sufficient.
2. **Opaque backing panels reduce measured density** — backing text for legibility masks the moving
   bed. Legibility and motion trade against each other; ~.78 alpha resolves it.
3. **The punch-in carries it** — a discrete re-frame inside the still every ~2.2s.

**Cadence rule: a stills-led build needs a discrete landing every 2–3 seconds.** Devices rotate —
punch / lateral pan / pullback / deal / match-cut / document-scroll — and no device repeats in
adjacent beats. Match-cut and document-scroll run leaner (~58/min) and are payoff devices, not
workhorses.

Annotation must **transform with the artifact it names**, or it drifts off target the moment a
device moves the image. And on an annotated beat the print **holds** while the marks land; the bed
carries the motion.

---

## 8. Discovery tools

| tool | what it does |
|---|---|
| **Filmot** | **1.7 billion transcripts across 1.5 billion YouTube videos** — search a quoted phrase, get the exact moment. Free. **The best single find in Kimi's report.** No usable API (every endpoint 302s) — `archival-search.py` links out to it |
| **YouGlish** | same, with in-context playback (~20 free searches/day) |
| **ClipCatalog** | local Whisper transcription of *your own* library → searchable by spoken word, SRT export |
| **YouTube transcript panel** | Ctrl/Cmd+F on any video |
| **`tools/archival-search.py`** | ours — Commons, Internet Archive/Prelinger, EDGAR, NASA, press rooms, CHM, AP Archive, C-SPAN, local news, Wayback, with rights tiers |

> **Title search and spoken-word search are different problems.** Ours matches titles and metadata;
> Filmot matches what was *said*. For "the moment Jensen Huang says X", use Filmot first.

---

## 9. Order of operations

**Generic-real layer (most of the timeline):** free stock + Commons for stills, one subscription
(Storyblocks ~$252–360/yr, Envato ~$198/yr, Motion Array ~$192–300/yr) if volume demands it.
Search **specific environments** — semiconductor fab, data centre, trading floor — never abstract
concepts ("innovation", "AI"), because concept keywords return the clips every other faceless
channel is already using.

**Specific-real layer (the shots that make it credible), cheapest first:**
1. Government / public domain — C-SPAN floor, NASA, White House, Fed, EDGAR filings
2. Corporate press rooms — free, broadcast-quality, made to be used
3. Commons + CHM + Internet Archive
4. Local news, town halls, social video — fair use, attributed, minimal
5. Pond5 editorial from $79 for the handful that must be exact
6. Reuters / AP / Veritone for the one or two moments that must be *the* moment

**Talking layer, in order:** C-SPAN & hearings (freest and most dramatic) → keynotes, earnings
calls, university interviews → broadcast (fair use or Veritone) → podcasts (richest, least
formalised) — with **TED carved out entirely.**

> **Money buys specificity and safety, not volume.** And remember Explorist ran a 7.48× outlier
> with **zero original interviews** — all 85 talking shots came from ~26 third-party sources, at a
> **4.0s median**. Talking footage is punctuation, not segments.
