from datetime import datetime

from pydantic import BaseModel

from typing import Optional


class OrderPayGateSchema(BaseModel):
    order_pay_gate_id: int
    order_app_id: str
    order_pay_gate_time: datetime
    order_pay_gate_money: float
    order_pay_gate_status: str
    pay_method: Optional[str]
    card_mask: Optional[str]


class OrderPayGateSourceSchema(BaseModel):
    count: int
    payed: int
    returned: int
    pay_gate_orders: list[OrderPayGateSchema]
