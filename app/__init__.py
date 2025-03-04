from fastapi import HTTPException, Request

__all__ = (
    'create_app',
)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.response import ResponseModel, ResponseStatusCodeEnum, get_response_message


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
    print('Start Success')
    yield
    print('Shutdown Core Application')


async def register_routers(app: FastAPI):
    # 導入所需的路由
    from app.api.account import router as account_router
    # app.include_router()
    app.include_router(account_router)
    return True


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
