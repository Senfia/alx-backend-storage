#!/usr/bin/env python3
'''A module for using basic Redis.
'''

import requests
import redis
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        key = f"count:{url}"
        result = method(url, *args, **kwargs)
        method.__self__._redis.incr(key)
        method.__self__._redis.expire(key, 10)
        return result

    return wrapper

class PageCache:
    def __init__(self, redis_url: str = 'redis://localhost:6379/0'):
        self._redis = redis.Redis.from_url(redis_url)

    @count_calls
    def get_page(self, url: str) -> str:
        response = requests.get(url)
        return response.text
