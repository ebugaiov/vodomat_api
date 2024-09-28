from pydantic import BaseModel


class CitySchema(BaseModel):
    id: int
    city: str
