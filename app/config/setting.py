from functools import lru_cache

__all__ = (
    'Setting',
    'get_setting',
)


class Setting:
    APP_NAME: str
    APP_NO: str
    APP_ENV: str
    
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str
    MONGODB_DB: str
    MONGODB_PORT: str
    
    
@lru_cache()
def get_setting() -> Setting:
    return Setting()
    