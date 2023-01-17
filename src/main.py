import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core import config
from core.logger import LOGGING

import security
import api

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.API_VERSION,
    docs_url='/docs',
    openapi_url='/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(security.router)
app.include_router(api.city_router)
app.include_router(api.street_router)
app.include_router(api.avtomat_router)
app.include_router(api.status_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
