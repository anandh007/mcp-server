# import redis.asyncio as redis
# from .config import settings

# _redis = None

# async def get_redis():
#     global _redis
#     if _redis is None:
#         _redis = redis.from_url(
#             settings.redis_url,
#             encoding="utf-8",
#             decode_responses=True
#         )
#     return _redis

# async def get_cached(key: str):
#     r = await get_redis()
#     return await r.get(key)

# async def set_cached(key: str, value: str, ttl: int | None = None):
#     r = await get_redis()
#     await r.set(key, value, ex=ttl)


import redis.asyncio as redis
from .config import settings

# GLOBAL Redis client reused for all tests & runtime
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

async def get_cached(key: str):
    try:
        return await redis_client.get(key)
    except Exception:
        return None

async def set_cached(key: str, value: str, ttl: int | None = None):
    try:
        await redis_client.set(key, value, ex=ttl)
    except Exception:
        pass
