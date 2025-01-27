from uuid import uuid4
from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import IntEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CHAR, String

from pydantic import BaseModel, Field

from .base import Base


class PurchaseStatus(IntEnum):
    CREATED = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    REFUND = 3
    FAIL_BY_PAYMENT_GATEWAY = 4
    FAIL_AND_NOT_REFUND = 5
    FAIL_BY_SERVER = 6  # vodomat_service has not gotten deposit_id from the server
    FAIL_BY_AVTOMAT = 7  # deposit was created on server but failed by avtomat


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
    order_app_money: float = Field(..., validation_alias='money')
    order_app_status: int = Field(..., validation_alias='status')
    avtomat_number: int
    address: str

    class Config:
        from_attributes = True

