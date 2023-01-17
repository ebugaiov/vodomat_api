from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_async_session_server

from .base import BaseService
from models import City


class CityService(BaseService):

    async def get_all(self) -> list[City]:
        query = select(City).order_by(City.city)
        data = (await self.db_session.execute(query)).scalars().all()
        return data


@lru_cache
def get_city_service(db_session: AsyncSession = Depends(get_async_session_server)) -> CityService:
    return CityService(db_session)
