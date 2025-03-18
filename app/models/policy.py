__all__ = (
    'PolicyModel',
)

from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel
from pymongo import HASHED

from app.models import BaseDBModel


class PolicyAffiliation(BaseModel):
    goodId: str = Field(..., description='good id')


class PolicyModel(BaseDBModel):
    name: str = Field(..., description='Policy name')
    status: str = Field(..., description='Policy status')
    deleted: Optional[bool] = Field(False, description='is deleted')
    description: str = Field(..., description='Policy description')
    startAt: datetime = Field(..., description='Start date')
    endAt: datetime = Field(..., description='End date')
    affiliation: Optional[PolicyAffiliation] = Field(None, description='policy affiliation, from good')

    class Settings:
        name = 'policies'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
