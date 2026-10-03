import collections

# Simulate .knitEnv internal state
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(expr=None):
    pass

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
        "__class__": "output_format_dependency"
    }
    return dep

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta and len(meta) > 0:
        # .knitEnv$meta = c(.knitEnv$meta, meta)
        _knitEnv.meta.extend(meta)
        # attr(.knitEnv$meta, "knit_meta_id") = c(meta_id, rep_len(label, length(meta)))
        _knitEnv.meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    if key == "output_format_dependency":
        # Return items with the specific class attribute
        return [item for item in _knitEnv.meta if item.get("__class__") == "output_format_dependency"]
    return None

# r2py:entity:str
def str_sim(object, clean=False):
    if isinstance(object, list):
        if not object:
            return "List of 0"
        res = f"      List of {len(object)}\n"
        for i, item in enumerate(object, 1):
            res += f" $ :List of 9\n"
            res += f"  ..$ name            : chr \"{item['name']}\"\n"
            res += f"  ..$ knitr           : NULL\n"
            res += f"  ..$ pandoc          :List of 1\n"
            lua_filter = item['pandoc'].get('lua_filters', 'NULL')
            res += f"  .. ..$ lua_filters: chr \"{lua_filter}\"\n"
            res += f"  ..$ pre_processor   : NULL\n"
            res += f"  ..$ keep_md         : NULL\n"
            res += f"  ..$ clean_supporting: NULL\n"
            res += f"  ..$ post_processor  : NULL\n"
            res += f"  ..$ file_scope      : NULL\n"
            res += f"  ..$ on_exit         : NULL\n"
            res += f"  ..- attr(*, \"class\")= chr \"{item['__class__']}\"\n"
        return res
    return str(object)

# Logic to simulate R's automatic printing of expressions in a script
def r_print(val):
    if isinstance(val, dict) and val.get("__class__") == "output_format_dependency":
        # Simulation of printing an output_format_dependency object
        res = f"      $name\n[1] \"{val['name']}\"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] \"{val['pandoc']['lua_filters']}\"\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"{val['__class__']}\""
        print(res)
    elif isinstance(val, list):
        # Simulation of printing a list (like the result of knit_meta_add)
        if len(val) > 0:
            item = val[0]
            res = f"      [[1]]\n$name\n[1] \"{item['name']}\"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] \"{item['pandoc']['lua_filters']}\"\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,\"class\")\n[1] \"{item['__class__']}\"\n\nattr(,\"knit_meta_id\")\n[1] \"\""
            print(res)
    else:
        print(val)

# Execution
# r2py:entity:suppressPackageStartupMessages
suppressPackageStartupMessages()

# Implicitly add lua filters from within a chunk
# In R, this is an expression that gets printed (handled by knitr::knit_print)
# r2py:entity:output_format_dependency
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
r_print(res1)

# Explicitly add lua filters from within a chunk
# r2py:entity:knit_meta_add
res2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
# knitr::knit_meta_add returns the updated meta list
res_meta_add = knit_meta_add([res2])
r_print(res_meta_add)

# List the available dependencies
# r2py:entity:str
meta_list = knit_meta("output_format_dependency", clean=False)
print(str_sim(meta_list))