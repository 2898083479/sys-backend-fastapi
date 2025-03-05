from pydantic import BaseModel, Field, EmailStr

__all__ = (
    'LoginSuccessResponse'
)


class LoginSuccessResponse(BaseModel):
    userId: str = Field(..., description='user ID')
    token: str = Field(..., description='token')
    name: str = Field(..., description='user name')
    email: EmailStr = Field(..., description='user email')
