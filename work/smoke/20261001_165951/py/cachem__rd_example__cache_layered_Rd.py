# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
import shutil
from pathlib import Path

# cachem doesn't have a 1:1 direct Python library for "layered" memory/disk caching 
# with specific size limits in a single object. 
# We implement this using joblib.Memory for disk and a dictionary/LRU for memory.

# Define cache directories
# r2py:entity:d
disk_cache_dir = './.disk_cache'
max_disk_size = 2 * 1024**3  # 2 GB

# d: disk cache (using joblib)
d = joblib.Memory(disk_cache_dir, verbose=0)

# r2py:entity:m
# m: memory cache (simulated with a dict, as Python handles memory dynamically)
# To strictly mimic max_size, one would use functools.lru_cache or a custom class
m = {} 

# r2py:entity:cl
# cl: layered cache (logic wrapper)
class LayeredCache:
    def __init__(self, mem_cache, disk_cache):
        self.m = mem_cache
        self.d = disk_cache

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            # Check memory first
            if key in self.m:
                return self.m[key]
            # Check disk second
            try:
                # joblib.Memory wraps the function call
                result = self.d.cache(func)(*args, **kwargs)
                self.m[key] = result
                return result
            except Exception:
                result = func(*args, **kwargs)
                self.m[key] = result
                return result
        return wrapper

cl = LayeredCache(m, d)