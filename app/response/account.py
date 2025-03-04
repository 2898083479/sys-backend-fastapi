from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

__all__ = (
    'AdminInfoResponse'
)


class AdminInfoResponse(BaseModel):
    id: str = Field(..., description='Admin id'),
    name: str = Field(..., description='Admin name'),
    email: EmailStr = Field(..., description='Admin email')
