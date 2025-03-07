from fastapi import Body
from pydantic import BaseModel, EmailStr

__all__ = (
    'LoginForm',
    'RegisterForm'
)


class LoginForm(BaseModel):
    identity: int = Body(..., embed=True, description='user identity')
    email: str = Body(..., embed=True, description='login email')
    password: str = Body(..., embed=True, description='login password')


class RegisterForm(BaseModel):
    name: str = Body(..., embed=True, description='register name')
    email: EmailStr = Body(..., embed=True, description='register email')
    password: str = Body(..., embed=True, description='register password')
    identity: int = Body(..., embed=True, description='register identity')
