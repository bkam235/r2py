# Translated from <R script> by r2py v0.3.0

import pprint

# Mocking the .knitEnv$meta environment used by knitr
class KnitEnv:
    def __init__(self):
        self.meta = []
        # Using a list to store metadata and a parallel list for IDs/labels
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# rmarkdown library does not have a direct Python equivalent for this metadata system.
# We implement the specific functions used in the script.

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, 
                             file_scope=None, on_exit=None):
    """
    Equivalent to rmarkdown::output_format_dependency
    """
    if pandoc is None:
        pandoc = {}
    
    # Create a structure similar to the R list with class 'output_format_dependency'
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
        "_class": "output_format_dependency"
    }
    return dep

# The R script calls this function as a top-level expression, 
# so we must print the result to match R's auto-printing behavior.
print(output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
))

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    """
    Equivalent to knitr::knit_meta_add
    """
    if isinstance(meta, list) and len(meta) > 0:
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    """
    Equivalent to knitr::knit_meta
    """
    # In the R source, knit_meta("output_format_dependency") filters for 
    # dependencies with that name or class.
    if key == "output_format_dependency":
        # The R version returns the dependencies associated with the format
        # We filter the global meta list for items that look like output_format_dependency
        return [item for item in _knitEnv.meta if item.get("_class") == "output_format_dependency"]
    return _knitEnv.meta

def suppressPackageStartupMessages(expr):
    # This is a no-op in Python translation of this script
    return expr

# --- Execution ---

# Implicitly add lua filters from within a chunk
# In R, the return value of this call in a chunk is passed to knit_print, 
# which internally calls knit_meta_add.
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
# Mimicking the implicit knit_print behavior:
knit_meta_add([dep1])

# Explicitly add lua filters from within a chunk
knit_meta_add([
    output_format_dependency(
        "lua_filter2",
        pandoc={"lua_filters": "example2.lua"}
    )
])

# List the available dependencies
# r2py:entity:str
# Use pprint.pprint to approximate R's str() output
res = knit_meta("output_format_dependency", clean=False)
pprint.pprint(res)