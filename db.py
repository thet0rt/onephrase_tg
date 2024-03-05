import json
from datetime import timedelta
from os import getenv
from typing import Optional

from redis import asyncio as aioredis

REDIS_URL = getenv("REDIS_URL")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def get_from(key: str) -> str | None:
    val = await redis_client.get(key)
    return val


async def set_to(key: str, val: str, ex: Optional[timedelta]) -> bool:
    res = await redis_client.set(
        name=key,
        ex=ex,
        value=val,
    )
    return res
