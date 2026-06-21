import os
from pathlib import Path
import markdown
from app.database import get_db, WIKI_DIR

def extract_title(content: str, path: str) -> str:
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line.lstrip('# ').strip()
    return Path(path).stem.replace('-', ' ').replace('_', ' ').title()

def get_category(path: str) -> str:
    parts = Path(path).parts
    if len(parts) >= 2:
        return parts[0]
    return 'root'

def index_all():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pages")

    md_files = sorted(WIKI_DIR.rglob('*.md'))
    count = 0
    skipped = 0

    for fpath in md_files:
        rel_path = fpath.relative_to(WIKI_DIR).as_posix()
        if any(part.startswith('.') for part in Path(rel_path).parts):
            continue
        if rel_path.startswith('app/') or rel_path.startswith('static/'):
            continue
        if rel_path in ('SCHEMA.md', 'log.md'):
            continue

        try:
            content = fpath.read_text(encoding='utf-8')
        except Exception:
            try:
                content = fpath.read_text(encoding='cp950')
            except Exception:
                skipped += 1
                continue

        title = extract_title(content, rel_path)
        category = get_category(rel_path)

        html = markdown.markdown(
            content,
            extensions=['fenced_code', 'codehilite', 'tables', 'toc']
        )

        cursor.execute(
            "INSERT OR REPLACE INTO pages (path, title, category, content) VALUES (?, ?, ?, ?)",
            (rel_path, title, category, html)
        )
        count += 1

    conn.commit()
    conn.close()
    return count, skipped

def search_pages(query: str, limit: int = 20):
    """Full-text search: FTS5 for English, LIKE fallback for Chinese."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if query has CJK characters
    has_cjk = any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u30ff' or '\uac00' <= c <= '\ud7af' for c in query)

    results = []

    if has_cjk:
        # CJK: Use LIKE search (FTS5 doesn't segment CJK well)
        like_q = f"%{query}%"
        cursor.execute("""
            SELECT id, path, title, category,
                   SUBSTR(content, 1, 100) AS snippet
            FROM pages
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY
                CASE WHEN title LIKE ? THEN 0 ELSE 1 END,
                id
            LIMIT ?
        """, (like_q, like_q, like_q, limit))
        results = [dict(row) for row in cursor.fetchall()]
    else:
        # English: Use FTS5
        clean = query.replace('"', '""')
        terms = [f'"{w}"' for w in clean.split() if w]
        if terms:
            fts_query = ' OR '.join(terms)
            cursor.execute("""
                SELECT p.id, p.path, p.title, p.category,
                       snippet(pages_fts, 1, '<mark>', '</mark>', '...', 40) AS snippet
                FROM pages_fts
                JOIN pages p ON pages_fts.rowid = p.id
                WHERE pages_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit))
            results = [dict(row) for row in cursor.fetchall()]

            # If FTS5 returns nothing, fall back to LIKE
            if not results:
                like_q = f"%{query}%"
                cursor.execute("""
                    SELECT id, path, title, category,
                           SUBSTR(content, 1, 100) AS snippet
                    FROM pages
                    WHERE title LIKE ? OR content LIKE ?
                    ORDER BY
                        CASE WHEN title LIKE ? THEN 0 ELSE 1 END,
                        id
                    LIMIT ?
                """, (like_q, like_q, like_q, limit))
                results = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return results

def get_page(path: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pages WHERE path = ?", (path,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def list_pages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT path, title, category FROM pages ORDER BY category, title")
    rows = cursor.fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        r = dict(row)
        cat = r['category'] or '其他'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(r)
    return grouped

def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM pages")
    total = cursor.fetchone()['total']
    cursor.execute("SELECT category, COUNT(*) as cnt FROM pages GROUP BY category ORDER BY cnt DESC")
    cats = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {'total_pages': total, 'categories': cats}
