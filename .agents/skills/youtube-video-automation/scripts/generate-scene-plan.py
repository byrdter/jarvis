#!/usr/bin/env python3
"""
generate-scene-plan.py — Generate visual treatment board from transcript

Usage:
    python3 generate-scene-plan.py \\
        --transcript assets/transcript.json \\
        --brief episode-brief.md \\
        --output visual-treatment-board.md
"""

import json
import argparse
import re
from pathlib import Path
from collections import Counter

# Visual registers from PRESENTATION-VARIETY.md
VISUAL_REGISTERS = [
    "Real Tool Screenshots",
    "Code And Terminal Action",
    "Web Rolls And Source Proof",
    "Self-Drawing Diagrams",
    "Documentary B-Roll",
    "Pixel / Generated B-Roll",
    "Data Visualization Beats",
    "Generated Sites / Interactive Surfaces",
    "Talking-Head Substitutes",
    "Audio Variety",
    "Pacing Variety"
]

def load_transcript(path):
    """Load transcript.json"""
    with open(path, 'r') as f:
        data = json.load(f)
    return data.get('words', [])

def load_brief(path):
    """Extract preferences from episode brief"""
    if not Path(path).exists():
        return {}

    with open(path, 'r') as f:
        content = f.read()

    # Extract visual register preferences (simple parsing)
    prefs = {}
    if "Visual Register Preferences" in content:
        section = content.split("Visual Register Preferences")[1].split("##")[0]
        for line in section.split('\n'):
            if '(' in line and ')' in line:
                parts = line.split('(')
                if len(parts) >= 2:
                    register = parts[0].strip(' -')
                    pref = parts[1].split(')')[0].strip()
                    prefs[register] = pref

    return prefs

def segment_transcript(words, target_scene_duration=25):
    """
    Segment transcript at natural pauses.
    Target ~25 seconds per scene (adjustable).
    """
    segments = []
    current_segment = []
    segment_start = 0

    for i, word in enumerate(words):
        current_segment.append(word)

        # Check if we should break into new segment
        duration_so_far = word.get('end', 0) - segment_start

        # Look for natural pause + duration threshold
        if i < len(words) - 1:
            gap = words[i + 1].get('start', 0) - word.get('end', 0)

            # Break if: pause ≥1.5s AND duration ≥15s OR duration >40s (force break)
            if (gap >= 1.5 and duration_so_far >= 15) or duration_so_far > 40:
                segments.append({
                    'words': current_segment,
                    'start': segment_start,
                    'end': word.get('end', 0),
                    'duration': round(duration_so_far, 1)
                })
                current_segment = []
                segment_start = words[i + 1].get('start', 0) if i + 1 < len(words) else word.get('end', 0)

    # Add final segment
    if current_segment:
        duration_so_far = current_segment[-1].get('end', 0) - segment_start
        segments.append({
            'words': current_segment,
            'start': segment_start,
            'end': current_segment[-1].get('end', 0),
            'duration': round(duration_so_far, 1)
        })

    return segments

def extract_keywords(words, top_n=10):
    """Extract top keywords from word list"""
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "what", "which", "who", "when", "where", "why", "how", "your", "our", "their"}

    # Extract words and clean
    text_words = [w.get('text', '').lower().strip('.,!?;:') for w in words]
    text_words = [w for w in text_words if w and w not in stopwords and len(w) > 2]

    # Count frequency
    freq = Counter(text_words)
    return [word for word, count in freq.most_common(top_n)]

def assign_visual_register(scene_num, keywords, preferences, prev_registers):
    """
    Assign visual register for scene.
    Apply variety gate: no more than 3 consecutive same register.
    """
    # Simple heuristic based on keywords
    keyword_set = set(keywords)

    # Check for specific content types
    if any(k in keyword_set for k in ['code', 'terminal', 'command', 'programming', 'git']):
        register = "Code And Terminal Action"
    elif any(k in keyword_set for k in ['data', 'statistics', 'percent', 'chart', 'graph', 'number']):
        register = "Data Visualization Beats"
    elif any(k in keyword_set for k in ['screenshot', 'interface', 'ui', 'app', 'platform']):
        register = "Real Tool Screenshots"
    elif any(k in keyword_set for k in ['web', 'website', 'page', 'article', 'docs', 'documentation']):
        register = "Web Rolls And Source Proof"
    elif any(k in keyword_set for k in ['diagram', 'flow', 'architecture', 'process', 'system']):
        register = "Self-Drawing Diagrams"
    else:
        # Default to B-roll
        register = "Documentary B-Roll"

    # Variety gate: check last 2 registers
    if len(prev_registers) >= 2 and prev_registers[-1] == prev_registers[-2] == register:
        # Used same register 2 times already, force variety
        # Pick next most likely register
        if register == "Documentary B-Roll":
            register = "Data Visualization Beats"
        else:
            register = "Documentary B-Roll"

    return register

