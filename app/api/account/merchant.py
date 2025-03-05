from fastapi import FastAPI

router = FastAPI(
    prefix='/merchant', tags=['Merchant Account API'], dependencies=[]
)


