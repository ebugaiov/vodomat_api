from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import get_async_session_server

from models import Street


class StreetService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self):
        query = select(Street).options(joinedload(Street.city)).order_by(Street.street)
        result = await self.db_session.execute(query)
        return result.scalars().all()


@lru_cache
def get_street_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StreetService:
    return StreetService(db_session)
