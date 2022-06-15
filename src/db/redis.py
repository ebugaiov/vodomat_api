from aioredis import Redis
from core import config

REDIS_URL = f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}'
redis: Redis = None


async def get_redis() -> Redis:
    return redis
