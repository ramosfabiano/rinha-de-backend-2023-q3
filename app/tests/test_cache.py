import unittest
from cache import Cache

class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        cache = Cache(use_local_cache = True, use_remote_cache = True, local_cache_size = 5000)
        self.assertNotEqual(cache._local_cache, None)
        self.assertEqual(cache._local_cache.maxsize, 5000)
        self.assertNotEqual(cache._remote_cache, None)
        cache = Cache(use_local_cache = True, use_remote_cache = True, local_cache_size = 4000)
        self.assertNotEqual(cache._local_cache, None)
        self.assertEqual(cache._local_cache.maxsize, 4000)
        self.assertNotEqual(cache._remote_cache, None)
        cache = Cache(use_local_cache = False, use_remote_cache = True, local_cache_size = 4000)
        self.assertEqual(cache._local_cache, None)
        self.assertNotEqual(cache._remote_cache, None)
        cache = Cache(use_local_cache = True, use_remote_cache = False, local_cache_size = 4000)
        self.assertNotEqual(cache._local_cache, None)
        self.assertEqual(cache._local_cache.maxsize, 4000)
        self.assertEqual(cache._remote_cache, None)  
        cache = Cache(use_local_cache = False, use_remote_cache = False, local_cache_size = 4000)
        self.assertEqual(cache._local_cache, None)
        self.assertEqual(cache._remote_cache, None)   

    def test_local_cache(self):
        cache = Cache(use_local_cache = True, use_remote_cache = False, local_cache_size = 3)
        rc = cache._set("1", {"key1": "value1"})
        self.assertEqual(rc, True)
        cached_value = cache._get("1")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("2", {"key2": "value2"})
        self.assertEqual(rc, True)
        cached_value = cache._get("2")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("3", {"key3": "value3"})
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("3", {"key3": "value3"})   # repeat
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("4", {"key4": "value4"})   
        self.assertEqual(rc, True)
        cached_value = cache._get("4")
        self.assertEqual(cached_value['cached'], 'local')    
        cached_value = cache._get("1")             # evicted (FIFO)
        self.assertEqual(cached_value, None)

    def test_remote_cache(self):
        cache = Cache(use_local_cache = False, use_remote_cache = True, local_cache_size = 3)
        rc = cache._set("1", {"key1": "value1"})
        self.assertEqual(rc, True)
        cached_value = cache._get("1")
        self.assertEqual(cached_value['cached'], 'remote')
        rc = cache._set("2", {"key2": "value2"})
        self.assertEqual(rc, True)
        cached_value = cache._get("2")
        self.assertEqual(cached_value['cached'], 'remote')
        rc = cache._set("3", {"key3": "value3"})
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'remote')
        rc = cache._set("3", {"key3": "value3"})   # repeat
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'remote')
        rc = cache._set("4", {"key4": "value4"})   
        self.assertEqual(rc, True)
        cached_value = cache._get("4")
        self.assertEqual(cached_value['cached'], 'remote')    
        cached_value = cache._get("1")
        self.assertEqual(cached_value['cached'], 'remote')

    def test_full_cache(self):
        cache = Cache(use_local_cache = True, use_remote_cache = True, local_cache_size = 3)
        rc = cache._set("1", {"key1": "value1"})
        self.assertEqual(rc, True)
        cached_value = cache._get("1")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("2", {"key2": "value2"})
        self.assertEqual(rc, True)
        cached_value = cache._get("2")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("3", {"key3": "value3"})
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("3", {"key3": "value3"})   # repeat
        self.assertEqual(rc, True)
        cached_value = cache._get("3")
        self.assertEqual(cached_value['cached'], 'local')
        rc = cache._set("4", {"key4": "value4"})   
        self.assertEqual(rc, True)
        cached_value = cache._get("4")
        self.assertEqual(cached_value['cached'], 'local')    
        cached_value = cache._get("1")            # evicted from local
        self.assertEqual(cached_value['cached'], 'remote')
        cached_value = cache._get("1")            # ... but reinserted
        self.assertEqual(cached_value['cached'], 'local')

if __name__ == "__main__":
    unittest.main()


