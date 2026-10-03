# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import cachetools
import diskcache

# m <- cache_mem(max_size = 100 * 1024^2)
# Note: cachetools LRUCache maxsize is usually number of items, 
# but we use it here to approximate the memory cache.
# r2py:entity:m
m = cachetools.LRUCache(maxsize=100 * 1024**2)

# d <- cache_disk(max_size = 2 * 1024^3)
# r2py:entity:d
d = diskcache.Cache(size_limit=2 * 1024**3)

# cl <- cache_layered(m, d)
# Python does not have a direct 'cache_layered' object like cachem.
# We implement a simple wrapper class to achieve the layered behavior.
# r2py:entity:cl
class CacheLayered:
    def __init__(self, mem_cache, disk_cache):
        self.m = mem_cache
        self.d = disk_cache

    def __setitem__(self, key, value):
        self.m[key] = value
        self.d[key] = value

    def __getitem__(self, key):
        if key in self.m:
            return self.m[key]
        if key in self.d:
            val = self.d[key]
            self.m[key] = val
            return val
        raise KeyError(key)

    def __contains__(self, key):
        return key in self.m or key in self.d

cl = CacheLayered(m, d)