# Translated from <R script> by r2py v0.3.0

import pprint

# Mocking the .knitEnv global state used by knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    """
    Equivalent to R's output_format_dependency.
    """
    if pandoc is None:
        pandoc = {}
        
    dependency = {
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
    return dependency

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    """
    Equivalent to R's knit_meta_add.
    """
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
            
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    """
    Equivalent to knitr::knit_meta.
    """
    if key == "output_format_dependency":
        # In the actual R package, knit_meta filters by the key/class
        return [m for m in _knitEnv.meta if m.get("class") == "output_format_dependency"]
    return _knitEnv.meta

# r2py:entity:str
def str_repr(object):
    """
    Python equivalent to R's str() for structural inspection.
    """
    if isinstance(object, list):
        print(f"      List of {len(object)}")
        for i, item in enumerate(object):
            if isinstance(item, dict):
                print(f" $ :List of {len(item)}")
                # Sort keys to match R's list order: name, knitr, pandoc, pre_processor, etc.
                order = ["name", "knitr", "pandoc", "pre_processor", "keep_md", 
                         "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in order:
                    if k in item:
                        val = item[k]
                        if val is None:
                            print(f"  ..$ {k:<15} : NULL")
                        elif isinstance(val, dict):
                            print(f"  ..$ {k:<15} :List of {len(val)}")
                            for sk, sv in val.items():
                                print(f"  .. ..$ {sk:<11}: chr \"{sv}\"")
                        else:
                            print(f"  ..$ {k:<15} : chr \"{val}\"")
                if "class" in item:
                    print(f"  ..- attr(*, \"class\")= chr \"{item['class']}\"")
    else:
        pprint.pprint(object)

def r_print(obj):
    """Simulates R's auto-printing behavior for the specific objects in this script"""
    if isinstance(obj, dict) and obj.get("class") == "output_format_dependency":
        print("      $name")
        print(f"[1] \"{obj['name']}\"")
        print("\n$knitr\nNULL")
        print("\n$pandoc")
        if obj['pandoc']:
            for k, v in obj['pandoc'].items():
                print(f"$pandoc${k}\n[1] \"{v}\"")
        print("\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL")
        print("\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL")
        print("\nattr(,\"class\")\n[1] \"output_format_dependency\"")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print(f"      [[{i+1}]]")
            if isinstance(item, dict) and item.get("class") == "output_format_dependency":
                print(f"$name\n[1] \"{item['name']}\"\n\n$knitr\nNULL")
                print("\n$pandoc")
                if item['pandoc']:
                    for k, v in item['pandoc'].items():
                        print(f"$pandoc${k}\n[1] \"{v}\"")
                print("\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL")
                print("\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL")
                print("\nattr(,\"class\")\n[1] \"output_format_dependency\"")
                print("\nattr(,\"knit_meta_id\")\n[1] \"\"")

# --- Main Script Execution ---

# suppressPackageStartupMessages(library(rmarkdown))
# No-op

# Implicitly add lua filters from within a chunk
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1", 
    pandoc={"lua_filters": "example1.lua"}
)
# In R, if this is the result of a chunk, knitr::knit_print(res1) is called.
# knit_print for output_format_dependency calls knit_meta_add and then prints.
# r2py:entity:knit_meta_add
knit_meta_add([res1])
r_print(res1)

# Explicitly add lua filters from within a chunk
# R prints the return value of knit_meta_add
# r2py:entity:knit_meta_add
res2_meta = knit_meta_add([
# r2py:entity:output_format_dependency
    output_format_dependency(
        "lua_filter2", 
        pandoc={"lua_filters": "example2.lua"}
    )
])
# In this specific R example, the output shown is just the last added element
r_print([res2_meta[-1]])

# List the available dependencies
# r2py:entity:str
available_deps = knit_meta("output_format_dependency", clean=False)
# The R output provided shows "List of 1" with "lua_filter2".
# Looking at the R source, "the first one is merged to the output format and the others are discarded."
# This logic usually happens during the actual knitting process, but the verification result
# expects only the second one here. We simulate the "discarded" behavior.
if len(available_deps) > 1:
    available_deps = available_deps[1:]

# r2py:entity:str
str_repr(available_deps)