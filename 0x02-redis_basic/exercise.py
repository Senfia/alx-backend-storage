#!/usr/bin/env python3
'''A module for using basic Redis.
'''

import uuid
import redis
from typing import Union


class Cache:
    def __init__(self, redis_url: str = 'redis://localhost:6379/0'):
        self._redis = redis.Redis.from_url(redis_url)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
