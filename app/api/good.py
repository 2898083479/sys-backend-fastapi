from fastapi import APIRouter

router = APIRouter(
    prefix='/good', tags=['Good API'], dependencies=[]
)
