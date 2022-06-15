import logging

import aioredis
import databases
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import config
from core.logger import LOGGING
from db import redis
from db import database

from api.v3 import status

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.API_VERSION,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await database.database.connect()
    redis.redis = await aioredis.from_url(redis.REDIS_URL, encoding='utf-8', decode_responses=True)


@app.on_event('shutdown')
async def shutdown():
    await database.database.disconnect()
    await redis.redis.close()

app.include_router(status.router, prefix='/v3/status', tags=['status'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
