from pydantic import BaseModel, RootModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class OrderSchema(BaseModel):
    id_payment_gateway: int
    id_purchase: str
    id_server: Optional[int]
    created_at: datetime
    time_payment_gateway: Optional[datetime]
    time_server: Optional[datetime]
    status_purchase: int
    status_payment_gateway: str
    status_server: Optional[int]
    money_purchase: Decimal
    money_payment_gateway: Decimal
    money_server: Optional[Decimal]
    price: Optional[int]
    avtomat_number: int
    address: Optional[str]
    card_mask: Optional[str]
    gate_type: Optional[str]
    transaction: Optional[int]
    error: bool


class OrdersSchema(BaseModel):
    count: int
    sum_pay_gate: Decimal
    sum_server: Decimal
    orders: list[OrderSchema]


class OrderRefundSchema(RootModel[dict[int, str]]):
    pass
