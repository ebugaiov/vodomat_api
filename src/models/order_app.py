from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import Column
from sqlalchemy import Integer, Float, String, DateTime
from sqlalchemy.types import SMALLINT

from pydantic import BaseModel, Field

from .base import Base


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, index=True)
    avtomat_number = Column(Integer, index=True)
    address = Column(String(120), index=True)
    money = Column(Float)
    status = Column(SMALLINT)
    payment_gateway_id = Column(String(20), unique=True, index=True)
    deposit_id = Column(Integer, unique=True, index=True)


class OrderApp(BaseModel):
    order_app_id: str = Field(..., validation_alias='id')
    order_pay_gate_id: Optional[int] = Field(None, validation_alias='payment_gateway_id')
    order_server_id: Optional[int] = Field(None, validation_alias='deposit_id')
    created_at: datetime
    order_app_money: Decimal = Field(..., validation_alias='money')
    order_app_status: int = Field(..., validation_alias='status')
    avtomat_number: int
    address: str

    class Config:
        from_attributes = True

