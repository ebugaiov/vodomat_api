from functools import lru_cache

from fastapi import Depends, HTTPException, status

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from models import Deposit, OrderServer


class OrderServerService(BaseService):

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderServer]:
        query = select(Deposit)\
            .filter(and_(
                func.date(Deposit.time) >= start_period,
                func.date(Deposit.time) <= end_period
            ))
        data = (await self.db_session.execute(query)).scalars().all()
        return [OrderServer.model_validate(item) for item in data]

    async def get_item_by_id(self, pk: int) -> OrderServer:
        query = select(Deposit).where(Deposit.id == pk)
        data = (await self.db_session.execute(query)).scalar()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Server Item not found')
        return OrderServer.model_validate(data)


@lru_cache
def get_order_server_service(db_session: AsyncSession = Depends(get_async_session_server)) -> OrderServerService:
    return OrderServerService(db_session)