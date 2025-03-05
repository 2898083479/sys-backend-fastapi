import pathlib
from functools import lru_cache

from pydantic.v1 import BaseSettings

__all__ = (
    'Settings',
    'get_settings',
)


class Settings(BaseSettings):
    APP_NAME: str
    APP_NO: str
    APP_ENV: str

    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str
    MONGODB_DB: str
    MONGODB_PORT: int
    MONGODB_AUTHENTICATION_SOURCE: str

    ENCRYPT_KEY: str

    class Config:
        env_file = f'{pathlib.Path(__file__).resolve().parent.parent.parent}/.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
