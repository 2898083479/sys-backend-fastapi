from app.models.account.user import UserModel
from app.response.account import UserInfoResponse
from app.view_models import BaseViewModel

__all__ = (
    'GetUserInfoViewModel',
    'GetUserInfoOneViewModel',
)


class GetUserInfoViewModel(BaseViewModel):
    def __init__(self):
        super().__init__()

    async def before(self):
        await self.get_user_info()

    async def get_user_info(self):
        self.operating_successfully(
            UserInfoResponse(
                id='1',
                name='ethan',
                email='ethan@gmail.com'
            )
        )


class GetUserInfoOneViewModel(BaseViewModel):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    async def before(self):
        await self.get_user_info()

    async def get_user_info(self):
        if not (user := await UserModel.get(self.user_id)):
            self.operating_failed('user not found')
        self.operating_successfully(
            UserInfoResponse(
                id=user.sid,
                name=user.name,
                email=user.email
            )
        )
