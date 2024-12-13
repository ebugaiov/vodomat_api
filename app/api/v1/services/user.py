from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_async_session_server

from .base import BaseService
from models import User


class UserService(BaseService):

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        :param username: The username to filter by.
        :return: A User object if found, else None.
        """
        query = select(User).where(User.username == username)
        return await self.db_session.scalar(query)


@lru_cache
def get_user_service(db_session: AsyncSession = Depends(get_async_session_server)) -> UserService:
    return UserService(db_session)
