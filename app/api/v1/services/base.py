from typing import Optional, Any, Type, Union
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from fastapi import HTTPException, status

class BaseService:
    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def _get_db_item_by_field(self, model_class: Type, field: str, value: Union[str, int]) -> Any:
        try:
            query = select(model_class).where(getattr(model_class, field) == value)
            item = (await self.db_session.execute(query)).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{model_class.__name__} Item with {field} == {value} not found')
        return item


    @staticmethod
    def get_ordered_data(data: Sequence, order_attribute: str, order_direction: str) -> Sequence:
        return sorted(data, key=lambda item: getattr(item, order_attribute) or 0,
                      reverse=order_direction == 'desc')
