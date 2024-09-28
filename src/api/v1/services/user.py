from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_async_session_server

from .base import BaseService
from api.v1.models import User


class UserService(BaseService):

    async def get_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        data = (await self.db_session.execute(query)).scalars().first()
        return data


@lru_cache
def get_user_service(db_session: AsyncSession = Depends(get_async_session_server)) -> UserService:
    return UserService(db_session)
