import datetime

from typing import Annotated

from fastapi import Depends, APIRouter, Query

from services import OrderService, get_order_service

from schemas import OrderSchema, OrdersSchema
from schemas.request_params import OrderByQueryParamOrders, OrderDirectionQueryParam

router = APIRouter(
    prefix='/order',
    tags=['order']
)


@router.get('')
async def read_all_by_period(
        start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        order_by: OrderByQueryParamOrders = 'created_at',
        order_direction: OrderDirectionQueryParam = 'desc',
        order_service: OrderService = Depends(get_order_service)) -> OrdersSchema:
    orders = await order_service.get_all_by_period(start_period, end_period, order_by, order_direction)
    resp = {
        'count': len(orders),
        'sum_pay_gate': sum([item.money_payment_gateway for item in orders if item.status_payment_gateway == 'PAYED']),
        'sum_server': sum([item.money_server for item in orders if item.status_server == 1]),
        'orders': orders
    }
    return resp


@router.get('/{pk}')
async def read_by_id(pk: int, order_service: OrderService = Depends(get_order_service)) -> OrderSchema:
    order = await order_service.get_item_by_id(pk)
    return order
