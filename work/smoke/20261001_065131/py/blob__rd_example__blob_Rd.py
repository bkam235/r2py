# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np
import pandas as pd

# r2py:entity:new_blob
class Blob:
    def __init__(self, data):
        # Ensure data is a list of bytes
        if isinstance(data, (bytes, bytearray)):
            self.data = [data]
        elif isinstance(data, list):
            self.data = [bytes(item) if item is not None else None for item in data]
        elif isinstance(data, (str, np.ndarray, pd.Series)):
            # handle as.blob cases where input might be a vector of strings
            self.data = [bytes(item) if isinstance(item, str) else bytes(item) for item in data]
        else:
            self.data = data

    def __repr__(self):
        # R prints:
        # <blob[2]>
        # [1] blob[12 B] blob[5 B]
        header = f"<blob[{len(self.data)}]> "
        elements = " ".join([f"blob[{len(x)} B]" if x is not None else "blob[0 B]" for x in self.data])
        return f"{header}\n[1] {elements}"

def new_blob(x=None):
    if x is None:
        return Blob([])
    return Blob(x)

# r2py:entity:blob
def blob(*args):
    # R's blob(...) uses list2(...) which captures all arguments into a list
    return new_blob(list(args))

# r2py:entity:as.blob
def as_blob(x):
    # Implementation of as_blob logic from R source
    if isinstance(x, (list, tuple, np.ndarray, pd.Series)):
        return Blob(x)
    return Blob([x])

def as_blob_deprecated(x, *args, **kwargs):
    # Maps to as.blob in R
    return as_blob(x)

# x1 <- charToRaw("Good morning")
# r2py:entity:x1
x1 = "Good morning".encode('utf-8')

# x2 <- as.raw(c(0x48, 0x65, 0x6c, 0x6c, 0x6f))
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# new_blob(list(x1, x2))
# r2py:entity:new_blob
new_blob_res = new_blob([x1, x2])
print(new_blob_res)

# blob(x1, x2)
# r2py:entity:blob
blob_res = blob(x1, x2)
print(blob_res)

# as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
as_blob_res = as_blob(["Good morning".encode('utf-8'), "Good evening".encode('utf-8')])
print(as_blob_res)