from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import get_async_session_server

from .base import BaseService
from api.v1.models import Street


class StreetService(BaseService):

    async def get_all(self) -> list[Street]:
        query = select(Street).options(joinedload(Street.city)).order_by(Street.street)
        streets = (await self.db_session.execute(query)).scalars().all()
        return streets


@lru_cache
def get_street_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StreetService:
    return StreetService(db_session)
