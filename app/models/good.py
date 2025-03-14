__all__ = (
    'GoodModel',
    'GoodCategoryEnum',
)

from enum import StrEnum
from typing import Optional

from pydantic import Field, BaseModel
from pymongo import HASHED

from app.models import BaseDBModel


class GoodCategoryEnum(StrEnum):
    SPICE = '香料',
    CARVING = '精雕',
    MEDICINE = '藥物',
    FURNITURE = '家具',


class GoodAffiliation(BaseModel):
    policyList: Optional[set[str]] = Field(default_factory=lambda: set, description='policy set')
    storeList: Optional[set[str]] = Field(default_factory=lambda: set, description='store set')


class GoodModel(BaseDBModel):
    name: str = Field(..., description='Good name'),
    source: str = Field(..., description='Good source'),
    deleted: Optional[bool] = Field(False, description='is deleted'),
    category: GoodCategoryEnum = Field(..., description='Good category'),
    goodPrice: float = Field(..., description='Good price'),
    goodCount: int = Field(..., description='Good count'),
    affiliation: Optional[GoodAffiliation] = Field(None, description='Good affiliation')

    class Settings:
        name = 'goods'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
