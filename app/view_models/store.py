from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import Request

from app.forms.store import CreateStoreForm, AddMerchantToStoreForm, UpdateStoreForm
from app.models.account import StoreStatusEnum
from app.models.store import StoreModel
from app.response.store import StoreInfoResponse
from app.view_models import BaseViewModel

__all__ = (
    'QueryStoreInfoViewModel',
    'CreateStoreViewModel',
    'AddMerchantToStoreViewModel',
    'QueryStoreListViewModel',
    'ReviewStoreViewModel',
    'UpdateStoreViewModel',
    'DeleteStoreViewModel',
)


class QueryStoreInfoViewModel(BaseViewModel):
    def __init__(self, store_id: str, request: Request):
        super().__init__(request=request)
        self.store_id = store_id

    async def before(self):
        await self.query_store_info()

    async def query_store_info(self):
        if not (store := await StoreModel.get(self.store_id)):
            self.not_found('store not found')
        self.operating_successfully(
            StoreInfoResponse(
                storeId=store.sid,
                name=store.name,
                email=store.email,
                status=store.status,
                description=store.description,
                merchant_count=store.merchant_count,
                good_count=store.good_count,
                createAt=store.createAt,
            )
        )


class CreateStoreViewModel(BaseViewModel):
    def __init__(self, form_data: CreateStoreForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.create_store()

    async def create_store(self):
        if self.form_data.email and not await StoreModel.find_one(StoreModel.email == self.form_data.email):
            store = StoreModel(
                name=self.form_data.name,
                email=self.form_data.email,
                description=self.form_data.description,
            )
            store = await StoreModel.insert(store)
            await store.update_fields({"$set": {"affiliation.merchantList": []}})
            await store.update_fields({"$set": {"affiliation.goodList": []}})
            self.operating_successfully('store created successfully')
        self.operating_failed('the store email has been registered')


class AddMerchantToStoreViewModel(BaseViewModel):
    def __init__(self, form_data: AddMerchantToStoreForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.add_merchant_to_store()

    async def add_merchant_to_store(self):
        if not (store := await StoreModel.get(self.form_data.storeId)):
            self.not_found('store not found')
        merchant_list = store.affiliation.merchantList
        merchant_list.add(self.form_data.merchantId)
        await store.update_fields({"$set": {"affiliation.merchantList": list(merchant_list)}})
        self.operating_successfully('merchant added to store successfully')


class QueryStoreListViewModel(BaseViewModel):
    def __init__(self, search: str, request: Request):
        super().__init__(request=request)
        self.search = search

    async def before(self):
        await self.query_store_list()

    async def query_store_list(self):
        store_list = await StoreModel.find(*self.generate_query_conditions()).to_list()
        res_list = [
            StoreInfoResponse(
                storeId=store.sid,
                name=store.name,
                email=store.email,
                status=store.status,
                description=store.description,
                merchant_count=store.merchant_count,
                good_count=store.good_count,
                createAt=store.createAt,
            ) for store in store_list
        ]
        self.operating_successfully(res_list)

    def generate_query_conditions(self):
        conditions = []
        if self.search:
            conditions.append(
                Or(
                    RegEx(StoreModel.name, self.search),
                    RegEx(StoreModel.email, self.search)
                )
            )
        conditions.append(StoreModel.deleted == False)
        return conditions


class ReviewStoreViewModel(BaseViewModel):
    def __init__(self, store_id: str, request: Request):
        super().__init__(request=request)
        self.store_id = store_id

    async def before(self):
        await self.review_store()

    async def review_store(self):
        if not (store := await StoreModel.get(self.store_id)):
            self.not_found('store not found')
        await store.update_fields(
            status=StoreStatusEnum.Approved
        )
        self.operating_successfully('store reviewed successfully')


class UpdateStoreViewModel(BaseViewModel):
    def __init__(self, form_data: UpdateStoreForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.update_store()

    async def update_store(self):
        if not (store := await StoreModel.get(self.form_data.storeId)):
            self.not_found('store not found')
        await store.update_fields(
            name=self.form_data.name,
            email=self.form_data.email,
            status=self.form_data.status,
            description=self.form_data.description,
        )
        self.operating_successfully('store updated successfully')


class DeleteStoreViewModel(BaseViewModel):
    def __init__(self, store_id: str, request: Request):
        super().__init__(request=request)
        self.store_id = store_id

    async def before(self):
        await self.delete_store()

    async def delete_store(self):
        if not (store := await StoreModel.get(self.store_id)):
            self.not_found('store not found')
        await store.update_fields(
            deleted=True
        )
        self.operating_successfully('store deleted successfully')
