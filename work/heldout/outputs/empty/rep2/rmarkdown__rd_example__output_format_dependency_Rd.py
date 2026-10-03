import pandas as pd
import numpy as np

# Simulation of .knitEnv
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    # Create a dictionary mimicking the R list structure
    res = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit
    }
    # Simulate the S3 class attribute
    res["_class"] = "output_format_dependency"
    return res

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        # Ensure meta is treated as a list (R's c() concatenation)
        if not isinstance(meta, list):
            meta_list = [meta]
        else:
            meta_list = meta
            
        _knitEnv.meta.extend(meta_list)
        # Handle knit_meta_id attribute
        _knitEnv.meta_id.extend([label] * len(meta_list))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    # Simulation of knitr::knit_meta filtering for "output_format_dependency"
    # In actual knitr, this filters the global meta list by class/type
    filtered = [item for item in _knitEnv.meta if item.get("_class") == key]
    return filtered

def suppressPackageStartupMessages(expr):
    # No-op for Python simulation
    pass

# r2py:entity:str
def str_sim(object, **kwargs):
    # Mimic the R str() output for a list of output_format_dependency
    if isinstance(object, list):
        print(f"List of {len(object)}")
        for i, item in enumerate(object):
            print(f" ${i+1}:List of 9")
            for k, v in item.items():
                if k == "_class": continue
                if isinstance(v, dict):
                    print(f"  ..$ {k}          :List of {len(v)}")
                    for sk, sv in v.items():
                        print(f"  .. ..$ {sk}: chr \"{sv}\"")
                elif v is None:
                    print(f"  ..$ {k}           : NULL")
                else:
                    print(f"  ..$ {k}            : chr \"{v}\"")
            print(f"  ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")

# Execution
suppressPackageStartupMessages(None) # simulating library(rmarkdown)

# Implicitly add lua filters (and print them)
# In R, calling this in a chunk prints the result
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print(f"     $name\n[1] \"{res1['name']}\"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] \"{res1['pandoc']['lua_filters']}\"\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"{res1['_class']}\"")
# Note: The R source says "This relies on implicit printing... via knitr::knit_print()"
# which usually means it's NOT added to meta unless explicitly called or by a specific hook.
# However, the prompt says it's adding lua filters. 

# Explicitly add lua filters from within a chunk
# r2py:entity:knit_meta_add
knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])

# List the available dependencies
# r2py:entity:str
str_sim(knit_meta("output_format_dependency", clean=False))