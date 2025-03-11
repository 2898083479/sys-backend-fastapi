from typing import Optional

from fastapi import APIRouter, Query, Request

from app.forms.store import CreateStoreForm, AddMerchantToStoreForm, UpdateStoreForm
from app.response import ResponseModel
from app.response.store import StoreInfoResponse
from app.view_models.store import (
    QueryStoreInfoViewModel, CreateStoreViewModel, AddMerchantToStoreViewModel,
    QueryStoreListViewModel, ReviewStoreViewModel, UpdateStoreViewModel, DeleteStoreViewModel
)

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


@router.get(
    '/list',
    response_model=ResponseModel[list[StoreInfoResponse] | str],
    description='Query Store List'
)
async def query_store_list(
        search: Optional[str] = Query('', description='Search key'),
        request: Request = None,
):
    async with QueryStoreListViewModel(search, request) as response:
        return response


@router.put(
    '/review',
    response_model=ResponseModel[str],
    description='Review Store'
)
async def review_store(
        store_id: str = Query(..., alias='storeId', description='Store id'),
        request: Request = None,
):
    async with ReviewStoreViewModel(store_id, request) as response:
        return response


@router.put(
    '',
    response_model=ResponseModel[str],
    description='Update store'
)
async def update_store(
        form_data: UpdateStoreForm,
        request: Request = None
):
    async with UpdateStoreViewModel(form_data, request) as response:
        return response


@router.delete(
    '',
    response_model=ResponseModel[str],
    description='Delete store'
)
async def delete_store(
        store_id: str = Query(..., alias='storeId', description='Delete store'),
        request: Request = None
):
    async with DeleteStoreViewModel(store_id, request) as response:
        return response
