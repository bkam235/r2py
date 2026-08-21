# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 10

import time
import pickle
import os
import glob
from pathlib import Path

# Temporary cache file base
# r2py:entity:f
f = "cache_file.pkl"

# r2py:entity:compute
def compute(*args, **kwargs):
    # Check if 'rerun' is True in kwargs
    rerun = kwargs.get('rerun', False)
    
    # In xfun::cache_rds, the cache is based on the function arguments.
    # For simplicity, we use a basic pickle cache here.
    if not os.path.exists(f) or rerun:
        # Simulate heavy computation
        time.sleep(1)
        res = list(range(1, 11))
        
        # Save to cache
        with open(f, 'wb') as pickle_file:
            pickle.dump(res, pickle_file)
    else:
        # Load from cache
        with open(f, 'rb') as pickle_file:
            res = pickle.load(pickle_file)
            
    return res

# takes one second
# r2py:entity:compute_1
print(compute()) 
# returns [1, ..., 10] immediately
# r2py:entity:compute_2
print(compute()) 
# fast again
# r2py:entity:compute_3
print(compute()) 
# one second to rerun
# r2py:entity:compute_4
print(compute(rerun=True)) 
# r2py:entity:compute_5
print(compute())

# Clean up
# r2py:entity:unlink
if os.path.exists(f):
    os.remove(f)