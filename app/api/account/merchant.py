from fastapi import APIRouter, Query, Request

from app.forms.account.merchant import UpdateMerchantForm
from app.response import ResponseModel
from app.response.merchant import MerchantInfoResponse
from app.view_models.account.merchant import QueryMerchantByIdViewMode, UpdateMerchantViewModel

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
        search: str = Query(..., description='search key'),
        request: Request = None
):
    pass
