from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import Column
from sqlalchemy import Integer, Float, String, DateTime
from sqlalchemy.dialects.mysql import TINYINT

from pydantic import BaseModel, Field

from .base import Base


class Deposit(Base):
    __tablename__ = 'deposit'

    id = Column(Integer, primary_key=True)
    avtomat_number = Column(Integer, index=True)
    purchase_id = Column(String(36), index=True)
    payment_gateway_id = Column(String(64), index=True)
    time = Column(DateTime, index=True)
    transaction = Column(Integer)
    money = Column(Float)
    price = Column(Integer)
    status = Column(TINYINT, index=True)
    fail_reason = Column(TINYINT)


class OrderServer(BaseModel):
    order_server_id: int = Field(..., validation_alias='id')
    order_pay_gate_id: int = Field(..., validation_alias='payment_gateway_id')
    order_app_id: str = Field(..., validation_alias='purchase_id')
    order_server_time: datetime = Field(..., validation_alias='time')
    order_server_money: Decimal = Field(..., validation_alias='money')
    order_server_status: int = Field(..., validation_alias='status')
    transaction: int
    price: Optional[int] = None
    fail_reason: Optional[int] = None

    class Config:
        from_attributes = True
