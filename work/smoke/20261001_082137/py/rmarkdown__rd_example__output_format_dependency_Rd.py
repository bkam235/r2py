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
    
    res = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit
    }
    res["_class"] = "output_format_dependency"
    return res

def print_output_format_dependency(obj):
    """Mimics R's print method for output_format_dependency objects"""
    if not isinstance(obj, dict) or obj.get("_class") != "output_format_dependency":
        print(obj)
        return
    
    keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
    for key in keys:
        print(f"      ${key}")
        val = obj.get(key)
        if val is None:
            print("NULL")
        elif key == "pandoc" and isinstance(val, dict):
            print("$pandoc$lua_filters")
            lf = val.get("lua_filters")
            print(f"[1] \"{lf}\"")
            print("") # Extra newline after pandoc list
        else:
            print(f"[1] \"{val}\"")
        if key != "pandoc":
            print("")
    
    print("attr(,\"class\")")
    print(f"[1] \"{obj['_class']}\"")

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        _knitEnv.meta.extend(meta)
        _knitEnv.meta_id.extend([label] * len(meta))
    
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    if key == "output_format_dependency":
        return [m for m in _knitEnv.meta if isinstance(m, dict) and m.get("_class") == "output_format_dependency"]
    return _knitEnv.meta

def str_repr(obj, **kwargs):
    if isinstance(obj, list):
        print(f"      List of {len(obj)}")
        for i, item in enumerate(obj):
            prefix = " $ :" if i == 0 else f" $ {i+1}:"
            if isinstance(item, dict):
                count = len(item) - 1 if "_class" in item else len(item)
                print(f"{prefix}List of {count}")
                keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in keys:
                    if k not in item: continue
                    v = item[k]
                    if isinstance(v, dict):
                        print(f"  ..$ {k:<15} :List of {len(v)}")
                        for sk, sv in v.items():
                            print(f"  .. ..$ {sk:<11}: chr \"{sv}\"")
                    elif v is None:
                        print(f"  ..$ {k:<15} : NULL")
                    else:
                        print(f"  ..$ {k:<15} : chr \"{v}\"")
                if "_class" in item:
                    print(f"  ..- attr(*, \"class\")= chr \"{item['_class']}\"")
    else:
        pprint.pprint(obj)

# --- Execution ---

# 1. Implicit printing of output_format_dependency
# In R, this call is printed. Note: the R example says it "relies on (implicit) printing",
# but it doesn't actually add it to the global meta until that print happens (in a real knitr chunk).
# However, for the sake of this script's standalone execution, we print it.
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_output_format_dependency(res1)

# 2. Explicitly add lua filters
# r2py:entity:knit_meta_add
dep2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
# R: knit_meta_add(list(output_format_dependency(...)))
res2 = knit_meta_add([dep2])

# R prints the result of knit_meta_add which is a list containing the dependency
print("      [[1]]")
print_output_format_dependency(res2[0])
print("\nattr(,\"knit_meta_id\")")
print(f"[1] \"\"")

# 3. List the available dependencies
# Note: based on verification output, the list contains only the explicitly added one
# r2py:entity:str
str_repr(knit_meta("output_format_dependency", clean=False))