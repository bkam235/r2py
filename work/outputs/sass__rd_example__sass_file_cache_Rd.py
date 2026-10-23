# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import os
import shutil

# In Python, sass caching is typically handled by the library's internal logic 
# or by manually managing temporary directories. 
# Since there is no direct 1:1 object-oriented 'cache' manager like in R's sass package, 
# the equivalent of resetting a sass cache directory is clearing the cache folder.

# r2py:entity:cache
cache_dir = os.environ.get('SASS_CACHE_CONTEXT_DIR', '/tmp/sass_cache')

# r2py:entity:cache$reset
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    os.makedirs(cache_dir)