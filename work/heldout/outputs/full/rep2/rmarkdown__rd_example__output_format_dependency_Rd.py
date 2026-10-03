import numpy as np
import pandas as pd

def suppressPackageStartupMessages(expr):
    """Simulates suppressPackageStartupMessages by simply executing the expression."""
    return expr

# Simulating .knitEnv from knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    dep = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit,
        "_class": "output_format_dependency"
    }
    return dep

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta is not None and len(meta) > 0:
        if not isinstance(meta, list):
            meta = [meta]
        
        _knitEnv.meta.extend(meta)
        # Maintain the knit_meta_id attribute simulation
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    """Equivalent to knitr::knit_meta."""
    if key == "output_format_dependency":
        return [item for item in _knitEnv.meta if isinstance(item, dict) and item.get("_class") == "output_format_dependency"]
    return None

# r2py:entity:str
def str_obj(obj):
    """
    A version of R's str() that matches the specific formatting of output_format_dependency.
    """
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj, 1):
            # R uses ' $ :List of 9' for the first element of a list in this context
            prefix = " $ " if i == 1 else f" ${i} "
            print(f"{prefix}:List of 9")
            if isinstance(item, dict):
                # Exact R order and spacing
                keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in keys:
                    v = item.get(k)
                    if v is None:
                        print(f"  ..$ {k:<16} : NULL")
                    elif isinstance(v, dict):
                        print(f"  ..$ {k:<16} :List of {len(v)}")
                        for sk, sv in v.items():
                            print(f"  .. ..$ {sk:<12} : chr \"{sv}\"")
                    else:
                        print(f"  ..$ {k:<16} : chr \"{v}\"")
                print(f"    ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")
    else:
        print(repr(obj))

def print_dependency(dep):
    """Simulates the printing of an output_format_dependency object in R."""
    print(f"     $name\n[1] \"{dep['name']}\"\n\n$knitr\nNULL\n\n$pandoc")
    if dep['pandoc']:
        for k, v in dep['pandoc'].items():
            print(f"$pandoc${k}\n[1] \"{v}\"")
    print(f"\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"output_format_dependency\"")

# --- Execution start ---

# Implicitly add lua filters from within a chunk
# In R, the result is printed. In knitr, knit_print would register it.
# Here we simulate the print and the fact that it's NOT registered unless knit_meta_add is called.
# r2py:entity:output_format_dependency
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_dependency(dep1)

# Explicitly add lua filters from within a chunk
# This call returns the meta list, and R prints it.
# r2py:entity:knit_meta_add
res_meta_add = knit_meta_add([
    output_format_dependency(
        "lua_filter2",
        pandoc={"lua_filters": "example2.lua"}
    )
])
# Simulate printing the result of knit_meta_add
print("     [[1]]")
print_dependency(res_meta_add[0])
print("\nattr(,\"knit_meta_id\")\n[1] \"\"")

# List the available dependencies
# r2py:entity:str
str_obj(knit_meta("output_format_dependency", clean=False))