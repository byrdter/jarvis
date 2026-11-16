# Three-Brain System - Quick Reference

**Status:** ✅ FULLY OPERATIONAL  
**Updated:** May 2, 2026

---

## Quick Commands

### Codex (GPT-5.5)
```bash
# Non-interactive (one-shot)
codex exec "your prompt"

# Code review
codex review path/to/file.ts

# Interactive session
codex "initial prompt"
codex  # No prompt, starts blank session

# Specify model (if needed)
codex exec --model gpt-5.5 "prompt"
```

---

### Gemini (Google AI)
```bash
# Non-interactive (headless)
gemini -p "your prompt"

# Interactive session
gemini "initial prompt"
gemini  # No prompt, starts blank session

# With specific model
gemini -p "prompt" --model gemini-2.5-pro
```

---

## Working Models

### Codex (with ChatGPT Subscription)
- ✅ **gpt-5.5** (default, recommended)
- ✅ **gpt-5.4**
- ✅ **gpt-5.4-mini**
- ✅ **gpt-5.3-codex**
- ✅ **gpt-5.2**

**Config location:** `~/.codex/config.toml`  
**Current default:** `gpt-5.5`

---

### Gemini (Free Tier)
- ✅ **gemini-2.5-pro** (default, 50 requests/day)
- ✅ **gemini-2.5-flash** (1,500 requests/day)

---

## Three-Brain Workflow

### Pattern 1: Build → Review
```bash
# 1. Claude builds code (in Claude Code session)
You: "Build JWT middleware for Express"
Claude: [writes code, saves to middleware/jwt.ts]

# 2. Review with Codex
$ codex review middleware/jwt.ts

Codex response:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HIGH:
- Line 23: JWT secret hardcoded
- Line 45: No token expiration check

MEDIUM:
- Line 67: Missing rate limiting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 3. Claude implements fixes
Claude: [fixes issues found by Codex]
```

---

### Pattern 2: Rescue Mode
```bash
# When Claude fails 2+ times on same task

$ codex exec "Problem: Database timeout after 10s.
Tried: increased timeout, added pooling.
Still getting 'Connection reset by peer'"

Codex: [provides fresh perspective, breaks the loop]
```

---

### Pattern 3: Video Analysis
```bash
# Analyze video with Gemini
$ gemini -p "Analyze this video: downloads/video.mp4
Extract: transcript, visual text overlays, scene descriptions"

Gemini: [provides comprehensive analysis]

# Then Claude builds interactive HTML from Gemini's output
```

---

### Pattern 4: Parallel Consensus
```bash
# Ask all three models same question

# 1. Claude responds (you're already here)
You: "Best database for social media app?"
Claude: "PostgreSQL with read replicas..."

# 2. Get Codex opinion
$ codex exec "Best database for social media app with 1M users?"
Codex: "MongoDB with sharding..."

# 3. Get Gemini opinion  
$ gemini -p "Best database for social media app with 1M users?"
Gemini: "Hybrid: Cassandra + PostgreSQL..."

# 4. Claude synthesizes verdict
Claude: [compares all three, provides final recommendation]
```

---

## Common Use Cases

### Code Review (After Building)
```bash
codex review src/api/auth.ts
codex review --adversarial src/security/crypto.ts  # Super critical
```

### Video Analysis
```bash
gemini -p "Analyze video: downloads/tutorial.mp4
Extract both audio transcript AND visual text overlays
Create timeline with timestamps"
```

### Large PDF Processing
```bash
gemini -p "Summarize this 200-page contract: docs/agreement.pdf
Focus on: liabilities, termination clauses, payment terms"
```

### Rescue from Loop
```bash
codex exec "Problem: [describe issue]
What Claude tried: [list attempts]  
Current error: [error message]
Suspected cause: [hypothesis]"
```

### Debate/Consensus
```bash
# Get multiple perspectives on important decisions
codex exec "Should we use microservices or monolith for this 3-person startup?"
gemini -p "Should we use microservices or monolith for this 3-person startup?"
# Then compare with Claude's view
```

---

## Authentication Status

```bash
# Check Codex login
codex login status
# Output: "Logged in using ChatGPT"

# Check Gemini (no status command, just try it)
gemini -p "test"
```

---

## Configuration Files

### Codex Config
**Location:** `~/.codex/config.toml`

**Current settings:**
```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
personality = "pragmatic"
```

**To change model:**
```bash
# Edit config file
nano ~/.codex/config.toml

# Or override per command
codex exec --model gpt-5.4 "prompt"
```

---

### Gemini Config
**Location:** `~/.gemini/config` (auto-created)

**Override per command:**
```bash
gemini -p "prompt" --model gemini-2.5-flash  # Faster, more quota
```

---

## Cost & Limits

### Codex (ChatGPT Subscription)
**Plus ($20/month):**
- ~50 messages per 3 hours
- GPT-5.5 access
- Resets every 3 hours

**Pro ($200/month):**
- Unlimited messages
- GPT-5.5 access
- Priority access

