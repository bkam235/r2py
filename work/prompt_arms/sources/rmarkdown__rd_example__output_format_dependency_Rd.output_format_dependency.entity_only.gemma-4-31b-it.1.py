import pprint

def print_r_style(obj):
    """Helper to mimic R's auto-printing of lists/dicts"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "__class__": continue
            print(f"${k}")
            if isinstance(v, dict):
                for sk, sv in v.items():
                    print(f"${k}${sk}\n[1] " + str(sv))
            else:
                print(f"[1] " + str(v))
        print(f"attr(,"class")\n[1] " + str(obj.get('__class__')))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print(f"[[{i+1}]]")
            print_r_style(item)
            print("attr(,"knit_meta_id")\n[1] " + str(""))

# Mocking the knitr environment
class KnitEnv:
    def __init__(self):
        self.meta = {}

_knitEnv = KnitEnv()

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
        "__class__": "output_format_dependency"
    }
    return res

def knit_meta_add(meta, label=""):
    if meta is None: return None
    meta_list = meta if isinstance(meta, list) else [meta]
    for item in meta_list:
        # R's knit_meta stores these under the 'output_format_dependency' key
        if "output_format_dependency" not in _knitEnv.meta:
            _knitEnv.meta["output_format_dependency"] = []
        _knitEnv.meta["output_format_dependency"].append(item)
    return meta_list

def knit_meta(key, clean=False):
    return _knitEnv.meta.get(key, [])

def suppressPackageStartupMessages(msg=None):
    pass

# --- Actual Script Translation ---

suppressPackageStartupMessages()

# Implicitly add lua filters from within a chunk
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_r_style(dep1)

# Explicitly add lua filters from within a chunk
res_add = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
print_r_style(res_add)

# List the available dependencies
# Note that the list may include dependencies with duplicated names.
# In R, str() for this list outputs specific structure
def str_knit_meta(obj):
    if not obj:
        print("List of 0")
        return
    print(f"List of {len(obj)}")
    for i, item in enumerate(obj):
        print(f" ${i+1}:List of 9")
        print(f"  ..$ name            : chr "{item['name']}"")
        print(f"  ..$ knitr           : NULL")
        if item['pandoc']:
            print(f"  ..$ pandoc          :List of 1")
            for k, v in item['pandoc'].items():
                print(f"  .. ..$ {k}: chr "{v}"")
        else:
            print(f"  ..$ pandoc          : NULL")
        print(f"  ..$ pre_processor   : NULL")
        print(f"  ..$ keep_md         : NULL")
        print(f"  ..$ clean_supporting: NULL")
        print(f"  ..$ post_processor  : NULL")
        print(f"  ..$ file_scope      : NULL")
        print(f"  ..$ on_exit         : NULL")
        print(f"  ..- attr(*, "class")= chr "{item['__class__']}"")

str_knit_meta(knit_meta("output_format_dependency", clean=False))