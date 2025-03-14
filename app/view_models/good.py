__all__ = (
    'CreateGoodViewModel',
    'QueryGoodViewModel',
    'QueryGoodListViewModel',
    'UpdateGoodViewModel',
    'DeleteGoodViewModel',
)

from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import Request

from app.forms.good import CreateGoodForm, UpdateGoodForm
from app.models.good import GoodModel
from app.response.good import QueryGoodResponse
from app.view_models import BaseViewModel


class CreateGoodViewModel(BaseViewModel):
    def __init__(self, form_data: CreateGoodForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.create_good()

    async def create_good(self):
        if not (good := await GoodModel.find_one(*self.generate_query_condition())):
            good = GoodModel(
                name=self.form_data.name,
                source=self.form_data.source,
                category=self.form_data.category,
                goodPrice=self.form_data.goodPrice,
                goodCount=self.form_data.goodCount
            )
            await GoodModel.insert(good)
            self.operating_successfully('Good created successfully')

        await good.update_fields(
            goodPrice=self.form_data.goodPrice,
            goodCount=good.goodCount + self.form_data.goodCount
        )
        self.operating_successfully('Good created successfully')

    def generate_query_condition(self):
        conditions = []
        if self.form_data.name:
            conditions.append(GoodModel.name == self.form_data.name)
        if self.form_data.source:
            conditions.append(GoodModel.source == self.form_data.source)
        if self.form_data.category:
            conditions.append(GoodModel.category == self.form_data.category)
        return conditions


class QueryGoodViewModel(BaseViewModel):
    def __init__(self, good_id: str, request):
        super().__init__(request=request)
        self.good_id = good_id

    async def before(self):
        await self.query_good()

    async def query_good(self):
        if not (good := await GoodModel.get(self.good_id)):
            self.not_found('Good not found')
        if good.deleted:
            self.operating_failed('The good was deleted')
        self.operating_successfully(
            QueryGoodResponse(
                goodId=good.sid,
                name=good.name,
                source=good.source,
                category=good.category,
                price=good.goodPrice,
                count=good.goodCount,
                createAt=good.createAt,
                policyList=good.affiliation.policyList if good.affiliation else set()
            )
        )


class QueryGoodListViewModel(BaseViewModel):
    def __init__(self, search: str, request: Request):
        super().__init__(request=request)
        self.search = search

    async def before(self):
        await self.query_good_list()

    async def query_good_list(self):
        good_list = await GoodModel.find(*self.generate_query_conditions()).to_list()
        res_list = [
            QueryGoodResponse(
                goodId=good.sid,
                name=good.name,
                source=good.source,
                category=good.category,
                price=good.goodPrice,
                count=good.goodCount,
                createAt=good.createAt,
                policyList=good.affiliation.policyList if good.affiliation else set()
            ) for good in good_list
        ]
        self.operating_successfully(res_list)

    def generate_query_conditions(self):
        conditions = []
        if self.search:
            conditions.append(Or(
                RegEx(GoodModel.name, self.search)
            ))
        conditions.append(GoodModel.deleted == False)
        return conditions


class UpdateGoodViewModel(BaseViewModel):
    def __init__(self, form_data: UpdateGoodForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.update_good()

    async def update_good(self):
        if not (good := await GoodModel.get(self.form_data.goodId)):
            self.not_found('Good not found')
        await good.update_fields(
            name=self.form_data.name,
            source=self.form_data.source,
            category=self.form_data.category,
            goodPrice=self.form_data.price,
            goodCount=self.form_data.count
        )
        self.operating_successfully('Good updated successfully')


class DeleteGoodViewModel(BaseViewModel):
    def __init__(self, good_id: str, request: Request):
        super().__init__(request=request)
        self.good_id = good_id

    async def before(self):
        await self.delete_good()

    async def delete_good(self):
        if not (good := await GoodModel.get(self.good_id)):
            self.not_found('Good not found')
        await good.update_fields(
            deleted=True
        )
        self.operating_successfully('Good deleted successfully')
