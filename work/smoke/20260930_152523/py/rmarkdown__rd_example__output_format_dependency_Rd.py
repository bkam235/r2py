import pprint

# Mocking the .knitEnv for knitr functionality
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    # In R, this returns a list with class "output_format_dependency"
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
        "class": "output_format_dependency"
    }
    return res

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    global _knitEnv
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        # Maintain a mirror of the knit_meta_id attribute
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    global _knitEnv
    # In R, knitr::knit_meta("output_format_dependency") returns 
    # objects of that class from the meta list.
    results = [item for item in _knitEnv.meta if item.get("class") == key]
    return results

# r2py:entity:str
def str_repr(object):
    """Python equivalent of R's str() for these structures."""
    if isinstance(object, list):
        print(f"List of {len(object)}")
        for i, item in enumerate(object):
            prefix = " $" if i == 0 else f" ${i+1}"
            if isinstance(item, dict):
                print(f"{prefix} :List of {len(item) - 1}") # -1 to ignore 'class'
                for k, v in item.items():
                    if k == "class": continue
                    if isinstance(v, dict):
                        print(f"  ..{k}          :List of {len(v)}")
                        for vk, vv in v.items():
                            print(f"  .. ..$ {vk}: chr \"{vv}\"")
                    elif v is None:
                        print(f"  ..{k}           : NULL")
                    else:
                        print(f"  ..{k}           : chr \"{v}\"")
                print(f"  ..- attr(*, \"class\")= chr \"{item.get('class')}\"")
    else:
        pprint.pprint(object)

# Implicitly add lua filters from within a chunk
# In R, this result is auto-printed.
# r2py:entity:output_format_dependency
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print(dep1)

# The R script implies this is handled by knit_print() in a real chunk
# r2py:entity:knit_meta_add
knit_meta_add([dep1])

# Explicitly add lua filters from within a chunk
# In R, this result is auto-printed.
# r2py:entity:knit_meta_add
res_meta = knit_meta_add([
# r2py:entity:output_format_dependency
    output_format_dependency(
        "lua_filter2",
        pandoc={"lua_filters": "example2.lua"}
    )
])
print(res_meta)

# List the available dependencies
# r2py:entity:str
str_repr(knit_meta("output_format_dependency", clean=False))