from enum import Enum
from functools import lru_cache
from typing import Generic, TypeVar

from pydantic import Field, BaseModel

T = TypeVar('T')

__all__ = (
    'ResponseModel',
    'ResponseStatusCodeEnum',
    'get_response_message',
)


class ResponseStatusCodeEnum(Enum):
    OPERATING_SUCCESSFULLY = '0000'
    EMPTY_CONTENT = '0001'
    NOTHING_CHANGED = '0002'
    OPERATING_FAILED = '0003'
    ILLEGAL_PARAMETERS = '0004'
    UNAUTHORIZED = '0005'
    FORBIDDEN = '0006'
    NOT_FOUND = '0007'
    METHOD_NOT_ALLOWED = '0008'
    REQUEST_TIMEOUT = '0009'
    SYSTEM_ERROR = '1111'


class ResponseMessageMap:
    OPERATING_SUCCESSFULLY = "Operating successfully"
    EMPTY_CONTENT = "Empty Content"
    NOTHING_CHANGED = "Nothing Changed"
    OPERATING_FAILED = "Operating Failed"
    ILLEGAL_PARAMETERS = "Illegal Parameters"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "Not Found"
    METHOD_NOT_ALLOWED = "Method Not Allowed"
    REQUEST_TIMEOUT = "Request Timeout"
    SYSTEM_ERROR = "System Error"


class ResponseModel(BaseModel, Generic[T]):
    category: str = Field(..., description='Response of Platform')
    code: str = Field(..., description='Response Code')
    message: str = Field(..., description='Response Message')
    data: T = Field(..., description='Response data')


@lru_cache()
def get_response_message(status_code: ResponseStatusCodeEnum | str):
    rm_map = ResponseMessageMap()
    if isinstance(status_code, ResponseStatusCodeEnum):
        return getattr(rm_map, status_code.name, 'Undefined status code')
    status_code_enum = ResponseStatusCodeEnum(status_code)
    return getattr(rm_map, status_code_enum.name, status_code)
