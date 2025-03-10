from typing import Optional

from fastapi import APIRouter, Query, Request

from app.forms.account.merchant import UpdateMerchantForm
from app.response import ResponseModel
from app.response.merchant import MerchantInfoResponse
from app.view_models.account.merchant import QueryMerchantByIdViewMode, UpdateMerchantViewModel, \
    QueryMerchantListViewModel, ReviewMerchantViewModel, DeleteMerchantViewModel

router = APIRouter(
    prefix='/merchant', tags=['Merchant Account API'], dependencies=[]
)


@router.get(
    '/one',
    response_model=ResponseModel[MerchantInfoResponse | str],
    description='Get Merchant info by id'
)
async def get_merchant(
        merchant_id: str = Query(..., alias='merchantId', description='merchant id'),
        request: Request = None
):
    async with QueryMerchantByIdViewMode(merchant_id, request) as response:
        return response


@router.put(
    '',
    response_model=ResponseModel[str],
    description='Update merchant account'
)
async def update_merchant_account(
        form_data: UpdateMerchantForm,
        request: Request
):
    async with UpdateMerchantViewModel(form_data, request) as response:
        return response


@router.get(
    '/list',
    response_model=ResponseModel[list[MerchantInfoResponse] | str],
    description='Query merchant list'
)
async def query_merchant_list(
        search: Optional[str] = Query('', description='search key'),
        request: Request = None
):
    async with QueryMerchantListViewModel(search, request) as response:
        return response


@router.put(
    '/review',
    response_model=ResponseModel[str],
    description='Review merchant'
)
async def review_merchant(
        merchant_id: str = Query(..., alias='merchantId', description='merchant id'),
        request: Request = None
):
    async with ReviewMerchantViewModel(merchant_id, request) as response:
        return response


@router.delete(
    '',
    response_model=ResponseModel[str],
    description='Delete merchant account'
)
async def delete_merchant_account(
        merchant_id: str = Query(..., alias='merchantId', description='merchant id'),
        request: Request = None
):
    async with DeleteMerchantViewModel(merchant_id, request) as response:
        return response
