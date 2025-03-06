from typing import Optional

from pydantic import Field, BaseModel
from pymongo import HASHED

from app.models import BaseUserModel

__all__ = (
    'MerchantAffiliation',
    'MerchantModel',
)


class MerchantAffiliation(BaseModel):
    storeId: str = Field(..., description='store id')


class MerchantModel(BaseUserModel):
    status: Optional[str] = Field('Pending', description='merchant status')
    affiliation: Optional[MerchantAffiliation] = Field(None, description='merchant affiliation: storeId')

    class Settings:
        name = 'merchants'
        strict = False
        indexes = [
            [('_id', HASHED)]
        ]
