from functools import lru_cache

from fastapi import Depends
from databases import Database
from sqlalchemy.sql import select

from db.database import get_database
from models import user


class UserService:
    def __init__(self, database: Database):
        self.database = database

    async def get_by_username(self, username: str):
        query = select(user).where(user.c.username == username)
        return await self.database.fetch_one(query=query)


@lru_cache
def get_user_service(database: Database = Depends(get_database)) -> UserService:
    return UserService(database)
