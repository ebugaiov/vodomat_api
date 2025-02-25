from typing import Optional, Any

from datetime import datetime

from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, computed_field


class Order(BaseModel):
    id_payment_gateway: int = Field(..., validation_alias='order_pay_gate_id')
    id_purchase: str = Field(..., validation_alias='order_app_id')
    id_server: Optional[int] = Field(None, validation_alias='order_server_id')
    created_at: datetime
    time_payment_gateway: Optional[datetime] = Field(None, validation_alias='order_pay_gate_time')
    time_server: Optional[datetime] = Field(None, validation_alias='order_server_time')
    status_purchase: int = Field(..., validation_alias='order_app_status')
    status_payment_gateway: str = Field(..., validation_alias='order_pay_gate_status')
    status_server: Optional[int] = Field(None, validation_alias='order_server_status')
    money_purchase: Decimal = Field(..., validation_alias='order_app_money')
    money_payment_gateway: Decimal = Field(..., validation_alias='order_pay_gate_money')
    money_server: Optional[Decimal] = Field(None, validation_alias='order_server_money')
    price: Optional[int] = None
    avtomat_number: int
    address: Optional[str] = ''
    card_mask: Optional[str] = ''
    gate_type: Optional[str] = Field(None, validation_alias='pay_method')
    transaction: Optional[int] = None

    @computed_field
    @property
    def error(self) -> bool:
        return \
                (self.status_payment_gateway == 'PAYED' and self.status_server != 1
                 and self.status_purchase not in (1, 3)) \
                or \
                (self.status_payment_gateway == 'PAYED' and self.status_server == 1
                 and self.money_payment_gateway != self.money_server)

    @field_validator('*', mode='before')
    @classmethod
    def transform_nan_to_none(cls, value: Any):
        if value != value:  # pandas.isnan(item) when item != item
            return None
        return value
