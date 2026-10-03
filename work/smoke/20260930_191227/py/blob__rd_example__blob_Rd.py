# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np

# r2py:entity:new_blob
class Blob:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        # R prints:
        # <blob[n]>
        # [1] blob[size1 B] blob[size2 B]
        n = len(self.data)
        header = f"<blob[{n}]>"
        elements = " ".join([f"blob[{len(x)} B]" for x in self.data])
        return f"{header}\n[1] {elements}"

def is_raw(x):
    return isinstance(x, (bytes, bytearray))

def is_raw_list(x):
    if not isinstance(x, list):
        return False
    for item in x:
        if item is not None and not is_raw(item):
            return False
    return True

def validate_blob(x):
    if not is_raw_list(x):
        raise TypeError("x must be a list of raw vectors")

def new_blob(x=None):
    if x is None:
        x = []
    return Blob(list(x))

# r2py:entity:blob
def blob(*args):
    x = list(args)
    validate_blob(x)
    return new_blob(x)

# r2py:entity:as.blob
def as_blob(x, *args, **kwargs):
    # R's as.blob calls as_blob, which uses vec_cast.
    # For strings, it converts them to raw vectors.
    if isinstance(x, (list, tuple, np.ndarray)):
        converted = []
        for item in x:
            if isinstance(item, str):
                converted.append(item.encode('utf-8'))
            else:
                converted.append(item)
        return new_blob(converted)
    elif isinstance(x, str):
        return new_blob([x.encode('utf-8')])
    else:
        return new_blob([x])

# r2py:entity:x1
x1 = "Good morning".encode('utf-8')
# r2py:entity:x2
x2 = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

# R script execution
# new_blob(list(x1, x2))
# r2py:entity:new_blob
res_new_blob = new_blob([x1, x2])
print(res_new_blob)

# blob(x1, x2)
# r2py:entity:blob
res_blob_val = blob(x1, x2)
print(res_blob_val)

# as.blob(c("Good morning", "Good evening"))
# r2py:entity:as.blob
res_as_blob = as_blob(["Good morning", "Good evening"])
print(res_as_blob)