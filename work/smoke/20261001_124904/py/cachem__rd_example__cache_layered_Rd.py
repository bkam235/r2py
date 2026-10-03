# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import shutil
import tempfile
import pickle
from collections import OrderedDict
from datetime import datetime

class KeyMissing:
    """Sentinel object to indicate a cache miss."""
    def __repr__(self):
        return "<key_missing>"

def is_key_missing(x):
    return isinstance(x, KeyMissing)

# r2py:entity:m
class CacheMem:
    def __init__(self, max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), 
                 evict="lru", missing=KeyMissing(), logfile=None):
        self.max_size = max_size
        self.max_age = max_age
        self.max_n = max_n
        self.evict = evict
        self.missing = missing
        self.logfile = logfile
        
        self.cache = OrderedDict()  # Stores (value, size, mtime)
        self.total_size = 0
        
    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] cache_mem {text}\n")

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key \"{key}\"")
        
        if key not in self.cache:
            self._log(f"get: key \"{key}\" is missing")
            return missing
            
        value, size, mtime = self.cache[key]
        
        if self.max_age != float('inf'):
            if (datetime.now().timestamp() - mtime) > self.max_age:
                self._log(f"pruning single object exceeding max_age: Removing {key}")
                self.remove(key)
                return missing
        
        if self.evict == "lru":
            self.cache.move_to_end(key)
            
        self._log(f"get: key \"{key}\" found")
        return value

    def set(self, key, value):
        self._log(f"set: key \"{key}\"")
        # Approximation of R's object.size
        size = len(pickle.dumps(value))
        
        if key in self.cache:
            self.remove(key)
            
        self.cache[key] = (value, size, datetime.now().timestamp())
        self.total_size += size
        
        # Eviction logic
        while (self.max_size != float('inf') and self.total_size > self.max_size) or \
              (self.max_n != float('inf') and len(self.cache) > self.max_n):
            if not self.cache:
                break
            # FIFO or LRU both pop the first item in an OrderedDict if we move_to_end on get/set
            k, (v, s, t) = self.cache.popitem(last=False)
            self.total_size -= s
            self._log(f"evicting {k}")

    def exists(self, key):
        return key in self.cache

    def keys(self):
        return list(self.cache.keys())

    def remove(self, key):
        if key in self.cache:
            _, size, _ = self.cache.pop(key)
            self.total_size -= size

    def reset(self):
        self.cache.clear()
        self.total_size = 0

def cache_mem(max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), 
              evict="lru", missing=KeyMissing(), logfile=None):
    return CacheMem(max_size, max_age, max_n, evict, missing, logfile)

# r2py:entity:d
class CacheDisk:
    def __init__(self, dir=None, max_size=1024 * 1024**2, max_age=float('inf'), 
                 max_n=float('inf'), evict="lru", destroy_on_finalize=False, 
                 read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), 
                 prune_rate=20, warn_ref_objects=False, logfile=None):
        self.dir = dir if dir else tempfile.mkdtemp(prefix="cache_disk-")
        if not os.path.exists(self.dir):
            os.makedirs(self.dir, exist_ok=True)
            
        self.max_size = max_size
        self.max_age = max_age
        self.max_n = max_n
        self.evict = evict
        self.extension = extension
        self.missing = missing
        self.logfile = logfile
        self.read_fn = read_fn if read_fn else self._default_read
        self.write_fn = write_fn if write_fn else self._default_write
        
    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] cache_disk {text}\n")

    def _default_read(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def _default_write(self, value, path):
        with open(path, 'wb') as f:
            pickle.dump(value, f)

    def _key_to_path(self, key):
        # Simple sanitization for filename
        safe_key = "".join([c if c.isalnum() else "_" for c in str(key)])
        return os.path.join(self.dir, safe_key + self.extension)

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key \"{key}\"")
        path = self._key_to_path(key)
        
        if not os.path.exists(path):
            return missing
            
        try:
            value = self.read_fn(path)
            # LRU update: touch the file
            if self.evict == "lru":
                os.utime(path, None)
            return value
        except Exception:
            return missing

    def set(self, key, value):
        self._log(f"set: key \"{key}\"")
        path = self._key_to_path(key)
        self.write_fn(value, path)
        
        # Pruning logic based on folder size
        files = [os.path.join(self.dir, f) for f in os.listdir(self.dir)]
        total_size = sum(os.path.getsize(f) for f in files)
        
        if self.max_size != float('inf') and total_size > self.max_size:
            # Sort by mtime (oldest first) for LRU/FIFO
            files.sort(key=os.path.getmtime)
            while total_size > self.max_size and files:
                f = files.pop(0)
                total_size -= os.path.getsize(f)
                os.remove(f)

    def exists(self, key):
        return os.path.exists(self._key_to_path(key))

    def keys(self):
        return [f.replace(self.extension, "") for f in os.listdir(self.dir)]

    def remove(self, key):
        path = self._key_to_path(key)
        if os.path.exists(path):
            os.remove(path)

    def reset(self):
        shutil.rmtree(self.dir)
        os.makedirs(self.dir, exist_ok=True)

def cache_disk(dir=None, max_size=1024 * 1024**2, max_age=float('inf'), 
               max_n=float('inf'), evict="lru", destroy_on_finalize=False, 
               read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), 
               prune_rate=20, warn_ref_objects=False, logfile=None):
    return CacheDisk(dir, max_size, max_age, max_n, evict, destroy_on_finalize, 
                     read_fn, write_fn, extension, missing, prune_rate, warn_ref_objects, logfile)

# r2py:entity:cl
class CacheLayered:
    def __init__(self, *caches, logfile=None):
        self.caches = list(caches)
        self.logfile = logfile
        
    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] cache_layered {text}\n")

    def get(self, key):
        self._log(f"Get: {key}")
        value = None
        for i, cache in enumerate(self.caches):
            value = cache.get(key)
            if not is_key_missing(value):
                self._log(f"Get from {type(cache).__name__}... hit")
                # Backfill higher layers
                for j in range(i):
                    self.caches[j].set(key, value)
                return value
            else:
                self._log(f"Get from {type(cache).__name__}... miss")
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

# Main execution
# r2py:entity:m
m = cache_mem(max_size=100 * 1024**2)
# r2py:entity:d
d = cache_disk(max_size=2 * 1024**3)
# r2py:entity:cl
cl = cache_layered(m, d)