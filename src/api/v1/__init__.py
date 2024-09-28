from fastapi import APIRouter

# Import individual routers
from api.v1.endpoints.city import router as city_router
from api.v1.endpoints.street import router as street_router
from api.v1.endpoints.avtomat import router as avtomat_router
from api.v1.endpoints.status import router as status_router
from api.v1.endpoints.statistic import router as statistic_router
from api.v1.endpoints.issue import router as issue_router
from api.v1.endpoints.order import router as order_router
from api.v1.endpoints.order_app import router as order_app_router
from api.v1.endpoints.order_server import router as order_server_router
from api.v1.endpoints.order_portmone import router as order_portmone_router

# Create a main router for API v1
router = APIRouter()

# Include all individual routers
router.include_router(city_router)
router.include_router(street_router)
router.include_router(avtomat_router)
router.include_router(status_router)
router.include_router(statistic_router)
router.include_router(issue_router)
router.include_router(order_router)
router.include_router(order_app_router)
router.include_router(order_server_router)
router.include_router(order_portmone_router)
