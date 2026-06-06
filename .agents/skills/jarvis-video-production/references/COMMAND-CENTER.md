# Episode Command Center

The command center is the live workspace for an episode. It can start as Markdown files and later become a local Site.

## Required Surfaces

- episode brief
- research brief
- claim/source map
- script status
- visual treatment board
- asset inventory
- scene production status
- render list and locked takes
- QC findings
- approval notes
- blockers
- beads issue links
- final packaging checklist

## Suggested Files

```text
video-XX-name/
  EPISODE.md
  RESEARCH-BRIEF.md
  CLAIM-SOURCE-MAP.md
  VISUAL-TREATMENT-BOARD.md
  ASSET-INVENTORY.md
  SCENE-STATUS.md
  QC-REPORT.md
  YOUTUBE-PACKAGE.md
```

## Scaffold

For a new episode, initialize the command center with:

```bash
.agents/skills/jarvis-video-production/scripts/scaffold-command-center.sh video-XX-name
```

The script copies templates from `templates/episode-command-center/`, creates `scenes/`, and skips existing files rather than overwriting them.

## Site Direction

When building this as a Site, prioritize a dense production workspace:

- scene table with status and approvals
- visual-board cards or rows
- asset thumbnails and semantic keys
- render preview links
- blockers and beads issues
- annotation-style review notes

The Site should be a working surface, not a marketing page.
