from pydantic import BaseModel, Field, EmailStr

__all__ = (
    'AdminInfoResponse'
)


class AdminInfoResponse(BaseModel):
    id: str = Field(..., description='Admin id'),
    name: str = Field(..., description='Admin name'),
    email: EmailStr = Field(..., description='Admin email')


class UserInfoResponse(BaseModel):
    id: str = Field(..., description='User id'),
    name: str = Field(..., description='User name'),
    email: str = Field(..., description='User email')
