#!/usr/bin/env python3
"""
generate-embeddings.py — Generate embeddings for all assets in database

Usage:
    python3 tools/generate-embeddings.py --db assets.db
    python3 tools/generate-embeddings.py --db assets.db --force  # Regenerate all
"""

import sqlite3
import numpy as np
import pickle
import argparse
from pathlib import Path
import time
import os

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

def get_assets_without_embeddings(db_path, force=False):
    """Get all assets that need embeddings"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if force:
        # Get all assets
        cursor.execute("SELECT id, description FROM assets")
    else:
        # Only get assets without embeddings
        cursor.execute("""
            SELECT a.id, a.description
            FROM assets a
            LEFT JOIN embeddings e ON a.id = e.asset_id
            WHERE e.asset_id IS NULL
        """)

    assets = cursor.fetchall()
    conn.close()

    return assets

def get_asset_keywords(db_path, asset_id):
    """Get all keywords for an asset"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT keyword FROM keywords WHERE asset_id = ?", (asset_id,))
    keywords = [row[0] for row in cursor.fetchall()]

    conn.close()
    return keywords

def store_embedding(db_path, asset_id, embedding):
    """Store embedding in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO embeddings (asset_id, embedding, model, dimensions)
        VALUES (?, ?, ?, ?)
    """, (asset_id, pickle.dumps(embedding), 'text-embedding-3-small', len(embedding)))

    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for assets")
    parser.add_argument('--db', default='assets.db', help="Database path")
    parser.add_argument('--force', action='store_true', help="Regenerate all embeddings")
    parser.add_argument('--api-key', help="OpenAI API key (or set OPENAI_API_KEY env var)")

    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found")
        print("   Set OPENAI_API_KEY environment variable or use --api-key")
        return

    # Get assets needing embeddings
    print(f"🔍 Scanning database for assets...")
    assets = get_assets_without_embeddings(db_path, force=args.force)

    if not assets:
        print("✅ All assets already have embeddings!")
        return

    print(f"   Found {len(assets)} assets needing embeddings\n")

    # Generate embeddings
    print(f"🚀 Generating embeddings...\n")

    processed = 0
    failed = 0
    start_time = time.time()

    for i, (asset_id, description) in enumerate(assets, 1):
        print(f"[{i}/{len(assets)}] Asset ID {asset_id}")

        # Get keywords
        keywords = get_asset_keywords(db_path, asset_id)

        # Create text for embedding
        text = f"{description} {' '.join(keywords)}"

        # Generate embedding
        embedding = generate_embedding(text, api_key=api_key)

        if embedding is not None:
            # Store in database
            store_embedding(db_path, asset_id, embedding)
            print(f"     ✅ Embedding generated ({len(embedding)} dimensions)")
            processed += 1
        else:
            print(f"     ❌ Failed")
            failed += 1

        # Rate limiting - be nice to API
        time.sleep(0.1)

    elapsed = time.time() - start_time

    print(f"\n" + "="*60)
    print(f"✅ Embedding generation complete!")
    print(f"   Processed: {processed}")
    print(f"   Failed: {failed}")
    print(f"   Time: {elapsed:.1f} seconds")
    print(f"   Database: {db_path}")
    print("="*60)

    if processed > 0:
        print("\n🎯 Semantic search is now ready!")
        print(f"   python3 tools/search-assets-db.py 'person working late at night' --db {db_path}")

if __name__ == '__main__':
    main()
