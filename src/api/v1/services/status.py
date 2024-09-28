from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from api.v1.models import Status, Avtomat, Street


class StatusService(BaseService):

    async def get_all(self, *args) -> list[Status]:
        order_attribute, order_direction = args
        query = select(Status)\
            .options(joinedload(Status.avtomat)
                     .options(joinedload(Avtomat.route), joinedload(Avtomat.street)
                              .options(joinedload(Street.city))))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, order_attribute, order_direction)
        return ordered_data

    async def get_item_by_avtomat_number(self, avtomat_number: int) -> Status:
        query = select(Status)\
            .options(joinedload(Status.avtomat).options(joinedload(Avtomat.route), joinedload(Avtomat.street)))\
            .where(Status.avtomat_number == avtomat_number)
        data = (await self.db_session.execute(query)).scalar()
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return data


@lru_cache
def get_status_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StatusService:
    return StatusService(db_session)
