from typing import Optional

from fastapi import APIRouter, Query, Request

from app.forms.good import CreateGoodForm, UpdateGoodForm
from app.response import ResponseModel
from app.response.good import QueryGoodResponse
from app.view_models.good import (
    CreateGoodViewModel, QueryGoodViewModel,
    QueryGoodListViewModel, UpdateGoodViewModel,
    DeleteGoodViewModel
)

router = APIRouter(
    prefix='/good', tags=['Good API'], dependencies=[]
)


@router.get(
    '/one',
    response_model=ResponseModel[QueryGoodResponse | str],
    description='Query one good'
)
async def query_good(
        good_id: str = Query(..., alias='goodId', description='Good id'),
        request: Request = None
):
    async with QueryGoodViewModel(good_id, request) as response:
        return response


@router.post(
    '',
    response_model=ResponseModel[str],
    description='Create good'
)
async def create_good(
        form_data: CreateGoodForm,
        request: Request = None
):
    async with CreateGoodViewModel(form_data, request) as response:
        return response


@router.get(
    '/list',
    response_model=ResponseModel[list[QueryGoodResponse] | str],
    description='Query good list'
)
async def query_good_list(
        search: Optional[str] = Query('', description='Search key'),
        request: Request = None
):
    async with QueryGoodListViewModel(search, request) as response:
        return response


@router.put(
    '',
    response_model=ResponseModel[str],
    description='Update good'
)
async def update_good(
        form_data: UpdateGoodForm,
        request: Request = None
):
    async with UpdateGoodViewModel(form_data, request) as response:
        return response


@router.delete(
    '',
    response_model=ResponseModel[str],
    description='Delete good'
)
async def delete_good(
        good_id: str = Query(..., alias='goodId', description='Good id'),
        request: Request = None
):
    async with DeleteGoodViewModel(good_id, request) as response:
        return response
