#!/usr/bin/env python3
"""format-index.py — the FORMAT axis. The demand layer has never had one.

TOOL CONTRACT
  SUBSYSTEM  D (Demand), upstream of P1a Market Selection
  STATE      reads/writes ratchet/formats.json  ·  reads nothing else
  GATE       none. This is a CATALOGUE, not a gate. It emits candidates for bend-map.py.
  MODULE     jarvis-video-production (tools tree), consumed by the studio umbrella.
  SCOPE      market-agnostic, subject-agnostic

WHY THIS EXISTS
  scout-niches.py answers "which MARKET should the studio serve". outlier-ratchet.py answers
  "what is beating its own distribution". Neither can answer "what SHAPE do we build", because
  neither models format at all. A niche is not a topic -- it is a (FORMAT x MARKET) pair:

      MARKET   macro · ~120 of them · near-permanent · WHO watches
      FORMAT   micro · unbounded · new ones daily   · HOW the story is told

  The opportunity is the EMPTY CELL in that grid, and the selection rule (measured by
  practitioners, mechanized here) is: pursue a format where the FREE cells outnumber the
  TAKEN ones. This file owns the row axis. bend-map.py walks the columns.

  Full derivation: jarvis-private/reports/FACELESS-NICHE-SYSTEM-2026-08-10.md

MEASURED LEVERAGE ORDER — why the format axis is worth building at all
  From our own prior investigation, jarvis-private/reports/YoutubeResearchTopics/
  YOUTUBE-DEMAND-RESEARCH-2026-08-09.md §3. These are OUR measurements, not the corpus's:

      subject choice              up to 43x   same channel, same template, six weeks apart
      REFILLABLE TITLE TEMPLATE      ~19x     ExtraMint era-titles median 631,043 vs its own
                                              non-era videos at 33,617
      runtime 15-30 min              ~2.5x    on revenue/video, replicated in two strata
      packaging (thumb/title)      NOTHING    above a floor; the relationship inverts at the top

  The ~19x row IS this file's subject, independently measured before the corpus was ever read.
  It also sharpens the definition: the asset is not the template, it is the FILLED SLOTS.
  "A template used once is just a title" -- ExtraMint's asset is fourteen of them. So a format's
  value has two separate components and they are not interchangeable:

      n_channels    >= 3 distinct channels share the frame  -> the shape is PORTABLE
                    (what --discover measures; the corpus's "format has 3 winners" rule)
      refill_slots  how many times ONE channel can refill it -> the shape is an ASSET
                    (what bend-map.py must measure; the corpus's "30+ ideas" rule)

  A portable shape with four refills is a dead end for a channel builder. Both are required.

  §7c, three independent confirmations: a CONCRETE ANCHOR beats an abstraction. Object-anchored
  ExtraMint titles carry the numbers while abstract ones underperform; "dead internet theory"
  probes 108.94x where "why does everything online look fake now" returns n=0. Hence the
  `anchor` field. Prefer concrete rows; treat an abstract row as needing an anchor supplied.

WHAT THIS TOOL DOES NOT DO -- READ BEFORE TRUSTING THE OUTPUT
  It does NOT verify that a format works. `tier`, `cost_usd` and `runtime_min` on seeded rows
  are PRACTITIONER CLAIMS lifted from the source corpus, not our measurements. Rows carry
  `provenance`; anything marked `corpus:<videoId>` is an assertion by an operator who sells a
  course, and the governing report's reliability audit says to re-measure rather than import.
  `corpus_occupied` is likewise a CLAIM about which cells are taken. bend-map.py measures the
  grid for real and writes `markets_occupied`. Never read one for the other.

  It also does NOT rank formats. Ranking needs market size x RPM (scout-niches.py) and trend
  stage (trend-stage.py). A format alone is not an opportunity.

⛔ --discover DOES NOT WORK AS A DISCOVERY METHOD. MEASURED AND FAILED 2026-08-10.
  Read this before spending another credit on it. Across 2,288 pooled videos from 1,903
  channels (~25 outlier calls), n-gram mining produced 8 frames at the 4-token floor, of which
  SIX were ordinary English and TWO were tested end-to-end and failed:
      "this will be worse than a"  -> 0 matches in a 168-video enumeration. Not enumerable.
      "must do this before"        -> 4 matches, best cell "Dr Joe Dispenza: You MUST Do This
                                      Before 10am!", a 120-minute podcast. Generic English.
  Zero usable formats. The earlier 3-token run was worse: every promoted frame enumerated to
  meme Shorts ("Nothing worse than a bad day gym day", "Best 6 year old Soccer player").

  THE DESIGN ERROR, so nobody rebuilds this: a format's signature is ONE CHANNEL'S OWN
  repeated template. Across unrelated channels, the only thing that recurs is English. The
  ">=3 distinct channels" rule is Danilov's test for whether a format you ALREADY KNOW is
  PORTABLE -- a validation rule. It was built here as a DISCOVERY rule, and it cannot be one,
  because generic phrases clear a 3-channel bar trivially while real formats do not appear in
  a cross-channel outlier scatter at all.

  WHAT WORKS INSTEAD, already evidenced in our own research: tear down ONE high-performing
  channel's catalogue and read its repeated template off its own uploads. That is how
  YOUTUBE-DEMAND-RESEARCH-2026-08-09.md found ExtraMint's ~14 refillable slots and measured the
  ~19x template lever. Discovery is a TEARDOWN problem, not a mining problem.
  So the working pipeline is:
      outlier channel  -> teardown.py    -> the channel's own repeated template + refill count
      that template    -> format-index   -> catalogue row (>=3 channels = portable?)
      that row         -> bend-map.py    -> which markets are free

  --discover and --frames are kept because the pooled corpus is reusable and the miner may
  still surface a lead worth eyeballing. Treat anything it emits as a hint, never a format,
  and never promote from it without watching the videos.

THE DISCOVERY RULE
  --discover pulls outlier video titles, reduces each to a FRAME (structural tokens kept,
  content spans replaced by {X}), and proposes a format wherever >=MIN_FRAME_CHANNELS
  DISTINCT channels share a frame. Distinct channels is the whole point: one channel repeating
  its own title formula is a template, not a format. Three unrelated channels converging on one
  frame is a format, and if its earliest seed channel is young it is a NEW format -- which is
  the "insider knowledge" barrier, automated.

  ONE CALL IS NOT A SAMPLE -- THIS IS THE CENTRAL CONSTRAINT. Measured 2026-08-10: a single
  vidiq_outliers call returned 99 videos from 93 DISTINCT CHANNELS. One video per channel is
  the worst possible shape for detecting repetition, and the run found zero frames not because
  the miner was broken but because there was nothing to find. So --discover ACCUMULATES: every
  call appends to raw/formats/corpus.json (deduped on videoId) and mines the whole pool. Same
  inversion as outlier-ratchet.py -- discovery is expensive, the accumulated pool is free, and
  each 5-credit call permanently improves every future run. Expect frames to appear somewhere
  around 400-600 pooled videos, not on run one.

CONFOUNDS
  vidIQ SEMANTIC SEARCH CANNOT TELL "about X" FROM "made with X". Measured 2026-08-10: a query
      for "AI agents, Claude Code, agent engineering" returned mostly AI-GENERATED drama and
      animation channels. This is the same on-entity/off-topic failure outlier-ratchet.py
      documents at line 40. Frames are mined from whatever comes back; garbage in, garbage out.
      Always eyeball --discover output before promoting anything.
  A SHARED FRAME IS NOT ALWAYS A SHARED FORMAT. Two channels may share "what actually happens
      to your" and be doing entirely different things. The frame is a place to LOOK. Promotion
      into the catalogue requires watching the videos and naming the visual signature.
  TITLE FRAMES MISS PURELY VISUAL FORMATS. "low-poly 3D shorts" has no title signature at all.
      Those enter the catalogue by hand, from the seed set or from a teardown.
  THE STRUCTURAL LEXICON IS ENGLISH-ONLY. Non-English titles yield no frames at all, which
      silently excludes the language-arbitrage bend the governing report calls out as an
      opportunity. Known gap, not a bug to be surprised by later.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

TOOLS   = Path(__file__).resolve().parent
RATCHET = TOOLS / "ratchet"
INDEX   = RATCHET / "formats.json"

URL      = "https://mcp.vidiq.com/mcp"
ENV_PATH = os.path.expanduser("~/Library/CloudStorage/Dropbox/jarvis/.env")
_SESSION = {}

# --- discovery thresholds ------------------------------------------------------------
MIN_FRAME_CHANNELS = 3      # distinct channels sharing a frame before it is a candidate.
                            # Matches the practitioner rule "the format has >=3 winners":
                            # validated by repetition, not yet owned by a whole channel.
MIN_FRAME_TOKENS   = 4      # RAISED from 3 on 2026-08-10 after four 3-token frames were
                            # promoted and every one turned out to be ordinary English rather
                            # than a format: "worse than a" enumerated to "Nothing worse than a
                            # bad day gym day #shorts"; "{N} year old" to "Best 6 year old
                            # Soccer player". A 3-token structural n-gram is a phrase everyone
                            # uses, and the >=3-distinct-channel rule cannot filter it because
                            # generic English trivially clears that bar. Distinctiveness comes
                            # from LENGTH: "so you don't have to" (5) and "explained in {N}
                            # minutes" (4) are signatures; "do this before" (3) is not.
MAX_FRAME_TOKENS   = 6      # longer than this and it is one channel's exact title formula
MIN_CONTENT_WORDS  = 2      # non-{N} tokens required; kills numeric artifacts like '{N} {N}'
NEW_FORMAT_DAYS    = 120    # earliest seed channel younger than this => flag as NEW

# --- authority position ---------------------------------------------------------------
# WHICH CLAIM DOES THE FORMAT MAKE ABOUT THE NARRATOR? Added 2026-08-10 after Terry read the
# first real lead ("The Economics of Owning a Gas Station") and declined it: "to be credible
# you have to own the business... things like that have to be experienced to get to the
# nitty-gritty." He is describing an axis nothing in this system modelled.
#
# It is NOT the same as `competence` (does he know the market) or `tier` (can competitors copy
# the production). It asks what STANDING the format's voice implicitly claims, and whether we
# can occupy it without the audience calling it. The corpus has the failure mode on record: an
# operator niche-bent into history, sourced facts from ChatGPT, and was dismantled in his own
# comments. Our own research says the same thing from the other side -- evidence quality pays
# off in RETENTION, which is precisely where a hollow authority claim collapses.
#
#   operator  the voice claims to have DONE it ("owning a gas station"). Needs lived
#             experience; research cannot close the gap and the comments will find it.
#   analyst   the voice claims to have STUDIED it. Credential + rigor are sufficient, and
#             this is Terry's natural position: PhD, 30+ years teaching MBAs and execs.
#   witness   the voice reports what OTHERS did. Needs sourcing, not standing.
#   curator   the voice ranks or compiles. Needs taste and completeness only.
AUTHORITY = {"operator", "analyst", "witness", "curator"}

# --- production tiers ----------------------------------------------------------------
# The longevity model from the corpus, restated as a catalogue field. RED dies in 4-6 months
# because anyone can copy it; GREEN survives for years because something in it cannot be
# copied (humour, voice, real footage, genuine expertise). The tier is a claim about the
# BARRIER TO ENTRY, which is why it is the field bend-map.py sorts on for us: our moat is
# skill + speed, so a RED format is worth nothing to us however empty its grid is.
TIERS = {"red", "yellow", "green"}

# =====================================================================================
# MARKET INDEX
# =====================================================================================
# The column axis. `competence` records TERRY'S standing in each market, which is not a
# nicety -- it is barrier-to-entry #2 (skill), the one an operator cannot fake with AI and
# the reason a dentist beats a 16-year-old on a channel about teeth.
#
# Recorded 2026-08-10 from Terry directly: PhD Business Administration (major MIS, minor
# strategic management), 30+ years teaching in a business college to undergraduates, MBAs
# and executive MBAs; weekly family investment calls, so current rather than academic on
# markets. Health/nutrition/fitness by personal practice. Legal is explicitly declined.
#
# expert  -> genuine depth; can say things competitors cannot fake or copy
# strong  -> real working knowledge, credible without research scaffolding
# general -> no advantage; enter only if the demand case is overwhelming
# avoid   -> declined by Terry; never surface these
MARKETS = {
    # --- money: the highest-RPM territory on the platform, and Terry's home ground -----
    "personal finance":        "expert",
    "investing & stock market": "expert",
    "retirement planning":     "expert",
    "insurance":               "expert",
    "real estate":             "expert",
    "economics":               "expert",
    "accounting":              "expert",
    "taxes":                   "strong",
    "credit & debt":           "strong",
    "banking":                 "strong",
    "crypto":                  "general",
    # --- business ---------------------------------------------------------------------
    "business strategy":       "expert",
    "management & leadership": "expert",
    "entrepreneurship":        "expert",
    "marketing":               "expert",
    "B2B & SaaS":              "expert",
    "information systems":     "expert",
    "supply chain":            "strong",
    "sales":                   "strong",
    "careers & jobs":          "strong",
    "higher education":        "expert",
    "productivity":            "strong",
    # --- health: Terry's by practice rather than credential ---------------------------
    "nutrition":               "strong",
    "fitness & exercise":      "strong",
    "longevity":               "strong",
    "mental health":           "general",
    "sleep":                   "general",
    "medicine":                "general",
    # --- tech --------------------------------------------------------------------------
    "AI & machine learning":   "strong",
    "software engineering":    "strong",
    "consumer tech":           "general",
    "cybersecurity":           "general",
    "space":                   "general",
    # --- knowledge ----------------------------------------------------------------------
    "history":                 "general",
    "military history":        "general",
    "science":                 "general",
    "psychology":              "general",
    "philosophy":              "general",
    "true crime":              "general",
    "geography":               "general",
    "engineering & how-things-work": "general",
    "aviation":                "general",
    "maritime":                "general",
    "disasters":               "general",
    # --- lifestyle ------------------------------------------------------------------------
    "parenting":               "general",
    "relationships":           "general",
    "self-improvement":        "general",
    "travel":                  "general",
    "food & cooking":          "general",
    "fashion & beauty":        "general",
    "home & DIY":              "general",
    "cars & automotive":       "general",
    "pets":                    "general",
    "gardening":               "general",
    # --- entertainment ----------------------------------------------------------------------
    "gaming":                  "general",
    "sports":                  "general",
    "football (soccer)":       "general",
    "basketball":              "general",
    "movies & TV":             "general",
    "music":                   "general",
    "anime":                   "general",
    "celebrity":               "general",
    "comics & superheroes":    "general",
    # --- declined ---------------------------------------------------------------------------
    "legal":                   "avoid",
}

# =====================================================================================
# SEED CATALOGUE
# =====================================================================================
# Bootstrapped 2026-08-10 from the 86-video source corpus (transcripts archived at
# jarvis-private/reports/timdanilov-transcripts/). Every row is a format an operator named
# ON RECORD with at least one concrete channel behind it, which makes this a far better
# starting corpus than anything we could invent -- but see the docstring: tier/cost/runtime
# are their claims, not our measurements.
#
# `corpus_occupied` lists cells the source ASSERTS are taken. It exists so bend-map.py can
# be checked against it, and so we never re-derive what was already stated. It is evidence
# about the source's beliefs, not evidence about the grid.
SEED = [
    {
        "format_id": "every-x-explained-whiteboard",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "Every X explained in N minutes (whiteboard)",
        "visual": "whiteboard / marker 2D over flat colour; multi-way split thumbnail",
        "title_template": "every {X} explained in {N} minutes",
        "title_regex": r"\bevery\b.+\bexplained\b.+\b\d+\s*minutes?\b",
        "runtime_min": [10, 20], "tier": "yellow", "cost_usd": [40, 120],
        "seed_channel": "Paint Explainer",
        "corpus_occupied": ["gaming", "self-improvement", "science", "fitness & exercise",
                            "true crime", "fashion & beauty", "personal finance"],
        "corpus_free": ["home & DIY", "consumer tech"],
        "provenance": "corpus:yvjNmAJIDjM",
        "notes": "The source's own worked bend map. Most-cited format in the corpus; also "
                 "the most likely to be saturated BY that citation -- 59k viewers saw it.",
    },
    {
        "format_id": "explained-with-object",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "Complex topic explained with an absurd object/mascot",
        "visual": "2D character (apes + bananas being the seed instance) over simple sets",
        "title_template": "how {X} works explained with {OBJECT}",
        "title_regex": r"\bexplained (with|by)\b",
        "runtime_min": [6, 15], "tier": "yellow", "cost_usd": [50, 150],
        "seed_channel": "Primate Economics",
        "corpus_occupied": ["economics", "fitness & exercise", "science"],
        "corpus_free": ["true crime", "gaming", "real estate", "self-improvement"],
        "provenance": "corpus:15E2KHXNotQ",
        "notes": "Source claims the grid is mostly empty here -- the stated free_ratio "
                 "trigger. Verify with bend-map before believing it.",
    },
    {
        "format_id": "anatomical-3d-breakdown",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "3D anatomical / physical breakdown of what happens to a body or object",
        "visual": "3D animation, cutaway anatomy, slow push-ins",
        "title_template": "what happens to your {X} when {Y}",
        "title_regex": r"what happens (to|when|if)\b",
        "runtime_min": [1, 10], "tier": "green", "cost_usd": [120, 400],
        "seed_channel": "Art of War / Zack D Films lineage",
        "corpus_occupied": ["military history", "fitness & exercise", "medicine"],
        "corpus_free": ["aviation", "maritime", "disasters"],
        "provenance": "corpus:yvjNmAJIDjM",
        "notes": "Top-tier: money AND skill barrier. Corpus's single most-cited earner.",
    },
    {
        "format_id": "low-poly-3d-shorts",
        "authority": "curator",
        "anchor": "concrete", "refill_slots": None,
        "name": "Low-poly 3D explainer shorts",
        "visual": "low-poly 3D, flat lighting, 30-60s vertical",
        "title_template": None, "title_regex": None,
        "runtime_min": [0.5, 1.5], "tier": "green", "cost_usd": [80, 300],
        "seed_channel": "Low Poly / Loaded Dice",
        "corpus_occupied": ["gaming"],
        "corpus_free": ["personal finance", "sports", "science"],
        "provenance": "corpus:15E2KHXNotQ",
        "notes": "PURELY VISUAL -- no title signature, so --discover can never find it. "
                 "Shorts economics; see the corpus's ~30-day shorts decay claim.",
    },
    {
        "format_id": "ai-influencer-sticker",
        "authority": "analyst",
        "anchor": "abstract", "refill_slots": None,
        "name": "AI presenter, sticker/cutout 2D, explaining a complex money topic",
        "visual": "AI-generated presenter cutout over bold flat 2D with kinetic text",
        "title_template": "why {X} is {ADJECTIVE}",
        "title_regex": None,
        "runtime_min": [1, 8], "tier": "yellow", "cost_usd": [30, 100],
        "seed_channel": "Nick Invests / Fasted Fred",
        "corpus_occupied": ["personal finance", "fitness & exercise"],
        "corpus_free": ["real estate", "insurance", "careers & jobs"],
        "provenance": "corpus:yvjNmAJIDjM",
        "notes": "Cheap, hence crowded, hence exposed to the inauthentic-content sweep.",
    },
    {
        "format_id": "split-figure-debate",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "Modern figure vs historical thinker, two-way split",
        "visual": "two-way split thumbnail, portrait vs portrait, high contrast",
        "title_template": "{PERSON} is what {THINKER} warned us about",
        "title_regex": r"\bwarned us about\b|\bvs\.?\b.+\b(aurelius|plato|marx|orwell)\b",
        "runtime_min": [8, 20], "tier": "yellow", "cost_usd": [60, 200],
        "seed_channel": "(unnamed, 4.1M-view seed video)",
        "corpus_occupied": ["philosophy", "celebrity"],
        "corpus_free": ["business strategy", "AI & machine learning", "economics"],
        "provenance": "corpus:15E2KHXNotQ",
        "notes": "Cited as a SCRIPT bend (one video), not a channel. Format may not sustain "
                 "a library -- check upload counts on any incumbent before committing.",
    },
    {
        "format_id": "pov-tier-ranking",
        "authority": "curator",
        "anchor": "concrete", "refill_slots": None,
        "name": "Ranking a life/career/wealth ladder, tier by tier",
        "visual": "tier ladder graphic, progressive reveal, POV framing",
        "title_template": "ranking every level of {X}",
        "title_regex": r"\bevery level of\b|\branking every\b",
        "runtime_min": [10, 25], "tier": "yellow", "cost_usd": [40, 150],
        "seed_channel": "Dark Ledger / Master POV / Chill POV Guy",
        "corpus_occupied": ["personal finance", "careers & jobs"],
        "corpus_free": ["real estate", "higher education", "insurance", "sports"],
        "provenance": "vidiq:FltNsyPXNdo",
        "notes": "The vidIQ teardown's clearest clone chain: wealth -> jobs -> emergency "
                 "services, each a separate channel at $2k-$15k/mo. Ladder = progress spine.",
    },
    {
        "format_id": "ai-moral-dilemma",
        "authority": "analyst",
        "anchor": "abstract", "refill_slots": None,
        "name": "Pose a dilemma to AI models and stage their answers",
        "visual": "clean 2D, model avatars, verdict cards",
        "title_template": "we asked AI {DILEMMA}",
        "title_regex": r"\bwe asked (ai|chatgpt|claude)\b|\bwould ai\b",
        "runtime_min": [5, 15], "tier": "yellow", "cost_usd": [30, 120],
        "seed_channel": "Polymatter (as named in corpus)",
        "corpus_occupied": ["AI & machine learning", "sports"],
        "corpus_free": ["parenting", "personal finance", "medicine"],
        "provenance": "corpus:15E2KHXNotQ",
        "notes": "Corpus notes this channel was later REMOVED for inauthentic content -- "
                 "repetitive script structure. Cautionary, not aspirational.",
    },
    {
        "format_id": "cohort-trivia-sweep",
        "authority": "witness",
        "anchor": "concrete", "refill_slots": None,
        "name": "One trivia axis swept across a famous closed cohort",
        "visual": "portrait grid, progressive reveal, archival stills",
        "title_template": "how every {COHORT} {VERB}",
        "title_regex": r"\bhow every\b|\bevery (president|king|ceo|champion)\b",
        "runtime_min": [8, 20], "tier": "yellow", "cost_usd": [40, 150],
        "seed_channel": "Agent Floppy",
        "corpus_occupied": ["history"],
        "corpus_free": ["business strategy", "sports", "economics"],
        "provenance": "corpus:yvjNmAJIDjM",
        "notes": "Closed cohort = bounded, enumerable content supply. Presidents -> monarchs "
                 "was the cited bend. CEOs / Fortune 500 founders is the obvious money cell.",
    },
    {
        "format_id": "secretly-reveals",
        "authority": "analyst",
        "anchor": "abstract", "refill_slots": None,
        "name": "A trait secretly reveals something about you",
        "visual": "three-way split thumbnail, comparison cards",
        "title_template": "what your {TRAIT} secretly reveals about your {QUALITY}",
        "title_regex": r"\bsecretly reveals\b|\bwhat your .+ says about\b",
        "runtime_min": [5, 12], "tier": "red", "cost_usd": [20, 80],
        "seed_channel": "(unnamed, cited from a report)",
        "corpus_occupied": ["sports"],
        "corpus_free": ["personal finance", "careers & jobs", "psychology"],
        "provenance": "corpus:iDyJgUEQq4c",
        "notes": "Named ON AIR to 26k viewers with the finance bend spelled out. Treat that "
                 "specific cell as burned; the frame may still travel elsewhere.",
    },
    {
        "format_id": "missed-the-lesson",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "You watched X but missed the lesson inside it",
        "visual": "film stills + annotation HUD, pull-quote cards",
        "title_template": "you watched {X} but missed the {DOMAIN} lesson",
        "title_regex": r"\bbut missed the\b|\bwhat .+ gets? (right|wrong) about\b",
        "runtime_min": [8, 18], "tier": "yellow", "cost_usd": [50, 180],
        "seed_channel": "(unnamed, cited at 800k views)",
        "corpus_occupied": ["movies & TV", "personal finance"],
        "corpus_free": ["business strategy", "real estate", "management & leadership"],
        "provenance": "corpus:iDyJgUEQq4c",
        "notes": "Borrowed authority via a title everyone recognises. Strong fit for a "
                 "business-strategy operator: films are a free, evergreen case library.",
    },
    {
        "format_id": "exhaustive-analysis-flex",
        "authority": "analyst",
        "anchor": "concrete", "refill_slots": None,
        "name": "I analyzed all N of X so you don't have to",
        "visual": "data-viz first: charts with labelled axes, tables, one lit row",
        "title_template": "I analyzed all {N} {X} so you don't have to",
        "title_regex": r"\bi (analy[sz]ed|studied|read|watched) (all|every)\b",
        "runtime_min": [8, 25], "tier": "green", "cost_usd": [60, 250],
        "seed_channel": "(math/battleship channel cited in corpus)",
        "corpus_occupied": ["science", "gaming"],
        "corpus_free": ["investing & stock market", "real estate", "insurance",
                        "business strategy", "careers & jobs"],
        "provenance": "corpus:bgvQ01qhSRA",
        "notes": "SKILL-BARRIER format: the work is the moat and cannot be faked. Highest "
                 "prima facie fit with a research-led operator and with our own data layer.",
    },
    {
        "format_id": "rapid-news-3d",
        "authority": "witness",
        "anchor": "concrete", "refill_slots": None,
        "name": "3D-animated breakdown of a world event, shipped within ~24h",
        "visual": "full 3D scene reconstruction, map inserts, lower-third HUD",
        "title_template": None,
        "title_regex": None,
        "runtime_min": [8, 19], "tier": "green", "cost_usd": [200, 800],
        "seed_channel": "Aitelly",
        "corpus_occupied": ["military history"],
        "corpus_free": [],
        "provenance": "corpus:bgvQ01qhSRA",
        "notes": "SPEED barrier -- the corpus's top-of-pyramid exemplar. Date-anchored, so "
                 "the library depreciates; violates our evergreen preference. Team of ~8.",
    },
    {
        "format_id": "sleep-length-narration",
        "authority": "curator",
        "anchor": "abstract", "refill_slots": None,
        "name": "Multi-hour soft-spoken narration built for background/sleep",
        "visual": "slow ambient bed, minimal cuts, no kinetic text",
        "title_template": None, "title_regex": None,
        "runtime_min": [90, 180], "tier": "yellow", "cost_usd": [40, 200],
        "seed_channel": "The Sleepless Historian",
        "corpus_occupied": ["history", "gaming"],
        "corpus_free": ["economics", "business strategy", "science"],
        "provenance": "vidiq:FltNsyPXNdo",
        "notes": "Monetization cheat: 4,000 watch-hours needs ~2,000 views at 2h vs ~24,000 "
                 "at 10min. Lean-back / TV surface. Cheapest known path to the MPP bar.",
    },
    {
        "format_id": "ai-avatar-documentary",
        "authority": "witness",
        "anchor": "concrete", "refill_slots": None,
        "name": "AI-avatar presenter fronting a documentary-grade script",
        "visual": "AI avatar, cinematic grade, archival inserts",
        "title_template": None, "title_regex": None,
        "runtime_min": [8, 25], "tier": "green", "cost_usd": [150, 600],
        "seed_channel": "Chloe vs History",
        "corpus_occupied": ["history"],
        "corpus_free": ["economics", "business strategy", "insurance"],
        "provenance": "corpus:hSaa2vby2og",
        "notes": "Corpus: weeks per video, which IS the barrier. 10M views on 6 videos.",
    },
    {
        "format_id": "named-system-verdict",
        "authority": "operator",
        "anchor": "concrete", "refill_slots": None,
        "name": "A named real system, a number, and a verdict",
        "visual": "cream evidence card / dark analysis panel over a moving bed (our own)",
        "title_template": "{SYSTEM}: {NUMBER} {UNIT} — {VERDICT}",
        "title_regex": None,
        "runtime_min": [8, 20], "tier": "green", "cost_usd": [0, 60],
        "seed_channel": "Byrddynasty (first-party) / Tristen O'Brien / Owain Lewis",
        "corpus_occupied": ["AI & machine learning", "software engineering"],
        "corpus_free": ["investing & stock market", "insurance", "real estate", "B2B & SaaS",
                        "business strategy", "nutrition", "fitness & exercise"],
        "provenance": "first-party:BYRDDYNASTY-CHANNEL-AUDIT.md",
        "notes": "THE ONLY ROW WITH FIRST-PARTY EVIDENCE. Our own audit: 3 videos -> 65 of "
                 "109 long-form subs; 11 of top 12 by CTR (4.4-9.5%). Independently, the two "
                 "channels beating the agent-engineering lane on avgViews/subs (1.66x, 1.11x "
                 "vs lane median 0.22x) both run this shape. Note the lane, not the format, "
                 "is what failed there -- see the 2026-08-10 sweep.",
    },
]


# =====================================================================================
# vidIQ transport (same shape as scout-niches.py -- deliberately duplicated, not imported;
# these tools are meant to be runnable one at a time without a package layout)
# =====================================================================================
def api_key():
    k = os.environ.get("VIDIQ_API_KEY")
    if k:
        return k
    try:
        for line in open(ENV_PATH):
            if re.match(r"\s*VIDIQ_API_KEY\s*=", line):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    sys.exit("No VIDIQ_API_KEY (env or jarvis/.env).")


def _rpc(method, params=None, notify=False):
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notify:
        body["id"] = 1
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {api_key()}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if "id" in _SESSION:
        req.add_header("Mcp-Session-Id", _SESSION["id"])
    try:
        r = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode()[:400]}
    sid = r.headers.get("Mcp-Session-Id")
    if sid:
        _SESSION["id"] = sid
    raw = r.read().decode()
    if not raw.strip():
        return {}
    if raw.lstrip().startswith("event:") or "\ndata:" in raw or raw.startswith("data:"):
        for line in raw.splitlines():
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
        return {}
    return json.loads(raw)


def call_tool(name, args):
    if "id" not in _SESSION:
        _rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                            "clientInfo": {"name": "format-index", "version": "1"}})
        _rpc("notifications/initialized", notify=True)
    res = _rpc("tools/call", {"name": name, "arguments": args})
    if "_http_error" in res:
        sys.exit(f"vidIQ HTTP {res['_http_error']}: {res['_body']}")
    content = (res.get("result") or {}).get("content") or []
    for block in content:
        if block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except json.JSONDecodeError:
                return {"_raw": block["text"]}
    return {}


# =====================================================================================
# frame extraction
# =====================================================================================
TOKEN = re.compile(r"[a-z0-9']+")

# THE STRUCTURAL LEXICON — topic-independent by construction.
#
# This replaced a frequency rule (structural := token appears in >=X% of the sample), which
# failed on real data 2026-08-10 and is worth recording because the failure is not obvious.
# On a keyword-filtered sample the TOPIC words are by far the most frequent tokens, so
# "retirement", "money", "investing" and "finance" were classified structural and the spines
# came out as topic fragments -- 'of money in retirement', 'for retirement' -- instead of
# shapes. Across 99 real finance outliers it produced ZERO usable frames. No threshold fixes
# this: the more precisely you target a market, the more the topic looks like structure.
#
# So structure is defined a priori. Function words, interrogatives, quantifiers, comparatives,
# negations and the verbs that carry a title's SHAPE rather than its subject. Everything else
# is content, whatever its frequency.
STRUCTURAL = set("""
a an the this that these those there here
i i'm i've i'd we we're we've you you're you'll you've your yours my mine our ours
he she it its they them their his her who whose whom
is are was were be been being am do does did doing done have has had
can could should would will won't shall may might must
not no never always still even just only also too very really actually literally
and or but if then than so because while when where why what which how whether
in on at to from of for with without within into onto over under after before until
about against between across through during per by as up down out off
every each all any some most least both few many more less fewer other another
first second third last next final one two three four five ten
vs versus beat beats beating killed kills destroyed destroys exposed exposes
explained explains explaining ranked ranking rank compared comparing comparison
tested testing tried trying built building made making analyzed analysed
reviewed reviewing happens happened happening means meaning costs cost works worked
looks looked feels felt gets got getting goes went going takes took
reveals revealed revealing says said told telling teaches taught learns learned
stop stopped stopping start started starting quit quitting avoid avoiding
secretly quietly accidentally suddenly finally already almost barely
better best worse worst bigger biggest smaller smallest cheaper cheapest
new old real fake true false wrong right good bad simple hard easy
nobody everyone someone anyone nothing everything something anything
minute minutes second seconds hour hours day days week weeks month months year years
dollars percent times level levels step steps way ways thing things reason reasons
""".split()) | {"{N}"}


def tokenize(title):
    # Numbers are structural ("every X explained in 14 minutes" and "...in 17 minutes" are the
    # same frame), so they become one placeholder. The sentinel has to survive TOKEN.findall,
    # which only matches [a-z0-9'] -- an out-of-alphabet marker is silently eaten.
    t = re.sub(r"\d+", " zqnumzq ", title.lower())
    return ["{N}" if w == "zqnumzq" else w for w in TOKEN.findall(t)]


def templated(tokens, structural):
    """Full shape: content spans collapsed to {X}. Display only — too brittle to group on."""
    parts = []
    for w in tokens:
        if w in structural:
            parts.append(w)
        elif not parts or parts[-1] != "{X}":
            parts.append("{X}")
    while parts and parts[0] == "{X}":
        parts.pop(0)
    while parts and parts[-1] == "{X}":
        parts.pop()
    return " ".join(parts)


def spines_of(tokens, structural):
    """EVERY structural n-gram in the title, length MIN_FRAME_TOKENS..MAX_FRAME_TOKENS.

    Three iterations to get here, each failing on real data, each worth recording:

      1. Group by full template ("every {X} explained in {N} minutes"). Fragmented — an
         optional prefix makes two identical formats two different strings.
      2. Group by the single LONGEST structural run. Survived a synthetic fixture and found
         ZERO frames across 99 real finance outliers, because real titles interleave content
         and structure, so the longest run lands in a different place in every title.
      3. This: mine ALL structural n-grams and count DISTINCT CHANNELS per n-gram. A shared
         hook is found wherever it sits — "what actually happens to your" is caught whether
         it opens the title or closes it.

    Cost is bounded: n-grams come only from structural runs, which are short.
    """
    out = set()
    run = []
    for w in tokens + [None]:
        if w is not None and w in structural:
            run.append(w)
            continue
        for size in range(MIN_FRAME_TOKENS, MAX_FRAME_TOKENS + 1):
            for i in range(0, len(run) - size + 1):
                out.add(" ".join(run[i:i + size]))
        run = []
    return out


def normalize(v):
    """vidIQ's outlier rows use videoTitle/viewCount/videoDuration, NOT title/views/duration.

    Measured 2026-08-10: extraction silently produced ZERO frames across 99 real videos
    because every v.get("title") was None. A missing key is not an empty title -- so this
    reads several spellings and the caller drops rows that still have nothing.
    """
    return {
        "title": v.get("videoTitle") or v.get("title") or "",
        "channelId": v.get("channelId") or v.get("channelTitle"),
        "channelTitle": v.get("channelTitle") or "?",
        "views": v.get("viewCount") or 0,
        "subs": v.get("subscriberCount") or 0,
        "duration": v.get("videoDuration") or 0,
        "category": v.get("mainCategory") or "?",
        "country": v.get("channelCountry") or "?",
    }


def extract_frames(videos):
    """videos: raw vidIQ outlier rows (or the canonical shape) -> frame rows."""
    videos = [normalize(v) for v in videos]
    videos = [v for v in videos if v["title"].strip()]
    toks = {}
    df = Counter()
    for v in videos:
        t = tokenize(v["title"])
        toks[id(v)] = t
        for w in set(t):
            df[w] += 1
    # Topic-independent: see STRUCTURAL. df is still computed because a frame whose spine
    # words are all rare is noise, but it no longer DEFINES structure.
    structural = {w for w in df if w in STRUCTURAL}

    groups = defaultdict(list)
    for v in videos:
        for f in spines_of(toks[id(v)], structural):
            # A frame needs real words. "{N} {N} {N}" matched 4 channels on the first live
            # pool run purely because finance titles are full of numbers and dates -- it is
            # an artifact of the placeholder, not a shape anyone recognises.
            if sum(1 for w in f.split() if w != "{N}") < MIN_CONTENT_WORDS:
                continue
            groups[f].append(v)

    def med(xs):
        xs = sorted(x for x in xs if x)
        return xs[len(xs) // 2] if xs else 0

    rows = []
    for f, vids in groups.items():
        chans = {v["channelId"] for v in vids}
        if len(chans) < MIN_FRAME_CHANNELS:
            continue
        # per_video (views/subs) is the house metric -- outlier-ratchet.py line 291, and the
        # axis market-gate.py floors at 5.0x. Ranking frames on RAW views would just surface
        # whichever frame the biggest channels happen to use, which is the opposite of the
        # question. Population reference: median 3.2x, p75 10.0x.
        ratios = [v["views"] / v["subs"] for v in vids if v["subs"]]
        rows.append({
            "frame": f,
            "n_videos": len(vids),
            "n_channels": len(chans),
            "median_views": med(v["views"] for v in vids),
            "per_video": round(med(ratios), 2) if ratios else None,
            "median_runtime_min": round(med(v["duration"] for v in vids) / 60, 1),
            "categories": [c for c, _ in Counter(v["category"] for v in vids).most_common(3)],
            "channels": sorted({v["channelTitle"] for v in vids})[:6],
            "template": templated(toks[id(vids[0])], structural),
            "examples": [v["title"] for v in vids[:3]],
        })
    # DEDUPE to maximal phrases. n-gram mining emits every sub-phrase, so "actually happens
    # to your" also yields "actually happens to" and "happens to your" with identical channel
    # sets. Keep the longest; drop any shorter phrase contained in a kept one that explains
    # the same channels. Without this the output is ~10x redundant and unreadable.
    rows.sort(key=lambda r: (-len(r["frame"].split()), -r["n_channels"]))
    kept = []
    for r in rows:
        if any(r["frame"] in k["frame"] and k["n_channels"] >= r["n_channels"] for k in kept):
            continue
        kept.append(r)
    # distinct channels first (that IS the format test), then our per-video ratio.
    return sorted(kept, key=lambda r: (-r["n_channels"], -(r["per_video"] or 0)))


# =====================================================================================
# catalogue I/O
# =====================================================================================
def load():
    if INDEX.exists():
        return json.loads(INDEX.read_text())
    return {"formats": {}, "seeded": None, "discovered": []}


def save(idx):
    RATCHET.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(idx, indent=1, sort_keys=False))


def do_seed(idx, force=False):
    added = kept = 0
    for row in SEED:
        fid = row["format_id"]
        if fid in idx["formats"] and not force:
            kept += 1
            continue
        rec = dict(row)
        rec.setdefault("markets_occupied", {})   # bend-map.py owns this; never seeded
        rec["added"] = dt.date.today().isoformat()
        idx["formats"][fid] = rec
        added += 1
    idx["seeded"] = dt.date.today().isoformat()
    save(idx)
    print(f"seeded {added} format(s), left {kept} existing untouched -> {INDEX}")
    if kept and not force:
        print("  (--force to overwrite existing rows with the seed definitions)")


def competence_of(market):
    return MARKETS.get(market, "general")


def do_list(idx, a):
    rows = list(idx["formats"].values())
    if a.tier:
        rows = [r for r in rows if r.get("tier") == a.tier]
    if a.market:
        rows = [r for r in rows if a.market in (r.get("corpus_free") or [])
                or a.market in (r.get("corpus_occupied") or [])]
    if not rows:
        print("no formats match. Run --seed first?")
        return
    print(f"{'format_id':30} {'tier':6} {'anch':5} {'slots':>5} {'runtime':>9}  free-cell hints")
    print("-" * 108)
    for r in sorted(rows, key=lambda x: (x.get("tier") or "z", x["format_id"])):
        rt = r.get("runtime_min") or [0, 0]
        cu = r.get("cost_usd") or [0, 0]
        free = [m for m in (r.get("corpus_free") or [])
                if competence_of(m) in ("expert", "strong")]
        hint = ", ".join(free[:3]) if free else "·"
        band = "*" if 15 <= rt[1] and rt[0] <= 30 else " "   # 15-30min revenue band, §3a
        slots = r.get("refill_slots")
        print(f"{r['format_id'][:30]:30} {r.get('tier','?'):6} "
              f"{(r.get('anchor') or '?')[:5]:5} {(slots if slots else '—'):>5} "
              f"{rt[0]:>4.0f}-{rt[1]:<4.0f}{band} {hint}")
    print(f"\n{len(rows)} format(s). free-cell hints are CLAIMS from the corpus, filtered to "
          f"markets where Terry is expert/strong.\n"
          f"  slots = refill count, the ~19x lever — UNMEASURED until bend-map.py runs.\n"
          f"  anch  = concrete anchors beat abstractions (3 independent confirmations, §7c).\n"
          f"  *     = runtime reaches the measured 15-30min revenue band ($289/video at 1k-50k subs).\n"
          f"Measure the grid with bend-map.py before acting.")


def do_show(idx, fid):
    r = idx["formats"].get(fid)
    if not r:
        sys.exit(f"unknown format_id '{fid}'. --list to see them.")
    print(f"{r['format_id']}  —  {r['name']}\n")
    for k in ("visual", "title_template", "title_regex", "tier", "runtime_min", "cost_usd",
              "seed_channel", "provenance", "added"):
        if r.get(k) is not None:
            print(f"  {k:16} {r[k]}")
    for label, key in (("occupied (CLAIM)", "corpus_occupied"), ("free (CLAIM)", "corpus_free")):
        cells = r.get(key) or []
        if cells:
            print(f"\n  {label}:")
            for m in cells:
                c = competence_of(m)
                mark = {"expert": "***", "strong": " **", "general": "   ", "avoid": " ✗ "}[c]
                print(f"    {mark} {m:34} {c}")
    if r.get("markets_occupied"):
        print(f"\n  MEASURED grid: {len(r['markets_occupied'])} cell(s) — from bend-map.py")
    else:
        print(f"\n  MEASURED grid: none yet. Run: bend-map.py --format {fid}")
    if r.get("notes"):
        print(f"\n  {r['notes']}")


def do_markets(a):
    order = {"expert": 0, "strong": 1, "general": 2, "avoid": 3}
    rows = sorted(MARKETS.items(), key=lambda kv: (order[kv[1]], kv[0]))
    if a.competence:
        rows = [r for r in rows if r[1] == a.competence]
    cur = None
    for m, c in rows:
        if c != cur:
            cur = c
            print(f"\n--- {c.upper()} ---")
        print(f"  {m}")
    print(f"\n{len(rows)} market(s). Competence is barrier-to-entry #2 (skill) and is the "
          f"axis\nbend-map.py ranks free cells on. 'avoid' markets are never surfaced.")


def frame_to_regex(frame):
    """Turn a mined spine into a title_regex bend-map.py can match on.

    The spine is a contiguous run of structural tokens, so the regex is that run with word
    boundaries, {N} standing for any number, and flexible whitespace. Deliberately literal:
    a cleverer regex would match things the miner never actually saw, and the whole point of
    a promoted frame is that it describes observed titles rather than imagined ones.
    """
    parts = []
    for w in frame.split():
        if w == "{N}":
            parts.append(r"\d[\d,\.]*")
        else:
            parts.append(re.escape(w).replace(r"\'", "'"))
    return r"\b" + r"\s+".join(parts) + r"\b"


def do_promote(idx, a):
    """Promote a mined frame into a catalogue row so bend-map.py can walk it.

    This is the join between the two tools, and it was missing: --discover wrote candidate
    frames to discovered[] and nothing could consume them. Promotion is deliberately a
    SEPARATE, EXPLICIT step -- a frame is a place to look, and turning it into a format is a
    judgement about what the videos actually are. The row lands with provenance
    'discovered:<date>' so it never reads like a measured format.
    """
    frames = [f for run in idx.get("discovered", []) for f in run.get("frames", [])]
    if not frames:
        sys.exit("nothing discovered yet. Run --discover first.")
    hit = next((f for f in frames if f["frame"] == a.promote), None)
    if not hit:
        near = [f["frame"] for f in frames if a.promote.lower() in f["frame"].lower()]
        sys.exit(f"no discovered frame '{a.promote}'."
                 + (f"\nDid you mean:\n  " + "\n  ".join(near[:6]) if near else ""))

    fid = a.as_id or re.sub(r"[^a-z0-9]+", "-", hit["frame"].replace("{N}", "n")).strip("-")
    if fid in idx["formats"] and not a.force:
        sys.exit(f"'{fid}' already in the catalogue. --force to overwrite.")

    idx["formats"][fid] = {
        "format_id": fid,
        "name": hit.get("template") or hit["frame"],
        "anchor": a.anchor, "refill_slots": None,
        "visual": None,                      # unknown until someone watches them
        "title_template": hit.get("template") or hit["frame"],
        "title_regex": frame_to_regex(hit["frame"]),
        "runtime_min": [hit["median_runtime_min"], hit["median_runtime_min"]],
        "tier": None, "cost_usd": None,      # claims we have not earned
        "seed_channel": ", ".join(hit.get("channels", [])[:3]),
        "corpus_occupied": [], "corpus_free": [],
        "markets_occupied": {},
        "provenance": f"discovered:{dt.date.today().isoformat()}",
        "discovered_evidence": {k: hit.get(k) for k in
                                ("n_channels", "n_videos", "per_video", "median_views",
                                 "median_runtime_min", "categories", "examples")},
        "added": dt.date.today().isoformat(),
        "notes": "PROMOTED FROM A MINED FRAME. tier/visual/cost are unset because nobody has "
                 "watched these videos yet. Fill them in from a teardown before treating this "
                 "as a real catalogue row.",
    }
    save(idx)
    print(f"promoted '{hit['frame']}' -> {fid}")
    print(f"  regex     {idx['formats'][fid]['title_regex']}")
    print(f"  evidence  {hit['n_channels']} channels · {hit['n_videos']} videos · "
          f"per-video {hit.get('per_video')}x · {hit['median_runtime_min']}m")
    print(f"  next      bend-map.py --format {fid}")


def do_frames(idx, a):
    """Re-mine the accumulated pool with no API call. Free."""
    pool_path = TOOLS / "raw" / "formats" / "corpus.json"
    if not pool_path.exists():
        sys.exit("no pool yet. Run --discover.")
    vids = list(json.loads(pool_path.read_text()).values())
    frames = extract_frames(vids)
    chans = len({v.get("channelId") for v in vids})
    print(f"{len(vids)} pooled videos · {chans} channels -> {len(frames)} frames\n")
    print(f"{'ch':>3} {'vid':>4} {'per-vid':>8} {'run':>5} {'med views':>10}  frame")
    print("-" * 100)
    for r in frames[: a.top or 25]:
        pv = f"{r['per_video']:.2f}x" if r["per_video"] else "—"
        print(f"{r['n_channels']:>3} {r['n_videos']:>4} {pv:>8} {r['median_runtime_min']:>4.0f}m "
              f"{r['median_views']:>10,}  {r['frame']}")
        print(f"{'':34}e.g. {str(r['examples'][0])[:64]}")
    # persist so --promote can consume whatever --frames just showed
    idx.setdefault("discovered", []).append({
        "run": dt.date.today().isoformat(), "keyword": "(pool re-mine)",
        "n_videos": len(vids), "frames": frames[: a.top or 25]})
    save(idx)


def do_discover(idx, a):
    args = {"limit": min(a.limit, 100), "contentType": "long",
            "publishedWithin": a.within, "sort": "score"}
    if a.keyword:
        args["keyword"] = a.keyword
    if a.max_subs:
        args["maxSubscribers"] = a.max_subs
    if a.min_outlier:
        args["minOutlierScore"] = a.min_outlier

    print(f"vidiq_outliers {json.dumps(args)}  (5 credits)")
    res = call_tool("vidiq_outliers", args)
    vids = res.get("videos") or res.get("results") or res.get("items") or []
    if not vids and isinstance(res, dict):
        for v in res.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "title" in v[0]:
                vids = v
                break
    if not vids:
        print("no videos returned. Raw keys: " + ", ".join(list(res)[:12]))
        return

    # ACCUMULATE. See the docstring: one call is ~1 video per channel, which cannot show
    # repetition. The pool is the instrument; the call is just how it grows.
    corpus_path = TOOLS / "raw" / "formats" / "corpus.json"
    corpus_path.parent.mkdir(parents=True, exist_ok=True)
    pool = json.loads(corpus_path.read_text()) if corpus_path.exists() else {}
    before = len(pool)
    for v in vids:
        vid = v.get("videoId") or v.get("videoTitle")
        if vid:
            pool[vid] = v
    corpus_path.write_text(json.dumps(pool, indent=1))
    print(f"pool {before} + {len(vids)} fetched = {len(pool)} unique videos "
          f"({len(pool) - before} new) -> {corpus_path.name}")
    vids = list(pool.values())

    print(f"{len(vids)} outlier videos -> extracting frames "
          f"({len(STRUCTURAL)}-token structural lexicon, >= {MIN_FRAME_CHANNELS} distinct channels)\n")
    frames = extract_frames(vids)
    if not frames:
        print("no frame reached the distinct-channel floor. Widen --limit or --keyword;\n"
              "a narrow sample makes topic words look structural (see CONFOUNDS).")
        return

    known = {f.get("title_regex") for f in idx["formats"].values() if f.get("title_regex")}
    print(f"{'chans':>5} {'vids':>5} {'per-vid':>8} {'run':>6} {'med views':>10}  frame")
    print("-" * 104)
    for r in frames[: a.top]:
        dup = any(re.search(k, r["frame"]) for k in known if k)
        pv = f"{r['per_video']:.2f}x" if r["per_video"] else "—"
        print(f"{r['n_channels']:>5} {r['n_videos']:>5} {pv:>8} {r['median_runtime_min']:>5.0f}m "
              f"{r['median_views']:>10,}  {r['frame'][:52]}{'  [~known]' if dup else ''}")
        print(f"{'':38}  tmpl: {r['template'][:60]}")
        print(f"{'':38}  e.g.  {str(r['examples'][0])[:60]}")
        print(f"{'':38}  ch:   {', '.join(r['channels'][:3])[:60]}")

    idx["discovered"].append({
        "run": dt.date.today().isoformat(),
        "keyword": a.keyword, "within": a.within, "n_videos": len(vids),
        "frames": frames[: a.top],
    })
    save(idx)
    print(f"\nwrote {len(frames[:a.top])} candidate frame(s) to {INDEX} (discovered[])")
    print("These are PLACES TO LOOK, not formats. Promote one by hand into SEED once you have\n"
          "seen the actual videos and can name its visual signature and tier.")


def main():
    p = argparse.ArgumentParser(description="The FORMAT axis for the demand layer.")
    p.add_argument("--seed", action="store_true", help="write the corpus seed catalogue")
    p.add_argument("--force", action="store_true", help="with --seed, overwrite existing rows")
    p.add_argument("--list", action="store_true", help="list the catalogue")
    p.add_argument("--show", metavar="FORMAT_ID", help="detail one format")
    p.add_argument("--markets", action="store_true", help="the market index + competence")
    p.add_argument("--competence", choices=["expert", "strong", "general", "avoid"],
                   help="with --markets, filter")
    p.add_argument("--tier", choices=sorted(TIERS), help="with --list, filter")
    p.add_argument("--market", help="with --list, only formats touching this market")
    p.add_argument("--discover", action="store_true", help="sweep outliers for new frames")
    p.add_argument("--frames", action="store_true",
                   help="re-mine the accumulated pool, no API call, free")
    p.add_argument("--promote", metavar="FRAME",
                   help="promote a mined frame into a walkable catalogue row")
    p.add_argument("--as-id", help="with --promote, override the generated format_id")
    p.add_argument("--anchor", choices=["concrete", "abstract"], default="concrete",
                   help="with --promote, does the frame name a thing or a feeling")
    p.add_argument("--keyword", help="with --discover, topic filter")
    p.add_argument("--within", default="threeMonths",
                   choices=["thisWeek", "thisMonth", "threeMonths", "sixMonths", "oneYear"])
    p.add_argument("--limit", type=int, default=100, help="videos to sample (max 100)")
    p.add_argument("--max-subs", type=int, help="cap channel size — keeps it reachable")
    p.add_argument("--min-outlier", type=float, help="minimum outlier score")
    p.add_argument("--top", type=int, default=20, help="frames to print")
    a = p.parse_args()

    idx = load()
    if a.seed:
        return do_seed(idx, a.force)
    if a.markets:
        return do_markets(a)
    if a.show:
        return do_show(idx, a.show)
    if a.frames:
        return do_frames(idx, a)
    if a.promote:
        return do_promote(idx, a)
    if a.discover:
        return do_discover(idx, a)
    if a.list or True:
        return do_list(idx, a)


if __name__ == "__main__":
    main()
