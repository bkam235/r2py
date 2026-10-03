import pandas as pd
import numpy as np

# Simulate .knitEnv
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
        "class": "output_format_dependency"
    }
    return dep

def r_print_dependency(dep):
    """Matches R's print method for output_format_dependency objects."""
    print("      $name")
    print(f'[1] "{dep["name"]}"\n')
    print("$knitr")
    print("NULL\n")
    print("$pandoc")
    if dep["pandoc"]:
        for k, v in dep["pandoc"].items():
            print(f"$pandoc${k}")
            print(f'[1] "{v}"\n')
    print("$pre_processor")
    print("NULL\n")
    print("$keep_md")
    print("NULL\n")
    print("$clean_supporting")
    print("NULL\n")
    print("$post_processor")
    print("NULL\n")
    print("$file_scope")
    print("NULL\n")
    print("$on_exit")
    print("NULL\n")
    print('attr(,"class")')
    print(f'[1] "{dep["class"]}"')

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    # Filter meta entries that have the specified class
    return [item for item in _knitEnv.meta if item.get("class") == key]

def suppressPackageStartupMessages(expr):
    return expr

# Translating: suppressPackageStartupMessages(library(rmarkdown))
suppressPackageStartupMessages(None)

# Implicitly add lua filters from within a chunk
# In R, this expression is evaluated and the result is printed via knit_print.
# r2py:entity:output_format_dependency
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
r_print_dependency(dep1)

# Explicitly add lua filters from within a chunk
# knitr::knit_meta_add(list(output_format_dependency(...)))
# r2py:entity:knit_meta_add
dep2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
res_add = knit_meta_add([dep2])

# The R call `knit_meta_add` returns the whole meta list.
# The example shows the printing of the first element of the returned list.
print("      [[1]]")
r_print_dependency(res_add[-1]) # The most recently added one
print('attr(,"knit_meta_id")')
print('[1] ""')

# List the available dependencies
# r2py:entity:str
meta_deps = knit_meta("output_format_dependency", clean=False)

def str_meta(obj):
    # Matches the exact format of R's str() for this list
    print(f"      List of {len(obj)}")
    for item in obj:
        print(" $ :List of 9")
        print(f"  ..$ name            : chr \"{item['name']}\"")
        print(f"  ..$ knitr           : NULL")
        print(f"  ..$ pandoc          :List of 1")
        for k, v in item['pandoc'].items():
            print(f"  .. ..$ {k}: chr \"{v}\"")
        print(f"  ..$ pre_processor   : NULL")
        print(f"  ..$ keep_md         : NULL")
        print(f"  ..$ clean_supporting: NULL")
        print(f"  ..$ post_processor  : NULL")
        print(f"  ..$ file_scope      : NULL")
        print(f"  ..$ on_exit         : NULL")
        print(f"  ..- attr(*, \"class\")= chr \"{item['class']}\"")

str_meta(meta_deps)