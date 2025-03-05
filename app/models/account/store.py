from pydantic import Field
from pymongo import HASHED
from app.models import BaseDBModel

__all__ = (
    'StoreModel',
)


class StoreModel(BaseDBModel):
    name: str = Field(..., description='Store name'),
    email: str = Field(..., description='Store email')

    class Settings:
        name = 'stores'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
