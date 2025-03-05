from fastapi import APIRouter, Query
from app.response import ResponseModel
from app.response.account import UserInfoResponse
from app.view_models.account.user import GetUserInfoViewModel, GetUserInfoOneViewModel

router = APIRouter(
    prefix='/user', tags=['User Account API'], dependencies=[]
)


@router.get(
    '',
    response_model=ResponseModel[UserInfoResponse | str],
    description='Get User Account Information',
)
async def get_admin_info():
    async with GetUserInfoViewModel() as response:
        return response


@router.get(
    '/one',
    response_model=ResponseModel[UserInfoResponse | str],
    description='Get User info by id'
)
async def get_user_info_by_id(
        user_id: str = Query(..., alias='userId', description='User')
):
    async with GetUserInfoOneViewModel(user_id) as response:
        return response
