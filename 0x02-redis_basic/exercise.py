#!/usr/bin/env python3
'''A module for using basic Redis.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return caller


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return caller


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fsn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fsn_name)
    out_key = '{}:outputs'.format(fsn_name)
    fsn_call_count = 0
    if redis_store.exists(fsn_name) != 0:
        fsn_call_count = int(redis_store.get(fsn_name))
    print('{} was called {} times:'.format(fsn_name, fsn_call_count))
    fsn_inputs = redis_store.lrange(in_key, 0, -1)
    fsn_outputs = redis_store.lrange(out_key, 0, -1)
    for fsn_input, fsn_output in zip(fsn_inputs, fsn_outputs):
        print('{}(*{}) -> {}'.format(
            fsn_name,
            fsn_input.decode("utf-8"),
            fsn_output,
        ))


class Cache:
    '''Object for storing data in Redis.
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Takes a data argument and returns a string.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Returns a value from a Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''returns a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''returns an integer value from a Redis data storage.
        '''
        return self.get(key, lambda x: int(x))
