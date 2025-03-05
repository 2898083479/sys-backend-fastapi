from typing import Optional

from pydantic import Field, EmailStr
from pymongo import HASHED

from app.models import BaseDBModel

__all__ = (
    'AdminModel',
)


class AdminModel(BaseDBModel):
    name: str = Field(..., description='Admin Name')
    email: EmailStr = Field(..., description='Admin Email')
    password: str = Field(..., description='Admin Password')
    deleted: Optional[bool] = Field(False, description='')

    class Settings:
        name = 'admins'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
