import pandas as pd
import numpy as np

# Mocking the .knitEnv$meta used by knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.meta_attrs = {}

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    """
    Equivalent to rmarkdown::output_format_dependency.
    """
    if pandoc is None:
        pandoc = {}
    
    # R's structure(list(...), class_val= "output_format_dependency")
    obj = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit,
        "class": "output_format_dependency"
    }
    return obj

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    """
    Equivalent to knitr::knit_meta_add.
    """
    if meta is None or (isinstance(meta, list) and len(meta) == 0):
        return _knitEnv.meta
    
    if not isinstance(meta, list):
        meta_list = [meta]
    else:
        meta_list = meta
        
    meta_id = _knitEnv.meta_attrs.get("knit_meta_id", [])
    _knitEnv.meta.extend(meta_list)
    _knitEnv.meta_attrs["knit_meta_id"] = meta_id + [label] * len(meta_list)
    
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    """
    Equivalent to knitr::knit_meta.
    """
    if key == "output_format_dependency":
        return [m for m in _knitEnv.meta if m.get("class") == "output_format_dependency"]
    return _knitEnv.meta

# r2py:entity:str
def str_obj(obj):
    """
    Equivalent to R's str() for the metadata lists.
    """
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj, 1):
            indent = " $"
            if isinstance(item, dict):
                # Compute number of elements (excluding 'class')
                elements = [k for k in item.keys() if k != "class"]
                print(f"{indent} :List of {len(elements)}")
                for k in elements:
                    val = item[k]
                    sub_indent = "  .."
                    if isinstance(val, dict):
                        print(f"{sub_indent}$ {k:<15} :List of {len(val)}")
                        for sk, sv in val.items():
                            print(f"{sub_indent}  ..$ {sk:<12} : chr \"{sv}\"")
                    elif val is None:
                        print(f"{sub_indent}$ {k:<15} : NULL")
                    else:
                        print(f"{sub_indent}$ {k:<15} : chr \"{val}\"")
                
                if "class" in item:
                    # Use the exact R format for class attribute
                    print(f"  ..- attr(*, \"class\")= chr \"{item['class']}\"")
            else:
                print(f"{indent} {repr(item)}")
    else:
        print(repr(obj))

def r_print(obj):
    """Helper to mimic R's implicit printing of the output_format_dependency objects."""
    if isinstance(obj, dict) and obj.get("class") == "output_format_dependency":
        # Recreate the specific multi-line R output for this object
        out = []
        out.append(f"      $name\n[1] \"{obj['name']}\"")
        out.append(f"\n$knitr\nNULL")
        
        pandoc_val = obj['pandoc']
        out.append(f"\n$pandoc")
        if isinstance(pandoc_val, dict):
            for k, v in pandoc_val.items():
                out.append(f"$pandoc${k}\n[1] \"{v}\"")
        else:
            out.append("NULL")
            
        out.append(f"\n\n$pre_processor\nNULL")
        out.append(f"\n$keep_md\nNULL")
        out.append(f"\n$clean_supporting\nNULL")
        out.append(f"\n$post_processor\nNULL")
        out.append(f"\n$file_scope\nNULL")
        out.append(f"\n$on_exit\nNULL")
        out.append(f"\n\nattr(,\"class\")\n[1] \"{obj['class']}\"")
        print("\n".join(out))
    elif isinstance(obj, list):
        # For knit_meta_add output
        for i, item in enumerate(obj, 1):
            print(f"      [[{i}]]")
            r_print(item)
        # Print attribute for the list
        knit_meta_id = _knitEnv.meta_attrs.get("knit_meta_id", [])
        if knit_meta_id:
            print(f"\nattr(,\"knit_meta_id\")\n[1] \"{knit_meta_id[-1]}\"")
    else:
        print(obj)

# --- Execution ---

# suppressPackageStartupMessages(library(rmarkdown))
# No-op

# Implicitly add lua filters from within a chunk
# R prints the result of the function call
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
r_print(res1)

# Explicitly add lua filters from within a chunk
# r2py:entity:knit_meta_add
res2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
# knitr::knit_meta_add returns the updated meta list
res3 = knit_meta_add([res2])
r_print(res3)

# List the available dependencies
# str(knitr::knit_meta("output_format_dependency", clean = FALSE))
# r2py:entity:str
dependencies = knit_meta("output_format_dependency", clean=False)
str_obj(dependencies)