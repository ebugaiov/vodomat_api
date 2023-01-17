from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StatusSchema(BaseModel):
    id: int
    avtomat_number: int = Field(..., ge=0, le=9999)
    address: Optional[str] = Field(None, example='MIRA STR., 74')
    route_name: Optional[str] = Field(None, example='05')
    route_car_number: Optional[str] = Field(None, example='52-81')
    time: datetime
    water: int
    money: int
    price: int = Field(..., description='Price in kop')
    grn: int
    kop: int
    money_app: Optional[int]
    bill_not_work: Optional[int] = Field(None, description='Period in seconds, Bill does not change its state')
    coin_not_work: Optional[int] = Field(None, description='Period in seconds, Coin does not change its state')
    bill_not_work_money: Optional[int]
    coin_not_work_money: Optional[int]
    time_to_block: int
    low_water_balance: bool
    error_volt: bool
    error_bill: bool
    error_counter: bool
    error_register: bool
    cashbox: Optional[bool]
    gsm: Optional[int]
    event: int

    class Config:
        orm_mode = True
