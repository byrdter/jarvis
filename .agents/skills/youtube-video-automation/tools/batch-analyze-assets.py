#!/usr/bin/env python3
"""
batch-analyze-assets.py — Auto-tag all assets using AI vision analysis

Usage:
    python3 tools/batch-analyze-assets.py --asset-dir /path/to/assets
    python3 tools/batch-analyze-assets.py --asset-dir /path/to/assets --db assets.db
    python3 tools/batch-analyze-assets.py --asset-dir /path/to/assets --limit 10 --dry-run
"""

import anthropic
import json
import argparse
import sqlite3
import subprocess
import base64
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
import time

def extract_video_frame(video_path, timestamp=2.0):
    """Extract a representative frame from video"""
    output = Path(video_path).parent / f"temp_frame_{video_path.stem}.jpg"

    try:
        subprocess.run([
            'ffmpeg', '-i', str(video_path),
            '-ss', str(timestamp),
            '-vframes', '1',
            '-y', str(output),
            '-loglevel', 'error'
        ], check=True, timeout=30)

        if output.exists():
            return output
    except Exception as e:
        print(f"  ⚠️  Frame extraction failed: {e}")

    return None

def get_video_info(video_path):
    """Get video duration and resolution"""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration:stream=width,height',
            '-of', 'json', str(video_path)
        ], capture_output=True, text=True, timeout=10)

        data = json.loads(result.stdout)
        duration = float(data.get('format', {}).get('duration', 0))

        streams = data.get('streams', [])
        if streams:
            width = streams[0].get('width')
            height = streams[0].get('height')
            resolution = f"{width}x{height}" if width and height else None
        else:
            resolution = None

        return {'duration': duration, 'resolution': resolution}
    except Exception as e:
        print(f"  ⚠️  Video info extraction failed: {e}")
        return {'duration': None, 'resolution': None}

def analyze_with_claude(image_path, client):
    """Use Claude to analyze image and generate metadata"""

    # Read image
    with open(image_path, 'rb') as f:
        image_data = base64.standard_b64encode(f.read()).decode('utf-8')

    # Determine media type
    ext = Path(image_path).suffix.lower()
    media_type = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp'
    }.get(ext, 'image/jpeg')

    # Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": """Analyze this asset for video B-roll/production use.

Generate comprehensive, searchable metadata in JSON format:

{
  "description": "Detailed 2-3 sentence description of what's shown",
  "keywords": ["15-25 specific, searchable keywords"],
  "categories": ["3-5 broad categories like 'technology', 'business', 'nature'"],
  "themes": ["abstract themes this could represent, like 'innovation', 'teamwork'"],
  "mood": "mood and tone (e.g., 'energetic, modern, professional')  ",
  "setting": "environment details (indoor/outdoor, lighting, time of day, location type)",
  "people": "description of people if visible, or 'none'",
  "objects": ["all significant objects/elements visible"],
  "actions": ["what's happening in the scene, or 'static'"],
  "color_palette": ["3-5 dominant colors"],
  "use_cases": ["5-8 specific video topics/contexts where this would work well"],
  "quality_notes": "technical quality, composition, suitability for production"
}

