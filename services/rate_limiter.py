import os
from services.redis_client import redis_client

WEEKLY_LIMIT = int(os.getenv('WEEKLY_LIMIT', 10))
TTL = 7 * 24 * 60 * 60


async def is_allowed(user_id: int) -> bool:
    return True  # DISABLE

    key = f"limit:{user_id}"
    count = await redis_client.get(key)

    if count is None:
        await redis_client.set(key, 1, ex=TTL)
        return True

    count = int(count)
    if count >= WEEKLY_LIMIT:
        return False

    await redis_client.incr(key)
    return True
