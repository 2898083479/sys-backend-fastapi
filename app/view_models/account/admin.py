from fastapi import Request

from app.response.account import AdminInfoResponse
from app.view_models import BaseViewModel

__all__ = (
    'GetAdminInfoViewModel',
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
