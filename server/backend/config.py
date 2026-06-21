from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://wiki:wiki123@127.0.0.1:5432/wiki"
    meili_url: str = "http://127.0.0.1:7700"
    meili_key: str = "wikikey123"
    wiki_path: str = "/wiki"

    model_config = {"env_prefix": ""}

settings = Settings()
