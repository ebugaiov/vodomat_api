from functools import lru_cache

from dateutil.parser import parse

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from models import Avtomat, Statistic, Street


class StatisticService(BaseService):

    async def get_collections_by_date(self, *args) -> list[Statistic]:
        order_attribute, order_direction, date = args
        query = select(Statistic)\
            .options(joinedload(Statistic.avtomat)
                     .options(joinedload(Avtomat.route), joinedload(Avtomat.street)
                              .options(joinedload(Street.city))))\
            .filter(Statistic['event'] == 3)\
            .filter(Statistic['time'].like(f'%{date}%'))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, order_attribute, order_direction)
        return ordered_data

    async def get_all_by_period(self, avtomat_number: int, start_period: str, end_period: str) -> list[Statistic]:
        query = select(Statistic).where(Statistic['avtomat_number'] == avtomat_number)
        start_period = parse(start_period)
        end_period = parse(end_period)
        if start_period.hour == 0 and start_period.minute == 0 and end_period.hour == 0 and end_period.minute == 0:
            query = query.filter(
                func.date(Statistic.time) >= start_period,
                func.date(Statistic.time) <= end_period
            )
        else:
            query = query.filter(Statistic['time'].between(start_period, end_period))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, 'time', 'desc')
        return ordered_data


@lru_cache
def get_statistic_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StatisticService:
    return StatisticService(db_session)