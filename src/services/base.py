from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession


class BaseService:
    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    @staticmethod
    def get_ordered_data(data, order_attribute, order_direction):
        return sorted(data, key=lambda item: getattr(item, order_attribute) or 0,
                      reverse=order_direction == 'desc')
