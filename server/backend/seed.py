#!/usr/bin/env python3
"""Seed: 將 wiki/ 底下的 .md 檔案匯入 PostgreSQL + Meilisearch。"""
import asyncio, os, re, httpx, frontmatter
from config import settings
from database import init_db, async_session
from models import WikiPage
from sqlalchemy import select

WIKI_ROOT = settings.wiki_path

def extract_title(filepath, content, fm):
    if fm.get("title"):
        return fm["title"]
    m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    name = os.path.splitext(os.path.basename(filepath))[0]
    return name.replace("-", " ").replace("_", " ").title()

def extract_category(filepath):
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
            existing_page = result.scalar_one_or_none()
            if existing_page:
                for k, v in p.items():
                    setattr(existing_page, k, v)
            else:
                db.add(WikiPage(**p))
        await db.commit()
    print(f"✅ DB: {len(pages)} pages seeded")

    # 寫入 Meilisearch
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = settings.meili_url
        hdr = {"Authorization": f"Bearer {settings.meili_key}"}
        
        # 1. 刪除舊索引（ignore error if not exists）
        try:
            await client.delete(url + "/indexes/wiki", headers=hdr)
        except:
            pass
        await asyncio.sleep(0.5)

        # 2. 用 primaryKey 建立索引
        r = await client.post(url + "/indexes", json={"uid": "wiki", "primaryKey": "id"}, headers=hdr)
        print(f"📦 Create index: {r.status_code} {r.json()}")
        await asyncio.sleep(0.5)

        # 3. 設定搜尋欄位
        r = await client.patch(url + "/indexes/wiki/settings", json={
            "searchableAttributes": ["title", "content", "tags", "category"],
            "filterableAttributes": ["category"],
        }, headers=hdr)
        print(f"⚙️  Settings: {r.status_code} {r.json()}")
        await asyncio.sleep(0.5)

        # 4. 寫入文件（用 sanitized slug 當 id，Meilisearch 不允許 / ）
        docs = [{"id": p["slug"].replace("/", "-"), **p} for p in pages]
        r = await client.post(url + "/indexes/wiki/documents", json=docs, headers=hdr)
        print(f"📄 Add docs: {r.status_code} {r.json()}")
        
        # 5. 等 indexing 完成後驗證
        await asyncio.sleep(2)
        r = await client.get(url + "/indexes/wiki/stats", headers=hdr)
        stats = r.json()
        print(f"📊 Stats: {stats.get('numberOfDocuments', 0)} documents")
        
        if stats.get("numberOfDocuments", 0) > 0:
            print(f"✅ Meilisearch: {stats['numberOfDocuments']} docs indexed")
        else:
            print(f"⚠️  Meilisearch: index may still be processing, check again later")

if __name__ == "__main__":
    asyncio.run(seed())
