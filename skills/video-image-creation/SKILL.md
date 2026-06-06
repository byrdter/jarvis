# Video Image Creation Skill

> **LEGACY / SUPPORTING ASSET SKILL:** This is no longer the main video-production workflow. Current Jarvis videos use a mixed faceless production stack: HyperFrames, real screenshots, web artifacts, B-roll, code/terminal simulations, diagrams, generated clips, and occasional stills. Use `.agents/skills/jarvis-video-production/SKILL.md` for full videos. Use this skill only for thumbnails, concept frames, or one-off generated still assets.

**Purpose:** Create high-quality, story-driven images for Byrddynasty educational videos that are simple, colorful, and visually engaging.

**Core Philosophy:** Images should tell the story through visuals, not text. Large headings, vibrant colors, and clear visual metaphors trump detailed explanations.

---

## Process Overview

```
Script Review → Image Planning → Prompt Crafting → Quality Check → Delivery
```

**One script segment = One image number (001, 002, 003...)**

### CRITICAL TIMING REQUIREMENT

**Each script segment must be 20-30 seconds maximum.**

- ✅ 20-30 seconds: Ideal for viewer attention
- ⚠️ 30-40 seconds: Maximum acceptable for complex concepts
- ❌ 40+ seconds: Too long - MUST break into multiple segments

**Why this matters:**
- Viewer attention drops after 30 seconds without visual change
- Educational videos need visual variety to maintain engagement
- One image on screen for 60-90 seconds kills retention

**If a script segment exceeds 30 seconds:**
1. Break it into multiple smaller segments (002A → 002, 003, 004)
2. Create separate image for each new segment
3. Maintain 1:1 script-to-image ratio

**Example:**
- ❌ WRONG: Segment 003 is 150 seconds with 1 image
- ✅ RIGHT: Break into Segments 003, 004, 005, 006, 007 (5 images, 30 sec each)

---

## Part 1: Image Planning from Script

### Step 1.1: Analyze the Script
Read through the complete video script and identify:
- **Key concepts** that need visualization
- **Natural transitions** between ideas
- **Data points** that need emphasis (percentages, timelines, comparisons)
- **Story beats** (problem → insight → solution)

### Step 1.2: Map Script to Image Numbers
Create a simple numbered sequence:

```
001 - [Main title/hook concept]
002 - [First major point]
003 - [Supporting data/example]
004 - [Transition concept]
005 - [Second major point]
...
```

**CRITICAL:**
- Each number = one complete thought/segment
- NO sub-numbering (001A, 001B) - just increment to next number
- If a concept needs multiple visuals, use separate numbers (002, 003, 004)

### Step 1.3: Determine Visual Type
For each image number, identify which visualization type fits best:

**Progression/Timeline:**
- Stages (Stage 1 → Stage 2 → Stage 3)
- Timeline with milestones
- Before → After transformations
- Step-by-step flows

**Comparison/Contrast:**
- Side-by-side split screens
- Top vs. Bottom contrasts
- This vs. That

**Data Visualization:**
- Large prominent statistics (346%, 85%)
- Line charts with zones (green/yellow/red)
- Bar charts showing comparisons
- Pie charts for splits

**Cycle/Loop:**
- Circular diagrams showing repeating patterns
- Feedback loops
- Paradox cycles

**Concept Illustration:**
- Central concept with surrounding elements
- Metaphorical scenes (treadmill progression, dashboard views)
- Icon-based explanations

---

## Part 2: Crafting Image Prompts

### Image Prompt Template

```
**Image [NUMBER]: [VISUAL TYPE]**

**Concept:** [What story does this tell?]

**Visual Elements:**
- [Primary element 1]
- [Primary element 2]
- [Primary element 3]

**Text on Image:**
- Main Heading: "[LARGE PROMINENT TEXT]"
- Subheading (if needed): "[Brief secondary text]"
- Data/Labels: "[Key numbers or short labels]"
- Source citation (if applicable): "[Source name]"

**Color Palette:**
- [Primary colors and their meaning/zones]
- [Background style - gradient, solid, zoned]

**Style Notes:**
- [Specific illustration style - infographic, realistic, cartoon-like]
- [Mood/tone - professional, energetic, cautionary]
- [Any specific visual metaphors]

**Image Generation Prompt:**
[Complete DALL-E/Midjourney prompt following style guide]
```

### Style Guide Principles

**DO:**
- ✅ Use rich, vibrant colors with purpose (green = good, red = danger, yellow = caution)
- ✅ Create gradient backgrounds or color-zoned regions
- ✅ Make headlines LARGE and bold
- ✅ Use illustrations, icons, and visual metaphors
- ✅ Show progression with arrows and flows
- ✅ Feature numbers/stats prominently (large size, bold)
- ✅ Keep explanatory text minimal (1-2 lines max per section)
- ✅ Use visual separation (split screens, bordered sections)
- ✅ Include small source citations at bottom when using data

