# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# purrr is not available, implementing chuck logic manually as per R function source

# library(purrr) is handled by the implementation of chuck

# r2py:entity:x
x = {"a": 1, "b": 2}

# r2py:entity:try_1
def chuck(x, key):
    # R's chuck() is a strict version of pluck()
    # It must error if the key is missing
    if key not in x:
        raise KeyError(f"key {key} not found")
    return x[key]

# When indexing an element that doesn't exist `[[` sometimes returns NULL:
# In R, x[["y"]] for a list returns NULL without error.
# Python dict.get() mimics this behavior.
res_y = x.get("y")
print(res_y) if res_y is not None else print("NULL")

# and sometimes errors:
# r2py:entity:try
try:
    # R: x[[3]] on a list with named elements often errors if index is out of bounds
    # Python dicts error on integer keys if they don't exist
    val = x[3]
except Exception:
    pass

# chuck() consistently errors:
# r2py:entity:try_1
try:
    chuck(x, "y")
except Exception:
    pass

# r2py:entity:try_2
try:
    chuck(x, 3)
except Exception:
    pass