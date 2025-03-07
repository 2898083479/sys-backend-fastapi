from fastapi import HTTPException, Request
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.config.setting import get_settings
from app.models import BaseDBModel
from app.response import ResponseModel, ResponseStatusCodeEnum, get_response_message
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from beanie import init_beanie

__all__ = (
    'create_app',
)

def create_app():
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*']
    )
    register_http_exception_handlers(app)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Load Core Application')
    result = await register_routers(app)
    if not result:
        print('Start Failed')
    mongo_client = await initialize_mongodb_client()
    await init_db(mongo_client)
    print('Start Success')
    yield
    mongo_client.close()
    print('Shutdown Core Application')


async def register_routers(app: FastAPI):
    # 導入所需的路由
    from app.api.account import router as account_router
    from app.api.store import router as store_router
    # app.include_router()
    app.include_router(account_router)
    app.include_router(store_router)
    return True


async def initialize_mongodb_client():
    return AsyncIOMotorClient(
        host=get_settings().MONGODB_URI,
        port=get_settings().MONGODB_PORT,
        username=get_settings().MONGODB_USERNAME,
        password=get_settings().MONGODB_PASSWORD,
    )


async def init_db(mongo_client: AsyncIOMotorClient):
    # 導入模型
    import app.models.account.admin as admin_model
    import app.models.account.user as user_model
    import app.models.store as store_model
    import app.models.account.merchant as merchant_model
    await init_beanie(
        database=getattr(mongo_client, get_settings().MONGODB_DB),
        document_models=[
            # *load_models_class
            *load_models_class(admin_model),
            *load_models_class(user_model),
            *load_models_class(store_model),
            *load_models_class(merchant_model),
        ]
    )


def load_models_class(module):
    class_list = []
    for model in module.__all__:
        module_class = getattr(module, model)
        if module_class and issubclass(module_class, BaseDBModel):
            class_list.append(module_class)
    return class_list


def register_http_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        response_data = ResponseModel(
            category='101',
            code=ResponseStatusCodeEnum.OPERATING_FAILED.value,
            message=get_response_message(ResponseStatusCodeEnum.OPERATING_FAILED),
            data=exc.detail
        )
        if exc.status_code in [401]:
            response_data = ResponseModel(
                category='101',
                code=ResponseStatusCodeEnum.UNAUTHORIZED.value,
                message=get_response_message(ResponseStatusCodeEnum.UNAUTHORIZED),
                data=exc.detail
            )
        return JSONResponse(status_code=200, content=response_data.model_dump())