**DON'T:**
- ❌ Create text-heavy slides with paragraphs
- ❌ Use drab, boring boxes or plain layouts
- ❌ Over-explain with text - let visuals do the talking
- ❌ Cram too many concepts into one image
- ❌ Use generic stock photo styles
- ❌ Make multiple versions of same concept (no 001A, 001B splits)

### Specific Visual Patterns (Based on Reference Images)

**Pattern 1: Stage Progression**
Example: 001CB (Stage 1 → Stage 2 → Stage 3)
- Horizontal flow with arrows
- Each stage in distinct visual section
- Clear labels (Stage 1, Stage 2, Stage 3)
- Simple icons/diagrams per stage
- Minimal text per stage (2-3 lines)
- Background color or accent per stage

**Pattern 2: Prominent Statistics**
Example: 002AB (18-Month Automation Progression)
- ONE giant number as focal point (346%, 85%)
- Timeline arrow or progression bar
- Color-coded zones (green/yellow/red)
- Brief labels for context
- Large heading at top or bottom

**Pattern 3: Circular Cycle**
Example: Productivity Paradox Cycle
- Central concept in middle
- 3-4 stages around circle with arrows
- Each stage has small illustration
- Brief text per stage
- Quote or key insight below

**Pattern 4: Split Comparison**
Example: Manager vs Employee Reality (004A)
- Top half: One perspective
- Bottom half: Contrasting perspective
- Clear visual separation
- Contrasting visuals (polished vs stressed)
- Labels showing the contrast

**Pattern 5: Data Chart with Zones**
Example: AI Tool Usage Chart (006A)
- X/Y axis chart as main element
- Color zones (green = optimal, yellow = marginal, red = negative)
- Annotations on chart (callout boxes)
- Large heading below chart
- Data points clearly labeled

**Pattern 6: Timeline Progression**
Example: Treadmill Speed Progression (003B)
- 3-panel side-by-side timeline
- Same scene evolving over time
- Labels showing progression (Month 1, Month 6, Month 18)
- Visual changes showing progression (speed increasing)
- Caption below summarizing insight

---

## Part 3: Quality Checklist

Before delivering any image prompts, verify:

### Visual Clarity
- [ ] Primary concept is immediately clear
- [ ] Visual hierarchy guides eye to most important element
- [ ] Colors have meaning (not random)
- [ ] Image tells a story without narration

### Text Balance
- [ ] Headlines are LARGE and prominent
- [ ] Explanatory text is minimal (2-3 lines max per section)
- [ ] Text supports visuals (not replaces them)
- [ ] Font sizes create clear hierarchy

### Color & Design
- [ ] Rich, vibrant color palette
- [ ] NOT just boxes and drab colors
- [ ] Gradients or zones used purposefully
- [ ] Professional but engaging style

### Simplicity
- [ ] ONE main concept per image
- [ ] NOT overcrowded with details
- [ ] Clean visual separation if multiple elements
- [ ] Easy to understand at a glance

### Numbering
- [ ] Simple sequential numbering (001, 002, 003...)
- [ ] NO sub-versions (001A, 001B, 001C)
- [ ] Each number maps to one script segment
- [ ] Easy to match with script for video production

---

## Part 4: Delivery Format

### Complete Deliverable Package

```markdown
# Video Images: [Video Title]

## Image Sequence Map
001 - [Concept name]
002 - [Concept name]
003 - [Concept name]
...

---

## Image 001: [Visual Type]

**Concept:** [Story this tells]

**Visual Elements:**
- [Element 1]
- [Element 2]
- [Element 3]

**Text on Image:**
- Main Heading: "[TEXT]"
- Subheading: "[TEXT]"
- Labels: "[TEXT]"

**Color Palette:**
- [Colors and zones]

**Image Generation Prompt:**
[Complete prompt for DALL-E/Midjourney]

---

## Image 002: [Visual Type]

[Repeat format...]

---

## Production Notes

**Style Consistency:**
- [Any cross-image consistency notes]

**Source Credits:**
- [Data sources to cite]

**Video Production Tips:**
- [Timing suggestions]
- [Transition ideas]
```

---

## Part 5: Execution Protocol

### When User Requests Video Images

**Step 1:** Read the script thoroughly
- Identify all major concepts
- Note data points and key messages
- Understand the narrative flow

**Step 2:** Create image sequence map
- Simple numbering (001, 002, 003...)
- One concept per number
- Map to script segments

**Step 3:** For EACH image, determine:
- Visual type (progression, comparison, data, cycle, etc.)
- Main elements
- Text content (headlines, labels)
- Color approach
- Style notes

**Step 4:** Write complete image prompts
- Follow template format
- Include all details
- Craft DALL-E/Midjourney prompt

**Step 5:** Quality check against checklist
- Verify simplicity
- Check color/visual appeal
- Confirm text balance
- Validate numbering

**Step 6:** Deliver complete package
- Sequence map
- All image prompts
- Production notes

---

