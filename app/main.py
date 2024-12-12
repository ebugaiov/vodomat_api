import logging

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core import config
from core.logger import LOGGING

import api.v1.security as security_v1
from api.v1 import router as router_v1

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.API_VERSION,
    description=config.DESCRIPTION,
    docs_url='/docs',
    redoc_url=None,
    openapi_url='/openapi.json',
    default_response_class=ORJSONResponse,
    contact=config.CONTACT,
)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url='/openapi.json',
                          title=config.PROJECT_NAME,
                          redoc_favicon_url='/static/favicon.ico')


# API v1
app.include_router(security_v1.router)
app.include_router(router_v1, prefix='/v1')

# API v2


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
