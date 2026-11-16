# Three-Brain LLM System - SETUP COMPLETE ✅

**Date:** May 2, 2026  
**Duration:** 20 minutes  
**Status:** Ready to authenticate and use

---

## What We Built

### Multi-Model AI System

**Architecture:**
```
Claude Code (You) - Main Driver
        ↓
        ├─→ Codex (ChatGPT o1) - Code Review + Rescue
        └─→ Gemini 2.5 Pro - Video/Audio/PDF Analysis
```

**Purpose:** Each model handles what it does best, dramatically improving overall performance.

---

## Components Installed

### 1. Codex CLI (ChatGPT o1)
**Version:** 0.128.0  
**Command:** `codex`  
**Purpose:** Code review, rescue operations

**Capabilities:**
- ✅ Code review (finds real issues Claude misses)
- ✅ Adversarial review (super critical analysis)
- ✅ Rescue mode (when Claude gets stuck in loops)
- ✅ Alternative implementation approaches
- ✅ Breaking out of circular logic

**Cost:** Uses existing ChatGPT subscription
- Plus ($20/month): 50 messages per 3 hours
- Pro ($200/month): Unlimited messages

---

### 2. Gemini CLI (Google AI)
**Version:** 0.40.1  
**Command:** `gemini`  
**Purpose:** Video/audio/PDF analysis, long context

**Capabilities:**
- ✅ Video analysis (up to 2 hours, frame-by-frame)
- ✅ Audio transcription (up to 10 hours)
- ✅ Large PDF processing (200+ pages)
- ✅ 1M token context window
- ✅ Visual overlay extraction from video

**Cost:** FREE
- Flash: 1,500 requests/day (text/images)
- Pro: 50 requests/day (video/audio/PDF)

---

### 3. Three-Brain Auto-Router Skill
**Location:** `skills/three-brain-router/SKILL.md`  
**Purpose:** Intelligent routing to best model

