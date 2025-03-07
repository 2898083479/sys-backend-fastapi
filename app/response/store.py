__all__ = (
    'StoreInfoResponse',
)

from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class StoreInfoResponse(BaseModel):
    name: str = Field(..., description='Store name')
    email: EmailStr = Field(..., description='Store email')
    status: str = Field(..., description='Store status')
    description: str = Field(..., description='Store description')
    merchant_count: int = Field(..., description='Number of merchants in the store')
    good_count: int = Field(..., description='Number of goods in the store')
    createdAt: datetime = Field(..., description='Store created time')
