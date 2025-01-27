from functools import lru_cache
from typing import Any

from fastapi import Depends

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from models import Deposit, OrderServer


class OrderServerService(BaseService):

    model_db_class = Deposit

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderServer]:
        query = select(Deposit)\
            .filter(and_(
                func.date(Deposit.time) >= start_period,
                func.date(Deposit.time) <= end_period
            ))
        data = (await self.db_session.execute(query)).scalars().all()
        return [OrderServer.model_validate(item) for item in data]

    async def get_item_by_id(self, pk: int) -> OrderServer:
        item = await self._get_db_item_by_field(self.model_db_class, 'id', pk)
        return OrderServer.model_validate(item)
    
    async def update_item(self, search_field: str, field_value: Any, new_data: dict) -> OrderServer:
        item = await self._get_db_item_by_field(self.model_db_class, search_field, field_value)
        
        for key, value in new_data.items():
            setattr(item, key, value)

        await self.db_session.commit()

        return OrderServer.model_validate(item)


@lru_cache
def get_order_server_service(db_session: AsyncSession = Depends(get_async_session_server)) -> OrderServerService:
    return OrderServerService(db_session)