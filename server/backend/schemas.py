from pydantic import BaseModel
from typing import Optional, List
import datetime

class WikiPageResponse(BaseModel):
    id: int
    slug: str
    title: str
    category: str
    tags: list
    content: str
    word_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {"from_attributes": True}

class WikiPageListItem(BaseModel):
    id: int
    slug: str
    title: str
    category: str
    tags: list
    word_count: int
    updated_at: datetime.datetime

    model_config = {"from_attributes": True}

class WikiPageCreate(BaseModel):
    slug: str
    title: str
    category: str = ""
    tags: list = []
    content: str
    published: bool = True

class WikiPageUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class SearchResult(BaseModel):
    slug: str
    title: str
    category: str
    snippet: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int

class StatsResponse(BaseModel):
    total_pages: int
    total_views: int
    top_pages: list[dict]
