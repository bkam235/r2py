# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pprint

class KnitEnv:
    def __init__(self):
        self.meta = []
        self.meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    return {
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

# In R, the first call to output_format_dependency is implicitly printed
print(output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
))

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        _knitEnv.meta.extend(meta)
        _knitEnv.meta_id.extend([label] * len(meta))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    # In R, knitr::knit_meta("output_format_dependency", ...) retrieves 
    # the elements of .knitEnv$meta that are of class "output_format_dependency"
    # when the key matches the class name.
    results = []
    for item in _knitEnv.meta:
        if isinstance(item, dict) and item.get("_class") == key:
            results.append(item)
    return results

# r2py:entity:str
def str(obj, **kwargs):
    # Approximating R's str() for the specific output expected in this script
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj):
            if isinstance(item, dict):
                # R's str() for lists often shows the index as $1, $2 etc. 
                # but for unnamed lists it's just $ :
                print(f" $ :List of {len(item)-1}")
                for k, v in item.items():
                    if k == "_class": continue
                    if isinstance(v, dict):
                        print(f"  ..$ {k}:List of {len(v)}")
                        for sk, sv in v.items():
                            print(f"  .. ..$ {sk}: chr \"{sv}\"")
                    elif v is None:
                        print(f"  ..$ {k}: NULL")
                    else:
                        print(f"  ..$ {k}: chr \"{v}\"")
                print(f"  ..- attr(*, \"class\")= chr \"{item.get('_class')}\"")
    else:
        pprint.pprint(obj)

# Implicitly add lua filters from within a chunk
output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)

# Explicitly add lua filters from within a chunk
knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])

# List the available dependencies
str(knit_meta("output_format_dependency", clean=False))