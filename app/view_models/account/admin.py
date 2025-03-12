from fastapi import Request

from app.forms.account.admin import CreateAdminForm, UpdateAdminForm
from app.forms.account.common import LoginForm
from app.models.account.admin import AdminModel
from app.response.account import AdminInfoResponse
from app.response.common import AdminLoginResponse
from app.view_models import BaseViewModel

__all__ = (
    'GetAdminInfoViewModel',
    'GetAdminInfoByIdViewModel',
    'CreateAdminViewModel',
    'UpdateAdminViewModel',
    'DeleteAdminViewModel',
    'QueryAdminListViewModel',
    'AdminLoginViewModel'
)


class GetAdminInfoViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request=request)

    async def before(self):
        await self.get_admin_info()

    async def get_admin_info(self):
        response = AdminInfoResponse(
            id='1',
            name='ethan',
            email='ethan@example.com',
        )
        self.operating_successfully(response)


class GetAdminInfoByIdViewModel(BaseViewModel):
    def __init__(self, admin_id: str, request: Request):
        super().__init__(request=request)
        self.admin_id = admin_id

    async def before(self):
        await self.get_admin_info_by_id()

    async def get_admin_info_by_id(self):
        if not (admin := await AdminModel.get(self.admin_id)):
            self.operating_failed('admin not found')
        self.operating_successfully(
            AdminInfoResponse(
                id=admin.sid,
                name=admin.name,
                email=admin.email
            )
        )


class CreateAdminViewModel(BaseViewModel):
    def __init__(self, form_data: CreateAdminForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.create_admin()

    async def create_admin(self):
        if self.form_data.email and not await AdminModel.find_one(AdminModel.email == self.form_data.email):
            await AdminModel.insert_one(AdminModel(
                name=self.form_data.name,
                email=self.form_data.email
            ))
            self.operating_successfully('admin created successfully')
        self.operating_failed('the email has already been')


class UpdateAdminViewModel(BaseViewModel):
    def __init__(self, form_data: UpdateAdminForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.update_admin()

    async def update_admin(self):
        if not (admin := await AdminModel.get(self.form_data.adminId)):
            self.not_found('admin not found')
        await admin.update_fields(
            name=self.form_data.name,
            email=self.form_data.email
        )
        self.operating_successfully('admin updated successfully')


class DeleteAdminViewModel(BaseViewModel):
    def __init__(self, admin_id: str):
        super().__init__()
        self.admin_id = admin_id

    async def before(self):
        await self.delete_admin()

    async def delete_admin(self):
        if not (admin := await AdminModel.get(self.admin_id)):
            self.not_found('admin not found')
        await admin.update_fields(
            deleted=True
        )
        self.operating_successfully('admin deleted successfully')


class QueryAdminListViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request=request)

    async def before(self):
        await self.query_admin_list()

    async def query_admin_list(self):
        admin_list = await AdminModel.find().to_list()
        res_list = [
            AdminInfoResponse(
                id=admin.sid,
                name=admin.name,
                email=admin.email
            ) for admin in admin_list
        ]
        self.operating_successfully(res_list)


class AdminLoginViewModel(BaseViewModel):
    def __init__(self, form_data: LoginForm, request: Request):
        super().__init__(request=request)
        self.form_data = form_data

    async def before(self):
        await self.admin_login()

    async def admin_login(self):
        if not (admin := await AdminModel.find_one(AdminModel.email == self.form_data.email)):
            self.operating_failed('the account is not registered')
        self.operating_successfully(
            AdminLoginResponse(
                accessToken=self.create_token(admin.email, admin.sid)
            )
        )