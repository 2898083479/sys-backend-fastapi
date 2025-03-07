from fastapi import APIRouter, Query, Request

from app.response import ResponseModel

router = APIRouter(
    prefix='/store', tags=['Store API'], dependencies=[]
)


@router.get(
    '',
    response_model=ResponseModel[str],
    description='Query Store'
)
async def query_store(
    store_id: str = Query(..., alias='storeId', description='Store Id'),
    request: Request = None,
):
    pass
