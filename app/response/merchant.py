__all__ = (
    'MerchantInfoResponse'
)

from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class MerchantInfoResponse(BaseModel):
    merchantId: str = Field(..., description='merchant id')
    storeId: str = Field(..., description='store id')
    name: str = Field(..., description='merchant name')
    email: EmailStr = Field(..., description='merchant email')
    status: str = Field(..., description='merchant status')
    createdAt: datetime = Field(..., description='merchant created time')
