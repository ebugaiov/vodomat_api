import datetime

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path

from security import get_current_user

from services import OrderServerService, get_order_server_service

from schemas import OrderServerSourceSchema
from schemas import OrderServerSchema

router = APIRouter(
    prefix='/order_server',
    tags=['order_server'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('/')
async def read_all_order_server_items_by_period(
        start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        order_server_service: OrderServerService = Depends(get_order_server_service)) -> OrderServerSourceSchema:
    server_orders = await order_server_service.get_all_by_period(start_period, end_period)
    resp = {'count': len(server_orders),
            'success_orders': len([order for order in server_orders if order.order_server_status == 1]),
            'fail_orders': len([order for order in server_orders if order.order_server_status == 2]),
            'server_orders': server_orders}
    return resp


@router.get('/{item_id}')
async def read_order_server_item_by_id(
        item_id: Annotated[int, Path(title='The ID of the Deposit item in the server db')],
        order_server_service: OrderServerService = Depends(get_order_server_service)) -> OrderServerSchema:
    order_server = await order_server_service.get_item_by_id(item_id)
    return order_server
