from uuid import uuid4
from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CHAR, String

from pydantic import BaseModel, Field

from .base import Base


class Purchase(Base):
    __tablename__ = 'purchase'

    id: Mapped[str] = mapped_column(CHAR(36), default=uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    avtomat_number: Mapped[int] = mapped_column(index=True)
    address: Mapped[str] = mapped_column(String(120))
    money: Mapped[float]
    status: Mapped[int] = mapped_column(index=True)
    payment_gateway_id: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True)
    deposit_id: Mapped[Optional[int]] = mapped_column(unique=True, index=True)


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

