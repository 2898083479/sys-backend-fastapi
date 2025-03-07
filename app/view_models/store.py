from fastapi import Request

from app.view_models import BaseViewModel

__all__ = (

)


class QueryStoreInfo(BaseViewModel):
    def __init__(self, store_id: str, request: Request):
        super().__init__(request=request)
        self.store_id = store_id

    async def before(self):
        await self.query_store_info()

    async def query_store_info(self):
        pass
