__all__ = (
    'CreateStoreForm',
    'AddMerchantToStoreForm',
    'UpdateStoreForm',
)

from typing import Optional

from fastapi import Body
from pydantic import BaseModel, EmailStr


class CreateStoreForm(BaseModel):
    name: str = Body(..., embed=True, description='Store name')
    email: EmailStr = Body(..., embed=True, description='Store email')
    description: Optional[str] = Body('', embed=True, description='Store description')


class AddMerchantToStoreForm(BaseModel):
    storeId: str = Body(..., embed=True, description='store id')
    merchantId: str = Body(..., embed=True, description='merchant id')


class UpdateStoreForm(BaseModel):
    storeId: str = Body(..., embed=True, description='store id')
    name: Optional[str] = Body('', embed=True, description='store name')
    email: Optional[EmailStr] = Body('', embed=True, description='store email')
    status: Optional[str] = Body('', embed=True, description='store status')
    description: Optional[str] = Body('', embed=True, description='store description')
