import redis
from cachetools import cached, LRUCache 
import os
import json

class Cache:

    def __init__(self, use_local_cache = True, use_remote_cache = True, local_cache_size = 4096):
        self.use_local_cache = use_local_cache
        self.use_remote_cache = use_remote_cache
        if (use_local_cache):
            self.local_cache = LRUCache(maxsize = local_cache_size) 
        if (use_remote_cache):
            self.remote_cache = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'], db=0)
                
    async def set(self, key:str, value: dict):
        if (self.use_remote_cache):
            self.remote_cache.set(key, json.dumps(value)) 
        if (self.use_local_cache):
            self.local_cache[key] = value
        
    async def get(self, key: str) -> dict :
        if (self.use_local_cache):    
            try:
                value = self.local_cache[key]
            except Exception as e:
                value = None
        else:
            value = None
        if (value is None and self.use_remote_cache):
            value = self.remote_cache.get(key)
            if (value):
                value = json.loads(value)
                if (self.use_local_cache):
                    self.local_cache[key] = value
        if (value):
            value['cached'] = True                   
        return value

