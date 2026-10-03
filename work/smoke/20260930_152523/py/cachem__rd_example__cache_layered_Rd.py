# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import shutil
import tempfile
import pickle
from collections import OrderedDict

class KeyMissing:
    """Sentinel object to indicate a key is missing from the cache."""
    def __repr__(self):
        return "<key_missing>"

def is_key_missing(x):
    return isinstance(x, KeyMissing)

# r2py:entity:m
class CacheMem:
    def __init__(self, max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", missing=KeyMissing(), logfile=None):
        self.max_size = max_size
        self.max_age = max_age
        self.max_n = max_n
        self.evict = evict
        self.missing = missing
        self.logfile = logfile
        self.cache = OrderedDict()
        self.total_size = 0

    def _get_obj_size(self, value):
        # Approximation of R's object.size
        return len(pickle.dumps(value))

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        if key not in self.cache:
            return missing
        
        val, size, mtime = self.cache[key]
        # In a real implementation, we would check max_age here
        if self.evict == "lru":
            self.cache.move_to_end(key)
        return val

    def set(self, key, value):
        size = self._get_obj_size(value)
        if key in self.cache:
            self.total_size -= self.cache[key][1]
        
        self.cache[key] = (value, size, 0) # simplified mtime
        self.total_size += size
        
        # Simple eviction logic
        while (self.max_n != float('inf') and len(self.cache) > self.max_n) or \
              (self.max_size != float('inf') and self.total_size > self.max_size):
            k, v = self.cache.popitem(last=False)
            self.total_size -= v[1]

    def exists(self, key):
        return key in self.cache

    def keys(self):
        return list(self.cache.keys())

    def remove(self, key):
        if key in self.cache:
            self.total_size -= self.cache[key][1]
            del self.cache[key]

    def reset(self):
        self.cache.clear()
        self.total_size = 0

def cache_mem(max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", missing=KeyMissing(), logfile=None):
    return CacheMem(max_size, max_age, max_n, evict, missing, logfile)

# r2py:entity:d
class CacheDisk:
    def __init__(self, dir=None, max_size=1024 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", destroy_on_finalize=False, read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), prune_rate=20, warn_ref_objects=False, logfile=None):
        self.dir = dir if dir else tempfile.mkdtemp(prefix="cache_disk-")
        self.max_size = max_size
        self.max_age = max_age
        self.max_n = max_n
        self.evict = evict
        self.extension = extension
        self.missing = missing
        self.logfile = logfile
        self.read_fn = read_fn if read_fn else self._default_read
        self.write_fn = write_fn if write_fn else self._default_write

    def _default_read(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def _default_write(self, value, path):
        with open(path, 'wb') as f:
            pickle.dump(value, f)

    def _key_to_path(self, key):
        # Basic implementation of key to filename
        safe_key = str(key).replace("/", "_").replace("\\", "_")
        return os.path.join(self.dir, safe_key + self.extension)

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        path = self._key_to_path(key)
        if not os.path.exists(path):
            return missing
        try:
            return self.read_fn(path)
        except:
            return missing

    def set(self, key, value):
        path = self._key_to_path(key)
        self.write_fn(value, path)

    def exists(self, key):
        return os.path.exists(self._key_to_path(key))

    def keys(self):
        return [os.path.basename(f).replace(self.extension, "") for f in os.listdir(self.dir)]

    def remove(self, key):
        path = self._key_to_path(key)
        if os.path.exists(path):
            os.remove(path)

    def reset(self):
        for f in os.listdir(self.dir):
            os.remove(os.path.join(self.dir, f))

def cache_disk(dir=None, max_size=1024 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", destroy_on_finalize=False, read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), prune_rate=20, warn_ref_objects=False, logfile=None):
    return CacheDisk(dir, max_size, max_age, max_n, evict, destroy_on_finalize, read_fn, write_fn, extension, missing, prune_rate, warn_ref_objects, logfile)

# r2py:entity:cl
class CacheLayered:
    def __init__(self, *caches, logfile=None):
        self.caches = list(caches)
        self.logfile = logfile

    def get(self, key):
        value = None
        for i, cache in enumerate(self.caches):
            value = cache.get(key)
            if not is_key_missing(value):
                for j in range(i):
                    self.caches[j].set(key, value)
                return value
        return value

    def set(self, key, value):
        for cache in self.caches:
            cache.set(key, value)

    def exists(self, key):
        for cache in self.caches:
            if cache.exists(key):
                return True
        return False

    def keys(self):
        all_keys = []
        for cache in self.caches:
            all_keys.extend(cache.keys())
        return list(set(all_keys))

    def remove(self, key):
        for cache in self.caches:
            cache.remove(key)

    def reset(self):
        for cache in self.caches:
            cache.reset()

    def get_caches(self):
        return self.caches

def cache_layered(*caches, logfile=None):
    return CacheLayered(*caches, logfile=logfile)

# r2py:entity:m
m = cache_mem(max_size=100 * 1024**2)
# r2py:entity:d
d = cache_disk(max_size=2 * 1024**3)
# r2py:entity:cl
cl = cache_layered(m, d)