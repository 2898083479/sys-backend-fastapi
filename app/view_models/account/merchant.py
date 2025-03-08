from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import Request

from app.forms.account.merchant import UpdateMerchantForm
from app.models.account.merchant import MerchantModel
from app.response.merchant import MerchantInfoResponse
from app.view_models import BaseViewModel

__all__ = (
    'QueryMerchantByIdViewMode',
    'UpdateMerchantViewModel',
)


class QueryMerchantByIdViewMode(BaseViewModel):
    def __init__(self, merchant_id: str, request: Request):
        super().__init__()
        self.merchant_id = merchant_id
        self.request = request

    async def before(self):
        await self.get_merchant_by_id()

    async def get_merchant_by_id(self):
        token_data = self.request.headers.get('Authorization')
        token = token_data.replace('Bearer ', '')
        await self.verify_token(token)
        if not (merchant := await MerchantModel.get(self.merchant_id)):
            self.operating_failed('merchant not found')
        self.operating_successfully(MerchantInfoResponse(
            merchantId=merchant.sid,
            name=merchant.name,
            email=merchant.email,
            status=merchant.status,
            createdAt=merchant.createAt,
            updatedAt=merchant.updateAt,
        ))


class UpdateMerchantViewModel(BaseViewModel):
    def __init__(self, form_data: UpdateMerchantForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.update_merchant()

    async def update_merchant(self):
        token = self.request.headers.get('Authorization')
        token = token.replace('Bearer ', '')
        await self.verify_token(token)
        if not (merchant := await MerchantModel.get(self.form_data.merchantId)):
            self.not_found('merchant not found')
        await merchant.update_fields(
            name=self.form_data.name,
            email=self.form_data.email,
            status=self.form_data.status,
        )
        self.operating_successfully('merchant updated successfully')


class QueryMerchantListViewModel(BaseViewModel):
    def __init__(self, search: str, request: Request):
        super().__init__(request=request)
        self.search = search

    async def before(self):
        await self.query_merchant_list()

    async def query_merchant_list(self):
        await self.verify_token(
            self.request.headers.get('Authorization').replace('Bearer ', '')
        )
        condition = []
        if self.search:
            condition.append(Or(
                RegEx(MerchantModel.name, self.search),
                RegEx(MerchantModel.email, self.search)
            ))
        merchant_list = await MerchantModel.find(**condition).to_list()
        res_list = [
            MerchantInfoResponse(
                merchantId=merchant.sid,
                name=merchant.name,
                email=merchant.email,
                status=merchant.status,
                createdAt=merchant.createAt,
                updatedAt=merchant.updateAt,
            ) for merchant in merchant_list
        ]
        self.operating_successfully(res_list)
