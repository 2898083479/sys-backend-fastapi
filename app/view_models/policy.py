__all__ = (
    'QueryOnePolicyViewModel',
    'CreatePolicyViewModel',
    'QueryPolicyListViewModel',
    'UpdatePolicyViewModel',
    'TogglePolicyViewModel',
)

from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import Request

from app.forms.policy import CreatePolicyForm, UpdatePolicyForm
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


class CreatePolicyViewModel(BaseViewModel):
    def __init__(self, form_data: CreatePolicyForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.create_policy()

    async def create_policy(self):
        if await PolicyModel.find_one(PolicyModel.name == self.form_data.name):
            self.operating_failed('Policy name already exists')
        policy = PolicyModel(
            name=self.form_data.name,
            status=self.form_data.status,
            description=self.form_data.description,
            startAt=self.form_data.startAt,
            endAt=self.form_data.endAt
        )
        await PolicyModel.insert(policy)
        self.operating_successfully('Policy created successfully')


class QueryPolicyListViewModel(BaseViewModel):
    def __init__(self, good_id: str, search: str, request: Request):
        super().__init__(request=request)
        self.search = search
        self.good_id = good_id

    async def before(self):
        await self.query_policy_list()

    async def query_policy_list(self):
        policy_list = await PolicyModel.find(*self.generate_query_conditions()).to_list()
        res_list = [
            QueryPolicyResponse(
                policyId=policy.sid,
                name=policy.name,
                status=policy.status,
                description=policy.description,
                startAt=policy.startAt,
                endAt=policy.endAt,
                createAt=policy.createAt,
                updateAt=policy.updateAt
            ) for policy in policy_list
        ]
        self.operating_successfully(res_list)

    def generate_query_conditions(self):
        conditions = []
        if self.good_id:
            conditions.append(
                PolicyModel.affiliation.goodId == self.good_id
            )
        if self.search:
            conditions.append(
                Or(
                    RegEx(PolicyModel.name, self.search),
                )
            )
        conditions.append(PolicyModel.deleted == False)
        return conditions


class UpdatePolicyViewModel(BaseViewModel):
    def __init__(self, form_data: UpdatePolicyForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.update_policy()

    async def update_policy(self):
        if not (policy := await PolicyModel.get(self.form_data.policyId)):
            self.not_found('Policy not found')
        await policy.update_fields(
            name=self.form_data.name,
            description=self.form_data.description,
            startAt=self.form_data.startAt,
            endAt=self.form_data.endAt
        )
        self.operating_successfully('Policy updated successfully')


class TogglePolicyViewModel(BaseViewModel):
    def __init__(self, policy_id: str, request: Request):
        super().__init__(request=request)
        self.policy_id = policy_id

    async def before(self):
        await self.toggle_policy()

    async def toggle_policy(self):
        if not (policy := await PolicyModel.get(self.policy_id)):
            self.not_found('Policy not found')
        match policy.status:
            case '啟用':
                await policy.update_fields(status='未啟用')
            case '未啟用':
                await policy.update_fields(status='啟用')
        self.operating_successfully('Policy status toggled successfully')
