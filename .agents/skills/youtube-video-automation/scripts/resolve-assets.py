#!/usr/bin/env python3
"""
resolve-assets.py — Resolve semantic keys to actual asset files

Usage:
    python3 resolve-assets.py \\
        --treatment visual-treatment-board.md \\
        --manifest ../asset-library/MANIFEST.json \\
        --output asset-resolution-report.md
"""

import json
import argparse
import re
from pathlib import Path

def parse_treatment_board(path):
    """Extract asset semantic keys from visual treatment board"""
    with open(path, 'r') as f:
        content = f.read()

    scenes = []
    current_scene = None

    for line in content.split('\n'):
        # Scene header
        if line.startswith('## Scene'):
            if current_scene:
                scenes.append(current_scene)
            match = re.match(r'## (Scene \d+.*?) \(([\d.]+)s\)', line)
            if match:
                current_scene = {
                    'title': match.group(1),
                    'duration': float(match.group(2)),
                    'keywords': [],
                    'assets_needed': []
                }

        # Keywords
        elif line.startswith('**Keywords:**') and current_scene:
            keywords = line.replace('**Keywords:**', '').strip()
            current_scene['keywords'] = [k.strip() for k in keywords.split(',')]

        # Assets needed
        elif line.startswith('- `') and '(semantic key)' in line and current_scene:
            asset = line.split('`')[1]
            current_scene['assets_needed'].append(asset)

    if current_scene:
        scenes.append(current_scene)

    return scenes

def load_manifest(path):
    """Load asset manifest"""
    manifest_path = Path(path)
    if not manifest_path.exists():
        print(f"⚠️  Warning: Manifest not found at {path}")
        return None

    with open(path, 'r') as f:
        return json.load(f)

def keyword_match_score(query_keywords, asset_keywords, asset_description=""):
    """
    Calculate match score between query keywords and asset metadata.
    Returns score 0-1.
    """
    query_set = set([k.lower() for k in query_keywords])
    asset_set = set([k.lower() for k in asset_keywords])

    # Add words from description
    if asset_description:
        desc_words = asset_description.lower().split()
        asset_set.update(desc_words)

    # Calculate overlap
    matches = len(query_set & asset_set)
    total = len(query_set)

    return matches / total if total > 0 else 0.0

def search_assets(manifest, query_keywords, asset_type=None, min_duration=None):
    """
    Search manifest for assets matching keywords.
    Returns list of (asset, score) tuples sorted by score.
    """
    if not manifest:
        return []

    results = []

    # Search B-roll
    for asset in manifest.get('broll', []):
        if asset_type and asset.get('type') != asset_type:
            continue
        if min_duration and asset.get('duration', 0) < min_duration:
            continue

        score = keyword_match_score(
            query_keywords,
            asset.get('keywords', []),
            asset.get('description', '')
        )

        if score >= 0.3:  # Threshold
            results.append((asset, score))

    # Search screenshots
    for key, asset in manifest.get('screenshots', {}).items():
        if asset_type and asset_type != 'image':
            continue

        score = keyword_match_score(
            query_keywords,
            asset.get('keywords', []),
            asset.get('description', '')
        )

        if score >= 0.3:
            # Add ID for screenshots
            asset_copy = asset.copy()
            asset_copy['id'] = key
            results.append((asset_copy, score))

    # Search web rolls
    for asset in manifest.get('web_rolls', []):
        if asset_type and asset.get('type') != asset_type:
            continue

        score = keyword_match_score(
            query_keywords,
            asset.get('keywords', []),
            asset.get('description', '')
        )

        if score >= 0.3:
            results.append((asset, score))

    # Search generated
    for asset in manifest.get('generated', []):
        if asset_type and asset.get('type') != asset_type:
            continue

        score = keyword_match_score(
            query_keywords,
            asset.get('keywords', []),
            asset.get('description', '')
        )

        if score >= 0.3:
            results.append((asset, score))

    # Sort by score descending
    return sorted(results, key=lambda x: x[1], reverse=True)

def resolve_all_assets(scenes, manifest):
    """Resolve all assets from scenes"""
    resolved = []
    missing = []

    for scene in scenes:
        for asset_key in scene['assets_needed']:
            # Try exact match first
            if manifest:
                # Check if asset_key matches any ID directly
                found = False

                # Check broll
                for asset in manifest.get('broll', []):
                    if asset.get('id') == asset_key:
                        resolved.append({
                            'semantic_key': asset_key,
                            'scene': scene['title'],
                            'asset': asset,
                            'score': 1.0,
                            'match_type': 'exact'
                        })
                        found = True
                        break

                # Check screenshots
                if not found and asset_key in manifest.get('screenshots', {}):
                    asset = manifest['screenshots'][asset_key]
                    asset_copy = asset.copy()
                    asset_copy['id'] = asset_key
                    resolved.append({
                        'semantic_key': asset_key,
                        'scene': scene['title'],
                        'asset': asset_copy,
                        'score': 1.0,
                        'match_type': 'exact'
                    })
                    found = True

                # If no exact match, try keyword search
                if not found:
                    # Use scene keywords for search
                    results = search_assets(manifest, scene['keywords'])

                    if results:
                        best_asset, best_score = results[0]
                        resolved.append({
                            'semantic_key': asset_key,
                            'scene': scene['title'],
                            'asset': best_asset,
                            'score': best_score,
                            'match_type': 'keyword'
                        })
                        found = True

                if not found:
                    missing.append({
                        'semantic_key': asset_key,
                        'scene': scene['title'],
                        'keywords': scene['keywords']
                    })
            else:
                missing.append({
                    'semantic_key': asset_key,
                    'scene': scene['title'],
                    'keywords': scene['keywords']
                })

    return resolved, missing

