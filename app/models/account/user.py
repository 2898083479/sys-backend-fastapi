from pymongo import HASHED

from app.models import BaseDBModel

__all__ = (
    'UserModel',
)


class UserModel(BaseDBModel):
    name: str
    email: str

    class Settings:
        name = 'users'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
