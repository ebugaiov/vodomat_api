import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.v1.security import get_current_user

from api.v1.schemas import CollectionsSchema, StatisticLinesSchema
from api.v1.schemas.request_params import OrderByQueryParamServer, OrderDirectionQueryParam
from api.v1.services import StatisticService, get_statistic_service

router = APIRouter(
    prefix='/statistic',
    tags=['statistic'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('/collections', response_model=CollectionsSchema)
async def read_all_collections_by_date(date: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
                                       order_by: OrderByQueryParamServer = 'time',
                                       order_direction: OrderDirectionQueryParam = 'desc',
                                       statistic_service: StatisticService = Depends(get_statistic_service)):
    collections = await statistic_service.get_collections_by_date(order_by, order_direction, date)
    return {'collections': collections}


@router.get('/{avtomat_number}', response_model=StatisticLinesSchema)
async def read_all_by_period(avtomat_number: int,
                             start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
                             end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
                             statistic_service: StatisticService = Depends(get_statistic_service)):
    statistic_lines = await statistic_service.get_all_by_period(avtomat_number, start_period, end_period)
    return {'statistic_lines': statistic_lines}
