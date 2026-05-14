import json
from typing import Any, Optional
import redis.asyncio as redis
from .config import settings

pool: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    global pool
    if pool is None:
        pool = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    return pool


async def cache_get(key: str) -> Any | None:
    r = await get_redis()
    val = await r.get(key)
    return json.loads(val) if val else None


async def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    r = await get_redis()
    await r.setex(key, ttl, json.dumps(value, default=str))


async def cache_delete(key: str) -> None:
    r = await get_redis()
    await r.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    r = await get_redis()
    async for key in r.scan_iter(match=pattern):
        await r.delete(key)
