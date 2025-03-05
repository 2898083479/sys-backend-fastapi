from fastapi import Request

from app.models.account.admin import AdminModel
from app.response.account import AdminInfoResponse
from app.view_models import BaseViewModel

__all__ = (
    'GetAdminInfoViewModel',
    'GetAdminInfoByIdViewModel',
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
