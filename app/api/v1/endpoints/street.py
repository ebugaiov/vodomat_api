from fastapi import APIRouter, Depends

from api.v1.security import get_current_user

from api.v1.schemas import StreetSchema
from api.v1.services import StreetService, get_street_service


router = APIRouter(
    prefix='/street',
    tags=['street'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('', response_model=list[StreetSchema])
async def read_all_streets(street_service: StreetService = Depends(get_street_service)) -> list[StreetSchema]:
    streets = await street_service.get_all()
    return streets
