from pydantic import BaseModel, Field, EmailStr

__all__ = (
    'LoginSuccessResponse',
    'AdminLoginResponse'
)


class LoginSuccessResponse(BaseModel):
    userId: str = Field(..., description='user ID')
    token: str = Field(..., description='token')
    name: str = Field(..., description='user name')
    email: EmailStr = Field(..., description='user email')


class AdminLoginResponse(BaseModel):
    accessToken: str = Field(..., description='access token')
