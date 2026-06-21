from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from app.database import init_db
from app.indexer import index_all
from app.routes import router

app = FastAPI(title="Jun's Wiki API")

WIKI_DIR = Path(__file__).resolve().parent.parent

@app.on_event("startup")
async def startup():
    init_db()
    count, skipped = index_all()
    print(f"✅ Wiki indexed: {count} pages ({skipped} skipped)")

# API routes
app.include_router(router)

# Serve static files (HTML, CSS, JS)
static_dir = WIKI_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Serve the landing page
@app.get("/")
async def root():
    return FileResponse(str(WIKI_DIR / "static" / "index.html"))

@app.get("/viewer")
async def viewer():
    return FileResponse(str(WIKI_DIR / "static" / "viewer.html"))