## Reference Quality Examples

**Location 1:** `${JARVIS_PRIVATE}/apps/content-creation/video-generator/ProjectsNew/ai-brain-fry-video-3-sloperator/images`
- 001A - Tier 1 vs Tier 2 divergence (circular flow)
- 001CB - 3-Stage progression (simple, clean)
- 002AB - Timeline with prominent percentages
- 002BB - Automation progression zones
- 002CB - ActivTrak study data (large number + chart)
- 004BB - 80/20 practice rule (pie + contrast boxes)
- 005BC - Sloperator vs Orchestrator comparison

**Location 2:** `${JARVIS_PRIVATE}/apps/content-creation/video-generator/ProjectsNew/ai-brain-fry-video-2-capacity-reuse/images`
- 001A - Productivity Paradox Cycle (circular)
- 001B - 4-stage cycle diagram
- 001C - ActivTrak data (prominent stats)
- 002B - Capacity reuse concept
- 002C - Parkinson's Law timeline
- 003A - AI Productivity Paradox (4-stage cycle)
- 003B - Treadmill progression timeline
- 004A - Manager vs Employee split screen
- 004B - Same illustration different style
- 006A - Tool usage chart with zones
- 007B - Data chart comparison

**When in doubt, reference these images for:**
- Color vibrancy
- Text-to-visual ratio
- Layout simplicity
- Story-telling approach

---

## Critical Reminders

1. **Each script segment = 20-30 seconds MAX** (break longer segments into multiple images)
2. **ONE concept = ONE number** (no 001A, 001B nonsense)
3. **Visuals tell the story** (not text blocks)
4. **Colorful and artistic** (not drab boxes)
5. **Simple but engaging** (not over-detailed)
6. **Headlines are LARGE** (supporting text is brief)
7. **Easy video production** (sequential numbering matches script)

---

## Success Criteria

An image set is successful when:
- Terry can copy-paste prompts into image generator
- Images match script segments 1:1 with simple numbering
- Each image tells its story visually
- Colors are vibrant and purposeful
- Text is minimal but effective
- Production process is straightforward (script → images → Heygen)
- No confusion about which image goes where

---

## Notes for Claude

**Before creating images:**
1. Ask: "Have I read the complete script?"
2. Ask: "Is each script segment 20-30 seconds max?" (If no, break it up!)
3. Ask: "Do I understand the story arc?"
4. Ask: "Can each concept be ONE image?"
5. Ask: "Am I using simple sequential numbering?"
6. Ask: "Are my prompts visual-first, text-second?"
7. Ask: "Would Terry approve this style?"

**If unsure:** Reference the example images listed above.

**Remember:** Simple, colorful, story-driven. Not text-heavy, not drab, not complicated.

---

## Pause-as-Scene-Marker Pattern (Recording Protocol)

**Status:** Codified 2026-04-25 from a workflow habit developed in practice on Videos 4-7.

When recording narration (avatar in HeyGen, or future on-camera takes), use deliberate pauses as **scene-change signals** that downstream automation can detect.

### The protocol — three rules

1. **Pause ~1-1.5 seconds** between distinct ideas → indicates scene change
2. **Don't pause** within a single thought → keep it as one scene
3. **Pause ~2-3 seconds** at major Act/Phase transitions → emphasis cut

### Why this works for HeyGen avatar narration

HeyGen renders SSML `<break>` tags to **deterministic millisecond precision**. In your script:

```
Here's the problem nobody talks about. <break time="1.5s"/>
Your AI doesn't break. <break time="1s"/>
The knowledge around it breaks.
```

The avatar pauses *exactly* the duration you specify. The downstream automation pipeline reads gaps via AssemblyAI word-level timestamps and treats them as **hard scene boundaries** — no single visual treatment is allowed to cross a pause longer than 1 second.

### Optional — encode scene treatment hints in the script

For maximum directorial control, add bracketed hints between paragraphs:

```
[SCENE: face-fullscreen]
Every knowledge base I've built rotted in ninety days. <break time="1.5s"/>

[SCENE: face-corner + loop-diagram + stages: detect, draft, approve, apply]
Here's the closed loop. <break time="1s"/>

[SCENE: no-face + vhs-agent-theater + cmd: jarvis detect broken-links]
Watch what happens when I run this.

[STATIC: ./assets/architecture.png · 6 sec]
And here's the architecture. <break time="6s"/>
```

The bracketed lines are stripped before HeyGen rendering but kept in the script-as-source for the pipeline director, which uses them as constraints on its visual-library lookup.

### Why this beats topic-detection from text

Pure text-based topic detection is ~70% accurate. Pause-detection is 100% accurate — you intentionally signaled the cut. The pipeline can't misread your intent.

### See also

- `/jarvis/AUTOMATED-VIDEO-PIPELINE-PLAN.md` — full automation architecture
- `/jarvis/video-pipeline/scripts/transcribe.ts` — AssemblyAI wrapper that produces word-level JSON
