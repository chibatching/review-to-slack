import os

import redis

_REDIS = redis.from_url(os.environ.get("REDIS_URL"))


def set_to_redis(key, value):
    _REDIS.set(key, value)


def get_from_redis(key):
    return _REDIS.get(key)
