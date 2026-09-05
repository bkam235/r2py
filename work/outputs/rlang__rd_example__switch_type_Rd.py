# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
from plotnine import *
import shiny as sh

# r2py:entity:switch_type
def switch_type(val, **kwargs):
    """
    Simplified Python implementation of rlang::switch_type.
    Maps a value's type to a specific result based on provided keyword arguments.
    """
    # Determine the type string based on Python's type system
    if isinstance(val, int) and not isinstance(val, bool):
        t = "integer"
    elif isinstance(val, float):
        t = "double"
    elif isinstance(val, str):
        t = "character"
    elif callable(val):
        # Check if it's a built-in function (similar to primitive)
        t = "primitive" if hasattr(val, '__name__') and (val.__module__ == 'builtins' or val.__module__ == 'rlang') else "function"
    else:
        t = type(val).__name__

    # Handle special case for 'string' alias to 'character'
    if t == "character" and "string" in kwargs and "character" not in kwargs:
        t = "string"

    # Return the mapped value or the 'default' key
    return kwargs.get(t, kwargs.get("default", "default"))

# r2py:entity:to_chr
def coerce_type(x, label, **mapping):
    """
    Simplified Python implementation of coerce_type.
    """
    t = "integer" if isinstance(x, int) else "double" if isinstance(x, float) else "character"
    if t in mapping:
        return mapping[t](x)
    raise TypeError(f"Cannot coerce {label} from type {t}")

# --- Execution ---

# switch_type(3L, double = "foo", integer = "bar", "default")
# r2py:entity:switch_type
print(switch_type(3, double="foo", integer="bar", default="default"))

# to_chr <- function(x) { ... }
# r2py:entity:to_chr
def to_chr(x):
    return coerce_type(x, "a chr", 
                       integer=lambda v: str(v), 
                       double=lambda v: str(v))

# r2py:entity:to_chr_1
print(to_chr(3))

# switch_type("str", character = "foo", string = "bar", "default")
# r2py:entity:switch_type_1
print(switch_type("str", character="foo", string="bar", default="default"))

# switch_type("str", string = , character = "foo", "default")
# In Python, we use None to represent the empty assignment in R
# r2py:entity:switch_type_2
print(switch_type("str", string=None, character="foo", default="default"))

# switch_type(base::list, primitive = "foo", "default")
# Using list as a type object
# r2py:entity:switch_type_3
print(switch_type(list, primitive="foo", default="default"))

# switch_type(base::`, primitive = "foo", "default")
# Python doesn't have the exact equivalent of $, using a lambda or getattr
# r2py:entity:switch_type_4
print(switch_type(getattr(pd.DataFrame, 'iloc'), primitive="foo", default="default"))

# switch_type(rlang::switch_type, primitive = "foo", "default")
# r2py:entity:switch_type_5
print(switch_type(switch_type, primitive="foo", default="default"))