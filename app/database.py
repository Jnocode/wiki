import sqlite3
import os
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent
DB_PATH = WIKI_DIR / "wiki.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT DEFAULT '',
            content TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # FTS5 with default tokenizer
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
            title, content, path UNINDEXED,
            content='pages', content_rowid='id'
        )
    """)
    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN
            INSERT INTO pages_fts(rowid, title, content, path) VALUES (new.id, new.title, new.content, new.path);
        END;
        CREATE TRIGGER IF NOT EXISTS pages_ad AFTER DELETE ON pages BEGIN
            INSERT INTO pages_fts(pages_fts, rowid, title, content, path) VALUES('delete', old.id, old.title, old.content, old.path);
        END;
        CREATE TRIGGER IF NOT EXISTS pages_au AFTER UPDATE ON pages BEGIN
            INSERT INTO pages_fts(pages_fts, rowid, title, content, path) VALUES('delete', old.id, old.title, old.content, old.path);
            INSERT INTO pages_fts(rowid, title, content, path) VALUES (new.id, new.title, new.content, new.path);
        END;
    """)
    conn.commit()
    conn.close()
