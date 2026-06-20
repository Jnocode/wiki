from fastapi import APIRouter, HTTPException
import httpx
from config import settings
from schemas import SearchResponse, SearchResult

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/", response_model=SearchResponse)
async def search(q: str = "", category: str = "", limit: int = 20):
    if not q.strip():
        return SearchResponse(query=q, results=[], total=0)

    filter_str = f"category = {category}" if category else ""

    body = {
        "q": q,
        "limit": limit,
        "attributesToSearchOn": ["title", "content", "tags", "category"],
        "attributesToCrop": ["content"],
        "cropLength": 120,
    }
    if filter_str:
        body["filter"] = filter_str

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.meili_url}/indexes/wiki/search",
            json=body,
            headers={"Authorization": f"Bearer {settings.meili_key}"},
        )
        if resp.status_code != 200:
            raise HTTPException(502, f"Search failed: {resp.text}")

        data = resp.json()
        results = [
            SearchResult(
                slug=h["slug"],
                title=h["title"],
                category=h.get("category", ""),
                snippet=h["_formatted"].get("content", "")[:200] if "_formatted" in h else "",
                score=h.get("_rankingScore", 0) or 0,
            )
            for h in data.get("hits", [])
        ]
        return SearchResponse(query=q, results=results, total=data.get("estimatedTotalHits", 0))
