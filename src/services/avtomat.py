from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import get_async_session_server

from .base import BaseService
from models import Avtomat
from models import Street


class AvtomatService(BaseService):

    async def get_all(self) -> list[Avtomat]:
        query = select(Avtomat)\
            .join(Avtomat.street)\
            .options(joinedload(Avtomat.street).options(joinedload(Street.city)), joinedload(Avtomat.route))\
            .order_by(Street.street, Avtomat.house)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_item_by_avtomat_number(self, avtomat_number: int) -> Avtomat:
        query = select(Avtomat)\
            .options(joinedload(Avtomat.street).options(joinedload(Street.city)), joinedload(Avtomat.route))\
            .where(Avtomat.avtomat_number == avtomat_number)
        data = (await self.db_session.execute(query)).scalar()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return data


@lru_cache
def get_avtomat_service(db_session: AsyncSession = Depends(get_async_session_server)) -> AvtomatService:
    return AvtomatService(db_session)
