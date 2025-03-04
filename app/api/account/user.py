from fastapi import APIRouter

router = APIRouter(
    prefix='/user', tags=['User Account API'], dependencies=[]
)


@router.get(
    '',
    description='Get User Account Information',
)
async def get_admin_info():
    return {'message': 'Get User Account Information'}
