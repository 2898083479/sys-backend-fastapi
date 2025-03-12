__all__ = (
    'GoodCategoryEnum',
)

from enum import StrEnum
from typing import Optional

from pydantic import Field, BaseModel

from app.models import BaseDBModel


class GoodCategoryEnum(StrEnum):
    SPICE = '香料',
    CARVING = '精雕',
    MEDICINE = '药物',
    FURNITURE = '家具',


class GoodAffiliation(BaseModel):
    policyList: Optional[set[str]] = Field(default_factory=lambda: set, description='policy set')
    storeList: Optional[set[str]] = Field(default_factory=lambda: set, description='store set')


class GoodModel(BaseDBModel):
    name: str = Field(..., description='Good name'),
    source: str = Field(..., description='Good source'),
    category: GoodCategoryEnum = Field(..., description='Good category'),
    price: float = Field(..., description='Good price'),
    count: int = Field(..., description='Good count'),
    affiliation: Optional[GoodAffiliation] = Field(None, description='Good affiliation')

