from fastapi import APIRouter, Depends

from security import get_current_user

from schemas import CitySchema
from services import CityService, get_city_service


router = APIRouter(
    prefix='/city',
    tags=['city'],
    dependencies=[Depends(get_current_user)]
)


@router.get('', response_model=list[CitySchema])
async def read_all_cities(city_service: CityService = Depends(get_city_service)):
    cities = await city_service.get_all()
    return cities
