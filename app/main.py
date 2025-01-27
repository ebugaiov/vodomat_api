import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from core import config

from api.v1.security import router as security_router_v1
from api.v1 import router as router_v1

# Main app for mounting different versions of api
app = FastAPI(docs_url=None, redoc_url=None)
app.mount('/static', StaticFiles(directory='static'), name='static')

# API v1 -----------------------------
api_v1 = FastAPI(docs_url=None,title=config.PROJECT_NAME, version='1.0', description=config.DESCRIPTION, contact=config.CONTACT)

@api_v1.get('/docs', include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/v1/openapi.json',
        title=config.PROJECT_NAME,
        swagger_favicon_url='/static/favicon.ico',
    )

api_v1.include_router(router_v1)
# END API v1 --------------------------

# API v2 ------------------------------

# END API v2 --------------------------

app.include_router(security_router_v1)
app.mount('/v1', api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
