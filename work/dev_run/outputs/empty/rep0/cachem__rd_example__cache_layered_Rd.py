# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
from joblib.memory import Memory

# Python does not have a direct equivalent to the 'cachem' layered cache system 
# that automatically overflows from RAM to Disk. 
# joblib.Memory provides disk-based caching.
# For a layered approach, we can define specific directories for 'm' (simulated via /tmp or RAM disk) 
# and 'd' (persistent disk).

# r2py:entity:m
# m: simulated memory cache (using a temporary directory or high-speed path)
m = Memory(location='/tmp/cache_mem', verbose=0)

# r2py:entity:d
# d: disk cache
d = Memory(location='./cache_disk', verbose=0)

# r2py:entity:cl
# cl: layered cache approximation
# In Python, we can create a wrapper or simply use the disk cache as the primary 
# since joblib handles the serialization/deserialization.
cl = d