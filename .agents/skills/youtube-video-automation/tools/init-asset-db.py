#!/usr/bin/env python3
"""
init-asset-db.py — Initialize asset database with schema

Usage:
    python3 tools/init-asset-db.py
    python3 tools/init-asset-db.py --db-path custom-assets.db
"""

import sqlite3
import argparse
from pathlib import Path

def create_schema(db_path):
    """Create complete asset database schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Main assets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE NOT NULL,
            file_name TEXT NOT NULL,
            type TEXT NOT NULL,  -- 'video', 'image', 'screenshot', 'web_roll'
            duration REAL,       -- seconds (NULL for images)
            resolution TEXT,     -- "1920x1080"
            file_size INTEGER,   -- bytes

            -- AI-generated metadata
            description TEXT NOT NULL,
            mood TEXT,
            setting TEXT,
            people TEXT,
            color_palette TEXT,  -- JSON array
            quality_notes TEXT,

            -- Manual overrides (optional)
            manual_keywords TEXT,  -- JSON array
            manual_notes TEXT,
            manual_category TEXT,

            -- Usage tracking
            use_count INTEGER DEFAULT 0,
            last_used TEXT,
            added_at TEXT NOT NULL,
            tagged_at TEXT NOT NULL
        )
    """)

    # Keywords table (for efficient keyword search)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            keyword TEXT NOT NULL,
            source TEXT NOT NULL,  -- 'ai' or 'manual'
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_keywords ON keywords(keyword)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_keywords_asset ON keywords(asset_id)")

    # Categories/themes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,  -- 'category', 'theme', 'object', 'action', 'use_case'
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categories ON categories(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categories_asset ON categories(asset_id)")

    # Embeddings (for vector search)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            asset_id INTEGER PRIMARY KEY,
            embedding BLOB NOT NULL,  -- Pickled numpy array
            model TEXT NOT NULL,
            dimensions INTEGER NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        )
    """)

    # Metadata cache (full AI response)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata_cache (
            asset_id INTEGER PRIMARY KEY,
            ai_metadata TEXT NOT NULL,  -- JSON blob of complete AI response
            model_used TEXT NOT NULL,
            analyzed_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

    print(f"✅ Database schema created: {db_path}")

def main():
    parser = argparse.ArgumentParser(description="Initialize asset database")
    parser.add_argument('--db-path', default='assets.db', help="Database file path")

    args = parser.parse_args()

    db_path = Path(args.db_path)

    if db_path.exists():
        response = input(f"Database {db_path} already exists. Recreate? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
        db_path.unlink()

    create_schema(args.db_path)

    print("")
    print("Database ready for asset ingestion.")
    print("")
    print("Next step:")
    print(f"  python3 tools/batch-analyze-assets.py --asset-dir /path/to/assets --db {args.db_path}")

if __name__ == '__main__':
    main()
