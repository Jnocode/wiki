from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://wiki:wiki_change_me@localhost:5432/wiki"
    meili_url: str = "http://localhost:7700"
    meili_key: str = "wiki_change_me_secret"
    wiki_path: str = "/wiki"

    model_config = {"env_prefix": ""}

settings = Settings()
