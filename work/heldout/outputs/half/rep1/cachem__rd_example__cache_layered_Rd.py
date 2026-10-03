# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
from pathlib import Path

# cachem is a specialized R caching library. 
# In Python, joblib.Memory is the standard equivalent for disk caching.
# Since Python manages memory automatically (unlike R's specific cache_mem), 
# we implement the layered approach using joblib for disk and a simple dict for memory.

# Setup disk cache directory
cache_dir = Path(".cache_disk")
cache_dir.mkdir(exist_ok=True)

# r2py:entity:m
# m: Memory cache (approximated by a dictionary or utilizing Python's internal memory)
# Note: Python does not have a built-in "max_size" constrained memory cache like cachem 
# without third party LRU caches, but for direct translation:
m = {} 

# r2py:entity:d
# d: Disk cache
d = joblib.Memory(location=str(cache_dir), verbose=0)

# r2py:entity:cl
# cl: Layered cache
# In Python, we can create a simple wrapper or logic to check 'm' then 'd'.
class LayeredCache:
    def __init__(self, mem_cache, disk_cache):
        self.m = mem_cache
        self.d = disk_cache

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in self.m:
                return self.m[key]
            
            # Use joblib for the disk layer
            result = self.d.cache(func)(*args, **kwargs)
            self.m[key] = result
            return result
        return wrapper

cl = LayeredCache(m, d)