import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core import config

from api.v1.security import router as security_router_v1
from api.v1 import router as router_v1

api_v1 = FastAPI(
    title=config.PROJECT_NAME,
    version='1.0',
    description=config.DESCRIPTION,
    contact=config.CONTACT,
    docs_url='/docs',
    openapi_url='/openapi.json',
)

api_v1.include_router(router_v1)

# Main app for mounting different versions of api
app = FastAPI(docs_url=None, redoc_url=None)

# API v1
app.include_router(security_router_v1)
app.mount('/v1', api_v1)

# API v2

# Static
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000,)
