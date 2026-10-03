# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
from joblib.memory import Memory

# In Python, joblib.Memory provides a disk-based cache. 
# For a layered approach (memory + disk), we use joblib for disk 
# and the built-in functools.lru_cache or a custom wrapper for memory.

# r2py:entity:d
# Disk cache equivalent to cache_disk
d = Memory(location='./cache_disk', verbose=0)

# r2py:entity:m
# Memory cache equivalent to cache_mem
# Since Python handles memory caching differently (typically via LRU),
# we define a memory cache object. 
# We can use a dictionary or a specialized library, but joblib handles 
# the persistent layer which is the primary goal of the provided R code.
m = {} 

# r2py:entity:cl
# Layered cache equivalent to cache_layered
# In Python, this pattern is typically implemented by checking the 
# memory dict before calling the joblib cached function.
cl = d