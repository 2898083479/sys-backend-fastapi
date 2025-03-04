from fastapi import APIRouter, Request
from app.response import ResponseModel
from app.response.account import AdminInfoResponse
from app.view_models.account.admin import GetAdminInfoViewModel

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