Be comprehensive and specific. Use descriptive keywords that someone would search for."""
                }
            ]
        }]
    )

    # Parse JSON from response
    content = response.content[0].text

    # Extract JSON (handle markdown code blocks)
    if '```json' in content:
        json_str = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        json_str = content.split('```')[1].split('```')[0].strip()
    else:
        json_str = content.strip()

    try:
        metadata = json.loads(json_str)
        return metadata
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse error: {e}")
        print(f"  Response: {content[:200]}...")
        return None

def generate_embedding(text, api_key=None):
    """Generate text embedding using OpenAI"""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key) if api_key else OpenAI()

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]  # Token limit
        )

        embedding = response.data[0].embedding
        return np.array(embedding, dtype=np.float32)

    except Exception as e:
        print(f"  ⚠️  Embedding generation failed: {e}")
        return None

def store_asset_metadata(db_path, file_path, metadata, embedding, asset_type, duration=None, resolution=None):
    """Store analyzed asset in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now = datetime.now().isoformat()
    file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0

    # Insert asset
    cursor.execute("""
        INSERT OR REPLACE INTO assets (
            file_path, file_name, type, duration, resolution, file_size,
            description, mood, setting, people, color_palette, quality_notes,
            added_at, tagged_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(file_path),
        Path(file_path).name,
        asset_type,
        duration,
        resolution,
        file_size,
        metadata.get('description', ''),
        metadata.get('mood', ''),
        metadata.get('setting', ''),
        metadata.get('people', ''),
        json.dumps(metadata.get('color_palette', [])),
        metadata.get('quality_notes', ''),
        now,
        now
    ))

    asset_id = cursor.lastrowid

    # Insert keywords
    for keyword in metadata.get('keywords', []):
        cursor.execute("""
            INSERT INTO keywords (asset_id, keyword, source)
            VALUES (?, ?, ?)
        """, (asset_id, keyword.lower(), 'ai'))

    # Insert categories
    for category in metadata.get('categories', []):
        cursor.execute("""
            INSERT INTO categories (asset_id, category, type)
            VALUES (?, ?, ?)
        """, (asset_id, category.lower(), 'category'))

    for theme in metadata.get('themes', []):
        cursor.execute("""
            INSERT INTO categories (asset_id, category, type)
            VALUES (?, ?, ?)
        """, (asset_id, theme.lower(), 'theme'))

    for obj in metadata.get('objects', []):
        cursor.execute("""
            INSERT INTO categories (asset_id, category, type)
            VALUES (?, ?, ?)
        """, (asset_id, obj.lower(), 'object'))

    for action in metadata.get('actions', []):
        cursor.execute("""
            INSERT INTO categories (asset_id, category, type)
            VALUES (?, ?, ?)
        """, (asset_id, action.lower(), 'action'))

    for use_case in metadata.get('use_cases', []):
        cursor.execute("""
            INSERT INTO categories (asset_id, category, type)
            VALUES (?, ?, ?)
        """, (asset_id, use_case.lower(), 'use_case'))

    # Store embedding
    if embedding is not None:
        cursor.execute("""
            INSERT OR REPLACE INTO embeddings (asset_id, embedding, model, dimensions)
            VALUES (?, ?, ?, ?)
        """, (asset_id, pickle.dumps(embedding), 'text-embedding-3-small', len(embedding)))

    # Cache full AI metadata
    cursor.execute("""
        INSERT OR REPLACE INTO metadata_cache (asset_id, ai_metadata, model_used, analyzed_at)
        VALUES (?, ?, ?, ?)
    """, (asset_id, json.dumps(metadata), 'claude-sonnet-4-6', now))

    conn.commit()
    conn.close()

    return asset_id

def process_asset(file_path, claude_client, db_path, dry_run=False):
    """Process a single asset (image or video)"""

    file_path = Path(file_path)

    # Determine type
    ext = file_path.suffix.lower()
    is_video = ext in ['.mp4', '.mov', '.avi', '.webm', '.mkv']
    is_image = ext in ['.jpg', '.jpeg', '.png', '.webp']

    if not (is_video or is_image):
        return None

    asset_type = 'video' if is_video else 'image'

    print(f"\n  📄 {file_path.name}")

    # For videos, extract frame and get info
    if is_video:
        video_info = get_video_info(file_path)
        duration = video_info.get('duration')
        resolution = video_info.get('resolution')

        print(f"     Type: video ({duration:.1f}s, {resolution})")

        # Extract frame
        frame_path = extract_video_frame(file_path, timestamp=min(2.0, duration/2 if duration else 2.0))
        if not frame_path:
            print("     ❌ Failed to extract frame")
            return None

        analyze_path = frame_path
    else:
        duration = None
        resolution = None
        analyze_path = file_path
        print(f"     Type: image")

    if dry_run:
        print("     🔍 [DRY RUN] Would analyze with Claude")
        if is_video and frame_path:
            frame_path.unlink()
        return None

    # Analyze with Claude
    print("     🔍 Analyzing with Claude...")
    try:
        metadata = analyze_with_claude(analyze_path, claude_client)
        if not metadata:
            print("     ❌ Analysis failed")
            if is_video and frame_path:
                frame_path.unlink()
            return None
    except Exception as e:
        print(f"     ❌ Analysis error: {e}")
        if is_video and frame_path:
            frame_path.unlink()
        return None

    # Generate embedding
    print("     🧬 Generating embedding...")
    embedding_text = f"{metadata.get('description', '')} {' '.join(metadata.get('keywords', []))}"
    embedding = generate_embedding(embedding_text)

    # Store in database
    print("     💾 Storing in database...")
    asset_id = store_asset_metadata(
        db_path, file_path, metadata, embedding, asset_type, duration, resolution
    )

    print(f"     ✅ Stored (ID: {asset_id})")
    print(f"     Keywords: {', '.join(metadata.get('keywords', [])[:8])}...")

    # Clean up temp frame
    if is_video and frame_path and frame_path.exists():
        frame_path.unlink()

    return asset_id

def find_assets(asset_dir):
    """Recursively find all image and video assets"""
    asset_dir = Path(asset_dir)

    extensions = ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov', '.avi', '.webm', '.mkv']
    assets = []

    for ext in extensions:
        assets.extend(asset_dir.glob(f'**/*{ext}'))
        assets.extend(asset_dir.glob(f'**/*{ext.upper()}'))

    return sorted(set(assets))

def main():
    parser = argparse.ArgumentParser(description="Batch analyze assets with AI")
    parser.add_argument('--asset-dir', required=True, help="Directory containing assets")
    parser.add_argument('--db', default='assets.db', help="Database file path")
    parser.add_argument('--limit', type=int, help="Limit number of assets to process")
    parser.add_argument('--dry-run', action='store_true', help="Don't actually analyze, just list")
    parser.add_argument('--skip-existing', action='store_true', help="Skip assets already in DB")

    args = parser.parse_args()

    asset_dir = Path(args.asset_dir)
    if not asset_dir.exists():
        print(f"❌ Asset directory not found: {asset_dir}")
        return

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print(f"   Run: python3 tools/init-asset-db.py --db-path {db_path}")
        return

    # Find all assets
    print(f"🔍 Scanning for assets in {asset_dir}...")
    assets = find_assets(asset_dir)

    print(f"   Found {len(assets)} assets")

    if args.limit:
        assets = assets[:args.limit]
        print(f"   Limited to {len(assets)} assets")

    if args.dry_run:
        print("\n📋 DRY RUN - Would process:")
        for asset in assets:
            print(f"   - {asset.relative_to(asset_dir)}")
        return

    # Initialize Claude client
    claude_client = anthropic.Anthropic()

    # Process each asset
    print(f"\n🚀 Processing {len(assets)} assets...\n")

    processed = 0
    skipped = 0
    failed = 0

    start_time = time.time()

    for i, asset in enumerate(assets, 1):
        print(f"[{i}/{len(assets)}]", end='')

        # Check if already processed
        if args.skip_existing:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM assets WHERE file_path = ?", (str(asset),))
            if cursor.fetchone():
                print(f" ⏭️  {asset.name} (already in DB)")
                conn.close()
                skipped += 1
                continue
            conn.close()

        try:
            asset_id = process_asset(asset, claude_client, db_path, dry_run=args.dry_run)
            if asset_id:
                processed += 1
            else:
                failed += 1

            # Rate limiting - be nice to API
            time.sleep(1)

        except Exception as e:
            print(f"     ❌ Error: {e}")
            failed += 1

    elapsed = time.time() - start_time

    print(f"\n" + "="*60)
    print(f"✅ Batch analysis complete!")
    print(f"   Processed: {processed}")
    print(f"   Skipped: {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Time: {elapsed/60:.1f} minutes")
    print(f"   Database: {db_path}")
    print("="*60)

    print("\nNext steps:")
    print(f"  python3 tools/search-assets-db.py 'office productivity' --db {db_path}")

if __name__ == '__main__':
    main()
