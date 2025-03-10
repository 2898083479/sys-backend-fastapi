from fastapi import APIRouter, Query, Request

from app.forms.store import CreateStoreForm, AddMerchantToStoreForm
from app.response import ResponseModel
from app.response.store import StoreInfoResponse
from app.view_models.store import QueryStoreInfoViewModel, CreateStoreViewModel, AddMerchantToStoreViewModel

router = APIRouter(
    prefix='/store', tags=['Store API'], dependencies=[]
)


@router.get(
    '',
    response_model=ResponseModel[StoreInfoResponse | str],
    description='Query Store'
)
async def query_store(
        store_id: str = Query(..., alias='storeId', description='Store Id'),
        request: Request = None,
):
    async with QueryStoreInfoViewModel(store_id, request) as response:
        return response


@router.post(
    '',
    response_model=ResponseModel[str],
    description='Create Store'
)
async def create_store(
        form_data: CreateStoreForm,
        request: Request
):
    async with CreateStoreViewModel(form_data, request) as response:
        return response


@router.post(
    '/add/merchant',
    response_model=ResponseModel[str],
    description='Add Merchant to Store'
)
async def add_merchant_to_store(
        form_data: AddMerchantToStoreForm,
        request: Request
):
    async with AddMerchantToStoreViewModel(form_data, request) as response:
        return response
