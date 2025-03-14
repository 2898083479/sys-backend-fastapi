__all__ = (
    'QueryGoodResponse',
)

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.good import GoodCategoryEnum


class QueryGoodResponse(BaseModel):
    goodId: str = Field(..., description='Good id'),
    name: str = Field(..., description='Good name'),
    source: str = Field(..., description='Good source'),
    category: GoodCategoryEnum = Field(..., description='Good category'),
    price: float = Field(..., description='Good price'),
    count: int = Field(..., description='Good count'),
    createAt: datetime = Field(..., description='Good created date'),
    policyList: set[str] = Field(..., description='Good policy list'),
