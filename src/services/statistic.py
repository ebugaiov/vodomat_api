from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from models import Avtomat, Statistic, Street


class StatisticService(BaseService):

    async def get_collections_by_date(self, *args) -> list[Statistic]:
        order_attribute, order_direction, date = args
        query = select(Statistic)\
            .options(joinedload(Statistic.avtomat)\
                .options(joinedload(Avtomat.route), joinedload(Avtomat.street)\
                    .options(joinedload(Street.city))))\
            .where(Statistic.event == 3)\
            .where(Statistic.time.like(f'%{date}%'))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, order_attribute, order_direction)
        return ordered_data

    async def get_all_by_period(self, avtomat_number: int, start_period: str, end_period: str) -> list[Statistic]:
        query = select(Statistic)\
            .where(Statistic.avtomat_number == avtomat_number)\
                .filter(and_(
                    func.date(Statistic.time) >= start_period,
                    func.date(Statistic.time) <= end_period
                ))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, 'time', 'desc')
        return ordered_data


@lru_cache
def get_statistic_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StatisticService:
    return StatisticService(db_session)