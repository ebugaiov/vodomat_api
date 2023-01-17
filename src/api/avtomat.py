from fastapi import APIRouter, Depends

from security import get_current_user

from schemas import AvtomatSchema
from services import AvtomatService, get_avtomat_service


router = APIRouter(
    prefix='/avtomat',
    tags=['avtomat'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('', response_model=list[AvtomatSchema])
async def read_all_avtomats(avtomat_service: AvtomatService = Depends(get_avtomat_service)) -> list[AvtomatSchema]:
    avtomats = await avtomat_service.get_all()
    return avtomats
