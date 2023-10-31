from cachetools import cached, FIFOCache 
import redis
import os
import json
import asyncio

class Cache:

    def __init__(self, use_local_cache: bool, use_remote_cache: bool, local_cache_size: int, remote_db_index = 0):
        if (use_remote_cache):
            self.__create_remote_cache(remote_db_index) 
        else:
            self._remote_cache = None  
            self._using_remote_cache = False
        if (use_local_cache):
            self.__create_local_cache(local_cache_size) 
        else:
            self._local_cache = None  
            self._using_local_cache = False

    def __del__(self):
        self.__release_remote_cache()
        self.__release_local_cache()

    def __create_local_cache(self, maxsize: int):
        self._local_cache = FIFOCache(maxsize = maxsize) 
        self._using_local_cache = True

    def __release_local_cache(self):
        self._local_cache = None 
        self._using_local_cache = False

    def __create_remote_cache(self, remote_db_index: int):
        if (not remote_db_index in range(0,16)): 
            raise Exception('cannot create remote cache, invalid db index')
        self._remote_cache = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'], db=remote_db_index) 
        self._using_remote_cache = True

    def __release_remote_cache(self):
        if (self._using_remote_cache):
            self._remote_cache = None
            self._using_remote_cache = False

    def _set(self, key: str, value: dict):    
        if (key is None):
            return False
        value_str = json.dumps(value)
        cached = False
        if (self._using_remote_cache):
            self._remote_cache.setnx(key, value_str) 
            cached = True
        if (self._using_local_cache):
            if (not key in self._local_cache):
                self._local_cache[key] = value_str
            cached = True
        return cached

    def _get(self, key: str) -> dict:
        if (key is None):
            return None
        if (self._using_local_cache and (key in self._local_cache)):
            value_str = self._local_cache.get(key)
            if (value_str):
                value_dict = json.loads(value_str)
                value_dict['cached'] = 'local'
                return value_dict
        if (self._using_remote_cache):
            value_str = self._remote_cache.get(key)
            if (value_str):
                value_dict = json.loads(value_str)
                if (self._local_cache):
                    self._local_cache[key] = value_str
                value_dict['cached'] = 'remote'
                return value_dict
        return None

    async def set(self, key: str, value: dict):    
        return self._set(key, value)

    async def get(self, key: str) -> dict:
        return self._get(key)

    def clear(self):
        if (self._using_remote_cache):
            self._remote_cache.flushdb()
        if (self._using_local_cache):
            cache_sz = self._local_cache.maxsize
            self.__release_local_cache()
            self.__create_local_cache(cache_sz)
