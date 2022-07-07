from functools import lru_cache

from fastapi import Depends
from databases import Database
from sqlalchemy.sql import select

from db.database import get_database
from models import city, street, avtomat, route, status


class StatusService:
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self):
        j = status.join(avtomat, status.c.avtomat_number == avtomat.c.avtomat_number) \
                  .join(street, avtomat.c.street_id == street.c.id, isouter=True) \
                  .join(city, street.c.city_id == city.c.id, isouter=True) \
                  .join(route, avtomat.c.route_id == route.c.id, isouter=True)
        query = select([status, city.c.city, street.c.street,
                        avtomat.c.house, route.c.car_number,
                        route.c.name.label('route_name')]).select_from(j)
        return await self.database.fetch_all(query)


@lru_cache
def get_status_service(database: Database = Depends(get_database)) -> StatusService:
    return StatusService(database)
