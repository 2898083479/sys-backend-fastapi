__all__ = (
    'CreatePolicyForm'
)

from datetime import datetime

from fastapi import Body
from pydantic import BaseModel


class CreatePolicyForm(BaseModel):
    name: str = Body(..., embed=True, description='Policy name')
    status: str = Body(..., embed=True, description='Policy status')
    startAt: datetime = Body(..., embed=True, description='Policy valid date')
    endAt: datetime = Body(..., embed=True, description='Policy deadline date')
    description: str = Body(..., embed=True, description='Policy description')
