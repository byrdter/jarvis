#!/usr/bin/env python3
"""
build-hyperframes-scenes.py — Generate HyperFrames HTML compositions from visual treatment

Usage:
    python3 build-hyperframes-scenes.py \\
        --treatment visual-treatment-board.md \\
        --transcript assets/transcript.json \\
        --design DESIGN.md \\
        --output-dir scenes/
"""

import json
import argparse
import re
import shutil
from pathlib import Path

def parse_treatment_board(path):
    """Parse visual treatment board"""
    with open(path, 'r') as f:
        content = f.read()

    scenes = []
    current_scene = None

    for line in content.split('\n'):
        if line.startswith('## Scene'):
            if current_scene:
                scenes.append(current_scene)
            match = re.match(r'## (Scene \d+)(.*?) \(([\d.]+)s\)', line)
            if match:
                scene_num = match.group(1).replace('Scene ', '').strip()
                title = match.group(2).strip().lstrip(':').strip()
                current_scene = {
                    'number': int(scene_num),
                    'title': title or f"Scene {scene_num}",
                    'slug': f"{scene_num.zfill(2)}-{title.lower().replace(' ', '-')}" if title else f"{scene_num.zfill(2)}-scene",
                    'duration': float(match.group(3)),
                    'keywords': [],
                    'register': '',
                    'avatar_timing': '',
                    'broll_plan': ''
                }

        elif current_scene:
            if line.startswith('**Keywords:**'):
                keywords = line.replace('**Keywords:**', '').strip()
                current_scene['keywords'] = [k.strip() for k in keywords.split(',')]

            elif line.startswith('**Visual Register:**'):
                current_scene['register'] = line.replace('**Visual Register:**', '').strip()

            elif line.startswith('**Avatar Timing:**'):
                current_scene['avatar_timing'] = line.replace('**Avatar Timing:**', '').strip()

            elif line.startswith('**B-roll Plan:**'):
                # Next line(s) contain the plan
                pass

            elif line.startswith('- ') and current_scene.get('register'):
                # B-roll plan line
                if not current_scene['broll_plan']:
                    current_scene['broll_plan'] = line.strip('- ')
                else:
                    current_scene['broll_plan'] += '\\n' + line.strip('- ')

    if current_scene:
        scenes.append(current_scene)

    return scenes

def load_transcript(path):
    """Load transcript with word-level timestamps"""
    with open(path, 'r') as f:
        data = json.load(f)
    return data.get('words', [])

def parse_design(path):
    """Extract colors and fonts from DESIGN.md"""
    if not Path(path).exists():
        # Return defaults
        return {
            'bg_color': '#050505',
            'text_color': '#ffffff',
            'accent_color': '#FFD700',
            'font_family': 'Inter, system-ui, sans-serif'
        }

    with open(path, 'r') as f:
        content = f.read()

    design = {}

    # Extract colors (simple regex-based extraction)
    color_matches = re.findall(r'#[0-9A-Fa-f]{6}', content)
    if color_matches:
        design['bg_color'] = color_matches[0] if len(color_matches) > 0 else '#050505'
        design['accent_color'] = color_matches[1] if len(color_matches) > 1 else '#FFD700'
        design['text_color'] = '#ffffff'

    # Extract fonts
    font_match = re.search(r'font[- ]family:\s*([^;\n]+)', content, re.IGNORECASE)
    if font_match:
        design['font_family'] = font_match.group(1).strip()
    else:
        design['font_family'] = 'Inter, system-ui, sans-serif'

    return design

def get_scene_words(all_words, scene_start, scene_end):
    """Extract words for this scene's time range"""
    scene_words = []
    for word in all_words:
        word_start = word.get('start', 0)
        if scene_start <= word_start <= scene_end:
            # Adjust timestamp to be relative to scene start
            word_copy = word.copy()
            word_copy['start'] = word_start - scene_start
            word_copy['end'] = word.get('end', 0) - scene_start
            scene_words.append(word_copy)
    return scene_words

