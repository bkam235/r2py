# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:x
x = {"a": 1, "b": 2}

# When indexing an element that doesn't exist `[[` sometimes returns NULL:
# R's x[["y"]] returns NULL
try:
    print(x["y"])
except KeyError:
    print("NULL")

# and sometimes errors:
# try(x[[3]])
# r2py:entity:try
try:
    # In R, lists can be indexed by position. Python dicts cannot.
    # We simulate the R list indexing error here.
    x_list = list(x.values())
    print(x_list[2]) # Index 3 in R is index 2 in Python
except (IndexError, KeyError):
    pass

# chuck() consistently errors:
# r2py:entity:try_1
def chuck(d, key):
    """
    Mimics purrr::chuck.
    Unlike [[, chuck() always errors if the element is missing.
    """
    if isinstance(d, dict):
        return d[key]
    elif isinstance(d, (list, tuple)):
        # R indices are 1-based
        return d[key - 1]
    else:
        raise TypeError("Object is not indexable")

# try(chuck(x, "y"))
try:
    chuck(x, "y")
except Exception as e:
    # R's try() prints the error if it occurs
    print(e)

# try(chuck(x, 3))
# r2py:entity:try_2
try:
    chuck(x, 3)
except Exception as e:
    print(e)