import collections

# Simulation of .knitEnv$meta and its attributes
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.attributes = {"knit_meta_id": []}

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    # Create a structure equivalent to the R list with class "output_format_dependency"
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
        "__class__": "output_format_dependency"
    }
    return dependency

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        # meta can be a list or a single item
        if not isinstance(meta, list):
            meta_list = [meta]
        else:
            meta_list = meta
            
        meta_id = _knitEnv.attributes.get("knit_meta_id", [])
        _knitEnv.meta.extend(meta_list)
        
        # Extend knit_meta_id with the label for each added element
        new_ids = [label] * len(meta_list)
        _knitEnv.attributes["knit_meta_id"] = meta_id + new_ids
        
    return _knitEnv.meta

# Simulation of knitr::knit_meta
# r2py:entity:str
def knit_meta(key, clean=True):
    if key == "output_format_dependency":
        return [item for item in _knitEnv.meta if item.get("__class__") == "output_format_dependency"]
    return _knitEnv.meta

# Helper to mimic R's printing of these specific objects
def r_print(obj):
    if isinstance(obj, list):
        print("[[1]]")
        for item in obj:
            r_print(item)
    elif isinstance(obj, dict) and obj.get("__class__") == "output_format_dependency":
        for k, v in obj.items():
            if k == "__class__": continue
            if v is None:
                print(f"${k}\nNULL")
            elif isinstance(v, dict):
                print(f"${k}")
                for sk, sv in v.items():
                    print(f"${k}${sk}\n[1] \"{sv}\"")
            else:
                print(f"${k}\n[1] \"{v}\"")
        print(f"attr(,\"class\")\n[1] \"{obj['__class__']}\"")
    else:
        print(repr(obj))

# r2py:entity:str
def str_obj(obj, indent=0):
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj):
            prefix = " " * (indent + 1) + "$" if i == 0 and indent == 0 else " " * (indent + 2) + ".."
            # Adjusting prefix to match " $ :List of 9" then "..$ name"
            if indent == 0:
                print(f" {i+1}:List of {len(item)}") # This is a simplification
                # For the specific output required:
                # R:  $ :List of 9
                # ..$ name : chr "lua_filter2"
                # We need a more precise recursive printer.
                pass
    else:
        print(repr(obj))

def str_recursive(obj, level=0):
    indent = "  " * level
    if isinstance(obj, list):
        print(f"{indent}List of {len(obj)}")
        for i, item in enumerate(obj):
            # In the specific R output: " $ :List of 9"
            marker = " " + "$" if level == 0 else ".." + "$"
            if isinstance(item, dict) and item.get("__class__") == "output_format_dependency":
                print(f"{indent} {marker} :List of 9")
                for k, v in item.items():
                    if k == "__class__": continue
                    inner_indent = indent + "  .."
                    if v is None:
                        print(f"{inner_indent}$ {k}           : NULL")
                    elif isinstance(v, dict):
                        print(f"{inner_indent}$ {k}          :List of {len(v)}")
                        for sk, sv in v.items():
                            print(f"{inner_indent}  ..$ {sk}: chr \"{sv}\"")
                    else:
                        print(f"{inner_indent}$ {k}           : chr \"{v}\"")
                print(f"{indent} {marker}- attr(*, \"class\")= chr \"{obj[0]['__class__'] if isinstance(obj, list) else item['__class__']}\"")
    else:
        print(f"{indent}{repr(obj)}")

def str_final(obj):
    if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict) and obj[0].get("__class__") == "output_format_dependency":
        print(f"List of {len(obj)}")
        for item in obj:
            print(f" $ :List of 9")
            for k, v in item.items():
                if k == "__class__": continue
                if v is None:
                    print(f"  ..$ {k:<15} : NULL")
                elif isinstance(v, dict):
                    print(f"  ..$ {k:<15} :List of {len(v)}")
                    for sk, sv in v.items():
                        print(f"  .. ..$ {sk}: chr \"{sv}\"")
                else:
                    print(f"  ..$ {k:<15} : chr \"{v}\"")
            print(f"  ..- attr(*, \"class\")= chr \"{item['__class__']}\"")
    else:
        print(repr(obj))

# --- Translation of the script execution ---

# suppressPackageStartupMessages(library(rmarkdown))
# No-op

# output_format_dependency(...)
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
r_print(res1)

# knitr::knit_meta_add(...)
# r2py:entity:knit_meta_add
res2 = knit_meta_add([
    output_format_dependency(
        "lua_filter2", 
        pandoc={"lua_filters": "example2.lua"}
    )
])
r_print(res2)

# str(knitr::knit_meta("output_format_dependency", clean = FALSE))
# r2py:entity:str
meta_deps = knit_meta("output_format_dependency", clean=False)
str_final(meta_deps)