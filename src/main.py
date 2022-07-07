import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import config
from core.logger import LOGGING
from db import database

import security
from api.v3 import status

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.API_VERSION,
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await database.database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.database.disconnect()

app.include_router(status.router, prefix='/v3/status', tags=['status'])
app.include_router(security.router, prefix='', tags=['security'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
