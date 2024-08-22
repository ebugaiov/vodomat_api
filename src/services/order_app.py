from functools import lru_cache
from typing import Any

import datetime

from fastapi import Depends, HTTPException, status

from sqlalchemy import select, text, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from db import get_async_session_app

from .base import BaseService
from models import Purchase, OrderApp


class OrderAppService(BaseService):

    model_db_class = Purchase

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderApp]:
        query = select(Purchase)\
            .filter(and_(
                func.date(Purchase.created_at) >= datetime.date.fromisoformat(start_period),
                func.date(Purchase.created_at) <= datetime.date.fromisoformat(end_period)
            ))
        data = (await self.db_session.execute(query)).scalars().all()
        return [OrderApp.model_validate(item) for item in data]

    async def get_item_by_id(self, pk: str) -> OrderApp:
        return OrderApp.model_validate(await self._get_db_item_by_field(self.model_db_class, 'pk', pk))
    
    async def update_item(self, field: str, field_value: Any, new_data: dict) -> OrderApp:
        item = await self._get_db_item_by_field(self.model_db_class, field, field_value)
        
        for key, value in new_data.items():
            setattr(item, key, value)

        await self.db_session.commit()

        return OrderApp.model_validate(item)


@lru_cache
def get_order_app_service(db_session: AsyncSession = Depends(get_async_session_app)) -> OrderAppService:
    return OrderAppService(db_session)