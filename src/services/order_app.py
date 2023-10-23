from functools import lru_cache

import datetime

from fastapi import Depends, HTTPException, status

from sqlalchemy import select, text, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_app

from .base import BaseService
from models import Purchase, OrderApp


class OrderAppService(BaseService):

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderApp]:
        query = select(Purchase)\
            .filter(and_(
                func.date(Purchase.created_at) >= datetime.date.fromisoformat(start_period),
                func.date(Purchase.created_at) <= datetime.date.fromisoformat(end_period)
            ))
        data = (await self.db_session.execute(query)).scalars().all()
        return [OrderApp.model_validate(item) for item in data]

    async def get_item_by_id(self, pk: str) -> OrderApp:
        query = select(Purchase).where(Purchase.id == pk)
        data = (await self.db_session.execute(query)).scalar()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='App Item not foundS')
        return OrderApp.model_validate(data)


@lru_cache
def get_order_app_service(db_session: AsyncSession = Depends(get_async_session_app)) -> OrderAppService:
    return OrderAppService(db_session)