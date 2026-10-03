# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
from pathlib import Path

# Python does not have a direct equivalent to R's cachem layered cache in a single object.
# The most common industry standard for memory/disk caching is joblib.Memory.
# Since cachem's layered cache handles memory first then disk, we approximate this
# by utilizing joblib's disk caching and relying on Python's internal object 
# referencing for the memory component.

# Define disk cache directory
# r2py:entity:d
cache_dir = Path("./.joblib_cache")
cache_dir.mkdir(exist_ok=True)

# m: approximated as a memory-based cache (using joblib.Memory with a temporary directory or a dict)
# However, to preserve the 'layered' logic (cl), we implement cl as the primary interface.
# r2py:entity:m
m = {} # Simple dictionary to simulate memory cache

# d: disk cache mapping
d = joblib.Memory(location=cache_dir, verbose=0)

# r2py:entity:cl
# cl: layered cache
# In Python, the 'layered' approach is typically handled by custom decorators or 
# joblib's built-in persistence. We define cl as the joblib Memory object 
# because it manages the disk-backend and internal memory-caching of results.
cl = d