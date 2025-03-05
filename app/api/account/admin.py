from fastapi import APIRouter, Request, Query
from app.forms.account.admin import CreateAdminForm, UpdateAdminForm
from app.response import ResponseModel
from app.response.account import AdminInfoResponse
from app.view_models.account.admin import (
        GetAdminInfoViewModel, GetAdminInfoByIdViewModel, CreateAdminViewModel,
        UpdateAdminViewModel, DeleteAdminViewModel, QueryAdminListViewModel
)

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


@router.post(
    '',
    response_model=ResponseModel[str],
    description='Create Admin account'
)
async def create_admin_account(
        form_data: CreateAdminForm
):
    async with CreateAdminViewModel(form_data) as response:
        return response


@router.put(
    '',
    response_model=ResponseModel[str],
    description='Update admin account'
)
async def update_admin_account(
        form_data: UpdateAdminForm,
):
    async with UpdateAdminViewModel(form_data) as response:
        return response


@router.delete(
    '',
    response_model=ResponseModel[str],
    description='Delete admin account'
)
async def delete_admin_account(
        admin_id: str = Query(..., alias='adminId', description='Admin ID'),
):
    async with DeleteAdminViewModel(admin_id) as response:
        return response


@router.get(
    '/list',
    response_model=ResponseModel[list[AdminInfoResponse] | str],
    description='Query admin list'
)
async def query_admin_list(
        request: Request,
):
    async with QueryAdminListViewModel(request) as response:
        return response
