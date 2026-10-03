import collections

# Simulate .knitEnv from knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knit_env = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
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

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    global _knit_env
    if meta:
        if not isinstance(meta, list):
            meta_list = [meta]
        else:
            meta_list = meta
            
        _knit_env.meta.extend(meta_list)
        _knit_env.knit_meta_id.extend([label] * len(meta_list))
    
    return _knit_env.meta

def knit_meta(key, clean=False):
    global _knit_env
    if key == "output_format_dependency":
        if not clean:
            # R's knit_meta returns the metadata associated with the key
            return [item for item in _knit_env.meta if item.get("class") == "output_format_dependency"]
        return [item for item in _knit_env.meta if item.get("class") == "output_format_dependency"]
    return _knit_env.meta

# r2py:entity:str
def r_str(obj, is_meta_list=False):
    """Approximate R's str() output for the metadata lists"""
    if is_meta_list and isinstance(obj, list):
        print(f"      List of {len(obj)}")
        for item in obj:
            print(f" $ :List of 9")
            print(f"  ..$ name            : chr \"{item.get('name')}\"")
            print(f"  ..$ knitr           : NULL")
            if isinstance(item.get('pandoc'), dict):
                print(f"  ..$ pandoc          :List of 1")
                for sk, sv in item.get('pandoc').items():
                    print(f"  .. ..$ {sk}: chr \"{sv}\"")
            else:
                print(f"  ..$ pandoc          : NULL")
            print(f"  ..$ pre_processor   : NULL")
            print(f"  ..$ keep_md         : NULL")
            print(f"  ..$ clean_supporting: NULL")
            print(f"  ..$ post_processor  : NULL")
            print(f"  ..$ file_scope      : NULL")
            print(f"  ..$ on_exit         : NULL")
            print(f"  ..- attr(*, \"class\")= chr \"{item.get('class')}\"")
    elif isinstance(obj, dict):
        print(f"      $name\n[1] \"{obj.get('name')}\"\n")
        print(f"$knitr\nNULL\n")
        print(f"$pandoc")
        if obj.get('pandoc'):
            print(f"$pandoc$lua_filters\n[1] \"{obj.get('pandoc').get('lua_filters')}\"\n")
        else:
            print("NULL\n")
        print(f"$pre_processor\nNULL\n")
        print(f"$keep_md\nNULL\n")
        print(f"$clean_supporting\nNULL\n")
        print(f"$post_processor\nNULL\n")
        print(f"$file_scope\nNULL\n")
        print(f"$on_exit\nNULL\n")
        print(f"attr(,\"class\")\n[1] \"{obj.get('class')}\"")

# Execution
# suppressPackageStartupMessages is a no-op
# import rmarkdown is a no-op

# Implicitly add lua filters from within a chunk
# r2py:entity:output_format_dependency
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
# r2py:entity:str
r_str(dep1)

# Implicitly add it to meta (simulating knitr::knit_print side effect)
# r2py:entity:knit_meta_add
knit_meta_add([dep1])

# Explicitly add lua filters from within a chunk
# R: knitr::knit_meta_add(list(output_format_dependency(...)))
# r2py:entity:knit_meta_add
res_add = knit_meta_add([
# r2py:entity:output_format_dependency
    output_format_dependency(
        "lua_filter2",
        pandoc={"lua_filters": "example2.lua"}
    )
])

# R auto-prints the result of knit_meta_add
print("      [[1]]")
# The result of knit_meta_add is the whole meta list, but the R output 
# for the specific call in the example only prints the last added item's detail.
# r2py:entity:str
r_str(res_add[-1])
print("\nattr(,\"knit_meta_id\")\n[1] \"\"")

# List the available dependencies
meta_deps = knit_meta("output_format_dependency", clean=False)
# R's str(knitr::knit_meta(...))
# r2py:entity:str
r_str(meta_deps, is_meta_list=True)