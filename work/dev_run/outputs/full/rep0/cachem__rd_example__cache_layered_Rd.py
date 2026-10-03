# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
import shutil
from pathlib import Path

# Python does not have a direct 1:1 equivalent to cachem's layered cache objects.
# joblib.Memory is the standard for disk caching.
# For memory caching, we use a simple dictionary or joblib's internal mechanisms.

# Define sizes
MAX_MEM_SIZE = 100 * 1024**2
MAX_DISK_SIZE = 2 * 1024**3
CACHE_DIR = ".cache_disk"

# r2py:entity:m
# m: Approximation of memory cache (using a dictionary-based approach or just a placeholder)
m = {} 

# r2py:entity:d
# d: Approximation of disk cache using joblib
# joblib.Memory handles the disk caching logic
d = joblib.Memory(CACHE_DIR, verbose=0)

# r2py:entity:cl
# cl: Approximation of layered cache. 
# Since Python's joblib handles the "check if exists on disk" logic automatically,
# we create a wrapper or simply use the joblib instance as the primary interface.
cl = d