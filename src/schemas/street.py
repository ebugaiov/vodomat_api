from pydantic import BaseModel


class StreetSchema(BaseModel):
    id: int
    street: str
    city_id: int
    city_name: str
