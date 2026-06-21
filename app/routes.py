from fastapi import APIRouter, Query, HTTPException
from app.indexer import search_pages, get_page, list_pages, get_stats, index_all

router = APIRouter(prefix="/api")

@router.get("/search")
async def search(q: str = Query(..., min_length=1), limit: int = Query(20, le=50)):
    results = search_pages(q, limit)
    return {"results": results, "total": len(results)}

@router.get("/page")
async def page(path: str = Query(...)):
    p = get_page(path)
    if not p:
        raise HTTPException(status_code=404, detail="Page not found")
    return p

@router.get("/list")
async def list_all():
    return list_pages()

@router.get("/stats")
async def stats():
    return get_stats()

@router.post("/reindex")
async def reindex():
    count, skipped = index_all()
    return {"indexed": count, "skipped": skipped}
