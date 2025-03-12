__all__ = (
    'CreatePolicyForm',
    'UpdatePolicyForm',
)

from datetime import datetime
from typing import Optional

from fastapi import Body
from pydantic import BaseModel


class CreatePolicyForm(BaseModel):
    name: str = Body(..., embed=True, description='Policy name')
    status: Optional[str] = Body('未啟用', embed=True, description='Policy status')
    startAt: datetime = Body(..., embed=True, description='Policy valid date')
    endAt: datetime = Body(..., embed=True, description='Policy deadline date')
    description: Optional[str] = Body('', embed=True, description='Policy description')


class UpdatePolicyForm(BaseModel):
    policyId: str = Body(..., embed=True, description='Policy id')
    name: str = Body(..., embed=True, description='Policy name')
    description: Optional[str] = Body('', embed=True, description='Policy description')
    startAt: datetime = Body(..., embed=True, description='Policy valid date')
    endAt: datetime = Body(..., embed=True, description='Policy deadline date')
