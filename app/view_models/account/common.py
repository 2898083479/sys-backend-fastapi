from app.forms.account.common import LoginForm, RegisterForm
from app.models.account.admin import AdminModel
from app.response.common import LoginSuccessResponse
from app.view_models import BaseViewModel
from app.libs.custom import decrypt
from app.config.setting import get_settings

__all__ = (
    'AdminLoginViewModel',
)


class AdminLoginViewModel(BaseViewModel):
    def __init__(self, form_data: LoginForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.login()

    async def login(self):
        if not (user := await AdminModel.find_one(AdminModel.email == self.form_data.email)):
            self.operating_failed('the email was not been registered')

        password = decrypt(user.password, get_settings().ENCRYPT_KEY)
        if password != self.form_data.password:
            self.operating_failed('password error')
        token = self.create_token(user.email, user.sid)
        self.operating_successfully(LoginSuccessResponse(
            userId=user.sid,
            name=user.name,
            email=user.email,
            token=token
        ))


class AdminRegisterViewModel(BaseViewModel):
    def __init__(self, form_data: RegisterForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.register()

    async def register(self):
        pass
