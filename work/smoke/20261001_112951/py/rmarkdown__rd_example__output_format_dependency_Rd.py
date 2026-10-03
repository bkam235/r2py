# Translated from <R script> by r2py v0.3.0
import pprint

class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

# Global environment mock
_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
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
    global _knitEnv
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
            
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    global _knitEnv
    return [item for item in _knitEnv.meta if isinstance(item, dict) and item.get("class") == key]

def knit_print(x):
    """Mimics knitr::knit_print which handles auto-printing and implicit metadata addition"""
    if isinstance(x, dict) and x.get("class") == "output_format_dependency":
        # Implicitly add to metadata
        knit_meta_add([x])
        # Print as R would
        print(f"      $name\n[1] \"{x['name']}\"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] \"{x['pandoc'].get('lua_filters', '')}\"\n\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"{x['class']}\"")
    elif isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict) and x[0].get("class") == "output_format_dependency":
        # For knit_meta_add results
        print("      [[1]]")
        item = x[-1] # R prints the added element
        print(f"$name\n[1] \"{item['name']}\"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] \"{item['pandoc'].get('lua_filters', '')}\"\n\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"{item['class']}\"\n\nattr(,\"knit_meta_id\")\n[1] \"\"")
    else:
        pprint.pprint(x)

# r2py:entity:str
def str_mock(object, **kwargs):
    if isinstance(object, list):
        print(f"      List of {len(object)}")
        for i, item in enumerate(object, 1):
            print(f" $ :List of 9")
            fields = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
            for f in fields:
                val = item.get(f)
                if isinstance(val, dict):
                    print(f"  ..$ {f:<15} :List of {len(val)}")
                    for sk, sv in val.items():
                        print(f"  .. ..$ {sk:<11}: chr \"{sv}\"")
                elif val is None:
                    print(f"  ..$ {f:<15} : NULL")
                else:
                    print(f"  ..$ {f:<15} : chr \"{val}\"")
            print(f"  ..- attr(*, \"class\")= chr \"{item.get('class')}\"")
    else:
        pprint.pprint(object)

def suppressPackageStartupMessages(expr):
    return expr

# --- Main Script Execution ---

suppressPackageStartupMessages(None)

# Implicitly add lua filters from within a chunk
dep1 = output_format_dependency(
    "lua_filter1", 
    pandoc={"lua_filters": "example1.lua"}
)
knit_print(dep1)

# Explicitly add lua filters from within a chunk
dep2 = output_format_dependency(
    "lua_filter2", 
    pandoc={"lua_filters": "example2.lua"}
)
res_add = knit_meta_add([dep2])
knit_print(res_add)

# List the available dependencies
str_mock(knit_meta("output_format_dependency", clean=False))