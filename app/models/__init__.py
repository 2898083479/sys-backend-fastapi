from datetime import datetime
from beanie import Document
from pydantic import Field
from beanie.odm.operators.update.general import Set as _Set
from app.config.setting import get_settings
from app.utils.encrypt import encrypt, decrypt
from typing import Any

__all__ = (
    
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
        if encrypt_fields and isinstance(encrypt_fields, dict):
            kwargs.update({key: encrypt(val, get_settings().ENCRYPT_KEY) for key, val in encrypt_fields.items()})

        kwargs.update(updatedAt=datetime.now())
        await self.set(kwargs)

    async def get_encrypted_fields(self, encrypted_field: str) -> Any | None:
        if not getattr(self, encrypted_field):
            return None
        return decrypt(getattr(self, encrypted_field), get_settings().ENCRYPT_KEY)
    