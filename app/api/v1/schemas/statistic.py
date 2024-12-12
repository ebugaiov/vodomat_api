from pydantic import BaseModel, Field

from datetime import datetime
from typing import Optional


class StatisticSchema(BaseModel):
    id: int
    avtomat_number: int = Field(..., ge=0, le=11000)
    time: datetime
    water: int
    money: int
    price: int = Field(..., description='Price in kop')
    grn: int
    kop: int
    money_app: Optional[int]
    bill_not_work_hours: int = Field(0, description='Period in hours, Bill does not change its state')
    coin_not_work_hours: int = Field(0, description='Period in hours, Coin does not change its state')
    bill_not_work_coins: float = Field(None, description='The sum of coins, accepted during the bills downtime')
    coin_not_work_bills: int = Field(None, description='The sum of bills, accepted during the coins downtime')
    time_to_block: int
    low_water_balance: bool
    error_volt: bool
    error_bill: bool
    error_counter: bool
    error_register: bool
    cashbox: Optional[bool]
    gsm: Optional[int]
    event: int


class StatisticLinesSchema(BaseModel):
    statistic_lines: list[StatisticSchema]