**Current subscription:** Plus or Pro (whichever you have)

---

### Gemini (FREE)
**Flash:**
- 1,500 requests/day
- Fast responses
- Good for text/images

**Pro:**
- 50 requests/day  
- Video analysis (up to 2 hours)
- Audio analysis (up to 10 hours)
- Large PDFs (200+ pages)
- 1M token context

**Resets:** Daily (midnight UTC)

---

## Troubleshooting

### "Model not supported with ChatGPT account"
**Solution:** Use `gpt-5.5` (or gpt-5.4, gpt-5.3, etc.)
```bash
# Update config
echo 'model = "gpt-5.5"' > ~/.codex/config.toml

# Or specify per command
codex exec --model gpt-5.5 "prompt"
```

---

### "Not authenticated"
```bash
# Codex
codex login  # Opens browser

# Gemini
gemini login  # Opens browser (Google AI Studio)
```

---

### "Rate limit exceeded" (Codex)
**ChatGPT Plus:** 50 messages per 3 hours
- Wait for reset (check timer in ChatGPT web)
- Or upgrade to Pro ($200/month, unlimited)

---

### "Rate limit exceeded" (Gemini)
**Free tier:**
- Flash: 1,500/day
- Pro: 50/day

**Solution:**
- Wait until midnight UTC (daily reset)
- Use Flash for simple queries (saves Pro quota)
- Upgrade to paid tier (if available)

---

## Integration with JARVIS

### With Claude-Mem (Phase 2)
```bash
# Codex reviews get captured automatically
codex review auth.ts
→ Claude-Mem stores finding with full context
→ Searchable: "Find Codex review about JWT"
```

### With Beads (Phase 3)
```bash
# Create issues from Codex findings
codex review api/endpoints.ts

# Codex finds: "Missing rate limiting on /login"

# Claude files issue
bd create --title="Add rate limiting to /login" \
         --description="From Codex review: api/endpoints.ts line 45" \
         --type=bug --priority=1
```

---

## Examples

### Example 1: Full Workflow
```bash
# 1. Build (Claude)
You: "Create user authentication system"
Claude: [builds auth system]

# 2. Review (Codex)
$ codex review src/auth/

# 3. Fix (Claude)
Claude: [implements Codex findings]

# 4. Document (Beads)
$ bd create --title="Auth system complete" \
           --description="Built with JWT, reviewed by Codex" \
           --type=feature
$ bd close jarvis-abc123

# 5. Memory (Claude-Mem)
# Automatically captured by Phase 2
```

---

### Example 2: Video Analysis
```bash
# 1. Gemini analyzes
$ gemini -p "Analyze: downloads/hormozi.mp4
Extract: transcript + visual overlays + timestamps"

# 2. Claude processes
You: "Create searchable HTML from Gemini's analysis"
Claude: [builds interactive interface]

# 3. Codex reviews
$ codex review video-analysis.html

# 4. Claude improves
Claude: [adds Codex suggestions]
```

---

### Example 3: Rescue Scenario
```bash
# Claude gets stuck
You: "Fix the WebSocket connection issue"
Claude: [tries approach A, fails]
You: "Still not working"
Claude: [tries approach A again, fails]

# Auto-trigger rescue (or manual)
$ codex exec "WebSocket connection drops after 30s.
Tried: keepalive pings, reconnection logic.
Error: 'WebSocket closed before connection established'"

Codex: "Issue is CORS configuration. Your WebSocket 
handshake is getting blocked. Add these headers:
Access-Control-Allow-Origin, 
Access-Control-Allow-Credentials..."

Claude: [implements Codex solution, SUCCESS]
```

---

## Tips

### DO ✅
- Use Codex for **code review** after building
- Use Gemini for **videos/audio/large PDFs**
- Use all three for **important decisions** (parallel consensus)
- Let **Claude drive** (you're the IDE, always)
- Save **all outputs** (Codex reviews, Gemini analysis)

### DON'T ❌
- Don't let Claude review its own code (use Codex)
- Don't analyze videos with Claude (use Gemini)
- Don't retry same approach 3+ times (use Codex rescue)
- Don't forget to save outputs to files
- Don't use wrong models (gpt-5.5 for Codex, not gpt-5.1-codex-max)

---

## Quick Tests

### Test Codex
```bash
codex exec "What is 2+2? Respond with just the number."
# Should output: 4
```

### Test Gemini
```bash
gemini -p "What is 2+2? Respond with just the number."
# Should output: 4
```

### Test Code Review
```bash
# Create test file
echo 'const password = "hardcoded123";' > test.js

# Review it
codex review test.js
# Should flag: hardcoded password
```

---

**Ready to use! All three brains operational.** 🧠🧠🧠

**Summary:**
- **Claude Code (you)**: Main driver, coding, building
- **Codex (GPT-5.5)**: Code review, rescue, fresh perspectives
- **Gemini**: Video/audio/PDF analysis, long context

**Total cost:** $20-200/month (ChatGPT subscription) + $0 (Gemini free)

**Power:** 3 AI models working together > 1 model alone
