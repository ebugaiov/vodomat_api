from pydantic import BaseModel, Field, field_validator

from datetime import datetime

from decimal import Decimal

from typing import Optional


class OrderPayGate(BaseModel):
    order_pay_gate_id: int = Field(..., validation_alias='shopBillId')
    order_app_id: str = Field(..., validation_alias='shopOrderNumber')
    order_pay_gate_time: datetime = Field(..., validation_alias='pay_date')
    order_pay_gate_money: Decimal = Field(..., validation_alias='billAmount')
    order_pay_gate_status: str = Field(..., validation_alias='status')
    pay_method: Optional[str] = Field(None, validation_alias='gateType')
    card_mask: Optional[str] = Field(None, validation_alias='cardMask')

    @field_validator('order_pay_gate_time', mode='before')
    @classmethod
    def handle_order_pay_gate_time(cls, value: str) -> datetime:
        return datetime.fromisoformat(f'{"-".join(value.split()[0].split(".")[::-1])}T{value.split()[1]}')
