import redis
from cachetools import cached, FIFOCache 
import os
import json

class Cache:

    _max_remote_dbs = 16 # redis limit
    _remote_db_avail_list = [True for _ in range(_max_remote_dbs)]

    def __init__(self, use_local_cache: bool, use_remote_cache: bool, local_cache_size: int):
        if (use_remote_cache):
            self.__create_remote_cache() 
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

    def __create_remote_cache(self):
        try:
            self._remote_cache_db_index = next(i for i, value in enumerate(self._remote_db_avail_list) if value)
            self._remote_db_avail_list[self._remote_cache_db_index] = False
        except StopIteration:
            raise Exception('cannot create remote cache')
        self._remote_cache = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'], db=self._remote_cache_db_index) 
        self._using_remote_cache = True

    def __release_remote_cache(self):
        if (self._using_remote_cache):
            self._remote_cache.flushdb()
            self._remote_db_avail_list[self._remote_cache_db_index] = True
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

    def reset(self):
        if (self._using_remote_cache):
            self.__release_remote_cache()
            self.__create_remote_cache()
        if (self._using_local_cache):
            cache_sz = self._local_cache.maxsize
            self.__release_local_cache()
            self.__create_local_cache(cache_sz)

    async def set(self, key: str, value: dict) -> bool: 
        return self._set(key, value)

    async def get(self, key: str) -> dict:
        return self._get(key)