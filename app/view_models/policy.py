__all__ = (
    'QueryOnePolicyViewModel',

)

from fastapi import Request

from app.models.policy import PolicyModel
from app.response.policy import QueryPolicyResponse
from app.view_models import BaseViewModel


class QueryOnePolicyViewModel(BaseViewModel):
    def __init__(self, policy_id: str, request: Request):
        super().__init__(request=request)
        self.policy_id = policy_id

    async def before(self):
        await self.get_policy_by_id()

    async def get_policy_by_id(self):
        if not (policy := await PolicyModel.get(self.policy_id)):
            self.not_found('Policy not found')
        response = QueryPolicyResponse(
            policyId=policy.sid,
            name=policy.name,
            status=policy.status,
            description=policy.description,
            startAt=policy.startAt,
            endAt=policy.endAt,
            createAt=policy.createAt,
            updateAt=policy.updateAt
        )
        self.operating_successfully(response)
