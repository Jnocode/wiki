from fastapi import APIRouter
from sqlalchemy import select, func, desc
from database import get_db
from models import WikiPage, PageView
from schemas import StatsResponse

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/", response_model=StatsResponse)
async def get_stats():
    async for db in get_db():
        total_pages = (await db.execute(
            select(func.count(WikiPage.id)).where(WikiPage.published == True)
        )).scalar() or 0

        total_views = (await db.execute(
            select(func.count(PageView.id))
        )).scalar() or 0

        top_raw = await db.execute(
            select(WikiPage.slug, WikiPage.title, func.count(PageView.id).label("cnt"))
            .join(PageView, WikiPage.id == PageView.page_id)
            .group_by(WikiPage.id)
            .order_by(desc("cnt"))
            .limit(10)
        )
        top_pages = [
            {"slug": slug, "title": title, "views": cnt}
            for slug, title, cnt in top_raw
        ]

        return StatsResponse(total_pages=total_pages, total_views=total_views, top_pages=top_pages)
