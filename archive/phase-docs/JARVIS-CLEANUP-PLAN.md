# JARVIS Directory Cleanup Plan

**Created:** 2026-06-15  
**Purpose:** Move video production, strategic planning, and content files from `jarvis` → `jarvis-private`

---

## Current Situation

### **jarvis directory** (Public GitHub repo)
**Should contain:** Core JARVIS functionality only
- agent-sdk, skills, cli-tools, ecosystem, examples, tests
- CLAUDE.md, README.md, core documentation

**Currently ALSO contains (shouldn't be here):**
- 12+ video production directories (video-8 through video-25)
- Video content (agent-stack-series, byrddynasty-blocks, asset-library)
- Strategic planning docs (REVENUE-ROADMAP, STRATEGIC-ADVISORY, etc.)
- Personal planning (SOUTH-AMERICA-35DAY-PLAN)
- Research and reports

**Result:** Cluttered, mixes public JARVIS code with private content

---

### **jarvis-private directory** (Private content)
**Contains:** 
- video-production/ (already moved previously)
- research/, reports/, logs/, docs/
- Various wikis (claude-code-wiki, ai-filmmaking-wiki, etc.)
- context/, claude-mem-data/
- Avatars/, MiscGuides/

**Pattern established:** This is where non-core-JARVIS content lives

---

## Recommendation: Use SAME `jarvis-private` Directory

**Why ONE jarvis-private (not jarvis-private2):**
✅ Simpler (one place for all non-core content)
✅ Pattern already established (you did this before)
✅ Easier to find things (don't have to remember "was that in private or private2?")
✅ Better organization (use subdirectories, not separate top-level folders)

---

## Proposed Directory Structure

### **jarvis/** (Public GitHub Repo - CORE ONLY)
```
jarvis/
├── agent-sdk/              ← STAYS (core)
├── skills/                 ← STAYS (core)
├── cli-tools/              ← STAYS (core)
├── ecosystem/              ← STAYS (core)
├── examples/               ← STAYS (core)
├── tests/                  ← STAYS (core)
├── scripts/                ← STAYS (core, if JARVIS scripts)
├── tools/                  ← STAYS (core)
├── .claude/                ← STAYS
├── .beads/                 ← STAYS
├── .git/                   ← STAYS
├── .env (gitignored)       ← STAYS
├── CLAUDE.md               ← STAYS (core docs)
├── README.md               ← STAYS (core docs)
├── CONTRIBUTING.md         ← STAYS (core docs)
├── LICENSE                 ← STAYS
├── .gitignore              ← STAYS
└── [other core files]      ← STAYS
```

**Total:** ~15-20 items (clean, focused, clear purpose)

---

### **jarvis-private/** (Private Content - EVERYTHING ELSE)
```
jarvis-private/
├── video-production/                      ← ALREADY HERE
│   ├── video-8-phase-8/                   ← MOVE FROM jarvis
│   ├── video-9-phase-9/                   ← MOVE FROM jarvis
│   ├── video-10-phase-10/                 ← MOVE FROM jarvis
│   ├── video-11-production-pipeline/      ← MOVE FROM jarvis
│   ├── video-12-mcp-token-stack/          ← MOVE FROM jarvis
│   ├── video-12-visual-treatment-board/   ← MOVE FROM jarvis
│   ├── video-13-humanoid-robots/          ← MOVE FROM jarvis
│   ├── video-14-three-brains/             ← MOVE FROM jarvis
│   ├── video-25-ai-builder-roadmap/       ← MOVE FROM jarvis
│   ├── video-capabilities-showcase/       ← MOVE FROM jarvis
│   ├── agent-stack-series/                ← MOVE FROM jarvis
│   ├── agent-stack-deep-dive/             ← MOVE FROM jarvis
│   ├── byrddynasty-blocks/                ← MOVE FROM jarvis
│   ├── asset-library/                     ← MOVE FROM jarvis
│   ├── keyadvances-assets/                ← MOVE FROM jarvis
│   ├── keyadvances-newsroom/              ← MOVE FROM jarvis
│   ├── YoutubeAutomation/                 ← MOVE FROM jarvis
│   ├── video-assets/                      ← MOVE FROM jarvis
│   └── public-broll/                      ← MOVE FROM jarvis
│
├── strategic-planning/                    ← NEW (or use docs/)
│   ├── REVENUE-ROADMAP-20K.md             ← MOVE FROM jarvis
│   ├── REVENUE-ROADMAP-SUMMARY.md         ← MOVE FROM jarvis
│   ├── STRATEGIC-ADVISORY-ROADMAP.md      ← MOVE FROM jarvis
│   ├── STRATEGIC-SUMMARY.md               ← MOVE FROM jarvis
│   ├── TRANSITION-IMPLEMENTATION-PLAN.md  ← MOVE FROM jarvis
│   ├── 12-WEEK-HYBRID-CONTENT-PLAN.md     ← MOVE FROM jarvis
│   ├── 25-STRATEGIC-VIDEO-TOPICS.md       ← MOVE FROM jarvis
│   ├── 2035-BOOK-TO-VIDEO-STRATEGY.md     ← MOVE FROM jarvis
│   └── BYRDDYNASTY-JARVIS-INTEGRATION-ROADMAP.md ← MOVE FROM jarvis
│
├── personal/                              ← NEW (or use docs/)
│   ├── SOUTH-AMERICA-35DAY-PLAN.md        ← MOVE FROM jarvis
│   └── SOUTH-AMERICA-35DAY-PLAN.pdf       ← MOVE FROM jarvis
│
├── research/                              ← ALREADY HERE
│   └── (move research, research-digests from jarvis)
│
├── reports/                               ← ALREADY HERE
│
├── docs/                                  ← ALREADY HERE
│   └── (various documentation)
│
├── context/                               ← ALREADY HERE (memory system)
├── claude-mem-data/                       ← ALREADY HERE
├── wikis/                                 ← ALREADY HERE (or keep flat)
│   ├── claude-code-wiki/
│   ├── ai-filmmaking-wiki/
│   ├── second-brain-wiki/
│   └── operations-wiki/
│
└── [other private content]
```

---

## What to Move (Detailed List)

### **Category 1: Video Production** → `jarvis-private/video-production/`

**Directories to move:**
- video-8-phase-8
- video-9-phase-9
- video-10-phase-10
- video-11-production-pipeline
- video-12-mcp-token-stack
- video-12-visual-treatment-board
- video-13-humanoid-robots-jarvis-brain
- video-14-three-brains-one-router
- video-25-2027-ai-builder-roadmap
- video-capabilities-showcase
- agent-stack-series
- agent-stack-deep-dive
- byrddynasty-blocks
- asset-library
- keyadvances-assets
- keyadvances-newsroom
- YoutubeAutomation
- video-assets
- public-broll

**Total:** 19 directories

---

### **Category 2: Strategic Planning** → `jarvis-private/strategic-planning/` (or `docs/`)

**Files to move:**
- REVENUE-ROADMAP-20K.md
- REVENUE-ROADMAP-SUMMARY.md
- STRATEGIC-ADVISORY-ROADMAP.md
- STRATEGIC-SUMMARY.md
- TRANSITION-IMPLEMENTATION-PLAN.md
- 12-WEEK-HYBRID-CONTENT-PLAN.md
- 25-STRATEGIC-VIDEO-TOPICS.md
- 2035-BOOK-TO-VIDEO-STRATEGY.md
- BYRDDYNASTY-JARVIS-INTEGRATION-ROADMAP.md

**Total:** 9 files

---

### **Category 3: Personal Planning** → `jarvis-private/personal/` (or `docs/`)

**Files to move:**
- SOUTH-AMERICA-35DAY-PLAN.md
- SOUTH-AMERICA-35DAY-PLAN.pdf
- HANDOFF.md (possibly)
- DESKTOP-SHORTCUTS-SETUP.md (possibly)
- MULTI-CLAUDE-QUICK-REFERENCE.md (possibly)
- WORKTREE-GUIDE.md (possibly - or keep in jarvis if it's JARVIS-related)

---

### **Category 4: Research** → `jarvis-private/research/`

**Directories to move:**
- research/ (from jarvis)
- research-digests/ (from jarvis)
- repos/ (if not JARVIS core)

---

### **Category 5: Reports** → `jarvis-private/reports/`

**Directories to move:**
- reports/ (from jarvis, if not already in jarvis-private)

---

### **Category 6: Might Move (Unclear Purpose)**

**Need to check:**
- 03-cli/ (is this for Agent Stack video or core JARVIS?)
- scripts/ (JARVIS scripts or video scripts?)
- apps/ (already in jarvis-private, check if anything in jarvis/apps)

---

## What STAYS in jarvis (Core JARVIS Only)

### **Directories:**
- agent-sdk/
- skills/
- cli-tools/
- ecosystem/
- examples/
- tests/
- tools/
- logs/ (if JARVIS execution logs, not video production logs)

### **Config/System:**
- .claude/
- .beads/
- .git/
- .env (gitignored)
- .gitignore
- .venv/
- .agents/
- .codex/
- .playwright-mcp/
- .claude-mem/

### **Core Documentation:**
- CLAUDE.md (project guidelines)
- README.md (setup, tech stack)
- CONTRIBUTING.md
- LICENSE

### **Possibly Keep (JARVIS-Related):**
- PHASE-1-MEMORY-COMPLETE.md
- PHASE-2-MEMORY-COMPLETE.md
- PHASE-3-MEMORY-COMPLETE.md
- SHORT_TERM_PERSISTENT_MEMORY.md
- MEMORY-SOLUTIONS-ANALYSIS.md
- THREE-BRAIN-SETUP-COMPLETE.md
- THREE-BRAIN-QUICK-REFERENCE.md
- AGENT-SDK-LLM-INTEGRATION-COMPLETE.md
- YOUTUBE-SCRAPERS-REFERENCE.md (if JARVIS skill)
- WORKTREE-GUIDE.md (if JARVIS development)

---

## Execution Plan (Commands)

### **Step 1: Move Video Production Directories**

```bash
# Create structure if needed (probably already exists)
mkdir -p ~/Library/CloudStorage/Dropbox/jarvis-private/video-production

# Move all video directories
mv ~/Library/CloudStorage/Dropbox/jarvis/video-8-phase-8 ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-9-phase-9 ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-10-phase-10 ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-11-production-pipeline ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-12-mcp-token-stack ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-12-visual-treatment-board ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-13-humanoid-robots-jarvis-brain ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-14-three-brains-one-router ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-25-2027-ai-builder-roadmap ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-capabilities-showcase ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/agent-stack-series ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/agent-stack-deep-dive ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/byrddynasty-blocks ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/asset-library ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/keyadvances-assets ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/keyadvances-newsroom ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/YoutubeAutomation ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/video-assets ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
mv ~/Library/CloudStorage/Dropbox/jarvis/public-broll ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
```

---

### **Step 2: Move Strategic Planning Docs**

```bash
# Create directory
mkdir -p ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning

# Move strategic docs
mv ~/Library/CloudStorage/Dropbox/jarvis/REVENUE-ROADMAP-20K.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/REVENUE-ROADMAP-SUMMARY.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/STRATEGIC-ADVISORY-ROADMAP.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/STRATEGIC-SUMMARY.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/TRANSITION-IMPLEMENTATION-PLAN.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/12-WEEK-HYBRID-CONTENT-PLAN.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/25-STRATEGIC-VIDEO-TOPICS.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/2035-BOOK-TO-VIDEO-STRATEGY.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
mv ~/Library/CloudStorage/Dropbox/jarvis/BYRDDYNASTY-JARVIS-INTEGRATION-ROADMAP.md ~/Library/CloudStorage/Dropbox/jarvis-private/strategic-planning/
```

---

### **Step 3: Move Personal Planning Docs**

```bash
# Create directory
mkdir -p ~/Library/CloudStorage/Dropbox/jarvis-private/personal

# Move personal docs
mv ~/Library/CloudStorage/Dropbox/jarvis/SOUTH-AMERICA-35DAY-PLAN.md ~/Library/CloudStorage/Dropbox/jarvis-private/personal/
mv ~/Library/CloudStorage/Dropbox/jarvis/SOUTH-AMERICA-35DAY-PLAN.pdf ~/Library/CloudStorage/Dropbox/jarvis-private/personal/
mv ~/Library/CloudStorage/Dropbox/jarvis/HANDOFF.md ~/Library/CloudStorage/Dropbox/jarvis-private/personal/
```

---

### **Step 4: Move Research (if exists)**

```bash
# Move research
mv ~/Library/CloudStorage/Dropbox/jarvis/research ~/Library/CloudStorage/Dropbox/jarvis-private/
mv ~/Library/CloudStorage/Dropbox/jarvis/research-digests ~/Library/CloudStorage/Dropbox/jarvis-private/
```

---

### **Step 5: Check 03-cli and decide**

```bash
# Check what's in 03-cli
ls -la ~/Library/CloudStorage/Dropbox/jarvis/03-cli

# If it's video-related, move it:
mv ~/Library/CloudStorage/Dropbox/jarvis/03-cli ~/Library/CloudStorage/Dropbox/jarvis-private/video-production/
```

---

### **Step 6: Verify Clean jarvis Directory**

```bash
# Check what's left
ls -la ~/Library/CloudStorage/Dropbox/jarvis | grep -v "^d.*\.\.\?$" | grep -v "^d.*\."
```

**Should only see:**
- agent-sdk, skills, cli-tools, ecosystem, examples, tests, tools
- .claude, .beads, .git, etc.
- CLAUDE.md, README.md, etc.
- JARVIS-related docs (PHASE-*, MEMORY-*, etc.)

---

## Benefits of This Cleanup

### **Cleaner Public Repo:**
- ✅ jarvis/ contains only core JARVIS code
- ✅ Clear what's public vs private
- ✅ Easier for others to understand the project
- ✅ Faster git operations (fewer files)

### **Better Organization:**
- ✅ All video content in one place (jarvis-private/video-production/)
- ✅ All strategic planning in one place (jarvis-private/strategic-planning/)
- ✅ Personal stuff separated (jarvis-private/personal/)
- ✅ Easy to find things

### **Simpler Mental Model:**
- jarvis = "The GitHub project"
- jarvis-private = "My work using the project"

---

## After Cleanup: Update .gitignore

Make sure your `jarvis/.gitignore` excludes anything that references jarvis-private:

```gitignore
# Private content lives in jarvis-private, not here
../jarvis-private/
```

(Probably already covered, but worth checking)

---

## Recommendation Summary

**Use SAME `jarvis-private` directory** (not jarvis-private2)

**Organize by purpose:**
- jarvis-private/video-production/ (all video work)
- jarvis-private/strategic-planning/ (business planning docs)
- jarvis-private/personal/ (personal stuff)
- jarvis-private/research/ (already there)
- jarvis-private/reports/ (already there)
- jarvis-private/docs/ (already there)
- jarvis-private/wikis/ (already there)

**Result:**
- jarvis/ is clean (20-30 items max, all core JARVIS)
- jarvis-private/ is organized (clear subdirectories by purpose)
- One place for everything (simple, not jarvis-private1, private2, etc.)

---

**Ready to execute the cleanup? I can run the commands above, or you can review first.**
