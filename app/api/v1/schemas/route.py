from pydantic import BaseModel


class RouteSchema(BaseModel):
    id: int
    name: str
    car_number: str
    driver_1: str
    driver_2: str
