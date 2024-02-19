import aioredis
from core import config

REDIS_URL = f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}'
redis_pool = aioredis.from_url(REDIS_URL)


async def get_redis_pool() -> aioredis.Redis:
    yield redis_pool
