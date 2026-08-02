---
name: obsidian-manager
description: Manage Obsidian vault organization across 7 domains
metadata:
  jarvis:
    requires:
      bins:
        []
      env:
        []
      config: []
      mcp_servers:
        []
    primaryEnv: ""
    domain: productivity
    security_level: medium
    requires_approval: false
    allowed_operations:
      - read
      - write
    version: 2.0.0
    author: JARVIS
    tags:
      - productivity
      - obsidian
      - knowledge-management
      - notes
    integrates_with:
      []
    feeds_into:
      []
    consumes_from:
      []
---
# Obsidian Manager Skill

**Purpose:** Manage JARVIS's Obsidian vault - organize content, search across domains, create daily notes, and maintain vault structure

**When to Use:** For vault organization, searching previous work, creating notes, or managing domain folders

## ⚠️ Vault locations — read this before running any command below

**LIVE vault (use this): `~/Obsidian/JARVIS/`** — 2,065 notes, written daily by the aggregator
jobs. Five date-partitioned folders:

| Folder | Notes | Written by |
|---|---|---|
| `News/YYYY-MM-DD/` | ~1,625 | `skills/news-aggregator/aggregate.py` (daily 07:00) |
| `YouTube/YYYY-MM-DD/` | ~194 | `skills/youtube-*/fetch_transcripts.py` (daily 07:20) |
| `Papers/YYYY-MM-DD/` | ~150 | `skills/arxiv-research-aggregator/aggregate-arxiv.py` |
| `Reports/` | ~95 | digest + report jobs |
| `arXiv-FullText/` | ~1 | `arxiv-fulltext.py` |

**ARCHIVED vault (do NOT use): `/Volumes/ORICO/jarvis/obsidian-vault/`** — last written
**2026-01-26**. This is the original 7-domain scheme (`content-creation`, `daily-notes`,
`documentation`, `investments`, `presentations`, `productivity`, `research`, `templates`,
`video-production`). It is a different vault with a different structure, not an older copy of
the live one.

**Corrected 2026-08-02.** This skill previously named only the ORICO path, so every command
below searched a vault that had been dead for six months. The sections that follow still
describe the 7-domain scheme — they apply to the **archived** vault. Nothing writes that
structure any more; treat those sections as historical until the domain model is rebuilt
against the live vault.

---

## Core Capabilities

### 1. Daily Note Management

**Create Today's Note:**
- Use template from `templates/daily-note.md`
- Save to `daily-notes/YYYY-MM-DD.md`
- Include date, idea sections, task checklist

**Find Recent Notes:**
- Search `daily-notes/` for recent entries
- Extract ideas tagged for JARVIS to process
- Identify action items across domains

### 2. Domain Organization

**Domain Structure:**
```
investments/        - Portfolio reports, analysis, decisions
content-creation/   - YouTube, LinkedIn, X, thumbnails
research/          - Daily digests, insights, papers
presentations/     - Slides, templates
documentation/     - SOPs, diagrams, guides
video-production/  - Video projects, B-roll
productivity/      - Calendar, tasks, email
```

**Organization Tasks:**
- File content in correct domain folders
- Create domain-specific notes
- Link related content across domains
- Tag appropriately for discoverability

### 3. Search & Retrieval

**Search Across Vault:**
- Use grep/ripgrep for content search
- Search by tags: `#youtube-script`, `#portfolio-report`, etc.
- Find references to specific topics
- Identify connections between domains

**Common Searches:**
```bash
# Find all portfolio reports
grep -r "#portfolio-report" /Volumes/ORICO/jarvis/obsidian-vault/

# Find investment decisions
grep -r "BUY\|SELL" /Volumes/ORICO/jarvis/obsidian-vault/investments/

# Find content ideas
grep -r "#content-idea" /Volumes/ORICO/jarvis/obsidian-vault/
```

### 4. Content Creation

**Create from Templates:**
- Daily note → `templates/daily-note.md`
- YouTube script → `templates/youtube-script.md`
- Portfolio report → `templates/portfolio-report.md`

**Save to Correct Location:**
- Investment reports → `investments/reports/`
- YouTube scripts → `content-creation/youtube/`
- Research digests → `research/daily-digests/`

### 5. Cross-Domain Intelligence

**Link Related Content:**
- Investment insights → Content ideas
- Research findings → Investment decisions
- Performance data → Social media posts

