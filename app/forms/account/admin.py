from typing import Optional

from fastapi import Body
from pydantic import BaseModel, EmailStr

__all__ = (
    'CreateAdminForm'
)


class CreateAdminForm(BaseModel):
    name: str = Body(..., embed=True, description='admin name'),
    email: EmailStr = Body(..., embed=True, description='admin email')


class UpdateAdminForm(BaseModel):
    adminId: Optional[str] = Body(..., embed=True, description='admin id')
    name: Optional[str] = Body(..., embed=True, description='admin name'),
    email: Optional[EmailStr] = Body(..., embed=True, description='admin email')
