from typing import Optional

from pydantic import Field
from pymongo import HASHED

from app.models import BaseUserModel

__all__ = (
    'AdminModel',
)


class AdminModel(BaseUserModel):
    deleted: Optional[bool] = Field(False, description='')

    class Settings:
        name = 'admins'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
