__all__ = (
    'MerchantStatusEnum',
    'StoreStatusEnum'
)

from enum import StrEnum


class MerchantStatusEnum(StrEnum):
    inactive = '未激活'
    Pending = '待審核'
    Approved = '已批准'
    Rejected = '已拒絕'


class StoreStatusEnum(StrEnum):
    Pending = '待審核'
    Approved = '已批准'
    Rejected = '已拒絕'
