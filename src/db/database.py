from databases import Database
import sqlalchemy
from core import config

DATABASE_URL = f'mysql+aiomysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}' \
               f'@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}'

database: Database = Database(DATABASE_URL)
database_metadata = sqlalchemy.MetaData()


async def get_database() -> Database:
    return database
