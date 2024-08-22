import datetime

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path

from security import get_current_user

from services import OrderAppService, get_order_app_service

from schemas import OrderAppSourceSchema
from schemas import OrderAppSchema

router = APIRouter(
    prefix='/order_app',
    tags=['order_app'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('/')
async def read_all_app_by_period(
        start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        order_app_service: OrderAppService = Depends(get_order_app_service)) -> OrderAppSourceSchema:
    app_orders = await order_app_service.get_all_by_period(start_period, end_period)
    resp = {
        'count': len(app_orders),
        'payed': len([order for order in app_orders if order.order_app_status == 2]),
        'refund': len([order for order in app_orders if order.order_app_status == 3]),
        'not_refund': len([order for order in app_orders if order.order_app_status == 5]),
        'app_orders': app_orders
    }
    return resp


@router.get('/{item_id}')
async def read_order_app_item_by_id(
        item_id: Annotated[str, Path(title='The ID of the Purchase item in the app db')],
        order_app_service: OrderAppService = Depends(get_order_app_service)) -> OrderAppSchema:
    order_app = await order_app_service.get_item_by_id(item_id)
    return order_app