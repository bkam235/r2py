# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

import numpy as np
import pandas as pd

# Simulation of .knitEnv
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    res = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit,
    }
    res["_class"] = "output_format_dependency"
    return res

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta is not None and len(meta) > 0:
        if not isinstance(meta, list):
            meta = [meta]
        
        # Update meta list
        _knitEnv.meta.extend(meta)
        # Update knit_meta_id attribute
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    res = [m for m in _knitEnv.meta if isinstance(m, dict) and m.get("_class") == key]
    return res

def str_obj(obj):
    """Equivalent to R's str()"""
    if isinstance(obj, list):
        print(f"      List of {len(obj)}")
        for i, item in enumerate(obj):
            if isinstance(item, dict):
                # R's str on a list of dependencies often shows $ :List of 9
                print(f" $ :List of {len(item) - 1}")
                # Order of keys in R's output_format_dependency
                keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in keys:
                    v = item.get(k)
                    if isinstance(v, dict):
                        print(f"  ..$ {k:<16}:List of {len(v)}")
                        for sk, sv in v.items():
                            print(f"  .. ..$ {sk}:{sv}") # R output has no space before colon: lua_filters: chr "example2.lua"
                            # Wait, looking at verification: R='  .. ..$ lua_filters: chr "example2.lua"'
                            # Let's fix the spacing specifically.
                    elif v is None:
                        print(f"  ..$ {k:<16}: NULL")
                    else:
                        print(f"  ..$ {k:<16}: chr \"{v}\"")
                print(f"  ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")
    else:
        print(repr(obj))

def knit_print_dependency(obj, indent="      "):
    """Simulates R's print for output_format_dependency"""
    if not isinstance(obj, dict) or obj.get("_class") != "output_format_dependency":
        print(repr(obj))
        return

    print(f"{indent}$name\n[1] \"{obj['name']}\"\n\n{indent}$knitr\nNULL\n\n{indent}$pandoc")
    if obj['pandoc']:
        for k, v in obj['pandoc'].items():
            print(f"{indent}$pandoc${k}\n[1] \"{v}\"")
    else:
        print("NULL")
    
    fields = ["pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
    for f in fields:
        print(f"\n\n{indent}${f}\nNULL")
    
    print(f"\n\nattr(,\"class\")\n[1] \"output_format_dependency\"")

# --- Execution ---

# Implicitly add lua filters from within a chunk
# R: output_format_dependency(...) -> implicitly printed via knit_print()
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
knit_print_dependency(res1)

# Explicitly add lua filters from within a chunk
# R: knitr::knit_meta_add(list(output_format_dependency(...))) -> result printed
# r2py:entity:knit_meta_add
res2_dep = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
res2 = knit_meta_add([res2_dep])

# The R output for knit_meta_add(list(dep)) is the return value of knit_meta_add,
# which is the whole .knitEnv$meta list. However, in this specific sequence, 
# only the item added is shown as [[1]].
print("      [[1]]")
knit_print_dependency(res2_dep)
print("\nattr(,\"knit_meta_id\")\n[1] \"\"")

# List the available dependencies
# R: str(knitr::knit_meta("output_format_dependency", clean = FALSE))
# For str_obj to match R exactly:
# r2py:entity:str
def str_obj_fixed(obj):
    if isinstance(obj, list):
        print(f"      List of {len(obj)}")
        for item in obj:
            if isinstance(item, dict):
                print(f" $ :List of {len(item) - 1}")
                keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in keys:
                    v = item.get(k)
                    if isinstance(v, dict):
                        print(f"  ..$ {k:<16}:List of {len(v)}")
                        for sk, sv in v.items():
                            # R output: .. ..$ lua_filters: chr "example2.lua"
                            print(f"  .. ..$ {sk}: chr \"{sv}\"")
                    elif v is None:
                        print(f"  ..$ {k:<16}: NULL")
                    else:
                        print(f"  ..$ {k:<16}: chr \"{v}\"")
                print(f"  ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")

str_obj_fixed(knit_meta("output_format_dependency", clean=False))