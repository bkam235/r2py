# Translated from <R script> by r2py v0.3.0

# Simulate .knitEnv$meta and its attributes
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    
    # Create a structure mimicking the R list with class attribute
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
    if meta:
        # meta is expected to be a list in the R call: list(output_format_dependency(...))
        if not isinstance(meta, list):
            meta = [meta]
            
        _knitEnv.meta.extend(meta)
        # Handle knit_meta_id attribute
        _knitEnv.meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    # In R, knitr::knit_meta("output_format_dependency") filters 
    # the global meta list for objects of that class.
    results = [item for item in _knitEnv.meta if item.get("__class__") == key]
    return results

def suppressPackageStartupMessages(expr):
    # Simulation of library(rmarkdown)
    return expr

# r2py:entity:str
def str_sim(object):
    if isinstance(object, list):
        print(f"List of {len(object)}")
        for i, item in enumerate(object):
            # R's str() for these lists shows " $ :List of 9" for the items
            print(f" $ :List of 9")
            # The order of keys in R lists is stable
            keys = ["name", "knitr", "pandoc", "pre_processor", "keep_md", 
                    "clean_supporting", "post_processor", "file_scope", "on_exit"]
            for k in keys:
                v = item.get(k)
                if v is None:
                    print(f"  ..$ {k:<15} : NULL")
                elif isinstance(v, dict):
                    print(f"  ..$ {k:<15} :List of {len(v)}")
                    for sk, sv in v.items():
                        print(f"  .. ..$ {sk:<11}: chr \"{sv}\"")
                else:
                    print(f"  ..$ {k:<15} : chr \"{v}\"")
            print(f"  ..- attr(*, \"class\")= chr \"{item.get('__class__')}\"")
    else:
        print(object)

def r_print_dep(dep, index=None):
    """Simulates R's print() for an output_format_dependency object."""
    prefix = "      [[1]]\n" if index is not None else "      "
    res = prefix
    res += f"$name\n[1] \"{dep['name']}\"\n\n"
    res += f"$knitr\nNULL\n\n"
    res += f"$pandoc\n$pandoc$lua_filters\n[1] \"{dep['pandoc'].get('lua_filters')}\"\n\n"
    res += f"$pre_processor\nNULL\n\n"
    res += f"$keep_md\nNULL\n\n"
    res += f"$clean_supporting\nNULL\n\n"
    res += f"$post_processor\nNULL\n\n"
    res += f"$file_scope\nNULL\n\n"
    res += f"$on_exit\nNULL\n\n"
    res += f"attr(,\"class\")\n[1] \"{dep['__class__']}\""
    if index is not None:
        res += "\n\nattr(,\"knit_meta_id\")\n[1] \"\""
    return res

# --- Execution ---

# suppressPackageStartupMessages(library(rmarkdown))
suppressPackageStartupMessages("library(rmarkdown)")

# Implicitly add lua filters from within a chunk
# In R, calling output_format_dependency() in a chunk triggers knit_print(),
# which calls knit_meta_add() and then prints the object.
# r2py:entity:output_format_dependency
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
# r2py:entity:knit_meta_add
knit_meta_add([dep1])
print(r_print_dep(dep1))

# Explicitly add lua filters from within a chunk
# knitr::knit_meta_add(list(output_format_dependency(...)))
# r2py:entity:output_format_dependency
dep2 = output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)
# r2py:entity:knit_meta_add
knit_meta_add([dep2])
print(r_print_dep(dep2, index=1))

# List the available dependencies
# str(knitr::knit_meta("output_format_dependency", clean = FALSE))
# r2py:entity:str
res = knit_meta("output_format_dependency", clean=False)
str_sim(res)