__all__ = (
    'CreateStoreForm',
    'AddMerchantToStoreForm',
)

from typing import Optional

from fastapi import Body
from pydantic import BaseModel, EmailStr


class CreateStoreForm(BaseModel):
    name: str = Body(..., embed=True, description='Store name')
    email: EmailStr = Body(..., embed=True, description='Store email')
    status: Optional[str] = Body('Pending', embed=True, description='Store status')
    description: str = Body(..., embed=True, description='Store description')


class AddMerchantToStoreForm(BaseModel):
    storeId: str = Body(..., embed=True, description='store id')
    merchantId: str = Body(..., embed=True, description='merchant id')