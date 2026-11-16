# Multi-Claude Parallel Workflow - Quick Reference

## Setup (One Time)

✅ **4 Desktops created** (via Mission Control: `Control + ↑`)  
✅ **wt command installed** (in `~/.zshrc`)  
✅ **Hammerspoon installed** (for window management - optional)

---

## Daily Workflow

### 1. Create New Worktree

```bash
# In main JARVIS directory (Desktop 1)
cd ~/Library/CloudStorage/Dropbox/jarvis

# Create worktree for a new feature
wt <feature-name>

# Examples:
wt add-drums
wt fix-bug-123
wt refactor-auth
```

**What happens:**
- ✅ Creates git branch: `<feature-name>`
- ✅ Creates worktree at: `~/worktrees/jarvis/<feature-name>`
- ✅ Copies .env, .claude files
- ✅ Opens new VS Code window

### 2. Move Window to Desktop

**Method: Drag in Mission Control**
1. Press `Control + ↑` (open Mission Control)
2. Drag the new VS Code window to Desktop 2/3/4
3. Click that desktop to switch to it

### 3. Start Claude in Each Worktree

**In each VS Code window:**
1. Open terminal: `` Control + ` ``
2. Verify you're in the worktree:
   ```bash
   pwd  # Should show: /Users/terrybyrd/worktrees/jarvis/<feature-name>
   git branch  # Should show: * <feature-name>
   ```
3. Start Claude:
   ```bash
   claude
   ```

### 4. Work in Parallel

**Switch between desktops:**
- `Control + 1` → Main JARVIS (Desktop 1)
- `Control + 2` → Feature 1 (Desktop 2)
- `Control + 3` → Feature 2 (Desktop 3)
- `Control + 4` → Feature 3 (Desktop 4)

**Or:** Swipe left/right with 3 fingers

**Now you can:**
- Give different tasks to each Claude instance
- Work on multiple features simultaneously
- No merge conflicts (each works in different branch)

---

## Finishing Up

### 5. Merge Work Back to Main

**When a feature is done:**

```bash
# Go back to Desktop 1 (main branch)
cd ~/Library/CloudStorage/Dropbox/jarvis
git checkout main

# Merge the feature branch
git merge <feature-name>

# Example:
git merge add-drums
```

**Handle merge conflicts if needed:**
```bash
# If conflicts occur:
# 1. Open the conflicted files
# 2. Resolve conflicts manually
# 3. Stage the resolved files
git add .
git commit -m "Merge add-drums feature"
```

### 6. Clean Up Worktrees

**Remove worktree when done:**
```bash
wtremove <feature-name>

# Examples:
wtremove add-drums
wtremove fix-bug-123
```

**Or manually:**
```bash
git worktree remove <feature-name> --force
git branch -D <feature-name>  # Delete branch too
```

**Close the VS Code windows** on Desktops 2/3/4.

---

## Useful Commands

### List All Worktrees
```bash
wtlist
# or
git worktree list
```

**Output example:**
```
/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis  361d61a [main]
/Users/terrybyrd/worktrees/jarvis/add-drums           abc1234 [add-drums]
/Users/terrybyrd/worktrees/jarvis/add-bass            def5678 [add-bass]
```

### Check Current Branch
```bash
git branch
# Shows: * <current-branch>
```

### View Git Status
```bash
git status
```

### Reload Shell Config (if wt not found)
```bash
source ~/.zshrc
```

---

## Desktop Layout Example

```
┌─────────────────────────────────────────────────────┐
│ Desktop 1: Main JARVIS (main branch)                │
│ - Original project                                  │
│ - Used for merging, reviewing, coordinating         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Desktop 2: add-drums (add-drums branch)             │
│ - Claude working on drums feature                   │
│ - ~/worktrees/jarvis/add-drums                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Desktop 3: add-bass (add-bass branch)               │
│ - Claude working on bass feature                    │
│ - ~/worktrees/jarvis/add-bass                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Desktop 4: add-keyboards (add-keyboards branch)     │
│ - Claude working on keyboards feature               │
│ - ~/worktrees/jarvis/add-keyboards                  │
└─────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### "wt: command not found"
```bash
source ~/.zshrc
# Or open a new terminal tab
```

### "Branch already exists"
```bash
git worktree remove <branch-name> --force 2>/dev/null || true
git branch -D <branch-name>
wt <branch-name>
```

### Can't move window between desktops
- Use manual drag method in Mission Control (`Control + ↑`)
- Most reliable method that always works

### Wrong directory after wt command
```bash
cd ~/worktrees/jarvis/<feature-name>
```

### Files not copied to worktree
```bash
# Manually copy if needed:
cp ~/Library/CloudStorage/Dropbox/jarvis/.env ~/worktrees/jarvis/<feature-name>/
```

---

## Benefits of This Workflow

✅ **No merge conflicts** - Each Claude works in isolated branch  
✅ **Parallel development** - Multiple features at once  
✅ **Safe isolation** - Main branch stays clean  
✅ **Easy review** - Test each feature separately  
✅ **Fast switching** - Jump between desktops instantly  
✅ **Full context** - Each Claude has complete project  

---

## Related Files

- **Full Setup Guide:** `WORKTREE-GUIDE.md`
- **Desktop Shortcuts:** `DESKTOP-SHORTCUTS-SETUP.md`
- **wt Script Location:** `~/.zshrc` (search for "wt()")

---

**Pro Tip:** Use descriptive branch names like `add-feature`, `fix-bug`, `refactor-component` so you know what each desktop is working on!
