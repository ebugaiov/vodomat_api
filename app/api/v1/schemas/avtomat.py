from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Size(int, Enum):
    SINGLE = 470
    DOUBLE = 940
    DOUBLE_HALF = 471


class State(int, Enum):
    UNDEFINED = 0
    NORMAL = 1
    NO_VOLT = 2
    CRASHED = 3
    LIMIT = 4


class AvtomatSchema(BaseModel):
    avtomat_number: int
    route_name: Optional[str]
    route_car_number: Optional[str]
    city_name: Optional[str]
    street_name: Optional[str]
    house: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    search_radius: Optional[int]
    price: Optional[int]
    price_for_app: Optional[int]
    payment_app_url: Optional[str]
    max_sum: Optional[int]
    size: Optional[Size]
    competitors: Optional[bool]
    state: Optional[State]
    rro_id: Optional[int]
    security_id: Optional[str]
    security_state: Optional[int]
