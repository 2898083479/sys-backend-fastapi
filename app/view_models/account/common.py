from app.config.setting import get_settings
from app.forms.account.common import LoginForm, RegisterForm
from app.libs.custom import decrypt, encrypt
from app.models.account.admin import AdminModel
from app.models.account.merchant import MerchantModel
from app.response.common import LoginSuccessResponse
from app.view_models import BaseViewModel

__all__ = (
    'AdminLoginViewModel',
    'UserRegisterViewModel',
)


class AdminLoginViewModel(BaseViewModel):
    def __init__(self, form_data: LoginForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.login()

    async def login(self):
        user = None
        match self.form_data.identity:
            case 0:
                if not (user := await AdminModel.find_one(AdminModel.email == self.form_data.email)):
                    self.operating_failed('the account is common user or not registered')
            case 1:
                if not (user := await MerchantModel.find_one(MerchantModel.email == self.form_data.email)):
                    self.operating_failed('not registered')
        password = decrypt(user.password, get_settings().ENCRYPT_KEY)
        if password != self.form_data.password:
            self.operating_failed('password error')
        self.operating_successfully(LoginSuccessResponse(
            userId=user.sid,
            name=user.name,
            email=user.email,
            token=self.create_token(user.email, user.sid)
        ))


class UserRegisterViewModel(BaseViewModel):
    def __init__(self, form_data: RegisterForm):
        super().__init__()
        self.form_data = form_data

    async def before(self):
        await self.register()

    async def register(self):
        if self.form_data.email and await MerchantModel.find_one(MerchantModel.email == self.form_data.email):
            self.operating_failed('email already exists')
        merchant = MerchantModel(
            name=self.form_data.name,
            email=self.form_data.email,
            password=encrypt(self.form_data.password, get_settings().ENCRYPT_KEY),
            identity=self.form_data.identity
        )
        await MerchantModel.insert(merchant)
        self.operating_successfully('register successfully')
