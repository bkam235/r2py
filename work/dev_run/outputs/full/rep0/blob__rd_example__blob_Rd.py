# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# R's blob class is a list of raw vectors with a specific print method.
class Blob(list):
    def __repr__(self):
        # R prints: 
        #   <blob[n]>
        # [1] blob[size1 B] blob[size2 B] ...
        n = len(self)
        header = f" <blob[{n}]>"
        elements = " ".join([f"blob[{len(x)} B]" for x in self])
        return f"{header}\n[1] {elements}"

# suppressPackageStartupMessages(library(blob))
# library(blob)
pass

# r2py:entity:new_blob
def new_blob(x=None):
    """Equivalent to R's new_blob, which creates a 'blob' object from a list of raw vectors."""
    if x is None:
        return Blob([])
    return Blob(list(x))

# r2py:entity:blob
def blob(*args):
    """Equivalent to R's blob(...) constructor."""
    x = list(args)
    # validate_blob logic: check if it is a list of raw vectors (bytes in Python)
    for item in x:
        if item is not None and not isinstance(item, (bytes, bytearray)):
            raise TypeError("must be a list of raw vectors")
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x):
    """Equivalent to R's as_blob coercion."""
    if isinstance(x, (list, np.ndarray)):
        return new_blob([i.encode('utf-8') if isinstance(i, str) else i for i in x])
    return new_blob([x.encode('utf-8') if isinstance(x, str) else x])

def as_blob_default(x, *args, **kwargs):
    """S3 method for as.blob."""
    return as_blob(x)

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
# r2py:entity:new_blob
res_new_blob = new_blob([x1, x2])
print(res_new_blob)

# blob(x1, x2)
# r2py:entity:blob
res_blob = blob(x1, x2)
print(res_blob)

# as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
res_as_blob = as_blob_default(["Good morning", "Good evening"])
print(res_as_blob)