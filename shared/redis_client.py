"""Redis client for caching"""
import redis
import os
import json

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)


def get_cache(key: str):
    """Get value from cache"""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Redis get error: {e}")
        return None


def set_cache(key: str, value: any, expire: int = 3600):
    """Set value in cache with expiration"""
    try:
        redis_client.setex(key, expire, json.dumps(value))
    except Exception as e:
        print(f"Redis set error: {e}")


def delete_cache(key: str):
    """Delete key from cache"""
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Redis delete error: {e}")

