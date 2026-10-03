# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sass
import os
import shutil

# In Python's libsass/sass, caching is typically handled by the 
# underlying C implementation or through manual file management.
# The R 'sass' package uses a specific cache context directory.
# To replicate 'sass_file_cache' and 'reset()', we target the cache directory.

# r2py:entity:cache
# Define the cache directory (approximating sass_cache_context_dir)
cache_dir = os.path.join(os.environ.get('TEMP', '/tmp'), 'sass_cache')

# r2py:entity:cache$reset
# cache$reset() equivalent: remove the cache directory contents
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
os.makedirs(cache_dir, exist_ok=True)

# 'cache' object mapping (mimicking the structure for subsequent use)
class SassCache:
    def __init__(self, directory):
        self.directory = directory
    def reset(self):
        shutil.rmtree(self.directory)
        os.makedirs(self.directory, exist_ok=True)

cache = SassCache(cache_dir)
# r2py:entity:cache$reset
cache.reset()