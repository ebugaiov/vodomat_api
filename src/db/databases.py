from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from core import config

# Vodomat Server Database
DATABASE_URL_SERVER = f'mysql+aiomysql://{config.DATABASE_SERVER_USER}:{config.DATABASE_SERVER_PASSWORD}' \
                      f'@{config.DATABASE_SERVER_HOST}:{config.DATABASE_SERVER_PORT}/{config.DATABASE_SERVER_NAME}'

engine_server = create_async_engine(DATABASE_URL_SERVER, echo=True)
async_session_server = async_sessionmaker(engine_server, expire_on_commit=False)


async def get_async_session_server():
    async with async_session_server() as session:
        yield session

# Vodomat App Database
DATABASE_URL_APP = f'mysql+aiomysql://{config.DATABASE_APP_USER}:{config.DATABASE_APP_PASSWORD}' \
                   f'@{config.DATABASE_APP_HOST}/{config.DATABASE_APP_NAME}'

engine_app = create_async_engine(DATABASE_URL_APP, echo=True)
async_session_app = async_sessionmaker(engine_app, expire_on_commit=False, )


async def get_async_session_app():
    async with async_session_app() as session:
        yield session
