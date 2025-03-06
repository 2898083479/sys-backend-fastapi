from datetime import datetime
from typing import Any

from beanie import Document, after_event, Update
from beanie.odm.operators.update.general import Set as _Set
from pydantic import Field, EmailStr

__all__ = (
    'Set',
    'BaseDBModel',
    'BaseUserModel'
)


class Set(_Set):
    def __init__(self, expression):
        super().__init__(expression | {'updateAt': datetime.now()})


class BaseDBModel(Document):
    createAt: datetime = Field(default_factory=lambda: datetime.now())
    updateAt: datetime = Field(default_factory=lambda: datetime.now())

    def keys(self):
        return list(self.model_fields.keys())

    def __getitem__(self, item):
        return getattr(self, item) if item != 'id' else str(self.id)

    @property
    def sid(self) -> str:
        return str(self.id)

    @after_event(Update)
    async def refresh_update_at(self):
        self.updateAt = datetime.now()

    async def update_fields(self, encrypt_fields: dict = None, **kwargs):
        await self.set(kwargs)

    async def get_encrypted_fields(self, encrypted_field: str) -> Any | None:
        if not getattr(self, encrypted_field):
            return None


class BaseUserModel(BaseDBModel):
    name: str = Field(..., description='user name')
    email: EmailStr = Field(..., description='user email')
    password: str = Field(..., description='user password')
    identity: int = Field(..., description='user identity: 0-admin, 1-common_user')
