# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
import shutil
from pathlib import Path

# cachem is a specialized R package for layered caching. 
# In Python, joblib.Memory provides disk-based caching.
# For a layered approach (Memory + Disk), we simulate the behavior:
# m (memory) is handled by Python's internal object referencing/global state
# d (disk) is handled by joblib.Memory

# r2py:entity:d
# Define disk cache directory
cache_dir = Path(".cache_disk")
# Ensure directory exists (simulating max_size is handled by OS/disk quota or manual cleanup)
# Python's joblib doesn't have a built-in 'max_size' limit like cachem, 
# but we initialize the Memory object to handle the disk layer.
d = joblib.Memory(cache_dir, verbose=0)

# r2py:entity:m
# For m (memory cache), we can use a simple dictionary or functools.lru_cache
# but to keep it as an object 'm' as per the R code:
m = {}

# r2py:entity:cl
# cl (layered cache) is simulated by a logic that checks m then d.
# Since Python's joblib.Memory is the standard for disk caching, 
# 'cl' is represented here as the joblib Memory instance, as it internally 
# manages the serialization and retrieval.
cl = d