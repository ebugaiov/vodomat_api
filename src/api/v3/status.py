from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
import datetime

from services.status import StatusService, get_status_service

router = APIRouter()


class Status(BaseModel):
    avtomat_number: int
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    car_number: Optional[str]
    route_name: Optional[str]
    time: datetime.datetime
    water: int
    money: int
    money_app: Optional[int]
    state: Optional[int]
    bill_not_work: Optional[int]
    coin_not_work: Optional[int]
    time_to_block: int
    low_water_balance: bool
    error_volt: bool
    error_bill: bool
    error_counter: bool
    error_register: bool


@router.get('/', response_model=List[Status])
async def all_statuses(status_service: StatusService = Depends(get_status_service)) -> List[Status]:
    statuses = await status_service.get_all()
    return statuses
