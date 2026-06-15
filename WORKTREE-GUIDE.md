# Git Worktree Multi-Claude Setup

## Quick Reference

### Create a new worktree for parallel work
```bash
wt <branch-name>
```

**What it does:**
1. ✅ Creates a git worktree + new branch
2. ✅ Copies necessary files (.env, .claude, .cursor, etc.)
3. ✅ Opens new Cursor window in the worktree
4. ✅ Ready for parallel `claude` instance

### Example Workflow

```bash
# In your main JARVIS folder
cd ~/Library/CloudStorage/Dropbox/jarvis

# Create worktree for adding drums feature
wt add-drums

# This creates:
# - Branch: add-drums
# - Folder: ~/worktrees/jarvis/add-drums (OUTSIDE Dropbox for performance)
# - New Cursor window opens automatically

# In the new Cursor window terminal:
claude

# Now you can work in parallel!
```

### Running Multiple Claude Instances

```bash
# Terminal 1 (main branch)
cd ~/Library/CloudStorage/Dropbox/jarvis
claude

# Terminal 2 (drums feature)
wt add-drums
# New Cursor window opens, then run:
claude

# Terminal 3 (bass feature)
wt add-bass
# New Cursor window opens, then run:
claude

# Terminal 4 (keyboard feature)
wt add-keyboard
# New Cursor window opens, then run:
claude
```

## Useful Commands

### List all worktrees
```bash
wtlist
# or
git worktree list
```

### Remove a worktree when done
```bash
wtremove add-drums
```

### Merge worktree back to main
```bash
# From main branch
git checkout main
git merge add-drums

# Then remove the worktree
wtremove add-drums
```

## File Structure

```
~/Library/CloudStorage/Dropbox/jarvis/  # Your main project (main branch)
├── .claude/
├── .env
└── ...

~/worktrees/jarvis/                      # Worktrees folder (OUTSIDE Dropbox)
├── add-drums/                           # Separate copy (add-drums branch)
│   ├── .claude/                         # Copied from main
│   ├── .env                             # Copied from main
│   └── ...
├── add-bass/                            # Separate copy (add-bass branch)
└── add-keyboard/                        # Separate copy (add-keyboard branch)
```

**Why outside Dropbox?**
- ✅ No sync overhead (faster performance)
- ✅ No wasted Dropbox storage quota
- ✅ Worktrees are temporary (don't need cloud backup)
- ✅ Avoids potential sync conflicts during editing

## Benefits

- ✅ **No merge conflicts** - Each Claude works in different files
- ✅ **Parallel work** - Multiple features at once
- ✅ **Safe isolation** - Main branch stays clean
- ✅ **Easy review** - Test each feature separately before merging
- ✅ **Fast switching** - Use macOS spaces/desktops for each window

## Tips

1. **Use macOS spaces** - Put each Cursor window in its own desktop (Mission Control)
2. **Test before merge** - Run/test the feature in the worktree first
3. **Commit in worktree** - Make commits in each worktree before merging
4. **Watch for conflicts** - If two features edit the same file, resolve during merge

## Common Issues

### "Branch already exists"
```bash
# Delete the old branch first
git branch -D add-drums
wtremove add-drums
wt add-drums
```

### "Cursor command not found"
Update the script to use `code` (VS Code) instead of `cursor`

### Files not copied
Check if the file exists in main project and add it to the `wt` function in `~/.zshrc`
