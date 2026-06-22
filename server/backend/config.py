from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://wiki:wiki123@127.0.0.1:5432/wiki")
    meili_url: str = os.getenv("MEILI_URL", "http://127.0.0.1:7700")
    meili_key: str = os.getenv("MEILI_KEY", "wikikey123")
    wiki_path: str = os.getenv("WIKI_PATH", "/wiki")

    model_config = {"env_prefix": ""}

settings = Settings()
