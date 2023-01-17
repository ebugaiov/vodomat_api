from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import get_async_session_server

from models import Avtomat
from models import Street


class AvtomatService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_all(self):
        query = select(Avtomat)\
            .join(Avtomat.street)\
            .options(joinedload(Avtomat.street).options(joinedload(Street.city)), joinedload(Avtomat.route))\
            .order_by(Street.street, Avtomat.house)
        result = await self.db_session.execute(query)
        return result.scalars().all()


@lru_cache
def get_avtomat_service(db_session: AsyncSession = Depends(get_async_session_server)) -> AvtomatService:
    return AvtomatService(db_session)
