from typing import Optional

from pydantic import Field, EmailStr, BaseModel
from pymongo import HASHED

from app.models import BaseDBModel

__all__ = (
    'StoreAffiliation',
    'StoreModel'
)


class StoreAffiliation(BaseModel):
    merchantList: Optional[set[str]] = Field(default_factory=lambda: set, description='Merchant list')
    goodList: Optional[set[str]] = Field(default_factory=lambda: set, description='Good list')


class StoreModel(BaseDBModel):
    name: str = Field(..., description='Store name')
    email: EmailStr = Field(..., description='Store email')
    deleted: Optional[bool] = Field(False, description='is deleted')
    status: Optional[str] = Field('待審核', description='Store status')
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
        if self.affiliation is not None:
            merchant_count = len(self.affiliation.merchantList)
            return merchant_count if merchant_count else 0
        return 0

    @property
    def good_count(self):
        if self.affiliation is not None:
            good_count = len(self.affiliation.goodList)
            return good_count if good_count else 0
        return 0
