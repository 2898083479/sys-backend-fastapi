__all__ = (
    'CreateGoodForm',
    'UpdateGoodForm',
)

from fastapi import Body
from pydantic import BaseModel

from app.models.good import GoodCategoryEnum


class CreateGoodForm(BaseModel):
    name: str = Body(..., embed=True, description='Good name')
    source: str = Body(..., embed=True, description='Good source'),
    category: GoodCategoryEnum = Body(..., embed=True, description='Good category')
    goodPrice: float = Body(..., embed=True, description='Good price')
    goodCount: int = Body(..., embed=True, description='Good count')


class UpdateGoodForm(BaseModel):
    goodId: str = Body(..., embed=True, description='Good id'),
    name: str = Body(..., embed=True, description='Good name'),
    source: str = Body(..., embed=True, description='Good source'),
    category: str = Body(..., embed=True, description='Good category')
    price: float = Body(..., embed=True, description='Good price')
    count: int = Body(..., embed=True, description='Good count')