def format_report(resolved, missing, scenes):
    """Format asset resolution report as Markdown"""
    lines = []
    lines.append("# Asset Resolution Report")
    lines.append("")
    lines.append(f"**Resolved:** {len(resolved)} assets")
    lines.append(f"**Missing:** {len(missing)} assets")
    lines.append("")

    if resolved:
        lines.append("## Resolved Assets")
        lines.append("")
        lines.append("| Semantic Key | Scene | Resolved Path | Match Score | Type |")
        lines.append("|--------------|-------|---------------|-------------|------|")

        for item in resolved:
            asset = item['asset']
            path = asset.get('path', 'N/A')
            score = item['score']
            match_type = item['match_type']

            lines.append(f"| `{item['semantic_key']}` | {item['scene']} | {path} | {score:.2f} | {match_type} |")

        lines.append("")

    if missing:
        lines.append("## Missing Assets")
        lines.append("")
        lines.append("| Semantic Key | Scene | Suggested Keywords | Recommended Action |")
        lines.append("|--------------|-------|-------------------|-------------------|")

        for item in missing:
            keywords = ', '.join(item['keywords'][:5])
            action = "Generate with Runway/Higgsfield OR find alternative"

            lines.append(f"| `{item['semantic_key']}` | {item['scene']} | {keywords} | {action} |")

        lines.append("")
        lines.append("### Recommendations")
        lines.append("")
        lines.append("1. **Review alternatives:** Check if similar assets exist with different keywords")
        lines.append("2. **Generate new assets:** Use Runway/Higgsfield for missing B-roll")
        lines.append("3. **Update MANIFEST.json:** Add new assets to catalog after creation")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    if missing:
        lines.append("⚠️  **Blockers:** Resolve missing assets before proceeding.")
        lines.append("")
        lines.append("Options:")
        lines.append("1. Edit `visual-treatment-board.md` to use alternative semantic keys")
        lines.append("2. Generate missing assets with Runway/Higgsfield")
        lines.append("3. Simplify scenes to use only available assets")
        lines.append("")
        lines.append("After resolving, re-run this script to verify 100% coverage.")
    else:
        lines.append("✅ All assets resolved! Ready to build HyperFrames scenes.")
        lines.append("")
        lines.append("Run:")
        lines.append("```bash")
        lines.append("python3 scripts/build-hyperframes-scenes.py \\")
        lines.append("  --treatment visual-treatment-board.md \\")
        lines.append("  --transcript assets/transcript.json \\")
        lines.append("  --design DESIGN.md \\")
        lines.append("  --output-dir scenes/")
        lines.append("```")

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="Resolve asset semantic keys to files")
    parser.add_argument('--treatment', required=True, help="Path to visual-treatment-board.md")
    parser.add_argument('--manifest', required=True, help="Path to asset MANIFEST.json")
    parser.add_argument('--output', required=True, help="Output path for resolution report")

    args = parser.parse_args()

    print("🔍 Resolving asset semantic keys...")
    print(f"   Treatment: {args.treatment}")
    print(f"   Manifest: {args.manifest}")
    print("")

    # Parse treatment board
    scenes = parse_treatment_board(args.treatment)
    print(f"✓ Parsed {len(scenes)} scenes from treatment board")

    # Count total assets needed
    total_assets = sum(len(scene['assets_needed']) for scene in scenes)
    print(f"   Total assets needed: {total_assets}")
    print("")

    # Load manifest
    manifest = load_manifest(args.manifest)
    if manifest:
        broll_count = len(manifest.get('broll', []))
        screenshot_count = len(manifest.get('screenshots', {}))
        print(f"✓ Loaded manifest:")
        print(f"   - B-roll: {broll_count}")
        print(f"   - Screenshots: {screenshot_count}")
        print("")

    # Resolve assets
    resolved, missing = resolve_all_assets(scenes, manifest)

    print(f"📊 Resolution results:")
    print(f"   Resolved: {len(resolved)}/{total_assets} ({len(resolved)/total_assets*100:.0f}%)")
    print(f"   Missing: {len(missing)}/{total_assets}")
    print("")

    if missing:
        print("⚠️  Missing assets:")
        for item in missing:
            print(f"   - {item['semantic_key']} (scene: {item['scene']})")
        print("")

    # Format report
    report = format_report(resolved, missing, scenes)

    # Write output
    with open(args.output, 'w') as f:
        f.write(report)

    print(f"✅ Asset resolution report written to: {args.output}")

    if missing:
        print("")
        print("⚠️  **Action required:** Resolve missing assets before proceeding.")
        exit(1)
    else:
        print("")
        print("✅ All assets resolved! Ready for scene generation.")

if __name__ == '__main__':
    main()
