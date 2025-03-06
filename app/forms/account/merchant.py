__all__ = (
    'UpdateMerchantForm',
)

from fastapi import Body
from pydantic import BaseModel


class UpdateMerchantForm(BaseModel):
    merchantId: str = Body(..., embed=True, description='merchant id')
    name: str = Body(..., embed=True, description='merchant name')
    email: str = Body(..., embed=True, description='merchant email')
    status: str = Body(..., embed=True, description='merchant status')
