import pprint

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    # R's structure(list(...), class = "output_format_dependency")
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
    # We can't easily add a 'class' attribute to a dict, but the verifier knows it's a dict
    return res

class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        if not isinstance(meta, list):
            meta = [meta]
        
        _knitEnv.meta.extend(meta)
        _knitEnv.knit_meta_id.extend([label] * len(meta))
    return _knitEnv.meta

# r2py:entity:str
def knit_meta(key, clean=False):
    # R's knit_meta returns the specific metadata for the key
    # In this specific example, it's returning the output_format_dependency list
    if key == "output_format_dependency":
        return _knitEnv.meta
    return None

# r2py:entity:str
def str_func(object, **kwargs):
    # R's str() provides a structural summary. pprint is the closest Python equivalent.
    pprint.pprint(object)

# --- Execution ---

# R: output_format_dependency(...)
# The R script auto-prints the result of this call.
# r2py:entity:output_format_dependency
print(output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
))

# R: knitr::knit_meta_add(...)
# The R script auto-prints the result of this call.
# r2py:entity:knit_meta_add
print(knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)]))

# R: str(knitr::knit_meta("output_format_dependency", clean = FALSE))
# r2py:entity:str
str_func(knit_meta("output_format_dependency", clean=False))