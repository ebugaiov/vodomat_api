from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session_server

from .base import BaseService
from models import Status, Avtomat, Street


class StatusService(BaseService):

    async def get_all(self, order_by: str, order_direction: str) -> list[Status]:
        """
        Fetch all Status objects, optionally ordered by a specified attribute and direction.

        :param order_by: The field to order results by.
        :param order_direction: The ordering direction, either 'asc' or 'desc'.
        :return: List of Status objects.
        """
        # Determine the ordering direction
        order_clause = asc(order_by) if order_direction == 'asc' else desc(order_by)

        query = (
            select(Status)
            .options(
                joinedload(Status.avtomat)
                .options(
                    joinedload(Avtomat.route),
                    joinedload(Avtomat.street).options(joinedload(Street.city))
                )
            )
            .order_by(order_clause)
        )

        return (await self.db_session.scalars(query)).all()

    async def get_item_by_avtomat_number(self, avtomat_number: int) -> Status:
        """
        Fetch a single Status object by its avtomat_number.

        :param avtomat_number: The avtomat_number to filter by.
        :return: A single Status object.
        :raises HTTPException: If no Status object is found.
        """
        query = (
            select(Status)
            .options(
                joinedload(Status.avtomat)
                .options(
                    joinedload(Avtomat.route),
                    joinedload(Avtomat.street).options(joinedload(Street.city))
                )
            )
            .where(Status.avtomat_number == avtomat_number)
        )

        result = await self.db_session.scalar(query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Status object with avtomat_number {avtomat_number} not found.',
            )
        return result


@lru_cache
def get_status_service(db_session: AsyncSession = Depends(get_async_session_server)) -> StatusService:
    return StatusService(db_session)
