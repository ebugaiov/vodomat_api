from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class OrderAppSchema(BaseModel):
    order_app_id: str
    order_pay_gate_id: Optional[int]
    order_server_id: Optional[int]
    created_at: datetime
    order_app_money: float
    order_app_status: int
    avtomat_number: int
    address: str


class OrderAppSourceSchema(BaseModel):
    count: int
    payed: int
    refund: int
    not_refund: int
    app_orders: list[OrderAppSchema]
