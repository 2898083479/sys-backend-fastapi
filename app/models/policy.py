__all__ = (
    'PolicyModel'
)

from datetime import datetime

from pydantic import Field
from pymongo import HASHED

from app.models import BaseDBModel


class PolicyModel(BaseDBModel):
    name: str = Field(..., description='Policy name')
    status: str = Field(..., description='Policy status')
    description: str = Field(..., description='Policy description')
    startAt: datetime = Field(..., description='Start date')
    endAt: datetime = Field(..., description='End date')
    createAt: datetime = Field(..., description='Create date')
    updateAt: datetime = Field(..., description='Update date')

    class Settings:
        name = 'policies'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
