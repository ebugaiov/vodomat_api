from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core import config

DATABASE_URL_SERVER = f'mysql+aiomysql://{config.DATABASE_SERVER_USER}:{config.DATABASE_SERVER_PASSWORD}' \
                      f'@{config.DATABASE_SERVER_HOST}:{config.DATABASE_SERVER_PORT}/{config.DATABASE_SERVER_NAME}'

engine = create_async_engine(DATABASE_URL_SERVER, echo=True)
async_session_server = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session_server() -> AsyncSession:
    async with async_session_server() as session:
        yield session
