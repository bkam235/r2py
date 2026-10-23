# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# cachem does not have a direct equivalent in standard Python libraries.
# A common substitute for layered caching is using joblib with a disk backend 
# or a custom dictionary for memory caching.
from joblib import Memory

# Approximate implementation of layered cache logic
# Memory cache (m)
# r2py:entity:m
m = {} 

# Disk cache (d)
# r2py:entity:d
d = Memory(location='./cache_disk', verbose=0)

# Layered cache (cl) wrapper logic
# r2py:entity:cl
class LayeredCache:
    def __init__(self, mem_cache, disk_cache):
        self.mem = mem_cache
        self.disk = disk_cache

    def __setitem__(self, key, value):
        self.mem[key] = value
        self.disk.cacheable(lambda x: value)(key)

    def __getitem__(self, key):
        if key in self.mem:
            return self.mem[key]
        # Simplified disk retrieval
        return self.disk.cacheable(lambda x: None)(key)

cl = LayeredCache(m, d)