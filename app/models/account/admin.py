from pydantic import Field, EmailStr
from pymongo import HASHED

__all__ = (
    'AdminModel',
)

from app.models import BaseDBModel


class AdminModel(BaseDBModel):
    name: str = Field(..., description='Admin Name'),
    email: EmailStr = Field(..., description='Admin Email')

    class Settings:
        name = 'admins'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
