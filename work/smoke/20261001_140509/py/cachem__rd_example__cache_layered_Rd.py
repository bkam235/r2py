# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import shutil
import tempfile
import time
import pickle
from collections import OrderedDict

class KeyMissing:
    """Sentinel object to indicate a cache miss."""
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

    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] cache_mem {text}\n")

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key {key}")
        if key not in self.cache:
            self._log(f"get: key {key} is missing")
            return missing
        
        val_data = self.cache[key]
        if self.max_age != float('inf'):
            if time.time() - val_data['mtime'] > self.max_age:
                self._log(f"pruning single object exceeding max_age: Removing {key}")
                self.remove(key)
                return missing

        if self.evict == "lru":
            self.cache.move_to_end(key)
        
        self._log(f"get: key {key} found")
        return val_data['value']

    def set(self, key, value):
        self._log(f"set: key {key}")
        size = len(pickle.dumps(value)) if self.max_size != float('inf') else 0
        
        if key in self.cache:
            self.total_size -= self.cache[key]['size']
        
        self.cache[key] = {'value': value, 'size': size, 'mtime': time.time()}
        self.total_size += size
        
        if self.evict == "lru":
            self.cache.move_to_end(key)

        while (self.max_size != float('inf') and self.total_size > self.max_size) or \
              (self.max_n != float('inf') and len(self.cache) > self.max_n):
            if not self.cache:
                break
            # Pop first item (LRU or FIFO)
            k, v = self.cache.popitem(last=False)
            self.total_size -= v['size']

    def exists(self, key):
        return key in self.cache

    def keys(self):
        return list(self.cache.keys())

    def remove(self, key):
        if key in self.cache:
            self.total_size -= self.cache[key]['size']
            del self.cache[key]

    def reset(self):
        self._log("reset")
        self.cache.clear()
        self.total_size = 0

def cache_mem(max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", missing=KeyMissing(), logfile=None):
    return CacheMem(max_size, max_age, max_n, evict, missing, logfile)

# r2py:entity:d
class CacheDisk:
    def __init__(self, dir=None, max_size=1024 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", destroy_on_finalize=False, read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), prune_rate=20, warn_ref_objects=False, logfile=None):
        if dir is None:
            dir = tempfile.mkdtemp(prefix="cache_disk-")
        self.dir = os.path.abspath(dir)
        os.makedirs(self.dir, exist_ok=True)
        
        self.max_size = max_size
        self.max_age = max_age
        self.max_n = max_n
        self.evict = evict
        self.extension = extension
        self.missing = missing
        self.logfile = logfile
        self.read_fn = read_fn or self._default_read
        self.write_fn = write_fn or self._default_write
        self.destroy_on_finalize = destroy_on_finalize

    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] cache_disk {text}\n")

    def _default_read(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def _default_write(self, value, filename):
        with open(filename, 'wb') as f:
            pickle.dump(value, f)

    def _key_to_filename(self, key):
        # Simple hash-based filename to avoid illegal characters
        import hashlib
        hashed = hashlib.sha256(str(key).encode()).hexdigest()
        return os.path.join(self.dir, hashed + self.extension)

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key {key}")
        filename = self._key_to_filename(key)
        if not os.path.exists(filename):
            return missing
        
        try:
            value = self.read_fn(filename)
            if self.evict == "lru":
                os.utime(filename, None)
            return value
        except Exception:
            return missing

    def set(self, key, value):
        self._log(f"set: key {key}")
        filename = self._key_to_filename(key)
        self.write_fn(value, filename)

    def exists(self, key):
        return os.path.exists(self._key_to_filename(key))

    def keys(self):
        return [f for f in os.listdir(self.dir) if f.endswith(self.extension)]

    def remove(self, key):
        filename = self._key_to_filename(key)
        if os.path.exists(filename):
            os.remove(filename)

    def reset(self):
        shutil.rmtree(self.dir)
        os.makedirs(self.dir, exist_ok=True)

    def destroy(self):
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)

def cache_disk(dir=None, max_size=1024 * 1024**2, max_age=float('inf'), max_n=float('inf'), evict="lru", destroy_on_finalize=False, read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), prune_rate=20, warn_ref_objects=False, logfile=None):
    return CacheDisk(dir, max_size, max_age, max_n, evict, destroy_on_finalize, read_fn, write_fn, extension, missing, prune_rate, warn_ref_objects, logfile)

# r2py:entity:cl
class CacheLayered:
    def __init__(self, *caches, logfile=None):
        self.caches = list(caches)
        self.logfile = logfile

    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] cache_layered {text}\n")

    def get(self, key):
        self._log(f"Get: {key}")
        for i, cache in enumerate(self.caches):
            value = cache.get(key)
            if not is_key_missing(value):
                self._log(f"Get from {type(cache).__name__}... hit")
                for j in range(i):
                    self.caches[j].set(key, value)
                return value
            else:
                self._log(f"Get from {type(cache).__name__}... miss")
        return KeyMissing()

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

# --- Example execution ---
# r2py:entity:m
m = cache_mem(max_size=100 * 1024**2)
# r2py:entity:d
d = cache_disk(max_size=2 * 1024**3)
# r2py:entity:cl
cl = cache_layered(m, d)