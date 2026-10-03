# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import joblib
import os
from joblib.memory import Memory

# Python does not have a direct 1:1 equivalent to cachem's layered memory/disk cache.
# joblib.Memory provides a disk-based cache. For a tiered approach, 
# we initialize a disk cache to simulate 'd' and 'cl'.
# Since Python handles memory management automatically, 'm' (mem cache) 
# is typically handled by the OS or specific LRU decorators, 
# but for this translation, we use joblib for the persistence layer.

# r2py:entity:m
m = {} # Simple dictionary to simulate memory cache
# r2py:entity:d
d = Memory(location='./cache_disk', verbose=0) # Disk cache
# r2py:entity:cl
cl = d # Layered cache approximated by the disk cache manager