from fastapi import APIRouter, Depends, Path, Query

from api.v1.security import get_current_user

from api.v1.schemas import StatusSchema, StatusesSchema
from api.v1.schemas.request_params import OrderByQueryParamServer, OrderDirectionQueryParam
from api.v1.services import StatusService, get_status_service

router = APIRouter(
    prefix='/status',
    tags=['status'],
    # dependencies=[Depends(get_current_user), ]
)


@router.get('', response_model=StatusesSchema)
async def read_all(
        status_service: StatusService = Depends(get_status_service),
        order_by: OrderByQueryParamServer = Query('avtomat_number', description='Field to order results by'),
        order_direction: OrderDirectionQueryParam = Query('asc', description='Order direction: asc or desc'),
):
    """
    Fetch all statuses with optional ordering.

    :param status_service: Dependency injection for StatusService.
    :param order_by: Field to order the results by. Defaults to 'avtomat_number'.
    :param order_direction: Ordering direction ('asc' or 'desc'). Defaults to 'asc'.
    :return: List of serialized statuses.
    """
    statuses = await status_service.get_all(order_by, order_direction)
    return {'statuses': statuses}


@router.get('/{avtomat_number}', response_model=StatusSchema)
async def read_by_avtomat_number(
        status_service: StatusService = Depends(get_status_service),
        avtomat_number: int = Path(..., ge=0, le=9999, description='Avtomat number to retrieve the status for'),
):
    """
    Fetch a specific status by avtomat number.

    :param status_service: Dependency injection for StatusService.
    :param avtomat_number: The avtomat number to filter by (must be between 0 and 9999).
    :return: Serialized status.
    """
    status = await status_service.get_item_by_avtomat_number(avtomat_number)
    return status
