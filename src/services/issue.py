from functools import lru_cache

from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_app

from .base import BaseService
from models import Issue


class IssueService(BaseService):

    async def get_all_by_date(self, *args) -> list[Issue]:
        order_attribute, order_direction, created_at = args
        query = select(Issue).where(Issue.created_at.like(f'%{created_at}%'))
        selected_data = (await self.db_session.execute(query)).scalars().all()
        ordered_data = self.get_ordered_data(selected_data, order_attribute, order_direction)
        return ordered_data

    async def get_item_by_id(self, pk: int) -> Issue:
        query = select(Issue).where(Issue.id == pk)
        data = (await self.db_session.execute(query)).scalar()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return data

    async def make_comment(self, pk: int, comment: Optional[str]) -> Issue:
        current_issue = await self.get_item_by_id(pk)
        current_issue.comment = comment
        await self.db_session.commit()
        return current_issue


@lru_cache
def get_issue_service(db_session: AsyncSession = Depends(get_async_session_app)) -> IssueService:
    return IssueService(db_session)