def generate_html_composition(scene, design, scene_words):
    """Generate HyperFrames HTML composition for scene"""

    # Determine if avatar or B-roll scene
    is_avatar_scene = 'avatar' in scene['avatar_timing'].lower() or scene['number'] == 1

    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{scene['slug']}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      background: {design['bg_color']};
      color: {design['text_color']};
      font-family: {design['font_family']};
      overflow: hidden;
    }}

    [data-composition-id] {{
      position: relative;
      width: 100%;
      height: 100%;
      background: {design['bg_color']};
    }}

    .scene-content {{
      width: 100%;
      height: 100%;
      padding: 120px 160px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 32px;
    }}

    .title {{
      font-size: 96px;
      font-weight: 800;
      color: {design['text_color']};
      line-height: 1.1;
    }}

    .subtitle {{
      font-size: 42px;
      font-weight: 400;
      color: rgba(255, 255, 255, 0.7);
      line-height: 1.3;
    }}

    .lower-third {{
      position: absolute;
      bottom: 80px;
      left: 80px;
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 20px 32px;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(10px);
      border-radius: 8px;
    }}

    .lower-third .logo {{
      width: 48px;
      height: 48px;
    }}

    .lower-third .channel-name {{
      font-size: 24px;
      font-weight: 600;
      color: {design['text_color']};
    }}

    video {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
  </style>
</head>
<body>
  <div data-composition-id="{scene['slug']}" data-width="1920" data-height="1080">
'''

    if is_avatar_scene:
        # Avatar scene
        html += f'''    <!-- Avatar video -->
    <video id="avatar"
           data-start="0"
           data-duration="{scene['duration']}"
           data-track-index="0"
           src="assets/heygen-segment.mp4"
           muted
           playsinline></video>

    <!-- Audio (same source, not muted) -->
    <audio id="vo"
           data-start="0"
           data-duration="{scene['duration']}"
           data-track-index="2"
           src="assets/heygen-segment.mp4"></audio>

    <!-- Lower-third branding -->
    <div class="lower-third">
      <div class="channel-name">Byrddynasty - Understanding AI</div>
    </div>
'''
    else:
        # B-roll scene
        html += f'''    <!-- Background content -->
    <div class="scene-content">
      <div class="title">Scene Title</div>
      <div class="subtitle">Subtitle or key point from VO</div>
    </div>

    <!-- Audio (VO from HeyGen, extracted per-scene) -->
    <audio id="vo"
           data-start="0"
           data-duration="{scene['duration']}"
           data-track-index="2"
           src="assets/vo-segment.mp3"></audio>
'''

    html += f'''  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    // Register timeline
    window.__timelines = window.__timelines || {{}};

    const tl = gsap.timeline({{ paused: true }});

    // TODO: Add VO-anchored animations based on transcript timestamps
    // Example (replace with actual word timestamps):
    // tl.from(".title", {{ y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }}, 0.5);
    // tl.from(".subtitle", {{ y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }}, 1.0);

'''

    # Add sample animations based on scene words
    if len(scene_words) > 5:
        # Example: Fade in title at first word
        first_word_time = scene_words[0].get('start', 0)
        html += f'''    // Fade in title when VO starts
    tl.from(".title", {{ y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }}, {first_word_time:.2f});

'''

        # Example: Fade in subtitle at ~3rd word
        if len(scene_words) > 3:
            third_word_time = scene_words[2].get('start', 0)
            html += f'''    // Fade in subtitle
    tl.from(".subtitle", {{ y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }}, {third_word_time:.2f});

'''

    if is_avatar_scene:
        html += f'''    // Fade in lower-third
    tl.from(".lower-third", {{ y: 20, opacity: 0, duration: 0.4, ease: "power2.out" }}, 2.0);

    // Fade out before scene end
    const sceneEnd = {scene['duration']};
    tl.to(".lower-third", {{ y: -20, opacity: 0, duration: 0.3, ease: "power2.in" }}, sceneEnd - 1.5);
'''

    html += f'''
    // Register timeline
    window.__timelines["{scene['slug']}"] = tl;
  </script>
</body>
</html>'''

    return html

def generate_hyperframes_json(scene):
    """Generate hyperframes.json for scene"""
    return {
        "name": f"video-scene-{scene['slug']}",
        "version": "0.1.0",
        "compositions": [
            {
                "id": scene['slug'],
                "file": "index.html",
                "width": 1920,
                "height": 1080,
                "duration": scene['duration']
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="Generate HyperFrames scenes from visual treatment")
    parser.add_argument('--treatment', required=True, help="Path to visual-treatment-board.md")
    parser.add_argument('--transcript', required=True, help="Path to transcript.json")
    parser.add_argument('--design', required=True, help="Path to DESIGN.md")
    parser.add_argument('--output-dir', required=True, help="Output directory for scenes/")

    args = parser.parse_args()

    print("🎬 Building HyperFrames scenes...")
    print(f"   Treatment: {args.treatment}")
    print(f"   Transcript: {args.transcript}")
    print(f"   Design: {args.design}")
    print(f"   Output: {args.output_dir}")
    print("")

    # Parse inputs
    scenes = parse_treatment_board(args.treatment)
    all_words = load_transcript(args.transcript)
    design = parse_design(args.design)

    print(f"✓ Parsed {len(scenes)} scenes from treatment board")
    print(f"✓ Loaded {len(all_words)} words from transcript")
    print(f"✓ Loaded design (colors: {design.get('accent_color', 'N/A')})")
    print("")

    # Create output directory
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Calculate cumulative scene start times
    cumulative_time = 0
    for scene in scenes:
        scene['start_time'] = cumulative_time
        scene['end_time'] = cumulative_time + scene['duration']
        cumulative_time += scene['duration']

    # Generate each scene
    for scene in scenes:
        scene_dir = output_path / scene['slug']
        scene_dir.mkdir(exist_ok=True)

        # Create assets directory
        assets_dir = scene_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)

        # Get words for this scene
        scene_words = get_scene_words(all_words, scene['start_time'], scene['end_time'])

        # Generate HTML
        html = generate_html_composition(scene, design, scene_words)

        # Write index.html
        with open(scene_dir / 'index.html', 'w') as f:
            f.write(html)

        # Generate hyperframes.json
        hf_json = generate_hyperframes_json(scene)
        with open(scene_dir / 'hyperframes.json', 'w') as f:
            json.dump(hf_json, f, indent=2)

        print(f"✓ Generated {scene['slug']} ({scene['duration']}s)")
        print(f"   - index.html")
        print(f"   - hyperframes.json")
        print(f"   - assets/ (ready for asset copies)")

    print("")
    print(f"✅ Generated {len(scenes)} HyperFrames scenes in {args.output_dir}")
    print("")
    print("⚠️  **Important:** These are skeleton scenes. You must:")
    print("")
    print("1. **Add actual animations** - Replace TODO comments with real GSAP timelines")
    print("2. **Copy assets** - Copy resolved assets to each scene's assets/ folder")
    print("3. **Customize HTML** - Adjust content, layout, and styles per scene")
    print("4. **Lint scenes** - Run `npx hyperframes lint` in each scene directory")
    print("")
    print("Next steps:")
    print("  cd", args.output_dir / scenes[0]['slug'])
    print("  npx hyperframes lint")
    print("  npx hyperframes preview")

if __name__ == '__main__':
    main()
