from typing import Optional

from fastapi import APIRouter, Query, Request

from app.forms.policy import CreatePolicyForm, UpdatePolicyForm
from app.response import ResponseModel
from app.response.policy import QueryPolicyResponse
from app.view_models.policy import CreatePolicyViewModel, QueryOnePolicyViewModel, QueryPolicyListViewModel, \
    UpdatePolicyViewModel

router = APIRouter(
    prefix='/policy', tags=['Policy API'], dependencies=[]
)


@router.get(
    '/one',
    response_model=ResponseModel[QueryPolicyResponse | str],
    description='Query policy by id'
)
async def query_policy(
        policy_id: str = Query(..., alias='policyId', description='Policy ID'),
        request: Request = None,
):
    async with QueryOnePolicyViewModel(policy_id, request) as response:
        return response


@router.post(
    '/',
    response_model=ResponseModel[str],
    description='Create policy'
)
async def create_policy(
        form_data: CreatePolicyForm,
        request: Request = None
):
    async with CreatePolicyViewModel(form_data, request) as response:
        return response


@router.get(
    '/list',
    response_model=ResponseModel[list[QueryPolicyResponse | str]],
    description='Query policy list'
)
async def query_policy_list(
        search: Optional[str] = Query('', description='Search key'),
        request: Request = None,
):
    async with QueryPolicyListViewModel(search, request) as response:
        return response


@router.put(
    '',
    response_model=ResponseModel[str],
    description='Update policy'
)
async def update_policy(
        form_data: UpdatePolicyForm,
        request: Request = None
):
    async with UpdatePolicyViewModel(form_data, request) as response:
        return response
