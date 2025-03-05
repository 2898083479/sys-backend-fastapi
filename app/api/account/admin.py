from fastapi import APIRouter, Request, Query
from pydantic import Field

from app.response import ResponseModel
from app.response.account import AdminInfoResponse
from app.view_models.account.admin import GetAdminInfoViewModel, GetAdminInfoByIdViewModel

router = APIRouter(
    prefix='/admin', tags=['Admin Account API'], dependencies=[]
)


@router.get(
    '',
    response_model=ResponseModel[AdminInfoResponse | str],
    description='Get Admin Account Information',
)
async def get_admin_account_info(
        request: Request
):
    async with GetAdminInfoViewModel(request) as response:
        return response


@router.get(
    '/one',
    response_model=ResponseModel[AdminInfoResponse | str],
    description='Get Admin info by id'
)
async def get_admin_info_by_id(
        admin_id: str = Query(..., alias='adminId', description='admin id , must be exist'),
        request: Request = None,
):
    async with GetAdminInfoByIdViewModel(admin_id, request) as response:
        return response
