#!/usr/bin/env python3
"""
search-assets-db.py — Search asset database with hybrid semantic + keyword search

Usage:
    python3 tools/search-assets-db.py "office workers using AI"
    python3 tools/search-assets-db.py "office" --type video --min-duration 10
    python3 tools/search-assets-db.py "productivity" --top 5 --json
"""

import sqlite3
import numpy as np
import pickle
import json
import argparse
from pathlib import Path

def generate_query_embedding(query):
    """Generate embedding for search query"""
    try:
        from openai import OpenAI
        client = OpenAI()

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query[:8000]
        )

        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        print(f"⚠️  Embedding generation failed: {e}")
        return None

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_assets(db_path, query, asset_type=None, min_duration=None, top_n=10):
    """
    Hybrid search: semantic similarity (70%) + keyword matching (30%)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Build SQL filter
    filters = []
    params = []

    if asset_type:
        filters.append("a.type = ?")
        params.append(asset_type)

    if min_duration:
        filters.append("a.duration >= ?")
        params.append(min_duration)

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    # Get all assets with embeddings
    cursor.execute(f"""
        SELECT
            a.id, a.file_path, a.file_name, a.type, a.duration, a.resolution,
            a.description, a.mood, a.setting, a.quality_notes,
            e.embedding
        FROM assets a
        JOIN embeddings e ON a.id = e.asset_id
        {where_clause}
    """, params)

    results = []

    for row in cursor.fetchall():
        (asset_id, file_path, file_name, atype, duration, resolution,
         description, mood, setting, quality_notes, embedding_blob) = row

        # Deserialize embedding
        asset_embedding = pickle.loads(embedding_blob)

        # Calculate semantic similarity
        if query_embedding is not None:
            semantic_score = float(cosine_similarity(query_embedding, asset_embedding))
        else:
            semantic_score = 0.0

        # Keyword matching score
        query_words = set(query.lower().split())

        # Get asset keywords
        cursor.execute("""
            SELECT keyword FROM keywords WHERE asset_id = ?
        """, (asset_id,))

        asset_keywords = set(row[0] for row in cursor.fetchall())

        # Count matches
        keyword_matches = len(query_words & asset_keywords)
        keyword_score = min(keyword_matches / len(query_words), 1.0) if query_words else 0.0

        # Combined score (70% semantic, 30% keyword)
        combined_score = (0.7 * semantic_score) + (0.3 * keyword_score)

        # Get categories/themes
        cursor.execute("""
            SELECT category, type FROM categories WHERE asset_id = ?
        """, (asset_id,))

        categories_data = cursor.fetchall()
        categories = [c[0] for c in categories_data if c[1] == 'category']
        themes = [c[0] for c in categories_data if c[1] == 'theme']
        use_cases = [c[0] for c in categories_data if c[1] == 'use_case']

        # Get keywords as list
        keywords = list(asset_keywords)[:15]  # Limit for display

        results.append({
            'id': asset_id,
            'file_path': file_path,
            'file_name': file_name,
            'type': atype,
            'duration': duration,
            'resolution': resolution,
            'description': description,
            'mood': mood,
            'setting': setting,
            'quality_notes': quality_notes,
            'keywords': keywords,
            'categories': categories,
            'themes': themes,
            'use_cases': use_cases,
            'semantic_score': round(semantic_score, 3),
            'keyword_score': round(keyword_score, 3),
            'combined_score': round(combined_score, 3)
        })

    # Sort by combined score
    results.sort(key=lambda x: x['combined_score'], reverse=True)

    conn.close()

    return results[:top_n]

def format_results(results, output_json=False):
    """Format search results"""
    if output_json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No results found.")
        return

    print(f"\n🔍 Found {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['file_name']} (score: {result['combined_score']:.3f})")
        print(f"   Type: {result['type']}", end='')

        if result['duration']:
            print(f" | Duration: {result['duration']:.1f}s", end='')

        if result['resolution']:
            print(f" | Resolution: {result['resolution']}", end='')

        print()

        print(f"   Description: {result['description'][:120]}...")
        print(f"   Keywords: {', '.join(result['keywords'][:8])}")

        if result['use_cases']:
            print(f"   Use cases: {', '.join(result['use_cases'][:3])}")

        print(f"   Scores: semantic={result['semantic_score']:.3f}, keyword={result['keyword_score']:.3f}")
        print(f"   Path: {result['file_path']}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Search asset database")
    parser.add_argument('query', help="Search query")
    parser.add_argument('--db', default='assets.db', help="Database path")
    parser.add_argument('--type', choices=['image', 'video'], help="Filter by asset type")
    parser.add_argument('--min-duration', type=float, help="Minimum duration (seconds, video only)")
    parser.add_argument('--top', type=int, default=10, help="Number of results to return")
    parser.add_argument('--json', action='store_true', help="Output JSON format")

    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print(f"   Run: python3 tools/init-asset-db.py --db-path {db_path}")
        return

    results = search_assets(
        db_path=db_path,
        query=args.query,
        asset_type=args.type,
        min_duration=args.min_duration,
        top_n=args.top
    )

    format_results(results, output_json=args.json)

if __name__ == '__main__':
    main()