def generate_scene_plan(segments, preferences):
    """Generate visual treatment board content"""
    scenes = []
    prev_registers = []

    for i, segment in enumerate(segments):
        scene_num = i + 1

        # Extract text
        text = ' '.join([w.get('text', '') for w in segment['words']])

        # Extract keywords
        keywords = extract_keywords(segment['words'], top_n=8)

        # Assign visual register
        register = assign_visual_register(scene_num, keywords, preferences, prev_registers)
        prev_registers.append(register)

        # Determine avatar timing (first and last scene usually have avatar)
        if scene_num == 1 or scene_num == len(segments):
            avatar_timing = "0-{}s: Avatar introduction/conclusion".format(int(segment['duration']))
            broll_plan = "None (avatar full-screen)"
        else:
            avatar_timing = "None (full B-roll)"
            # Simple B-roll plan (placeholder - needs real asset matching)
            broll_plan = "0-{}s: B-roll matching keywords: {}".format(
                int(segment['duration']),
                ', '.join(keywords[:3])
            )

        # Scene pacing
        if segment['duration'] < 15:
            pacing = "Quick (multiple visual changes)"
        elif segment['duration'] > 30:
            pacing = "Slow (long holds with subtle motion)"
        else:
            pacing = "Medium (one visual change every 5-7s)"

        # Build scene entry
        scene = {
            'number': scene_num,
            'title': f"Scene {scene_num:02d}",
            'duration': segment['duration'],
            'vo_summary': text[:200] + "..." if len(text) > 200 else text,
            'keywords': keywords,
            'register': register,
            'avatar_timing': avatar_timing,
            'broll_plan': broll_plan,
            'pacing': pacing,
            'assets_needed': [f"broll-{kw}" for kw in keywords[:3]] if scene_num > 1 and scene_num < len(segments) else ["heygen-avatar"]
        }

        scenes.append(scene)

    return scenes, prev_registers

def check_variety_gate(registers):
    """Check if variety gate is satisfied"""
    unique_registers = len(set(registers))

    # Check for more than 3 consecutive same
    max_consecutive = 1
    current_consecutive = 1
    for i in range(1, len(registers)):
        if registers[i] == registers[i-1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    return {
        'unique_count': unique_registers,
        'max_consecutive': max_consecutive,
        'passes': unique_registers >= 6 and max_consecutive <= 3
    }

def format_markdown(scenes, variety_check):
    """Format as Markdown visual treatment board"""
    lines = []
    lines.append("# Visual Treatment Board")
    lines.append("")
    lines.append("Auto-generated from transcript analysis.")
    lines.append("")
    lines.append("## Variety Gate Check")
    lines.append("")
    lines.append(f"- Unique registers used: {variety_check['unique_count']}")
    lines.append(f"- Max consecutive same: {variety_check['max_consecutive']}")
    lines.append(f"- Status: {'✅ PASSED' if variety_check['passes'] else '⚠️  REVIEW NEEDED'}")
    lines.append("")

    if not variety_check['passes']:
        lines.append("**Recommendation:** Adjust scene registers to ensure ≥6 unique and ≤3 consecutive same.")
        lines.append("")

    lines.append("---")
    lines.append("")

    for scene in scenes:
        lines.append(f"## {scene['title']} ({scene['duration']}s)")
        lines.append("")
        lines.append(f"**VO Summary:** \"{scene['vo_summary']}\"")
        lines.append("")
        lines.append(f"**Keywords:** {', '.join(scene['keywords'])}")
        lines.append("")
        lines.append(f"**Visual Register:** {scene['register']}")
        lines.append("")
        lines.append(f"**Avatar Timing:** {scene['avatar_timing']}")
        lines.append("")
        lines.append(f"**B-roll Plan:**")
        lines.append(f"- {scene['broll_plan']}")
        lines.append("")
        lines.append(f"**Scene Pacing:** {scene['pacing']}")
        lines.append("")
        lines.append(f"**Assets Needed:**")
        for asset in scene['assets_needed']:
            lines.append(f"- `{asset}` (semantic key)")
        lines.append("")
        lines.append("**Approval:** [ ] Pending")
        lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate visual treatment board from transcript")
    parser.add_argument('--transcript', required=True, help="Path to transcript.json")
    parser.add_argument('--brief', required=True, help="Path to episode-brief.md")
    parser.add_argument('--output', required=True, help="Output path for visual-treatment-board.md")

    args = parser.parse_args()

    print("📋 Generating visual treatment board...")
    print(f"   Transcript: {args.transcript}")
    print(f"   Brief: {args.brief}")
    print("")

    # Load inputs
    words = load_transcript(args.transcript)
    preferences = load_brief(args.brief)

    print(f"✓ Loaded transcript: {len(words)} words")
    print("")

    # Segment transcript
    segments = segment_transcript(words, target_scene_duration=25)
    print(f"✓ Segmented into {len(segments)} scenes")
    for i, seg in enumerate(segments):
        print(f"   Scene {i+1:02d}: {seg['duration']}s ({seg['start']:.1f}s → {seg['end']:.1f}s)")
    print("")

    # Generate scene plan
    scenes, registers = generate_scene_plan(segments, preferences)
    print(f"✓ Generated scene plan with visual registers")
    print("")

    # Check variety gate
    variety_check = check_variety_gate(registers)
    print(f"✓ Variety gate check:")
    print(f"   - Unique registers: {variety_check['unique_count']}")
    print(f"   - Max consecutive: {variety_check['max_consecutive']}")
    print(f"   - Status: {'PASSED ✅' if variety_check['passes'] else 'REVIEW NEEDED ⚠️'}")
    print("")

    # Format as Markdown
    markdown = format_markdown(scenes, variety_check)

    # Write output
    with open(args.output, 'w') as f:
        f.write(markdown)

    print(f"✅ Visual treatment board written to: {args.output}")
    print("")
    print("Next steps:")
    print("  1. Review and edit visual-treatment-board.md")
    print("  2. Mark scenes as approved: **Approval:** [x] Approved")
    print("  3. Run: python3 scripts/resolve-assets.py \\")
    print("       --treatment visual-treatment-board.md \\")
    print("       --manifest ../asset-library/MANIFEST.json \\")
    print("       --output asset-resolution-report.md")

if __name__ == '__main__':
    main()
