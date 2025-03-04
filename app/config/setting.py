from functools import lru_cache
import pathlib
from pydantic.v1 import BaseSettings
__all__ = (
    'Setting',
    'get_setting',
)


class Setting(BaseSettings):
    APP_NAME: str
    APP_NO: str
    APP_ENV: str
    
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str
    MONGODB_DB: str
    MONGODB_PORT: str
    
    class Config:
        env_file = f'{pathlib.Path(__file__).resolve().parent.parent.parent}/.env'
    
    
@lru_cache()
def get_setting() -> Setting:
    return Setting()
    