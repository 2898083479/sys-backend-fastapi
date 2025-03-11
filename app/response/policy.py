__all__ = (
    'QueryPolicyResponse'
)

from datetime import datetime

from pydantic import Field, BaseModel


class QueryPolicyResponse(BaseModel):
    policyId: str = Field(..., description='Policy id')
    name: str = Field(..., description='Policy Name')
    status: str = Field(..., description='Policy Status')
    description: str = Field(..., description='Policy Description')
    startAt: datetime = Field(..., description='Start date')
    endAt: datetime = Field(..., description='End date')
    createAt: datetime = Field(..., description='Create date')
    updateAt: datetime = Field(..., description='Update date')
