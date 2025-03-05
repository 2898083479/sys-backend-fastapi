import abc

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
        # return self

    async def __aenter__(self):
        try:
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

    def request_timeout(self, msg: str):
        self.code = ResponseStatusCodeEnum.REQUEST_TIMEOUT.value
        self.message = get_response_message(ResponseStatusCodeEnum.REQUEST_TIMEOUT)
        self.data = msg
        raise ViewModelRequestException(message=msg)
