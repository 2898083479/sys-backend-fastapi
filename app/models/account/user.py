from pydantic import Field
from pymongo import HASHED

from app.models import BaseUserModel

__all__ = (
    'UserModel',
)


class UserModel(BaseUserModel):

    class Settings:
        name = 'users'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
