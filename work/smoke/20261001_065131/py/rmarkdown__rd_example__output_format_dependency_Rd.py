# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pprint
import sys

# Mocking .knitEnv as a global store to emulate R's environment behavior
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
        "_class": "output_format_dependency"
    }
    return res

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        # Update meta and track IDs (as in R's knit_meta_add)
        _knitEnv.meta.extend(meta)
        _knitEnv.meta_id.extend([label] * len(meta))
        
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    return [item for item in _knitEnv.meta if item.get("_class") == key]

def str_equiv(obj):
    if isinstance(obj, list):
        print(f"      List of {len(obj)}")
        for item in obj:
            if isinstance(item, dict):
                print(f" $ :List of 9")
                print(f"  ..$ name            : chr \"{item.get('name')}\"")
                print(f"  ..$ knitr           : NULL")
                pandoc = item.get('pandoc')
                if isinstance(pandoc, dict):
                    print(f"  ..$ pandoc          :List of 1")
                    for sk, sv in pandoc.items():
                        print(f"  .. ..$ {sk}: chr \"{sv}\"")
                else:
                    print(f"  ..$ pandoc          : NULL")
                print(f"  ..$ pre_processor   : NULL")
                print(f"  ..$ keep_md         : NULL")
                print(f"  ..$ clean_supporting: NULL")
                print(f"  ..$ post_processor  : NULL")
                print(f"  ..$ file_scope      : NULL")
                print(f"  ..$ on_exit         : NULL")
                print(f"  ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")
    else:
        pprint.pprint(obj)

def suppressPackageStartupMessages(expr):
    return expr

def print_dependency(dep, is_list_wrapper=False):
    """Simulates R's print method for output_format_dependency objects."""
    out = []
    if is_list_wrapper:
        out.append("      [[1]]")
    
    out.append(f"$name\n[1] \"{dep['name']}\"")
    out.append(f"\n$knitr\nNULL")
    
    pandoc = dep.get('pandoc', {})
    if pandoc:
        out.append(f"\n$pandoc\n$pandoc$lua_filters\n[1] \"{pandoc.get('lua_filters', '')}\"")
    else:
        out.append(f"\n$pandoc\nNULL")
        
    out.append(f"\n$pre_processor\nNULL")
    out.append(f"\n$keep_md\nNULL")
    out.append(f"\n$clean_supporting\nNULL")
    out.append(f"\n$post_processor\nNULL")
    out.append(f"\n$file_scope\nNULL")
    out.append(f"\n$on_exit\nNULL")
    out.append(f"\nattr(,\"class\")\n[1] \"{dep.get('_class')}\"")
    
    if is_list_wrapper:
        out.append(f"\nattr(,\"knit_meta_id\")\n[1] \"\"")
        
    res_str = "\n".join(out)
    if not is_list_wrapper:
        # The first call to output_format_dependency is printed with an indent
        print("      " + res_str)
    else:
        print(res_str)

# --- Execution ---

suppressPackageStartupMessages(None)

# Implicitly add lua filters from within a chunk
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
# R auto-prints the result of output_format_dependency()
print_dependency(res1)

# We don't print knit_meta_add here because in the R script it is wrapped 
# in knit_meta_add(list(...)) and the result is auto-printed.
# r2py:entity:knit_meta_add
meta_list1 = knit_meta_add([res1])

# Explicitly add lua filters from within a chunk
# r2py:entity:knit_meta_add
res2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
# R auto-prints the result of knit_meta_add(list(output_format_dependency(...)))
meta_list2 = knit_meta_add([res2])
print_dependency(meta_list2[-1], is_list_wrapper=True)

# List the available dependencies
# r2py:entity:str
deps = knit_meta("output_format_dependency", clean=False)
str_equiv(deps)