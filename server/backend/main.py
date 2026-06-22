from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from database import init_db, engine
from routers import pages, search, tracking
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(
    title="Wiki API",
    version="1.0.0",
    docs_url="/api/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jno-worldline.myds.me",
        "http://192.168.1.107:8000",
        "http://localhost:8000",
        "https://jnocode.github.io",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)
app.include_router(search.router)
app.include_router(tracking.router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

# 前台靜態檔案（VitePress build output）
WIKI_DIR = os.environ.get("WIKI_PATH", "/wiki")

@app.api_route("/{path:path}", methods=["GET"])
async def serve_frontend(path: str):
    # API 路徑已由上方 router 處理，不會進到這裡
    file_path = os.path.join(WIKI_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # SPA fallback: 找不到檔案就回 index.html
    index_path = os.path.join(WIKI_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Not found"}, status_code=404)
