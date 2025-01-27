from pydantic import BaseModel, Field
from typing import Optional

from .statistic import StatisticSchema
from .avtomat import Size, State


class StatusSchema(StatisticSchema):
    city: Optional[str] = Field(None, examples=['Kharkov', ])
    street: Optional[str] = Field(None, examples = ['MIRA ST.,', ])
    house: Optional[str] = Field(None, examples=['78 A', ])
    route_name: Optional[str] = Field(None, examples=['05', ])
    route_car_number: Optional[str] = Field(None, examples=['52-81', ])
    size: Optional[Size] = None
    state: Optional[State] = None


class StatusesSchema(BaseModel):
    statuses: list[StatusSchema]
