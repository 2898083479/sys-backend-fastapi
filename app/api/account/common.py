from fastapi import FastAPI

from app.forms.account.common import LoginForm
from app.response import ResponseModel
from app.response.common import LoginSuccessResponse
from app.view_models.account.common import AdminLoginViewModel

router = FastAPI(
    prefix='/common', tags=['Account common API'], dependencies=[]
)


@router.get(
    '/login',
    response_model=ResponseModel[LoginSuccessResponse | str],
    description='User login'
)
async def login(
        form_data: LoginForm
):
    async with AdminLoginViewModel(form_data) as response:
        return response


@router.get(
    '/register',
    response_model=ResponseModel[str],
    description='User register'
)
async def register(

):
    pass
