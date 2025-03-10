__all__ = (
    'StoreAffiliation',
    'StoreModel'
)

from typing import Optional

from pydantic import Field, EmailStr, BaseModel
from pymongo import HASHED

from app.models import BaseDBModel


class StoreAffiliation(BaseModel):
    merchantList: Optional[set[str]] = Field(default_factory=lambda: set, description='Merchant list')
    goodList: Optional[set[str]] = Field(default_factory=lambda: set, description='Good list')


class StoreModel(BaseDBModel):
    name: str = Field(..., description='Store name')
    email: EmailStr = Field(..., description='Store email')
    status: str = Field(..., description='Store status')
    description: str = Field(..., description='Store description')
    affiliation: Optional[StoreAffiliation] = Field(None, description='Store Affiliation: merchant_list, good_list')

    class Settings:
        name = 'stores'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]

    @property
    def merchant_count(self):
        return len(self.affiliation.merchant_list)

    @property
    def good_count(self):
        return len(self.affiliation.good_list)
