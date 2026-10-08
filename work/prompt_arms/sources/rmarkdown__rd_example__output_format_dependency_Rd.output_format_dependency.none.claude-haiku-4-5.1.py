# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pprint
import io
import sys

# Mocking the .knitEnv globally to mimic R's environment
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# r2py:entity:output_format_dependency
def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    obj = {
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
    # Add class attribute
    obj["__class__"] = "output_format_dependency"
    return obj

# r2py:entity:knit_meta_add
def knit_meta_add(meta, label=""):
    if meta:
        meta_list = meta if isinstance(meta, list) else [meta]
        _knitEnv.meta.extend(meta_list)
        _knitEnv.knit_meta_id.extend([label] * len(meta_list))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    """Filter metadata by class attribute."""
    result = []
    for item in _knitEnv.meta:
        if isinstance(item, dict) and item.get("__class__") == key:
            result.append(item)
    return result

def r_str(obj, max_level=10):
    """Mimic R's str() function for printing object structure."""
    def format_obj(obj, indent=0, level=0):
        prefix = " " * indent
        if level > max_level:
            return f"{prefix}..."
        
        if isinstance(obj, list):
            lines = []
            for i, item in enumerate(obj):
                if isinstance(item, dict) and "__class__" in item:
                    lines.append(f"{prefix}[[{i+1}]]")
                    lines.append(format_obj(item, indent + 1, level + 1))
                else:
                    lines.append(f"{prefix}[[{i+1}]]")
                    lines.append(format_obj(item, indent + 1, level + 1))
            return "\n".join(lines)
        elif isinstance(obj, dict):
            lines = []
            class_attr = obj.get("__class__")
            for key in sorted(obj.keys()):
                if key == "__class__":
                    continue
                val = obj[key]
                if isinstance(val, dict) and val and not isinstance(list(val.values())[0] if val else None, (dict, list)):
                    lines.append(f"{prefix}${key}")
                    for subkey in sorted(val.keys()):
                        subval = val[subkey]
                        if isinstance(subval, str):
                            lines.append(f"{prefix}..${subkey}: chr \"{subval}\"")
                        else:
                            lines.append(f"{prefix}..${subkey}: {subval}")
                elif val is None:
                    lines.append(f"{prefix}${key}")
                    lines.append(f"{prefix}: NULL")
                elif isinstance(val, str):
                    lines.append(f"{prefix}${key}")
                    lines.append(f"{prefix}: chr \"{val}\"")
                elif isinstance(val, dict):
                    lines.append(f"{prefix}${key}:List of {len(val)}")
                    for subkey in sorted(val.keys()):
                        subval = val[subkey]
                        if isinstance(subval, str):
                            lines.append(f"{prefix}..${subkey}: chr \"{subval}\"")
                else:
                    lines.append(f"{prefix}${key}: {val}")
            if class_attr:
                lines.append(f"{prefix}- attr(*, \"class\")= chr \"{class_attr}\"")
            return "\n".join(lines)
        else:
            return repr(obj)
    
    output = format_obj(obj, 0, 0)
    return output

# suppressPackageStartupMessages(library(rmarkdown))
# (Python equivalent: just import suppressed)

# Implicitly add lua filters from within a chunk
# This relies on (implicit) printing of the dependency in a chunk via
# knitr::knit_print()
result1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print(result1)

# Explicitly add lua filters from within a chunk
result2 = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
print(result2)

# List the available dependencies
print(r_str(knit_meta("output_format_dependency", clean=False)))
