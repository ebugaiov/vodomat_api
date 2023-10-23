import datetime

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from security import get_current_user

from services import OrderPayGateService, get_order_pay_gate_service
from services import OrderAppService, get_order_app_service
from services import OrderServerService, get_order_server_service

from schemas import OrderServerSourceSchema, OrderAppSourceSchema, OrderPayGateSourceSchema

router = APIRouter(
    prefix='/source',
    tags=['source'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('/portmone')
async def read_all_pay_gate_by_period(
        start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        order_pay_gate_service: OrderPayGateService = Depends(get_order_pay_gate_service)) -> OrderPayGateSourceSchema:
    pay_gate_orders = await order_pay_gate_service.get_all_by_period(start_period, end_period)
    resp = {
        'count': len(pay_gate_orders),
        'payed': len([order for order in pay_gate_orders if order.order_pay_gate_status == 'PAYED']),
        'returned': len([order for order in pay_gate_orders if order.order_pay_gate_status == 'RETURN']),
        'pay_gate_orders': pay_gate_orders
    }
    return resp


@router.get('/app')
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


@router.get('/server')
async def read_all_server_by_period(
        start_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        end_period: Annotated[str, Query(default_factory=datetime.date.today().isoformat)],
        order_server_service: OrderServerService = Depends(get_order_server_service)) -> OrderServerSourceSchema:
    server_orders = await order_server_service.get_all_by_period(start_period, end_period)
    resp = {'count': len(server_orders),
            'success_orders': len([order for order in server_orders if order.order_server_status == 1]),
            'fail_orders': len([order for order in server_orders if order.order_server_status == 2]),
            'server_orders': server_orders}
    return resp
