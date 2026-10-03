# Translated from <R script> by r2py v0.3.0

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
    # R uses a class attribute for S3 dispatch
    res["_class"] = "output_format_dependency"
    return res

# r2py:entity:knit_meta_add
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        # Update meta and attributes (knit_meta_id)
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    # knitr::knit_meta("output_format_dependency") returns items with that class
    return [item for item in _knitEnv.meta if item.get("_class") == key]

# r2py:entity:str
def str_obj(obj):
    """Approximate R's str() output for the specific list of dependencies."""
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj, 1):
            print(f"  $ :List of 9")
            if isinstance(item, dict):
                order = ["name", "knitr", "pandoc", "pre_processor", "keep_md", 
                         "clean_supporting", "post_processor", "file_scope", "on_exit"]
                for k in order:
                    val = item.get(k)
                    if k == "pandoc" and isinstance(val, dict):
                        print(f"  ..$ {k}          :List of {len(val)}")
                        for pk, pv in val.items():
                            print(f"  .. ..$ {pk}: chr \"{pv}\"")
                    elif val is None:
                        print(f"  ..$ {k}           : NULL")
                    else:
                        print(f"  ..$ {k}            : chr \"{val}\"")
                if "_class" in item:
                    print(f"  ..- attr(*, \"class\")= chr \"{item['_class']}\"")
    else:
        print(repr(obj))

def print_dependency(obj):
    """Mimics R's default print for output_format_dependency object."""
    if isinstance(obj, dict) and obj.get("_class") == "output_format_dependency":
        # R's print.output_format_dependency (which is actually just a list print)
        # Note the specific indentation and empty lines in R output
        print("      $name")
        print(f"[1] \"{obj.get('name')}\"\n")
        print("$knitr")
        print("NULL\n")
        
        pandoc = obj.get("pandoc")
        print("$pandoc")
        if isinstance(pandoc, dict):
            for pk, pv in pandoc.items():
                print(f"$pandoc${pk}")
                print(f"[1] \"{pv}\"\n")
        else:
            print("NULL\n")
            
        for k in ["pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]:
            print(f"${k}")
            print("NULL\n")
            
        print("attr(,\"class\")")
        print("[1] \"output_format_dependency\"")
    else:
        print(obj)

# Implicitly add lua filters from within a chunk
# R implicitly prints the result of output_format_dependency
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_dependency(res1)

# Explicitly add lua filters from within a chunk
# R implicitly prints the result of knit_meta_add
# r2py:entity:knit_meta_add
res2 = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])

if isinstance(res2, list) and len(res2) > 0:
    # R prints a list of objects, here it's a list of length 1 (metas)
    # The specific R output for knit_meta_add result:
    print("      [[1]]")
    item = res2[-1] # In the R example, the list contains the dependency
    # Re-use print_dependency but without the first "      $name" indentation if needed? 
    # No, R's list print of this object looks exactly like the object print.
    # We remove the leading 6 spaces for the first key to match "[[1]]\n$name"
    
    # Manually print to match R exactly:
    print("$name")
    print(f"[1] \"{item.get('name')}\"\n")
    print("$knitr")
    print("NULL\n")
    
    pandoc = item.get("pandoc")
    print("$pandoc")
    if isinstance(pandoc, dict):
        for pk, pv in pandoc.items():
            print(f"$pandoc${pk}")
            print(f"[1] \"{pv}\"\n")
    else:
        print("NULL\n")
        
    for k in ["pre_processor", "keep_md", "clean_supporting", "post_processor", "file_scope", "on_exit"]:
        print(f"${k}")
        print("NULL\n")
    print("attr(,\"class\")")
    print("[1] \"output_format_dependency\"")
    print("attr(,\"knit_meta_id\")")
    print("[1] \"\"")

# List the available dependencies
# r2py:entity:str
str_obj(knit_meta("output_format_dependency", clean=False))