**Auto-routing rules:**
- **Video/audio/PDF** → Gemini (automatically)
- **Code building** → Claude (you're always the driver)
- **Code review** → Codex (after completion)
- **Stuck/failed twice** → Codex rescue (hard stop rule)
- **"Ask all three"** → Parallel consensus

---

## Installation Results

```
✅ Codex CLI installed: /usr/local/bin/codex (v0.128.0)
✅ Gemini CLI installed: /usr/local/bin/gemini (v0.40.1)
✅ Three-Brain skill: skills/three-brain-router/SKILL.md
✅ npm packages: 19 packages installed
```

---

## Next Steps (Authentication Required)

### Authenticate Codex (ChatGPT)

**Run in terminal:**
```bash
codex login
```

**What happens:**
1. Opens browser window
2. Sign in with OpenAI/ChatGPT account
3. Authorize CLI access
4. Returns to terminal (authenticated)

**Verify:**
```bash
codex chat "Hello, test message"
```

---

### Authenticate Gemini

**Run in terminal:**
```bash
gemini login
```

**What happens:**
1. Opens browser window
2. Sign in with Google account
3. Authorize CLI access (Google AI Studio)
4. Returns to terminal (authenticated)

**Verify:**
```bash
gemini chat "Hello, test message"
```

---

## How It Works

### Pattern 1: Build → Review (Default)

**Every time you complete code:**

1. **Claude builds** (automatic, you're the driver)
   ```
   User: "Build JWT middleware"
   Claude: [writes code, saves files]
   ```

2. **Codex reviews** (automatic or on request)
   ```bash
   codex review middleware/jwt.ts
   ```

3. **Claude presents findings**
   ```
   Codex found:
   - High: No JWT secret rotation
   - Medium: Missing expiration check
   - Low: Could add rate limiting
   ```

4. **Claude implements fixes**
   ```
   [Updates code based on Codex feedback]
   ```

---

### Pattern 2: Rescue Mode (Hard Stop Rule)

**When Claude fails twice:**

1. **Detect failure** (same error 2+ times)
   ```
   User: "Fix the auth bug"
   Claude: [tries approach A, fails]
   User: "Still not working"
   Claude: [tries approach A again, fails]
   ```

2. **Auto-trigger rescue**
   ```bash
   codex rescue "Auth failing after password reset.
   Tried: clearing sessions, resetting DB. 
   Still getting 'invalid token' error."
   ```

3. **Codex provides solution**
   ```
   Codex: "Issue isn't sessions or DB. Token invalidation
   happens async. Add await before returning response."
   ```

4. **Claude implements** Codex's recommendation
   ```
   [Implements fix, SUCCESS]
   ```

**Result:** Breaks out of loops, solves stubborn bugs

---

### Pattern 3: Video Analysis (Auto-Route)

**When analyzing videos:**

1. **User provides video**
   ```
   User: "Analyze this Alex Hormozi video, extract transcript
   AND visual overlays, create interactive HTML"
   ```

2. **Auto-route to Gemini** (file extension detected)
   ```bash
   gemini analyze-video downloads/hormozi.mp4
   ```

3. **Gemini extracts**
   - Full transcript (audio → text)
   - Visual overlays (text on screen)
   - Scene descriptions (frame-by-frame)
   - Timestamps

4. **Claude builds** interactive HTML
   - Combines transcript + visuals
   - Searchable interface
   - Jump-to-timestamp links

5. **Codex reviews** HTML
   - Check accuracy
   - Verify structure
   - Suggest improvements

6. **Claude implements** improvements

**Result:** Rich video analysis impossible with single model

---

### Pattern 4: Parallel Consensus

**When asking all three:**

```
User: "Ask all three: Best database for social media app?"

Claude: "PostgreSQL with read replicas..."
↓
codex chat "Best database for social media app?"
Codex: "MongoDB with sharding..."
↓  
gemini chat "Best database for social media app?"
Gemini: "Hybrid: Cassandra + PostgreSQL..."
↓
VERDICT (synthesized): "Hybrid approach best..."
```

**Result:** Three perspectives, better decision

---

## Command Reference

### Codex Commands

**Basic:**
```bash
codex chat "question"              # Interactive query
codex --version                    # Check version
codex login                        # Authenticate
```

**Code Review:**
```bash
codex review <file>                # Review code
codex review --adversarial <file>  # Super critical review
```

**Rescue:**
```bash
codex rescue "problem description"
```

---

### Gemini Commands

**Basic:**
```bash
gemini chat "question"             # Interactive query  
gemini --version                   # Check version
gemini login                       # Authenticate
```

**Analysis:**
```bash
gemini analyze-video <file>        # Video (up to 2hrs)
gemini analyze-audio <file>        # Audio (up to 10hrs)
gemini analyze-pdf <file>          # PDF (200+ pages)
```

---

## Usage Examples

### Example 1: Code Review After Building

**Terminal interaction:**
```
$ claude

You: Build a REST API for user authentication

Claude: [builds API, saves files]

AUTO: After completion, review with Codex

$ codex review src/api/auth.ts

Codex findings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HIGH PRIORITY:
- Line 45: JWT secret hardcoded (use env var)
- Line 78: Password hash rounds too low (current: 8, recommended: 12)

MEDIUM PRIORITY:
- Line 102: No rate limiting on /login endpoint
- Line 156: Error messages leak user existence

LOW PRIORITY:
- Could add refresh token rotation
- Consider adding MFA support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claude: [implements HIGH + MEDIUM fixes]
```

---

### Example 2: Rescue from Loop

**Terminal interaction:**
```
$ claude

You: Fix the database connection timeout

Claude: [increases timeout to 30s]
"Try now"

You: Still timing out

Claude: [adds connection pooling]
"Try now"

You: Still timing out

AUTO-TRIGGER: Failed 2x → Codex rescue

$ codex rescue "DB connection timeout after 10s.
Tried: increase timeout (30s), connection pooling.
Error: 'Connection reset by peer'"

Codex: "Not a timeout issue. Your DB firewall drops
idle connections after 10s. Add keepalive pings every 5s:

connection: {
  keepAlive: true,
  keepAliveInitialDelay: 5000
}
"

Claude: [adds keepalive config]
"Fixed! Connection stable now."
```

---

### Example 3: Video Analysis

**Terminal interaction:**
```
$ claude

You: Analyze this YouTube video, extract both audio transcript
AND visual text overlays, create searchable HTML

Claude: Detected video file → Routing to Gemini

$ gemini analyze-video downloads/alex-hormozi.mp4

Analyzing 8min 55sec video...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRANSCRIPT:
[00:00] "In this video I'll show you..."
[00:15] "The three pillars are..."
...

VISUAL OVERLAYS:
[00:05] Screen text: "$100M OFFERS"
[00:12] Screen text: "3 PILLARS"
[00:45] Handwritten: "Status, Power, Credibility"
...

SCENES:
[00:00-00:10] Wide shot, wooden desk, books visible
[00:10-00:30] Close-up, white paper with blue marker
...

Claude: [builds interactive HTML combining all elements]

$ codex review video-analysis.html

Codex: "Good structure. Add:
- Search functionality for transcript
- Jump-to-timestamp links  
- Mobile responsive CSS"

Claude: [adds improvements]

Output: video-analysis.html (complete, reviewed, polished)
```

---

### Example 4: Parallel Consensus

**Terminal interaction:**
```
$ claude

You: Ask all three: What's the best way to handle file
uploads in a Next.js app?

Claude: "Use Next.js API routes with Multer middleware.
Advantages: Server-side validation, direct S3 upload,
progress tracking. Code example:..."

$ codex chat "Best way to handle file uploads in Next.js?"

Codex: "Client-side pre-signed URLs for S3. Advantages:
No server bandwidth, faster uploads, built-in retry.
Use @aws-sdk/s3-request-presigner. Code example:..."

$ gemini chat "Best way to handle file uploads in Next.js?"

Gemini: "Hybrid approach: Small files (<10MB) via API route,
large files via presigned URLs. Reasoning: API routes good
for validation/processing, presigned URLs good for efficiency.
Also consider Vercel Blob for simplicity."

VERDICT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended: Gemini's hybrid approach

Small files (<10MB):
→ Next.js API route + Multer
→ Server validates, processes, stores
→ Good for images, documents

Large files (>10MB):
→ Presigned S3 URLs from API
→ Client uploads directly to S3
→ Good for videos, archives

Why hybrid wins:
✅ Best of both (security + performance)
✅ Proven pattern (YouTube, Dropbox)
✅ Scales to millions of users

Implementation: [code example combining both]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Integration with Memory System

**Works seamlessly with 3-phase memory:**

**Phase 1 (Auto-Memory):**
- Tracks current phase state
- "What are we working on NOW?"

**Phase 2 (Claude-Mem):**
- Captures Codex reviews automatically
- Stores Gemini analysis outputs
- Searchable: "Find the video analysis we did last week"

**Phase 3 (Beads):**
- Files issues from Codex findings
- Tracks rescue operations
- Dependencies: "Tests blocked until Codex review complete"

**Together:**
```bash
# Codex finds bug
codex review auth.ts
→ "High: JWT secret rotation missing"

# Claude files issue
bd create --title="Fix: JWT secret rotation" \
         --description="From Codex review" \
         --priority=1

# Phase 2 captures for future
Claude-Mem: Stores Codex finding with full context

# Phase 3 tracks until done
bd show jarvis-abc123
→ Status: in_progress
→ Blocked by: None
→ Created from: codex-review-auth.md
```

**Result:** Three-brain system + three-phase memory = complete AI development environment

---

## Troubleshooting

### "codex: command not found"

**Check installation:**
```bash
which codex
# Should show: /usr/local/bin/codex (or /opt/homebrew/bin/codex)
```

**If not found:**
```bash
npm install -g @openai/codex
hash -r  # Refresh shell PATH
```

---

### "gemini: command not found"

**Check installation:**
```bash
which gemini
# Should show: /usr/local/bin/gemini
```

**If not found:**
```bash
npm install -g @google/gemini-cli
hash -r  # Refresh shell PATH
```

---

### "Authentication required"

**For Codex:**
```bash
codex login
# Opens browser → Sign in to ChatGPT → Authorize
```

**For Gemini:**
```bash
gemini login  
# Opens browser → Sign in to Google → Authorize (AI Studio)
```

---

### "Codex rate limit exceeded"

**Check tier:**
- Plus ($20/mo): 50 messages per 3 hours
- Pro ($200/mo): Unlimited

**Solutions:**
- Wait for rate limit reset (3 hours)
- Upgrade to Pro tier
- Use less frequently (only for reviews/rescues)

---

### "Gemini rate limit exceeded"

**Check usage:**
- Flash: 1,500 requests/day (resets daily)
- Pro: 50 requests/day (resets daily)

**Solutions:**
- Wait 24 hours for reset
- Use Flash tier for text/images (saves Pro requests)
- Upgrade to paid tier (if available)

---

## Best Practices

### DO ✅

- **Use Claude for all coding** (you're the driver, always)
- **Auto-invoke Codex after completion** (catch issues early)
- **Route video/audio/PDF to Gemini** (it's built for this)
- **Hand off after 2 failures** (hard stop rule prevents loops)
- **Save all outputs** (Codex reviews, Gemini analysis)
- **File Beads issues** from Codex findings
- **Use parallel consensus** for important decisions

---

### DON'T ❌

- **Don't review your own code** (blind spots, Claude can't see own errors)
- **Don't retry same approach 3+ times** (hand off to Codex)
- **Don't analyze videos with Claude** (use Gemini, it has native support)
- **Don't forget to save outputs** (file all Codex/Gemini results)
- **Don't ignore Codex findings** (they're usually right)
- **Don't skip authentication** (CLIs won't work without it)

---

## Cost Summary

### Total Monthly Cost

**Minimum setup:**
```
Claude Code: $20/month (or $200/month Pro)
ChatGPT: $20/month (Plus) - already have for Codex
Gemini: $0/month (free tier)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: $40/month (or $220/month Pro)
```

**What you get:**
- Claude: Unlimited coding (main driver)
- Codex: 50 reviews/3hrs (or unlimited on Pro)
- Gemini: 1,500 text + 50 video/day (FREE)

**Alternative (if don't have ChatGPT):**
```
Claude Code: $20/month
ChatGPT Plus: $20/month (for Codex)
Gemini: $0/month
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: $40/month
```

**Value:**
- 3 AI models for the price of 2
- Gemini completely free (massive value)
- Codex uses existing ChatGPT subscription (no extra cost)

---

## Session Close Protocol

**When using Codex/Gemini in session:**

1. **Save all outputs:**
   ```bash
   # Codex reviews
   reviews/2026-05-02-codex-auth.md
   
   # Gemini analysis
   analysis/2026-05-02-gemini-video-hormozi.html
   ```

2. **File issues from findings:**
   ```bash
   bd create --title="From Codex: JWT rotation missing" \
            --description="..." --priority=1
   ```

3. **Standard close:**
   ```bash
   bd close <completed>
   git add . && git commit -m "..."
   git push
   ```

---

## Success Metrics

**After three-brain setup:**

✅ **Fewer bugs** (Codex catches what Claude misses)  
✅ **No more loops** (Codex rescue breaks circular logic)  
✅ **Video analysis** (Gemini unlocks new capabilities)  
✅ **Better decisions** (parallel consensus from 3 models)  
✅ **Faster development** (right model for right job)  

**You should notice:**
- Higher code quality (Codex reviews catch real issues)
- Less frustration (rescue mode breaks stuck situations)
- New capabilities (video/audio/PDF analysis)
- More confidence (three brains better than one)

---

## Resources

**Official Documentation:**
- Codex: https://platform.openai.com/docs/guides/codex
- Gemini: https://ai.google.dev/gemini-api/docs

**JARVIS Skill:**
- `skills/three-brain-router/SKILL.md`

**Commands:**
```bash
codex --help    # Full Codex command list
gemini --help   # Full Gemini command list
```

---

**Built:** May 2, 2026  
**Time:** 20 minutes  
**Status:** ✅ Installed, ready to authenticate

**Next steps:**
1. Run `codex login` in terminal
2. Run `gemini login` in terminal  
3. Test: `codex chat "hello"` and `gemini chat "hello"`
4. Start using three-brain system!

---

## Summary

**What you have:**
- **Claude Code** (main driver) - builds, refactors, files
- **Codex** (reviewer + rescue) - catches bugs, breaks loops
- **Gemini** (analyzer) - videos, audio, PDFs, long context

**What it unlocks:**
- No more blind spots (Codex sees what Claude misses)
- No more loops (rescue mode breaks stuck situations)
- Video analysis (Gemini's native capability)
- Better decisions (three perspectives vs one)

**Cost:** $40/month (or $220/month Pro)  
**Value:** Dramatically improved development quality

**Authenticate now and start using the three-brain system! 🧠🧠🧠**
