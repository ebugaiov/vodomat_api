from fastapi import APIRouter, Depends, Path

from security import get_current_user

from schemas import StatusSchema, StatusesSchema
from schemas.request_params import OrderByQueryParamServer, OrderDirectionQueryParam
from services import StatusService, get_status_service


router = APIRouter(
    prefix='/status',
    tags=['status'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('', response_model=StatusesSchema)
async def read_all(status_service: StatusService = Depends(get_status_service),
                   order_by: OrderByQueryParamServer = 'avtomat_number',
                   order_direction: OrderDirectionQueryParam = 'asc'):
    statuses = await status_service.get_all(order_by, order_direction)
    return {'statuses': statuses}


@router.get('/{avtomat_number}', response_model=StatusSchema)
async def read_by_avtomat_number(status_service: StatusService = Depends(get_status_service),
                                 avtomat_number: int = Path(..., ge=0, le=9999)):
    status = await status_service.get_item_by_avtomat_number(avtomat_number)
    return status
