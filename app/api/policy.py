from fastapi import APIRouter, Query, Request

from app.response import ResponseModel
from app.response.policy import QueryPolicyResponse

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
    pass


@router.post(
    '/',
    response_model=ResponseModel[str],
    description='Create policy'
)
async def create_policy(

):
    pass
