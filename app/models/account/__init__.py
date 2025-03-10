__all__ = (
    'MerchantStatusEnum'
)

from enum import StrEnum


class MerchantStatusEnum(StrEnum):
    inactive = '未激活'
    Pending = '待審核'
    Approved = '已批准'
    Rejected = '已拒絕'