**Example:**
```markdown
Portfolio gained 5% this month
→ LinkedIn post: "How Asset Revesting outperformed..."
→ YouTube video: "My ETF strategy results..."
→ Research note: "Why this approach worked..."
```

---

## Usage Examples

### Example 1: Create Today's Daily Note

**User Request:** "Create today's daily note"

**Actions:**
1. Get today's date (YYYY-MM-DD format)
2. Read template from `templates/daily-note.md`
3. Replace {{date}} placeholders
4. Save to `daily-notes/2026-01-26.md`
5. Confirm creation

### Example 2: Find Recent Investment Decisions

**User Request:** "What investments did I make this month?"

**Actions:**
1. Search `investments/decisions/` for files from current month
2. Search `investments/reports/` for allocation reports
3. Extract BUY/SELL decisions with dates
4. Summarize: positions entered, amounts, rationale

### Example 3: Organize Content Ideas

**User Request:** "Process my daily notes for content ideas"

**Actions:**
1. Read recent daily notes (last 7 days)
2. Extract items under "Content Ideas" section
3. Categorize by platform (YouTube, LinkedIn, X)
4. Create draft files in `content-creation/` folders
5. Link back to source daily note

### Example 4: Cross-Domain Insights

**User Request:** "What can I share on social media about my portfolio?"

**Actions:**
1. Read recent portfolio reports from `investments/reports/`
2. Identify interesting insights (performance, strategy, lessons)
3. Draft LinkedIn post in `content-creation/linkedin/`
4. Draft X thread in `content-creation/x-posts/`
5. Link to source portfolio report

---

## File Naming Conventions

**Daily Notes:** `YYYY-MM-DD.md`
**Portfolio Reports:** `portfolio-[type]-YYYY-MM-DD.md`
- Types: screening, allocation, review, performance

**Content:**
- YouTube: `youtube-[title-slug]-YYYY-MM-DD.md`
- LinkedIn: `linkedin-[topic]-YYYY-MM-DD.md`
- X Posts: `x-[topic]-YYYY-MM-DD.md`

**Research:**
- Daily digest: `digest-YYYY-MM-DD.md`
- Insights: `insight-[topic]-YYYY-MM-DD.md`

---

## Tags System

**Domain Tags:**
- `#investments` - Investment-related content
- `#youtube-script` - YouTube video scripts
- `#linkedin-post` - LinkedIn drafts
- `#x-post` - X/Twitter posts
- `#research` - Research findings
- `#daily-note` - Daily capture notes

**Status Tags:**
- `#draft` - Work in progress
- `#review` - Ready for human review
- `#published` - Finalized/published
- `#archived` - Historical reference

**Action Tags:**
- `#action-required` - Needs user action
- `#monitoring` - Under observation
- `#completed` - Done

---

## Integration with Other Skills

**Inputs from:**
- `etf-screener` → Portfolio reports to `investments/reports/`
- `portfolio-builder` → Allocation plans to `investments/reports/`
- Content engine (future) → Research digests to `research/daily-digests/`
- YouTube skill (future) → Scripts to `content-creation/youtube/`

**Outputs to:**
- Daily notes → Ideas for other skills to process
- Organized vault → Easy search and retrieval
- Cross-domain links → Connections for insights

---

## Best Practices

**DO:**
- Always save to correct domain folder
- Use templates for consistency
- Tag appropriately for discoverability
- Link related content across domains
- Date-stamp all content
- Include source references

**DON'T:**
- Don't create content outside vault structure
- Don't skip template usage
- Don't forget to tag
- Don't duplicate content across folders
- Don't leave files unorganized

---

## Vault Maintenance

**Weekly:**
- Review unorganized files
- Clean up empty folders
- Update README with new domains
- Check for broken links

**Monthly:**
- Archive old daily notes (>90 days)
- Review tag usage
- Update templates if needed
- Prune obsolete content

---

## Troubleshooting

**Issue:** Can't find recent content
- Check file naming follows conventions
- Verify saved to correct domain folder
- Search by tags if filename unknown

**Issue:** Template not found
- Templates in `/Volumes/ORICO/jarvis/obsidian-vault/templates/`
- Create from examples if missing
- Check template filename matches skill expectations

**Issue:** Vault structure broken
- Recreate folders: see README for structure
- Never delete domain folders manually
- Use this skill to reorganize if needed

---

*This skill maintains JARVIS's central knowledge base and ensures all AI work is properly organized, searchable, and accessible.*
