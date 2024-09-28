import datetime

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path

from api.v1.security import get_current_user

from api.v1.services import OrderPayGateService, get_order_pay_gate_service
from api.v1.schemas import OrderPayGateSourceSchema

router = APIRouter(
    prefix='/order_portmone',
    tags=['order_portmone'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('/')
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
