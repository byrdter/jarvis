#!/usr/bin/env python3
"""Quick script to insert manually analyzed metadata into database"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

def insert_asset(db_path, file_path, metadata):
    """Insert asset metadata into database"""
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
        'image',
        None,
        None,
        file_size,
        metadata.get('description', ''),
        metadata.get('mood', ''),
        metadata.get('setting', ''),
        metadata.get('people', ''),
        json.dumps(metadata.get('color_palette', [])),
        metadata.get('quality_notes', 'Analyzed by Claude in conversation'),
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

    # Cache metadata
    cursor.execute("""
        INSERT OR REPLACE INTO metadata_cache (asset_id, ai_metadata, model_used, analyzed_at)
        VALUES (?, ?, ?, ?)
    """, (asset_id, json.dumps(metadata), 'claude-sonnet-4-20250514', now))

    conn.commit()
    conn.close()

    return asset_id

if __name__ == '__main__':
    import sys

    # Read JSON from stdin
    data = json.load(sys.stdin)

    db_path = data['db_path']
    assets = data['assets']

    for asset in assets:
        asset_id = insert_asset(db_path, asset['file_path'], asset['metadata'])
        print(f"✓ Inserted {Path(asset['file_path']).name} (ID: {asset_id})")
