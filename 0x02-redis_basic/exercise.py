#!/usr/bin/env python3
'''A module for using basic Redis.
'''
import uuid
import redis
from typing import Union, Callable, Optional


class Cache:
    def __init__(self, redis_url: str = 'redis://localhost:6379/0'):
        self._redis = redis.Redis.from_url(redis_url)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''takes a data argument and returns a string
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None)
    -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        return self.get(
                key,
                fn=lambda d: d.decode("utf-8") if isinstance(d, bytes)
                else d)

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)
