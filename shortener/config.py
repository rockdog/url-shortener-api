from functools import lru_cache

from pydantic import BaseSettings
from starlette.datastructures import URL


class Settings(BaseSettings):
    env_name: str
    base_url: str
    db_url: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def base_url() -> Settings:
    return URL(get_settings().base_url)
