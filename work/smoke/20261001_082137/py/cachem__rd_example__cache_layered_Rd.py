# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import shutil
import tempfile
import time
import pickle
from collections import OrderedDict

class KeyMissing:
    pass

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
        self.cache = OrderedDict()
        self.total_size = 0

    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] cache_mem {text}\n")

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key \"{key}\"")
        if key not in self.cache:
            self._log(f"get: key \"{key}\" is missing")
            return missing
        
        val_data = self.cache[key]
        if self.max_age != float('inf'):
            if time.time() - val_data['mtime'] > self.max_age:
                self._log(f"pruning single object exceeding max_age: Removing {key}")
                self.remove(key)
                return missing

        if self.evict == "lru":
            self.cache.move_to_end(key)
        
        self._log(f"get: key \"{key}\" found")
        return val_data['value']

    def set(self, key, value):
        self._log(f"set: key \"{key}\"")
        size = len(pickle.dumps(value)) if self.max_size != float('inf') else 0
        
        if key in self.cache:
            self.total_size -= self.cache[key]['size']
        
        self.cache[key] = {'value': value, 'size': size, 'mtime': time.time()}
        self.total_size += size
        
        if self.evict == "lru":
            self.cache.move_to_end(key)

        while (self.max_size != float('inf') and self.total_size > self.max_size) or \
              (self.max_n != float('inf') and len(self.cache) > self.max_n):
            self._evict()

    def _evict(self):
        if not self.cache:
            return
        if self.evict == "lru":
            key, val = self.cache.popitem(last=False)
        else: # fifo
            key, val = self.cache.popitem(last=False)
        self.total_size -= val['size']

    def exists(self, key):
        return key in self.cache

    def keys(self):
        return list(self.cache.keys())

    def remove(self, key):
        if key in self.cache:
            self.total_size -= self.cache[key]['size']
            del self.cache[key]

    def reset(self):
        self.cache.clear()
        self.total_size = 0

def cache_mem(max_size=512 * 1024**2, max_age=float('inf'), max_n=float('inf'), 
              evict="lru", missing=KeyMissing(), logfile=None):
    return CacheMem(max_size=max_size, max_age=max_age, max_n=max_n, 
                    evict=evict, missing=missing, logfile=logfile)

# r2py:entity:d
class CacheDisk:
    def __init__(self, dir=None, max_size=1024 * 1024**2, max_age=float('inf'), 
                 max_n=float('inf'), evict="lru", destroy_on_finalize=False, 
                 read_fn=None, write_fn=None, extension=".rds", missing=KeyMissing(), 
                 prune_rate=20, warn_ref_objects=False, logfile=None):
        self.dir = dir if dir else tempfile.gettempdir()
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

    def _default_read(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def _default_write(self, value, path):
        with open(path, 'wb') as f:
            pickle.dump(value, f)

    def _log(self, text):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] cache_disk {text}\n")

    def _key_to_path(self, key):
        # Simple mapping of key to safe filename
        safe_key = "".join([c for c in str(key) if c.isalnum() or c in (' ', '.', '_', '-')]).strip()
        return os.path.join(self.dir, safe_key + self.extension)

    def get(self, key, missing=None):
        if missing is None:
            missing = self.missing
        self._log(f"get: key \"{key}\"")
        path = self._key_to_path(key)
        if not os.path.exists(path):
            return missing
        
        try:
            return self.read_fn(path)
        except Exception:
            return missing

    def set(self, key, value):
        self._log(f"set: key \"{key}\"")
        path = self._key_to_path(key)
        self.write_fn(value, path)

    def exists(self, key):
        return os.path.exists(self._key_to_path(key))

    def keys(self):
        return [f.replace(self.extension, "") for f in os.listdir(self.dir) if f.endswith(self.extension)]

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
    return CacheDisk(dir=dir, max_size=max_size, max_age=max_age, max_n=max_n, 
                     evict=evict, destroy_on_finalize=destroy_on_finalize, 
                     read_fn=read_fn, write_fn=write_fn, extension=extension, 
                     missing=missing, prune_rate=prune_rate, 
                     warn_ref_objects=warn_ref_objects, logfile=logfile)

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
        value = None
        for i, cache in enumerate(self.caches):
            value = cache.get(key)
            if not is_key_missing(value):
                self._log(f"Get from {type(cache).__name__}... hit")
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

# r2py:entity:m
m = cache_mem(max_size=100 * 1024**2)
# r2py:entity:d
d = cache_disk(max_size=2 * 1024**3)
# r2py:entity:cl
cl = cache_layered(m, d)