from pydantic import BaseModel

from datetime import datetime

from typing import Optional


class OrderServerSchema(BaseModel):
    order_server_id: int
    order_pay_gate_id: int
    order_app_id: str
    order_server_time: datetime
    order_server_money: float
    order_server_status: int
    transaction: int
    price: Optional[int]
    fail_reason: Optional[int]


class OrderServerSourceSchema(BaseModel):
    count: int
    success_orders: int
    fail_orders: int
    server_orders: list[OrderServerSchema]
