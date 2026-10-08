import pprint

# Mocking the .knitEnv globally to mimic R's environment
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    # Return a dictionary with a 'class' key to mimic R's S3 structure
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
    if meta:
        # Handle case where meta is a single item or a list
        meta_list = meta if isinstance(meta, list) else [meta]
        _knitEnv.meta.extend(meta_list)
        _knitEnv.knit_meta_id.extend([label] * len(meta_list))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    # Mimics R's knitr::knit_meta which filters the global meta list by class attribute
    if key == "output_format_dependency":
        return [item for item in _knitEnv.meta if isinstance(item, dict) and item.get("__class__") == "output_format_dependency"]
    return _knitEnv.meta

def suppressPackageStartupMessages(expr):
    # No-op in Python
    return None

# --- Actual Script Translation ---

# Implicitly add lua filters from within a chunk
# This relies on (implicit) printing of the dependency in a chunk via knitr::knit_print()
output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)

# Explicitly add lua filters from within a chunk
knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])

# List the available dependencies
# Note that the list may include dependencies with duplicated names. In that
# case, the first one is merged to the output format and the others are
# discarded.
str(knit_meta("output_format_dependency", clean=False))