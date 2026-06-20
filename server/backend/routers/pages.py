from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from database import get_db
from models import WikiPage, PageView
from schemas import WikiPageResponse, WikiPageListItem

router = APIRouter(prefix="/api/pages", tags=["pages"])

@router.get("/", response_model=list[WikiPageListItem])
async def list_pages(category: str = "", offset: int = 0, limit: int = 50):
    async for db in get_db():
        stmt = select(WikiPage).where(WikiPage.published == True)
        if category:
            stmt = stmt.where(WikiPage.category == category)
        stmt = stmt.order_by(WikiPage.updated_at.desc()).offset(offset).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

@router.get("/categories")
async def list_categories():
    async for db in get_db():
        stmt = select(WikiPage.category, func.count(WikiPage.id)).where(
            WikiPage.published == True
        ).group_by(WikiPage.category).order_by(WikiPage.category)
        result = await db.execute(stmt)
        return [{"category": row[0], "count": row[1]} for row in result if row[0]]

@router.get("/{slug}", response_model=WikiPageResponse)
async def get_page(slug: str):
    async for db in get_db():
        stmt = select(WikiPage).where(WikiPage.slug == slug)
        result = await db.execute(stmt)
        page = result.scalar_one_or_none()
        if not page:
            raise HTTPException(404, "Page not found")
        return page

@router.post("/{slug}/view")
async def track_view(slug: str, x_real_ip: str = "", user_agent: str = ""):
    async for db in get_db():
        stmt = select(WikiPage.id).where(WikiPage.slug == slug)
        result = await db.execute(stmt)
        page_id = result.scalar_one_or_none()
        if not page_id:
            raise HTTPException(404, "Page not found")
        view = PageView(page_id=page_id, ip=x_real_ip, user_agent=user_agent)
        db.add(view)
        await db.commit()
        return {"ok": True}
