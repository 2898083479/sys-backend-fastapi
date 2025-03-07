import abc
import time

import jwt
from fastapi import Request
from jenkins import TimeoutException

from app.config.setting import get_settings
from app.response import ResponseModel, ResponseStatusCodeEnum, get_response_message

__all__ = (
    'BaseViewModel',
)


class ViewModelException(Exception):
    pass


class ViewModelRequestException(ViewModelException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BaseViewModel:
    def __init__(
            self, request: Request = None,
            need_auth: bool = True
    ):
        self.request: Request = request
        self.token = ''
        self.user_info = {}
        self.need_auth = need_auth
        self.code = ResponseStatusCodeEnum.OPERATING_SUCCESSFULLY.value
        self.message = get_response_message(ResponseStatusCodeEnum.OPERATING_SUCCESSFULLY)
        self.data = None

    def __enter__(self):
        try:
            self.before()
        except ViewModelRequestException:
            pass
        return ResponseModel(
            category=get_settings().APP_NO,
            code=self.code,
            message=self.message,
            data=self.data
        )

    async def __aenter__(self):
        try:
            if self.need_auth and self.request.url.path not in [
                '/account/common/login', '/account/common/register'
            ]:
                await self.verify_token(self.request.headers.get('Authorization').replace('Bearer ', ''))
            await self.before()
        except TimeoutException as e:
            self.request_timeout(str(e))
        except ViewModelRequestException:
            pass
        return ResponseModel(
            category=get_settings().APP_NO,
            code=self.code,
            message=self.message,
            data=self.data
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.after()
        if exc_type:
            print(f'exc_type: {exc_type}')
        return True

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.after()
        if exc_type:
            print(f'exc_type: {exc_type}')
        return True

    @abc.abstractmethod
    async def before(self):
        pass

    async def after(self):
        pass

    def operating_successfully(self, data: str | dict | list):
        self.code = ResponseStatusCodeEnum.OPERATING_SUCCESSFULLY.value
        self.message = get_response_message(ResponseStatusCodeEnum.OPERATING_SUCCESSFULLY)
        self.data = data
        raise ViewModelRequestException(message=data)

    def operating_failed(self, data: str | dict | list):
        self.code = ResponseStatusCodeEnum.OPERATING_FAILED.value
        self.message = get_response_message(ResponseStatusCodeEnum.OPERATING_FAILED)
        self.data = data
        raise ViewModelRequestException(message=data)

    def not_found(self, data: str | dict | list):
        self.code = ResponseStatusCodeEnum.NOT_FOUND.value
        self.message = get_response_message(ResponseStatusCodeEnum.NOT_FOUND)
        self.data = data
        raise ViewModelRequestException(message=data)

    def request_timeout(self, msg: str):
        self.code = ResponseStatusCodeEnum.REQUEST_TIMEOUT.value
        self.message = get_response_message(ResponseStatusCodeEnum.REQUEST_TIMEOUT)
        self.data = msg
        raise ViewModelRequestException(message=msg)

    def unauthorized(self, data: str | dict | list):
        self.code = ResponseStatusCodeEnum.UNAUTHORIZED.value
        self.message = get_response_message(ResponseStatusCodeEnum.UNAUTHORIZED)
        self.data = data
        raise ViewModelRequestException(message=data)

    @staticmethod
    def create_token(email, user_id: str):
        payload = {
            'userId': user_id,
            'email': email,
            'exp': int(time.time()) + 60 * 60 * 24
        }
        cookie_key = get_settings().COOKIE_KEY
        token = jwt.encode(payload, cookie_key, algorithm='HS256')
        return token

    async def verify_token(self, token: str):
        try:
            result = jwt.decode(token, get_settings().COOKIE_KEY, algorithms=['HS256']) or {}
            if not result:
                self.unauthorized('please pass the token in the authorization header to proceed')
            if not result.get('userId'):
                self.unauthorized('invalid token')
            return result
        except jwt.ExpiredSignatureError:
            self.unauthorized('token expired, Please login again to continue')
