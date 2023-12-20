#!/usr/bin/env python3
'''A module for using basic Redis.
'''
from functools import wraps
from typing import Any, Callable, Union
import redis


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def wrapper_func(self, *args, **kwargs) -> Any:
        '''returns method with an incremented call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper_func
