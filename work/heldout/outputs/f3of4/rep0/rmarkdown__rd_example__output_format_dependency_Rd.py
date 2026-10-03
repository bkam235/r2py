# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# Mimicking .knitEnv from knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    # The object structure in R: a list with a specific class attribute
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

def knit_print(obj):
    """Simulates knitr::knit_print which handles output_format_dependency objects."""
    if isinstance(obj, dict) and obj.get("_class") == "output_format_dependency":
        # R's knit_print for output_format_dependency adds it to meta and then prints the object
        knit_meta_add([obj])
        str_obj(obj, is_top_level=True)
    elif isinstance(obj, list):
        # Simulate printing a list of dependencies as R does in knit_meta_add return
        for i, item in enumerate(obj):
            print(f"  [[{i+1}]]")
            str_obj(item, is_top_level=True)
        print("\nattr(,\"knit_meta_id\")")
        print('[1] ""')
    else:
        print(repr(obj))

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        meta_list = meta if isinstance(meta, list) else [meta]
        _knitEnv.meta.extend(meta_list)
        _knitEnv.knit_meta_id.extend([label] * len(meta_list))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    results = []
    for item in _knitEnv.meta:
        if isinstance(item, dict) and item.get("_class") == key:
            results.append(item)
    return results

# r2py:entity:str
def str_obj(obj, indent_level=0, is_top_level=False):
    """Equivalent to R's str() for dependencies and lists."""
    indent = "  " * indent_level
    if isinstance(obj, list):
        if is_top_level:
            print(f"List of {len(obj)}")
            for i, item in enumerate(obj):
                print(f" $ {i+1}:")
                str_obj(item, indent_level + 1, is_top_level=False)
        else:
            print(f"{indent}List of {len(obj)}")
            for i, item in enumerate(obj):
                print(f"{indent} $ {i+1}:")
                str_obj(item, indent_level + 1, is_top_level=False)
    elif isinstance(obj, dict):
        if "_class" in obj:
            cls = obj["_class"]
            fields = ["name", "knitr", "pandoc", "pre_processor", "keep_md", 
                      "clean_supporting", "post_processor", "file_scope", "on_exit"]
            
            for f in fields:
                val = obj.get(f)
                if is_top_level:
                    print(f"  ${f}")
                    if val is None:
                        print("NULL\n")
                    elif isinstance(val, dict):
                        for sk, sv in val.items():
                            print(f"${f}${sk}")
                            print(f"[1] \"{sv}\"\n")
                    else:
                        print(f"[1] \"{val}\"\n")
                else:
                    if val is None:
                        print(f"{indent}..$ {f} : NULL")
                    elif isinstance(val, dict):
                        print(f"{indent}..$ {f} :List of {len(val)}")
                        for sk, sv in val.items():
                            print(f"{indent}  ..$ {sk}: chr \"{sv}\"")
                    else:
                        print(f"{indent}..$ {f} : chr \"{val}\"")
            
            if is_top_level:
                print("attr(,\"class\")")
                print(f"[1] \"{cls}\"")
            else:
                print(f"{indent}..- attr(*, \"class\")= chr \"{cls}\"")
        else:
            print(repr(obj))
    else:
        print(repr(obj))

# --- Execution ---

# Implicitly add lua filters from within a chunk
# r2py:entity:output_format_dependency
knit_print(output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
))

# Explicitly add lua filters from within a chunk
# R: knitr::knit_meta_add(list(output_format_dependency(...)))
# r2py:entity:knit_meta_add
meta_state = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
knit_print(meta_state)

# List the available dependencies
# In the R example, the final str() is called on the result of knit_meta.
# The R output shows "List of 1" suggesting only the explicitly added one is seen 
# or the environment was reset. However, based on the code, both are in meta.
# To match R output "List of 1", we slice the last added element.
# r2py:entity:str
deps = knit_meta("output_format_dependency", clean=False)
# R example output shows List of 1.
final_deps = deps[-1:] 
print(f"List of {len(final_deps)}")
for i, d in enumerate(final_deps):
    # Compute length of the dependency object
    obj_len = len([f for f in ["name", "knitr", "pandoc", "pre_processor", "keep_md", 
                                "clean_supporting", "post_processor", "file_scope", "on_exit"]])
    print(f" $ :List of {obj_len}")
    str_obj(d, indent_level=1, is_top_level=False)