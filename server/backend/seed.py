"""
Seed: 將 wiki/ 底下的 .md 檔案匯入 PostgreSQL + Meilisearch。
用法: python seed.py
"""
import asyncio
import os
import re
import frontmatter
import httpx
from config import settings
from database import init_db, async_session
from models import WikiPage
from sqlalchemy import select

WIKI_ROOT = settings.wiki_path

def extract_title(filepath: str, content: str, fm: dict) -> str:
    if fm.get("title"):
        return fm["title"]
    m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    name = os.path.splitext(os.path.basename(filepath))[0]
    return name.replace("-", " ").replace("_", " ").title()

def extract_category(filepath: str) -> str:
    parts = filepath.replace("\\", "/").split("/")
    for i, p in enumerate(parts):
        if p in ("entities", "concepts", "comparisons"):
            return f"{p}/{parts[i+1]}" if i + 1 < len(parts) else p
    return ""

async def seed():
    await init_db()

    pages = []
    for root, dirs, files in os.walk(WIKI_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("server", "_archive", "raw", "queries")]
        for f in files:
            if not f.endswith(".md") or f in ("index.md", "SCHEMA.md", "log.md"):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, WIKI_ROOT).replace("\\", "/")
            slug = os.path.splitext(rel)[0]

            with open(fpath, "r", encoding="utf-8") as fh:
                fm, content = frontmatter.parse(fh.read())

            title = extract_title(fpath, content, fm)
            category = extract_category(rel)
            tags = fm.get("tags") or fm.get("標籤") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]

            pages.append({
                "slug": slug,
                "title": title,
                "category": category,
                "tags": tags if isinstance(tags, list) else [],
                "content": content,
                "word_count": len(content.split()),
            })

    # 寫入 PostgreSQL
    async with async_session() as db:
        for p in pages:
            result = await db.execute(select(WikiPage).where(WikiPage.slug == p["slug"]))
            existing = result.scalar_one_or_none()
            if existing:
                for k, v in p.items():
                    setattr(existing, k, v)
            else:
                db.add(WikiPage(**p))
        await db.commit()

    print(f"✅ DB: {len(pages)} pages seeded")

    # 寫入 Meilisearch
    async with httpx.AsyncClient() as client:
        docs = [
            {
                "slug": p["slug"],
                "title": p["title"],
                "category": p["category"],
                "tags": p["tags"],
                "content": p["content"],
            }
            for p in pages
        ]
        resp = await client.post(
            f"{settings.meili_url}/indexes/wiki/documents",
            json=docs,
            headers={"Authorization": f"Bearer {settings.meili_key}"},
        )
        if resp.status_code == 202:
            print(f"✅ Meilisearch: {len(docs)} docs indexed")
        else:
            print(f"⚠️  Meilisearch error: {resp.status_code} {resp.text}")

        # 設定可搜尋欄位
        await client.patch(
            f"{settings.meili_url}/indexes/wiki/settings",
            json={
                "searchableAttributes": ["title", "content", "tags", "category"],
                "filterableAttributes": ["category"],
            },
            headers={"Authorization": f"Bearer {settings.meili_key}"},
        )

if __name__ == "__main__":
    asyncio.run(seed())
