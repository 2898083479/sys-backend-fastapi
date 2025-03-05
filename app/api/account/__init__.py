from fastapi import APIRouter
from .admin import router as admin_router
from .user import router as user_router


router = APIRouter(
    prefix='/account', tags=['Account API'], dependencies=[]
)


router.include_router(admin_router)
router.include_router(user_router)
